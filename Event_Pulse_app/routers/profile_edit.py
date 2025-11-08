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


@router.get("/profile_edit")
async def profile_edit(request: Request, db: AsyncSession = Depends(get_db)):
    user_id = request.state.user_id
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return templates.TemplateResponse(
        "profile_edit.html",
        {"request": request, "user": user}
    )

@router.post("/profile_edit")
async def profile_edit(
        request: Request,
        db: AsyncSession = Depends(get_db),
        username: str = Form(...),
        email: str = Form(...),
        new_password: str = Form(...),
        new_password_confirmed: str = Form(...)):

    username = username.strip()
    email = email.strip()
    new_password = new_password.strip()
    new_password_confirmed = new_password_confirmed.strip()

    user_id = request.state.user_id
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")


    # Проверка уникальности нового username/email
    result = await db.execute(
        select(User).where(
            ((User.name == username) | (User.email == email)) &
            (User.id != user_id)
        )
    )
    if result.scalar_one_or_none():
        return templates.TemplateResponse(
            "profile_edit.html",
            {   "user": user,
                "request": request,
                "message": "Имя или email уже заняты",
                "success": False
            }
        )


    if new_password:
        if new_password != new_password_confirmed:
            return templates.TemplateResponse(
                "profile_edit.html",
                {   "user": user,
                    "request": request,
                    "message": "Пароли не совпадают",
                    "success": False
                }
            )



    # Обновление данных
    user.name = username
    user.email = email
    if new_password:
        user.password_hash = hash_password(new_password)
    await db.commit()
    await db.refresh(user)

    return templates.TemplateResponse(
        "profile_edit.html",
        {   "user": user,
            "request": request,
            "message": "Данные успешно обновлены"
        }
    )