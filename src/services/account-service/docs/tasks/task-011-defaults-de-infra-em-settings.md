# Tarefa 011 - Defaults De Infra Em Settings

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
1. [ ] Levantar todos os defaults sensiveis de infraestrutura em `settings.py`.
2. [ ] Remover defaults inseguros e exigir configuracao explicita por ambiente.
3. [ ] Atualizar `.env.example` e documentacao de setup.

## Dependencias
- `src/services/account-service/docs/tasks/task-014-consistencia-de-nome-de-variavel-rabbitmq.md`

## Conflitos Mapeados
- Sobreposicao com task antiga da raiz `docs/tasks/archive/task-006-settings-defaults-hardcoded.md` (canonica agora no servico).

## Contexto
Defaults sensiveis de infraestrutura ainda estao hardcoded em codigo.

## Evidencias
- `src/services/account-service/src/account_service/settings.py`

## Observacoes
- Sem observacoes adicionais.
