# Arquitetura

## Objetivo
Documentar a arquitetura do sistema como um todo no monorepo.

## Escopo
Diretrizes de alto nivel, estrutura global e fronteiras entre dominios tecnicos.

## Visao Geral Do Monorepo

- `backend/services/`: servicos de negocio independentes.
- `backend/infra/`: componentes tecnicos compartilhados entre servicos.
- `docs/`: documentacao estavel de arquitetura, contratos, regras e setup.
- `development/`: diretrizes operacionais e roadmap de evolucao tecnica.

## Principios Arquiteturais

- Servicos devem ser fracamente acoplados e evoluir de forma independente.
- Dominio de negocio deve ficar isolado de detalhes de infraestrutura.
- Contratos externos devem ser documentados por servico.
- Componentes tecnicos compartilhados devem ficar em `backend/infra/`.
- Dependencias entre servicos devem ser explicitas e minimizadas.

## Fronteiras De Responsabilidade

- Cada servico define sua arquitetura interna em `backend/services/<servico>/docs/Architecture.md`.
- O modulo compartilhado define sua arquitetura interna em `backend/infra/docs/Architecture.md`.
- Este documento nao descreve implementacao interna de um servico especifico.

## Referencias

- [Contracts.md](./Contracts.md)
- [BusinessRules.md](./BusinessRules.md)
- [Setup.md](./Setup.md)
- [Desenvolvimento](../development/Index.md)
