# Tarefa 001 - Migracao De Hash De Senha

## Metadados
- Data de criacao: 2026-03-26
- Data de finalizacao: 2026-03-26
- Commit de implementacao: dd67e71, fefc694
- Branch de implementacao: feat/account-service-password-hardening
- Risco/Urgencia: Alta / Curto prazo

## Status
Concluida com observacoes

## Contexto
Migrar hashing de senha para bcrypt via portas/adaptadores.

## Evidencias
- `src/services/account-service/src/account_service/application/use_cases/users.py`
- `src/services/account-service/src/account_service/application/interfaces/hasher.py`
- `src/services/account-service/src/account_service/infra/security/bcrypt_hasher_adapter.py`
- `src/infra/security/password_hashers/bcrypt.py`
