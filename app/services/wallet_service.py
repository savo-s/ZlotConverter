import logging
from typing import Dict, Any

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Wallet, User
from app.services.nbp_api_service import NbpApiService


logger = logging.getLogger(__name__)


class WalletService:

    def __init__(self, db: AsyncSession, current_user: User) -> None:
        self.db = db
        self.current_user = current_user
        self.user_id = current_user.id

        nbp = NbpApiService()
        self.ask_prices = nbp.get_ask_prices()
        self.currency_codes = set(self.ask_prices)

    def _validate_currency(self, currency: str) -> str:
        code = currency.upper()
        if code not in self.currency_codes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Currency '{currency}' does not exist on the NBP exchange.",
            )
        return code

    async def _get_wallet_row(self, currency: str) -> Wallet | None:
        stmt = (
            select(Wallet)
            .where(Wallet.user_id == self.user_id, Wallet.currency == currency)
            .limit(1)
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()

    # --------------------------------------------------- #
    #  Public API                                         #
    # --------------------------------------------------- #

    async def get_my_wallet(self) -> Dict[str, Any]:
        """
        Returns:
            {
                "balances": {"EUR": 100.0, "USD": 20.0, ...},
                "total_pln": 718.0
            }
        """
        stmt = select(Wallet).where(Wallet.user_id == self.user_id)
        result = await self.db.execute(stmt)
        rows = result.scalars().all()

        balances: dict[str, float] = {}
        total_pln: float = 0.0

        for row in rows:
            balances[row.currency] = row.amount
            total_pln += row.amount * self.ask_prices.get(row.currency, 0.0)

        return {"balances": balances, "total_pln": round(total_pln, 2)}

    async def add_currency_amount(self, currency: str, amount: float) -> Dict[str, float]:
        if amount <= 0:
            raise HTTPException(status_code=400, detail="Amount must be positive.")

        code = self._validate_currency(currency)
        row = await self._get_wallet_row(code)

        if row:
            row.amount += amount
        else:
            row = Wallet(user_id=self.user_id, currency=code, amount=amount)
            self.db.add(row)

        await self.db.commit()
        await self.db.refresh(row)

        return {code: round(row.amount, 8)}

    async def sub_currency_amount(self, currency: str, amount: float) -> Dict[str, float]:
        if amount <= 0:
            raise HTTPException(status_code=400, detail="Amount must be positive.")

        code = self._validate_currency(currency)
        row = await self._get_wallet_row(code)

        if not row:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User has zero balance for {code}.",
            )

        if row.amount < amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient funds in {code} balance.",
            )

        row.amount -= amount

        # auto-cleanup if balance hits zero
        if row.amount == 0:
            await self.db.delete(row)
            await self.db.commit()
            return {code: 0.0}

        await self.db.commit()
        await self.db.refresh(row)
        return {code: round(row.amount, 8)}

    async def delete_currency(self, currency: str) -> Dict[str, str]:
        code = self._validate_currency(currency)
        row = await self._get_wallet_row(code)

        if not row:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User has zero balance for {code}.",
            )

        await self.db.delete(row)
        await self.db.commit()
        return {"deleted": code}
