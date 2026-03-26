# Tarefa 017 - Offloading Async Do Bcrypt

## Metadados
- Data de criacao: 2026-03-26
- Data de finalizacao: -
- Commit de implementacao: -
- Branch de implementacao: -
- Risco/Urgencia: Alta / Curto prazo

## Status
Pendente

## Contexto
Hash/check de senha com bcrypt e CPU-bound e pode bloquear event loop.

## Evidencias
- `src/services/account-service/src/account_service/application/use_cases/users.py`
- `src/infra/security/password_hashers/bcrypt.py`
