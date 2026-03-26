# Tarefa 016 - Alinhamento De Tamanho De Senha

## Metadados
- Data de criacao: 2026-03-26
- Data de finalizacao: -
- Commit de implementacao: fefc694
- Branch de implementacao: feat/account-service-password-hardening
- Risco/Urgencia: Alta / Curto prazo

## Status
Em revisao humana

## Contexto
Dominio e API divergiam no limite maximo de senha; o ajuste para `72` foi aplicado na branch e aguarda merge.

## Evidencias
- API aceita ate `128`: `src/services/account-service/src/account_service/api/schemas.py`
- Dominio valida ate `72`: `src/services/account-service/src/account_service/domain/value_objects/user.py`
