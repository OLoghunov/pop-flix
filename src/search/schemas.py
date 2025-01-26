from pydantic import BaseModel, Field
from typing import List, Optional


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
   
 
class CountryModel(BaseModel):
    name: str = Field(...)   
    
    
class PersonModel(BaseModel):
    id: int = Field(...)
    photo: Optional[str] = Field(None)
    name: str = Field(...)
    enName: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    profession: str = Field(...)
    enProfession: str = Field(...)
    

class SearchFilmModel(BaseModel):
    id: int
    title: Optional[str] = Field(None, alias="alternativeName")
    titleRu: Optional[str] = Field(None, alias="name")
    altTitle: Optional[str] = Field(None)
    year: Optional[int] = Field(None)
    rating: Optional[RatingModel] = Field(None)
    genre: List[GenreModel] = Field(None)
    description: Optional[str] = Field(None)
    poster: Optional[PosterModel] = Field(None)


class FilmDetailModel(BaseModel):
    id: int
    title: Optional[str] = Field(None, alias="alternativeName")
    titleRu: Optional[str] = Field(None, alias="name") 
    year: Optional[int] = Field(None)
    rating: Optional[RatingModel] = Field(None)
    genre: List[GenreModel] = Field(alias="genres")
    countries: List[CountryModel] = Field(None)
    persons: List[PersonModel] = Field(None)
    description: Optional[str] = Field(None)
    poster: Optional[PosterModel] = Field(None)
