# Setup

## Objetivo
Documentar o fluxo estavel de execucao local do `account-service`.

## Execucao Via Workspace

Da raiz do repositorio:

```bash
uv run --package account-service uvicorn account_service.main:app --reload --host 0.0.0.0 --port 8000
```

## Execucao Via Docker Compose

```bash
docker compose up -d postgres account-service
docker compose logs -f account-service
```

## Ambiente

- Arquivo de referencia: `.env.example`
- Variaveis obrigatorias para sessao JWT: `APP_JWT_SECRET` (e opcionalmente `APP_JWT_ALGORITHM`).
- Bootstrap opcional do primeiro admin: `APP_BOOTSTRAP_ADMIN_*`.
