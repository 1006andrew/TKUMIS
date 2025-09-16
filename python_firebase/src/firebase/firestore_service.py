# src/firebase/firestore_service.py
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from firebase_admin import firestore
from google.cloud.firestore_v1 import FieldFilter  # for typed where()
from .init_firebase import get_db


class FS:
    """
    通用 Firestore 存取層：
    - get/create/update/delete
    - query（支援 filters、排序、簡單游標分頁）
    使用方式：在你的 repos 繼承 FS，設定 self.col = "<collection_name>"
    """

    def __init__(self, db: Optional[firestore.Client] = None):
        self.db: firestore.Client = db or get_db()

    # ---------- 基本 CRUD ----------
    def get(self, col: str, doc_id: str) -> Optional[Dict[str, Any]]:
        snap = self.db.collection(col).document(str(doc_id)).get()
        return ({**snap.to_dict(), "id": snap.id} if snap.exists else None)

    def create(
        self,
        col: str,
        data: Dict[str, Any],
        doc_id: Optional[str] = None,
    ) -> str:
        now = datetime.utcnow()
        payload = {**data, "updated_at": now}
        payload.setdefault("created_at", now)
        ref = (
            self.db.collection(col).document(str(doc_id))
            if doc_id
            else self.db.collection(col).document()
        )
        # merge=True 讓重跑 migration 可覆蓋同名欄位、保留未提到欄位
        ref.set(payload, merge=True)
        return ref.id

    def update(self, col: str, doc_id: str, data: Dict[str, Any]) -> None:
        payload = {**data, "updated_at": datetime.utcnow()}
        self.db.collection(col).document(str(doc_id)).set(payload, merge=True)

    def delete(self, col: str, doc_id: str) -> None:
        self.db.collection(col).document(str(doc_id)).delete()

    # ---------- 查詢 / 分頁 ----------
    def query(
        self,
        col: str,
        filters: Optional[List[Tuple[str, str, Any]]] = None,
        order_by: Optional[str] = None,
        direction: str = "ASC",
        limit: int = 20,
        cursor_after: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        filters: [(field, op, value)], 例如 [("client_id","==",123)]
        order_by: 例如 "order_date"（與 filters 欄位常需要複合索引）
        direction: "ASC" | "DESC"
        cursor_after: 上一頁最後一筆的 doc id（簡易游標）
        """
        q = self.db.collection(col)
        if filters:
            for field, op, val in filters:
                q = q.where(filter=FieldFilter(field, op, val))

        if order_by:
            q = q.order_by(
                order_by,
                direction=firestore.Query.DESCENDING
                if direction.upper() == "DESC"
                else firestore.Query.ASCENDING,
            )

        if cursor_after:
            after_snap = self.db.collection(col).document(cursor_after).get()
            if after_snap.exists:
                # 若想更精準，可改用 order_by 欄位值作 start_after
                q = q.start_after(after_snap)

        snaps = q.limit(limit).stream()
        items: List[Dict[str, Any]] = []
        last_id: Optional[str] = None
        for s in snaps:
            d = s.to_dict() or {}
            d["id"] = s.id
            items.append(d)
            last_id = s.id

        return {"items": items, "next_cursor": last_id}


# ------------------------------------------------------------
# 相容層：保留你原本的函式呼叫風格（可逐步移除）
# ------------------------------------------------------------
_db = get_db()

def create_document(collection: str, doc_id: str, data: dict) -> bool:
    """
    舊版相容：寫入/覆蓋單一文件
    """
    ref = _db.collection(collection).document(str(doc_id))
    ref.set(data, merge=True)  # 與 FS.create 行為一致（merge=True）
    return True


def get_document(collection: str, doc_id: str):
    """
    舊版相容：讀單一文件
    """
    ref = _db.collection(collection).document(str(doc_id))
    doc = ref.get()
    return (doc.to_dict() if doc.exists else None)
