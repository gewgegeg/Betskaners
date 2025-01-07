from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String, index=True)
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="SET NULL"), nullable=True)
    position = Column(Integer)  # 1-5 позиция
    avg_kda = Column(Float, default=0.0)
    avg_gpm = Column(Float, default=0.0)
    avg_xpm = Column(Float, default=0.0)

    team = relationship("Team", back_populates="players") 