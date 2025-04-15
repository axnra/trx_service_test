from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class WalletIn(BaseModel):
    """Schema for incoming wallet address in POST request."""
    wallet_address: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"wallet_address": "TXYZ1234567890"}
            ]
        }
    }


class WalletOut(BaseModel):
    """Schema representing wallet data fetched from Tron network."""
    wallet_address: str
    balance: int
    energy: int
    bandwidth: int


class WalletDB(WalletOut):
    """Schema representing a stored wallet request in the database."""
    id: int
    success: bool
    error_message: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
