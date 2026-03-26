# Chat Operacional

## Objetivo
Este arquivo recebe a solicitacao ativa para criacao/implementacao de tarefas.

## Regra De Uso

- Escrever a solicitacao no bloco `Solicitacao Atual`.
- O agente deve ler e respeitar os documentos obrigatorios antes de executar.
- O agente deve classificar o escopo (geral ou servico) antes de criar/alterar task.
- O agente deve verificar conflito com tasks existentes antes de abrir nova task.
- Ao final da chamada, o agente pode limpar a solicitacao deste arquivo.
- O resultado nao pode se perder: deve ser persistido na task correspondente.

## Bloco 1 - Solicitacao Atual

Preencha abaixo com o pedido atual:

```text
[descreva aqui a tarefa, contexto, restricoes e resultado esperado]
```

## Bloco 2 - Compliance Obrigatorio Do Agente

Antes de executar, o agente deve confirmar leitura dos documentos:

- [ ] `docs/Index.md`
- [ ] `docs/Contributing.md`
- [ ] `docs/Architecture.md`
- [ ] `docs/Contracts.md`
- [ ] `docs/BusinessRules.md`
- [ ] `docs/ValidationRoadmap.md`
- [ ] `src/services/account-service/docs/Index.md` (se a tarefa for do servico)

## Bloco 3 - Mapeamento De Execucao

O agente deve registrar:

- Escopo unico identificado:
- Branch planejada (sempre a partir de `develop`):
- Task alvo (arquivo em `docs/tasks/` ou `src/services/.../docs/tasks/`):
- Conflitos com tasks existentes:
- Necessidade de task em outro servico (sim/nao):

## Bloco 4 - Persistencia Obrigatoria

Ao concluir, o agente deve atualizar a task com:

- `Branch de implementacao`
- `Commit de implementacao`
- `Status`
- `Data de finalizacao` (se concluida)
- `Linha Do Tempo` (ordem e dependencias)
- `Conflitos Mapeados`
- Evidencias da implementacao

## Bloco 5 - Reset Controlado

- O agente pode resetar os blocos 1, 2 e 3 ao fim da chamada.
- Nao pode apagar historico funcional: tudo deve estar persistido na task.
