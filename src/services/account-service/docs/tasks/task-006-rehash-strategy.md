# Tarefa 006 - Estrategia De Rehash

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
1. [ ] Definir criterio de `needs_rehash` e ponto de avaliacao no fluxo.
2. [ ] Implementar rehash progressivo sem forcar reset global.
3. [ ] Validar retrocompatibilidade de hashes existentes.

## Dependencias
- `src/services/account-service/docs/tasks/task-001-password-hashing-migration.md`
- `src/services/account-service/docs/tasks/task-005-rounds-validation.md`

## Conflitos Mapeados
- Sobreposicao com task antiga da raiz `docs/tasks/archive/task-019-needs-rehash-strategy.md` (canonica agora no servico).

## Contexto
Fluxo atual nao define estrategia explicita para rehash progressivo.

## Evidencias
- `src/services/account-service/src/account_service/application/interfaces/hasher.py`

## Observacoes
- Sem observacoes adicionais.
