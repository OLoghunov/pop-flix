from typing import List
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from .schemas import SearchFilmModel, FilmDetailModel, FilmShortModel
from .service import SearchService
from src.db.main import getSession
from src.db.models import User, FilmStatus
from src.auth.dependencies import getCurrentUser

searchRouter = APIRouter()
searchService = SearchService()


@searchRouter.get("/{filmName}", response_model=List[SearchFilmModel])
async def getFilmByName(filmName: str):
    films = await searchService.getFilms(filmName)

    return films


@searchRouter.post("/film")
async def addFilmToUser(
    filmData: FilmShortModel,
    currentUser: User = Depends(getCurrentUser),
    session: AsyncSession = Depends(getSession),
):
    try:
        newFilm = await searchService.addFilmForUser(
            filmData=filmData, currentUser=currentUser, session=session
        )
        return JSONResponse(content=newFilm)

    except HTTPException as e:
        raise e

    except Exception as e:
        logging.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Oops... Something went wrong",
        )


@searchRouter.delete("/film/{filmId}")
async def removeFilmFromUser(
    filmId: int,
    currentUser: User = Depends(getCurrentUser),
    session: AsyncSession = Depends(getSession),
):
    try:
        response = await searchService.removeFilmForUser(
            film_id=filmId, currentUser=currentUser, session=session
        )
        return JSONResponse(content=response)

    except HTTPException as e:
        raise e

    except Exception as e:
        logging.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Oops... Something went wrong",
        )


@searchRouter.get("/film/{filmId}", response_model=FilmDetailModel)
async def getFilmById(filmId: str):
    film = await searchService.getFilmById(filmId)

    return JSONResponse(content=film)
