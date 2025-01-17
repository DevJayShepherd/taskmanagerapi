# SQLAlchemy imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Local Imports
from taskmanager.core.config import settings


DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
