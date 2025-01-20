from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import Config
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker


asyncEngine = AsyncEngine(create_engine(url=Config.DATABASE_URL, echo=True))


async def getSession():
    Session = sessionmaker(
        bind=asyncEngine, class_=AsyncSession, expire_on_commit=False
    )

    async with Session() as session:
        yield session