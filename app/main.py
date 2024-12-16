from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from routes import reservation_route, test_data, login
from database import engine, Base

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.include_router(login.router)
app.include_router(test_data.router)
app.include_router(reservation_route.router)

# 테이블 생성 함수
def create_tables():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

# 애플리케이션이 시작될 때 테이블 생성
@app.on_event("startup")
async def startup_event():
    create_tables()

@app.get("/", response_class=HTMLResponse)
async def login_form(request: Request): #로그인 페이지로 이동
    return templates.TemplateResponse("login_view.html", {"request": request})