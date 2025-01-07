import pytest
from sqlalchemy.orm import Session
from app.models import Match, Team, MatchStatus, MatchFormat

def test_create_match(db: Session):
    # Создаем тестовые команды
    team1 = Team(name="Test Team 1", rating=1500)
    team2 = Team(name="Test Team 2", rating=1450)
    db.add_all([team1, team2])
    db.commit()
    
    # Создаем тестовый матч
    match = Match(
        team1_id=team1.id,
        team2_id=team2.id,
        tournament_name="Test Tournament",
        format=MatchFormat.BO3,
        status=MatchStatus.SCHEDULED
    )
    db.add(match)
    db.commit()
    
    # Проверяем создание матча
    assert match.id is not None
    assert match.team1.name == "Test Team 1"
    assert match.team2.name == "Test Team 2"
    assert match.status == MatchStatus.SCHEDULED

def test_update_match_score(db: Session):
    # Создаем тестовый матч
    team1 = Team(name="Team A", rating=1500)
    team2 = Team(name="Team B", rating=1450)
    db.add_all([team1, team2])
    db.commit()
    
    match = Match(
        team1_id=team1.id,
        team2_id=team2.id,
        tournament_name="Test Match",
        format=MatchFormat.BO3,
        status=MatchStatus.LIVE
    )
    db.add(match)
    db.commit()
    
    # Обновляем счет
    match.score_team1 = 2
    match.score_team2 = 1
    match.status = MatchStatus.FINISHED
    match.winner_id = team1.id
    db.commit()
    
    # Проверяем обновление
    updated_match = db.query(Match).filter(Match.id == match.id).first()
    assert updated_match.score_team1 == 2
    assert updated_match.score_team2 == 1
    assert updated_match.status == MatchStatus.FINISHED
    assert updated_match.winner_id == team1.id 