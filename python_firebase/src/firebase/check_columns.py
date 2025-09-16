import firebase_admin
from firebase_admin import credentials, firestore
from init_firebase import get_db

db = get_db()

schema = {}

for coll in db.collections():
    coll_name = coll.id
    schema[coll_name] = {}

    for doc in coll.stream():
        data = doc.to_dict()
        for field, value in data.items():
            # 如果這個欄位第一次出現，初始化
            if field not in schema[coll_name]:
                schema[coll_name][field] = {
                    "types": set(),
                    "sample": value
                }
            # 累積型別
            schema[coll_name][field]["types"].add(type(value).__name__)

# 輸出結果
for coll_name, fields in schema.items():
    print(f"Collection: {coll_name}")
    for field, info in fields.items():
        types = ", ".join(info["types"])
        sample = info["sample"]
        print(f"  - {field} ({types}) e.g. {sample}")
    print()