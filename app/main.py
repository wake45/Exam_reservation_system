from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from routes import loginRoute

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.include_router(loginRoute.router)

@app.get("/", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("LoginView.html", {"request": request})