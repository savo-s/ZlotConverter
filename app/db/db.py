from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy import String
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeMeta, Mapped, mapped_column, declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./database.db"

Base: DeclarativeMeta = declarative_base()
engine = create_async_engine(DATABASE_URL, echo=False)
async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


class User(SQLAlchemyBaseUserTableUUID, Base):
    """
    Extra field `username` is UNIQUE and **required** at registration time.
    E-mail stays because FastAPI-Users uses it internally.
    """
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def create_db_and_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
