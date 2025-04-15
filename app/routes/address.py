from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.schemas import WalletIn, WalletDB, WalletOut
from app.db import get_session
from app.tron import TronClient
from app.crud import create_wallet_record, get_wallet_records
from app.deps import get_tron_client
from app.logger import logger
router = APIRouter(tags=["Wallet API"])


@router.post("/address", response_model=WalletDB, responses={
        200: {"description": "Successful response"},
        400: {"description": "Invalid wallet address"},
        503: {"description": "Tron API unavailable"},
        500: {"description": "Internal server error"},
    })
async def fetch_wallet_info(
    payload: WalletIn,
    session: AsyncSession = Depends(get_session),
    tron: TronClient = Depends(get_tron_client)
):
    """
    Fetch wallet info by address and store the result in the database.

    Returns 200 with data if successful,
    400 for invalid address or not found,
    503 if external API is unavailable,
    500 for unexpected server errors.
    """
    logger.info(f"→ Request to /address: {payload.wallet_address}")

    try:
        data = await tron.get_wallet_info(payload.wallet_address)
        wallet_out = WalletOut(**data)
        return await create_wallet_record(session, wallet_out)

    except ValueError as e:
        return await _handle_error(session, payload.wallet_address, str(e), 400)

    except ConnectionError as e:
        return await _handle_error(session, payload.wallet_address, str(e), 503)

    except Exception as e:
        return await _handle_error(session, payload.wallet_address, f"Unexpected error: {e}", 500)


async def _handle_error(
    session: AsyncSession,
    wallet_address: str,
    error_message: str,
    status_code: int
):
    logger.error(f"[{status_code}] Error for {wallet_address}: {error_message}")

    fake = WalletOut(
        wallet_address=wallet_address,
        balance=0,
        energy=0,
        bandwidth=0,
    )
    await create_wallet_record(
        session, fake, success=False, error_message=error_message
    )
    raise HTTPException(status_code=status_code, detail=error_message)


@router.get("/records", response_model=List[WalletDB], responses={
    200: {"description": "Successful Response"},
    422: {"description": "Validation Error"}
})
async def list_wallet_records(
    limit: int = Query(10, ge=0),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session)
):
    """
    Return a paginated list of wallet records stored in the database.
    """
    return await get_wallet_records(session, limit, offset)
