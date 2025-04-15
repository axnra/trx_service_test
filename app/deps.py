from app.tron import TronClient
from app.db import get_session

__all__ = ["get_session", "get_tron_client"]

_tron_client: TronClient | None = None


def get_tron_client() -> TronClient:
    global _tron_client
    if _tron_client is None:
        _tron_client = TronClient()
    return _tron_client
