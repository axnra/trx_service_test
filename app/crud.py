from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import WalletRequest
from app.schemas import WalletOut


async def create_wallet_record(
    session: AsyncSession,
    data: WalletOut,
    success: bool = True,
    error_message: str | None = None,
) -> WalletRequest:
    """
    Creates a new wallet record in the database.

    Args:
        session (AsyncSession): Database session.
        data (WalletOut): Parsed wallet data.
        success (bool, optional): Indicates if the retrieval was successful. Defaults to True.
        error_message (str | None, optional): Error description if failed. Defaults to None.

    Returns:
        WalletRequest: The created record.
    """
    record = WalletRequest(
        wallet_address=data.wallet_address,
        balance=data.balance,
        energy=data.energy,
        bandwidth=data.bandwidth,
        success=success,
        error_message=error_message,
    )
    session.add(record)
    await session.commit()
    await session.refresh(record)
    return record


async def get_wallet_records(
    session: AsyncSession,
    limit: int = 10,
    offset: int = 0,
) -> Sequence[WalletRequest]:
    """
    Retrieves wallet records with pagination.

    Args:
        session (AsyncSession): Database session.
        limit (int, optional): Number of records to retrieve. Defaults to 10.
        offset (int, optional): Number of records to skip. Defaults to 0.

    Returns:
        Sequence[WalletRequest]: List of retrieved records.
    """
    result = await session.execute(
        select(WalletRequest)
        .order_by(WalletRequest.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    return result.scalars().all()
