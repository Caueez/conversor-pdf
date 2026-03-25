# Validacao Tecnica do Projeto

Data da validacao: 2026-03-25

## Resumo Executivo

- Estado geral: funcional para desenvolvimento, mas com riscos relevantes de seguranca, API contract e operacao.
- Itens da validacao anterior conferidos: 1 concluido, 11 ainda pendentes.
- Validacoes executadas:
  - `uv run --package account-service python -m compileall src/services/account-service/src/account_service src/infra` -> OK
  - `uv run --package account-service pytest -q` -> falhou (`pytest` nao instalado)
  - `uv run --package account-service uvicorn account_service.main:app ...` -> falhou (`ModuleNotFoundError: account_service`)
  - `PYTHONPATH=src/services/account-service/src:src uv run --package account-service python -c "from account_service.main import app"` -> OK

## Conferencia Da Revisao Anterior (2026-03-24)

1. Critico - Hash de senha com `sha256` sem salt -> **PENDENTE**
2. Alto - `except Exception` generico em rotas -> **PENDENTE**
3. Alto - `str(e)` retornado ao cliente -> **PENDENTE**
4. Alto - Ausencia de testes automatizados -> **PENDENTE**
5. Alto - Build nao deterministico com fallback no Dockerfile -> **PENDENTE**
6. Medio - Defaults de infraestrutura em `settings.py` -> **PENDENTE**
7. Medio - `account-service` sem `env_file`/`environment` dedicado -> **PENDENTE**
8. Medio - PostgreSQL sem volume persistente -> **PENDENTE**
9. Medio - Migrations sem versionamento/rollback -> **PENDENTE**
10. Baixo - Metodo `conect` -> **CONCLUIDO** (`connect` em `src/infra/database/implementations/postgres.py:13`)
11. Baixo - `trace_id` sem uso efetivo em logs -> **PENDENTE**
12. Baixo - README do servico vazio -> **PENDENTE**

## Pendencias Atuais Por Risco (O Que Precisa Ser Feito)

## Critico

- **Seguranca de senha inadequada** (`src/services/account-service/src/account_service/domain/value_objects/user.py:30`):
  - Substituir `sha256` por `argon2id` ou `bcrypt` com salt e fator de custo.
  - Planejar migracao de hashes legados (rehash no login ou job de migracao).

## Alto

- **Contrato de API inconsistente em DELETE/PATCH** (`src/services/account-service/src/account_service/api/routes/user.py:55`, `:69`):
  - Rota define `/{user_id}`, mas handler ignora path param e exige `user_id` no body.
  - Ajustar assinatura para receber `user_id` da URL e remover `user_id` do body.
  - Validar mismatch entre path e body enquanto nao houver breaking change.
- **Tratamento de erro amplo e com vazamento interno** (`src/services/account-service/src/account_service/api/routes/user.py:37-38`, `:52-53`, `:66-67`, `:80-81`):
  - Trocar `except Exception` por mapeamento de erros de dominio/aplicacao.
  - Nao expor `str(e)` ao cliente; retornar mensagem segura e registrar detalhe internamente.
- **Execucao local documentada quebra** (`README.md` x runtime atual):
  - Comando documentado `uv run --package account-service uvicorn account_service.main:app ...` falhou com `ModuleNotFoundError`.
  - Corrigir empacotamento/import path (preferencial) ou ajustar comando/documentacao com `PYTHONPATH`.
- **Cobertura de testes inexistente**:
  - Adicionar `pytest` em dependencias de desenvolvimento e criar suite minima (use cases + rotas principais + repositorio).

## Medio

- **Status HTTP incorretos para operacoes nao-create** (`src/services/account-service/src/account_service/api/routes/user.py:35`, `:64`, `:78`):
  - `GET` e `DELETE/PATCH` retornando `201`; usar `200`/`204` conforme semantica REST.
- **Build de container nao deterministico** (`src/services/account-service/Dockerfile:9`):
  - Remover fallback `|| uv sync ...` em pipeline de CI/producao, mantendo modo fail-fast.
- **Configuracoes sensiveis/defaults hardcoded** (`src/services/account-service/src/account_service/settings.py:17-19`):
  - Reduzir defaults de DSN em codigo e depender de variaveis de ambiente em ambientes reais.
- **Inconsistencia de nome de variavel RabbitMQ** (`REBBITMQ_DSN` em `settings.py:19`):
  - Corrigir para `RABBITMQ_DSN` e alinhar com `.env.example` (`APP_RABBITMQ_DSN`).
- **Compose sem configuracao explicita do account-service** (`docker-compose.yml`):
  - Declarar `env_file` ou `environment` para o servico `account-service`.
- **PostgreSQL sem persistencia** (`docker-compose.yml`):
  - Adicionar volume nomeado para dados do banco.
- **Migrations sem controle de versao** (`src/services/account-service/src/account_service/infra/migration.py`):
  - Adotar ferramenta de migration versionada (ex.: Alembic) com rollback e historico.

## Baixo

- **`trace_id` ainda nao propagado para logs** (`src/services/account-service/src/account_service/api/dependencies.py:10-14`):
  - Enriquecer logs estruturados com `trace_id` por request.
- **README especifico do servico vazio** (`src/services/account-service/README.md`):
  - Documentar setup local, variaveis, endpoints e estrategia de testes.

## Pontos Positivos Confirmados

- Separacao arquitetural em camadas (API, Application, Domain, Infra).
- Queries SQL parametrizadas.
- Lifecycle da app com `startup`/`shutdown`.
- Logging estruturado em JSON inicializado no lifecycle.
- Correcao do metodo `connect` no adapter PostgreSQL.
