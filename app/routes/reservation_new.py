from fastapi import APIRouter, Form, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime

from services.reservation_new_service import ReservationNewService
from database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/reservation_new") # 신규예약 페이지로 이동
async def reservation_new(request: Request, id: int):
    return templates.TemplateResponse("reservation_new_view.html", {"request": request, "id": id})

@router.post("/reservation") # 신규 예약 등록
async def reservation(
    user_id: str = Form(...),
    exam_name: str = Form(...),
    exam_start_date: str = Form(...),
    exam_end_date: str = Form(...),
    exam_participants: int = Form(...),
    db: Session = Depends(get_db)
):

    # 날짜를 datetime 객체로 변환
    exam_start = datetime.strptime(exam_start_date, "%Y%m%d %H%M%S")
    exam_end = datetime.strptime(exam_end_date, "%Y%m%d %H%M%S")

    # 서비스 호출
    reservation_new_service = ReservationNewService(db)  # DB 세션을 전달하여 서비스 인스턴스 생성
    result = reservation_new_service.create_reservation(exam_name,exam_start,exam_end,exam_participants,user_id)
    
    print(result)

    return result