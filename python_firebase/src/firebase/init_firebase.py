# src/firebase/init_firebase.py

from __future__ import annotations
import firebase_admin
from firebase_admin import credentials, firestore
from functools import lru_cache

@lru_cache
def get_db() -> firestore.Client:
    """
    初始化並回傳 Firestore Client。
    - 只使用 config/firebase_cred.json 進行初始化
    """
    if not firebase_admin._apps:
        cred = credentials.Certificate("config/firebase_cred.json")
        firebase_admin.initialize_app(cred)
    return firestore.client()

# 與舊程式碼相容：提供 initialize()
def initialize() -> firestore.Client:
    return get_db()