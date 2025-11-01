import asyncio
import sys
from fastapi import FastAPI
from Event_Pulse_app.routers import all_routers
from Event_Pulse_app.database import init_db
from Event_Pulse_app import models  # 👈 загружаем модели

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()

for r in all_routers:
    app.include_router(r)
