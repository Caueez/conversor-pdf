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

## Limites

- Nao alterar contrato de API silenciosamente.
- Nao vazar detalhes internos de excecao para clientes externos.
- Nao acoplar `domain` a framework ou tecnologia de infraestrutura.
- Nao executar acoes destrutivas sem solicitacao explicita.

## Referencias

- [Architecture.md](./Architecture.md)
- [Contracts.md](./Contracts.md)
- [BusinessRules.md](./BusinessRules.md)
- [Contributing.md](./Contributing.md)
- [ValidationRoadmap.md](./ValidationRoadmap.md)
