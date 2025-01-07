from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime
import enum

class PredictionStatus(str, enum.Enum):
    PENDING = "pending"    # Ожидает начала матча
    ACTIVE = "active"     # Матч идет
    WIN = "win"          # Прогноз выиграл
    LOSS = "loss"        # Прогноз проиграл
    CANCELLED = "cancelled"  # Матч отменен

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    predicted_winner_id = Column(Integer, ForeignKey("teams.id"))
    status = Column(SQLEnum(PredictionStatus), default=PredictionStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)

    match = relationship("Match", back_populates="predictions")
    user = relationship("User", back_populates="predictions")
    predicted_winner = relationship("Team", foreign_keys=[predicted_winner_id]) 