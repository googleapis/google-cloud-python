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

    :type location_id: str
    :param location_id: ID of the location in which the cluster will be
                        created. For e.g "us-central1-b"
                        List of locations id is :
                        https://cloud.google.com/bigtable/docs/locations
                        For best performance, clients should be located
                        as close as possible to this cluster.

    :type serve_nodes: int
    :param serve_nodes: (Optional) The number of nodes in the cluster.
                        Defaults to :data:`DEFAULT_SERVE_NODES`.

    :type default_storage_type: int
    :param default_storage_type: (Optional) The default values are
                                  STORAGE_TYPE_UNSPECIFIED = 0: The user
                                  did not specify a storage type.
                                  SSD = 1: Flash (SSD) storage should be used.
                                  HDD = 2: Magnetic drive (HDD) storage
                                  should be used.
    """

    def __init__(self, cluster_id, instance, location_id,
                 serve_nodes=DEFAULT_SERVE_NODES,
                 storage_type=_STORAGE_TYPE_UNSPECIFIED):
        self.cluster_id = cluster_id
        self._instance = instance
        self.location = location_id
        self.serve_nodes = serve_nodes
        self.storage_type = storage_type

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
        self._instance._client.instance_admin_client.get_cluster(self.name)

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

        :rtype: :class:`~google.api_core.operation.Operation`
        :returns: The long-running operation corresponding to the
                  create operation.
        """
        client = self._instance._client
        return client.instance_admin_client.create_cluster(
            self._instance.name, self.cluster_id, {})

    def update(self, location='', serve_nodes=0):
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
        client = self._instance._client
        client.instance_admin_client.delete_cluster(self.name)

    def create_pb_request(self):
        """ Create cluster proto buff message for API calls """
        client = self._instance._client
        cluster_name = client.instance_admin_client.cluster_path(
            client.project, self._instance.instance_id, self.cluster_id)
        location = client.instance_admin_client.location_path(
            client.project, self.location)
        cluster_message = instance_pb2.Cluster(
            name=cluster_name, location=location,
            serve_nodes=self.serve_nodes,
            default_storage_type=self.storage_type)
        return cluster_message
