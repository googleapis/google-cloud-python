# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

"""Spanner DB API exceptions."""


class Warning(Exception):
    """Important DB API warning."""

    pass


class Error(Exception):
    """The base class for all the DB API exceptions.

    Does not include :class:`Warning`.
    """

    pass


class InterfaceError(Error):
    """
    Error related to the database interface
    rather than the database itself.
    """

    pass


class DatabaseError(Error):
    """Error related to the database."""

    pass


class DataError(DatabaseError):
    """
    Error due to problems with the processed data like
    division by zero, numeric value out of range, etc.
    """

    pass


class OperationalError(DatabaseError):
    """
    Error related to the database's operation, e.g. an
    unexpected disconnect, the data source name is not
    found, a transaction could not be processed, a
    memory allocation error, etc.
    """

    pass


class IntegrityError(DatabaseError):
    """
    Error for cases of relational integrity of the database
    is affected, e.g. a foreign key check fails.
    """

    pass


class InternalError(DatabaseError):
    """
    Internal database error, e.g. the cursor is not valid
    anymore, the transaction is out of sync, etc.
    """

    pass


class ProgrammingError(DatabaseError):
    """
    Programming error, e.g. table not found or already
    exists, syntax error in the SQL statement, wrong
    number of parameters specified, etc.
    """

    pass


class NotSupportedError(DatabaseError):
    """
    Error for case of a method or database API not
    supported by the database was used.
    """

    pass
