# Tarefa 003 - Alinhamento De Tamanho De Senha

## Metadados
- Data de criacao: 2026-03-26
- Data de finalizacao: -
- Commit de implementacao: fefc694
- Branch de implementacao: feat/account-service-password-hardening
- Risco/Urgencia: Alta / Curto prazo

## Status
Em revisao humana

## Escopo
- Escopo principal: Servico
- Servico alvo: account-service

## Linha Do Tempo
1. [x] Mapear divergencia entre validacao de API e regra de dominio.
2. [x] Aplicar ajuste para `72` em branch dedicada.
3. [ ] Aguardar revisao humana e merge em `develop`.

## Dependencias
- `src/services/account-service/docs/tasks/task-001-password-hashing-migration.md`

## Conflitos Mapeados
- Sobreposicao com task antiga da raiz `docs/tasks/archive/task-016-password-length-alignment.md` (canonica agora no servico).

## Contexto
API e dominio divergiam no limite maximo aceito para senha; ajuste para `72` aplicado em branch e aguardando merge.

## Evidencias
- Estado atual em `develop`: API aceita ate `128` em `src/services/account-service/src/account_service/api/schemas.py`
- Implementacao em revisao: `fefc694` ajusta API para `72` e `dd67e71` aplica limite maximo no dominio (`src/services/account-service/src/account_service/domain/value_objects/user.py`)

## Observacoes
- Sem observacoes adicionais.
