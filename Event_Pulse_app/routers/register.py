import os

from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from Event_Pulse_app.database import get_db
from Event_Pulse_app.models import User
from Event_Pulse_app.utils.password import hash_password
from sqlalchemy.future import select
from Event_Pulse_app.utils.auth_jwt import create_access_token
from dotenv import load_dotenv

load_dotenv()
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

router = APIRouter()
templates = Jinja2Templates(directory="Event_Pulse_app/templates")

@router.get("/register")
async def show_register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
async def register_user(request: Request, db: AsyncSession = Depends(get_db)):
    form = await request.form()
    name = form.get("name")
    email = form.get("email")
    password = form.get("password")
    confirm_password = form.get("confirm_password")


    if len(password) > 20 or len(password) < 5:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Пароль должен содержать 5–20 символов"
        })

    if password != confirm_password:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Пароли не совпадают"
        })

    result = await db.execute(
        select(User).where((User.name == name) | (User.email == email))
    )
    if result.scalar_one_or_none():
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Имя пользователя или email заняты"
        })

    password = password[:72]

    user = User(
        email=email,
        name=name,
        password_hash=hash_password(password)
    )

    try:
        db.add(user)
        await db.commit()
        await db.refresh(user)
    except Exception:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Произошла ошибка, повторите попытку"
        })

    token = create_access_token({"sub": str(user.id)})
    response = RedirectResponse(url="/profile", status_code=302)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        secure=True
    )
    return response


