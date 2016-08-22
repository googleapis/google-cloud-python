# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Parent client for calling the Google Cloud Bigtable API.

This is the base from which all interactions with the API occur.

In the hierarchy of API concepts

* a :class:`Client` owns an :class:`.Instance`
* a :class:`.Instance` owns a :class:`Table <gcloud.bigtable.table.Table>`
* a :class:`Table <gcloud.bigtable.table.Table>` owns a
  :class:`ColumnFamily <.column_family.ColumnFamily>`
* a :class:`Table <gcloud.bigtable.table.Table>` owns a :class:`Row <.row.Row>`
  (and all the cells in the row)
"""


from pkg_resources import get_distribution

from gcloud._helpers import make_stub
from gcloud.bigtable._generated import bigtable_instance_admin_pb2
from gcloud.bigtable._generated import bigtable_pb2
from gcloud.bigtable._generated import bigtable_table_admin_pb2
from gcloud.bigtable._generated import operations_grpc_pb2
from gcloud.bigtable.cluster import DEFAULT_SERVE_NODES
from gcloud.bigtable.instance import Instance
from gcloud.bigtable.instance import _EXISTING_INSTANCE_LOCATION_ID
from gcloud.client import _ClientFactoryMixin
from gcloud.client import _ClientProjectMixin
from gcloud.credentials import get_credentials


TABLE_ADMIN_HOST = 'bigtableadmin.googleapis.com'
"""Table Admin API request host."""
TABLE_ADMIN_PORT = 443
"""Table Admin API request port."""

INSTANCE_ADMIN_HOST = 'bigtableadmin.googleapis.com'
"""Cluster Admin API request host."""
INSTANCE_ADMIN_PORT = 443
"""Cluster Admin API request port."""

DATA_API_HOST = 'bigtable.googleapis.com'
"""Data API request host."""
DATA_API_PORT = 443
"""Data API request port."""

OPERATIONS_API_HOST = INSTANCE_ADMIN_HOST
OPERATIONS_API_PORT = INSTANCE_ADMIN_PORT

ADMIN_SCOPE = 'https://www.googleapis.com/auth/bigtable.admin'
"""Scope for interacting with the Cluster Admin and Table Admin APIs."""
DATA_SCOPE = 'https://www.googleapis.com/auth/bigtable.data'
"""Scope for reading and writing table data."""
READ_ONLY_SCOPE = 'https://www.googleapis.com/auth/bigtable.data.readonly'
"""Scope for reading table data."""

DEFAULT_USER_AGENT = 'gcloud-python/{0}'.format(
    get_distribution('gcloud').version)
"""The default user agent for API requests."""


def _make_data_stub(client):
    """Creates gRPC stub to make requests to the Data API.

    :type client: :class:`Client`
    :param client: The client that will hold the stub.

    :rtype: :class:`._generated.bigtable_pb2.BigtableStub`
    :returns: A gRPC stub object.
    """
    return make_stub(client.credentials, client.user_agent,
                     bigtable_pb2.BigtableStub,
                     DATA_API_HOST, DATA_API_PORT)


def _make_instance_stub(client):
    """Creates gRPC stub to make requests to the Instance Admin API.

    :type client: :class:`Client`
    :param client: The client that will hold the stub.

    :rtype: :class:`.bigtable_instance_admin_pb2.BigtableInstanceAdminStub`
    :returns: A gRPC stub object.
    """
    return make_stub(client.credentials, client.user_agent,
                     bigtable_instance_admin_pb2.BigtableInstanceAdminStub,
                     INSTANCE_ADMIN_HOST, INSTANCE_ADMIN_PORT)


def _make_operations_stub(client):
    """Creates gRPC stub to make requests to the Operations API.

    These are for long-running operations of the Instance Admin API,
    hence the host and port matching.

    :type client: :class:`Client`
    :param client: The client that will hold the stub.

    :rtype: :class:`._generated.operations_grpc_pb2.OperationsStub`
    :returns: A gRPC stub object.
    """
    return make_stub(client.credentials, client.user_agent,
                     operations_grpc_pb2.OperationsStub,
                     OPERATIONS_API_HOST, OPERATIONS_API_PORT)


def _make_table_stub(client):
    """Creates gRPC stub to make requests to the Table Admin API.

    :type client: :class:`Client`
    :param client: The client that will hold the stub.

    :rtype: :class:`.bigtable_instance_admin_pb2.BigtableTableAdminStub`
    :returns: A gRPC stub object.
    """
    return make_stub(client.credentials, client.user_agent,
                     bigtable_table_admin_pb2.BigtableTableAdminStub,
                     TABLE_ADMIN_HOST, TABLE_ADMIN_PORT)


class Client(_ClientFactoryMixin, _ClientProjectMixin):
    """Client for interacting with Google Cloud Bigtable API.

    .. note::

        Since the Cloud Bigtable API requires the gRPC transport, no
        ``http`` argument is accepted by this class.

    :type project: :class:`str` or :func:`unicode <unicode>`
    :param project: (Optional) The ID of the project which owns the
                    instances, tables and data. If not provided, will
                    attempt to determine from the environment.

    :type credentials:
        :class:`OAuth2Credentials <oauth2client.client.OAuth2Credentials>` or
        :data:`NoneType <types.NoneType>`
    :param credentials: (Optional) The OAuth2 Credentials to use for this
                        client. If not provided, defaults to the Google
                        Application Default Credentials.

    :type read_only: bool
    :param read_only: (Optional) Boolean indicating if the data scope should be
                      for reading only (or for writing as well). Defaults to
                      :data:`False`.

    :type admin: bool
    :param admin: (Optional) Boolean indicating if the client will be used to
                  interact with the Instance Admin or Table Admin APIs. This
                  requires the :const:`ADMIN_SCOPE`. Defaults to :data:`False`.

    :type user_agent: str
    :param user_agent: (Optional) The user agent to be used with API request.
                       Defaults to :const:`DEFAULT_USER_AGENT`.

    :raises: :class:`ValueError <exceptions.ValueError>` if both ``read_only``
             and ``admin`` are :data:`True`
    """

    _instance_stub_internal = None
    _operations_stub_internal = None
    _table_stub_internal = None

    def __init__(self, project=None, credentials=None,
                 read_only=False, admin=False, user_agent=DEFAULT_USER_AGENT):
        _ClientProjectMixin.__init__(self, project=project)
        if credentials is None:
            credentials = get_credentials()

        if read_only and admin:
            raise ValueError('A read-only client cannot also perform'
                             'administrative actions.')

        scopes = []
        if read_only:
            scopes.append(READ_ONLY_SCOPE)
        else:
            scopes.append(DATA_SCOPE)

        if admin:
            scopes.append(ADMIN_SCOPE)

        self._admin = bool(admin)
        try:
            credentials = credentials.create_scoped(scopes)
        except AttributeError:
            pass
        self._credentials = credentials
        self.user_agent = user_agent

        # Create gRPC stubs for making requests.
        self._data_stub = _make_data_stub(self)
        if self._admin:
            self._instance_stub_internal = _make_instance_stub(self)
            self._operations_stub_internal = _make_operations_stub(self)
            self._table_stub_internal = _make_table_stub(self)

    def copy(self):
        """Make a copy of this client.

        Copies the local data stored as simple types but does not copy the
        current state of any open connections with the Cloud Bigtable API.

        :rtype: :class:`.Client`
        :returns: A copy of the current client.
        """
        credentials = self._credentials
        copied_creds = credentials.create_scoped(credentials.scopes)
        return self.__class__(
            self.project,
            copied_creds,
            READ_ONLY_SCOPE in copied_creds.scopes,
            self._admin,
            self.user_agent,
        )

    @property
    def credentials(self):
        """Getter for client's credentials.

        :rtype:
            :class:`OAuth2Credentials <oauth2client.client.OAuth2Credentials>`
        :returns: The credentials stored on the client.
        """
        return self._credentials

    @property
    def project_name(self):
        """Project name to be used with Instance Admin API.

        .. note::

            This property will not change if ``project`` does not, but the
            return value is not cached.

        The project name is of the form

            ``"projects/{project}"``

        :rtype: str
        :returns: The project name to be used with the Cloud Bigtable Admin
                  API RPC service.
        """
        return 'projects/' + self.project

    @property
    def _instance_stub(self):
        """Getter for the gRPC stub used for the Instance Admin API.

        :rtype: :class:`.bigtable_instance_admin_pb2.BigtableInstanceAdminStub`
        :returns: A gRPC stub object.
        :raises: :class:`ValueError <exceptions.ValueError>` if the current
                 client is not an admin client or if it has not been
                 :meth:`start`-ed.
        """
        if not self._admin:
            raise ValueError('Client is not an admin client.')
        return self._instance_stub_internal

    @property
    def _operations_stub(self):
        """Getter for the gRPC stub used for the Operations API.

        :rtype: :class:`._generated.operations_grpc_pb2.OperationsStub`
        :returns: A gRPC stub object.
        :raises: :class:`ValueError <exceptions.ValueError>` if the current
                 client is not an admin client or if it has not been
                 :meth:`start`-ed.
        """
        if not self._admin:
            raise ValueError('Client is not an admin client.')
        return self._operations_stub_internal

    @property
    def _table_stub(self):
        """Getter for the gRPC stub used for the Table Admin API.

        :rtype: :class:`.bigtable_instance_admin_pb2.BigtableTableAdminStub`
        :returns: A gRPC stub object.
        :raises: :class:`ValueError <exceptions.ValueError>` if the current
                 client is not an admin client or if it has not been
                 :meth:`start`-ed.
        """
        if not self._admin:
            raise ValueError('Client is not an admin client.')
        return self._table_stub_internal

    def instance(self, instance_id, location=_EXISTING_INSTANCE_LOCATION_ID,
                 display_name=None, serve_nodes=DEFAULT_SERVE_NODES):
        """Factory to create a instance associated with this client.

        :type instance_id: str
        :param instance_id: The ID of the instance.

        :type location: string
        :param location: location name, in form
                         ``projects/<project>/locations/<location>``; used to
                         set up the instance's cluster.

        :type display_name: str
        :param display_name: (Optional) The display name for the instance in
                             the Cloud Console UI. (Must be between 4 and 30
                             characters.) If this value is not set in the
                             constructor, will fall back to the instance ID.

        :type serve_nodes: int
        :param serve_nodes: (Optional) The number of nodes in the instance's
                            cluster; used to set up the instance's cluster.

        :rtype: :class:`.Instance`
        :returns: an instance owned by this client.
        """
        return Instance(instance_id, self, location,
                        display_name=display_name, serve_nodes=serve_nodes)

    def list_instances(self):
        """List instances owned by the project.

        :rtype: tuple
        :returns: A pair of results, the first is a list of
                  :class:`.Instance` objects returned and the second is a
                  list of strings (the failed locations in the request).
        """
        request_pb = bigtable_instance_admin_pb2.ListInstancesRequest(
            parent=self.project_name)

        response = self._instance_stub.ListInstances(request_pb)

        instances = [Instance.from_pb(instance_pb, self)
                     for instance_pb in response.instances]
        return instances, response.failed_locations
