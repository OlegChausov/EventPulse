from fastapi import FastAPI
from Event_Pulse_app.routers import all_routers

app = FastAPI()

# app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

for r in all_routers:
    app.include_router(r)