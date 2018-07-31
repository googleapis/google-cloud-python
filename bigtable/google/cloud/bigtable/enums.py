# Copyright 2018 Google LLC
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
"""Wrappers for gapic enum types."""

from google.cloud.bigtable_admin_v2 import enums


class StorageType(object):
    """
    Storage media types for persisting Bigtable data.

    Attributes:
      UNSPECIFIED (int): The user did not specify a storage type.
      SSD (int): Flash (SSD) storage should be used.
      HDD (int): Magnetic drive (HDD) storage should be used.
    """
    UNSPECIFIED = enums.StorageType.STORAGE_TYPE_UNSPECIFIED
    SSD = enums.StorageType.SSD
    HDD = enums.StorageType.HDD


class Instance(object):
    class State(object):
        """
        Possible states of an instance.

        Attributes:
          STATE_NOT_KNOWN (int): The state of the instance could not be
          determined.
          READY (int): The instance has been successfully created and can
          serve requests to its tables.
          CREATING (int): The instance is currently being created, and may be
          destroyed if the creation process encounters an error.
        """
        NOT_KNOWN = enums.Instance.State.STATE_NOT_KNOWN
        READY = enums.Instance.State.READY
        CREATING = enums.Instance.State.CREATING

    class Type(object):
        """
        The type of the instance.

        Attributes:
          UNSPECIFIED (int): The type of the instance is unspecified.
          If set when creating an instance, a ``PRODUCTION`` instance will
          be created. If set when updating an instance, the type will be
          left unchanged.
          PRODUCTION (int): An instance meant for production use.
          ``serve_nodes`` must be set on the cluster.
          DEVELOPMENT (int): The instance is meant for development and testing
          purposes only; it has no performance or uptime guarantees and is not
          covered by SLA.
          After a development instance is created, it can be upgraded by
          updating the instance to type ``PRODUCTION``. An instance created
          as a production instance cannot be changed to a development instance.
          When creating a development instance, ``serve_nodes`` on the cluster
          must not be set.
        """
        UNSPECIFIED = enums.Instance.Type.TYPE_UNSPECIFIED
        PRODUCTION = enums.Instance.Type.PRODUCTION
        DEVELOPMENT = enums.Instance.Type.DEVELOPMENT


class Cluster(object):
    class State(object):
        """
        Possible states of a cluster.

        Attributes:
          NOT_KNOWN (int): The state of the cluster could not be determined.
          READY (int): The cluster has been successfully created and is ready
          to serve requests.
          CREATING (int): The cluster is currently being created, and may be
          destroyed if the creation process encounters an error.
          A cluster may not be able to serve requests while being created.
          RESIZING (int): The cluster is currently being resized, and may
          revert to its previous node count if the process encounters an error.
          A cluster is still capable of serving requests while being resized,
          but may exhibit performance as if its number of allocated nodes is
          between the starting and requested states.
          DISABLED (int): The cluster has no backing nodes. The data (tables)
          still exist, but no operations can be performed on the cluster.
        """
        NOT_KNOWN = enums.Cluster.State.STATE_NOT_KNOWN
        READY = enums.Cluster.State.READY
        CREATING = enums.Cluster.State.CREATING
        RESIZING = enums.Cluster.State.RESIZING
        DISABLED = enums.Cluster.State.DISABLED


class RoutingPolicyType(object):
    """
    The type of the routing policy for app_profile.

    Attributes:
      ANY (int): Read/write requests may be routed to any cluster in the
      instance, and will fail over to another cluster in the event of
      transient errors or delays.
      Choosing this option sacrifices read-your-writes consistency to
      improve availability.
      See
      https://cloud.google.com/bigtable/docs/reference/admin/rpc/google.bigtable.admin.v2#google.bigtable.admin.v2.AppProfile.MultiClusterRoutingUseAny

      SINGLE (int): Unconditionally routes all read/write requests to a
      specific cluster.
      This option preserves read-your-writes consistency, but does not improve
      availability.
      See
      https://cloud.google.com/bigtable/docs/reference/admin/rpc/google.bigtable.admin.v2#google.bigtable.admin.v2.AppProfile.SingleClusterRouting
    """
    ANY = enums.RoutingPolicyType.ANY
    SINGLE = enums.RoutingPolicyType.SINGLE
