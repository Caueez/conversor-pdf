FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY src/services/account-service/pyproject.toml ./pyproject.toml
COPY src/services/account-service/README.md ./README.md
RUN uv sync --frozen --no-install-project || uv sync --no-install-project

COPY src/services/account-service/src/account_service ./src/account_service
COPY src/infra ./src/infra
ENV PYTHONPATH=/app/src

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "account_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
