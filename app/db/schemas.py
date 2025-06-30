from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class WalletOperation(BaseModel):
    currency: str
    amount: float


class UserResponse(BaseModel):
    id: str
    username: str

