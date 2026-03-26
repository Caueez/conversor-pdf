# Tarefa 005 - Validacao De Rounds

## Metadados
- Data de criacao: 2026-03-26
- Data de finalizacao: -
- Commit de implementacao: -
- Branch de implementacao: -
- Risco/Urgencia: Media / Medio prazo

## Status
Pendente

## Escopo
- Escopo principal: Servico
- Servico alvo: account-service

## Linha Do Tempo
1. [ ] Definir faixa aceita de rounds por ambiente.
2. [ ] Implementar validacao em settings com falha explicita para valores invalidos.
3. [ ] Documentar valor recomendado e impacto de custo.

## Dependencias
- `src/services/account-service/docs/tasks/task-001-password-hashing-migration.md`

## Conflitos Mapeados
- Sobreposicao com task antiga da raiz `docs/tasks/archive/task-018-rounds-validation.md` (canonica agora no servico).

## Contexto
Configuracao de custo do bcrypt ainda sem validacao de faixa.

## Evidencias
- `src/services/account-service/src/account_service/settings.py`

## Observacoes
- Sem observacoes adicionais.
