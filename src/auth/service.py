import uuid

from src.db.models import User, UserFilmLink
from src.search.schemas import FilmShortModel, UserResponseModel
from .schemas import UserCreateModel
from .utils import generatePasswordHash
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import selectinload


class UserService:
    async def getUserByEmail(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)

        user = result.first()

        return user

    async def userExists(self, email: str, session: AsyncSession):
        user = await self.getUserByEmail(email, session)

        return user is not None

    async def createUser(self, userData: UserCreateModel, session: AsyncSession):
        userDataDict = userData.model_dump()
        newUser = User(**userDataDict)
        newUser.passwordHash = generatePasswordHash(userDataDict["password"])
        newUser.role = "user"

        session.add(newUser)
        await session.commit()

        return newUser

    async def updateUser(self, user: User, userData: dict, session: AsyncSession):
        for key, val in userData.items():
            setattr(user, key, val)

        await session.commit()

        return user

    async def getUserWithFilms(self, userUid: uuid.UUID, session: AsyncSession):
        result = await session.exec(
            select(User)
            .where(User.uid == userUid)
            .options(selectinload(User.film_links).joinedload(UserFilmLink.film))
        )
        user_with_links = result.first()

        if not user_with_links:
            raise Exception("User not found")

        films = [
            FilmShortModel(
                id=link.film.apiId,
                title=link.film.title,
                year=link.film.year,
                poster=link.film.poster,
                status=link.status,
            )
            for link in user_with_links.film_links
        ]

        return UserResponseModel(**user_with_links.model_dump(), films=films)
