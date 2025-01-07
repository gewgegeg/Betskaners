from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models import Match, MatchStatus
from fastapi.templating import Jinja2Templates
from datetime import datetime, timedelta
from typing import List

router = APIRouter(prefix="/api/v1")
templates = Jinja2Templates(directory="app/templates")

@router.get("/matches")
async def get_matches(
    request: Request, 
    type: str = "all",
    tournament: str = None,
    db: Session = Depends(get_db)
):
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
    
    # Получаем список уникальных турниров для фильтра
    tournaments = db.query(Match.tournament_name).distinct().all()
    tournaments = [t[0] for t in tournaments]
    
    return templates.TemplateResponse(
        "matches.html",
        {
            "request": request,
            "matches": matches,
            "title": title,
            "current_type": type,
            "tournaments": tournaments,
            "current_tournament": tournament
        }
    )

@router.get("/matches/live")
async def get_live_matches(db: Session = Depends(get_db)):
    """Получить список live матчей"""
    matches = db.query(Match).filter(Match.status == MatchStatus.LIVE).all()
    return {
        "matches": [
            {
                "id": match.id,
                "tournament_name": match.tournament_name,
                "team1": {
                    "name": match.team1.name,
                    "logo_url": match.team1.logo_url
                },
                "team2": {
                    "name": match.team2.name,
                    "logo_url": match.team2.logo_url
                },
                "score_team1": match.score_team1,
                "score_team2": match.score_team2,
                "status": match.status.value
            }
            for match in matches
        ]
    } 