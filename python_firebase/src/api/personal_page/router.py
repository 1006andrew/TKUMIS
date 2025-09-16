from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from .schemas import PersonalPageProfile, PersonalPageRecordItem

from .service import get_profile, list_records

# ✅ 改為 personal_page
router = APIRouter(prefix="/api/personal_page", tags=["personal_page"])

def _resolve_user_id(user_id: Optional[str]) -> str:
    # 這裡先簡化：若沒傳 user_id，就用 demo 帳號（或從 token 取）
    return user_id or "demo-user"

@router.get("/me", response_model=PersonalPageProfile)
def read_me(user_id: Optional[str] = Query(default=None)):
    uid = _resolve_user_id(user_id)
    profile = get_profile(uid)
    if not profile:
        raise HTTPException(404, "Personal Page profile not found")
    return profile

@router.get("/me/records", response_model=List[PersonalPageRecordItem])
def read_my_records(user_id: Optional[str] = Query(default=None), limit: int = 10):
    uid = _resolve_user_id(user_id)
    return list_records(uid, limit=limit)
