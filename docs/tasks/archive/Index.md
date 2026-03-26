# Arquivo De Migracao De Tasks

## Objetivo
Manter historico de tasks antigas que estavam na raiz, mas cujo escopo real pertence ao `account-service`.

## Regra Atual
- `docs/tasks/` (raiz): apenas tarefas de escopo geral do monorepo.
- `src/services/account-service/docs/tasks/`: tarefas especificas do `account-service`.
- As tasks canonicas do servico devem conter `Linha Do Tempo`, `Dependencias`, `Conflitos Mapeados` e `Observacoes`.

## Mapeamento Para Tasks Canonicas Do Servico

- `task-001-password-hashing-migration.md` -> `src/services/account-service/docs/tasks/task-001-password-hashing-migration.md`
- `task-002-generic-exception-routes.md` -> `src/services/account-service/docs/tasks/task-009-error-handling-hardening.md`
- `task-003-error-leakage-to-client.md` -> `src/services/account-service/docs/tasks/task-009-error-handling-hardening.md`
- `task-006-settings-defaults-hardcoded.md` -> `src/services/account-service/docs/tasks/task-011-defaults-de-infra-em-settings.md`
- `task-009-migrations-versioning.md` -> `src/services/account-service/docs/tasks/task-012-versionamento-de-migrations.md`
- `task-010-trace-id-propagation.md` -> `src/services/account-service/docs/tasks/task-013-propagacao-de-trace-id.md`
- `task-011-service-readme-completeness.md` -> `src/services/account-service/docs/tasks/task-010-service-docs-completeness.md`
- `task-012-runtime-import-path.md` -> `src/services/account-service/docs/tasks/task-008-runtime-import-path-reliability.md`
- `task-013-delete-patch-path-contract.md` -> `src/services/account-service/docs/tasks/task-002-api-route-contract-consistency.md`
- `task-014-http-status-codes.md` -> `src/services/account-service/docs/tasks/task-002-api-route-contract-consistency.md`
- `task-015-rabbitmq-setting-name.md` -> `src/services/account-service/docs/tasks/task-014-consistencia-de-nome-de-variavel-rabbitmq.md`
- `task-016-password-length-alignment.md` -> `src/services/account-service/docs/tasks/task-003-password-length-alignment.md`
- `task-017-bcrypt-async-offloading.md` -> `src/services/account-service/docs/tasks/task-004-bcrypt-async-offloading.md`
- `task-018-rounds-validation.md` -> `src/services/account-service/docs/tasks/task-005-rounds-validation.md`
- `task-019-needs-rehash-strategy.md` -> `src/services/account-service/docs/tasks/task-006-rehash-strategy.md`
