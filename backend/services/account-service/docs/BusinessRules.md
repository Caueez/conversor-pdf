# Regras De Negocio

## Objetivo
Registrar regras de negocio ativas no `account-service`.

## Escopo
Regras funcionais implementadas em dominio, aplicacao e contrato de entrada.

## Regras Atuais

- Email deve ter formato valido.
- Senha deve ter minimo de 8 caracteres e maximo de 72.
- Email deve ser unico para criacao de usuario.
- Em atualizacao, se email for alterado, deve continuar unico.
- Atualizacao de usuario exige ao menos um campo no payload (`name`, `email` ou `password`).
- Operacoes de update/delete exigem que o usuario exista.
- `password_hash` nao deve ser retornado em respostas da API.
- Endpoints de usuario exigem access token valido.
- Register deve criar usuario e abrir sessao com par access/refresh.
- Login deve validar email/senha e retornar par access/refresh.
- Refresh deve validar sessao ativa + `jti` atual e rotacionar refresh token.
- Logout deve revogar a sessao atual imediatamente.
- Access token revogado deve ser bloqueado por validacao de sessao em banco.
- Bootstrap de admin: quando habilitado e sem usuarios, cria usuario inicial a partir de variaveis de ambiente.

## Observacoes

- Sessao usa access JWT (TTL curto) + refresh JWT (TTL longo) com estado em `sessions`.
- Algoritmo padrao de token: `HS256`.

## Referencias

- [Contracts.md](./Contracts.md)
