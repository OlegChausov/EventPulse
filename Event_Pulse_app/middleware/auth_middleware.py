from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import RedirectResponse
from fastapi.requests import Request
from jose import JWTError
from Event_Pulse_app.utils.auth_jwt import decode_access_token

class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        public_paths = ["/login", "/register", "/static", "/favicon.ico"]

        if any(request.url.path.startswith(path) for path in public_paths):
            return await call_next(request)

        token = request.cookies.get("access_token")
        if not token:
            return RedirectResponse(url="/login")

        try:
            payload = decode_access_token(token)
            request.state.user_id = payload["sub"]
        except JWTError:
            return RedirectResponse(url="/login")

        return await call_next(request)
