import os
import uuid
from sqlalchemy import Column, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker


# Create data directory

DATABASE_URL = os.getenv("DATABASE_URL")
Base = declarative_base()
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    def __init__(self, **kwargs):
        # Ensure ID is always a string
        if 'id' not in kwargs:
            kwargs['id'] = str(uuid.uuid4())
        super().__init__(**kwargs)


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), index=True)
    currency = Column(String(3), index=True)
    amount = Column(Float)

    def __init__(self, **kwargs):
        # Ensure ID is always a string
        if 'id' not in kwargs:
            kwargs['id'] = str(uuid.uuid4())
        super().__init__(**kwargs)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def create_db_and_tables():
    # Create database file if it doesn't exist
    db_file = DATA_DIR / "database.db"
    if not db_file.exists():
        db_file.touch()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)