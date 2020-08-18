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
from google.cloud.bigtable_admin_v2.types import instance_pb2
from google.api_core.exceptions import NotFound


_CLUSTER_NAME_RE = re.compile(
    r"^projects/(?P<project>[^/]+)/"
    r"instances/(?P<instance>[^/]+)/clusters/"
    r"(?P<cluster_id>[a-z][-a-z0-9]*)$"
)


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
    :param location_id: (Creation Only) The location where this cluster's
                        nodes and storage reside . For best performance,
                        clients should be located as close as possible to
                        this cluster.
                        For list of supported locations refer to
                        https://cloud.google.com/bigtable/docs/locations

    :type serve_nodes: int
    :param serve_nodes: (Optional) The number of nodes in the cluster.

    :type default_storage_type: int
    :param default_storage_type: (Optional) The type of storage
                                 Possible values are represented by the
                                 following constants:
                                 :data:`google.cloud.bigtable.enums.StorageType.SSD`.
                                 :data:`google.cloud.bigtable.enums.StorageType.HDD`,
                                 Defaults to
                                 :data:`google.cloud.bigtable.enums.StorageType.UNSPECIFIED`.

    :type _state: int
    :param _state: (`OutputOnly`)
                   The current state of the cluster.
                   Possible values are represented by the following constants:
                   :data:`google.cloud.bigtable.enums.Cluster.State.NOT_KNOWN`.
                   :data:`google.cloud.bigtable.enums.Cluster.State.READY`.
                   :data:`google.cloud.bigtable.enums.Cluster.State.CREATING`.
                   :data:`google.cloud.bigtable.enums.Cluster.State.RESIZING`.
                   :data:`google.cloud.bigtable.enums.Cluster.State.DISABLED`.
    """

    def __init__(
        self,
        cluster_id,
        instance,
        location_id=None,
        serve_nodes=None,
        default_storage_type=None,
        _state=None,
    ):
        self.cluster_id = cluster_id
        self._instance = instance
        self.location_id = location_id
        self.serve_nodes = serve_nodes
        self.default_storage_type = default_storage_type
        self._state = _state

    @classmethod
    def from_pb(cls, cluster_pb, instance):
        """Creates an cluster instance from a protobuf.

        For example:

        .. literalinclude:: snippets.py
            :start-after: [START bigtable_cluster_from_pb]
            :end-before: [END bigtable_cluster_from_pb]
            :dedent: 4

        :type cluster_pb: :class:`instance_pb2.Cluster`
        :param cluster_pb: An instance protobuf object.

        :type instance: :class:`google.cloud.bigtable.instance.Instance`
        :param instance: The instance that owns the cluster.

        :rtype: :class:`Cluster`
        :returns: The Cluster parsed from the protobuf response.
        :raises: :class:`ValueError <exceptions.ValueError>` if the cluster
                 name does not match
                 ``projects/{project}/instances/{instance_id}/clusters/{cluster_id}``
                 or if the parsed instance ID does not match the istance ID
                 on the client.
                 or if the parsed project ID does not match the project ID
                 on the client.
        """
        match_cluster_name = _CLUSTER_NAME_RE.match(cluster_pb.name)
        if match_cluster_name is None:
            raise ValueError(
                "Cluster protobuf name was not in the " "expected format.",
                cluster_pb.name,
            )
        if match_cluster_name.group("instance") != instance.instance_id:
            raise ValueError(
                "Instance ID on cluster does not match the " "instance ID on the client"
            )
        if match_cluster_name.group("project") != instance._client.project:
            raise ValueError(
                "Project ID on cluster does not match the " "project ID on the client"
            )
        cluster_id = match_cluster_name.group("cluster_id")

        result = cls(cluster_id, instance)
        result._update_from_pb(cluster_pb)
        return result

    def _update_from_pb(self, cluster_pb):
        """Refresh self from the server-provided protobuf.
        Helper for :meth:`from_pb` and :meth:`reload`.
        """

        self.location_id = cluster_pb.location.split("/")[-1]
        self.serve_nodes = cluster_pb.serve_nodes
        self.default_storage_type = cluster_pb.default_storage_type
        self._state = cluster_pb.state

    @property
    def name(self):
        """Cluster name used in requests.

        .. note::
          This property will not change if ``_instance`` and ``cluster_id``
          do not, but the return value is not cached.

        For example:

        .. literalinclude:: snippets.py
            :start-after: [START bigtable_cluster_name]
            :end-before: [END bigtable_cluster_name]
            :dedent: 4

        The cluster name is of the form

            ``"projects/{project}/instances/{instance}/clusters/{cluster_id}"``

        :rtype: str
        :returns: The cluster name.
        """
        return self._instance._client.instance_admin_client.cluster_path(
            self._instance._client.project, self._instance.instance_id, self.cluster_id
        )

    @property
    def state(self):
        """google.cloud.bigtable.enums.Cluster.State: state of cluster.

        For example:

        .. literalinclude:: snippets.py
            :start-after: [START bigtable_cluster_state]
            :end-before: [END bigtable_cluster_state]
            :dedent: 4

        """
        return self._state

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        # NOTE: This does not compare the configuration values, such as
        #       the serve_nodes. Instead, it only compares
        #       identifying values instance, cluster ID and client. This is
        #       intentional, since the same cluster can be in different states
        #       if not synchronized. Clusters with similar instance/cluster
        #       settings but different clients can't be used in the same way.
        return other.cluster_id == self.cluster_id and other._instance == self._instance

    def __ne__(self, other):
        return not self == other

    def reload(self):
        """Reload the metadata for this cluster.

        For example:

        .. literalinclude:: snippets.py
            :start-after: [START bigtable_reload_cluster]
            :end-before: [END bigtable_reload_cluster]
            :dedent: 4
        """
        cluster_pb = self._instance._client.instance_admin_client.get_cluster(self.name)

        # NOTE: _update_from_pb does not check that the project and
        #       cluster ID on the response match the request.
        self._update_from_pb(cluster_pb)

    def exists(self):
        """Check whether the cluster already exists.

        For example:

        .. literalinclude:: snippets.py
            :start-after: [START bigtable_check_cluster_exists]
            :end-before: [END bigtable_check_cluster_exists]
            :dedent: 4

        :rtype: bool
        :returns: True if the table exists, else False.
        """
        client = self._instance._client
        try:
            client.instance_admin_client.get_cluster(name=self.name)
            return True
        # NOTE: There could be other exceptions that are returned to the user.
        except NotFound:
            return False

    def create(self):
        """Create this cluster.

        For example:

        .. literalinclude:: snippets.py
            :start-after: [START bigtable_create_cluster]
            :end-before: [END bigtable_create_cluster]
            :dedent: 4

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
        cluster_pb = self._to_pb()

        return client.instance_admin_client.create_cluster(
            self._instance.name, self.cluster_id, cluster_pb
        )

    def update(self):
        """Update this cluster.

        For example:

        .. literalinclude:: snippets.py
            :start-after: [START bigtable_update_cluster]
            :end-before: [END bigtable_update_cluster]
            :dedent: 4

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
        # We are passing `None` for third argument location.
        # Location is set only at the time of creation of a cluster
        # and can not be changed after cluster has been created.
        return client.instance_admin_client.update_cluster(
            name=self.name, serve_nodes=self.serve_nodes, location=None
        )

    def delete(self):
        """Delete this cluster.

        For example:

        .. literalinclude:: snippets.py
            :start-after: [START bigtable_delete_cluster]
            :end-before: [END bigtable_delete_cluster]
            :dedent: 4

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

    def _to_pb(self):
        """ Create cluster proto buff message for API calls """
        client = self._instance._client
        location = client.instance_admin_client.location_path(
            client.project, self.location_id
        )
        cluster_pb = instance_pb2.Cluster(
            location=location,
            serve_nodes=self.serve_nodes,
            default_storage_type=self.default_storage_type,
        )
        return cluster_pb
