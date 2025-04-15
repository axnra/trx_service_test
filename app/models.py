from sqlalchemy import Column, String, Integer, BigInteger, DateTime, Boolean
from datetime import datetime, timezone
from app.db import Base


class WalletRequest(Base):
    """Database model representing a single wallet request log."""

    __tablename__ = "wallet_requests"

    id = Column(Integer, primary_key=True, index=True)
    wallet_address = Column(String, index=True, nullable=False)

    balance = Column(BigInteger, nullable=True)
    energy = Column(BigInteger, nullable=True)
    bandwidth = Column(BigInteger, nullable=True)

    success = Column(Boolean, default=True, nullable=False)
    error_message = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.now(timezone.utc))
