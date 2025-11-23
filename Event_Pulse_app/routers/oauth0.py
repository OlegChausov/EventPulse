from fastapi import APIRouter
from fastapi.responses import RedirectResponse
import os
from dotenv import load_dotenv
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
import httpx, os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

OAUTH0_DOMAIN = os.getenv("OAUTH0_DOMAIN")
OAUTH0_CLIENT_ID = os.getenv("OAUTH0_CLIENT_ID")
OAUTH0_REDIRECT_URI = os.getenv("OAUTH0_REDIRECT_URI")
OAUTH0_CLIENT_SECRET = os.getenv("OAUTH0_CLIENT_SECRET")

@router.get("/login/social")
async def login_social():
    return RedirectResponse(
        f"https://{OAUTH0_DOMAIN}/authorize?"
        f"response_type=code&"
        f"client_id={OAUTH0_CLIENT_ID}&"
        f"redirect_uri={OAUTH0_REDIRECT_URI}&"
        f"scope=openid profile email"
    )


router1 = APIRouter()

@router1.get("/login/callback")
async def callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return {"error": "Missing code"}

    async with httpx.AsyncClient() as client:
        # 1. Обмен кода на токен
        token_resp = await client.post(f"https://{OAUTH0_DOMAIN}/oauth/token", data={
            "grant_type": "authorization_code",
            "client_id": OAUTH0_CLIENT_ID,
            "client_secret": OAUTH0_CLIENT_SECRET,
            "code": code,
            "redirect_uri": OAUTH0_REDIRECT_URI,
        })
        tokens = token_resp.json()

        # 2. Получение профиля пользователя
        userinfo_resp = await client.get(
            f"https://{OAUTH0_DOMAIN}/userinfo",
            headers={"Authorization": f"Bearer {tokens['access_token']}"}
        )
        profile = userinfo_resp.json()

    # Пока просто возвращаем профиль для проверки
    # return profile
        #после получения данных с oauth0

        email = profile.get("email")  # вернёт None, если ключа нет
        name = profile.get("name", email)  # если не вернулось имя, назовем клиента по имэйлу. Имэйл и имя будут совпадать


