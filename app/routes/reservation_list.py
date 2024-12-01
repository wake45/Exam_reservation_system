from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

from services.reservation_list_service import ReservationListService
from database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/reservation_list") # 예약 목록 조회 페이지로 이동
async def reservation_list(request: Request, id: int, db: Session = Depends(get_db)):

    # 서비스 호출
    reservation_list_service = ReservationListService(db)  # DB 세션을 전달하여 서비스 인스턴스 생성
    reservationListResult = reservation_list_service.select_reservationList(id)

    return templates.TemplateResponse("reservation_list_view.html", {"request": request, "reservationList": reservationListResult, "id": id})