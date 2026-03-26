# Contratos

## Objetivo
Documentar os contratos de API do `account-service`.

## Escopo
Contratos HTTP expostos atualmente pelo servico.

## Endpoints

### `GET /`

- Objetivo: listar usuarios
- Resposta: `200`
- Corpo: lista de `UserResponse`

### `POST /`

- Objetivo: criar usuario
- Requisicao (`CreateUserRequest`):
  - `name: string (2..120)`
  - `email: string (5..255)`
  - `password: string (8..128)`
- Resposta: `201` com `UserResponse`

### `DELETE /{user_id}`

- Objetivo: remover usuario por id
- Parametro de rota: `user_id`
- Resposta: `204` sem corpo

### `PATCH /{user_id}`

- Objetivo: atualizar parcialmente um usuario
- Parametro de rota: `user_id`
- Requisicao (`UpdateUserRequest`):
  - `name?: string (2..120)`
  - `email?: string (5..255)`
  - `password?: string (8..128)`
  - regra: ao menos um campo deve ser enviado
- Resposta: `200` com `UserResponse`

## Observacao De Evolucao

- Existe ajuste para `8..72` em revisao humana na branch `feat/account-service-password-hardening` (tasks 003 e 016).

## Contrato De Erro (Atual)

- `422`: validacao de dominio
- `409`: conflito de negocio
- `400`: erro de validacao de request/value
- `500`: erro inesperado com mensagem generica

## Referencias

- [BusinessRules.md](./BusinessRules.md)
- [ValidationRoadmap.md](./ValidationRoadmap.md)
- [Contratos da raiz](../../../../docs/Contracts.md)
