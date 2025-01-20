from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class RatingModel(BaseModel):
    kp: Optional[float] = None
    imdb: Optional[float] = None
    filmCritics: Optional[float] = None
    awaitReward: Optional[float] = None

class GenreModel(BaseModel):
    name: str

class SearchFilmModel(BaseModel):
    id: int
    title: Optional[str] = None
    titleRu: Optional[str] = None
    altTitle: Optional[str] = None
    year: Optional[int] = None
    rating: Optional[RatingModel] = None
    genre: List[GenreModel] = []
    description: Optional[str] = None
    poster_url: Optional[str] = None