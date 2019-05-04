# -*- coding: utf-8 -*-
#
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
"""Wrappers for protocol buffer enum types."""

import enum


class StorageType(enum.IntEnum):
    """
    Storage media types for persisting Bigtable data.

    Attributes:
      STORAGE_TYPE_UNSPECIFIED (int): The user did not specify a storage type.
      SSD (int): Flash (SSD) storage should be used.
      HDD (int): Magnetic drive (HDD) storage should be used.
    """

    STORAGE_TYPE_UNSPECIFIED = 0
    SSD = 1
    HDD = 2


class Cluster(object):
    class State(enum.IntEnum):
        """
        Possible states of a cluster.

        Attributes:
          STATE_NOT_KNOWN (int): The state of the cluster could not be determined.
          READY (int): The cluster has been successfully created and is ready to serve requests.
          CREATING (int): The cluster is currently being created, and may be destroyed
          if the creation process encounters an error.
          A cluster may not be able to serve requests while being created.
          RESIZING (int): The cluster is currently being resized, and may revert to its previous
          node count if the process encounters an error.
          A cluster is still capable of serving requests while being resized,
          but may exhibit performance as if its number of allocated nodes is
          between the starting and requested states.
          DISABLED (int): The cluster has no backing nodes. The data (tables) still
          exist, but no operations can be performed on the cluster.
        """

        STATE_NOT_KNOWN = 0
        READY = 1
        CREATING = 2
        RESIZING = 3
        DISABLED = 4


class Instance(object):
    class State(enum.IntEnum):
        """
        Possible states of an instance.

        Attributes:
          STATE_NOT_KNOWN (int): The state of the instance could not be determined.
          READY (int): The instance has been successfully created and can serve requests
          to its tables.
          CREATING (int): The instance is currently being created, and may be destroyed
          if the creation process encounters an error.
        """

        STATE_NOT_KNOWN = 0
        READY = 1
        CREATING = 2

    class Type(enum.IntEnum):
        """
        The type of the instance.

        Attributes:
          TYPE_UNSPECIFIED (int): The type of the instance is unspecified. If set when creating an
          instance, a ``PRODUCTION`` instance will be created. If set when
          updating an instance, the type will be left unchanged.
          PRODUCTION (int): An instance meant for production use. ``serve_nodes`` must be set on the
          cluster.
          DEVELOPMENT (int): The instance is meant for development and testing purposes only; it has
          no performance or uptime guarantees and is not covered by SLA. After a
          development instance is created, it can be upgraded by updating the
          instance to type ``PRODUCTION``. An instance created as a production
          instance cannot be changed to a development instance. When creating a
          development instance, ``serve_nodes`` on the cluster must not be set.
        """

        TYPE_UNSPECIFIED = 0
        PRODUCTION = 1
        DEVELOPMENT = 2


class Snapshot(object):
    class State(enum.IntEnum):
        """
        Possible states of a snapshot.

        Attributes:
          STATE_NOT_KNOWN (int): The state of the snapshot could not be determined.
          READY (int): The snapshot has been successfully created and can serve all requests.
          CREATING (int): The snapshot is currently being created, and may be destroyed if the
          creation process encounters an error. A snapshot may not be restored to a
          table while it is being created.
        """

        STATE_NOT_KNOWN = 0
        READY = 1
        CREATING = 2


class Table(object):
    class TimestampGranularity(enum.IntEnum):
        """
        Possible timestamp granularities to use when keeping multiple versions
        of data in a table.

        Attributes:
          TIMESTAMP_GRANULARITY_UNSPECIFIED (int): The user did not specify a granularity. Should not be returned.
          When specified during table creation, MILLIS will be used.
          MILLIS (int): The table keeps data versioned at a granularity of 1ms.
        """

        TIMESTAMP_GRANULARITY_UNSPECIFIED = 0
        MILLIS = 1

    class View(enum.IntEnum):
        """
        Defines a view over a table's fields.

        Attributes:
          VIEW_UNSPECIFIED (int): Uses the default view for each method as documented in its request.
          NAME_ONLY (int): Only populates ``name``.
          SCHEMA_VIEW (int): Only populates ``name`` and fields related to the table's schema.
          REPLICATION_VIEW (int): Only populates ``name`` and fields related to the table's replication
          state.
          FULL (int): Populates all fields.
        """

        VIEW_UNSPECIFIED = 0
        NAME_ONLY = 1
        SCHEMA_VIEW = 2
        REPLICATION_VIEW = 3
        FULL = 4

    class ClusterState(object):
        class ReplicationState(enum.IntEnum):
            """
            Table replication states.

            Attributes:
              STATE_NOT_KNOWN (int): The replication state of the table is unknown in this cluster.
              INITIALIZING (int): The cluster was recently created, and the table must finish copying
              over pre-existing data from other clusters before it can begin
              receiving live replication updates and serving Data API requests.
              PLANNED_MAINTENANCE (int): The table is temporarily unable to serve Data API requests from this
              cluster due to planned internal maintenance.
              UNPLANNED_MAINTENANCE (int): The table is temporarily unable to serve Data API requests from this
              cluster due to unplanned or emergency maintenance.
              READY (int): The table can serve Data API requests from this cluster. Depending on
              replication delay, reads may not immediately reflect the state of the
              table in other clusters.
            """

            STATE_NOT_KNOWN = 0
            INITIALIZING = 1
            PLANNED_MAINTENANCE = 2
            UNPLANNED_MAINTENANCE = 3
            READY = 4
