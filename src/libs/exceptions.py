class AlreadyExists(Exception):
    """Raised when object violets uniqueness rules, and already exists"""


class NotFound(Exception):
    """Raised when object not found"""


class PaginationError(Exception):
    """Raised when pagination limit or offset incorrect"""
