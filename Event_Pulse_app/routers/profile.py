from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from Event_Pulse_app.database import get_db
from Event_Pulse_app.models import User
from Event_Pulse_app.utils.password import hash_password
from sqlalchemy.future import select
from Event_Pulse_app.utils.auth_jwt import create_access_token


router = APIRouter()
templates = Jinja2Templates(directory="Event_Pulse_app/templates")

@router.get("/profile")
async def profile(request: Request):
    user_id = request.state.user_id
    return templates.TemplateResponse("profile.html", {
        "request": request,
        "user_id": user_id
    })