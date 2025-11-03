from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from Event_Pulse_app.database import get_db
from Event_Pulse_app.models import User
from Event_Pulse_app.utils.password import hash_password


router = APIRouter()
templates = Jinja2Templates(directory="Event_Pulse_app/templates")

@router.get("/register")
async def show_register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
async def register_user(
    request: Request,
    email: str = Form(...),
    name: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    user = User(
        email=email,
        name=name,
        password=password,
        password_hash=hash_password(password)
    )
    db.add(user)
    await db.commit()
    return RedirectResponse(url="/register", status_code=302)
