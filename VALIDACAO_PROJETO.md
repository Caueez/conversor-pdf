# Validacao Tecnica do Projeto

Data da validacao: 2026-03-24

## Critico

- Hash de senha usando `sha256` puro sem salt (`domain/value_objects/user.py`). Em producao, use `argon2` ou `bcrypt`.

## Alto

- Endpoints com `except Exception` generico (`api/routes/user.py`), escondendo causa real e dificultando observabilidade.
- Mensagem de excecao retornada para cliente (`{"message": str(e)}`), com risco de vazamento de detalhe interno.
- Ausencia de suite de testes automatizados (`tests/`, `pytest`, `unittest` nao encontrados).
- Build de container potencialmente nao deterministico (`uv sync --frozen ... || uv sync ...`) sem lock dedicado do servico.

## Medio

- Defaults de infraestrutura no codigo (`POSTGRES_DSN` em `settings.py`) em vez de depender de ambiente externo.
- Servico `account-service` sem `env_file`/`environment` explicito no `docker-compose.yml`.
- PostgreSQL no `docker-compose.yml` sem volume persistente.
- Migrations executadas no startup sem versionamento/rollback.

## Baixo

- Nome do metodo `conect` em vez de `connect` (`src/infra/database/implementations/postgres.py`).
- `trace_id` lido no endpoint e nao usado em logs/observabilidade.
- `README` do servico ainda vazio (`src/services/account-service/README.md`).

## Pontos Positivos

- Separacao arquitetural clara em camadas: API, Application, Domain e Infra.
- Queries SQL parametrizadas (boa base contra SQL injection).
- Lifecycle da aplicacao com `startup`/`shutdown` definido no FastAPI.
- `docker compose watch` configurado para produtividade no desenvolvimento.
