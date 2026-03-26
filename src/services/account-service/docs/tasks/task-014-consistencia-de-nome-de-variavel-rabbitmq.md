# Tarefa 014 - Consistencia De Nome De Variavel RabbitMQ

## Metadados
- Data de criacao: 2026-03-26
- Data de finalizacao: 2026-03-26
- Commit de implementacao: nao informado (registrar hash apos commit)
- Branch de implementacao: nao informada (registrar nome apos commit)
- Risco/Urgencia: Baixa / Planejado

## Status
Concluida

## Escopo
- Escopo principal: Servico
- Servico alvo: account-service

## Linha Do Tempo
1. [x] Padronizar nome da variavel de configuracao de DSN do RabbitMQ.
2. [x] Garantir consistencia de nomenclatura entre settings e uso no servico.
3. [ ] Backfill dos metadados de branch/commit quando o historico for confirmado.

## Dependencias
- Nenhuma dependencia registrada.

## Conflitos Mapeados
- Sobreposicao com task antiga da raiz `docs/tasks/archive/task-015-rabbitmq-setting-name.md` (canonica agora no servico).

## Contexto
Padronizacao do nome da configuracao de DSN do RabbitMQ.

## Evidencias
- `src/services/account-service/src/account_service/settings.py` (`RABBITMQ_DSN`).

## Observacoes
- Sem observacoes adicionais.
