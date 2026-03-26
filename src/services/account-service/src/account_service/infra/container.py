from __future__ import annotations

from dataclasses import dataclass

from infra.database.implementations.postgres import Postgres
# from infra.cache.implementations.redis import Redis
# from infra.messagering.implementations.rabbitmq import RabbitMQ

from account_service.settings import AccountSettings

from account_service.application.interfaces.repository import UserRepositoryPort

from account_service.application.use_cases.users import UserUseCase

from account_service.infra.repositories.user import PostgresUserRepoAdapter

from account_service.infra.migration import Migrations
from infra.security.password_hashers.bcrypt import BcryptHasher

from account_service.infra.security.bcrypt_hasher_adapter import BcryptPasswordHasherAdapter


@dataclass(slots=True)
class ContainerService:
    settings: AccountSettings
    
    users: UserUseCase

    user_repo: UserRepositoryPort

    _migrations: Migrations
    _persistence_backend: Postgres

    @classmethod
    def build(cls, settings: AccountSettings) -> ContainerService:

        persistence_backend = cls._persistence_build(settings=settings)
        user_repo = cls._repo_build(settings, persistence_backend)

        password_hasher = BcryptHasher(rounds=settings.PASSWORD_HASHER_ROUNDS)
        password_hasher = BcryptPasswordHasherAdapter(password_hasher)

        user_use_case = UserUseCase(user_repo, password_hasher)

        migrations = Migrations(persistence_backend)

        return cls(
            settings=settings,
            user_repo=user_repo,
            users=user_use_case,
            _persistence_backend=persistence_backend,
            _migrations=migrations
        )
    
    @classmethod
    def _persistence_build(cls, settings: AccountSettings) -> Postgres:
        match settings.PERSISTENCE_BACKEND:
            case "postgres":
                return Postgres(settings.POSTGRES_DSN)
            case _:
                raise ValueError("Persistence backend not found")
    
    @classmethod
    def _repo_build(
        cls, settings: AccountSettings, persistence_backend: Postgres
    ) -> UserRepositoryPort:
        match settings.USER_REPO:
            case "postgres":
                return PostgresUserRepoAdapter(persistence_backend)
            case _:
                raise ValueError("Persistence backend not found")
            
    async def startup(self) -> None:
        await self._persistence_backend.connect()
        await self._migrations.run()
            
    async def shutdown(self) -> None:
        await self._persistence_backend.close() 
