# Tarefa 008 - Confiabilidade De Import Path Em Runtime

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
1. [ ] Identificar cenarios onde `PYTHONPATH` manual ainda e necessario.
2. [ ] Ajustar bootstrap/runtime para import estavel sem override manual.
3. [ ] Validar execucao local e em container.

## Dependencias
- Nenhuma dependencia registrada.

## Conflitos Mapeados
- Sobreposicao com task antiga da raiz `docs/tasks/archive/task-012-runtime-import-path.md` (canonica agora no servico).

## Contexto
Execucao local ainda pode depender de `PYTHONPATH` manual.

## Evidencias
- Import de `account_service` falha em alguns cenarios sem override de ambiente.

## Observacoes
- Sem observacoes adicionais.
