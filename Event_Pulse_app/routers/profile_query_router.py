import os

from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from Event_Pulse_app.database import get_db
from Event_Pulse_app.models import User, EventQuery
from Event_Pulse_app.utils.password import hash_password
from sqlalchemy.future import select
from sqlalchemy import delete
from Event_Pulse_app.utils.auth_jwt import create_access_token
from dotenv import load_dotenv
from Event_Pulse_app.utils.template_functions import templates
from Event_Pulse_app.utils.QueryNormalizer import QueryNormalizer


router = APIRouter()
router1 = APIRouter()
router2 = APIRouter()
router3 = APIRouter()


@router.get("/profile/query/list")
async def query_list(request: Request, db: AsyncSession = Depends(get_db)):
    user_id = request.state.user_id

    if user_id is None:
        return templates.TemplateResponse("partials/quaries_error.html", {"request": request, "message": "Пользователь не найден"} )

    result = await db.execute(select(EventQuery).where(EventQuery.user_id == user_id))
    queries = result.scalars().all()
    return templates.TemplateResponse("partials/query_list.html", {"request": request, "queries": queries, "success" : True})


@router1.get("/profile/query/form")
async def query_form(request: Request):
    return templates.TemplateResponse("partials/query_form.html", {"request": request})

@router2.post("/profile/query/add")
async def add_query(
    request: Request,
    db: AsyncSession = Depends(get_db),
    query_text: str = Form(...),
    query_type: str = Form(...)
):
    user_id = request.state.user_id

    await db.execute(
        delete(EventQuery).where(
            EventQuery.user_id == user_id,
            EventQuery.query_text == query_text
        )
    )

    query = EventQuery(
        user_id=user_id,
        query_text=query_text,
        preprocessed_name=QueryNormalizer.preprocess(query_text, query_type),
        query_type=query_type,
        is_active=True
    )
    db.add(query)
    await db.commit()

    result = await db.execute(select(EventQuery).where(EventQuery.user_id == user_id))
    queries = result.scalars().all()
    return templates.TemplateResponse("partials/query_list.html", {"request": request, "queries": queries})

@router3.post("/profile/query/deactivate/{query_id}")
async def deactivate_query(query_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(EventQuery).where(EventQuery.id == query_id))
    query = result.scalar_one_or_none()
    if query:
        query.is_active = False
        await db.commit()

    user_id = request.state.user_id
    result = await db.execute(select(EventQuery).where(EventQuery.user_id == user_id))
    queries = result.scalars().all()
    return templates.TemplateResponse("partials/query_list.html", {"request": request, "queries": queries})
