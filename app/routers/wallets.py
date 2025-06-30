# app/routers/wallets.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.services.wallet_service import WalletService
from app.db.models import User

router = APIRouter(prefix="/wallet", tags=["Wallet"])


# ------------------------------------------------------------------
# Factory dependency that builds a per-request WalletService
# ------------------------------------------------------------------
def get_wallet_service(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> WalletService:
    return WalletService(db, current_user)
# ------------------------------------------------------------------


@router.get("", summary="Get current wallet contents")
async def get_wallet(service: WalletService = Depends(get_wallet_service)):
    return await service.get_my_wallet()


@router.post("/add/{currency}/{amount}", summary="Add amount")
async def add_currency(
    currency: str,
    amount: float,
    service: WalletService = Depends(get_wallet_service),
):
    return await service.add_currency_amount(currency, amount)


@router.post("/sub/{currency}/{amount}", summary="Subtract amount")
async def sub_currency(
    currency: str,
    amount: float,
    service: WalletService = Depends(get_wallet_service),
):
    return await service.sub_currency_amount(currency, amount)


@router.delete("/{currency}", summary="Delete currency from wallet")
async def delete_currency(
    currency: str,
    service: WalletService = Depends(get_wallet_service),
):
    return await service.delete_currency(currency)
