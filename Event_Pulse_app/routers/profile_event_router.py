import os

from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from Event_Pulse_app.database import get_db
from Event_Pulse_app.models import User, Event, EventQuery
from Event_Pulse_app.utils.password import hash_password
from sqlalchemy.future import select
from Event_Pulse_app.utils.auth_jwt import create_access_token
from dotenv import load_dotenv
from Event_Pulse_app.utils.template_functions import templates
from Event_Pulse_app.utils.QueryNormalizer import QueryNormalizer

router = APIRouter()
router1 = APIRouter()
router2 = APIRouter()

@router.get("/profile/events/list")
async def events_list(request: Request, db: AsyncSession = Depends(get_db)):
    user_id = request.state.user_id

    if user_id is None:
        return templates.TemplateResponse("partials/quaries_error.html", {"request": request, "message": "Пользователь не найден"} )

    result = await db.execute(select(Event).where(Event.user_id == user_id))
    events = result.scalars().all()
    return templates.TemplateResponse("partials/event_list.html", {"request": request, "events": events, "success" : True})


@router.get("/profile/event/deactivate_related_query/{event_id}")
async def deactivate_query(event_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    user_id = request.state.user_id

    result = await db.execute(
        select(EventQuery)
        .join(EventQuery.matched_events)
        .where(Event.id == event_id)
    )
    event_query = result.scalar_one_or_none()
    if event_query:
        event_query.is_active = False
        await db.commit()

    result = await db.execute(select(EventQuery).where(EventQuery.user_id == user_id))
    queries = result.scalars().all()

    return templates.TemplateResponse(
        "partials/query_list.html",
        {"request": request, "queries": queries}
    )



@router.get("/profile/event/deactivate_event/{event_id}")
async def deactivate_event(event_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    user_id = request.state.user_id

    result = await db.execute(select(Event).where(Event.id == event_id))
    event = result.scalar_one_or_none()

    if event:
        event.is_active = False
        await db.commit()

    result_stmt = await db.execute(select(Event).where(Event.user_id == user_id))
    events = result_stmt.scalars().all()
    return templates.TemplateResponse("partials/event_list.html",
                                      {"request": request, "events": events, "success": True})
