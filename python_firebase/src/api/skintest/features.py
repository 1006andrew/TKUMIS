import cv2
import numpy as np
from skimage.feature import graycomatrix, graycoprops, local_binary_pattern
from .config import IMG_SIZE

def extract_glossiness_features(image_path: str) -> np.ndarray:
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Failed to load image: {image_path}")

    h, w = img.shape[:2]
    t_zone = img[int(h*0.2):int(h*0.6), int(w*0.3):int(w*0.7)]
    t_zone = cv2.resize(t_zone, IMG_SIZE)

    img_hsv = cv2.cvtColor(t_zone, cv2.COLOR_BGR2HSV)
    glossiness_mean = np.mean(img_hsv[:, :, 2]) / 255.0
    glossiness_high = (img_hsv[:, :, 2] > 150).sum() / img_hsv.size

    img_gray = cv2.cvtColor(t_zone, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(img_gray, 50, 150)
    pore_density = np.sum(edges) / img.size

    return np.array([glossiness_mean, glossiness_high, pore_density], dtype=np.float32)


def extract_svm_features(image_path: str) -> np.ndarray | None:
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Failed to load image: {image_path}")

    h, w = img.shape[:2]
    t_zone = img[int(h*0.2):int(h*0.6), int(w*0.3):int(w*0.7)]
    t_zone = cv2.resize(t_zone, IMG_SIZE)

    try:
        # 紅色區域比例
        hsv = cv2.cvtColor(t_zone, cv2.COLOR_BGR2HSV)
        lower_red, upper_red = np.array([0, 50, 50]), np.array([30, 255, 255])
        mask = cv2.inRange(hsv, lower_red, upper_red)
        red_ratio = np.sum(mask) / (mask.shape[0] * mask.shape[1] * 255)

        # 邊緣密度
        gray = cv2.cvtColor(t_zone, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        edge_density = np.sum(edges) / (edges.shape[0] * edges.shape[1] * 255)

        # GLCM 紋理特徵
        glcm = graycomatrix(gray, distances=[5], angles=[0], levels=256, symmetric=True, normed=True)
        contrast = graycoprops(glcm, 'contrast')[0, 0]
        correlation = graycoprops(glcm, 'correlation')[0, 0]

        # 斑點檢測
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        spot_count = len([c for c in contours if cv2.contourArea(c) > 10])

        # LBP 特徵
        radius, n_points = 3, 8 * 3
        lbp = local_binary_pattern(gray, n_points, radius, method='uniform')
        lbp_hist, _ = np.histogram(lbp.ravel(), bins=np.arange(0, n_points + 3), density=True)
        lbp_mean, lbp_std = np.mean(lbp_hist), np.std(lbp_hist)

        # 顏色直方圖 (48 維)
        color_hist = []
        for channel in range(t_zone.shape[2]):
            hist = cv2.calcHist([t_zone], [channel], None, [16], [0, 256])
            hist = hist.flatten() / np.sum(hist)
            color_hist.extend(hist[:16])
        color_hist = color_hist[:48]

        # 區域特徵 (每區 2 維 × 4 區 = 8 維)
        h, w = t_zone.shape[:2]
        regions = [
            t_zone[0:h//2, 0:w//2],
            t_zone[0:h//2, w//2:],
            t_zone[h//2:, 0:w//2],
            t_zone[h//2:, w//2:]
        ]
        regional_features = []
        for region in regions:
            hsv_region = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)
            mask_region = cv2.inRange(hsv_region, lower_red, upper_red)
            red_ratio_region = np.sum(mask_region) / (mask_region.shape[0] * mask_region.shape[1] * 255)
            gray_region = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
            _, thresh_region = cv2.threshold(gray_region, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            contours_region, _ = cv2.findContours(thresh_region, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            spot_count_region = len([c for c in contours_region if cv2.contourArea(c) > 10])
            regional_features.extend([red_ratio_region, spot_count_region])

        # 最後組合所有特徵 → 共 63 維
        return np.array(
            [red_ratio, edge_density, contrast, correlation, spot_count, lbp_mean, lbp_std]
            + color_hist
            + regional_features,
            dtype=np.float32
        )

    except Exception as e:
        print(f"Feature extraction failed for image: {str(e)}")
        return None
