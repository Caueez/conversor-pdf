# Arquitetura

## Objetivo
Documentar os principios arquiteturais estaveis do `account-service`.

## Escopo
Camadas, dependencias e responsabilidades tecnicas do servico.

## Camadas

- `api`: rotas, schemas HTTP, dependencies de autenticacao e apresentacao de resposta.
- `application`: casos de uso, DTOs e portas.
- `domain`: entidades, value objects e regras de negocio.
- `infra`: adaptadores de repositorio, seguranca, container e migracao.

## Regras De Dependencia

- `api` depende de `application`.
- `application` depende de contratos/ports e `domain`.
- `domain` nao depende de infraestrutura.
- `infra` implementa portas da aplicacao.

## Componentes De Sessao

- `SessionUseCase` concentra login, refresh, logout, `me` e validacao de access token.
- Persistencia de sessao fica em `sessions` no Postgres para suportar revogacao imediata.
- Tokens JWT (`HS256`) sao emitidos/validados por adapter de token na camada `infra`.
- Rotas de usuario sao protegidas por dependency de autenticacao na camada `api`.

## Compartilhamento Com Infra

- Integracoes compartilhadas devem usar componentes em `backend/infra` quando aplicavel.

## Referencias

- [Contracts.md](./Contracts.md)
- [BusinessRules.md](./BusinessRules.md)
