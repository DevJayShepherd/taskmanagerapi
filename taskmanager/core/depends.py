from typing import Generator
from sqlalchemy.orm import Session

from taskmanager.core.db.db import SessionLocal


def get_db_session() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
