from datetime import datetime
from typing import List, Optional

from sqlmodel import SQLModel, Field, Relationship, Column, String

from app.core.config import settings

TZ = settings.TZ


def current_time():
    return datetime.now().isoformat()


class Threads(SQLModel, table=True):
    __tablename__ = "threads"

    id: int = Field(default=None, primary_key=True, index=True)
    sender_id: str = Field(index=True)
    thread_id: str = Field()
    expiration_time: datetime = Field()