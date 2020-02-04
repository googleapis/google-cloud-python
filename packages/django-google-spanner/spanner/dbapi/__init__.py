# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

import threading

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
# '@' is used by Cloud Spanner as the param style but that style isn't listed
# in any of the options  https://www.python.org/dev/peps/pep-0249/#paramstyle
# so we are going with a custom named paramstyle.
paramstyle = 'at-named'
threadsafety = 2  # Threads may share the module and connections but not cursors.


def connect(project=None, instance=None, database=None, credentials_uri=None):
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
        'client_info': google_client_info(),
    }
    if credentials_uri:
        client = spanner.Client.from_service_account_json(credentials_uri, **client_kwargs)
    else:
        client = spanner.Client(**client_kwargs)

    client_instance = client.instance(instance)
    if not client_instance.exists():
        raise ProgrammingError("instance '%s' does not exist." % instance)

    # Create a session pool that'll periodically refresh every 3 minutes (arbitrary choice value).
    pool = spanner.PingingPool(size=10, default_timeout=5, ping_interval=180)
    background_thread = threading.Thread(target=pool.ping, name='ping-pool')
    background_thread.daemon = True
    background_thread.start()

    db = client_instance.database(database, pool=pool)
    if not db.exists():
        raise ProgrammingError("database '%s' does not exist." % database)

    return Connection(db)


__all__ = [
    'DatabaseError', 'DataError', 'Error', 'IntegrityError', 'InterfaceError',
    'InternalError', 'NotSupportedError', 'OperationalError', 'ProgrammingError',
    'Warning', 'USER_AGENT', 'apilevel', 'connect', 'paramstyle', 'threadsafety',
    'get_param_types',
    'Binary', 'Date', 'DateFromTicks', 'Time', 'TimeFromTicks', 'Timestamp',
    'TimestampFromTicks',
    'BINARY', 'STRING', 'NUMBER', 'DATETIME', 'ROWID', 'TimestampStr',
]
