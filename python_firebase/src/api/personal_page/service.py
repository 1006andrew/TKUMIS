from typing import List, Optional, Dict, Any
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

from src.firebase.init_firebase import get_db

# # 初始化 Firestore Client
# def get_db():
#     if not firebase_admin._apps:
#         print("[DEBUG] Initializing Firebase Admin...")
#         try:
#             cred = credentials.Certificate("serviceAccountKey.json")  # 請確認路徑正確
#             firebase_admin.initialize_app(cred)
#             print("[DEBUG] Firebase Admin initialized successfully.")
#         except Exception as e:
#             print(f"[ERROR] Firebase initialization failed: {e}")
#             raise
#     else:
#         print("[DEBUG] Firebase Admin already initialized.")
#     return firestore.client()


def get_profile(user_id: str) -> Optional[Dict[str, Any]]:
    print(f"[DEBUG] get_profile called with user_id={user_id}")
    db = get_db()

    try:
        doc = db.collection('clients').document(user_id).get()
        if not doc.exists:
            print(f"[WARN] No client document found for user_id={user_id}")
            return None

        data = doc.to_dict() or {}
        print(f"[DEBUG] Raw client data: {data}")

        # ✅ 預設膚質描述
        skin_desc_list = []

        skin_test = data.get("skin_test_result", {})

        # 轉換 oil_label
        oil_label = skin_test.get("oil_label")
        if oil_label == "Oil_yes":
            skin_desc_list.append("油性肌膚 : 是")
        elif oil_label == "Oil_no":
            skin_desc_list.append("油性肌膚 : 否")

        # 轉換 sensi_label
        sensi_label = skin_test.get("sensi_label")
        if sensi_label == "Sensi_yes":
            skin_desc_list.append("敏感肌膚 : 是")
        elif sensi_label == "Sensi_no":
            skin_desc_list.append("敏感肌膚 : 否")

        # 合併為一個字串顯示
        skin_desc = "；".join(skin_desc_list) if skin_desc_list else None

        profile = {
            'id': doc.id,
            'displayName': data.get('name') or '使用者',
            'email': data.get('email'),
            'phone': data.get('phone'),
            'avatarUrl': data.get('photoURL') or data.get('avatarUrl'),
            'points': int(data.get('points') or 0),
            'bookingsCount': int(data.get('bookingsCount') or 0),
            'skinType': skin_desc,   # ✅ 改成轉換後的中文描述
            'lastVisitAt': (
                data.get('updated_at').isoformat()
                if isinstance(data.get('updated_at'), datetime)
                else data.get('updated_at')
            ),
        }

        print(f"[DEBUG] Parsed profile: {profile}")
        return profile
    except Exception as e:
        print(f"[ERROR] get_profile failed: {e}")
        raise


def list_records(user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
    print(f"[DEBUG] list_records called with user_id={user_id}, limit={limit}")
    db = get_db()

    try:
        q = (
            db.collection('records')
            .where('userId', '==', user_id)
            .order_by('createdAt', direction=firestore.Query.DESCENDING)
            .limit(limit)
        )
        items = []
        for doc in q.stream():
            data = doc.to_dict() or {}
            print(f"[DEBUG] Record {doc.id}: {data}")

            created = data.get('createdAt')
            if isinstance(created, datetime):
                created = created.isoformat()

            items.append({
                'id': doc.id,
                'title': data.get('title') or '—',
                'type': data.get('type') or 'note',
                'createdAt': created or datetime.utcnow().isoformat(),
                'amount': data.get('amount'),
                'status': data.get('status'),
            })
        print(f"[DEBUG] Total records fetched: {len(items)}")
        return items
    except Exception as e:
        print(f"[ERROR] list_records failed: {e}")
        raise
