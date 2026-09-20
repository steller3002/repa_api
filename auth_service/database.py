from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from auth_service.settings import DbSettings

db_settings = DbSettings()
connection_string = db_settings.connection_string

engine = create_engine(connection_string, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()