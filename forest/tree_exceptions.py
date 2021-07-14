"""Tree Exception Definitions."""


class DuplicateKeyError(Exception):
    """Raised when a key already exists."""

    def __init__(self, key: str) -> None:
        Exception.__init__(self, f"{key} already exists.")
