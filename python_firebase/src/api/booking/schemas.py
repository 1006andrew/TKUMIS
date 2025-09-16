from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BookingCreate(BaseModel):
    userId: str
    treatment: str
    date: str  # YYYY-MM-DD
    time: str  # HH:mm
    createdAt: Optional[datetime] = None

class BookingResponse(BookingCreate):
    id: str
