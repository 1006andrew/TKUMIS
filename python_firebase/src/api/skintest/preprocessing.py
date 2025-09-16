import cv2
import numpy as np
from .config import IMG_SIZE

def preprocess_image_for_mobilenet(image_path: str) -> np.ndarray:
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Failed to load image: {image_path}")

    # CLAHE 預處理
    img_lab = cv2.cvtColor(img, cv2.COLOR_BGR2Lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    img_lab[:, :, 0] = clahe.apply(img_lab[:, :, 0])
    img_processed = cv2.cvtColor(img_lab, cv2.COLOR_Lab2BGR)

    # 裁剪 T 字部位
    h, w = img_processed.shape[:2]
    t_zone = img_processed[int(h*0.2):int(h*0.6), int(w*0.3):int(w*0.7)]
    img_resized = cv2.resize(t_zone, IMG_SIZE)

    # 標準化
    return img_resized / 255.0
