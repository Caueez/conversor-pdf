from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

from infra.database.implementations.postgres import Postgres
# from infra.cache.implementations.redis import Redis
# from infra.messagering.implementations.rabbitmq import RabbitMQ
from infra.security.password_hashers.bcrypt import BcryptHasher

from account_service.application.interfaces.repository import (
    AuthorizationRepositoryPort,
    SessionRepositoryPort,
    UserRepositoryPort,
)
from account_service.application.schemas import CreateUserDTO
from account_service.application.services.authorization_service import AuthorizationService
from account_service.application.services.user_service import UserService
from account_service.application.use_cases.sessions import SessionUseCase
from account_service.application.use_cases.users import UserUseCase
from account_service.domain.entities.role import ROLE_KEY_ADMIN
from account_service.infra.migration import Migrations
from account_service.infra.repositories.authorization import PostgresAuthorizationRepoAdapter
from account_service.infra.repositories.session import PostgresSessionRepoAdapter
from account_service.infra.repositories.user import PostgresUserRepoAdapter
from account_service.infra.security.bcrypt_hasher_adapter import BcryptPasswordHasherAdapter
from account_service.infra.security.jwt_token_service_adapter import JwtTokenServiceAdapter
from account_service.settings import AccountSettings


@dataclass(slots=True)
class ContainerService:
    settings: AccountSettings

    users: UserUseCase
    sessions: SessionUseCase
    user_service: UserService
    authorization_service: AuthorizationService

    user_repo: UserRepositoryPort
    session_repo: SessionRepositoryPort
    authorization_repo: AuthorizationRepositoryPort

    _migrations: Migrations
    _persistence_backend: Postgres

    @classmethod
    def build(cls, settings: AccountSettings) -> ContainerService:
        persistence_backend = cls._persistence_build(settings=settings)

        user_repo = cls._user_repo_build(settings, persistence_backend)
        session_repo = cls._session_repo_build(settings, persistence_backend)
        authorization_repo = cls._authorization_repo_build(settings, persistence_backend)

        password_hasher = BcryptHasher(rounds=settings.PASSWORD_HASHER_ROUNDS)
        password_hasher = BcryptPasswordHasherAdapter(password_hasher)

        token_service = JwtTokenServiceAdapter(
            secret=settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM,
        )

        authorization_service = AuthorizationService(authorization_repo)
        user_service = UserService(user_repo, password_hasher, authorization_service)
        user_use_case = UserUseCase(user_service)
        session_use_case = SessionUseCase(
            user_service=user_service,
            authorization_service=authorization_service,
            session_repository=session_repo,
            token_service=token_service,
            access_ttl=timedelta(minutes=settings.ACCESS_TOKEN_TTL_MINUTES),
            refresh_ttl=timedelta(days=settings.REFRESH_TOKEN_TTL_DAYS),
        )

        migrations = Migrations(persistence_backend)

        return cls(
            settings=settings,
            user_repo=user_repo,
            session_repo=session_repo,
            authorization_repo=authorization_repo,
            users=user_use_case,
            sessions=session_use_case,
            user_service=user_service,
            authorization_service=authorization_service,
            _persistence_backend=persistence_backend,
            _migrations=migrations,
        )

    @classmethod
    def _persistence_build(cls, settings: AccountSettings) -> Postgres:
        match settings.PERSISTENCE_BACKEND:
            case "postgres":
                return Postgres(settings.POSTGRES_DSN)
            case _:
                raise ValueError("Persistence backend not found")

    @classmethod
    def _user_repo_build(
        cls,
        settings: AccountSettings,
        persistence_backend: Postgres,
    ) -> UserRepositoryPort:
        match settings.USER_REPO:
            case "postgres":
                return PostgresUserRepoAdapter(persistence_backend)
            case _:
                raise ValueError("User repository backend not found")

    @classmethod
    def _session_repo_build(
        cls,
        settings: AccountSettings,
        persistence_backend: Postgres,
    ) -> SessionRepositoryPort:
        match settings.SESSION_REPO:
            case "postgres":
                return PostgresSessionRepoAdapter(persistence_backend)
            case _:
                raise ValueError("Session repository backend not found")

    @classmethod
    def _authorization_repo_build(
        cls,
        settings: AccountSettings,
        persistence_backend: Postgres,
    ) -> AuthorizationRepositoryPort:
        # Authorization persistence is coupled to User repository backend for now.
        match settings.USER_REPO:
            case "postgres":
                return PostgresAuthorizationRepoAdapter(persistence_backend)
            case _:
                raise ValueError("Authorization repository backend not found")

    async def startup(self) -> None:
        await self._persistence_backend.connect()
        await self._migrations.run()
        await self.authorization_service.ensure_defaults()
        await self._bootstrap_admin_if_needed()

    async def shutdown(self) -> None:
        await self._persistence_backend.close()

    async def _bootstrap_admin_if_needed(self) -> None:
        if not self.settings.BOOTSTRAP_ADMIN_ENABLED:
            return

        existing_admin = await self.user_repo.get_by_email(self.settings.BOOTSTRAP_ADMIN_EMAIL)
        if existing_admin:
            return

        dto = CreateUserDTO(
            name=self.settings.BOOTSTRAP_ADMIN_NAME,
            email=self.settings.BOOTSTRAP_ADMIN_EMAIL,
            password=self.settings.BOOTSTRAP_ADMIN_PASSWORD,
            role=ROLE_KEY_ADMIN,
        )
        await self.user_service.create(dto)
