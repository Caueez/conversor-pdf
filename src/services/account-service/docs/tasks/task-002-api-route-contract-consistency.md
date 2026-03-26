# Tarefa 002 - Consistencia De Contrato De Rotas

## Metadados
- Data de criacao: 2026-03-26
- Data de finalizacao: 2026-03-26
- Commit de implementacao: fefc694
- Branch de implementacao: feat/account-service-password-hardening
- Risco/Urgencia: Media / Medio prazo

## Status
Concluida

## Escopo
- Escopo principal: Servico
- Servico alvo: account-service

## Linha Do Tempo
1. [x] Ajustar construcao de DTOs de rota com tipagem consistente.
2. [x] Garantir contrato por path em `DELETE/PATCH` e respostas coerentes.
3. [x] Alinhar response model para presenter da API.

## Dependencias
- Nenhuma dependencia registrada.

## Conflitos Mapeados
- Sobreposicao com tasks antigas da raiz `task-013-delete-patch-path-contract.md` e `task-014-http-status-codes.md` (canonica agora no servico).

## Contexto
Garantir uso de `user_id` por path e status HTTP corretos nas rotas principais.

## Evidencias
- `src/services/account-service/src/account_service/api/routes/user.py`

## Observacoes
- Sem observacoes adicionais.
