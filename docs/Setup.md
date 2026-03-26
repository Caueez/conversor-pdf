# Setup

## Objetivo
Concentrar instrucoes estaveis para preparar e executar o projeto localmente.

## Pre-Requisitos

- Python 3.12+
- `uv`
- Docker e Docker Compose

## Sincronizacao Do Workspace

```bash
uv lock
uv sync --all-packages
```

## Execucao (Compose)

```bash
docker compose up -d postgres account-service
docker compose logs -f account-service
```

## Referencias

- Guia de setup do servico: [account-service/docs/Setup.md](../src/services/account-service/docs/Setup.md)
- Variaveis de ambiente do servico: `src/services/account-service/.env.example`
