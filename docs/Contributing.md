# Contribuindo

## Objetivo
Padronizar contribuicoes tecnicas, fluxo de git e qualidade de entrega.

## Escopo
Aplica-se a todo o monorepo.

## Escopo Das Tasks

- `docs/tasks/` (raiz): somente tarefas de escopo geral do monorepo.
- `src/services/<servico>/docs/tasks/`: tarefas especificas de cada servico.
- Se a implementacao principal exigir mudancas em outro servico, criar task no servico impactado e registrar a ordem na linha do tempo da task principal.

## Fluxo Git Obrigatorio (Fim Da Implementacao)

1. Classificar o escopo da entrega (geral do monorepo ou servico especifico).
2. Verificar se ja existe task com mesmo objetivo para evitar duplicidade/conflito.
3. Separar arquivos em grupos de escopo unico.
4. Para cada grupo, criar uma branch nova sempre a partir de `develop`.
5. Dentro de cada branch, realizar commits pequenos com escopo ainda mais reduzido.
6. Preencher as tasks da branch com commits de implementacao, linha do tempo, dependencias e conflitos mapeados.
7. Aguardar revisao humana.
8. Somente apos confirmacao humana, fazer merge da branch em `develop`.

## Regras De Branch

- Toda branch deve nascer de `develop`.
- Sugestao de nome: `tipo/escopo-curto`.
- Cada branch deve tratar um unico objetivo tecnico.

Exemplo:

```bash
git checkout develop
git pull
git checkout -b feat/nome-do-escopo
```

## Regras De Commit

- Commits pequenos e coesos.
- Cada commit deve representar uma mudanca verificavel.
- Mensagem de commit deve ser objetiva e descrever o escopo real.

## Registro Em Tasks

Para cada task tocada na branch:

- Preencher `Branch de implementacao` com o nome da branch.
- Preencher `Commit de implementacao` com os hashes dos commits da branch relacionados a task.
- Atualizar `Status` e `Data de finalizacao` quando concluida.
- Manter `Linha Do Tempo` com ordem real de execucao e dependencias entre tasks.
- Registrar em `Conflitos Mapeados` qualquer sobreposicao de escopo com outra task (e a decisao tomada).

## Script De Tarefas

- Criar nova tarefa na raiz:
  - `scripts/docs/new_task.sh --scope root --titulo "Titulo da tarefa"`
- Criar nova tarefa em um servico:
  - `scripts/docs/new_task.sh --scope service --service account-service --titulo "Titulo da tarefa"`

## Regras De Contribuicao

- Atualizar contratos quando houver mudanca de payload/response/status.
- Atualizar regras de negocio quando invariantes mudarem.
- Registrar tarefas concluidas/pendentes em `ValidationRoadmap.md` e `tasks/`.
- Priorizar retrocompatibilidade e explicitar breaking changes.
- Quando houver impacto em mais de um servico, quebrar em tasks por servico e registrar ordem de implementacao na task principal.

## Checklist Minimo Antes De Finalizar

- Codigo compila/roda no contexto local.
- Documentacao impactada foi atualizada.
- Riscos e pendencias foram registrados.

## Referencias

- [Agent.md](./Agent.md)
- [Contracts.md](./Contracts.md)
- [ValidationRoadmap.md](./ValidationRoadmap.md)
