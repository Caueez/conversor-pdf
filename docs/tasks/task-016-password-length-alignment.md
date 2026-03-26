# Tarefa 016 - Alinhamento De Tamanho De Senha

## Metadados
- Data de criacao: 2026-03-26
- Data de finalizacao: -
- Commit de implementacao: -
- Branch de implementacao: -
- Risco/Urgencia: Alta / Curto prazo

## Status
Pendente

## Contexto
Dominio e API ainda divergem no limite maximo de senha.

## Evidencias
- API aceita ate `128`: `src/services/account-service/src/account_service/api/schemas.py`
- Dominio valida ate `72`: `src/services/account-service/src/account_service/domain/value_objects/user.py`
