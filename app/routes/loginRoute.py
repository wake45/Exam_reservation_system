from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/main")
async def menu_from(request: Request, id: str = Form(...)):
    name = None
    if id ==  "":
        name = "관리자"
    elif id == "1":
        name = "그렙"
    elif id == "2":
        name = "테슬라"
    elif id == "3":
        name = "애플"
    else:
        name = ""
    return templates.TemplateResponse("MainView.html", {"request": request, "name": name, "id": id})