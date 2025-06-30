from pydantic import BaseModel
import uuid


class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


# class UserUpdate(BaseModel):
#     username: str
#     password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class WalletOperation(BaseModel):
    currency: str
    amount: float


class UserResponse(BaseModel):
    id: str
    username: str

# class WalletItem(BaseModel):
#     currency: str
#     amount: float
#     pln_value: float
#
#
# class WalletResponse(BaseModel):
#     items: list[WalletItem]
#     total_pln: float
