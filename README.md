# Tron Wallet Info Service

A simple microservice that fetches balance, energy, and bandwidth info for a TRON wallet address.  
Built with **FastAPI**, **SQLAlchemy**, and **TronPy**.  
Each request is stored in the database for future retrieval.

## Features

- **POST /address** — Accepts a TRON wallet address, fetches info from the network, and saves it in the DB.
- **GET /records** — Returns saved requests with pagination.
- Handles invalid addresses and network failures gracefully.
- Includes **unit** and **integration tests**.

---

## Requirements

- Python 3.12
- [Poetry](https://python-poetry.org/) (>=1.8)
- (Optional) Docker & Docker Compose

---

### 📮 Example Requests

#### 🔸 Fetch wallet information

```bash
curl -X POST http://localhost:8000/address \
  -H "Content-Type: application/json" \
  -d '{"wallet_address": "TXYZ1234567890"}'
```

#### 🔸 Fetch stored wallet request records

```bash
curl "http://localhost:8000/records?limit=5&offset=0"
```

---

### 🧾 Possible Response Codes

| Code | Description                       |
|------|-----------------------------------|
| 200  | Successful response               |
| 400  | Invalid or missing wallet address |
| 503  | Tron API unavailable              |
| 500  | Internal server error             |

---

### 🧱 Example Request Payload

```json
{
  "wallet_address": "TXYZ1234567890"
}
```

> ⚠️ The address must be a valid Base58Check TRON wallet address.  
> It should start with `T`, be 34 characters long, and must not contain `0`, `O`, `I`, or `l`.

## 🚀 Quickstart

### 1. Clone and install dependencies

```bash
git clone https://github.com/axnra/trx-service-test.git
cd trx-service-test
poetry install
```

### 2. Run app locally (SQLite)

```bash
uvicorn app.main:app --reload
```

Visit: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🗃️ Local development DB setup (SQLite)

To initialize the database for local development using SQLite:

```bash
poetry run python init_db.py
```

This will create a `local.db` file in the project root using the defined models.
Make sure your `.env` has the following entry (or use the default):

```dotenv
DATABASE_URL=sqlite+aiosqlite:///./local.db
```

This avoids the need for Docker or PostgreSQL during development.

## 📜 Logs

Application logs are saved to `logs/app.log` with rotation:
- Max file size: **1 MB**
- Retention: **10 days**

Logs are also printed to **stdout** for easier debugging during development.

## 🧪 Running tests

Uses SQLite in-memory.

```bash
poetry run pytest
```

> 🧠 Tests use an in-memory SQLite database for speed and isolation. Production uses PostgreSQL.

All tests live in the `/tests` directory.

---

> ℹ️ **Note:** The `DATABASE_URL` is set directly in `docker-compose.yml`. You don't need a `.env` file when using Docker.

## 🐳 Run with Docker

Uses PostgreSQL.

```bash
docker compose up --build
```

Visit: [http://localhost:8000](http://localhost:8000)