# src/api/auth/repos.py
from datetime import datetime, timezone
from typing import Optional
from google.cloud import firestore
from src.firebase.firestore_service import FS

USERS_COLLECTION = "users"

class UsersRepo:
    def __init__(self):
        self.fs: FS = FS()
        self.db: firestore.Client = self.fs.db

    def get_by_email(self, email: str) -> Optional[dict]:
        qs = self.db.collection(USERS_COLLECTION).where("email", "==", email).limit(1).stream()
        for doc in qs:
            d = doc.to_dict()
            d["id"] = doc.id
            return d
        return None

    def create_user(self, *, name: str, email: str, password_hash: str, provider: str = "password") -> str:
        now = datetime.now(timezone.utc)
        doc_ref = self.db.collection(USERS_COLLECTION).document()
        doc_ref.set({
            "name": name,
            "email": email,
            "password_hash": password_hash,
            "provider": provider,
            "created_at": now,
            "last_login_at": None,
        })
        return doc_ref.id

    def update_last_login(self, doc_id: str):
        now = datetime.now(timezone.utc)
        self.db.collection(USERS_COLLECTION).document(doc_id).update({"last_login_at": now})
