# Arquitetura

## Objetivo
Documentar os principios arquiteturais estaveis do monorepo.

## Escopo
Diretrizes de alto nivel e fronteiras tecnicas entre componentes.

## Principios

- Arquitetura em camadas com portas e adaptadores.
- Regras de negocio centralizadas no `domain` e orquestracao no `application`.
- Infraestrutura implementa portas definidas pela aplicacao.
- API atua como camada de transporte e adaptacao de contrato externo.

## Regras De Dependencia

- `domain` nao depende de framework ou infraestrutura.
- `application` depende de abstracoes (ports), nao de implementacoes concretas.
- `infra` depende de `application`/`domain` para implementar portas.
- `api` depende de `application` para executar casos de uso.

## Referencias Por Servico

- `account-service`: [Architecture.md](../src/services/account-service/docs/Architecture.md)

## Referencias

- [Contracts.md](./Contracts.md)
- [BusinessRules.md](./BusinessRules.md)
- [ValidationRoadmap.md](./ValidationRoadmap.md)
