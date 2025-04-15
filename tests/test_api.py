import pytest
from unittest.mock import patch
from app.schemas import WalletOut
from app.crud import create_wallet_record


@pytest.mark.asyncio
@patch("app.routes.address.tron.get_wallet_info")
async def test_post_address(mock_get_wallet_info, client):
    """
    Integration test for POST /address endpoint with mocked Tron API.

    Ensures that the response contains expected fields and successful flag.
    """
    mock_get_wallet_info.return_value = {
        "wallet_address": "mock_trongrid_address",
        "balance": 9999999,
        "energy": 1111,
        "bandwidth": 2222,
    }

    payload = {"wallet_address": "mock_trongrid_address"}
    response = await client.post("/address", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["wallet_address"] == payload["wallet_address"]
    assert data["balance"] == 9999999
    assert data["success"] is True
    assert "created_at" in data


@pytest.mark.asyncio
async def test_get_records(client, async_session):
    """
    Integration test for GET /records endpoint.

    Ensures that newly created record appears in the response.
    """
    wallet = WalletOut(
        wallet_address="mock_trongrid_address",
        balance=123456789,
        energy=1000,
        bandwidth=2000
    )
    await create_wallet_record(async_session, wallet)

    response = await client.get("/records?limit=5&offset=0")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert any(record["wallet_address"] == "mock_trongrid_address" for record in data)
