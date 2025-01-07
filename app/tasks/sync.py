from fastapi import BackgroundTasks
from app.services.sync_service import SyncService
from app.db.base import SessionLocal
import asyncio
import logging

logger = logging.getLogger(__name__)

async def sync_data():
    """Задача для синхронизации данных"""
    db = SessionLocal()
    try:
        sync_service = SyncService(db)
        await sync_service.sync_teams()
        await sync_service.sync_live_matches()
        await sync_service.sync_upcoming_matches()
    finally:
        db.close()

def schedule_sync(background_tasks: BackgroundTasks):
    """Планирует синхронизацию данных"""
    background_tasks.add_task(sync_data) 