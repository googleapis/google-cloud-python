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

"""User friendly container for Google Cloud Bigtable Cluster."""


import re

from google.api_core import operation
from google.cloud.bigtable._generated import (
    instance_pb2 as data_v2_pb2)
from google.cloud.bigtable._generated import (
    bigtable_instance_admin_pb2 as messages_v2_pb2)

_CLUSTER_NAME_RE = re.compile(r'^projects/(?P<project>[^/]+)/'
                              r'instances/(?P<instance>[^/]+)/clusters/'
                              r'(?P<cluster_id>[a-z][-a-z0-9]*)$')

DEFAULT_SERVE_NODES = 3
"""Default number of nodes to use when creating a cluster."""


def _prepare_create_request(cluster):
    """Creates a protobuf request for a CreateCluster request.

    :type cluster: :class:`Cluster`
    :param cluster: The cluster to be created.

    :rtype: :class:`.messages_v2_pb2.CreateClusterRequest`
    :returns: The CreateCluster request object containing the cluster info.
    """
    return messages_v2_pb2.CreateClusterRequest(
        parent=cluster._instance.name,
        cluster_id=cluster.cluster_id,
        cluster=data_v2_pb2.Cluster(
            location=cluster.location,
            serve_nodes=cluster.serve_nodes,
        ),
    )


class Cluster(object):
    """Representation of a Google Cloud Bigtable Cluster.

    We can use a :class:`Cluster` to:

    * :meth:`reload` itself
    * :meth:`create` itself
    * :meth:`update` itself
    * :meth:`delete` itself

    .. note::

        For now, we leave out the ``default_storage_type`` (an enum)
        which if not sent will end up as :data:`.data_v2_pb2.STORAGE_SSD`.

    :type cluster_id: str
    :param cluster_id: The ID of the cluster.

    :type instance: :class:`~google.cloud.bigtable.instance.Instance`
    :param instance: The instance where the cluster resides.

    :type serve_nodes: int
    :param serve_nodes: (Optional) The number of nodes in the cluster.
                        Defaults to :data:`DEFAULT_SERVE_NODES`.
    """

    def __init__(self, cluster_id, instance,
                 serve_nodes=DEFAULT_SERVE_NODES):
        self.cluster_id = cluster_id
        self._instance = instance
        self.serve_nodes = serve_nodes
        self.location = None

    def _update_from_pb(self, cluster_pb):
        """Refresh self from the server-provided protobuf.

        Helper for :meth:`from_pb` and :meth:`reload`.
        """
        if not cluster_pb.serve_nodes:  # Simple field (int32)
            raise ValueError('Cluster protobuf does not contain serve_nodes')
        self.serve_nodes = cluster_pb.serve_nodes
        self.location = cluster_pb.location

    @classmethod
    def from_pb(cls, cluster_pb, instance):
        """Creates a cluster instance from a protobuf.

        :type cluster_pb: :class:`instance_pb2.Cluster`
        :param cluster_pb: A cluster protobuf object.

        :type instance: :class:`~google.cloud.bigtable.instance.Instance>`
        :param instance: The instance that owns the cluster.

        :rtype: :class:`Cluster`
        :returns: The cluster parsed from the protobuf response.
        :raises:
            :class:`ValueError <exceptions.ValueError>` if the cluster
            name does not match
            ``projects/{project}/instances/{instance}/clusters/{cluster_id}``
            or if the parsed project ID does not match the project ID
            on the client.
        """
        match = _CLUSTER_NAME_RE.match(cluster_pb.name)
        if match is None:
            raise ValueError('Cluster protobuf name was not in the '
                             'expected format.', cluster_pb.name)
        if match.group('project') != instance._client.project:
            raise ValueError('Project ID on cluster does not match the '
                             'project ID on the client')
        if match.group('instance') != instance.instance_id:
            raise ValueError('Instance ID on cluster does not match the '
                             'instance ID on the client')

        result = cls(match.group('cluster_id'), instance)
        result._update_from_pb(cluster_pb)
        return result

    def copy(self):
        """Make a copy of this cluster.

        Copies the local data stored as simple types and copies the client
        attached to this instance.

        :rtype: :class:`.Cluster`
        :returns: A copy of the current cluster.
        """
        new_instance = self._instance.copy()
        return self.__class__(self.cluster_id, new_instance,
                              serve_nodes=self.serve_nodes)

    @property
    def name(self):
        """Cluster name used in requests.

        .. note::
          This property will not change if ``_instance`` and ``cluster_id``
          do not, but the return value is not cached.

        The cluster name is of the form

            ``"projects/{project}/instances/{instance}/clusters/{cluster_id}"``

        :rtype: str
        :returns: The cluster name.
        """
        return self._instance.name + '/clusters/' + self.cluster_id

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        # NOTE: This does not compare the configuration values, such as
        #       the serve_nodes. Instead, it only compares
        #       identifying values instance, cluster ID and client. This is
        #       intentional, since the same cluster can be in different states
        #       if not synchronized. Clusters with similar instance/cluster
        #       settings but different clients can't be used in the same way.
        return (other.cluster_id == self.cluster_id and
                other._instance == self._instance)

    def __ne__(self, other):
        return not self == other

    def reload(self):
        """Reload the metadata for this cluster."""
        request_pb = messages_v2_pb2.GetClusterRequest(name=self.name)
        # We expect a `._generated.instance_pb2.Cluster`.
        cluster_pb = self._instance._client._instance_stub.GetCluster(
            request_pb)

        # NOTE: _update_from_pb does not check that the project, instance and
        #       cluster ID on the response match the request.
        self._update_from_pb(cluster_pb)

    def create(self):
        """Create this cluster.

        .. note::

            Uses the ``project``, ``instance`` and ``cluster_id`` on the
            current :class:`Cluster` in addition to the ``serve_nodes``.
            To change them before creating, reset the values via

            .. code:: python

                cluster.serve_nodes = 8
                cluster.cluster_id = 'i-changed-my-mind'

            before calling :meth:`create`.

        :rtype: :class:`Operation`
        :returns: The long-running operation corresponding to the
                  create operation.
        """
        client = self._instance._client

        # We expect a `google.longrunning.operations_pb2.Operation`.
        request_pb = _prepare_create_request(self)
        operation_pb = client._instance_stub.CreateCluster(request_pb)

        operation_future = operation.from_grpc(
            operation_pb,
            client._operations_stub,
            data_v2_pb2.Cluster,
            metadata_type=messages_v2_pb2.UpdateClusterMetadata)
        return operation_future

    def update(self):
        """Update this cluster.

        .. note::

            Updates the ``serve_nodes``. If you'd like to
            change them before updating, reset the values via

            .. code:: python

                cluster.serve_nodes = 8

            before calling :meth:`update`.

        :rtype: :class:`Operation`
        :returns: The long-running operation corresponding to the
                  update operation.
        """
        client = self._instance._client

        # We expect a `google.longrunning.operations_pb2.Operation`.
        request_pb = data_v2_pb2.Cluster(
            name=self.name,
            serve_nodes=self.serve_nodes,
        )
        operation_pb = client._instance_stub.UpdateCluster(request_pb)

        operation_future = operation.from_grpc(
            operation_pb,
            client._operations_stub,
            data_v2_pb2.Cluster,
            metadata_type=messages_v2_pb2.UpdateClusterMetadata)
        return operation_future

    def delete(self):
        """Delete this cluster.

        Marks a cluster and all of its tables for permanent deletion in 7 days.

        Immediately upon completion of the request:

        * Billing will cease for all of the cluster's reserved resources.
        * The cluster's ``delete_time`` field will be set 7 days in the future.

        Soon afterward:

        * All tables within the cluster will become unavailable.

        At the cluster's ``delete_time``:

        * The cluster and **all of its tables** will immediately and
          irrevocably disappear from the API, and their data will be
          permanently deleted.
        """
        request_pb = messages_v2_pb2.DeleteClusterRequest(name=self.name)
        # We expect a `google.protobuf.empty_pb2.Empty`
        self._instance._client._instance_stub.DeleteCluster(request_pb)
