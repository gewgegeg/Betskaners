from datetime import datetime
from pydantic import BaseModel
from app.models.match import MatchFormat, MatchStatus

class MatchBase(BaseModel):
    tournament_name: str
    start_time: datetime
    format: MatchFormat
    status: MatchStatus = MatchStatus.SCHEDULED

class MatchCreate(MatchBase):
    team1_id: int
    team2_id: int

class Match(MatchBase):
    id: int
    team1_id: int
    team2_id: int
    winner_id: int | None = None
    score_team1: int = 0
    score_team2: int = 0

    class Config:
        from_attributes = True 