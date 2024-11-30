from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from services.test_data_service import TestDataService
from database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/test_data") # 예약 목록 조회 페이지로 이동
async def test_data(request: Request, db: Session = Depends(get_db)):
    test_data_service = TestDataService(db)

    test_data_results = [
        test_data_service.create_test_data('그렙'),
        test_data_service.create_test_data('테슬라'),
        test_data_service.create_test_data('애플'),
    ]

    # 결과 메시지를 포함한 응답 반환
    return templates.TemplateResponse("test_data_view.html", {"request": request, "results": test_data_results})