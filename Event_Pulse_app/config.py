from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
IMAGES_DIR = STATIC_DIR / "images"



SEMI_PUBLIC_PATHS = ["/events", "/concerts", "/login", "/login",]
PUBLIC_PATHS = [ "/register", "/static", "/favicon.ico"]