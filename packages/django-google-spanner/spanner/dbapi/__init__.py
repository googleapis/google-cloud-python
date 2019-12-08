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
    extract_connection_params, infer_param_types, parse_spanner_url,
    validate_instance_config,
)
from .types import (
    BINARY, DATETIME, NUMBER, ROWID, STRING, Date, DateFromTicks, Time,
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


def connect(spanner_url, credentials_uri=None):
    """Connects to Cloud Spanner.

    Args:
        spanner_url: A string specifying how to connect to Cloud Spanner.
                     It will be of the format:
                        cloudspanner:[//host[:port]]/projects/<project-id>/instances/<instance-id>/databases/<database-name>[?property-name=property-value[;]]*

                     For example:
                        * cloudspanner:/projects/foo/instances/bar/databases/db
                        * cloudspanner://spanner.googleapis.com/projects/foo/instances/bar/databases/db
                        * cloudspanner://spanner.googleapis.com:443/projects/foo/instances/bar/databases/db

                    If an instance doesn't yet exist, the property
                            "instance_config"
                    must be set and match the format.
                                ^projects/project-id/instanceConfigs/region$
                    for example:
                                projects/odeke-sandbox/instanceConfigs/regional-us-west2

        credentials_uri: An optional string specifying where to retrieve the service
                         account JSON for the credentials to connect to Cloud Spanner.

    Returns:
        The Connection object associated to the Cloud Spanner instance.

    Raises:
        Error if it encounters any unexpected inputs.
    """

    conn_params = parse_spanner_url(spanner_url)

    kwargs = dict(
        project=conn_params.get('project_id'),
        client_info=google_client_info(),
    )

    # Pre-requisite are the database and instance names.
    db_name = conn_params.get('database')
    if not db_name:
        raise Error("expected 'database'")
    instance_name = conn_params.get('instance')
    if not instance_name:
        raise Error("expected 'instance'")

    credentials_uri = conn_params.get('credentials_uri')
    client = None

    if credentials_uri:
        client = spanner.Client.from_service_account_json(credentials_uri, **kwargs)
    else:
        client = spanner.Client(**kwargs)

    instance = client.instance(instance_name)
    if not instance.exists():
        # Attempt to create the instance if it doesn't yet exist.
        instance_config = conn_params.get('instance_config')
        if not instance_config:
            raise Error("instance '%s' does not yet exist yet no 'default_zone' was set" % instance_name)

        err_msg = validate_instance_config(instance_config)
        if err_msg:
            raise Error(err_msg)

        instance.configuration_name = instance_config
        lro = instance.create()
        # Synchronously wait on the operation's completion.
        # TODO: Report the long-running operation result.
        _ = lro.result()

    db = instance.database(db_name)
    if not db.exists():
        lro = db.create()
        # Synchronously wait on the operation's completion.
        # TODO: Report the long-running operation result.
        _ = lro.result()

    return Connection(db)


__all__ = [
    'DatabaseError', 'DataError', 'Error', 'IntegrityError', 'InterfaceError',
    'InternalError', 'NotSupportedError', 'OperationalError', 'ProgrammingError',
    'Warning', 'USER_AGENT', 'apilevel', 'connect', 'paramstyle', 'threadsafety',
    'extract_connection_params', 'infer_param_types', 'parse_spanner_url',
    'Date', 'DateFromTicks', 'Time', 'TimeFromTicks', 'Timestamp', 'TimestampFromTicks',
    'BINARY', 'STRING', 'NUMBER', 'DATETIME', 'ROWID', 'TimestampStr',
]
