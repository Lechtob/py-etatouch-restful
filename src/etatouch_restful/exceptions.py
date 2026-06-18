"""ETA Touch client exceptions."""


class EtaTouchError(Exception):
    """Base exception for ETA Touch client errors."""


class EtaTouchConnectionError(EtaTouchError):
    """Raised when the ETA Touch device cannot be reached."""


class EtaTouchResponseError(EtaTouchError):
    """Raised when ETA Touch returns an unsuccessful response."""

    def __init__(self, message: str, *, status: int | None = None, body: str | None = None) -> None:
        super().__init__(message)
        self.status = status
        self.body = body

