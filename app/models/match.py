from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLEnum, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum
from datetime import datetime

class MatchStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    LIVE = "live"
    FINISHED = "finished"
    CANCELLED = "cancelled"

class MatchFormat(str, enum.Enum):
    BO1 = "bo1"
    BO2 = "bo2"
    BO3 = "bo3"
    BO5 = "bo5"

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    tournament_name = Column(String)
    team1_id = Column(Integer, ForeignKey("teams.id"))
    team2_id = Column(Integer, ForeignKey("teams.id"))
    format = Column(SQLEnum(MatchFormat))
    status = Column(SQLEnum(MatchStatus), default=MatchStatus.SCHEDULED)
    start_time = Column(DateTime, default=datetime.utcnow)
    score_team1 = Column(Integer, default=0)
    score_team2 = Column(Integer, default=0)
    winner_id = Column(Integer, ForeignKey("teams.id"), nullable=True)

    team1 = relationship("Team", foreign_keys=[team1_id])
    team2 = relationship("Team", foreign_keys=[team2_id])
    winner = relationship("Team", foreign_keys=[winner_id])
    predictions = relationship("Prediction", back_populates="match") 