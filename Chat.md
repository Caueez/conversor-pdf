# Chat Operacional

## Objetivo
Este arquivo recebe a solicitacao ativa para criacao/implementacao de tarefas.

## Regra De Uso

- Escrever a solicitacao no bloco `Solicitacao Atual`.
- O agente deve ler e respeitar os documentos obrigatorios antes de executar.
- O agente deve classificar o escopo (geral ou servico) antes de criar/alterar task.
- O agente deve verificar conflito com tasks existentes antes de abrir nova task.
- O planejamento formal da task deve ser validado pelo programador antes de execucao de alteracoes de implementacao.
- Ao final da chamada, o agente pode limpar a solicitacao deste arquivo.
- O resultado nao pode se perder: deve ser persistido na task correspondente.

## Bloco 1 - Solicitacao Atual

Preencha abaixo com o pedido atual:

### Mudancas/adição na documentacao do agente
    O agente deve apenas auxiliar na idealização do task, planejando implementação, integração, validando ideias para resolução da task, criando a timeline ideal, validando/criando tasks auxiliares e buscando incongruencias, incompatibilidades e/ou problemas invisiveis na taks. A mesma task deve tambem informar se novos testes devem ser criados, alem de validar se testes existentes ja fazem parte do escopo. Tambem é importante dentro da task exibir alterações necessarias na documentação (geralmente apenas o agente realizara mudanças na documentação, mas quero manter um contexto valido para o programador responsavel).
    
    O agente tambem deve ao final da implementação do programador, validar todos os arquivos alterados, verificando se atende os requisitos da task, buscando erros e bugs, alem de podem rodar os testes necessarios.

    O agente pode realizar perguntas para o programador ao criar a task ou modificações requeridas em codigo, quando encontrar pontos de ambiguidade.

### Testes
    Testes devem ser realizados antes da implementação, na timeline das tasks, os testes devem estar logo no inicio.
    Os testes são o principal meio de validação, alem de erros de escrita, sintax ou logica que o programador ou/e o agente devem localizar e corrigir.

### Fluxo de desenvolvimento
    Todo codigo deve ser feito pelo programador, o agente deve realizar modificações em arquivos dentro de /src quando solicitado e a alteração deve ser focada em um arquivo apenas, se alterações devem ser feitas em varios arquivos, apenas deve ser realizado com permissão do programador ou apenas informado quais alterações precisam ser feitas (O arquivo da task pode ser alterado pela necessidade de alterações ou criações intermediarias as ja impostas no arquivo e na timeline, task é o arquivo vivo das mudanças realizadas).
    Realizado o escopo da task, o agente fica responsavel por toda validação com os testes e codigo, tambem é resposavel pelo fluxo do git.
    O agente tambem fica responsavel por toda a documentação.

### OBS
    O sistema de tasks ja deve ser utilizado, entao mudanças necessarias para esse Chat.md devem ser colocadas em task de escopo, mesmo as mudanças que provavelmente apenas o agente ira realizar ou que seja apenas de documentação, tudo vai para task.

## Bloco 2 - Compliance Obrigatorio Do Agente

Antes de executar, o agente deve confirmar leitura dos documentos:

- [x] `docs/Index.md`
- [x] `docs/Contributing.md`
- [x] `docs/Architecture.md`
- [x] `docs/Contracts.md`
- [x] `docs/BusinessRules.md`
- [x] `docs/ValidationRoadmap.md`
- [ ] `src/services/account-service/docs/Index.md` (nao aplicavel: tarefa de escopo geral)

## Bloco 3 - Mapeamento De Execucao

O agente deve registrar:

- Escopo unico identificado: Geral do monorepo (governanca operacional do agente e fluxo de tasks/documentacao).
- Branch planejada (sempre a partir de `develop`): `docs/governanca-operacional-agente` (criada).
- Task alvo (arquivo em `docs/tasks/` ou `src/services/.../docs/tasks/`): `docs/tasks/task-009-governanca-operacional-do-agente-e-fluxo-de-tasks.md`.
- Conflitos com tasks existentes: sobreposicao parcial com `docs/tasks/task-004-test-coverage.md` no tema de testes; sem conflito bloqueante por escopo distinto (governanca x implementacao tecnica).
- Necessidade de task em outro servico (sim/nao): nao.

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
