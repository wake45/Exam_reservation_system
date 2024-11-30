from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

from services.reservation_confirm_service import ReservationConfirmService
from database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/reservation_confirm") # 예약 인원 추가
async def reservation_confirm(
    id: int = Form(...),
    db: Session = Depends(get_db)
):

    print(id)

    # 서비스 호출
    reservation_confirm_service = ReservationConfirmService(db)  # DB 세션을 전달하여 서비스 인스턴스 생성
    result = reservation_confirm_service.confirm_reservation(id)

    return result