# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

"""Connection-based DB API for Cloud Spanner."""

from google.cloud import spanner_v1

from .connection import Connection
from .exceptions import (
    DatabaseError,
    DataError,
    Error,
    IntegrityError,
    InterfaceError,
    InternalError,
    NotSupportedError,
    OperationalError,
    ProgrammingError,
    Warning,
)
from .parse_utils import get_param_types
from .types import (
    BINARY,
    DATETIME,
    NUMBER,
    ROWID,
    STRING,
    Binary,
    Date,
    DateFromTicks,
    Time,
    TimeFromTicks,
    Timestamp,
    TimestampFromTicks,
)
from .version import google_client_info

apilevel = "2.0"  # supports DP-API 2.0 level.
paramstyle = "format"  # ANSI C printf format codes, e.g. ...WHERE name=%s.

# Threads may share the module, but not connections. This is a paranoid threadsafety
# level, but it is necessary for starters to use when debugging failures.
# Eventually once transactions are working properly, we'll update the
# threadsafety level.
threadsafety = 1


def connect(
    instance_id, database_id, project=None, credentials=None, user_agent=None
):
    """
    Create a connection to Cloud Spanner database.

    :type instance_id: :class:`str`
    :param instance_id: ID of the instance to connect to.

    :type database_id: :class:`str`
    :param database_id: The name of the database to connect to.

    :type project: :class:`str`
    :param project: (Optional) The ID of the project which owns the
                    instances, tables and data. If not provided, will
                    attempt to determine from the environment.

    :type credentials: :class:`google.auth.credentials.Credentials`
    :param credentials: (Optional) The authorization credentials to attach to requests.
                        These credentials identify this application to the service.
                        If none are specified, the client will attempt to ascertain
                        the credentials from the environment.

    :rtype: :class:`google.cloud.spanner_dbapi.connection.Connection`
    :returns: Connection object associated with the given Cloud Spanner resource.

    :raises: :class:`ValueError` in case of given instance/database
             doesn't exist.
    """
    client = spanner_v1.Client(
        project=project,
        credentials=credentials,
        client_info=google_client_info(user_agent),
    )

    instance = client.instance(instance_id)
    if not instance.exists():
        raise ValueError("instance '%s' does not exist." % instance_id)

    database = instance.database(
        database_id, pool=spanner_v1.pool.BurstyPool()
    )
    if not database.exists():
        raise ValueError("database '%s' does not exist." % database_id)

    return Connection(database)


__all__ = [
    "Connection",
    "DatabaseError",
    "DataError",
    "Error",
    "IntegrityError",
    "InterfaceError",
    "InternalError",
    "NotSupportedError",
    "OperationalError",
    "ProgrammingError",
    "Warning",
    "DEFAULT_USER_AGENT",
    "apilevel",
    "connect",
    "paramstyle",
    "threadsafety",
    "get_param_types",
    "Binary",
    "Date",
    "DateFromTicks",
    "Time",
    "TimeFromTicks",
    "Timestamp",
    "TimestampFromTicks",
    "BINARY",
    "STRING",
    "NUMBER",
    "DATETIME",
    "ROWID",
    "TimestampStr",
]
