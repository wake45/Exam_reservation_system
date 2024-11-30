from fastapi import APIRouter, Form, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from services.reservation_available_service import ReservationAvailableService
from database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/reservation_new") # 신규예약 페이지로 이동
async def reservation_new(request: Request, id: int, db: Session = Depends(get_db)):

    # 서비스 호출
    reservation_available_service = ReservationAvailableService(db)  # DB 세션을 전달하여 서비스 인스턴스 생성
    result = reservation_available_service.select_available_reservation()

    return templates.TemplateResponse("reservation_new_view.html", {"request": request, "id": id, "reservations": result})