from src.libs.exceptions import AlreadyExists, NotFound


class UserAlreadyExist(AlreadyExists):
    """
    Raised when attempting to create a user that conflicts with an existing one.

    This typically occurs due to unique constraints on the 'login' or 'email'
    fields in the database.

    This usually translates to an HTTP 409 Conflict response.
    """

    pass


class UserNotFound(NotFound):
    """
    Raised when a requested user cannot be found in the database.

    This is used during retrieval, update, or deletion operations when the
    primary key or search criteria yield no results.

    This usually translates to an HTTP 404 Not Found response.
    """

    pass
