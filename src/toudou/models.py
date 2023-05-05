import os
import pickle
import uuid
import sqlite3
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy.types import String, Boolean, DateTime, BIGINT
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from toudou import config


# https://medium.com/swlh/flask-sqlalchemy-basics-60d4f7f122
class Base(DeclarativeBase):
    pass

@dataclass
class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True)
    task: Mapped[str] = mapped_column(String(100))
    complete: Mapped[bool] = mapped_column(Boolean)
    due: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

engine = create_engine(config['DATABASE_URL'], echo=config['DEBUG'])

def init_db() -> None:
    Base.metadata.create_all(engine)


def read_from_file(filename: str) -> Todo:
    with open(os.path.join(TODO_FOLDER, filename), "rb") as f:
        return pickle.load(f)


def write_to_file(todo: Todo, filename: str) -> None:
    with open(os.path.join(TODO_FOLDER, filename), "wb") as f:
        pickle.dump(todo, f)


def create_todo(
    task: str,
    complete: bool = False,
    due: Optional[datetime] = None,
) -> int:
    with Session(engine) as session:
        id = random.randint(1, 100000000)
        todo = Todo(id=id, task=task, complete=complete, due=due)
        session.add(todo)
        session.commit()
        return id


def get_todo(id: int) -> Todo:
    with Session(engine) as session:
        return session.query(Todo).get(id)


def get_todos_completed(complete: bool) -> list[Todo]:
    with Session(engine) as session:
        return session.query(Todo).filter(Todo.complete == complete).all()
    
def get_todos() -> list[Todo]:
    with Session(engine) as session:
        return session.query(Todo).all()


def update_todo(
    id: int,
    task: str,
    complete: bool,
    due: Optional[datetime] = None,
) -> None:
    todo = get_todo(id)
    if todo:
        todo.task = task
        todo.complete = complete
        todo.due = due
        with Session(engine) as session:
            session.add(todo)
            session.commit()


def delete_todo(id: int) -> None:
    todo = get_todo(id)
    if todo:
        with Session(engine) as session:
            session.delete(todo)
            session.commit()

