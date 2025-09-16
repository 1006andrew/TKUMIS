from fastapi import APIRouter, UploadFile, File, HTTPException
import tempfile
import uuid
from .predictor import test_single_image
from pydantic import BaseModel
from src.firebase.init_firebase import initialize

router = APIRouter(prefix="/skintest", tags=["Skin Test"])

# ✅ 初始化 Firestore
db = initialize()

@router.post("/analyze")
async def analyze_skin(file: UploadFile = File(...)):
    # 🔥 建立唯一檔名，避免覆蓋舊檔
    unique_name = f"{uuid.uuid4()}.jpg"
    with tempfile.NamedTemporaryFile(delete=False, suffix=unique_name) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    # 呼叫 predictor
    result = test_single_image(tmp_path)

    return result


# ===============================
# ✅ 新增：寫入膚質結果到 Firestore
# ===============================

class SaveSkinResultIn(BaseModel):
    client_id: str
    oil_label: str
    oil_prob: float
    sensi_label: str
    sensi_prob: float

@router.post("/save_result")
async def save_result(data: SaveSkinResultIn):
    try:
        client_ref = db.collection("clients").document(data.client_id)
        client_ref.set({
            "skin_test_result": {
                "oil_label": data.oil_label,
                "oil_prob": data.oil_prob,
                "sensi_label": data.sensi_label,
                "sensi_prob": data.sensi_prob,
            }
        }, merge=True)

        return {"ok": True, "message": f"Skin test result saved for {data.client_id}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

