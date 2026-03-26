# Tarefa 004 - Offloading Async Do Bcrypt

## Metadados
- Data de criacao: 2026-03-26
- Data de finalizacao: -
- Commit de implementacao: -
- Branch de implementacao: -
- Risco/Urgencia: Alta / Curto prazo

## Status
Pendente

## Escopo
- Escopo principal: Servico
- Servico alvo: account-service

## Linha Do Tempo
1. [ ] Definir estrategia de offloading de bcrypt para nao bloquear event loop.
2. [ ] Implementar execucao em thread pool/process pool onde aplicavel.
3. [ ] Validar latencia sob carga e registrar resultado.

## Dependencias
- `src/services/account-service/docs/tasks/task-001-password-hashing-migration.md`

## Conflitos Mapeados
- Sobreposicao com task antiga da raiz `docs/tasks/archive/task-017-bcrypt-async-offloading.md` (canonica agora no servico).

## Contexto
Operacoes de bcrypt sao CPU-bound e podem impactar latencia em fluxo async.

## Evidencias
- `src/services/account-service/src/account_service/application/use_cases/users.py`
- `src/infra/security/password_hashers/bcrypt.py`

## Observacoes
- Sem observacoes adicionais.
