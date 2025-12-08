from fastapi import FastAPI
app = FastAPI()
import asyncio
import sys
from sqlalchemy import TryCast
from sqlalchemy.ext.asyncio import AsyncSession
from Event_Pulse_app.utils.get_events_for_user import create_events
from Event_Pulse_app.utils.parse_all import run_all_parsers
from sqlalchemy.future import select
from Event_Pulse_app.config import STATIC_DIR
from Event_Pulse_app.routers import all_routers
from Event_Pulse_app.middleware.auth_middleware import JWTMiddleware
from Event_Pulse_app.middleware.token_expiration_moddleware import SlidingExpirationMiddleware
from Event_Pulse_app.middleware.set_lang_middleware import SetLangMiddleware

from fastapi.staticfiles import StaticFiles
from Event_Pulse_app.config import STATIC_DIR

from Event_Pulse_app.parser_loop import parser_loop


if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI()
app.add_middleware(JWTMiddleware)
app.add_middleware(SlidingExpirationMiddleware)
app.add_middleware(SetLangMiddleware)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")




for r in all_routers:
    app.include_router(r)




@app.on_event("startup")
async def startup():
    asyncio.create_task(parser_loop())