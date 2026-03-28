# Tarefa 002 - Correcao de update de email no user use-case

## Metadados
- Data de criacao: 2026-03-28 02:38:27 -0300
- Ultima atualizacao: 2026-03-28 02:59:43 -0300
- Data de finalizacao: -
- Status: Em planejamento
- Escopo principal: Servico
- Servico alvo: account-service
- Risco/Urgencia: Media / Medio prazo
- Branch de implementacao: -
- Commit de implementacao: -

## Solicitacoes Versionadas (Chat)

### Versao 1 - 2026-03-28 02:38:27 -0300
- Bug identificado durante a implementacao da suite de testes da `task-001-planejamento-de-testes-do-account-service`.
- Cenário: `PATCH /{user_id}` com campo `email` diferente retorna `200`, mas mantem email antigo.
- Necessidade: corrigir o caso de uso `UserUseCase.update` para aplicar o novo email apos validacao e verificacao de unicidade.

## Analise Consolidada Da Task
- Objetivo consolidado:
  - Corrigir comportamento de update de email em `account_service.application.use_cases.users.UserUseCase.update`.
- Estado atual consolidado:
  - O fluxo de update valida email e consulta unicidade, mas nao aplica `dto.email` na entidade final persistida.
  - O bug esta coberto como `xfail` em:
    - `tests/unit/application/test_user_use_case.py::test_update_email_should_change_email_value`
    - `tests/e2e/api/test_user_routes.py::test_patch_email_should_update_email_field`
- Consistencia entre solicitacoes:
  - Sem conflito; task aberta especificamente para bug de produto.
- Controle de duplicidade e divergencia:
  - Bug isolado desta task para manter `task-001` focada em testes, conforme politica aprovada.
- Pontos de atencao atuais:
  - Atualizar testes `xfail` para testes normais apos correcao validada.
  - Revisar impacto de contrato e regras de negocio documentadas.

## Escopos Alterados E Mudancas Planejadas
- Escopo: camada de aplicacao (`use_cases`)
  - Mudanca planejada: aplicar novo email quando `dto.email` for fornecido e aprovado.
- Escopo: testes afetados
  - Mudanca planejada: remover `xfail` e manter cobertura de regressao.

## Arquivos Previstos Para Alteracao (Quando Houver Liberacao)
- `src/services/account-service/src/account_service/application/use_cases/users.py`
  - Corrigir atribuicao do email no fluxo de update.
- `src/services/account-service/tests/unit/application/test_user_use_case.py`
  - Remover `xfail` apos correcao.
- `src/services/account-service/tests/e2e/api/test_user_routes.py`
  - Remover `xfail` apos correcao.

## Mudancas Previstas Por Arquivo (Rascunho)
1. `src/services/account-service/src/account_service/application/use_cases/users.py`
   - Aplicar `email = dto.email` quando presente e valido.
2. `src/services/account-service/tests/unit/application/test_user_use_case.py`
   - Converter teste de regressao de `xfail` para `pass`.
3. `src/services/account-service/tests/e2e/api/test_user_routes.py`
   - Converter teste de regressao de `xfail` para `pass`.

## Plano Evolutivo Da Task (Por Etapas)

### Etapa 1 - Estruturacao Inicial (Concluida)
1. [x] Registrar solicitacao inicial da task.
2. [x] Consolidar analise inicial.
3. [x] Mapear escopos e arquivos previstos sem implementar.

### Etapa 2 - Refinamento
1. [ ] Incorporar novas versoes de solicitacao com marcacao temporal.
2. [ ] Revalidar consistencia do plano.
3. [ ] Refinar mudancas previstas por arquivo.

### Etapa 3 - Liberacao
1. [ ] Validar planejamento com o programador.
2. [ ] Ajustar pendencias finais do plano.
3. [ ] Aguardar autorizacao explicita para iniciar implementacao.

### Etapa 4 - Implementacao
1. [ ] Executar implementacao autorizada.
2. [ ] Validar implementacao do agente (escopo, requisitos e testes).
3. [ ] Registrar resultado da validacao para revisao do programador.

### Etapa 5 - Versionamento Git
1. [ ] Solicitar autorizacao explicita do programador para iniciar versionamento Git apos validacao da implementacao.
2. [ ] Classificar arquivos alterados e revisar diff final.
3. [ ] Executar versionamento Git autorizado (branch, commit, push e merge conforme instrucao do programador).
