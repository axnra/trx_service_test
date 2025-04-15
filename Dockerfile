# Stage 1: build dependencies
FROM python:3.12-slim AS builder

ENV POETRY_VERSION=1.8.2
ENV POETRY_NO_INTERACTION=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl \
    && pip install --no-cache-dir poetry==$POETRY_VERSION

WORKDIR /app

# Copy only dependency files first for better cache
COPY pyproject.toml poetry.lock ./

# Disable virtualenvs and install only runtime dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-root

# Stage 2: runtime
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy installed dependencies from builder
COPY --from=builder /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy app source code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
