from fastapi import APIRouter, Depends, Security, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db import get_db
# from app.db.security import decode_token      # ← uncomment when you add real logic

security_scheme = HTTPBearer(                 # **same name** as in main.py
    scheme_name="BearerAuth",
    bearerFormat="JWT",
    description="Paste your JWT here – format: **Bearer <token>**",
)

router = APIRouter(prefix="/wallet", tags=["Wallet"])


@router.get("", summary="Get current wallet contents")
async def get_wallet(
    credentials: HTTPAuthorizationCredentials = Security(security_scheme),
    db: AsyncSession = Depends(get_db),
):
    """Stub – replace with real wallet lookup."""
    # user_id = decode_token(credentials.credentials)["sub"]  # example
    return {"message": "wallet stub"}


@router.post("/add/{currency}/{amount}", summary="Add amount to wallet currency")
async def add_currency(
    currency: str,
    amount: float,
    credentials: HTTPAuthorizationCredentials = Security(security_scheme),
    db: AsyncSession = Depends(get_db),
):
    """Stub – increment currency balance."""
    return {"message": f"add {amount} {currency} – stub"}


@router.post("/sub/{currency}/{amount}", summary="Subtract amount from wallet currency")
async def sub_currency(
    currency: str,
    amount: float,
    credentials: HTTPAuthorizationCredentials = Security(security_scheme),
    db: AsyncSession = Depends(get_db),
):
    """Stub – decrement currency balance."""
    return {"message": f"subtract {amount} {currency} – stub"}


@router.post("/set/{currency}/{amount}", summary="Set wallet currency amount")
async def set_currency(
    currency: str,
    amount: float,
    credentials: HTTPAuthorizationCredentials = Security(security_scheme),
    db: AsyncSession = Depends(get_db),
):
    """Stub – set currency balance."""
    return {"message": f"set {currency} to {amount} – stub"}


@router.post("/delete/{currency}", summary="Delete (zero-out) wallet currency")
async def delete_currency(
    currency: str,
    credentials: HTTPAuthorizationCredentials = Security(security_scheme),
    db: AsyncSession = Depends(get_db),
):
    """Stub – delete currency or specific amount."""
    return {"message": f"delete {currency} – stub"}
