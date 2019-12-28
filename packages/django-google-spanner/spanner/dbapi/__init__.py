# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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

    db = client_instance.database(database)
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
