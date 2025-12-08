from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from Event_Pulse_app.models import User
from Event_Pulse_app.utils.translations import translations
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Event_Pulse_app.models import User
from Event_Pulse_app.database import get_db
from fastapi import APIRouter, Request, Form, Depends, HTTPException

#определяем язык в куке и если не выбран, кладем туда язык браузера

def get_browser_lang(request: Request, default: str = "RU") -> str:
    lang_header = request.headers.get("accept-language", "")
    if not lang_header:
        return default
    # Берём первую часть до запятой и до дефиса
    return lang_header.split(",")[0].split("-")[0]


class SetLangMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        lang = request.cookies.get("lang")
        if not lang:
            lang = get_browser_lang(request, default="RU")


        #пока кладем в реквест дефолтный язык
        request.state.lang = lang
        request.state.t = translations.get(lang, translations["RU"])
        return await call_next(request)




