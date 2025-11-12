import asyncio
import sys
from fastapi import FastAPI
from sqlalchemy import TryCast

from Event_Pulse_app.utils.parse_all import run_all_parsers

from Event_Pulse_app.config import STATIC_DIR
from Event_Pulse_app.routers import all_routers
from Event_Pulse_app.database import init_db
from Event_Pulse_app.middleware.auth_middleware import JWTMiddleware
from Event_Pulse_app.middleware.token_expiration_moddleware import SlidingExpirationMiddleware
from fastapi.staticfiles import StaticFiles
from Event_Pulse_app.config import STATIC_DIR, PARSER_REFRESH_INTERVAL_SECONDS



if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI()
app.add_middleware(JWTMiddleware)
app.add_middleware(SlidingExpirationMiddleware)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# @app.on_event("startup")
# async def on_startup():
#     await init_db()

for r in all_routers:
    app.include_router(r)


async def parser_loop():
    while True:
        try:
            app.state.parsed_events = await run_all_parsers()
            # print(app.state.parsed_events)
            await asyncio.sleep(PARSER_REFRESH_INTERVAL_SECONDS)
        except Exception as e:
            print(f"❌ Ошибка: {type(e).__name__}: {e}")
        await asyncio.sleep(PARSER_REFRESH_INTERVAL_SECONDS)


@app.on_event("startup")
async def startup():
    asyncio.create_task(parser_loop())
