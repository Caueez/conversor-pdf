# Agent

## Objetivo
Definir como agentes devem atuar no `account-service` sem quebrar regras de dominio e contrato de API.

## Escopo
`api`, `application`, `domain`, `infra`, migrations e documentacao do servico.

## Regras De Operacao

- Tratar `domain` como fonte de invariantes de negocio.
- Implementar detalhes tecnicos (hash, banco, observabilidade) em `infra` via portas.
- Manter alinhamento entre validacoes de API e regras de dominio.
- Registrar alteracoes relevantes em contratos e roadmap de validacao.

## Limites

- Nao expor `password_hash` em respostas da API.
- Nao adicionar dependencia de framework dentro de `domain`.
- Nao alterar contrato externo sem atualizar `Contracts.md`.

## Referencias

- [Architecture.md](./Architecture.md)
- [Contracts.md](./Contracts.md)
- [BusinessRules.md](./BusinessRules.md)
- [Contributing.md](./Contributing.md)
- [ValidationRoadmap.md](./ValidationRoadmap.md)
