from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

from services.reservation_delete_service import ReservationDeleteService
from database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/reservation_delete") # 예약 인원 추가
async def reservation_delete(
    id: int = Form(...),
    db: Session = Depends(get_db)
):

    print(id)

    # 서비스 호출
    reservation_delete_service = ReservationDeleteService(db)  # DB 세션을 전달하여 서비스 인스턴스 생성
    result = reservation_delete_service.delete_reservation(id)

    return result