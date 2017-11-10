# Copyright 2015 Google LLC
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

"""User-friendly container for Google Cloud Bigtable Instance."""


import re

from google.api_core import operation
from google.cloud.bigtable._generated import (
    instance_pb2 as data_v2_pb2)
from google.cloud.bigtable._generated import (
    bigtable_instance_admin_pb2 as messages_v2_pb2)
from google.cloud.bigtable._generated import (
    bigtable_table_admin_pb2 as table_messages_v2_pb2)
from google.cloud.bigtable.cluster import Cluster
from google.cloud.bigtable.cluster import DEFAULT_SERVE_NODES
from google.cloud.bigtable.table import Table


_EXISTING_INSTANCE_LOCATION_ID = 'see-existing-cluster'
_INSTANCE_NAME_RE = re.compile(r'^projects/(?P<project>[^/]+)/'
                               r'instances/(?P<instance_id>[a-z][-a-z0-9]*)$')


def _prepare_create_request(instance):
    """Creates a protobuf request for a CreateInstance request.

    :type instance: :class:`Instance`
    :param instance: The instance to be created.

    :rtype: :class:`.messages_v2_pb2.CreateInstanceRequest`
    :returns: The CreateInstance request object containing the instance info.
    """
    parent_name = ('projects/' + instance._client.project)
    message = messages_v2_pb2.CreateInstanceRequest(
        parent=parent_name,
        instance_id=instance.instance_id,
        instance=data_v2_pb2.Instance(
            display_name=instance.display_name,
        ),
    )
    cluster = message.clusters[instance.instance_id]
    cluster.name = instance.name + '/clusters/' + instance.instance_id
    cluster.location = (
        parent_name + '/locations/' + instance._cluster_location_id)
    cluster.serve_nodes = instance._cluster_serve_nodes
    return message


class Instance(object):
    """Representation of a Google Cloud Bigtable Instance.

    We can use an :class:`Instance` to:

    * :meth:`reload` itself
    * :meth:`create` itself
    * :meth:`update` itself
    * :meth:`delete` itself

    .. note::

        For now, we leave out the ``default_storage_type`` (an enum)
        which if not sent will end up as :data:`.data_v2_pb2.STORAGE_SSD`.

    :type instance_id: str
    :param instance_id: The ID of the instance.

    :type client: :class:`Client <google.cloud.bigtable.client.Client>`
    :param client: The client that owns the instance. Provides
                   authorization and a project ID.

    :type location_id: str
    :param location_id: ID of the location in which the instance will be
                        created.  Required for instances which do not yet
                        exist.

    :type display_name: str
    :param display_name: (Optional) The display name for the instance in the
                         Cloud Console UI. (Must be between 4 and 30
                         characters.) If this value is not set in the
                         constructor, will fall back to the instance ID.

    :type serve_nodes: int
    :param serve_nodes: (Optional) The number of nodes in the instance's
                        cluster; used to set up the instance's cluster.
    """

    def __init__(self, instance_id, client,
                 location_id=_EXISTING_INSTANCE_LOCATION_ID,
                 display_name=None,
                 serve_nodes=DEFAULT_SERVE_NODES):
        self.instance_id = instance_id
        self.display_name = display_name or instance_id
        self._cluster_location_id = location_id
        self._cluster_serve_nodes = serve_nodes
        self._client = client

    def _update_from_pb(self, instance_pb):
        """Refresh self from the server-provided protobuf.

        Helper for :meth:`from_pb` and :meth:`reload`.
        """
        if not instance_pb.display_name:  # Simple field (string)
            raise ValueError('Instance protobuf does not contain display_name')
        self.display_name = instance_pb.display_name

    @classmethod
    def from_pb(cls, instance_pb, client):
        """Creates an instance instance from a protobuf.

        :type instance_pb: :class:`instance_pb2.Instance`
        :param instance_pb: An instance protobuf object.

        :type client: :class:`Client <google.cloud.bigtable.client.Client>`
        :param client: The client that owns the instance.

        :rtype: :class:`Instance`
        :returns: The instance parsed from the protobuf response.
        :raises: :class:`ValueError <exceptions.ValueError>` if the instance
                 name does not match
                 ``projects/{project}/instances/{instance_id}``
                 or if the parsed project ID does not match the project ID
                 on the client.
        """
        match = _INSTANCE_NAME_RE.match(instance_pb.name)
        if match is None:
            raise ValueError('Instance protobuf name was not in the '
                             'expected format.', instance_pb.name)
        if match.group('project') != client.project:
            raise ValueError('Project ID on instance does not match the '
                             'project ID on the client')
        instance_id = match.group('instance_id')

        result = cls(instance_id, client, _EXISTING_INSTANCE_LOCATION_ID)
        result._update_from_pb(instance_pb)
        return result

    def copy(self):
        """Make a copy of this instance.

        Copies the local data stored as simple types and copies the client
        attached to this instance.

        :rtype: :class:`.Instance`
        :returns: A copy of the current instance.
        """
        new_client = self._client.copy()
        return self.__class__(self.instance_id, new_client,
                              self._cluster_location_id,
                              display_name=self.display_name)

    @property
    def name(self):
        """Instance name used in requests.

        .. note::
          This property will not change if ``instance_id`` does not,
          but the return value is not cached.

        The instance name is of the form

            ``"projects/{project}/instances/{instance_id}"``

        :rtype: str
        :returns: The instance name.
        """
        return self._client.project_name + '/instances/' + self.instance_id

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        # NOTE: This does not compare the configuration values, such as
        #       the display_name. Instead, it only compares
        #       identifying values instance ID and client. This is
        #       intentional, since the same instance can be in different states
        #       if not synchronized. Instances with similar instance
        #       settings but different clients can't be used in the same way.
        return (other.instance_id == self.instance_id and
                other._client == self._client)

    def __ne__(self, other):
        return not self == other

    def reload(self):
        """Reload the metadata for this instance."""
        request_pb = messages_v2_pb2.GetInstanceRequest(name=self.name)
        # We expect `data_v2_pb2.Instance`.
        instance_pb = self._client._instance_stub.GetInstance(request_pb)

        # NOTE: _update_from_pb does not check that the project and
        #       instance ID on the response match the request.
        self._update_from_pb(instance_pb)

    def create(self):
        """Create this instance.

        .. note::

            Uses the ``project`` and ``instance_id`` on the current
            :class:`Instance` in addition to the ``display_name``.
            To change them before creating, reset the values via

            .. code:: python

                instance.display_name = 'New display name'
                instance.instance_id = 'i-changed-my-mind'

            before calling :meth:`create`.

        :rtype: :class:`Operation`
        :returns: The long-running operation corresponding to the
                  create operation.
        """
        request_pb = _prepare_create_request(self)
        # We expect a `google.longrunning.operations_pb2.Operation`.
        operation_pb = self._client._instance_stub.CreateInstance(request_pb)

        operation_future = operation.from_grpc(
            operation_pb,
            self._client._operations_stub,
            data_v2_pb2.Instance,
            metadata_type=messages_v2_pb2.CreateInstanceMetadata)
        return operation_future

    def update(self):
        """Update this instance.

        .. note::

            Updates the ``display_name``. To change that value before
            updating, reset its values via

            .. code:: python

                instance.display_name = 'New display name'

            before calling :meth:`update`.
        """
        request_pb = data_v2_pb2.Instance(
            name=self.name,
            display_name=self.display_name,
        )
        # Ignore the expected `data_v2_pb2.Instance`.
        self._client._instance_stub.UpdateInstance(request_pb)

    def delete(self):
        """Delete this instance.

        Marks an instance and all of its tables for permanent deletion
        in 7 days.

        Immediately upon completion of the request:

        * Billing will cease for all of the instance's reserved resources.
        * The instance's ``delete_time`` field will be set 7 days in
          the future.

        Soon afterward:

        * All tables within the instance will become unavailable.

        At the instance's ``delete_time``:

        * The instance and **all of its tables** will immediately and
          irrevocably disappear from the API, and their data will be
          permanently deleted.
        """
        request_pb = messages_v2_pb2.DeleteInstanceRequest(name=self.name)
        # We expect a `google.protobuf.empty_pb2.Empty`
        self._client._instance_stub.DeleteInstance(request_pb)

    def cluster(self, cluster_id, serve_nodes=3):
        """Factory to create a cluster associated with this client.

        :type cluster_id: str
        :param cluster_id: The ID of the cluster.

        :type serve_nodes: int
        :param serve_nodes: (Optional) The number of nodes in the cluster.
                            Defaults to 3.

        :rtype: :class:`.Cluster`
        :returns: The cluster owned by this client.
        """
        return Cluster(cluster_id, self, serve_nodes=serve_nodes)

    def list_clusters(self):
        """Lists clusters in this instance.

        :rtype: tuple
        :returns: A pair of results, the first is a list of :class:`.Cluster` s
                  returned and the second is a list of strings (the failed
                  locations in the request).
        """
        request_pb = messages_v2_pb2.ListClustersRequest(parent=self.name)
        # We expect a `.cluster_messages_v1_pb2.ListClustersResponse`
        list_clusters_response = self._client._instance_stub.ListClusters(
            request_pb)

        failed_locations = [
            location for location in list_clusters_response.failed_locations]
        clusters = [Cluster.from_pb(cluster_pb, self)
                    for cluster_pb in list_clusters_response.clusters]
        return clusters, failed_locations

    def table(self, table_id):
        """Factory to create a table associated with this instance.

        :type table_id: str
        :param table_id: The ID of the table.

        :rtype: :class:`Table <google.cloud.bigtable.table.Table>`
        :returns: The table owned by this instance.
        """
        return Table(table_id, self)

    def list_tables(self):
        """List the tables in this instance.

        :rtype: list of :class:`Table <google.cloud.bigtable.table.Table>`
        :returns: The list of tables owned by the instance.
        :raises: :class:`ValueError <exceptions.ValueError>` if one of the
                 returned tables has a name that is not of the expected format.
        """
        request_pb = table_messages_v2_pb2.ListTablesRequest(parent=self.name)
        # We expect a `table_messages_v2_pb2.ListTablesResponse`
        table_list_pb = self._client._table_stub.ListTables(request_pb)

        result = []
        for table_pb in table_list_pb.tables:
            table_prefix = self.name + '/tables/'
            if not table_pb.name.startswith(table_prefix):
                raise ValueError('Table name %s not of expected format' % (
                    table_pb.name,))
            table_id = table_pb.name[len(table_prefix):]
            result.append(self.table(table_id))

        return result
