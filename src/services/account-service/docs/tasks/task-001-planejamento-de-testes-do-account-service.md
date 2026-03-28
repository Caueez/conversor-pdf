# Tarefa 001 - Planejamento de testes do account-service

## Metadados
- Data de criacao: 2026-03-28 01:56:31 -0300
- Ultima atualizacao: 2026-03-28 15:12:26 -0300
- Data de finalizacao: -
- Status: Em versionamento
- Escopo principal: Servico
- Servico alvo: account-service
- Risco/Urgencia: Media / Medio prazo
- Branch de implementacao: feat/account-service-test-suite
- Commit de implementacao: -

## Solicitacoes Versionadas (Chat)

### Versao 1 - 2026-03-28 01:57:03 -0300
- Iniciar planejamento para implementacao de testes no servico `account-service`.
- Planejar testes de:
  - Unitarios
  - Integracao
  - E2E

### Versao 2 - 2026-03-28 02:19:55 -0300
- Atualizar a task para cobertura funcional completa do `account-service`:
  - cenarios
  - regras de negocio
  - classes e entidades
  - APIs e contratos
- Definir baseline de integracao/E2E com infra real via `docker compose`, usando Postgres de teste dedicado.
- Definir politica fixa: qualquer bug encontrado durante criacao de testes deve abrir task separada, sem correcao nesta task.

### Versao 3 - 2026-03-28 02:25:10 -0300
- Inserir ganhos adicionais na task:
  - matriz de rastreabilidade entre `BusinessRules.md`/`Contracts.md` e casos de teste;
  - gates de qualidade em CI por tipo de suite;
  - cobertura minima para unitarios e cobertura por cenario para integracao/E2E;
  - estrategia anti-flake (seed fixa, UTC controlado e isolamento de dados);
  - protecao de contrato contra drift de status/payload;
  - factories/builders de dados para reduzir duplicacao;
  - suite smoke rapida para feedback local e pre-PR.

### Versao 4 - 2026-03-28 02:58:36 -0300
- Autorizacao explicita recebida para executar a Etapa 4.
- Executar implementacao da suite de testes (unitario, integracao, E2E, contrato e smoke), com gates e rastreabilidade.

### Versao 5 - 2026-03-28 14:49:26 -0300
- Docker/Postgres local ativo para validar novamente as suites dependentes de infra real.
- Reexecutar `integration`, `e2e/contract`, `smoke` e full suite para encerrar a Etapa 4 sem `skip`.

### Versao 6 - 2026-03-28 14:58:04 -0300
- Corrigir import de `account_service` nos testes sem depender de `PYTHONPATH` manual.
- Transformar o projeto em pacote uv com `tool.uv.package = true`.
- Configurar empacotamento do modulo `account_service` no build backend.

### Versao 7 - 2026-03-28 15:12:26 -0300
- Validacao final da entrega concluida (`pytest` e `pyright` OK).
- Autorizacao explicita recebida para executar a Etapa 5 de versionamento Git.
- Branch de trabalho criada para entrega da task.

## Analise Consolidada Da Task
- Objetivo consolidado:
  - Definir um plano de testes decision complete para cobertura funcional completa do `account-service`, incluindo unitarios, integracao, E2E e validacao de contrato HTTP.
- Estado atual consolidado:
  - O servico possui camadas `api`, `application`, `domain` e `infra`, com endpoints de usuarios (`GET /`, `POST /`, `PATCH /{user_id}`, `DELETE /{user_id}`).
  - Estrutura de testes implementada em `src/services/account-service/tests/` com suites unitaria, integracao, E2E, contrato e smoke.
  - Dependencias e configuracao de testes adicionadas em `src/services/account-service/pyproject.toml`.
  - `account_service` agora e importavel diretamente via `uv run --package account-service ...`.
  - Gates de CI configurados em `.github/workflows/account-service-tests.yml`.
  - Matriz de rastreabilidade criada em `src/services/account-service/tests/TRACEABILITY.md`.
  - Bug funcional detectado em update de email foi isolado na `task-002-correcao-de-update-de-email-no-user-use-case`.
  - O plano aprovado fixa que integracao e E2E devem usar infra real, sem substituir por mock os adapters externos.
- Consistencia entre solicitacoes:
  - As versoes 1, 2, 3, 4, 5, 6 e 7 sao complementares e sem conflito.
- Controle de duplicidade e divergencia:
  - Nao ha task ativa no servico com o mesmo objetivo (`src/services/account-service/docs/tasks/` estava vazio antes desta task).
  - Escopo permanece exclusivo do `account-service`, sem dependencia de outro servico.
- Pontos de atencao atuais:
  - Restam 2 cenarios `xfail` esperados, vinculados a `task-002-correcao-de-update-de-email-no-user-use-case`.
  - Esta task permanece sem correcao de bug de produto; bugs detectados seguem para tasks separadas.

## APIs/Interfaces Publicas
- Nenhuma mudanca de API publica e planejada nesta task.
- Contratos HTTP existentes serao validados por testes; qualquer divergencia funcional deve gerar task separada de correcao/ajuste contratual.

## Escopos Alterados E Mudancas Planejadas
- Escopo: planejamento de qualidade do servico `account-service`
  - Mudanca planejada: formalizar cobertura funcional completa por tipo de teste.
- Escopo: padronizacao de infraestrutura de testes do servico
  - Mudanca planejada: adotar `docker compose` como baseline para testes de integracao e E2E com infra real.
- Escopo: governanca de bugs durante criacao de testes
  - Mudanca planejada: registrar politica de abrir task separada para qualquer bug identificado.
- Escopo: confiabilidade e operacao da suite
  - Mudanca planejada: adicionar rastreabilidade de regras/contratos, protecao anti-flake e gates por etapa em CI.

## Arquivos Previstos Para Alteracao (Quando Houver Liberacao)
- `src/services/account-service/pyproject.toml`
  - Configuracao de stack e comandos de execucao da suite.
- `src/services/account-service/tests/`
  - Implementacao da estrutura de testes unitarios, de integracao e E2E.
- `src/services/account-service/docs/BusinessRules.md`
  - Fonte para rastreabilidade de regras de negocio cobertas por teste.
- `src/services/account-service/docs/Contracts.md`
  - Fonte para rastreabilidade de contratos HTTP cobertos por teste.
- `.github/workflows/` (ou equivalente de pipeline no repositorio)
  - Gates de CI para `smoke`, `unit`, `integration`, `e2e` e full suite.
- `src/services/account-service/docs/tasks/task-001-planejamento-de-testes-do-account-service.md`
  - Registro da analise consolidada, matriz obrigatoria, criterios e evolucao da task.

## Matriz Obrigatoria De Testes
| Tipo | Alvo | Cenarios obrigatorios |
|---|---|---|
| Unitario | `domain.value_objects.user` | Email valido/invalido; senha `<8`, `8`, `72`, `>72`; mensagens de erro corretas. |
| Unitario | `domain.entities.user` | `to_dict` sem `password_hash`; serializacao de datas; defaults de `id`, `is_active`, `created_at`, `updated_at`. |
| Unitario | `application.use_cases.users` | `create`, `list`, `delete`, `update` em todos os ramos: sucesso, conflito, inexistente, validacao, hash aplicado e update parcial por campo. |
| Unitario | `api.schemas`, `api.presenters`, `api.dependencies`, `api.exception_handlers` | Limites e validacoes de payload; regra de PATCH com pelo menos um campo; mapeamentos request/DTO/response; mapeamento HTTP 422/409/400/500; comportamento de `trace_id`. |
| Unitario | `infra.container`, `infra.migration`, `settings`, `shared.typed` | Build/startup/shutdown; backend valido/invalido; idempotencia de migracao; UUID/tempo e carregamento de settings. |
| Integracao | `infra.repositories.user` + Postgres real | CRUD completo, busca por email, lista, unicidade de email e persistencia real de UUID/timestamps. |
| Integracao | Componentes usados de `src/infra` | `Query.create` valido/invalido, execucao real no Postgres, hash/check com bcrypt adapter. |
| E2E | API FastAPI + Postgres real | Fluxo completo criar/listar/atualizar/remover; status codes e payloads do contrato; erros de validacao, conflito e not found. |
| Contrato | Documentacao x comportamento HTTP | Verificar shape e status de todos os endpoints documentados; divergencia abre task separada. |
| Governanca | Rastreabilidade regra/contrato -> teste | Cada regra de `BusinessRules.md` e contrato de `Contracts.md` deve mapear para caso(s) de teste identificado(s). |
| Operacional | Smoke suite | Rodar subconjunto rapido de cenarios criticos para feedback local e pre-PR. |

## Ganhos De Qualidade Inseridos Nesta Iteracao
1. Matriz de rastreabilidade entre documentacao funcional e suite.
2. Gates de qualidade por etapa em CI (smoke, unit, integration/e2e, full suite).
3. Cobertura minima de unitarios com threshold explicito.
4. Estrategia anti-flake para estabilidade de execucao.
5. Protecao de contrato para evitar drift silencioso de API.
6. Builders/factories de dados de teste reutilizaveis.
7. Smoke suite para reduzir tempo de feedback no ciclo local.

## Mudancas Previstas Por Camada (Rascunho)
1. Stack de testes
   - Configurar framework e comandos para rodar unitarios, integracao, E2E e suite completa.
2. Dominio e aplicacao
   - Criar cobertura total das regras e dos ramos de decisao dos casos de uso.
3. API e contratos
   - Validar schemas, handlers, rotas e conformidade do contrato HTTP documentado.
4. Infra e persistencia
   - Validar adapters com Postgres real em ambiente de teste dedicado.
5. Governanca de bugs
   - Abrir task separada para cada divergencia encontrada durante implementacao dos testes.
6. Qualidade operacional da suite
   - Implementar rastreabilidade, gates de CI, anti-flake e smoke suite.

## Criterios De Aceite
1. Nenhum modulo funcional do `account_service` fica sem cenario positivo e negativo.
2. Todos os endpoints documentados possuem testes de contrato e E2E de sucesso.
3. Integracao e E2E executam com Postgres real isolado por suite (reset de dados entre testes).
4. A suite deve permitir execucao separada de unitario, integracao, E2E e full suite.
5. Todo bug encontrado durante criacao dos testes deve gerar task vinculada imediatamente, sem correcao nesta task.
6. Toda regra de `BusinessRules.md` e todo endpoint de `Contracts.md` deve estar mapeado para caso(s) de teste.
7. Gate `unit` deve ser obrigatorio em PR; `integration` e `e2e` obrigatorios antes de merge em `develop`.
8. Cobertura minima de testes unitarios deve ser >= 90%.
9. Suite deve incluir controle anti-flake (dados deterministas, tempo UTC controlado e isolamento forte).
10. Smoke suite deve executar em tempo reduzido e cobrir os fluxos HTTP criticos.

## Assuncoes E Defaults
- "Cobertura total" nesta task e funcional/comportamental, nao meta fixa de percentual de linha.
- Para futuras infras externas, manter padrao:
  - unitario com mock/fake de portas;
  - integracao com adapter + infra real containerizada;
  - E2E dos fluxos criticos.
- Threshold padrao de cobertura minima para unitarios definido em 90%.
- Protecao de contrato deve validar, no minimo, status code e chaves obrigatorias de payload por endpoint.
- A implementacao desta task pode depender de novas tasks de correcao identificadas durante os testes.

## Evidencias Da Iteracao
- Testes implementados:
  - `src/services/account-service/tests/unit/...`
  - `src/services/account-service/tests/integration/...`
  - `src/services/account-service/tests/e2e/...`
  - `src/services/account-service/tests/TRACEABILITY.md`
- Pipeline de gates implementado:
  - `.github/workflows/account-service-tests.yml`
- Roadmap do servico sincronizado:
  - `src/services/account-service/docs/ValidationRoadmap.md`
- Execucoes realizadas:
  - `PYTHONPATH=src/services/account-service/src:src uv run --package account-service pytest src/services/account-service/tests -m unit --cov=account_service --cov=infra --cov-branch --cov-report=term-missing --cov-fail-under=90`
    - Resultado: `75 passed, 15 deselected, 1 xfailed`; cobertura total `92.54%`.
  - `docker compose up -d postgres`
    - Resultado: Postgres local iniciado e saudavel.
  - `PYTHONPATH=src/services/account-service/src:src APP_TEST_POSTGRES_DSN=postgresql://postgres:postgres@127.0.0.1:5432/user_service uv run --package account-service pytest src/services/account-service/tests -m integration`
    - Resultado: `5 passed`.
  - `PYTHONPATH=src/services/account-service/src:src APP_TEST_POSTGRES_DSN=postgresql://postgres:postgres@127.0.0.1:5432/user_service uv run --package account-service pytest src/services/account-service/tests -m "e2e or contract"`
    - Resultado: `9 passed, 1 xfailed`.
  - `PYTHONPATH=src/services/account-service/src:src APP_TEST_POSTGRES_DSN=postgresql://postgres:postgres@127.0.0.1:5432/user_service uv run --package account-service pytest src/services/account-service/tests -m smoke -q`
    - Resultado: `3 passed`.
  - `PYTHONPATH=src/services/account-service/src:src APP_TEST_POSTGRES_DSN=postgresql://postgres:postgres@127.0.0.1:5432/user_service uv run --package account-service pytest src/services/account-service/tests -q`
    - Resultado: `89 passed, 2 xfailed`.
  - `uv run --package account-service python -c "import account_service; print(account_service.__file__)"`
    - Resultado: import de `account_service` resolvido sem `PYTHONPATH` manual.
  - `uv run --package account-service pytest src/services/account-service/tests -q`
    - Resultado: `89 passed, 2 xfailed` sem `PYTHONPATH` manual.

## Plano Evolutivo Da Task (Por Etapas)

### Etapa 1 - Estruturacao Inicial (Concluida)
1. [x] Registrar solicitacao inicial da task.
2. [x] Consolidar analise inicial.
3. [x] Mapear escopos e arquivos previstos sem implementar.

### Etapa 2 - Refinamento (Concluida)
1. [x] Detalhar matriz obrigatoria por tipo de teste e alvo de cobertura.
2. [x] Priorizar ordem de implementacao: unitario -> integracao -> E2E -> contrato.
3. [x] Definir estrategia de ambiente para integracao/E2E com `docker compose` e Postgres dedicado.
4. [x] Inserir ganhos de rastreabilidade, gates de CI, anti-flake e smoke suite.

### Etapa 3 - Liberacao
1. [x] Validar planejamento com o programador.
2. [x] Ajustar pendencias finais do plano.
3. [x] Aguardar autorizacao explicita para iniciar implementacao.

### Etapa 4 - Implementacao
1. [x] Implementar testes unitarios de dominio, aplicacao, API e componentes internos.
2. [x] Implementar testes de integracao com adapters e componentes de infra usando Postgres real.
3. [x] Implementar testes E2E dos endpoints e validacao de contrato HTTP documentado.
4. [x] Implementar matriz de rastreabilidade regra/contrato -> casos de teste.
5. [x] Configurar gates de CI por tipo de suite (`smoke`, `unit`, `integration`, `e2e`, full suite).
6. [x] Implementar estrategia anti-flake e builders/factories de teste.
7. [x] Registrar bug encontrado em task separada e manter esta task focada na suite de testes.
8. [x] Executar validacao final da suite (smoke, unitario, integracao, E2E e full suite) com Postgres real ativo.
9. [x] Registrar resultado da validacao para revisao do programador.

### Etapa 5 - Versionamento Git
1. [x] Solicitar autorizacao explicita do programador para iniciar versionamento Git apos validacao da implementacao.
2. [x] Classificar arquivos alterados e revisar diff final.
3. [ ] Executar versionamento Git autorizado (branch, commit, push e merge conforme instrucao do programador).
