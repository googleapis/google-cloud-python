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


class Cluster(object):
    class Status(enum.IntEnum):
        """
        The current status of the cluster.

        Attributes:
          STATUS_UNSPECIFIED (int): Not set.
          PROVISIONING (int): The PROVISIONING state indicates the cluster is being created.
          RUNNING (int): The RUNNING state indicates the cluster has been created and is fully
          usable.
          RECONCILING (int): The RECONCILING state indicates that some work is actively being done on
          the cluster, such as upgrading the master or node software. Details can
          be found in the ``statusMessage`` field.
          STOPPING (int): The STOPPING state indicates the cluster is being deleted.
          ERROR (int): The ERROR state indicates the cluster may be unusable. Details can be
          found in the ``statusMessage`` field.
          DEGRADED (int): The DEGRADED state indicates the cluster requires user action to restore
          full functionality. Details can be found in the ``statusMessage`` field.
        """

        STATUS_UNSPECIFIED = 0
        PROVISIONING = 1
        RUNNING = 2
        RECONCILING = 3
        STOPPING = 4
        ERROR = 5
        DEGRADED = 6


class NetworkPolicy(object):
    class Provider(enum.IntEnum):
        """
        Allowed Network Policy providers.

        Attributes:
          PROVIDER_UNSPECIFIED (int): Not set
          CALICO (int): Tigera (Calico Felix).
        """

        PROVIDER_UNSPECIFIED = 0
        CALICO = 1


class NodePool(object):
    class Status(enum.IntEnum):
        """
        The current status of the node pool instance.

        Attributes:
          STATUS_UNSPECIFIED (int): Not set.
          PROVISIONING (int): The PROVISIONING state indicates the node pool is being created.
          RUNNING (int): The RUNNING state indicates the node pool has been created
          and is fully usable.
          RUNNING_WITH_ERROR (int): The RUNNING\_WITH\_ERROR state indicates the node pool has been created
          and is partially usable. Some error state has occurred and some
          functionality may be impaired. Customer may need to reissue a request or
          trigger a new update.
          RECONCILING (int): The RECONCILING state indicates that some work is actively being done on
          the node pool, such as upgrading node software. Details can be found in
          the ``statusMessage`` field.
          STOPPING (int): The STOPPING state indicates the node pool is being deleted.
          ERROR (int): The ERROR state indicates the node pool may be unusable. Details can be
          found in the ``statusMessage`` field.
        """

        STATUS_UNSPECIFIED = 0
        PROVISIONING = 1
        RUNNING = 2
        RUNNING_WITH_ERROR = 3
        RECONCILING = 4
        STOPPING = 5
        ERROR = 6


class Operation(object):
    class Status(enum.IntEnum):
        """
        Current status of the operation.

        Attributes:
          STATUS_UNSPECIFIED (int): Not set.
          PENDING (int): The operation has been created.
          RUNNING (int): The operation is currently running.
          DONE (int): The operation is done, either cancelled or completed.
          ABORTING (int): The operation is aborting.
        """

        STATUS_UNSPECIFIED = 0
        PENDING = 1
        RUNNING = 2
        DONE = 3
        ABORTING = 4

    class Type(enum.IntEnum):
        """
        Operation type.

        Attributes:
          TYPE_UNSPECIFIED (int): Not set.
          CREATE_CLUSTER (int): Cluster create.
          DELETE_CLUSTER (int): Cluster delete.
          UPGRADE_MASTER (int): A master upgrade.
          UPGRADE_NODES (int): A node upgrade.
          REPAIR_CLUSTER (int): Cluster repair.
          UPDATE_CLUSTER (int): Cluster update.
          CREATE_NODE_POOL (int): Node pool create.
          DELETE_NODE_POOL (int): Node pool delete.
          SET_NODE_POOL_MANAGEMENT (int): Set node pool management.
          AUTO_REPAIR_NODES (int): Automatic node pool repair.
          AUTO_UPGRADE_NODES (int): Automatic node upgrade.
          SET_LABELS (int): Set labels.
          SET_MASTER_AUTH (int): Set/generate master auth materials
          SET_NODE_POOL_SIZE (int): Set node pool size.
          SET_NETWORK_POLICY (int): Updates network policy for a cluster.
          SET_MAINTENANCE_POLICY (int): Set the maintenance policy.
        """

        TYPE_UNSPECIFIED = 0
        CREATE_CLUSTER = 1
        DELETE_CLUSTER = 2
        UPGRADE_MASTER = 3
        UPGRADE_NODES = 4
        REPAIR_CLUSTER = 5
        UPDATE_CLUSTER = 6
        CREATE_NODE_POOL = 7
        DELETE_NODE_POOL = 8
        SET_NODE_POOL_MANAGEMENT = 9
        AUTO_REPAIR_NODES = 10
        AUTO_UPGRADE_NODES = 11
        SET_LABELS = 12
        SET_MASTER_AUTH = 13
        SET_NODE_POOL_SIZE = 14
        SET_NETWORK_POLICY = 15
        SET_MAINTENANCE_POLICY = 16


class SetMasterAuthRequest(object):
    class Action(enum.IntEnum):
        """
        Operation type: what type update to perform.

        Attributes:
          UNKNOWN (int): Operation is unknown and will error out.
          SET_PASSWORD (int): Set the password to a user generated value.
          GENERATE_PASSWORD (int): Generate a new password and set it to that.
          SET_USERNAME (int): Set the username.  If an empty username is provided, basic authentication
          is disabled for the cluster.  If a non-empty username is provided, basic
          authentication is enabled, with either a provided password or a generated
          one.
        """

        UNKNOWN = 0
        SET_PASSWORD = 1
        GENERATE_PASSWORD = 2
        SET_USERNAME = 3
