from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models import Match, MatchStatus
from fastapi.templating import Jinja2Templates
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def index(request: Request, db: Session = Depends(get_db)):
    """Главная страница"""
    matches = db.query(Match).filter(Match.status == MatchStatus.LIVE).all()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "matches": matches
        }
    )

@router.get("/matches")
async def matches(
    request: Request,
    type: str = "all",
    tournament: str = None,
    db: Session = Depends(get_db)
):
    """Страница матчей"""
    query = db.query(Match)
    
    if type == "live":
        query = query.filter(Match.status == MatchStatus.LIVE)
        title = "Матчи в прямом эфире"
    elif type == "upcoming":
        query = query.filter(
            Match.status == MatchStatus.SCHEDULED,
            Match.start_time >= datetime.utcnow()
        )
        title = "Предстоящие матчи"
    else:
        title = "Все матчи"
    
    if tournament:
        query = query.filter(Match.tournament_name == tournament)
    
    matches = query.order_by(Match.start_time).all()
    tournaments = db.query(Match.tournament_name).distinct().all()
    
    return templates.TemplateResponse(
        "matches.html",
        {
            "request": request,
            "matches": matches,
            "title": title,
            "current_type": type,
            "tournaments": [t[0] for t in tournaments],
            "current_tournament": tournament
        }
    )

@router.get("/predictions")
async def predictions(request: Request):
    """Страница прогнозов"""
    return templates.TemplateResponse(
        "predictions.html",
        {
            "request": request
        }
    )

@router.get("/predictions/{match_id}")
async def prediction_detail(request: Request, match_id: int, db: Session = Depends(get_db)):
    """Страница прогноза на конкретный матч"""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Матч не найден")
    
    return templates.TemplateResponse(
        "prediction_detail.html",
        {
            "request": request,
            "match": match
        }
    ) 