from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models import Match, Team, Prediction, PredictionStatus, MatchStatus
from datetime import datetime

router = APIRouter()

@router.post("/predictions")
async def create_prediction(
    match_id: int,
    predicted_winner_id: int,
    db: Session = Depends(get_db)
):
    """Создать новый прогноз"""
    # Проверяем существование матча
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Матч не найден")
    
    # Проверяем, что матч еще не начался
    if match.status != MatchStatus.SCHEDULED:
        raise HTTPException(status_code=400, detail="Нельзя сделать прогноз на начавшийся матч")
    
    # Проверяем, что предсказанная команда участвует в матче
    if predicted_winner_id not in [match.team1_id, match.team2_id]:
        raise HTTPException(status_code=400, detail="Выбранная команда не участвует в матче")
    
    # Создаем прогноз
    prediction = Prediction(
        match_id=match_id,
        user_id=1,  # Временно используем тестового пользователя
        predicted_winner_id=predicted_winner_id,
        status=PredictionStatus.PENDING
    )
    
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    
    return prediction

@router.get("/predictions")
async def get_predictions(db: Session = Depends(get_db)):
    """Получить список всех прогнозов"""
    predictions = db.query(Prediction).all()
    return predictions

@router.get("/predictions/{prediction_id}")
async def get_prediction(prediction_id: int, db: Session = Depends(get_db)):
    """Получить конкретный прогноз"""
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if not prediction:
        raise HTTPException(status_code=404, detail="Прогноз не найден")
    return prediction 