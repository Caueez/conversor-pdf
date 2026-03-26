# Arquitetura

## Objetivo
Documentar os principios arquiteturais estaveis do `account-service`.

## Escopo
Camadas, dependencias e responsabilidades tecnicas do servico.

## Camadas

- `api`: rotas, schemas HTTP e apresentacao de resposta
- `application`: casos de uso, DTOs e portas
- `domain`: entidades, value objects e regras de negocio
- `infra`: adaptadores de repositorio, seguranca, container e migracao

## Regras De Dependencia

- `api` depende de `application`.
- `application` depende de contratos/ports e `domain`.
- `domain` nao depende de infraestrutura.
- `infra` implementa portas da aplicacao.

## Componentes Tecnicos Atuais

- API HTTP com FastAPI.
- Persistencia em PostgreSQL.
- Hash de senha com bcrypt via adapter.

## Referencias

- [Contracts.md](./Contracts.md)
- [BusinessRules.md](./BusinessRules.md)
- [ValidationRoadmap.md](./ValidationRoadmap.md)
- [Arquitetura da raiz](../../../../docs/Architecture.md)
