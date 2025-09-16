# firebase/admin_service.py
from firebase_admin import auth

def set_admin(uid: str):
    """給指定 UID 的使用者加上 admin 權限"""
    auth.set_custom_user_claims(uid, {"admin": True})
    return {"uid": uid, "admin": True}
