# Contribuindo

## Objetivo
Padronizar contribuicoes tecnicas com um fluxo simples e previsivel.

## Escopo
Aplica-se a todo o monorepo.

## Fluxo De Trabalho

1. Entender o problema e confirmar escopo da mudanca.
2. Definir o comportamento esperado em teste (TDD).
3. Escrever teste primeiro e validar falha inicial.
4. Implementar o minimo necessario para o teste passar.
5. Refatorar mantendo testes verdes.
6. Atualizar documentacao impactada.
7. Abrir revisao com contexto objetivo da alteracao.

## Regra TDD

- Ordem obrigatoria: `Red -> Green -> Refactor`.
- Testes devem guiar implementacao, nao o contrario.
- Ao corrigir bug, primeiro criar/ajustar teste de regressao.
- Toda task deve usar o checklist completo em `development/tasks/task-template.md`.

## Regras De Branch

- Criar branch a partir de `develop`.
- Cada branch deve tratar um unico objetivo tecnico.
- Nome sugerido: `tipo/escopo-curto`.

## Regras De Commit

- Commits pequenos e coesos.
- Cada commit deve representar uma mudanca verificavel.
- Mensagem de commit deve descrever o escopo real.

## Checklist Minimo Antes De Finalizar

- Codigo compila/roda no contexto local.
- Testes relevantes passaram.
- Documentacao impactada foi atualizada.
- Riscos e pendencias relevantes foram registrados na revisao.

## Referencias

- [Agent.md](./Agent.md)
- [ValidationRoadmap.md](./ValidationRoadmap.md)
