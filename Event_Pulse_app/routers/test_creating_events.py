from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from Event_Pulse_app.database import get_db
from Event_Pulse_app.models import User
from Event_Pulse_app.utils.get_events_for_user import create_events

router = APIRouter()

@router.get("/test-creating-events")
async def test_all(request: Request, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.id == 2)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        return {"error": "Пользователь не найден"}

    parsed_events = request.app.state.parsed_events

    if not parsed_events:
        return {"error": "Нет распарсенных событий"}

    new_events = await create_events(user, parsed_events, db)

    return {"added": len(new_events)}
