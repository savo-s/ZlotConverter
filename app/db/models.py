import uuid
from sqlalchemy import Column, String, Float
from app.db.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)


class Wallet(Base):
    __tablename__ = "wallets"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), index=True, nullable=False)
    currency = Column(String(3), index=True, nullable=False)
    amount = Column(Float, nullable=False)