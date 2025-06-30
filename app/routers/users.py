# app/routers/users.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession           # type annotation (optional)

from app.db.database import get_db
from app.db.schemas import UserResponse
from app.dependencies.auth import get_current_user

router = APIRouter(tags=["Users"])


@router.get("/users/me", response_model=UserResponse, summary="Get current user")
async def read_current_user(current_user = Depends(get_current_user)):
    return current_user


@router.delete(
    "/users/me",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete current user account",
)
async def delete_current_user(
    db: AsyncSession = Depends(get_db),         # now resolved
    current_user = Depends(get_current_user),
):
    await db.delete(current_user)
    await db.commit()
