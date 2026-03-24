class DomainError(Exception):
    """Base exception for domain failures."""


class ValidationDomainError(DomainError):
    """Raised when a value object or entity validation fails."""


class EntityNotFoundError(DomainError):
    """Raised when an entity is not found."""


class ConflictDomainError(DomainError):
    """Raised when data conflicts with existing records."""


class AuthenticationDomainError(DomainError):
    """Raised when authentication cannot be completed."""


class AuthorizationDomainError(DomainError):
    """Raised when a user does not have enough permissions."""
