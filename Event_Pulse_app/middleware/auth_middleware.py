from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import RedirectResponse
from fastapi.requests import Request
from jose import JWTError
from Event_Pulse_app.utils.auth_jwt import decode_access_token

class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        public_paths = ["/login", "/register", "/static", "/favicon.ico"]
        semi_public_paths = ["/events", "/concerts", "/login"]


        path = request.url.path
        # если путь публичный — пропускаем без проверки
        if any(path.startswith(p) for p in public_paths):
            return await call_next(request)

        token = request.cookies.get("access_token")
        # если нет токена
        if not token:
            # если маршрут полупубличный
            if any(path.startswith(p) for p in semi_public_paths):
                # нет токена, но маршрут разрешён → просто идём дальше
                return await call_next(request)
            else:
                # защищённый маршрут → редирект
                return RedirectResponse(url="/login")

        # Пробуем декодировать токен
        try:
            payload = decode_access_token(token)
            request.state.user_id = int(payload["sub"])
        except JWTError:
            # если токен битый и маршрут полупубличный
            if any(path.startswith(p) for p in semi_public_paths):
                return await call_next(request)
            return RedirectResponse(url="/login")

        # передаём управление дальше (роутеру или следующему middleware)
        return await call_next(request)
