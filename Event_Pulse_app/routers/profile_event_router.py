import os

from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from Event_Pulse_app.database import get_db
from Event_Pulse_app.models import User, Event
from Event_Pulse_app.utils.password import hash_password
from sqlalchemy.future import select
from Event_Pulse_app.utils.auth_jwt import create_access_token
from dotenv import load_dotenv
from Event_Pulse_app.utils.template_functions import templates
from Event_Pulse_app.utils.QueryNormalizer import QueryNormalizer

router = APIRouter()

@router.get("/profile/events/list")
async def events_list(request: Request, db: AsyncSession = Depends(get_db)):
    user_id = request.state.user_id

    if user_id is None:
        return templates.TemplateResponse("partials/quaries_error.html", {"request": request, "message": "Пользователь не найден"} )

    result = await db.execute(select(Event).where(Event.user_id == user_id))
    events = result.scalars().all()
    return templates.TemplateResponse("partials/event_list.html", {"request": request, "events": events, "success" : True})