# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
#
import proto  # type: ignore

from google.cloud.gke_backup_v1.types import common
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.gkebackup.v1",
    manifest={
        "Restore",
        "RestoreConfig",
    },
)


class Restore(proto.Message):
    r"""Represents both a request to Restore some portion of a Backup
    into a target GKE cluster and a record of the restore operation
    itself. Next id: 18

    Attributes:
        name (str):
            Output only. The full name of the Restore resource. Format:
            projects/\ */locations/*/restorePlans/*/restores/*
        uid (str):
            Output only. Server generated global unique identifier of
            `UUID <https://en.wikipedia.org/wiki/Universally_unique_identifier>`__
            format.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp when this Restore
            resource was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp when this Restore
            resource was last updated.
        description (str):
            User specified descriptive string for this
            Restore.
        backup (str):
            Required. Immutable. A reference to the
            [Backup][google.cloud.gkebackup.v1.Backup] used as the
            source from which this Restore will restore. Note that this
            Backup must be a sub-resource of the RestorePlan's
            [backup_plan][google.cloud.gkebackup.v1.RestorePlan.backup_plan].
            Format: projects/\ */locations/*/backupPlans/*/backups/*.
        cluster (str):
            Output only. The target cluster into which this Restore will
            restore data. Valid formats:

            -  projects/\ */locations/*/clusters/\*
            -  projects/\ */zones/*/clusters/\*

            Inherited from parent RestorePlan's
            [cluster][google.cloud.gkebackup.v1.RestorePlan.cluster]
            value.
        restore_config (google.cloud.gke_backup_v1.types.RestoreConfig):
            Output only. Configuration of the Restore. Inherited from
            parent RestorePlan's
            [restore_config][google.cloud.gkebackup.v1.RestorePlan.restore_config].
        labels (Mapping[str, str]):
            A set of custom labels supplied by user.
        state (google.cloud.gke_backup_v1.types.Restore.State):
            Output only. The current state of the
            Restore.
        state_reason (str):
            Output only. Human-readable description of
            why the Restore is in its current state.
        complete_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Timestamp of when the restore
            operation completed.
        resources_restored_count (int):
            Output only. Number of resources restored
            during the restore execution.
        resources_excluded_count (int):
            Output only. Number of resources excluded
            during the restore execution.
        resources_failed_count (int):
            Output only. Number of resources that failed
            to be restored during the restore execution.
        volumes_restored_count (int):
            Output only. Number of volumes restored
            during the restore execution.
        etag (str):
            Output only. ``etag`` is used for optimistic concurrency
            control as a way to help prevent simultaneous updates of a
            restore from overwriting each other. It is strongly
            suggested that systems make use of the ``etag`` in the
            read-modify-write cycle to perform restore updates in order
            to avoid race conditions: An ``etag`` is returned in the
            response to ``GetRestore``, and systems are expected to put
            that etag in the request to ``UpdateRestore`` or
            ``DeleteRestore`` to ensure that their change will be
            applied to the same version of the resource.
    """

    class State(proto.Enum):
        r"""Possible values for state of the Restore."""
        STATE_UNSPECIFIED = 0
        CREATING = 1
        IN_PROGRESS = 2
        SUCCEEDED = 3
        FAILED = 4
        DELETING = 5

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    uid = proto.Field(
        proto.STRING,
        number=2,
    )
    create_time = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    update_time = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    description = proto.Field(
        proto.STRING,
        number=5,
    )
    backup = proto.Field(
        proto.STRING,
        number=6,
    )
    cluster = proto.Field(
        proto.STRING,
        number=7,
    )
    restore_config = proto.Field(
        proto.MESSAGE,
        number=8,
        message="RestoreConfig",
    )
    labels = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=9,
    )
    state = proto.Field(
        proto.ENUM,
        number=10,
        enum=State,
    )
    state_reason = proto.Field(
        proto.STRING,
        number=11,
    )
    complete_time = proto.Field(
        proto.MESSAGE,
        number=12,
        message=timestamp_pb2.Timestamp,
    )
    resources_restored_count = proto.Field(
        proto.INT32,
        number=13,
    )
    resources_excluded_count = proto.Field(
        proto.INT32,
        number=14,
    )
    resources_failed_count = proto.Field(
        proto.INT32,
        number=15,
    )
    volumes_restored_count = proto.Field(
        proto.INT32,
        number=16,
    )
    etag = proto.Field(
        proto.STRING,
        number=17,
    )


class RestoreConfig(proto.Message):
    r"""Configuration of a restore.
    Next id: 9

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        volume_data_restore_policy (google.cloud.gke_backup_v1.types.RestoreConfig.VolumeDataRestorePolicy):
            Specifies the mechanism to be used to restore volume data.
            Default: VOLUME_DATA_RESTORE_POLICY_UNSPECIFIED (will be
            treated as NO_VOLUME_DATA_RESTORATION).
        cluster_resource_conflict_policy (google.cloud.gke_backup_v1.types.RestoreConfig.ClusterResourceConflictPolicy):
            Defines the behavior for handling the situation where
            cluster-scoped resources being restored already exist in the
            target cluster. This MUST be set to a value other than
            CLUSTER_RESOURCE_CONFLICT_POLICY_UNSPECIFIED if
            [cluster_resource_restore_scope][google.cloud.gkebackup.v1.RestoreConfig.cluster_resource_restore_scope]
            is not empty.
        namespaced_resource_restore_mode (google.cloud.gke_backup_v1.types.RestoreConfig.NamespacedResourceRestoreMode):
            Defines the behavior for handling the situation where sets
            of namespaced resources being restored already exist in the
            target cluster. This MUST be set to a value other than
            NAMESPACED_RESOURCE_RESTORE_MODE_UNSPECIFIED.
        cluster_resource_restore_scope (google.cloud.gke_backup_v1.types.RestoreConfig.ClusterResourceRestoreScope):
            Identifies the cluster-scoped resources to
            restore from the Backup. Not specifying it means
            NO cluster resource will be restored.
        all_namespaces (bool):
            Restore all namespaced resources in the
            Backup if set to "True". Specifying this field
            to "False" is an error.

            This field is a member of `oneof`_ ``namespaced_resource_restore_scope``.
        selected_namespaces (google.cloud.gke_backup_v1.types.Namespaces):
            A list of selected Namespaces to restore from
            the Backup. The listed Namespaces and all
            resources contained in them will be restored.

            This field is a member of `oneof`_ ``namespaced_resource_restore_scope``.
        selected_applications (google.cloud.gke_backup_v1.types.NamespacedNames):
            A list of selected ProtectedApplications to
            restore. The listed ProtectedApplications and
            all the resources to which they refer will be
            restored.

            This field is a member of `oneof`_ ``namespaced_resource_restore_scope``.
        substitution_rules (Sequence[google.cloud.gke_backup_v1.types.RestoreConfig.SubstitutionRule]):
            A list of transformation rules to be applied
            against Kubernetes resources as they are
            selected for restoration from a Backup. Rules
            are executed in order defined - this order
            matters, as changes made by a rule may impact
            the filtering logic of subsequent rules. An
            empty list means no substitution will occur.
    """

    class VolumeDataRestorePolicy(proto.Enum):
        r"""Defines how volume data should be restored"""
        VOLUME_DATA_RESTORE_POLICY_UNSPECIFIED = 0
        RESTORE_VOLUME_DATA_FROM_BACKUP = 1
        REUSE_VOLUME_HANDLE_FROM_BACKUP = 2
        NO_VOLUME_DATA_RESTORATION = 3

    class ClusterResourceConflictPolicy(proto.Enum):
        r"""Defines the behavior for handling the situation where
        cluster-scoped resources being restored already exist in the
        target cluster.
        """
        CLUSTER_RESOURCE_CONFLICT_POLICY_UNSPECIFIED = 0
        USE_EXISTING_VERSION = 1
        USE_BACKUP_VERSION = 2

    class NamespacedResourceRestoreMode(proto.Enum):
        r"""Defines the behavior for handling the situation where sets of
        namespaced resources being restored already exist in the target
        cluster.
        """
        NAMESPACED_RESOURCE_RESTORE_MODE_UNSPECIFIED = 0
        DELETE_AND_RESTORE = 1
        FAIL_ON_CONFLICT = 2

    class GroupKind(proto.Message):
        r"""This is a direct map to the Kubernetes GroupKind type
        `GroupKind <https://godoc.org/k8s.io/apimachinery/pkg/runtime/schema#GroupKind>`__
        and is used for identifying specific "types" of resources to
        restore.

        Attributes:
            resource_group (str):
                API group string of a Kubernetes resource,
                e.g. "apiextensions.k8s.io", "storage.k8s.io",
                etc. Note: use empty string for core API group
            resource_kind (str):
                Kind of a Kubernetes resource, e.g.
                "CustomResourceDefinition", "StorageClass", etc.
        """

        resource_group = proto.Field(
            proto.STRING,
            number=1,
        )
        resource_kind = proto.Field(
            proto.STRING,
            number=2,
        )

    class ClusterResourceRestoreScope(proto.Message):
        r"""Identifies the cluster-scoped resources to restore from the
        Backup.

        Attributes:
            selected_group_kinds (Sequence[google.cloud.gke_backup_v1.types.RestoreConfig.GroupKind]):
                A list of "types" of cluster-scoped resources
                to be restored from the Backup.  An empty list
                means that NO cluster-scoped resources will be
                restored. Note that Namespaces and
                PersistentVolume restoration is handled
                separately and is not governed by this field.
        """

        selected_group_kinds = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="RestoreConfig.GroupKind",
        )

    class SubstitutionRule(proto.Message):
        r"""A transformation rule to be applied against Kubernetes
        resources as they are selected for restoration from a Backup. A
        rule contains both filtering logic (which resources are subject
        to substitution) and substitution logic.

        Attributes:
            target_namespaces (Sequence[str]):
                (Filtering parameter) Any resource subject to
                substitution must be contained within one of the
                listed Kubernetes Namespace in the Backup. If
                this field is not provided, no namespace
                filtering will be performed (all resources in
                all Namespaces, including all cluster-scoped
                resources, will be candidates for substitution).
                To mix cluster-scoped and namespaced resources
                in the same rule, use an empty string ("") as
                one of the target namespaces.
            target_group_kinds (Sequence[google.cloud.gke_backup_v1.types.RestoreConfig.GroupKind]):
                (Filtering parameter) Any resource subject to
                substitution must belong to one of the listed
                "types". If this field is not provided, no type
                filtering will be performed (all resources of
                all types matching previous filtering parameters
                will be candidates for substitution).
            target_json_path (str):
                Required. This is a [JSONPath]
                (https://kubernetes.io/docs/reference/kubectl/jsonpath/)
                expression that matches specific fields of candidate
                resources and it operates as both a filtering parameter
                (resources that are not matched with this expression will
                not be candidates for substitution) as well as a field
                identifier (identifies exactly which fields out of the
                candidate resources will be modified).
            original_value_pattern (str):
                (Filtering parameter) This is a [regular expression]
                (https://en.wikipedia.org/wiki/Regular_expression) that is
                compared against the fields matched by the target_json_path
                expression (and must also have passed the previous filters).
                Substitution will not be performed against fields whose
                value does not match this expression. If this field is NOT
                specified, then ALL fields matched by the target_json_path
                expression will undergo substitution. Note that an empty
                (e.g., "", rather than unspecified) value for for this field
                will only match empty fields.
            new_value (str):
                This is the new value to set for any fields
                that pass the filtering and selection criteria.
                To remove a value from a Kubernetes resource,
                either leave this field unspecified, or set it
                to the empty string ("").
        """

        target_namespaces = proto.RepeatedField(
            proto.STRING,
            number=1,
        )
        target_group_kinds = proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message="RestoreConfig.GroupKind",
        )
        target_json_path = proto.Field(
            proto.STRING,
            number=3,
        )
        original_value_pattern = proto.Field(
            proto.STRING,
            number=4,
        )
        new_value = proto.Field(
            proto.STRING,
            number=5,
        )

    volume_data_restore_policy = proto.Field(
        proto.ENUM,
        number=1,
        enum=VolumeDataRestorePolicy,
    )
    cluster_resource_conflict_policy = proto.Field(
        proto.ENUM,
        number=2,
        enum=ClusterResourceConflictPolicy,
    )
    namespaced_resource_restore_mode = proto.Field(
        proto.ENUM,
        number=3,
        enum=NamespacedResourceRestoreMode,
    )
    cluster_resource_restore_scope = proto.Field(
        proto.MESSAGE,
        number=4,
        message=ClusterResourceRestoreScope,
    )
    all_namespaces = proto.Field(
        proto.BOOL,
        number=5,
        oneof="namespaced_resource_restore_scope",
    )
    selected_namespaces = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="namespaced_resource_restore_scope",
        message=common.Namespaces,
    )
    selected_applications = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="namespaced_resource_restore_scope",
        message=common.NamespacedNames,
    )
    substitution_rules = proto.RepeatedField(
        proto.MESSAGE,
        number=8,
        message=SubstitutionRule,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
