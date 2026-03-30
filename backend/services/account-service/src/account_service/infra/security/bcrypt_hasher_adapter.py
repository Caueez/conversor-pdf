

from account_service.application.interfaces.hasher import PasswordHasherPort

from infra.security.password_hashers.bcrypt import BcryptHasher


class BcryptPasswordHasherAdapter(PasswordHasherPort):
    def __init__(self, password_hasher: BcryptHasher) -> None:
        self._password_hasher = password_hasher

    def hash(self, password: str) -> str:
        return self._password_hasher.hash(password)

    def check(self, password: str, hashed_password: str) -> bool:
        return self._password_hasher.check(password, hashed_password)

        