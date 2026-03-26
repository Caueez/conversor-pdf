# Tarefa 003 - Alinhamento De Tamanho De Senha

## Metadados
- Data de criacao: 2026-03-26
- Data de finalizacao: -
- Commit de implementacao: fefc694
- Branch de implementacao: feat/account-service-password-hardening
- Risco/Urgencia: Alta / Curto prazo

## Status
Em revisao humana

## Contexto
API e dominio divergiam no limite maximo aceito para senha; ajuste para `72` aplicado em branch e aguardando merge.

## Evidencias
- API: `src/services/account-service/src/account_service/api/schemas.py`
- Dominio: `src/services/account-service/src/account_service/domain/value_objects/user.py`
