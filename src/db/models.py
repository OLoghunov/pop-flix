import uuid
from datetime import datetime
from typing import List, Optional
from enum import Enum

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, ForeignKey
import sqlalchemy.dialects.postgresql as pg


class FilmStatus(str, Enum):
    WATCHED = "watched"
    PLANNED = "planned"


class UserFilmLink(SQLModel, table=True):
    __tablename__ = "user_film_association"

    user_uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, ForeignKey("users.uid", ondelete="CASCADE"), primary_key=True)
    )
    film_uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, ForeignKey("films.uid", ondelete="CASCADE"), primary_key=True)
    )
    status: FilmStatus = Field(
        sa_column=Column(pg.VARCHAR, nullable=False)
    )
    
    user: "User" = Relationship(back_populates="film_links")
    film: "Film" = Relationship(back_populates="user_links")



class Film(SQLModel, table=True):
    __tablename__ = "films"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True, default=uuid.uuid4)
    )
    apiId: int = Field(default=None)
    title: str = Field(nullable=False)
    year: Optional[int] = None
    poster: Optional[str] = None
    
    user_links: List["UserFilmLink"] = Relationship(back_populates="film")
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
    
    film_links: List["UserFilmLink"] = Relationship(back_populates="user")
    films: List["Film"] = Relationship(
        back_populates="users", link_model=UserFilmLink
    )
