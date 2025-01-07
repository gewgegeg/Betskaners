from sqlalchemy.orm import Session
from app.models import Team, Match, MatchFormat, MatchStatus
from app.services.pandascore_service import PandaScoreService
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class SyncService:
    def __init__(self, db: Session):
        self.db = db
        self.pandascore = PandaScoreService()
    
    async def sync_teams(self):
        """Синхронизирует данные о командах"""
        try:
            # Получаем все матчи для сбора команд
            live_matches = await self.pandascore.get_live_matches()
            upcoming_matches = await self.pandascore.get_upcoming_matches()
            all_matches = live_matches + upcoming_matches
            
            team_names = set()
            for match in all_matches:
                if match and match.get('team1') != 'TBD':
                    team_names.add(match['team1'])
                if match and match.get('team2') != 'TBD':
                    team_names.add(match['team2'])
            
            # Получаем существующие команды
            existing_teams = {
                team.name: team 
                for team in self.db.query(Team).all()
            }
            
            # Добавляем новые команды
            for team_name in team_names:
                if team_name not in existing_teams:
                    team = Team(
                        name=team_name,
                        rating=1000.0
                    )
                    self.db.add(team)
            
            self.db.commit()
            logger.info("Teams sync completed successfully")
            
        except Exception as e:
            logger.error(f"Error syncing teams: {e}")
            self.db.rollback()
    
    async def sync_live_matches(self):
        """Синхронизирует live матчи"""
        try:
            live_matches = await self.pandascore.get_live_matches()
            
            for match_data in live_matches:
                if not match_data:  # Пропускаем None значения
                    continue
                    
                try:
                    # Проверяем существование команд
                    team1_name = match_data.get('team1')
                    team2_name = match_data.get('team2')
                    
                    if not team1_name or not team2_name or team1_name == 'TBD' or team2_name == 'TBD':
                        continue
                    
                    team1 = self.db.query(Team).filter(Team.name == team1_name).first()
                    team2 = self.db.query(Team).filter(Team.name == team2_name).first()
                    
                    if not team1 or not team2:
                        continue
                    
                    # Определяем формат матча
                    format_str = match_data.get('format', 'bo3').lower()
                    if format_str == 'bo1':
                        match_format = MatchFormat.BO1
                    elif format_str == 'bo2':
                        match_format = MatchFormat.BO2
                    elif format_str == 'bo5':
                        match_format = MatchFormat.BO5
                    else:
                        match_format = MatchFormat.BO3
                    
                    # Создаем или обновляем матч
                    match = self.db.query(Match).filter(
                        Match.team1_id == team1.id,
                        Match.team2_id == team2.id,
                        Match.tournament_name == match_data.get('tournament', 'Unknown Tournament')
                    ).first()
                    
                    score1, score2 = self._parse_score(match_data.get('score', '0:0'))
                    
                    if not match:
                        match = Match(
                            team1_id=team1.id,
                            team2_id=team2.id,
                            tournament_name=match_data.get('tournament', 'Unknown Tournament'),
                            start_time=datetime.now(),
                            format=match_format,
                            status=MatchStatus.LIVE,
                            is_live=True,
                            score_team1=score1,
                            score_team2=score2
                        )
                        self.db.add(match)
                    else:
                        match.status = MatchStatus.LIVE
                        match.is_live = True
                        match.score_team1 = score1
                        match.score_team2 = score2
                    
                    self.db.flush()
                    
                except Exception as e:
                    logger.error(f"Error processing live match: {e}")
                    continue
            
            self.db.commit()
            logger.info("Live matches sync completed successfully")
            
        except Exception as e:
            logger.error(f"Error syncing live matches: {e}")
            self.db.rollback()
    
    async def sync_upcoming_matches(self):
        """Синхронизирует предстоящие матчи"""
        try:
            upcoming_matches = await self.pandascore.get_upcoming_matches()
            
            for match_data in upcoming_matches:
                if not match_data:  # Пропускаем None значения
                    continue
                    
                try:
                    team1_name = match_data.get('team1')
                    team2_name = match_data.get('team2')
                    
                    if not team1_name or not team2_name or team1_name == 'TBD' or team2_name == 'TBD':
                        continue
                    
                    team1 = self.db.query(Team).filter(Team.name == team1_name).first()
                    team2 = self.db.query(Team).filter(Team.name == team2_name).first()
                    
                    if not team1 or not team2:
                        continue
                    
                    # Определяем формат матча
                    format_str = match_data.get('format', 'bo3').lower()
                    if format_str == 'bo1':
                        match_format = MatchFormat.BO1
                    elif format_str == 'bo2':
                        match_format = MatchFormat.BO2
                    elif format_str == 'bo5':
                        match_format = MatchFormat.BO5
                    else:
                        match_format = MatchFormat.BO3
                    
                    # Парсим время начала матча
                    start_time = datetime.strptime(match_data['start_time'], '%Y-%m-%d %H:%M')
                    
                    # Создаем матч если его еще нет
                    match = self.db.query(Match).filter(
                        Match.team1_id == team1.id,
                        Match.team2_id == team2.id,
                        Match.tournament_name == match_data.get('tournament', 'Unknown Tournament')
                    ).first()
                    
                    if not match:
                        match = Match(
                            team1_id=team1.id,
                            team2_id=team2.id,
                            tournament_name=match_data.get('tournament', 'Unknown Tournament'),
                            start_time=start_time,
                            format=match_format,
                            status=MatchStatus.SCHEDULED
                        )
                        self.db.add(match)
                        self.db.flush()
                    
                except Exception as e:
                    logger.error(f"Error processing upcoming match: {e}")
                    continue
            
            self.db.commit()
            logger.info("Upcoming matches sync completed successfully")
            
        except Exception as e:
            logger.error(f"Error syncing upcoming matches: {e}")
            self.db.rollback()
    
    def _parse_score(self, score_str: str) -> tuple[int, int]:
        """Парсит строку со счетом в два числа"""
        try:
            score1, score2 = score_str.split(':')
            return int(score1), int(score2)
        except:
            return 0, 0
    
    def _parse_datetime(self, datetime_str: str) -> datetime:
        """Парсит строку с датой и временем"""
        try:
            return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
        except:
            return datetime.now() + timedelta(hours=1) 