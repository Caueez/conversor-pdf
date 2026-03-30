# Roadmap De Validacao

## Objetivo
Consolidar o foco atual de validacao tecnica do monorepo.

## Escopo
Riscos, lacunas de qualidade e proximas melhorias por area.

## Estado Atual

- Arquitetura de servicos por camadas ativa.
- Servico `account-service` com suites `unit`, `integration`, `e2e`, `contract` e `smoke`.
- Componentes compartilhados centralizados em `backend/infra`.

## Prioridades Atuais

- Adocao consistente de TDD (`Red -> Green -> Refactor`) em novas mudancas.
- Estabilidade de testes de integracao e e2e.
- Consistencia de contratos HTTP e regras de negocio.
- Evolucao de observabilidade e padronizacao operacional.

## Referencias

- [Index.md](./Index.md)
- [Contributing.md](./Contributing.md)
- [Arquitetura do sistema](../docs/Architecture.md)
