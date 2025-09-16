from fastapi import APIRouter, HTTPException
from google.cloud import firestore

from src.firebase.init_firebase import get_db
from .schemas import BookingCreate, BookingResponse
from datetime import datetime
import uuid

router = APIRouter(prefix="/api/bookings", tags=["bookings"])

@router.post("", response_model=BookingResponse)
def create_booking(booking: BookingCreate):
    try:
        db = get_db()
        booking_id = str(uuid.uuid4())
        doc_ref = db.collection("bookings").document(booking_id)

        data = {
            "userId": booking.userId,
            "treatment": booking.treatment,
            "date": booking.date,
            "time": booking.time,
            "createdAt": booking.createdAt or datetime.utcnow().isoformat()
        }

        doc_ref.set(data)

        return BookingResponse(id=booking_id, **data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
