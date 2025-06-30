import os
from pathlib import Path
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.db.base import Base

DATABASE_URL = os.getenv("DATABASE_URL")

# ensure ./data exists for SQLite
if DATABASE_URL.startswith("sqlite"):
    db_path = Path(DATABASE_URL.split("///", 1)[-1])
    db_path.parent.mkdir(parents=True, exist_ok=True)

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def create_db_and_tables():
    """
    • For SQLite → check if the file exists; if not, create tables.
    • For other DBs → inspect the metadata; create tables only if at
      least one of our tables is missing.
    """

    # ----------- SQLITE shortcut ----------------------------------
    if db_path and db_path.exists():
        return  # DB file already present → assume schema exists

    # ----------- Generic check (Postgres, MySQL, etc.) ------------
    async with engine.begin() as conn:
        inspector = inspect(conn)
        existing_tables = set(await inspector.get_table_names())
        required_tables = set(Base.metadata.tables)

        if required_tables.issubset(existing_tables):
            # All our tables already exist → nothing to do
            return

        # At least one table missing → create the full schema
        await conn.run_sync(Base.metadata.create_all)
