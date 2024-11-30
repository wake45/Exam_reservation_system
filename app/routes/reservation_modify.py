from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from datetime import datetime

from services.reservation_modify_service import ReservationModifyService
from database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/reservation_modify") # 예약 내역 수정
async def reservation_modify(
    id: int = Form(...),
    exam_name: str = Form(...),
    exam_start_date: str = Form(...),
    exam_end_date: str = Form(...),
    exam_participants: int = Form(...),
    db: Session = Depends(get_db)
):

    print(id)

    # 날짜를 datetime 객체로 변환
    exam_start = datetime.strptime(exam_start_date, "%Y%m%d %H%M%S")
    exam_end = datetime.strptime(exam_end_date, "%Y%m%d %H%M%S")

    # 서비스 호출
    reservation_modify_service = ReservationModifyService(db)  # DB 세션을 전달하여 서비스 인스턴스 생성
    result = reservation_modify_service.modify_reservation(id, exam_name, exam_start, exam_end, exam_participants)

    return result