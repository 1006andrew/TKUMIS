import numpy as np
import joblib
import os
import tensorflow as tf
import keras
from tensorflow.keras.layers import InputLayer

from .config import MODEL_PATH_MOBILENET, MODEL_PATH_SVM, SCALER_PATH
from .preprocessing import preprocess_image_for_mobilenet
from .features import extract_glossiness_features, extract_svm_features

# ✅ 全域載入模型（程式啟動時就讀取一次）
if MODEL_PATH_MOBILENET.endswith(".keras"):
    mobilenet_model = keras.models.load_model(MODEL_PATH_MOBILENET, compile=False)
elif MODEL_PATH_MOBILENET.endswith(".h5"):
    mobilenet_model = tf.keras.models.load_model(
        MODEL_PATH_MOBILENET, compile=False, custom_objects={"InputLayer": InputLayer}
    )
else:
    raise ValueError("Unsupported model format")

svm_model = joblib.load(MODEL_PATH_SVM)
scaler = joblib.load(SCALER_PATH)


def test_single_image(image_path: str) -> dict | None:
    try:
        # 前處理
        img_for_mobilenet = preprocess_image_for_mobilenet(image_path)
        glossiness_features = extract_glossiness_features(image_path)
        svm_features = extract_svm_features(image_path)

        if svm_features is None:
            return {"error": "Failed to extract SVM features"}

        # MobileNet 預測
        img_batch = np.expand_dims(img_for_mobilenet, axis=0)
        glossiness_batch = np.expand_dims(glossiness_features, axis=0)
        oil_prob = mobilenet_model.predict([img_batch, glossiness_batch])[0][0]
        oil_label = "Oil_yes" if oil_prob > 0.5 else "Oil_no"

        # SVM 預測
        svm_features_scaled = scaler.transform([svm_features])
        sensi_prob = svm_model.predict_proba(svm_features_scaled)[0][1]
        sensi_label = "Sensi_yes" if sensi_prob > 0.5 else "Sensi_no"

        result = {
            "oil_prob": float(oil_prob),
            "oil_label": oil_label,
            "sensi_prob": float(sensi_prob),
            "sensi_label": sensi_label,
        }

        print("[CMD Debug] Analysis Result:", result)
        return result

    finally:
        # 🔥 用完就刪檔，避免下次讀到舊圖
        if os.path.exists(image_path):
            os.remove(image_path)
