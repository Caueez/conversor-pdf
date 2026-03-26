# Agent

## Objetivo
Definir como agentes devem atuar neste repositorio para manter consistencia tecnica e colaboracao segura.

## Escopo
Aplica-se a alteracoes de codigo, infraestrutura e documentacao.

## Regras De Operacao

- Respeitar os limites de arquitetura (`api`, `application`, `domain`, `infra`).
- Priorizar mudancas pequenas, rastreaveis e com justificativa clara.
- Tratar seguranca (senha, token, segredo) como fluxo explicito e revisavel.
- Atualizar documentacao sempre que contrato, regra de negocio ou arquitetura mudar.
- Priorizar a idealizacao de tasks com escopo claro, dependencias, conflitos, riscos e linha do tempo.
- Apresentar o planejamento da task para validacao do programador antes de executar alteracoes de implementacao.
- Incluir testes no inicio da linha do tempo e registrar se novos testes sao necessarios.
- Ao final da implementacao do programador, revisar arquivos alterados, validar aderencia a task e executar testes necessarios.
- Em caso de ambiguidade tecnica, registrar perguntas objetivas ao programador antes de alterar codigo.
- Manter a task como fonte viva de contexto, evidencias e decisoes.
- Em `src/`, alterar por padrao um arquivo por vez; mudancas em multiplos arquivos exigem permissao explicita do programador.

## Limites

- Nao alterar contrato de API silenciosamente.
- Nao vazar detalhes internos de excecao para clientes externos.
- Nao acoplar `domain` a framework ou tecnologia de infraestrutura.
- Nao executar acoes destrutivas sem solicitacao explicita.
- Nao implementar codigo de produto sem solicitacao do programador.

## Referencias

- [Architecture.md](./Architecture.md)
- [Contracts.md](./Contracts.md)
- [BusinessRules.md](./BusinessRules.md)
- [Contributing.md](./Contributing.md)
- [ValidationRoadmap.md](./ValidationRoadmap.md)
