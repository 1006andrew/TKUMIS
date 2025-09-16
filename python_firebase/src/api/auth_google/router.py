from fastapi import APIRouter, Depends, Request
from src.api.auth_google.service import verify_google_token

router = APIRouter(prefix="/auth/google", tags=["GoogleAuth"])

@router.post("/login")
async def google_login(request: Request):
    """
    前端將 Google 登入後的 id_token 傳給這裡
    """
    data = await request.json()
    id_token = data.get("id_token")
    if not id_token:
        return {"error": "Missing id_token"}

    user_info = verify_google_token(id_token)
    return {"message": "Login successful", "user": user_info}
