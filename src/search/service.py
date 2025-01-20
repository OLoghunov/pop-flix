import httpx

from sqlmodel.ext.asyncio.session import AsyncSession
from src.config import Config
from .schemas import SearchFilmModel, RatingModel, GenreModel

class SearchService:
    async def findFilms(self, filmName: str, session: AsyncSession):
        url = f"https://api.kinopoisk.dev/v1.4/movie/search?query={filmName}"
        headers = {
            "X-API-KEY": Config.KINOPOISK_API_KEY
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
        
        if response.status_code != 200:
            raise Exception(f"Error fetching data from Kinopoisk API: {response.status_code}")

        filmsData = response.json()["docs"]
        films = []

        for film in filmsData:
            rating_data = film.get("rating", {})
            genre_data = film.get("genres", [])

            rating = RatingModel(
                kp=rating_data.get("kp"),
                imdb=rating_data.get("imdb"),
                filmCritics=rating_data.get("filmCritics"),
                awaitReward=rating_data.get("await")
            ) if rating_data else None

            genres = [GenreModel(name=genre.get("name")) for genre in genre_data]

            film_model = SearchFilmModel(
                id=film.get("id"),
                title=film.get("name"),
                titleRu=film.get("nameRu"),
                altTitle=film.get("alternativeName"),
                year=film.get("year"),
                rating=rating,
                genre=genres,
                description=film.get("description", ""),
                poster_url=film.get("posterUrl", "")
            )

            films.append(film_model)

        return films