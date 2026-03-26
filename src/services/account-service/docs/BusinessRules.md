# Regras De Negocio

## Objetivo
Registrar regras de negocio ativas no `account-service`.

## Escopo
Regras funcionais implementadas em dominio, aplicacao e contrato de entrada.

## Regras Atuais

- Email deve ter formato valido.
- Senha deve ter minimo de 8 caracteres.
- No estado atual de `develop`, dominio nao aplica limite maximo de senha.
- Email deve ser unico para criacao de usuario.
- Em atualizacao, se email for alterado, deve continuar unico.
- Atualizacao de usuario exige ao menos um campo no payload (`name`, `email` ou `password`).
- Operacoes de update/delete exigem que o usuario exista.
- `password_hash` nao deve ser retornado em respostas da API.

## Observacoes

- Contrato de API atual limita senha em `128` caracteres.
- Existe proposta de alinhamento para `72` em revisao humana na branch `feat/account-service-password-hardening`.

## Referencias

- [Contracts.md](./Contracts.md)
- [ValidationRoadmap.md](./ValidationRoadmap.md)
- [Regras de negocio da raiz](../../../../docs/BusinessRules.md)
