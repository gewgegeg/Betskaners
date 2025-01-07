import pytest
from sqlalchemy.orm import Session
from app.models import Team, Match, Prediction, MatchStatus, PredictionStatus
from app.ml.prediction_model import MatchPredictor

def test_create_prediction(db: Session):
    # Создаем тестовые данные
    team1 = Team(name="Team X", rating=1600, wins=80, total_matches=100)
    team2 = Team(name="Team Y", rating=1400, wins=60, total_matches=100)
    db.add_all([team1, team2])
    db.commit()
    
    match = Match(
        team1_id=team1.id,
        team2_id=team2.id,
        tournament_name="Test Tournament",
        status=MatchStatus.SCHEDULED
    )
    db.add(match)
    db.commit()
    
    # Создаем прогноз
    prediction = Prediction(
        match_id=match.id,
        predicted_winner_id=team1.id,
        coefficient=1.5,
        status=PredictionStatus.PENDING
    )
    db.add(prediction)
    db.commit()
    
    # Проверяем создание прогноза
    assert prediction.id is not None
    assert prediction.match_id == match.id
    assert prediction.status == PredictionStatus.PENDING

def test_prediction_model():
    predictor = MatchPredictor()
    
    # Создаем тестовые команды
    team1 = Team(
        name="Strong Team",
        rating=1800,
        wins=90,
        total_matches=100
    )
    team2 = Team(
        name="Weak Team",
        rating=1200,
        wins=30,
        total_matches=100
    )
    
    # Создаем тестовый матч
    match = Match(
        team1_id=1,
        team2_id=2,
        tournament_name="Test Match"
    )
    
    # Получаем предсказание
    prediction = predictor.predict_winner(team1, team2, match)
    
    # Проверяем результаты
    assert prediction['team1_win_probability'] > prediction['team2_win_probability']
    assert 0 <= prediction['prediction_confidence'] <= 1
    assert len(prediction['features_importance']) > 0 