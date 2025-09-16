import os

# 圖像大小
IMG_SIZE = (224, 224)

# 模型與資源路徑 (固定在 skintest/model 資料夾)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "model")

MODEL_PATH_MOBILENET = os.path.join(MODEL_DIR, "mobilenet_oily_skin_with_glossiness_fixed.keras")
MODEL_PATH_SVM = os.path.join(MODEL_DIR, "skin_svm_model.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")
