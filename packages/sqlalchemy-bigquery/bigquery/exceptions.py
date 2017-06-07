"""Exceptions used in the Google BigQuery DB-API."""


class Warning(Exception):
    """Exception raised for important warnings."""
    pass


class Error(Exception):
    """Exception representing all non-warning errors."""
    pass


class InterfaceError(Error):
    """Exception raised for errors related to the database interface."""
    pass


class DatabaseError(Error):
    """Exception raised for errors related to the database."""
    pass


class DataError(DatabaseError):
    """Exception raised for errors due to problems with the processed data."""
    pass


class OperationalError(DatabaseError):
    """Exception raised for errors related to the database operation.

    These errors are not necessarily under the control of the programmer.
    """
    pass


class IntegrityError(DatabaseError):
    """Exception raised when integrity of the database is affected."""
    pass


class InternalError(DatabaseError):
    """Exception raised when the database encounters an internal error."""
    pass


class ProgrammingError(DatabaseError):
    """Exception raised for programming errors."""
    pass


class NotSupportedError(DatabaseError):
    """Exception raised for operations not supported by the database or API."""
    pass
