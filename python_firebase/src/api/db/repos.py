# src/api/db/repos.py
from __future__ import annotations
from typing import Optional, Dict, Any, List, Tuple
from src.firebase.firestore_service import FS  # 基礎層：通用 CRUD / 交易 / 批次

class ClientsRepo(FS):
    """
    Firestore collection: clients
    對應 MySQL `client` 表欄位：name, gender, age, username, password
    """
    col = "clients"

    def get_by_id(self, client_id: str):
        return self.get(self.col, client_id)

    def list(self, limit: int = 20, cursor_after: Optional[str] = None):
        return self.query(self.col, limit=limit, cursor_after=cursor_after)

    def create_one(self, data: Dict[str, Any], doc_id: Optional[str] = None):
        return self.create(self.col, data, doc_id)

    def update_one(self, client_id: str, data: Dict[str, Any]):
        return self.update(self.col, client_id, data)

    def delete_one(self, client_id: str):
        return self.delete(self.col, client_id)


class ProductsRepo(FS):
    """
    Firestore collection: products
    對應 MySQL `product` 表欄位：order_no, product_name, description, price_min, price_max
    """
    col = "products"

    def get_by_id(self, product_id: str):
        return self.get(self.col, product_id)

    def list(self, limit: int = 20, cursor_after: Optional[str] = None):
        return self.query(self.col, limit=limit, cursor_after=cursor_after)

    def create_one(self, data: Dict[str, Any], doc_id: Optional[str] = None):
        return self.create(self.col, data, doc_id)

    def update_one(self, product_id: str, data: Dict[str, Any]):
        return self.update(self.col, product_id, data)

    def delete_one(self, product_id: str):
        return self.delete(self.col, product_id)


class PurchaseRecordsRepo(FS):
    """
    Firestore collection: purchase_records
    對應 MySQL `user_purchase_record` 表欄位：
    client_id, product_id, order_date, quantity, amount
    """
    col = "purchase_records"

    def get_by_id(self, record_id: str):
        return self.get(self.col, record_id)

    def list_by_client(self, client_id: int, limit: int = 20, cursor_after: Optional[str] = None):
        # 常見查詢：依 client_id 篩選並依 order_date 排序（需要複合索引）
        return self.query(
            self.col,
            filters=[("client_id", "==", int(client_id))],
            order_by="order_date",
            limit=limit,
            cursor_after=cursor_after,
        )

    def create_one(self, data: Dict[str, Any], doc_id: Optional[str] = None):
        return self.create(self.col, data, doc_id)

    def update_one(self, record_id: str, data: Dict[str, Any]):
        return self.update(self.col, record_id, data)

    def delete_one(self, record_id: str):
        return self.delete(self.col, record_id)
