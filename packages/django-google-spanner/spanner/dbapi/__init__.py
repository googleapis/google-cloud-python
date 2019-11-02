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

from .connect import Connection
from .exceptions import Error
from .parse_utils import parse_spanner_url

def connect(conn_params, credentials_uri=None):
    """Connects to Cloud Spanner.

    Args:
        conn_params: A dictionary specifying how to connect to Cloud Spanner.
                     Its keys include:
                        database        (mandatory)  -- the name of the database to be connected to or created.
                        instance        (mandatory)  -- the name of the instance to be connected to or created.
                        project_id      (optional)   -- the project_id of the Cloud Spanner instance.
                        instance_config (optional) -- the zone that'll be used to create any non-existent instances.
                                        Should be of the form:
                                                    projects/project-id/instanceConfigs/region

        credentials_uri: An optional string specifying where to retrieve the service
                         account JSON for the credentials to connect to Cloud Spanner.

    Returns:
        The Connection object associated to the Cloud Spanner instance.

    Raises:
        Error if it encounters any unexpected inputs.
    """
    kwargs = dict(
        project=conn_params.get('project_id'),
        user_agent=USER_AGENT,
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

        instance.configuration_name =  instance_config
        lro = instance.create()
        # TODO: Report the long-running operation result.
        _ = lro

    db = instance.database(db_name)
    if not db.exists():
        lro = db.create()
        # TODO: Report the long-running operation result.
        _ = lro

    return Connection(db)
