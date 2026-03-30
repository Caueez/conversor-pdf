FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml ./pyproject.toml
COPY uv.lock ./uv.lock
COPY backend/infra/pyproject.toml ./backend/infra/pyproject.toml
COPY backend/services/account-service/pyproject.toml ./backend/services/account-service/pyproject.toml
COPY backend/services/account-service/README.md ./backend/services/account-service/README.md

COPY backend ./backend

RUN uv sync --frozen --package account-service || uv sync --package account-service

ENV PYTHONPATH=/app/backend/services/account-service/src:/app/backend/infra/src

EXPOSE 8000

CMD ["uv", "run", "--package", "account-service", "uvicorn", "account_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
