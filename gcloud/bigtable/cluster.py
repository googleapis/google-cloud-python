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

"""User friendly container for Google Cloud Bigtable Cluster."""


import re

from gcloud.bigtable._generated import (
    bigtable_cluster_service_messages_pb2 as messages_pb2)
from gcloud.bigtable.table import Table


_CLUSTER_NAME_RE = re.compile(r'^projects/(?P<project>[^/]+)/'
                              r'zones/(?P<zone>[^/]+)/clusters/'
                              r'(?P<cluster_id>[a-z][-a-z0-9]*)$')
_DEFAULT_SERVE_NODES = 3


def _get_pb_property_value(message_pb, property_name):
    """Return a message field value.

    :type message_pb: :class:`google.protobuf.message.Message`
    :param message_pb: The message to check for ``property_name``.

    :type property_name: str
    :param property_name: The property value to check against.

    :rtype: object
    :returns: The value of ``property_name`` set on ``message_pb``.
    :raises: :class:`ValueError <exceptions.ValueError>` if the result returned
             from the ``message_pb`` does not contain the ``property_name``
             value.
    """
    # Make sure `property_name` is set on the response.
    # NOTE: As of proto3, HasField() only works for message fields, not for
    #       singular (non-message) fields.
    all_fields = set([field.name for field in message_pb._fields])
    if property_name not in all_fields:
        raise ValueError('Message does not contain %s.' % (property_name,))
    return getattr(message_pb, property_name)


class Cluster(object):
    """Representation of a Google Cloud Bigtable Cluster.

    :type zone: str
    :param zone: The name of the zone where the cluster resides.

    :type cluster_id: str
    :param cluster_id: The ID of the cluster.

    :type client: :class:`.client.Client`
    :param client: The client that owns the cluster. Provides
                   authorization and a project ID.

    :type display_name: str
    :param display_name: (Optional) The display name for the cluster in the
                         Cloud Console UI. (Must be between 4 and 30
                         characters.) If this value is not set in the
                         constructor, will fall back to the cluster ID.

    :type serve_nodes: int
    :param serve_nodes: (Optional) The number of nodes in the cluster.
                        Defaults to 3.
    """

    def __init__(self, zone, cluster_id, client,
                 display_name=None, serve_nodes=_DEFAULT_SERVE_NODES):
        self.zone = zone
        self.cluster_id = cluster_id
        self.display_name = display_name or cluster_id
        self.serve_nodes = serve_nodes
        self._client = client

    def table(self, table_id):
        """Factory to create a table associated with this cluster.

        :type table_id: str
        :param table_id: The ID of the table.

        :rtype: :class:`Table <gcloud.bigtable.table.Table>`
        :returns: The table owned by this cluster.
        """
        return Table(table_id, self)

    def _update_from_pb(self, cluster_pb):
        self.display_name = _get_pb_property_value(cluster_pb, 'display_name')
        self.serve_nodes = _get_pb_property_value(cluster_pb, 'serve_nodes')

    @classmethod
    def from_pb(cls, cluster_pb, client):
        """Creates a cluster instance from a protobuf.

        :type cluster_pb: :class:`bigtable_cluster_data_pb2.Cluster`
        :param cluster_pb: A cluster protobuf object.

        :type client: :class:`.client.Client`
        :param client: The client that owns the cluster.

        :rtype: :class:`Cluster`
        :returns: The cluster parsed from the protobuf response.
        :raises: :class:`ValueError <exceptions.ValueError>` if the cluster
                 name does not match :data:`_CLUSTER_NAME_RE` or if the parsed
                 project ID does not match the project ID on the client.
        """
        match = _CLUSTER_NAME_RE.match(cluster_pb.name)
        if match is None:
            raise ValueError('Cluster protobuf name was not in the '
                             'expected format.', cluster_pb.name)
        if match.group('project') != client.project:
            raise ValueError('Project ID on cluster does not match the '
                             'project ID on the client')

        result = cls(match.group('zone'), match.group('cluster_id'), client)
        result._update_from_pb(cluster_pb)
        return result

    @property
    def name(self):
        """Cluster name used in requests.

        .. note::
          This property will not change if ``zone`` and ``cluster_id`` do not,
          but the return value is not cached.

        The cluster name is of the form

            ``"projects/{project}/zones/{zone}/clusters/{cluster_id}"``

        :rtype: str
        :returns: The cluster name.
        """
        return (self._client.project_name + '/zones/' + self.zone +
                '/clusters/' + self.cluster_id)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        # NOTE: This does not compare the configuration values, such as
        #       the serve_nodes or display_name. Instead, it only compares
        #       identifying values zone, cluster ID and client. This is
        #       intentional, since the same cluster can be in different states
        #       if not synchronized. Clusters with similar zone/cluster
        #       settings but different clients can't be used in the same way.
        return (other.zone == self.zone and
                other.cluster_id == self.cluster_id and
                other._client == self._client)

    def __ne__(self, other):
        return not self.__eq__(other)

    def reload(self):
        """Reload the metadata for this cluster."""
        request_pb = messages_pb2.GetClusterRequest(name=self.name)
        # We expect a `._generated.bigtable_cluster_data_pb2.Cluster`.
        cluster_pb = self._client._cluster_stub.GetCluster(
            request_pb, self._client.timeout_seconds)

        # NOTE: _update_from_pb does not check that the project, zone and
        #       cluster ID on the response match the request.
        self._update_from_pb(cluster_pb)
