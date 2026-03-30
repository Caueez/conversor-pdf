# Matriz De Rastreabilidade

## Regras De Negocio (`docs/BusinessRules.md`)

- `BR-001` Email deve ter formato valido
  - `tests/unit/domain/test_user_value_objects.py::test_email_rejects_invalid_format`
  - `tests/e2e/api/test_user_routes.py::test_create_user_with_invalid_domain_email_returns_422`
- `BR-002` Senha deve ter minimo de 8 caracteres
  - `tests/unit/domain/test_user_value_objects.py::test_password_rejects_too_short`
  - `tests/unit/api/test_api_schemas.py::test_create_user_request_rejects_invalid_min_lengths`
- `BR-003` Senha com limite maximo de 72 caracteres
  - `tests/unit/domain/test_user_value_objects.py::test_password_rejects_above_maximum_length`
  - `tests/unit/api/test_api_schemas.py::test_update_user_request_rejects_password_above_max_length`
- `BR-004` Email unico na criacao
  - `tests/unit/application/test_user_use_case.py::test_create_user_raises_conflict_when_email_already_exists`
  - `tests/e2e/api/test_user_routes.py::test_duplicate_email_returns_409`
- `BR-005` Email unico na atualizacao
  - `tests/unit/application/test_user_use_case.py::test_update_raises_conflict_when_target_email_belongs_to_another_user`
- `BR-006` Update exige ao menos um campo
  - `tests/unit/api/test_api_schemas.py::test_update_user_request_requires_at_least_one_field`
  - `tests/e2e/api/test_user_routes.py::test_patch_requires_at_least_one_field`
- `BR-007` Update/Delete exigem usuario existente
  - `tests/unit/application/test_user_use_case.py::test_delete_raises_when_user_not_found`
  - `tests/unit/application/test_user_use_case.py::test_update_raises_when_user_not_found`
  - `tests/e2e/api/test_user_routes.py::test_delete_missing_user_returns_409`
- `BR-008` `password_hash` nao deve sair na resposta da API
  - `tests/unit/domain/test_user_entity.py::test_user_to_dict_excludes_password_hash_and_serializes_dates`
  - `tests/e2e/api/test_user_routes.py::test_create_user_returns_contract_shape`
- `BR-009` Endpoints de usuario exigem autenticacao
  - `tests/e2e/api/test_user_routes.py::test_user_endpoints_require_authentication`
- `BR-010` Register cria usuario e abre sessao
  - `tests/unit/application/test_session_use_case.py::test_register_creates_user_and_returns_token_pair`
  - `tests/e2e/api/test_session_routes.py::test_register_returns_token_pair_and_authenticates_user`
- `BR-011` Login valida credenciais
  - `tests/unit/application/test_session_use_case.py::test_login_rejects_invalid_credentials`
  - `tests/e2e/api/test_session_routes.py::test_login_with_invalid_credentials_returns_401`
- `BR-012` Refresh valida sessao/jti e rotaciona token
  - `tests/unit/application/test_session_use_case.py::test_refresh_rotates_refresh_token_and_rejects_previous_one`
  - `tests/e2e/api/test_session_routes.py::test_refresh_rotates_refresh_token`
- `BR-013` Logout revoga sessao imediatamente
  - `tests/unit/application/test_session_use_case.py::test_logout_revokes_session_and_blocks_token_usage`
  - `tests/e2e/api/test_session_routes.py::test_logout_revokes_current_session_immediately`

## Contratos HTTP (`docs/Contracts.md`)

- `CT-001` `GET /` -> `200` lista de `UserResponse` (autenticado)
  - `tests/e2e/api/test_user_routes.py::test_get_users_returns_contract_shape`
- `CT-002` `POST /` -> `201` com `UserResponse` (autenticado)
  - `tests/e2e/api/test_user_routes.py::test_create_user_returns_contract_shape`
- `CT-003` `PATCH /{user_id}` -> `200` com `UserResponse` (autenticado)
  - `tests/e2e/api/test_user_routes.py::test_patch_user_returns_contract_shape`
- `CT-004` `DELETE /{user_id}` -> `204` sem corpo (autenticado)
  - `tests/e2e/api/test_user_routes.py::test_delete_user_returns_204_without_body`
- `CT-005` `POST /session/register` -> `201` com `TokenPairResponse`
  - `tests/e2e/api/test_session_routes.py::test_register_returns_token_pair_and_authenticates_user`
- `CT-006` `POST /session/login` -> `200` com `TokenPairResponse`
  - `tests/e2e/api/test_session_routes.py::test_login_returns_token_pair_contract_shape`
- `CT-007` `POST /session/refresh` -> `200` com novo `TokenPairResponse`
  - `tests/e2e/api/test_session_routes.py::test_refresh_rotates_refresh_token`
- `CT-008` `GET /session/me` -> `200` com `UserResponse`
  - `tests/e2e/api/test_session_routes.py::test_me_returns_authenticated_user`
- `CT-009` `POST /session/logout` -> `204` sem corpo
  - `tests/e2e/api/test_session_routes.py::test_logout_revokes_current_session_immediately`
- `CT-010` Mapeamento de erros (`422`/`409`/`401`/`403`/`400`/`500`)
  - `tests/unit/api/test_exception_handlers.py`
  - `tests/e2e/api/test_user_routes.py::test_create_user_with_invalid_domain_email_returns_422`
  - `tests/e2e/api/test_user_routes.py::test_duplicate_email_returns_409`
  - `tests/e2e/api/test_user_routes.py::test_user_endpoints_require_authentication`
  - `tests/e2e/api/test_user_routes.py::test_delete_with_invalid_uuid_returns_400`
