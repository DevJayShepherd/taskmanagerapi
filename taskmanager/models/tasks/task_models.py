import uuid
from datetime import datetime

from sqlalchemy import Column, String, Boolean, DateTime

from taskmanager.core.db.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()),
                unique=True, index=True)
    title = Column(String, nullable=False)  # TODO decide on character limit
    description = Column(String, nullable=True)  # TODO decide on character limit
    completed = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
