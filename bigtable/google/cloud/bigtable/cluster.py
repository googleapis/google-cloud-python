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

from google.cloud.bigtable_admin_v2 import enums
from google.cloud.bigtable_admin_v2.types import instance_pb2

_CLUSTER_NAME_RE = re.compile(r'^projects/(?P<project>[^/]+)/'
                              r'instances/(?P<instance>[^/]+)/clusters/'
                              r'(?P<cluster_id>[a-z][-a-z0-9]*)$')

DEFAULT_SERVE_NODES = 3
"""Default number of nodes to use when creating a cluster."""

_STORAGE_TYPE_UNSPECIFIED = enums.StorageType.STORAGE_TYPE_UNSPECIFIED


class Cluster(object):
    """Representation of a Google Cloud Bigtable Cluster.

    We can use a :class:`Cluster` to:

    * :meth:`reload` itself
    * :meth:`create` itself
    * :meth:`update` itself
    * :meth:`delete` itself

    :type cluster_id: str
    :param cluster_id: The ID of the cluster.

    :type instance: :class:`~google.cloud.bigtable.instance.Instance`
    :param instance: The instance where the cluster resides.

    :type serve_nodes: int
    :param serve_nodes: (Optional) The number of nodes in the cluster.
                        Defaults to :data:`DEFAULT_SERVE_NODES`.

    :type location_id: str
    :param location_id: (Optional) The location where this cluster's nodes and
                          storage reside. For best performance, clients should
                          be located as close as possible to this cluster.
                          Currently only zones are supported, so values
                          should be of the form
                          ``projects/<project>/locations/<zone>``.

    :type default_storage_type: int
    :param default_storage_type: (Optional) The type of storage used by this
                                    cluster.
    """

    def __init__(self, cluster_id, instance,
                 serve_nodes=DEFAULT_SERVE_NODES,
                 location_id=None,
                 default_storage_type=_STORAGE_TYPE_UNSPECIFIED
                 ):
        self.cluster_id = cluster_id
        self._instance = instance
        self.serve_nodes = serve_nodes
        self.location = location_id
        self.default_storage_type = default_storage_type

    def _update_from_pb(self, cluster_pb):
        """Refresh self from the server-provided protobuf.
        Helper for :meth:`from_pb` and :meth:`reload`.
        """
        if not cluster_pb.serve_nodes:  # Simple field (int32)
            raise ValueError('Cluster protobuf does not contain serve_nodes')
        self.serve_nodes = cluster_pb.serve_nodes
        self.location = cluster_pb.location
        self.default_storage_type = cluster_pb.default_storage_type

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

        cluster = cls(match.group('cluster_id'), instance)
        cluster._update_from_pb(cluster_pb)
        return cluster

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
        return self._instance._client.instance_admin_client.cluster_path(
            self._instance._client.project, self._instance.instance_id,
            self.cluster_id)

    @property
    def to_pb(self):
        """Generate pb message to GAPIC api calls"""
        return instance_pb2.Cluster(
            name=self.name, location=self.location,
            serve_nodes=self.serve_nodes,
            default_storage_type=self.default_storage_type)

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
        cluster_pb = self._instance._client.instance_admin_client.get_cluster(
            self.name)

        self._update_from_pb(cluster_pb)

    @staticmethod
    def cluster_name(instance, cluster_id):
        """Get the cluster path name in string

        :type instance: :class:`~google.cloud.bigtable.instance.Instance>`
        :param instance: The instance that owns the cluster.

        :type cluster_id: str
        :param cluster_id: The ID of the cluster.

        :rtype: str
        :returns: Return a fully-qualified cluster string.
        """
        return instance._client.instance_admin_client.cluster_path(
            instance._client.project, instance.instance_id, cluster_id)

    @staticmethod
    def get_cluster(instance, cluster_id):
        """Get the cluster in form of protobuf

        :type instance: :class:`~google.cloud.bigtable.instance.Instance>`
        :param instance: The instance that owns the cluster.

        :type cluster_id: str
        :param cluster_id: The ID of the cluster.

        :rtype: :class:`~google.cloud.bigtable.cluster.Cluster`
        :returns: Return the instance of
                    :class:`~google.cloud.bigtable.cluster.Cluster`.
        """

        cluster = Cluster(cluster_id=cluster_id, instance=instance)
        cluster_name = Cluster.cluster_name(instance, cluster_id)
        cluster_pb = instance._client.instance_admin_client.get_cluster(
            cluster_name)

        cluster.serve_nodes = cluster_pb.serve_nodes
        cluster.default_storage_type = cluster_pb.default_storage_type
        cluster.location = cluster_pb.location

        return cluster

    def create_cluster(self):
        """Create this cluster.

        .. note::

            Uses the ``project``, ``instance`` and ``cluster_id`` on the
            current :class:`Cluster` in addition to the ``serve_nodes``.
            To change them before creating, reset the values via

            .. code:: python

                cluster.serve_nodes = 8
                cluster.cluster_id = 'i-changed-my-mind'

            before calling :meth:`create`.

        :rtype: :class:`~google.api_core.operation.Operation`
        :returns: The long-running operation corresponding to the
                  create operation.
        """
        client = self._instance._client
        cluster = instance_pb2.Cluster(
            location=self.location,
            serve_nodes=self.serve_nodes,
            default_storage_type=self.default_storage_type)

        return client.instance_admin_client.create_cluster(
            self._instance.name, self.cluster_id, cluster)

    def update_cluster(self, location='', serve_nodes=0):
        """Update this cluster.

        .. note::

            Updates the ``serve_nodes``. If you'd like to
            change them before updating, reset the values via

            .. code:: python

                cluster.serve_nodes = 8

            before calling :meth:`update`.

        :type location: :str:``CreationOnly``
        :param location: The location where this cluster's nodes and storage
                reside. For best performance, clients should be located as
                close as possible to this cluster. Currently only zones are
                supported, so values should be of the form
                ``projects/<project>/locations/<zone>``.

        :type serve_nodes: :int
        :param serve_nodes: The number of nodes allocated to this cluster.
                More nodes enable higher throughput and more consistent
                performance.

        :rtype: :class:`Operation`
        :returns: The long-running operation corresponding to the
                  update operation.
        """
        client = self._instance._client
        return client.instance_admin_client.update_cluster(
            self.name, location, serve_nodes)

    def delete_cluster(self):
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
        client = self._instance._client
        client.instance_admin_client.delete_cluster(self.name)
