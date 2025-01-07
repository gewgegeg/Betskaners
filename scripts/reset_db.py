import os
import sys
from pathlib import Path

# Добавляем корневую директорию проекта в PYTHONPATH
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

from app.db.base import Base, engine
from app.db.init_db import init_db
from app.db.base import SessionLocal

def reset_database():
    # Удаляем все таблицы
    Base.metadata.drop_all(bind=engine)
    
    # Создаем таблицы заново
    Base.metadata.create_all(bind=engine)
    
    # Инициализируем тестовые данные
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()

if __name__ == "__main__":
    reset_database()
    print("База данных успешно сброшена и заполнена тестовыми данными") 