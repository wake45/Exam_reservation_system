from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

from services.reservation_add_service import ReservationAddService
from database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/reservation_add") # 예약 인원 추가
async def reservation_add(
    id: int = Form(...),
    add_exam_participants: int = Form(...),
    db: Session = Depends(get_db)
):

    print(id)

    # 서비스 호출
    reservation_add_service = ReservationAddService(db)  # DB 세션을 전달하여 서비스 인스턴스 생성
    result = reservation_add_service.add_reservation(id, add_exam_participants)

    return result