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
    exam_participants: str = Form(...),
    db: Session = Depends(get_db)
):
    # 시험명 길이 검사
    if len(exam_name) > 100:
        return {"error": "시험명은 최대 100자까지 입력할 수 있습니다."}

    # 날짜 형식 검사
    try:
        exam_start = datetime.strptime(exam_start_date, "%Y%m%d %H%M%S")
        exam_end = datetime.strptime(exam_end_date, "%Y%m%d %H%M%S")
    except ValueError:
        return {"error": "날짜 형식이 잘못되었습니다. yyyyMMdd hhmmss 형식으로 입력하세요."}

    # 응시인원 형식 검사
    try:
        exam_participants = int(exam_participants)  # 문자열을 정수로 변환
        if exam_participants < 1:
            return {"error": "응시 인원은 1명 이상의 정수여야 합니다."}
    except ValueError:
        return {"error": "응시 인원은 1명 이상의 정수여야 합니다."}

    # 서비스 호출
    reservation_modify_service = ReservationModifyService(db)  # DB 세션을 전달하여 서비스 인스턴스 생성
    result = reservation_modify_service.modify_reservation(id, exam_name, exam_start, exam_end, exam_participants)

    return result