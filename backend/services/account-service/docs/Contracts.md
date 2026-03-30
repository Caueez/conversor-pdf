# Contratos

## Objetivo
Documentar os contratos de API do `account-service`.

## Escopo
Contratos HTTP expostos atualmente pelo servico.

## Endpoints

### `POST /session/register`

- Objetivo: registrar conta publica e abrir sessao.
- Requisicao (`CreateUserRequest`):
  - `name: string (2..120)`
  - `email: string (5..255)`
  - `password: string (8..72)`
- Resposta: `201` com `TokenPairResponse`.

### `POST /session/login`

- Objetivo: autenticar usuario por email/senha e abrir sessao.
- Requisicao (`LoginRequest`):
  - `email: string (5..255)`
  - `password: string (8..72)`
- Resposta: `200` com `TokenPairResponse`.

### `POST /session/refresh`

- Objetivo: renovar sessao com rotacao de refresh token.
- Requisicao: header `Authorization: Bearer <refresh_token>`.
- Resposta: `200` com novo `TokenPairResponse`.

### `POST /session/logout`

- Objetivo: revogar sessao atual.
- Requisicao: header `Authorization: Bearer <access_token>`.
- Resposta: `204` sem corpo.

### `GET /session/me`

- Objetivo: retornar usuario autenticado.
- Requisicao: header `Authorization: Bearer <access_token>`.
- Resposta: `200` com `UserResponse`.

### `GET /`

- Objetivo: listar usuarios.
- Requisicao: header `Authorization: Bearer <access_token>`.
- Resposta: `200`.
- Corpo: lista de `UserResponse`.

### `POST /`

- Objetivo: criar usuario.
- Requisicao: header `Authorization: Bearer <access_token>`.
- Requisicao (`CreateUserRequest`):
  - `name: string (2..120)`
  - `email: string (5..255)`
  - `password: string (8..72)`
- Resposta: `201` com `UserResponse`.

### `DELETE /{user_id}`

- Objetivo: remover usuario por id.
- Requisicao: header `Authorization: Bearer <access_token>`.
- Parametro de rota: `user_id`.
- Resposta: `204` sem corpo.

### `PATCH /{user_id}`

- Objetivo: atualizar parcialmente um usuario.
- Requisicao: header `Authorization: Bearer <access_token>`.
- Parametro de rota: `user_id`.
- Requisicao (`UpdateUserRequest`):
  - `name?: string (2..120)`
  - `email?: string (5..255)`
  - `password?: string (8..72)`
  - regra: ao menos um campo deve ser enviado.
- Resposta: `200` com `UserResponse`.

## Contrato De Erro (Atual)

- `422`: validacao de dominio/request.
- `409`: conflito de negocio.
- `401`: autenticacao invalida ou ausente.
- `403`: autorizacao negada.
- `400`: erro de validacao de request/value.
- `500`: erro inesperado com mensagem generica.

## Referencias

- [BusinessRules.md](./BusinessRules.md)
