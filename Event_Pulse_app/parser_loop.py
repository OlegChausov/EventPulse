import asyncio
from Event_Pulse_app.utils.get_events_for_user import create_events
from Event_Pulse_app.utils.parse_all import run_all_parsers
from sqlalchemy.future import select
from Event_Pulse_app.config import PARSER_REFRESH_INTERVAL_SECONDS
from Event_Pulse_app.models import User
from Event_Pulse_app.database import AsyncSessionLocal

from Event_Pulse_app.main import app




async def parser_loop():
    while True:
        async with AsyncSessionLocal() as db:
            try:
                app.state.parsed_events = await run_all_parsers()
                parsed_events = app.state.parsed_events
                await asyncio.sleep(2)

                result = await db.execute(select(User))
                users = result.scalars().all()

                for user in users:
                    try:
                        await create_events(user, parsed_events, db)
                    except Exception as e:
                        print(f"❌ Ошибка: {type(e).__name__}: {e} для {user.id} {user.name}")

            except Exception as e:
                print(f"❌ Ошибка: {type(e).__name__}: {e}")
            finally:
                await asyncio.sleep(PARSER_REFRESH_INTERVAL_SECONDS)









