from typing import List

from fastapi import APIRouter, status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from .schemas import SearchFilmModel
from .service import SearchService
from src.db.main import getSession

searchRouter = APIRouter()
searchService = SearchService()

@searchRouter.get("/{filmName}", response_model=List[SearchFilmModel])
async def getFilmByName(
    filmName: str,
    session: AsyncSession = Depends(getSession)
):
    films = await searchService.findFilms(filmName, session)
    return films
