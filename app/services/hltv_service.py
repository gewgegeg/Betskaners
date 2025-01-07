import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class HLTVService:
    BASE_URL = "https://www.hltv.org"
    MATCHES_URL = f"{BASE_URL}/matches"
    
    async def get_page(self, url: str) -> str:
        """Получает HTML страницу"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                return await response.text()
    
    async def get_live_matches(self):
        """Получает текущие live матчи"""
        try:
            html = await self.get_page(self.MATCHES_URL)
            soup = BeautifulSoup(html, 'html.parser')
            live_matches = []
            
            # Находим все live матчи
            live_section = soup.find('div', {'class': 'live-matches'})
            if live_section:
                for match in live_section.find_all('div', {'class': 'match'}):
                    try:
                        team1 = match.find('div', {'class': 'team1'}).text.strip()
                        team2 = match.find('div', {'class': 'team2'}).text.strip()
                        score = match.find('div', {'class': 'score'}).text.strip()
                        tournament = match.find('div', {'class': 'tournament'}).text.strip()
                        
                        live_matches.append({
                            'team1': team1,
                            'team2': team2,
                            'score': score,
                            'tournament': tournament,
                            'format': 'bo3',  # По умолчанию
                            'status': 'Live'
                        })
                    except Exception as e:
                        logger.error(f"Error parsing live match: {e}")
                        continue
            
            return live_matches
            
        except Exception as e:
            logger.error(f"Error getting live matches: {e}")
            return []
    
    async def get_upcoming_matches(self):
        """Получает предстоящие матчи"""
        try:
            html = await self.get_page(self.MATCHES_URL)
            soup = BeautifulSoup(html, 'html.parser')
            upcoming_matches = []
            
            # Находим все предстоящие матчи
            upcoming_section = soup.find('div', {'class': 'upcoming-matches'})
            if upcoming_section:
                for match in upcoming_section.find_all('div', {'class': 'match'}):
                    try:
                        team1 = match.find('div', {'class': 'team1'}).text.strip()
                        team2 = match.find('div', {'class': 'team2'}).text.strip()
                        time = match.find('div', {'class': 'time'}).text.strip()
                        tournament = match.find('div', {'class': 'tournament'}).text.strip()
                        
                        # Конвертируем время
                        match_time = datetime.strptime(time, '%H:%M')
                        match_time = match_time.replace(
                            year=datetime.now().year,
                            month=datetime.now().month,
                            day=datetime.now().day
                        )
                        
                        upcoming_matches.append({
                            'team1': team1,
                            'team2': team2,
                            'start_time': match_time.strftime('%Y-%m-%d %H:%M'),
                            'tournament': tournament,
                            'format': 'bo3',  # По умолчанию
                            'status': 'Scheduled'
                        })
                    except Exception as e:
                        logger.error(f"Error parsing upcoming match: {e}")
                        continue
            
            return upcoming_matches
            
        except Exception as e:
            logger.error(f"Error getting upcoming matches: {e}")
            return [] 