from pathlib import Path
from Event_Pulse_app.parsers.afisha_me import get_afisha_me_films
from Event_Pulse_app.parsers.biletai_lt import get_biletai_lt_concerts
from Event_Pulse_app.parsers.concertful import get_concertful_pl

PARSERS = [
    {"name": "afisha_me", "func": get_afisha_me_films, "type": "film", "region": "BY"},
    {"name": "biletail_lt", "func": get_biletai_lt_concerts, "type": "concert", "region": "LT"},
    {"name": "concertful", "func": get_concertful_pl, "type": "concert", "region": "PL"},
]


BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
IMAGES_DIR = STATIC_DIR / "images"



SEMI_PUBLIC_PATHS = ["/events", "/concerts", "/login", "/login",]
PUBLIC_PATHS = [
    "/register",
    "/static",
    "/favicon.ico",
    "/test-parse-all",
    "/ping",
    "/docs",
    "/openapi.json"
]

# "/test-parse-all" "/ping" - подчистить

