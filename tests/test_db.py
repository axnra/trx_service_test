import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import create_wallet_record
from app.schemas import WalletOut
from app.models import WalletRequest


@pytest.mark.asyncio
async def test_create_wallet_record_success(async_session: AsyncSession):
    """
    Unit test for successful wallet record creation.

    Verifies that a wallet with valid data is properly stored
    in the database with all fields correctly set.
    """
    data = WalletOut(
        wallet_address="mock_trongrid_address",
        balance=123456789,
        energy=5000,
        bandwidth=3000,
    )

    record = await create_wallet_record(async_session, data)

    assert isinstance(record, WalletRequest)
    assert record.id is not None

    assert record.wallet_address == data.wallet_address
    assert record.balance == data.balance
    assert record.energy == data.energy
    assert record.bandwidth == data.bandwidth

    assert record.success is True
    assert record.error_message is None
    assert record.created_at is not None


@pytest.mark.asyncio
async def test_create_wallet_record_failure(async_session: AsyncSession):
    """
    Unit test for failed wallet record creation.

    Simulates a failed fetch by setting success=False and verifies
    that the error message is stored and other fields remain consistent.
    """
    data = WalletOut(
        wallet_address="mock_trongrid_address",
        balance=0,
        energy=0,
        bandwidth=0,
    )

    error_message = "Address format is invalid"

    record = await create_wallet_record(
        async_session,
        data,
        success=False,
        error_message=error_message,
    )

    assert isinstance(record, WalletRequest)
    assert record.id is not None

    assert record.wallet_address == data.wallet_address
    assert record.balance == 0
    assert record.success is False
    assert record.error_message == error_message
    assert record.created_at is not None
