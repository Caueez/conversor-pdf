# Roadmap De Validacao

## Objetivo
Acompanhar o status tecnico do `account-service` e mapear melhorias por tarefa.

## Escopo
Pendencias e entregas relacionadas ao servico de contas/usuarios.

## Estado Atual

- Fluxo principal de usuarios esta implementado.
- Arquitetura por camadas e portas/adaptadores esta ativa.
- Existem pendencias de robustez operacional, testes e endurecimento do fluxo de senha.

## Tarefas

- [Tarefa 001 - Migracao De Hash De Senha](./tasks/task-001-password-hashing-migration.md)
- [Tarefa 002 - Consistencia De Contrato De Rotas](./tasks/task-002-api-route-contract-consistency.md)
- [Tarefa 003 - Alinhamento De Tamanho De Senha](./tasks/task-003-password-length-alignment.md)
- [Tarefa 004 - Offloading Async Do Bcrypt](./tasks/task-004-bcrypt-async-offloading.md)
- [Tarefa 005 - Validacao De Rounds](./tasks/task-005-rounds-validation.md)
- [Tarefa 006 - Estrategia De Rehash](./tasks/task-006-rehash-strategy.md)
- [Tarefa 007 - Cobertura Basica De Testes](./tasks/task-007-test-coverage-baseline.md)
- [Tarefa 008 - Confiabilidade De Import Path Em Runtime](./tasks/task-008-runtime-import-path-reliability.md)
- [Tarefa 009 - Endurecimento De Tratamento De Erros](./tasks/task-009-error-handling-hardening.md)
- [Tarefa 010 - Completude De Documentacao Do Servico](./tasks/task-010-service-docs-completeness.md)

## Referencias

- [Contracts.md](./Contracts.md)
- [BusinessRules.md](./BusinessRules.md)
- [Roadmap da raiz](../../../../docs/ValidationRoadmap.md)
