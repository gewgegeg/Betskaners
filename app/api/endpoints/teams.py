from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models import Team, Match
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/teams")
async def get_teams(request: Request, db: Session = Depends(get_db)):
    teams = db.query(Team).order_by(Team.rating.desc()).all()
    
    return templates.TemplateResponse(
        "teams.html",
        {
            "request": request,
            "teams": teams
        }
    ) 

@router.get("/teams/{team_id}")
async def get_team(request: Request, team_id: int, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Получаем последние матчи команды
    recent_matches = db.query(Match).filter(
        (Match.team1_id == team_id) | (Match.team2_id == team_id)
    ).order_by(Match.start_time.desc()).limit(5).all()
    
    return templates.TemplateResponse(
        "team_detail.html",
        {
            "request": request,
            "team": team,
            "recent_matches": recent_matches
        }
    ) 