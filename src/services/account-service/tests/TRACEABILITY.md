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

## Contratos HTTP (`docs/Contracts.md`)

- `CT-001` `GET /` -> `200` lista de `UserResponse`
  - `tests/e2e/api/test_user_routes.py::test_get_users_returns_contract_shape`
- `CT-002` `POST /` -> `201` com `UserResponse`
  - `tests/e2e/api/test_user_routes.py::test_create_user_returns_contract_shape`
- `CT-003` `PATCH /{user_id}` -> `200` com `UserResponse`
  - `tests/e2e/api/test_user_routes.py::test_patch_user_returns_contract_shape`
- `CT-004` `DELETE /{user_id}` -> `204` sem corpo
  - `tests/e2e/api/test_user_routes.py::test_delete_user_returns_204_without_body`
- `CT-005` Mapeamento de erros (`422`/`409`/`400`/`500`)
  - `tests/unit/api/test_exception_handlers.py`
  - `tests/e2e/api/test_user_routes.py::test_create_user_with_invalid_domain_email_returns_422`
  - `tests/e2e/api/test_user_routes.py::test_duplicate_email_returns_409`
  - `tests/e2e/api/test_user_routes.py::test_delete_with_invalid_uuid_returns_400`
