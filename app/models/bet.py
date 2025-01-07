from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Bet(Base):
    __tablename__ = "bets"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id"))
    predicted_winner_id = Column(Integer, ForeignKey("teams.id"))
    confidence = Column(Float)  # Уверенность в прогнозе (0-1)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    match = relationship("Match")
    predicted_winner = relationship("Team") 