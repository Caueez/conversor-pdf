# Arquitetura

## Objetivo
Documentar a arquitetura interna do modulo `infra`.

## Escopo
Componentes compartilhados reutilizaveis entre servicos do monorepo.

## Estrutura Atual

- `infra.database.shared`
  - `Statement`, `Query`, `DatabaseRow`
- `infra.database.implementations.postgres`
  - cliente `Postgres` para `connect`, `fetch_one`, `fetch_all`, `execute`
- `infra.security.password_hashers.bcrypt`
  - `BcryptHasher` para `hash` e `check`

## Regras De Uso

- `infra` nao deve conter regra de negocio de servico.
- `infra` deve expor apenas blocos tecnicos compartilhados.
- Mudancas de comportamento compartilhado exigem revisao de impacto nos servicos consumidores.
