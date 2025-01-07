import aiohttp
from datetime import datetime, timedelta
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class PandaScoreService:
    BASE_URL = "https://api.pandascore.co/dota2"
    
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {settings.PANDASCORE_TOKEN}"
        }
    
    async def get_live_matches(self):
        """Получает текущие live матчи"""
        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                url = f"{self.BASE_URL}/matches/running"
                async with session.get(url) as response:
                    if response.status == 200:
                        matches = await response.json()
                        return [self._format_match(match) for match in matches]
                    else:
                        logger.error(f"Error getting live matches: {response.status}")
                        return []
        except Exception as e:
            logger.error(f"Error getting live matches: {e}")
            return []
    
    async def get_upcoming_matches(self):
        """Получает предстоящие матчи"""
        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                # Получаем матчи на следующие 7 дней
                range_start = datetime.now().strftime("%Y-%m-%d")
                range_end = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
                
                url = f"{self.BASE_URL}/matches/upcoming"
                params = {
                    "range[begin_at]": f"{range_start},{range_end}",
                    "per_page": 100
                }
                
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        matches = await response.json()
                        return [self._format_match(match) for match in matches]
                    else:
                        logger.error(f"Error getting upcoming matches: {response.status}")
                        return []
        except Exception as e:
            logger.error(f"Error getting upcoming matches: {e}")
            return []
    
    def _format_match(self, match_data):
        """Форматирует данные матча в нужный формат"""
        try:
            # Определяем формат матча
            match_format = "bo3"  # По умолчанию
            if match_data.get("number_of_games") == 1:
                match_format = "bo1"
            elif match_data.get("number_of_games") == 5:
                match_format = "bo5"
            
            # Форматируем время
            start_time = datetime.fromisoformat(match_data["scheduled_at"].replace("Z", "+00:00"))
            
            return {
                "team1": match_data["opponents"][0]["opponent"]["name"] if match_data.get("opponents") and len(match_data["opponents"]) > 0 else "TBD",
                "team2": match_data["opponents"][1]["opponent"]["name"] if match_data.get("opponents") and len(match_data["opponents"]) > 1 else "TBD",
                "tournament": match_data["league"]["name"],
                "format": match_format,
                "start_time": start_time.strftime("%Y-%m-%d %H:%M"),
                "status": "Live" if match_data["status"] == "running" else "Scheduled",
                "score": f"{match_data.get('results', [{'score': 0}])[0].get('score', 0)}:{match_data.get('results', [{'score': 0}, {'score': 0}])[1].get('score', 0)}" if match_data.get("status") == "running" else "0:0"
            }
        except Exception as e:
            logger.error(f"Error formatting match: {e}")
            return None 