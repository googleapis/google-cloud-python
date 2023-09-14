# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
from __future__ import annotations

from typing import MutableMapping, MutableSequence

from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.gke_backup_v1.types import common

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
            ``projects/*/locations/*/restorePlans/*/restores/*``
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
            Format: ``projects/*/locations/*/backupPlans/*/backups/*``.
        cluster (str):
            Output only. The target cluster into which this Restore will
            restore data. Valid formats:

            -  ``projects/*/locations/*/clusters/*``
            -  ``projects/*/zones/*/clusters/*``

            Inherited from parent RestorePlan's
            [cluster][google.cloud.gkebackup.v1.RestorePlan.cluster]
            value.
        restore_config (google.cloud.gke_backup_v1.types.RestoreConfig):
            Output only. Configuration of the Restore. Inherited from
            parent RestorePlan's
            [restore_config][google.cloud.gkebackup.v1.RestorePlan.restore_config].
        labels (MutableMapping[str, str]):
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
        r"""Possible values for state of the Restore.

        Values:
            STATE_UNSPECIFIED (0):
                The Restore resource is in the process of
                being created.
            CREATING (1):
                The Restore resource has been created and the
                associated RestoreJob Kubernetes resource has
                been injected into target cluster.
            IN_PROGRESS (2):
                The gkebackup agent in the cluster has begun
                executing the restore operation.
            SUCCEEDED (3):
                The restore operation has completed
                successfully. Restored workloads may not yet be
                operational.
            FAILED (4):
                The restore operation has failed.
            DELETING (5):
                This Restore resource is in the process of
                being deleted.
        """
        STATE_UNSPECIFIED = 0
        CREATING = 1
        IN_PROGRESS = 2
        SUCCEEDED = 3
        FAILED = 4
        DELETING = 5

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=2,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    description: str = proto.Field(
        proto.STRING,
        number=5,
    )
    backup: str = proto.Field(
        proto.STRING,
        number=6,
    )
    cluster: str = proto.Field(
        proto.STRING,
        number=7,
    )
    restore_config: "RestoreConfig" = proto.Field(
        proto.MESSAGE,
        number=8,
        message="RestoreConfig",
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=9,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=10,
        enum=State,
    )
    state_reason: str = proto.Field(
        proto.STRING,
        number=11,
    )
    complete_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=12,
        message=timestamp_pb2.Timestamp,
    )
    resources_restored_count: int = proto.Field(
        proto.INT32,
        number=13,
    )
    resources_excluded_count: int = proto.Field(
        proto.INT32,
        number=14,
    )
    resources_failed_count: int = proto.Field(
        proto.INT32,
        number=15,
    )
    volumes_restored_count: int = proto.Field(
        proto.INT32,
        number=16,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=17,
    )


class RestoreConfig(proto.Message):
    r"""Configuration of a restore.
    Next id: 12

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
        no_namespaces (bool):
            Do not restore any namespaced resources if
            set to "True". Specifying this field to "False"
            is not allowed.

            This field is a member of `oneof`_ ``namespaced_resource_restore_scope``.
        excluded_namespaces (google.cloud.gke_backup_v1.types.Namespaces):
            A list of selected namespaces excluded from
            restoration. All namespaces except those in this
            list will be restored.

            This field is a member of `oneof`_ ``namespaced_resource_restore_scope``.
        substitution_rules (MutableSequence[google.cloud.gke_backup_v1.types.RestoreConfig.SubstitutionRule]):
            A list of transformation rules to be applied
            against Kubernetes resources as they are
            selected for restoration from a Backup. Rules
            are executed in order defined - this order
            matters, as changes made by a rule may impact
            the filtering logic of subsequent rules. An
            empty list means no substitution will occur.
        transformation_rules (MutableSequence[google.cloud.gke_backup_v1.types.RestoreConfig.TransformationRule]):
            A list of transformation rules to be applied
            against Kubernetes resources as they are
            selected for restoration from a Backup. Rules
            are executed in order defined - this order
            matters, as changes made by a rule may impact
            the filtering logic of subsequent rules. An
            empty list means no transformation will occur.
    """

    class VolumeDataRestorePolicy(proto.Enum):
        r"""Defines how volume data should be restored.

        Values:
            VOLUME_DATA_RESTORE_POLICY_UNSPECIFIED (0):
                Unspecified (illegal).
            RESTORE_VOLUME_DATA_FROM_BACKUP (1):
                For each PVC to be restored, create a new
                underlying volume and PV from the corresponding
                VolumeBackup contained within the Backup.
            REUSE_VOLUME_HANDLE_FROM_BACKUP (2):
                For each PVC to be restored, attempt to reuse
                the original PV contained in the Backup (with
                its original underlying volume). This option is
                likely only usable when restoring a workload to
                its original cluster.
            NO_VOLUME_DATA_RESTORATION (3):
                For each PVC to be restored, create PVC
                without any particular action to restore data.
                In this case, the normal Kubernetes provisioning
                logic would kick in, and this would likely
                result in either dynamically provisioning blank
                PVs or binding to statically provisioned PVs.
        """
        VOLUME_DATA_RESTORE_POLICY_UNSPECIFIED = 0
        RESTORE_VOLUME_DATA_FROM_BACKUP = 1
        REUSE_VOLUME_HANDLE_FROM_BACKUP = 2
        NO_VOLUME_DATA_RESTORATION = 3

    class ClusterResourceConflictPolicy(proto.Enum):
        r"""Defines the behavior for handling the situation where
        cluster-scoped resources being restored already exist in the
        target cluster.

        Values:
            CLUSTER_RESOURCE_CONFLICT_POLICY_UNSPECIFIED (0):
                Unspecified. Only allowed if no
                cluster-scoped resources will be restored.
            USE_EXISTING_VERSION (1):
                Do not attempt to restore the conflicting
                resource.
            USE_BACKUP_VERSION (2):
                Delete the existing version before
                re-creating it from the Backup. This is a
                dangerous option which could cause unintentional
                data loss if used inappropriately. For example,
                deleting a CRD will cause Kubernetes to delete
                all CRs of that type.
        """
        CLUSTER_RESOURCE_CONFLICT_POLICY_UNSPECIFIED = 0
        USE_EXISTING_VERSION = 1
        USE_BACKUP_VERSION = 2

    class NamespacedResourceRestoreMode(proto.Enum):
        r"""Defines the behavior for handling the situation where sets of
        namespaced resources being restored already exist in the target
        cluster.

        Values:
            NAMESPACED_RESOURCE_RESTORE_MODE_UNSPECIFIED (0):
                Unspecified (invalid).
            DELETE_AND_RESTORE (1):
                When conflicting top-level resources (either
                Namespaces or ProtectedApplications, depending
                upon the scope) are encountered, this will first
                trigger a delete of the conflicting resource AND
                ALL OF ITS REFERENCED RESOURCES (e.g., all
                resources in the Namespace or all resources
                referenced by the ProtectedApplication) before
                restoring the resources from the Backup. This
                mode should only be used when you are intending
                to revert some portion of a cluster to an
                earlier state.
            FAIL_ON_CONFLICT (2):
                If conflicting top-level resources (either
                Namespaces or ProtectedApplications, depending
                upon the scope) are encountered at the beginning
                of a restore process, the Restore will fail.  If
                a conflict occurs during the restore process
                itself (e.g., because an out of band process
                creates conflicting resources), a conflict will
                be reported.
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

        resource_group: str = proto.Field(
            proto.STRING,
            number=1,
        )
        resource_kind: str = proto.Field(
            proto.STRING,
            number=2,
        )

    class ClusterResourceRestoreScope(proto.Message):
        r"""Defines the scope of cluster-scoped resources to restore.

        Some group kinds are not reasonable choices for a restore, and
        will cause an error if selected here. Any scope selection that
        would restore "all valid" resources automatically excludes these
        group kinds.
        - gkebackup.gke.io/BackupJob
        - gkebackup.gke.io/RestoreJob
        - metrics.k8s.io/NodeMetrics
        - migration.k8s.io/StorageState
        - migration.k8s.io/StorageVersionMigration
        - Node
        - snapshot.storage.k8s.io/VolumeSnapshotContent
        - storage.k8s.io/CSINode

        Some group kinds are driven by restore configuration elsewhere,
        and will cause an error if selected here.
        - Namespace
        - PersistentVolume

        Attributes:
            selected_group_kinds (MutableSequence[google.cloud.gke_backup_v1.types.RestoreConfig.GroupKind]):
                A list of cluster-scoped resource group kinds
                to restore from the backup. If specified, only
                the selected resources will be restored.
                Mutually exclusive to any other field in the
                message.
            excluded_group_kinds (MutableSequence[google.cloud.gke_backup_v1.types.RestoreConfig.GroupKind]):
                A list of cluster-scoped resource group kinds
                to NOT restore from the backup. If specified,
                all valid cluster-scoped resources will be
                restored except for those specified in the list.
                Mutually exclusive to any other field in the
                message.
            all_group_kinds (bool):
                If True, all valid cluster-scoped resources
                will be restored. Mutually exclusive to any
                other field in the message.
            no_group_kinds (bool):
                If True, no cluster-scoped resources will be
                restored. This has the same restore scope as if
                the message is not defined. Mutually exclusive
                to any other field in the message.
        """

        selected_group_kinds: MutableSequence[
            "RestoreConfig.GroupKind"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="RestoreConfig.GroupKind",
        )
        excluded_group_kinds: MutableSequence[
            "RestoreConfig.GroupKind"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message="RestoreConfig.GroupKind",
        )
        all_group_kinds: bool = proto.Field(
            proto.BOOL,
            number=3,
        )
        no_group_kinds: bool = proto.Field(
            proto.BOOL,
            number=4,
        )

    class SubstitutionRule(proto.Message):
        r"""A transformation rule to be applied against Kubernetes
        resources as they are selected for restoration from a Backup. A
        rule contains both filtering logic (which resources are subject
        to substitution) and substitution logic.

        Attributes:
            target_namespaces (MutableSequence[str]):
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
            target_group_kinds (MutableSequence[google.cloud.gke_backup_v1.types.RestoreConfig.GroupKind]):
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
                (e.g., "", rather than unspecified) value for this field
                will only match empty fields.
            new_value (str):
                This is the new value to set for any fields
                that pass the filtering and selection criteria.
                To remove a value from a Kubernetes resource,
                either leave this field unspecified, or set it
                to the empty string ("").
        """

        target_namespaces: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=1,
        )
        target_group_kinds: MutableSequence[
            "RestoreConfig.GroupKind"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message="RestoreConfig.GroupKind",
        )
        target_json_path: str = proto.Field(
            proto.STRING,
            number=3,
        )
        original_value_pattern: str = proto.Field(
            proto.STRING,
            number=4,
        )
        new_value: str = proto.Field(
            proto.STRING,
            number=5,
        )

    class TransformationRuleAction(proto.Message):
        r"""TransformationRuleAction defines a TransformationRule action
        based on the JSON Patch RFC
        (https://www.rfc-editor.org/rfc/rfc6902)

        Attributes:
            op (google.cloud.gke_backup_v1.types.RestoreConfig.TransformationRuleAction.Op):
                Required. op specifies the operation to
                perform.
            from_path (str):
                A string containing a JSON Pointer value that
                references the location in the target document
                to move the value from.
            path (str):
                A string containing a JSON-Pointer value that
                references a location within the target document
                where the operation is performed.
            value (str):
                A string that specifies the desired value in
                string format to use for transformation.
        """

        class Op(proto.Enum):
            r"""Possible values for operations of a transformation rule
            action.

            Values:
                OP_UNSPECIFIED (0):
                    Unspecified operation
                REMOVE (1):
                    The "remove" operation removes the value at
                    the target location.
                MOVE (2):
                    The "move" operation removes the value at a
                    specified location and adds it to the target
                    location.
                COPY (3):
                    The "copy" operation copies the value at a
                    specified location to the target location.
                ADD (4):
                    The "add" operation performs one of the
                    following functions, depending upon what the
                    target location references:

                    1. If the target location specifies an array
                        index, a new value is inserted into the
                        array at the specified index.
                    2. If the target location specifies an object
                        member that does not already exist, a new
                        member is added to the object.
                    3. If the target location specifies an object
                        member that does exist, that member's value
                        is replaced.
                TEST (5):
                    The "test" operation tests that a value at
                    the target location is equal to a specified
                    value.
                REPLACE (6):
                    The "replace" operation replaces the value at
                    the target location with a new value.  The
                    operation object MUST contain a "value" member
                    whose content specifies the replacement value.
            """
            OP_UNSPECIFIED = 0
            REMOVE = 1
            MOVE = 2
            COPY = 3
            ADD = 4
            TEST = 5
            REPLACE = 6

        op: "RestoreConfig.TransformationRuleAction.Op" = proto.Field(
            proto.ENUM,
            number=1,
            enum="RestoreConfig.TransformationRuleAction.Op",
        )
        from_path: str = proto.Field(
            proto.STRING,
            number=2,
        )
        path: str = proto.Field(
            proto.STRING,
            number=3,
        )
        value: str = proto.Field(
            proto.STRING,
            number=4,
        )

    class ResourceFilter(proto.Message):
        r"""ResourceFilter specifies matching criteria to limit the scope
        of a change to a specific set of kubernetes resources that are
        selected for restoration from a backup.

        Attributes:
            namespaces (MutableSequence[str]):
                (Filtering parameter) Any resource subject to
                transformation must be contained within one of
                the listed Kubernetes Namespace in the Backup.
                If this field is not provided, no namespace
                filtering will be performed (all resources in
                all Namespaces, including all cluster-scoped
                resources, will be candidates for
                transformation).
                To mix cluster-scoped and namespaced resources
                in the same rule, use an empty string ("") as
                one of the target namespaces.
            group_kinds (MutableSequence[google.cloud.gke_backup_v1.types.RestoreConfig.GroupKind]):
                (Filtering parameter) Any resource subject to
                transformation must belong to one of the listed
                "types". If this field is not provided, no type
                filtering will be performed (all resources of
                all types matching previous filtering parameters
                will be candidates for transformation).
            json_path (str):
                This is a [JSONPath]
                (https://github.com/json-path/JsonPath/blob/master/README.md)
                expression that matches specific fields of candidate
                resources and it operates as a filtering parameter
                (resources that are not matched with this expression will
                not be candidates for transformation).
        """

        namespaces: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=1,
        )
        group_kinds: MutableSequence["RestoreConfig.GroupKind"] = proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message="RestoreConfig.GroupKind",
        )
        json_path: str = proto.Field(
            proto.STRING,
            number=3,
        )

    class TransformationRule(proto.Message):
        r"""A transformation rule to be applied against Kubernetes
        resources as they are selected for restoration from a Backup. A
        rule contains both filtering logic (which resources are subject
        to transform) and transformation logic.

        Attributes:
            field_actions (MutableSequence[google.cloud.gke_backup_v1.types.RestoreConfig.TransformationRuleAction]):
                Required. A list of transformation rule
                actions to take against candidate resources.
                Actions are executed in order defined - this
                order matters, as they could potentially
                interfere with each other and the first
                operation could affect the outcome of the second
                operation.
            resource_filter (google.cloud.gke_backup_v1.types.RestoreConfig.ResourceFilter):
                This field is used to specify a set of fields
                that should be used to determine which resources
                in backup should be acted upon by the supplied
                transformation rule actions, and this will
                ensure that only specific resources are affected
                by transformation rule actions.
            description (str):
                The description is a user specified string
                description of the transformation rule.
        """

        field_actions: MutableSequence[
            "RestoreConfig.TransformationRuleAction"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="RestoreConfig.TransformationRuleAction",
        )
        resource_filter: "RestoreConfig.ResourceFilter" = proto.Field(
            proto.MESSAGE,
            number=2,
            message="RestoreConfig.ResourceFilter",
        )
        description: str = proto.Field(
            proto.STRING,
            number=3,
        )

    volume_data_restore_policy: VolumeDataRestorePolicy = proto.Field(
        proto.ENUM,
        number=1,
        enum=VolumeDataRestorePolicy,
    )
    cluster_resource_conflict_policy: ClusterResourceConflictPolicy = proto.Field(
        proto.ENUM,
        number=2,
        enum=ClusterResourceConflictPolicy,
    )
    namespaced_resource_restore_mode: NamespacedResourceRestoreMode = proto.Field(
        proto.ENUM,
        number=3,
        enum=NamespacedResourceRestoreMode,
    )
    cluster_resource_restore_scope: ClusterResourceRestoreScope = proto.Field(
        proto.MESSAGE,
        number=4,
        message=ClusterResourceRestoreScope,
    )
    all_namespaces: bool = proto.Field(
        proto.BOOL,
        number=5,
        oneof="namespaced_resource_restore_scope",
    )
    selected_namespaces: common.Namespaces = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="namespaced_resource_restore_scope",
        message=common.Namespaces,
    )
    selected_applications: common.NamespacedNames = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="namespaced_resource_restore_scope",
        message=common.NamespacedNames,
    )
    no_namespaces: bool = proto.Field(
        proto.BOOL,
        number=9,
        oneof="namespaced_resource_restore_scope",
    )
    excluded_namespaces: common.Namespaces = proto.Field(
        proto.MESSAGE,
        number=10,
        oneof="namespaced_resource_restore_scope",
        message=common.Namespaces,
    )
    substitution_rules: MutableSequence[SubstitutionRule] = proto.RepeatedField(
        proto.MESSAGE,
        number=8,
        message=SubstitutionRule,
    )
    transformation_rules: MutableSequence[TransformationRule] = proto.RepeatedField(
        proto.MESSAGE,
        number=11,
        message=TransformationRule,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
