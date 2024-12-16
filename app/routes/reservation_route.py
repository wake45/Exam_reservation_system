from fastapi import APIRouter, Depends, Form, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from datetime import datetime

from services.reservation_service import ReservationAddService, ReservationAvailableService, ReservationConfirmService, ReservationDeleteService, ReservationListService, ReservationModifyService, ReservationNewService
from database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# 신규 예약 등록
@router.post("/reservation_new")
async def reservation(
    user_id: int = Form(...),
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

    # 응시 인원 형식 검사
    try:
        exam_participants = int(exam_participants)  # 문자열을 정수로 변환
        if exam_participants < 1:
            return {"error": "응시 인원은 1명 이상의 정수여야 합니다."}
    except ValueError:
        return {"error": "응시 인원은 1명 이상의 정수여야 합니다."}

    # 서비스 호출
    reservation_new_service = ReservationNewService(db)  # DB 세션을 전달하여 서비스 인스턴스 생성
    result = reservation_new_service.create_reservation(exam_name,exam_start,exam_end,exam_participants,user_id)

    return result


# 예약되어있는 리스트 조회(신규예약 페이지로 이동)
@router.get("/reservation_available") 
async def reservation_new(request: Request, id: int, db: Session = Depends(get_db)):

    # 서비스 호출
    reservation_available_service = ReservationAvailableService(db)  # DB 세션을 전달하여 서비스 인스턴스 생성
    result = reservation_available_service.select_available_reservation()

    return templates.TemplateResponse("reservation_new_view.html", {"request": request, "id": id, "reservations": result})


# 예약 목록 조회 페이지로 이동
@router.get("/reservation_list") 
async def reservation_list(request: Request, id: int, db: Session = Depends(get_db)):

    # 서비스 호출
    reservation_list_service = ReservationListService(db)  # DB 세션을 전달하여 서비스 인스턴스 생성
    reservationListResult = reservation_list_service.select_reservationList(id)

    return templates.TemplateResponse("reservation_list_view.html", {"request": request, "reservationList": reservationListResult, "id": id})


# 예약 내역 수정
@router.put("/reservation_modify")
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

# 예약 삭제
@router.delete("/reservation_delete")
async def reservation_delete(
    id: int = Form(...),
    db: Session = Depends(get_db)
):
    
    # 서비스 호출
    reservation_delete_service = ReservationDeleteService(db)  # DB 세션을 전달하여 서비스 인스턴스 생성
    result = reservation_delete_service.delete_reservation(id)

    return result

# 예약 확정
@router.patch("/reservation_confirm")
async def reservation_confirm(
    id: int = Form(...),
    db: Session = Depends(get_db)
):

    # 서비스 호출
    reservation_confirm_service = ReservationConfirmService(db)  # DB 세션을 전달하여 서비스 인스턴스 생성
    result = reservation_confirm_service.confirm_reservation(id)

    return result


# 예약 인원 추가
@router.patch("/reservation_add") 
async def reservation_add(
    id: int = Form(...),
    add_exam_participants: str = Form(...),
    db: Session = Depends(get_db)
):

    try:
        add_exam_participants = int(add_exam_participants)  # 문자열을 정수로 변환
        if add_exam_participants < 1:
            return {"error": "응시 인원은 1명 이상의 정수여야 합니다."}
    except ValueError:
        return {"error": "응시 인원은 1명 이상의 정수여야 합니다."}

    # 서비스 호출
    reservation_add_service = ReservationAddService(db)  # DB 세션을 전달하여 서비스 인스턴스 생성
    result = reservation_add_service.add_reservation(id, add_exam_participants)

    return result