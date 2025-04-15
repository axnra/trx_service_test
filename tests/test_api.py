import pytest
from unittest.mock import MagicMock

from app.schemas import WalletOut
from app.crud import create_wallet_record
from app.tron import TronClient
from app.deps import get_tron_client
from app.main import app


@pytest.mark.asyncio
async def test_post_address(client):
    """
    Integration test for POST /address endpoint with mocked Tron API.

    Ensures that the response contains expected fields and successful flag.
    """
    mock_tron = MagicMock(spec=TronClient)
    mock_tron.get_wallet_info.return_value = {
        "wallet_address": "mock_trongrid_address",
        "balance": 9999999,
        "energy": 1111,
        "bandwidth": 2222,
    }

    app.dependency_overrides[get_tron_client] = lambda: mock_tron  # type: ignore

    payload = {"wallet_address": "mock_trongrid_address"}
    response = await client.post("/address", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["wallet_address"] == payload["wallet_address"]
    assert data["balance"] == 9999999
    assert data["success"] is True
    assert "created_at" in data

    app.dependency_overrides.clear()  # type: ignore


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


@pytest.mark.asyncio
async def test_post_address_with_none_fields(client):
    """
    Test POST /address with mocked Tron API returning None in balance-related fields.

    Ensures that fields with None values are correctly handled and stored,
    and that the response remains valid.
    """
    mock_tron = MagicMock(spec=TronClient)
    mock_tron.get_wallet_info.return_value = {
        "wallet_address": "TXYZmock123",
        "balance": None,
        "energy": None,
        "bandwidth": None,
    }

    app.dependency_overrides[get_tron_client] = lambda: mock_tron  # type: ignore

    payload = {"wallet_address": "TXYZmock123"}
    response = await client.post("/address", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["wallet_address"] == payload["wallet_address"]
    assert data["balance"] is None
    assert data["energy"] is None
    assert data["bandwidth"] is None
    assert data["success"] is True

    app.dependency_overrides.clear()  # type: ignore


@pytest.mark.asyncio
async def test_get_records_with_large_offset(client):
    """
    Test GET /records with an offset that exceeds existing records.

    Ensures that an empty list is returned and the request succeeds.
    """
    response = await client.get("/records?limit=10&offset=99999")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


@pytest.mark.asyncio
async def test_post_invalid_address(client):
    """
    Test POST /address with an invalid Tron address format.

    Ensures that validation fails and the response returns 400 with appropriate detail.
    """
    payload = {"wallet_address": "123"}
    response = await client.post("/address", json=payload)

    assert response.status_code == 400
    assert "Invalid Tron address format" in response.json()["detail"]


@pytest.mark.asyncio
async def test_post_empty_address(client):
    """
    Test POST /address with an empty wallet address.

    Ensures that min_length validation triggers and returns 400 with a proper schema error.
    """
    payload = {"wallet_address": ""}
    response = await client.post("/address", json=payload)

    assert response.status_code == 400
    detail = response.json()["detail"]
    assert isinstance(detail, list)
    assert any(
        d["type"] == "string_too_short" and d["loc"] == ["body", "wallet_address"]
        for d in detail
    )


@pytest.mark.asyncio
async def test_post_address_api_unavailable(client):
    """
    Test POST /address when the Tron API is unavailable.

    Simulates a network failure by raising ConnectionError in the mocked TronClient.
    Expects a 503 Service Unavailable response with a relevant error message.
    """
    mock_tron = MagicMock(spec=TronClient)
    mock_tron.get_wallet_info.side_effect = ConnectionError("Network error")
    app.dependency_overrides[get_tron_client] = lambda: mock_tron  # type: ignore

    payload = {"wallet_address": "TXYZmock123"}
    response = await client.post("/address", json=payload)

    assert response.status_code == 503
    assert "Network error" in response.json()["detail"]

    app.dependency_overrides.clear()  # type: ignore


@pytest.mark.asyncio
async def test_post_address_unexpected_error(client):
    """
    Test POST /address when an unexpected exception occurs.

    Simulates an internal server error and checks for 500 response.
    """
    mock_tron = MagicMock(spec=TronClient)
    mock_tron.get_wallet_info.side_effect = Exception("Unexpected error")
    app.dependency_overrides[get_tron_client] = lambda: mock_tron  # type: ignore

    payload = {"wallet_address": "TXYZmock123"}
    response = await client.post("/address", json=payload)

    assert response.status_code == 500
    assert "Unexpected error" in response.json()["detail"]

    app.dependency_overrides.clear()  # type: ignore
