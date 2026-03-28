# Testes Do account-service

## Suites

- `smoke`: fluxo critico rapido para feedback local/pre-PR.
- `unit`: regras de negocio, validacoes e componentes internos sem dependencias externas.
- `integration`: adapters e componentes de infra usando Postgres real.
- `e2e`: fluxo HTTP completo com app + banco real.
- `contract`: validacao de status e shape dos endpoints documentados.

## Pre-requisitos

- Para `integration`/`e2e`, subir Postgres local:
  - `docker compose up -d postgres`

## Comandos

```bash
uv run --package account-service pytest src/services/account-service/tests -m smoke -q
uv run --package account-service pytest src/services/account-service/tests -m unit --cov=account_service --cov=infra --cov-branch --cov-report=term-missing --cov-fail-under=90
APP_TEST_POSTGRES_DSN=postgresql://postgres:postgres@127.0.0.1:5432/user_service uv run --package account-service pytest src/services/account-service/tests -m integration
APP_TEST_POSTGRES_DSN=postgresql://postgres:postgres@127.0.0.1:5432/user_service uv run --package account-service pytest src/services/account-service/tests -m "e2e or contract"
APP_TEST_POSTGRES_DSN=postgresql://postgres:postgres@127.0.0.1:5432/user_service uv run --package account-service pytest src/services/account-service/tests
```
