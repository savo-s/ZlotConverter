from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import Boolean, Column, Integer, String
from db import Base


class Wallet(SQLModel, table=True):
    __tablename__ = "wallets"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    currency: str = Field(index=True, min_length=3, max_length=3)
    amount: float = Field(gt=0)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)