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


class FilmGenreLink(SQLModel, table=True):
    __tablename__ = "film_genres"

    film_uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID, ForeignKey("films.uid", ondelete="CASCADE"), primary_key=True
        )
    )
    genre_id: int = Field(
        sa_column=Column(
            pg.INTEGER, ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True
        )
    )


class Genre(SQLModel, table=True):
    __tablename__ = "genres"

    id: int = Field(sa_column=Column(pg.INTEGER, primary_key=True, autoincrement=True))
    name: str = Field(sa_column=Column(pg.VARCHAR, unique=True, nullable=False))

    films: List["Film"] = Relationship(
        back_populates="genres",
        link_model=FilmGenreLink,
    )


class UserFilmLink(SQLModel, table=True):
    __tablename__ = "user_film_association"

    user_uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID, ForeignKey("users.uid", ondelete="CASCADE"), primary_key=True
        )
    )
    film_uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID, ForeignKey("films.uid", ondelete="CASCADE"), primary_key=True
        )
    )
    status: FilmStatus = Field(sa_column=Column(pg.VARCHAR, nullable=False))

    user: "User" = Relationship(back_populates="film_links")
    film: "Film" = Relationship(back_populates="user_links")


class Film(SQLModel, table=True):
    __tablename__ = "films"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True, default=uuid.uuid4)
    )
    apiId: int = Field(default=None)
    tmdbId: int = Field(default=None)
    title: str = Field(nullable=False)
    year: Optional[int] = None
    poster: Optional[str] = None

    user_links: List["UserFilmLink"] = Relationship(back_populates="film")
    users: List["User"] = Relationship(back_populates="films", link_model=UserFilmLink)
    genres: List["Genre"] = Relationship(
        back_populates="films",
        link_model=FilmGenreLink,
        sa_relationship_kwargs={"lazy": "selectin"},
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
    films: List["Film"] = Relationship(back_populates="users", link_model=UserFilmLink)
