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

## 🧪 Running tests

Uses SQLite in-memory.

```bash
poetry run pytest
```

All tests live in the `/tests` directory.

---

## 🐳 Run with Docker

Uses PostgreSQL.

```bash
docker compose up --build
```

Visit: [http://localhost:8000](http://localhost:8000)
