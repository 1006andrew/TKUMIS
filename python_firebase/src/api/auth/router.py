# src/api/auth/router.py
from fastapi import APIRouter, status, Query
from fastapi.responses import JSONResponse
import firebase_admin
from firebase_admin import auth, credentials, firestore

router = APIRouter(prefix="/api/users", tags=["auth"])

# 初始化 Firebase Admin
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")  # 這裡要放你的金鑰檔
    firebase_admin.initialize_app(cred)

# Firestore 客戶端
db = firestore.client()

@router.post("/login")
def login(payload: dict):
    """
    前端會傳入 {"id_token": "..."}
    """
    id_token = payload.get("id_token")
    if not id_token:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"ok": False, "message": "缺少 id_token"}
        )

    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token["uid"]
        email = decoded_token.get("email")
        return {
            "ok": True,
            "message": "登入成功",
            "uid": uid,
            "email": email
        }
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"ok": False, "message": f"Token 驗證失敗: {str(e)}"}
        )


@router.get("/check")
def check_user(email: str = Query(..., description="要檢查的使用者 email")):
    """
    檢查 Firestore 的 users 集合中是否有該 email
    回傳 {"exists": True/False}
    """
    try:
        users_ref = db.collection("users").where("email", "==", email).limit(1).get()
        exists = len(users_ref) > 0
        return {"exists": exists}
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"ok": False, "message": f"檢查失敗: {str(e)}"}
        )
