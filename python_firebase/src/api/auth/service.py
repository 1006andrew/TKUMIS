# src/api/auth/service.py
import bcrypt
from src.api.auth.repos import UsersRepo


class AuthService:
    def __init__(self):
        self.repo = UsersRepo()

    def register(self, name: str, email: str, password: str):
        # 檢查是否已存在相同 email
        exists = self.repo.get_by_email(email)
        if exists:
            return {"ok": False, "message": "此 Email 已被註冊，請改用其他 Email"}

        # 雜湊密碼
        pwd_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        # 建立使用者文件
        self.repo.create_user(
            name=name,
            email=email,
            password_hash=pwd_hash,
            provider="password"
        )

        return {"ok": True, "message": "註冊成功！歡迎加入", "redirect": "/Naitre-Beauty/"}

    def login(self, email: str, password: str):
        user = self.repo.get_by_email(email)
        if not user or not user.get("password_hash"):
            return {"ok": False, "message": "帳號或密碼不正確"}

        # 驗證密碼
        ok = bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8"))
        if not ok:
            return {"ok": False, "message": "帳號或密碼不正確"}

        # 更新最後登入時間
        self.repo.update_last_login(user["id"])

        return {"ok": True, "message": "登入成功！", "redirect": "/Naitre-Beauty/"}
