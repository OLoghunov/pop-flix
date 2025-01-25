import httpx
from typing import List

from src.config import Config
from .schemas import (
    SearchFilmModel,
    RatingModel,
    GenreModel,
    FilmDetailModel,
    PosterModel,
)


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
        return film
