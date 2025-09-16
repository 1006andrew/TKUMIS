from pydantic import BaseModel
from typing import Optional, Literal

# ✅ 使用更具體的名稱，避免和 api.profile 重疊
class PersonalPageProfile(BaseModel):
    id: str
    displayName: str
    email: Optional[str] = None
    phone: Optional[str] = None
    avatarUrl: Optional[str] = None
    points: Optional[int] = 0
    bookingsCount: Optional[int] = 0
    skinType: Optional[str] = None
    lastVisitAt: Optional[str] = None  # ISO string

class PersonalPageRecordItem(BaseModel):
    id: str
    title: str
    type: Literal['booking', 'purchase', 'skintest', 'note']
    createdAt: str
    amount: Optional[float] = None
    status: Optional[str] = None
