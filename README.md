# conversor-pdf

Monorepo Python com workspace `uv`, contendo atualmente o serviço `account-service` (FastAPI) e infraestrutura de banco compartilhada (`src/infra`).

## Estrutura

```text
.
├── pyproject.toml                 # workspace root (uv)
├── docker-compose.yml
├── src/
│   ├── infra/
│   │   └── database/
│   └── services/
│       └── account-service/
│           ├── pyproject.toml
│           ├── Dockerfile
│           ├── .env.example
│           └── src/account_service/
└── uv.lock
```

## Requisitos

- Python 3.12+
- `uv`
- Docker + Docker Compose

## Ambiente local (uv workspace)

Na raiz do projeto:

```bash
uv lock
uv sync --all-packages
```

Executar o serviço:

```bash
uv run --package account-service uvicorn account_service.main:app --reload --host 0.0.0.0 --port 8000
```

## Ambiente com Docker Compose

Subir PostgreSQL + API:

```bash
docker compose up -d postgres account-service
```

Ver logs:

```bash
docker compose logs -f account-service
```

Parar serviços:

```bash
docker compose down
```

## Watch (hot reload via Compose)

O `docker-compose.yml` já está configurado com `develop.watch` para:

- `sync+restart` em `src/services/account-service/src/account_service`
- `sync+restart` em `src/infra`
- `rebuild` quando altera `src/services/account-service/pyproject.toml`
- `rebuild` quando altera `src/services/account-service/Dockerfile`

Uso:

```bash
docker compose up -d postgres account-service
docker compose watch account-service
```

## Endpoints atuais

Base URL local: `http://localhost:8000`

- `GET /` lista usuários
- `POST /` cria usuário

Exemplo `POST /`:

```bash
curl -X POST http://localhost:8000/ \
  -H "Content-Type: application/json" \
  -d '{"name":"caue","email":"caue@example.com","password":"12345678"}'
```

## Variáveis de ambiente

Referência: `src/services/account-service/.env.example`

Principais:

- `APP_PERSISTENCE_BACKEND=postgres`
- `APP_POSTGRES_DSN=postgresql://postgres:postgres@postgres:5432/user_service`
- `APP_USER_REPO=postgres`

## Observações

- O schema de banco é criado no startup da aplicação (`infra/migration.py`).
- `README` do serviço pode evoluir depois para documentação mais específica (regras de domínio, fluxos e testes).
