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
from .parse_utils import (
    extract_connection_params, get_param_types, parse_spanner_url,
)
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


def connect(project_name=None, instance_name=None, db_name=None, credentials_uri=None):
    """
    Connect to Cloud Spanner.

    Args:
        project_name: A project that already exists.
        instance_name: An instance that already exists.
        db_name: A database that already exists.
        credentials_uri: An optional string specifying where to retrieve the service
                         account JSON for the credentials to connect to Cloud Spanner.

    Returns:
        The Connection object associated to the Cloud Spanner instance.

    Raises:
        Error if it encounters any unexpected inputs.
    """
    if not db_name:
        raise Error("'db_name' is required.")
    if not instance_name:
        raise Error("'instance_name' is required.")

    client_kwargs = {
        'project': project_name,
        'client_info': google_client_info(),
    }
    if credentials_uri:
        client = spanner.Client.from_service_account_json(credentials_uri, **client_kwargs)
    else:
        client = spanner.Client(**client_kwargs)

    instance = client.instance(instance_name)
    if not instance.exists():
        raise ProgrammingError("instance '%s' does not exist." % instance_name)

    db = instance.database(db_name)
    if not db.exists():
        raise ProgrammingError("database '%s' does not exist." % db_name)

    return Connection(db)


__all__ = [
    'DatabaseError', 'DataError', 'Error', 'IntegrityError', 'InterfaceError',
    'InternalError', 'NotSupportedError', 'OperationalError', 'ProgrammingError',
    'Warning', 'USER_AGENT', 'apilevel', 'connect', 'paramstyle', 'threadsafety',
    'extract_connection_params', 'get_param_types', 'parse_spanner_url',
    'Binary', 'Date', 'DateFromTicks', 'Time', 'TimeFromTicks', 'Timestamp',
    'TimestampFromTicks',
    'BINARY', 'STRING', 'NUMBER', 'DATETIME', 'ROWID', 'TimestampStr',
]
