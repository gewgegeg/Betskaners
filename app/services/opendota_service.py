import httpx
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class OpenDotaService:
    BASE_URL = "https://api.opendota.com/api"
    
    async def get_pro_teams(self) -> List[Dict[str, Any]]:
        """Получает список профессиональных команд"""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.BASE_URL}/teams")
            response.raise_for_status()
            return response.json()
    
    async def get_team_matches(self, team_id: int) -> List[Dict[str, Any]]:
        """Получает последние матчи команды"""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.BASE_URL}/teams/{team_id}/matches")
            response.raise_for_status()
            return response.json()
    
    async def get_match_details(self, match_id: int) -> Dict[str, Any]:
        """Получает детальную информацию о матче"""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.BASE_URL}/matches/{match_id}")
            response.raise_for_status()
            return response.json() 