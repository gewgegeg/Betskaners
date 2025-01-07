from liquipediapy import dota
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class LiquipediaService:
    def __init__(self):
        self.dota_client = dota("Betskaners")  # Имя вашего приложения
    
    async def get_upcoming_matches(self):
        """Получает предстоящие матчи"""
        try:
            matches = self.dota_client.get_upcoming_and_ongoing_games()
            return [m for m in matches if m.get('status') != 'Live']
        except Exception as e:
            logger.error(f"Error getting upcoming matches: {e}")
            return []
    
    async def get_live_matches(self):
        """Получает текущие live матчи"""
        try:
            matches = self.dota_client.get_upcoming_and_ongoing_games()
            return [m for m in matches if m.get('status') == 'Live']
        except Exception as e:
            logger.error(f"Error getting live matches: {e}")
            return [] 