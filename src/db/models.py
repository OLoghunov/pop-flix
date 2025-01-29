import uuid
from datetime import datetime
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, ForeignKey
import sqlalchemy.dialects.postgresql as pg


class UserFilmLink(SQLModel, table=True):
    __tablename__ = "user_film_association"

    user_uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, ForeignKey("users.uid", ondelete="CASCADE"), primary_key=True)
    )
    film_uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, ForeignKey("films.uid", ondelete="CASCADE"), primary_key=True)
    )


class Film(SQLModel, table=True):
    __tablename__ = "films"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True, default=uuid.uuid4)
    )
    title: str = Field(nullable=False)
    year: Optional[int] = None
    poster: Optional[str] = None
    users: List["User"] = Relationship(
        back_populates="films", link_model=UserFilmLink
    )


class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True, default=uuid.uuid4)
    )
    username: str
    email: str
    firstName: str
    lastName: str
    role: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False, server_default="user")
    )
    isVerified: bool = Field(default=False)
    passwordHash: str = Field(exclude=True)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    films: List["Film"] = Relationship(
        back_populates="users", link_model=UserFilmLink
    )
