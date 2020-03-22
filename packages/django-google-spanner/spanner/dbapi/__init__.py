# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

from google.cloud import spanner_v1 as spanner

from .connection import Connection
# These need to be included in the top-level package for PEP-0249 DB API v2.
from .exceptions import (
    DatabaseError, DataError, Error, IntegrityError, InterfaceError,
    InternalError, NotSupportedError, OperationalError, ProgrammingError,
    Warning,
)
from .parse_utils import get_param_types
from .types import (
    BINARY, DATETIME, NUMBER, ROWID, STRING, Binary, Date, DateFromTicks, Time,
    TimeFromTicks, Timestamp, TimestampFromTicks,
)
from .version import google_client_info

# Globals that MUST be defined ###
apilevel = "2.0"  # Implements the Python Database API specification 2.0 version.
# We accept arguments in the format '%s' aka ANSI C print codes.
# as per https://www.python.org/dev/peps/pep-0249/#paramstyle
paramstyle = 'format'
# Threads may share the module but not connections. This is a paranoid threadsafety level,
# but it is necessary for starters to use when debugging failures. Eventually once transactions
# are working properly, we'll update the threadsafety level.
threadsafety = 1


def connect(project=None, instance=None, database=None, credentials_uri=None, user_agent=None, autocommit=True):
    """
    Connect to Cloud Spanner.

    Args:
        project: The id of a project that already exists.
        instance: The id of an instance that already exists.
        database: The name of a database that already exists.
        credentials_uri: An optional string specifying where to retrieve the service
                         account JSON for the credentials to connect to Cloud Spanner.

    Returns:
        The Connection object associated to the Cloud Spanner instance.

    Raises:
        Error if it encounters any unexpected inputs.
    """
    if not project:
        raise Error("'project' is required.")
    if not instance:
        raise Error("'instance' is required.")
    if not database:
        raise Error("'database' is required.")

    client_kwargs = {
        'project': project,
        'client_info': google_client_info(user_agent),
    }
    if credentials_uri:
        client = spanner.Client.from_service_account_json(credentials_uri, **client_kwargs)
    else:
        client = spanner.Client(**client_kwargs)

    client_instance = client.instance(instance)
    if not client_instance.exists():
        raise ProgrammingError("instance '%s' does not exist." % instance)

    db = client_instance.database(database, pool=spanner.pool.BurstyPool())
    if not db.exists():
        raise ProgrammingError("database '%s' does not exist." % database)

    # Correctly retrieve a session from the session pool.
    # See:
    #   * https://github.com/orijtech/django-spanner/issues/291
    #   * https://github.com/googleapis/python-spanner/issues/10#issuecomment-585056760
    #
    # Adapted from:
    #   https://bit.ly/3c8MK6p: python-spanner, Git hash 997a03477b07ec39c7184
    #   google/cloud/spanner_v1/pool.py#L514-L535
    # TODO: File a bug to googleapis/python-spanner asking for a convenience
    # method since invoke database.session() gives the wrong result
    # yet requires a context manager wrapped with SessionCheckout
    # and needs accessing private methods, which leaks the details of the
    # implementation in order to try to use it correctly.
    pool = db._pool
    session_checkout = spanner.pool.SessionCheckout(pool)
    session = session_checkout.__enter__()
    if not session.exists():
        session.create()
    return_session = lambda: session_checkout.__exit__() # noqa

    return Connection(autocommit, db, session, return_session)


__all__ = [
    'DatabaseError', 'DataError', 'Error', 'IntegrityError', 'InterfaceError',
    'InternalError', 'NotSupportedError', 'OperationalError', 'ProgrammingError',
    'Warning', 'DEFAULT_USER_AGENT', 'apilevel', 'connect', 'paramstyle', 'threadsafety',
    'get_param_types',
    'Binary', 'Date', 'DateFromTicks', 'Time', 'TimeFromTicks', 'Timestamp',
    'TimestampFromTicks',
    'BINARY', 'STRING', 'NUMBER', 'DATETIME', 'ROWID', 'TimestampStr',
]
