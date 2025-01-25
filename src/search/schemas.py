from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class RatingModel(BaseModel):
    kp: Optional[float] = Field(None)
    imdb: Optional[float] = Field(None)
    filmCritics: Optional[float] = Field(None)
    await_: Optional[float] = Field(None, alias="await")


class GenreModel(BaseModel):
    name: str = Field(...)


class PosterModel(BaseModel):
    url: Optional[str] = Field(None)
    previewUrl: Optional[str] = Field(None)
    

class SearchFilmModel(BaseModel):
    id: int
    title: Optional[str] = None
    titleRu: Optional[str] = None
    altTitle: Optional[str] = None
    year: Optional[int] = None
    rating: Optional[RatingModel] = None
    genre: List[GenreModel] = []
    description: Optional[str] = None
    poster: Optional[PosterModel] = None


class FilmDetailModel(BaseModel):
    id: int
    title: Optional[str] = Field(None, alias="name")
    title_en: Optional[str] = Field(None, alias="alternativeName")
    year: Optional[int] = Field(None)
    rating: Optional[RatingModel] = Field(None)
    genre: List[GenreModel] = Field(alias="genres")
    description: Optional[str] = Field(None)
    poster: Optional[PosterModel] = Field(None)
