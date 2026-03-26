# Tarefa 012 - Confiabilidade De Import Path Em Runtime

## Metadados
- Data de criacao: 2026-03-26
- Data de finalizacao: -
- Commit de implementacao: -
- Branch de implementacao: -
- Risco/Urgencia: Alta / Curto prazo

## Status
Pendente

## Contexto
Execucao via workspace ainda depende de ajuste manual de `PYTHONPATH` em alguns cenarios.

## Evidencias
- `uv run --package account-service python -c "import account_service"` pode falhar sem override.
