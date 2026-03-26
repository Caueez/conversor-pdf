# Contribuindo

## Objetivo
Padronizar contribuicoes tecnicas para o `account-service`.

## Escopo
Fluxo de branch, commits, revisao e sincronizacao de documentacao.

## Fluxo Git Obrigatorio (Fim Da Implementacao)

1. Separar arquivos em grupos de escopo unico.
2. Criar uma branch por grupo, sempre a partir de `develop`.
3. Realizar commits pequenos e focados dentro da branch.
4. Registrar branch e commits nas tasks do servico.
5. Aguardar revisao humana.
6. Com aprovacao humana, seguir com merge em `develop`.

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

## Script De Tarefas

- Para criar tarefas do servico:
  - `scripts/docs/new_task.sh --scope service --service account-service --titulo "Titulo da tarefa"`

## Regras De Entrega

- Atualizar `Contracts.md` quando houver mudanca de API.
- Atualizar `BusinessRules.md` quando regra funcional mudar.
- Atualizar `ValidationRoadmap.md` e `tasks/` com status real do trabalho.
- Registrar riscos tecnicos relevantes no arquivo da task correspondente.

## Referencias

- [Agent.md](./Agent.md)
- [Contracts.md](./Contracts.md)
- [ValidationRoadmap.md](./ValidationRoadmap.md)
- [Contributing da raiz](../../../../docs/Contributing.md)
