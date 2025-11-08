from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from Event_Pulse_app.database import get_db
from Event_Pulse_app.models import User
from Event_Pulse_app.utils.password import hash_password
from sqlalchemy.future import select
from Event_Pulse_app.utils.auth_jwt import create_access_token
from Event_Pulse_app.utils.template_functions import templates

router = APIRouter()


@router.get("/profile")
async def profile(request: Request, db: AsyncSession = Depends(get_db)):
    user_id = request.state.user_id
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return templates.TemplateResponse("profile.html", {
        "request": request,
        "user": user,
    })