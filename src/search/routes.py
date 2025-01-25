from typing import List

from fastapi import APIRouter

from .schemas import SearchFilmModel, FilmDetailModel
from .service import SearchService

searchRouter = APIRouter()
searchService = SearchService()


@searchRouter.get("/{filmName}", response_model=List[SearchFilmModel])
async def getFilmByName(filmName: str):
    films = await searchService.getFilms(filmName)

    return films


@searchRouter.get("/film/{filmId}", response_model=FilmDetailModel)
async def getFilmById(filmId: str):
    film = await searchService.getFilmById(filmId)

    return film
