import httpx
from typing import List
import logging
import uuid

from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from src.db.models import User, Film, UserFilmLink, FilmStatus
from src.config import Config
from .schemas import (
    SearchFilmModel,
    FilmDetailModel,
    FilmShortModel,
)
from src.auth.service import UserService


userService = UserService()


class SearchService:
    async def getFilms(self, filmName: str):
        url = f"https://api.kinopoisk.dev/v1.4/movie/search?query={filmName}"
        headers = {"X-API-KEY": Config.KINOPOISK_API_KEY}

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)

        if response.status_code != 200:
            raise Exception(
                f"Error fetching data from Kinopoisk API: {response.status_code}"
            )

        filmsData: List[dict] = response.json()["docs"]
        films = []

        filmsData.sort(key=lambda x: x["rating"]["kp"], reverse=True)

        for film in filmsData:
            films.append(SearchFilmModel.model_validate(film))

        return films

    async def getFilmById(self, filmId: int) -> FilmDetailModel:
        url = f"https://api.kinopoisk.dev/v1.4/movie/{filmId}"

        headers = {"X-API-KEY": Config.KINOPOISK_API_KEY}

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)

        if response.status_code != 200:
            raise Exception(
                f"Error fetching data from Kinopoisk API: {response.status_code} {response.text}"
            )

        film_data = response.json()
        film = FilmDetailModel.model_validate(film_data)
        return film.model_dump(by_alias=True)

    async def addFilmForUser(
        self, filmData: FilmShortModel, currentUser: User, session: AsyncSession
    ):
        film_uid = uuid.uuid5(uuid.NAMESPACE_DNS, str(filmData.id))
        filmStatus = filmData.status
        
        result = await session.exec(select(Film).where(Film.uid == film_uid))
        
        film = result.first()
        if not film:
            film = Film(
                uid=film_uid,
                title=filmData.title,
                year=filmData.year,
                poster=filmData.poster,
                apiId=filmData.id
            )
            session.add(film)
            await session.commit()
            await session.refresh(film)
            
        result = await session.exec(
            select(UserFilmLink).where(
                UserFilmLink.user_uid == currentUser.uid,
                UserFilmLink.film_uid == film.uid,
            )
        )
 
        existing_link = result.first()
        if existing_link:
            if existing_link.status == filmStatus:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Фильм уже в списке {filmStatus.value}",
                )
                
            existing_link.status = filmStatus
            await session.commit()
            
            return {"message": f"Фильм перемещен в список {filmStatus.value}"}
        
        user_film_link = UserFilmLink(
            user_uid=currentUser.uid, film_uid=film.uid, status=filmStatus
        )
        session.add(user_film_link)
        await session.commit()
        
        return {"message": f"Фильм добавлен в список {filmStatus.value}"}

    async def removeFilmForUser(
        self, film_id: int, currentUser: User, session: AsyncSession
    ):
        film_uid = uuid.uuid5(uuid.NAMESPACE_DNS, str(film_id))
        result = await session.exec(
            select(UserFilmLink).where(
                UserFilmLink.user_uid == currentUser.uid,
                UserFilmLink.film_uid == film_uid,
            )
        )
        film_link = result.first()
        
        if not film_link:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Фильм не найден в вашем списке",
            )
        
        await session.delete(film_link)
        await session.commit()
        
        return {"message": "Фильм удален из вашего списка"}
