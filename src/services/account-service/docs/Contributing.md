# Contribuindo

## Objetivo
Padronizar contribuicoes tecnicas para o `account-service`.

## Escopo
Fluxo de branch, commits, revisao e sincronizacao de documentacao.

## Escopo Das Tasks

- Tasks deste servico ficam somente em `src/services/account-service/docs/tasks/`.
- Tasks de escopo geral ficam na raiz em `docs/tasks/`.
- Se esta task depender de outro servico, criar task no servico impactado e registrar a ordem na linha do tempo.

## Fluxo Git Obrigatorio (Fim Da Implementacao)

1. Confirmar que a task pertence ao escopo do `account-service`.
2. Verificar conflitos com tasks existentes de mesmo objetivo.
3. Separar arquivos em grupos de escopo unico.
4. Criar uma branch por grupo, sempre a partir de `develop`.
5. Realizar commits pequenos e focados dentro da branch.
6. Registrar branch, commits, linha do tempo e dependencias nas tasks do servico.
7. Aguardar revisao humana.
8. Com aprovacao humana, seguir com merge em `develop`.

## Regras De Branch

- Branch de trabalho sempre criada a partir de `develop`.
- Branch deve tratar somente um objetivo do servico.

## Regras De Commit

- Commits pequenos com escopo tecnico unico.
- Nao misturar alteracao de contrato com refatoracao ampla no mesmo commit.

## Registro Em Tasks

Para cada task alterada:

- Preencher `Branch de implementacao`.
- Preencher `Commit de implementacao` com hashes da branch.
- Atualizar `Status` e `Data de finalizacao` quando aplicavel.
- Atualizar `Linha Do Tempo` com a ordem de implementacao e dependencias.
- Atualizar `Conflitos Mapeados` quando houver sobreposicao com outra task.

## Script De Tarefas

- Para criar tarefas do servico:
  - `scripts/docs/new_task.sh --scope service --service account-service --titulo "Titulo da tarefa"`

## Regras De Entrega

- Atualizar `Contracts.md` quando houver mudanca de API.
- Atualizar `BusinessRules.md` quando regra funcional mudar.
- Atualizar `ValidationRoadmap.md` e `tasks/` com status real do trabalho.
- Registrar riscos tecnicos relevantes no arquivo da task correspondente.
- Se houver impacto em outro servico, abrir task no servico impactado e registrar o encadeamento no timeline da task principal.

## Referencias

- [Agent.md](./Agent.md)
- [Contracts.md](./Contracts.md)
- [ValidationRoadmap.md](./ValidationRoadmap.md)
- [Contributing da raiz](../../../../docs/Contributing.md)
