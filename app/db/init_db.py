from sqlalchemy.orm import Session
from app.models import Team, Match, MatchStatus, MatchFormat, User
from datetime import datetime, timedelta
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def init_db(db: Session) -> None:
    """Инициализирует базу данных тестовыми данными"""
    
    # Создаем тестового пользователя
    test_user = User(
        username="test_user",
        email="test@example.com",
        hashed_password=pwd_context.hash("password123")
    )
    db.add(test_user)
    db.commit()
    
    # Создаем тестовые команды
    teams = [
        Team(
            name="Team Spirit",
            rating=1500,
            wins=70,
            total_matches=100,
            logo_url="/static/img/teams/spirit.png"
        ),
        Team(
            name="Virtus.pro",
            rating=1450,
            wins=65,
            total_matches=100,
            logo_url="/static/img/teams/virtus.png"
        ),
        Team(
            name="9 Pandas",
            rating=1400,
            wins=50,
            total_matches=80,
            logo_url="/static/img/teams/9pandas.png"
        ),
        Team(
            name="L1ga Team",
            rating=1350,
            wins=35,
            total_matches=60,
            logo_url="/static/img/teams/l1ga.png"
        )
    ]
    
    db.add_all(teams)
    db.commit()
    
    # Создаем тестовые матчи
    now = datetime.utcnow()
    
    matches = [
        # Live матчи
        Match(
            team1_id=1,  # Team Spirit
            team2_id=2,  # Virtus.pro
            tournament_name="The International 2024",
            format=MatchFormat.BO3,
            status=MatchStatus.LIVE,
            start_time=now - timedelta(minutes=30),
            score_team1=0,
            score_team2=1
        ),
        Match(
            team1_id=3,  # 9 Pandas
            team2_id=4,  # L1ga Team
            tournament_name="DreamLeague",
            format=MatchFormat.BO3,
            status=MatchStatus.LIVE,
            start_time=now - timedelta(minutes=15),
            score_team1=1,
            score_team2=1
        ),
        # Предстоящие матчи
        Match(
            team1_id=1,  # Team Spirit
            team2_id=3,  # 9 Pandas
            tournament_name="ESL One",
            format=MatchFormat.BO3,
            status=MatchStatus.SCHEDULED,
            start_time=now + timedelta(hours=2)
        ),
        Match(
            team1_id=2,  # Virtus.pro
            team2_id=4,  # L1ga Team
            tournament_name="DreamLeague",
            format=MatchFormat.BO3,
            status=MatchStatus.SCHEDULED,
            start_time=now + timedelta(hours=4)
        ),
        Match(
            team1_id=1,  # Team Spirit
            team2_id=4,  # L1ga Team
            tournament_name="The International 2024",
            format=MatchFormat.BO5,
            status=MatchStatus.SCHEDULED,
            start_time=now + timedelta(days=1)
        )
    ]
    
    db.add_all(matches)
    db.commit() 