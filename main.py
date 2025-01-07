from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from sqlalchemy.orm import Session

from app.core.config import settings
from app.api.endpoints import matches, predictions, teams
from app.routes import web
from app.db.base import get_db
from app.models import Match

app = FastAPI(
    title="Betskaners",
    description="Система прогнозирования киберспортивных матчей",
    version=settings.API_VERSION,
    debug=settings.DEBUG
)

# Монтируем статические файлы
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "app", "static")), name="static")

# Подключаем роутеры
app.include_router(web.router)  # Веб-маршруты
app.include_router(matches.router)  # API маршруты
app.include_router(predictions.router, prefix=settings.API_PREFIX)
app.include_router(teams.router, prefix=settings.API_PREFIX)

# Шаблоны
templates = Jinja2Templates(directory="app/templates") 