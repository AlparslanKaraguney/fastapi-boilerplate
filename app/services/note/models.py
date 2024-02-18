from datetime import datetime, timedelta

from sqlmodel import Field

from app.core.auth.functions import (
    create_access_token,
    create_jwt_token,
    verify_password,
)
from app.core.models.base import ModelCore
from app.settings import settings


class Note(ModelCore, table=True):
    __tablename__ = "note"

    title: str
    description: str


class Todo(ModelCore, table=True):
    __tablename__ = "todo"

    order: int
    note_id: int = Field(foreign_key="note.id")
    importance: int = 0
    done: bool = False
