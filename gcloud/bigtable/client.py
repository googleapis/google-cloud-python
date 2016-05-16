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

* a :class:`Client` owns a :class:`.Cluster`
* a :class:`.Cluster` owns a :class:`Table <gcloud.bigtable.table.Table>`
* a :class:`Table <gcloud.bigtable.table.Table>` owns a
  :class:`ColumnFamily <.column_family.ColumnFamily>`
* a :class:`Table <gcloud.bigtable.table.Table>` owns a :class:`Row <.row.Row>`
  (and all the cells in the row)
"""


from pkg_resources import get_distribution

from grpc.beta import implementations

from gcloud.bigtable._generated import bigtable_cluster_data_pb2 as data_pb2
from gcloud.bigtable._generated import bigtable_cluster_service_pb2
from gcloud.bigtable._generated import (
    bigtable_cluster_service_messages_pb2 as messages_pb2)
from gcloud.bigtable._generated import bigtable_service_pb2
from gcloud.bigtable._generated import bigtable_table_service_pb2
from gcloud.bigtable._generated import operations_grpc_pb2
from gcloud.bigtable.cluster import Cluster
from gcloud.client import _ClientFactoryMixin
from gcloud.client import _ClientProjectMixin
from gcloud.credentials import get_credentials


TABLE_STUB_FACTORY = (
    bigtable_table_service_pb2.beta_create_BigtableTableService_stub)
TABLE_ADMIN_HOST = 'bigtabletableadmin.googleapis.com'
"""Table Admin API request host."""
TABLE_ADMIN_PORT = 443
"""Table Admin API request port."""

CLUSTER_STUB_FACTORY = (
    bigtable_cluster_service_pb2.beta_create_BigtableClusterService_stub)
CLUSTER_ADMIN_HOST = 'bigtableclusteradmin.googleapis.com'
"""Cluster Admin API request host."""
CLUSTER_ADMIN_PORT = 443
"""Cluster Admin API request port."""

DATA_STUB_FACTORY = bigtable_service_pb2.beta_create_BigtableService_stub
DATA_API_HOST = 'bigtable.googleapis.com'
"""Data API request host."""
DATA_API_PORT = 443
"""Data API request port."""

OPERATIONS_STUB_FACTORY = operations_grpc_pb2.beta_create_Operations_stub

ADMIN_SCOPE = 'https://www.googleapis.com/auth/bigtable.admin'
"""Scope for interacting with the Cluster Admin and Table Admin APIs."""
DATA_SCOPE = 'https://www.googleapis.com/auth/bigtable.data'
"""Scope for reading and writing table data."""
READ_ONLY_SCOPE = 'https://www.googleapis.com/auth/bigtable.data.readonly'
"""Scope for reading table data."""

DEFAULT_TIMEOUT_SECONDS = 10
"""The default timeout to use for API requests."""

DEFAULT_USER_AGENT = 'gcloud-python/{0}'.format(
    get_distribution('gcloud').version)
"""The default user agent for API requests."""


class Client(_ClientFactoryMixin, _ClientProjectMixin):
    """Client for interacting with Google Cloud Bigtable API.

    .. note::

        Since the Cloud Bigtable API requires the gRPC transport, no
        ``http`` argument is accepted by this class.

    :type project: :class:`str` or :func:`unicode <unicode>`
    :param project: (Optional) The ID of the project which owns the
                    clusters, tables and data. If not provided, will
                    attempt to determine from the environment.

    :type credentials:
        :class:`OAuth2Credentials <oauth2client.client.OAuth2Credentials>` or
        :data:`NoneType <types.NoneType>`
    :param credentials: (Optional) The OAuth2 Credentials to use for this
                        cluster. If not provided, defaults to the Google
                        Application Default Credentials.

    :type read_only: bool
    :param read_only: (Optional) Boolean indicating if the data scope should be
                      for reading only (or for writing as well). Defaults to
                      :data:`False`.

    :type admin: bool
    :param admin: (Optional) Boolean indicating if the client will be used to
                  interact with the Cluster Admin or Table Admin APIs. This
                  requires the :const:`ADMIN_SCOPE`. Defaults to :data:`False`.

    :type user_agent: str
    :param user_agent: (Optional) The user agent to be used with API request.
                       Defaults to :const:`DEFAULT_USER_AGENT`.

    :type timeout_seconds: int
    :param timeout_seconds: Number of seconds for request time-out. If not
                            passed, defaults to
                            :const:`DEFAULT_TIMEOUT_SECONDS`.

    :raises: :class:`ValueError <exceptions.ValueError>` if both ``read_only``
             and ``admin`` are :data:`True`
    """

    def __init__(self, project=None, credentials=None,
                 read_only=False, admin=False, user_agent=DEFAULT_USER_AGENT,
                 timeout_seconds=DEFAULT_TIMEOUT_SECONDS):
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
        self.timeout_seconds = timeout_seconds

        # These will be set in start().
        self._data_stub_internal = None
        self._cluster_stub_internal = None
        self._operations_stub_internal = None
        self._table_stub_internal = None

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
            self.timeout_seconds,
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
        """Project name to be used with Cluster Admin API.

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
    def _data_stub(self):
        """Getter for the gRPC stub used for the Data API.

        :rtype: :class:`grpc.beta._stub._AutoIntermediary`
        :returns: A gRPC stub object.
        :raises: :class:`ValueError <exceptions.ValueError>` if the current
                 client has not been :meth:`start`-ed.
        """
        if self._data_stub_internal is None:
            raise ValueError('Client has not been started.')
        return self._data_stub_internal

    @property
    def _cluster_stub(self):
        """Getter for the gRPC stub used for the Cluster Admin API.

        :rtype: :class:`grpc.beta._stub._AutoIntermediary`
        :returns: A gRPC stub object.
        :raises: :class:`ValueError <exceptions.ValueError>` if the current
                 client is not an admin client or if it has not been
                 :meth:`start`-ed.
        """
        if not self._admin:
            raise ValueError('Client is not an admin client.')
        if self._cluster_stub_internal is None:
            raise ValueError('Client has not been started.')
        return self._cluster_stub_internal

    @property
    def _operations_stub(self):
        """Getter for the gRPC stub used for the Operations API.

        :rtype: :class:`grpc.beta._stub._AutoIntermediary`
        :returns: A gRPC stub object.
        :raises: :class:`ValueError <exceptions.ValueError>` if the current
                 client is not an admin client or if it has not been
                 :meth:`start`-ed.
        """
        if not self._admin:
            raise ValueError('Client is not an admin client.')
        if self._operations_stub_internal is None:
            raise ValueError('Client has not been started.')
        return self._operations_stub_internal

    @property
    def _table_stub(self):
        """Getter for the gRPC stub used for the Table Admin API.

        :rtype: :class:`grpc.beta._stub._AutoIntermediary`
        :returns: A gRPC stub object.
        :raises: :class:`ValueError <exceptions.ValueError>` if the current
                 client is not an admin client or if it has not been
                 :meth:`start`-ed.
        """
        if not self._admin:
            raise ValueError('Client is not an admin client.')
        if self._table_stub_internal is None:
            raise ValueError('Client has not been started.')
        return self._table_stub_internal

    def _make_data_stub(self):
        """Creates gRPC stub to make requests to the Data API.

        :rtype: :class:`grpc.beta._stub._AutoIntermediary`
        :returns: A gRPC stub object.
        """
        return _make_stub(self, DATA_STUB_FACTORY,
                          DATA_API_HOST, DATA_API_PORT)

    def _make_cluster_stub(self):
        """Creates gRPC stub to make requests to the Cluster Admin API.

        :rtype: :class:`grpc.beta._stub._AutoIntermediary`
        :returns: A gRPC stub object.
        """
        return _make_stub(self, CLUSTER_STUB_FACTORY,
                          CLUSTER_ADMIN_HOST, CLUSTER_ADMIN_PORT)

    def _make_operations_stub(self):
        """Creates gRPC stub to make requests to the Operations API.

        These are for long-running operations of the Cluster Admin API,
        hence the host and port matching.

        :rtype: :class:`grpc.beta._stub._AutoIntermediary`
        :returns: A gRPC stub object.
        """
        return _make_stub(self, OPERATIONS_STUB_FACTORY,
                          CLUSTER_ADMIN_HOST, CLUSTER_ADMIN_PORT)

    def _make_table_stub(self):
        """Creates gRPC stub to make requests to the Table Admin API.

        :rtype: :class:`grpc.beta._stub._AutoIntermediary`
        :returns: A gRPC stub object.
        """
        return _make_stub(self, TABLE_STUB_FACTORY,
                          TABLE_ADMIN_HOST, TABLE_ADMIN_PORT)

    def is_started(self):
        """Check if the client has been started.

        :rtype: bool
        :returns: Boolean indicating if the client has been started.
        """
        return self._data_stub_internal is not None

    def start(self):
        """Prepare the client to make requests.

        Activates gRPC contexts for making requests to the Bigtable
        Service(s).
        """
        if self.is_started():
            return

        # NOTE: We __enter__ the stubs more-or-less permanently. This is
        #       because only after entering the context managers is the
        #       connection created. We don't want to immediately close
        #       those connections since the client will make many
        #       requests with it over HTTP/2.
        self._data_stub_internal = self._make_data_stub()
        self._data_stub_internal.__enter__()
        if self._admin:
            self._cluster_stub_internal = self._make_cluster_stub()
            self._operations_stub_internal = self._make_operations_stub()
            self._table_stub_internal = self._make_table_stub()

            self._cluster_stub_internal.__enter__()
            self._operations_stub_internal.__enter__()
            self._table_stub_internal.__enter__()

    def __enter__(self):
        """Starts the client as a context manager."""
        self.start()

    def stop(self):
        """Closes all the open gRPC clients."""
        if not self.is_started():
            return

        # When exit-ing, we pass None as the exception type, value and
        # traceback to __exit__.
        self._data_stub_internal.__exit__(None, None, None)
        if self._admin:
            self._cluster_stub_internal.__exit__(None, None, None)
            self._operations_stub_internal.__exit__(None, None, None)
            self._table_stub_internal.__exit__(None, None, None)

        self._data_stub_internal = None
        self._cluster_stub_internal = None
        self._operations_stub_internal = None
        self._table_stub_internal = None

    def __exit__(self, exc_type, exc_val, exc_t):
        """Stops the client as a context manager."""
        self.stop()

    def cluster(self, zone, cluster_id, display_name=None, serve_nodes=3):
        """Factory to create a cluster associated with this client.

        :type zone: str
        :param zone: The name of the zone where the cluster resides.

        :type cluster_id: str
        :param cluster_id: The ID of the cluster.

        :type display_name: str
        :param display_name: (Optional) The display name for the cluster in the
                             Cloud Console UI. (Must be between 4 and 30
                             characters.) If this value is not set in the
                             constructor, will fall back to the cluster ID.

        :type serve_nodes: int
        :param serve_nodes: (Optional) The number of nodes in the cluster.
                            Defaults to 3.

        :rtype: :class:`.Cluster`
        :returns: The cluster owned by this client.
        """
        return Cluster(zone, cluster_id, self,
                       display_name=display_name, serve_nodes=serve_nodes)

    def list_zones(self):
        """Lists zones associated with project.

        :rtype: list
        :returns: The names (as :class:`str`) of the zones
        :raises: :class:`ValueError <exceptions.ValueError>` if one of the
                 zones is not in ``OK`` state.
        """
        request_pb = messages_pb2.ListZonesRequest(name=self.project_name)
        # We expect a `.messages_pb2.ListZonesResponse`
        list_zones_response = self._cluster_stub.ListZones(
            request_pb, self.timeout_seconds)

        result = []
        for zone in list_zones_response.zones:
            if zone.status != data_pb2.Zone.OK:
                raise ValueError('Zone %s not in OK state' % (
                    zone.display_name,))
            result.append(zone.display_name)
        return result

    def list_clusters(self):
        """Lists clusters owned by the project.

        :rtype: tuple
        :returns: A pair of results, the first is a list of :class:`.Cluster` s
                  returned and the second is a list of strings (the failed
                  zones in the request).
        """
        request_pb = messages_pb2.ListClustersRequest(name=self.project_name)
        # We expect a `.messages_pb2.ListClustersResponse`
        list_clusters_response = self._cluster_stub.ListClusters(
            request_pb, self.timeout_seconds)

        failed_zones = [zone.display_name
                        for zone in list_clusters_response.failed_zones]
        clusters = [Cluster.from_pb(cluster_pb, self)
                    for cluster_pb in list_clusters_response.clusters]
        return clusters, failed_zones


class _MetadataPlugin(object):
    """Callable class to transform metadata for gRPC requests.

    :type client: :class:`.client.Client`
    :param client: The client that owns the cluster. Provides authorization and
                   user agent.
    """

    def __init__(self, client):
        self._credentials = client.credentials
        self._user_agent = client.user_agent

    def __call__(self, unused_context, callback):
        """Adds authorization header to request metadata."""
        access_token = self._credentials.get_access_token().access_token
        headers = [
            ('Authorization', 'Bearer ' + access_token),
            ('User-agent', self._user_agent),
        ]
        callback(headers, None)


def _make_stub(client, stub_factory, host, port):
    """Makes a stub for an RPC service.

    Uses / depends on the beta implementation of gRPC.

    :type client: :class:`.client.Client`
    :param client: The client that owns the cluster. Provides authorization and
                   user agent.

    :type stub_factory: callable
    :param stub_factory: A factory which will create a gRPC stub for
                         a given service.

    :type host: str
    :param host: The host for the service.

    :type port: int
    :param port: The port for the service.

    :rtype: :class:`grpc.beta._stub._AutoIntermediary`
    :returns: The stub object used to make gRPC requests to a given API.
    """
    # Leaving the first argument to ssl_channel_credentials() as None
    # loads root certificates from `grpc/_adapter/credentials/roots.pem`.
    transport_creds = implementations.ssl_channel_credentials(None, None, None)
    custom_metadata_plugin = _MetadataPlugin(client)
    auth_creds = implementations.metadata_call_credentials(
        custom_metadata_plugin, name='google_creds')
    channel_creds = implementations.composite_channel_credentials(
        transport_creds, auth_creds)
    channel = implementations.secure_channel(host, port, channel_creds)
    return stub_factory(channel)
