from fastapi import FastAPI

app = FastAPI()

# app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
async def root():
    return {"message": "Event Pulse API is alive"}