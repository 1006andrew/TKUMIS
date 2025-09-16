# src/scripts/add_skin_test_field.py
from src.firebase.init_firebase import initialize

def add_skin_field():
    db = initialize()   # ✅ 初始化並取得 Firestore client
    clients_ref = db.collection("clients")
    docs = clients_ref.stream()

    for doc in docs:
        client_ref = clients_ref.document(doc.id)
        client_ref.set({
            "skin_test_result": {}
        }, merge=True)
        print(f"Updated client {doc.id}")

if __name__ == "__main__":
    add_skin_field()
