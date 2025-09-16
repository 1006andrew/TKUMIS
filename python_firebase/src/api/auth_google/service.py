from fastapi import HTTPException
from firebase_admin import auth

def verify_google_token(id_token: str):
    """
    驗證從前端傳來的 Google ID Token
    """
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token["uid"]
        email = decoded_token.get("email")
        name = decoded_token.get("name", "")
        picture = decoded_token.get("picture", "")
        return {
            "uid": uid,
            "email": email,
            "name": name,
            "picture": picture
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
