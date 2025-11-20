import os

from fastapi import APIRouter, Request, Form, Depends, Request
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
from typing import List
from fastapi.responses import RedirectResponse



router = APIRouter()
router1 = APIRouter()
router2 = APIRouter()
router3 = APIRouter()

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



@router.post("/profile/event/event_bulk")
async def event_bulk(
    request: Request,
    selected_ids: List[int] = Form(...),
    action: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    user_id = request.state.user_id

    if action == "hide":
        success_count = 0
        fail_count = 0
        for event_id in selected_ids:
            obj = await db.get(Event, event_id)
            if not obj:
                print(f"событие с id {event_id} не найдено для действия Hide")
                fail_count += 1
                continue
            try:
                obj.is_active = False
                db.add(obj)
                success_count += 1
            except Exception as e:
                print(f"Ошибка при деактивации : {obj.id} {e}")

        await db.commit()


        # result = await db.execute(select(Event).where(Event.user_id == user_id))
        # updated_events = result.scalars().all()
        #
        # return templates.TemplateResponse(
        #     "partials/event_list.html",
        #     {"request": request, "events": updated_events, "message": f"Hide: {success_count}/{fail_count}"}
        # )

        return RedirectResponse(url="/profile", status_code=303)


    elif action == "deactivate_related_query":
        success_count = 0
        fail_count = 0
        for event_id in selected_ids:
            obj = await db.get(Event, event_id)
            if not obj:
                print(f"событие с id {event_id} не найдено для действия deactivate_related_query")
                fail_count += 1
                continue
            try:
                result = await db.execute(
                    select(EventQuery)
                    .join(EventQuery.matched_events)
                    .where(Event.id == obj.id)
                )
                event_query = result.scalar_one_or_none()
                if event_query:
                    event_query.is_active = False
                    success_count += 1
                    db.add(event_query)

            except Exception as e:
                print(f"Ошибка при деактивации EventQuery связанного с : {obj.id} {e}")



        await db.commit()
        # result = await db.execute(select(EventQuery).where(EventQuery.user_id == user_id))
        # new_queries = result.scalars().all()
        #
        # return templates.TemplateResponse(
        # "partials/query_list.html",
        # {"request": request, "queries": new_queries, "message": f"Deactivate_related_quaries: {success_count}/{fail_count}"})

        return RedirectResponse(url="/profile", status_code=303)





