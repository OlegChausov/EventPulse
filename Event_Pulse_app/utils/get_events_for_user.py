from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from Event_Pulse_app.database import get_db
from Event_Pulse_app.models import User, Event, EventQuery
from Event_Pulse_app.utils.fuzzy_match import fuzzy_match
from Event_Pulse_app.utils.password import hash_password
from sqlalchemy.future import select
from Event_Pulse_app.utils.QueryNormalizer import QueryNormalizer
from Event_Pulse_app.utils.template_functions import templates


async def send_an_email(user: User, new_events = list):
    pass

async def create_events(user: User, parsed_events: list[dict], db: AsyncSession):

    list_of_new_events = []

    stmt = await db.execute(select(EventQuery).where(EventQuery.user_id == user.id))
    user_event_queries = stmt.scalars().all()

    raw_events = parsed_events

    if not raw_events:
        raise HTTPException(status_code=400, detail="Нет распарсенных событий")

    stmt1 = await db.execute(select(Event.url).where(Event.user_id == user.id))
    old_user_events_urls = stmt1.scalars().all()



    for user_event_queriy in user_event_queries:
        for raw_event in raw_events:
            if fuzzy_match(user_event_queriy, raw_event) and raw_event['url'] not in old_user_events_urls:
                new_event = Event(
                user_id = user.id,
                event_query_id = user_event_queriy.id,
                title = raw_event.get('title'),
                preprocessed_title = QueryNormalizer.preprocess(raw_event['title'], user_event_queriy.query_type),
                url = raw_event['url'],
                location = raw_event.get('location'),
                )
                try:
                    db.add(new_event)
                    list_of_new_events.append(new_event)
                except Exception as e:
                    print(f"{raw_event} не обработалось: {e}")




    await db.commit()
    print("НОВЫЕ СОБЫТИЯ")
    print(list_of_new_events) #для проверки
    await send_an_email(user, list_of_new_events)
    return list_of_new_events


