from pydantic import BaseModel, ConfigDict, field_validator, Field
from datetime import datetime
from typing import Optional
from tronpy.keys import is_base58check_address


class WalletIn(BaseModel):
    """Schema for incoming wallet address in POST request."""
    wallet_address: str = Field(..., min_length=1)

    model_config = {
        "strict": True,
        "json_schema_extra": {
            "examples": [{"wallet_address": "TXYZ1234567890"}]
        }
    }

    @classmethod
    @field_validator("wallet_address")
    def validate_address(cls, v: str) -> str:
        if not is_base58check_address(v):
            raise ValueError("Invalid Tron address format")
        return v


class WalletOut(BaseModel):
    """Schema representing wallet data fetched from Tron network."""
    wallet_address: str
    balance: Optional[int]
    energy: Optional[int]
    bandwidth: Optional[int]


class WalletDB(WalletOut):
    """Schema representing a stored wallet request in the database."""
    id: int
    success: bool
    error_message: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
