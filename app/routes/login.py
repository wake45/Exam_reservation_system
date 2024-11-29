from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/main") # 메뉴 선택 페이지로 이동
async def login(request: Request, id: int):
    if id ==  999:
        name = "관리자"
    elif id == 1:
        name = "그렙"
    elif id == 2:
        name = "테슬라"
    elif id == 3:
        name = "애플"
    else:
        name = ""
    return templates.TemplateResponse("main_view.html", {"request": request, "name": name, "id": id})