from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging

from app.db.db import get_db, User
from app.db.schemas import UserResponse
from app.db.security import decode_token

logger = logging.getLogger(__name__)

# keep the scheme-name identical to the one declared in main.py
security_scheme = HTTPBearer(
    scheme_name="BearerAuth",
    bearerFormat="JWT",
    description="Paste your JWT here:",
)

router = APIRouter(prefix="", tags=["Users"])


@router.get(
    "/users/me",
    response_model=UserResponse,
    summary="Get current user information",
)
async def read_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security_scheme),
    db: AsyncSession = Depends(get_db),
):
    """Return the user represented by the supplied JWT."""
    token = credentials.credentials
    try:
        payload = decode_token(token)
        username: str | None = payload.get("sub")
    except Exception as exc:
        logger.error("Token decode error: %s", exc)
        raise HTTPException(status_code=401, detail="Invalid token")

    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")

    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.delete(
    "/users/me",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete current user account",
)
async def delete_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security_scheme),
    db: AsyncSession = Depends(get_db),
):
    """Delete the account identified by the supplied JWT."""
    token = credentials.credentials
    try:
        payload = decode_token(token)
        username: str | None = payload.get("sub")
    except Exception as exc:
        logger.error("Token decode error: %s", exc)
        raise HTTPException(status_code=401, detail="Invalid token")

    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")

    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()
    return {"message": "User deleted successfully"}
