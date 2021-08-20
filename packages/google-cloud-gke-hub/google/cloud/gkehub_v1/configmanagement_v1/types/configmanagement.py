# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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

from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.gkehub.configmanagement.v1",
    manifest={
        "DeploymentState",
        "MembershipState",
        "MembershipSpec",
        "ConfigSync",
        "GitConfig",
        "PolicyController",
        "HierarchyControllerConfig",
        "HierarchyControllerDeploymentState",
        "HierarchyControllerVersion",
        "HierarchyControllerState",
        "OperatorState",
        "InstallError",
        "ConfigSyncState",
        "ConfigSyncVersion",
        "ConfigSyncDeploymentState",
        "SyncState",
        "SyncError",
        "ErrorResource",
        "GroupVersionKind",
        "PolicyControllerState",
        "PolicyControllerVersion",
        "GatekeeperDeploymentState",
    },
)


class DeploymentState(proto.Enum):
    r"""Enum representing the state of an ACM's deployment on a
    cluster
    """
    DEPLOYMENT_STATE_UNSPECIFIED = 0
    NOT_INSTALLED = 1
    INSTALLED = 2
    ERROR = 3


class MembershipState(proto.Message):
    r"""**Anthos Config Management**: State for a single cluster.

    Attributes:
        cluster_name (str):
            The user-defined name for the cluster used by
            ClusterSelectors to group clusters together. This should
            match Membership's membership_name, unless the user
            installed ACM on the cluster manually prior to enabling the
            ACM hub feature. Unique within a Anthos Config Management
            installation.
        membership_spec (google.cloud.gkehub.configmanagement_v1.types.MembershipSpec):
            Membership configuration in the cluster. This
            represents the actual state in the cluster,
            while the MembershipSpec in the FeatureSpec
            represents the intended state
        operator_state (google.cloud.gkehub.configmanagement_v1.types.OperatorState):
            Current install status of ACM's Operator
        config_sync_state (google.cloud.gkehub.configmanagement_v1.types.ConfigSyncState):
            Current sync status
        policy_controller_state (google.cloud.gkehub.configmanagement_v1.types.PolicyControllerState):
            PolicyController status
        hierarchy_controller_state (google.cloud.gkehub.configmanagement_v1.types.HierarchyControllerState):
            Hierarchy Controller status
    """

    cluster_name = proto.Field(proto.STRING, number=1,)
    membership_spec = proto.Field(proto.MESSAGE, number=2, message="MembershipSpec",)
    operator_state = proto.Field(proto.MESSAGE, number=3, message="OperatorState",)
    config_sync_state = proto.Field(proto.MESSAGE, number=4, message="ConfigSyncState",)
    policy_controller_state = proto.Field(
        proto.MESSAGE, number=5, message="PolicyControllerState",
    )
    hierarchy_controller_state = proto.Field(
        proto.MESSAGE, number=7, message="HierarchyControllerState",
    )


class MembershipSpec(proto.Message):
    r"""**Anthos Config Management**: Configuration for a single cluster.
    Intended to parallel the ConfigManagement CR.

    Attributes:
        config_sync (google.cloud.gkehub.configmanagement_v1.types.ConfigSync):
            Config Sync configuration for the cluster.
        policy_controller (google.cloud.gkehub.configmanagement_v1.types.PolicyController):
            Policy Controller configuration for the
            cluster.
        hierarchy_controller (google.cloud.gkehub.configmanagement_v1.types.HierarchyControllerConfig):
            Hierarchy Controller configuration for the
            cluster.
        version (str):
            Version of ACM installed.
    """

    config_sync = proto.Field(proto.MESSAGE, number=1, message="ConfigSync",)
    policy_controller = proto.Field(
        proto.MESSAGE, number=2, message="PolicyController",
    )
    hierarchy_controller = proto.Field(
        proto.MESSAGE, number=4, message="HierarchyControllerConfig",
    )
    version = proto.Field(proto.STRING, number=10,)


class ConfigSync(proto.Message):
    r"""Configuration for Config Syn.

    Attributes:
        git (google.cloud.gkehub.configmanagement_v1.types.GitConfig):
            Git repo configuration for the cluster.
        source_format (str):
            Specifies whether the Config Sync Repo is
            in “hierarchical” or “unstructured” mode.
    """

    git = proto.Field(proto.MESSAGE, number=7, message="GitConfig",)
    source_format = proto.Field(proto.STRING, number=8,)


class GitConfig(proto.Message):
    r"""Git repo configuration for a single cluster.

    Attributes:
        sync_repo (str):
            The URL of the Git repository to use as the
            source of truth.
        sync_branch (str):
            The branch of the repository to sync from.
            Default: master.
        policy_dir (str):
            The path within the Git repository that
            represents the top level of the repo to sync.
            Default: the root directory of the repository.
        sync_wait_secs (int):
            Period in seconds between consecutive syncs.
            Default: 15.
        sync_rev (str):
            Git revision (tag or hash) to check out.
            Default HEAD.
        secret_type (str):
            Type of secret configured for access to the
            Git repo.
        https_proxy (str):
            URL for the HTTPS proxy to be used when
            communicating with the Git repo.
        gcp_service_account_email (str):
            The GCP Service Account Email used for auth when secret_type
            is gcpServiceAccount.
    """

    sync_repo = proto.Field(proto.STRING, number=1,)
    sync_branch = proto.Field(proto.STRING, number=2,)
    policy_dir = proto.Field(proto.STRING, number=3,)
    sync_wait_secs = proto.Field(proto.INT64, number=4,)
    sync_rev = proto.Field(proto.STRING, number=5,)
    secret_type = proto.Field(proto.STRING, number=6,)
    https_proxy = proto.Field(proto.STRING, number=7,)
    gcp_service_account_email = proto.Field(proto.STRING, number=8,)


class PolicyController(proto.Message):
    r"""Configuration for Policy Controlle.

    Attributes:
        enabled (bool):
            Enables the installation of Policy
            Controller. If false, the rest of
            PolicyController fields take no effect.
        template_library_installed (bool):
            Installs the default template library along
            with Policy Controller.
        audit_interval_seconds (int):
            Sets the interval for Policy Controller Audit
            Scans (in seconds). When set to 0, this disables
            audit functionality altogether.
        exemptable_namespaces (Sequence[str]):
            The set of namespaces that are excluded from
            Policy Controller checks. Namespaces do not need
            to currently exist on the cluster.
        referential_rules_enabled (bool):
            Enables the ability to use Constraint
            Templates that reference to objects other than
            the object currently being evaluated.
        log_denies_enabled (bool):
            Logs all denies and dry run failures.
    """

    enabled = proto.Field(proto.BOOL, number=1,)
    template_library_installed = proto.Field(proto.BOOL, number=2, optional=True,)
    audit_interval_seconds = proto.Field(proto.INT64, number=3, optional=True,)
    exemptable_namespaces = proto.RepeatedField(proto.STRING, number=4,)
    referential_rules_enabled = proto.Field(proto.BOOL, number=5,)
    log_denies_enabled = proto.Field(proto.BOOL, number=6,)


class HierarchyControllerConfig(proto.Message):
    r"""Configuration for Hierarchy Controlle.

    Attributes:
        enabled (bool):
            Whether Hierarchy Controller is enabled in
            this cluster.
        enable_pod_tree_labels (bool):
            Whether pod tree labels are enabled in this
            cluster.
        enable_hierarchical_resource_quota (bool):
            Whether hierarchical resource quota is
            enabled in this cluster.
    """

    enabled = proto.Field(proto.BOOL, number=1,)
    enable_pod_tree_labels = proto.Field(proto.BOOL, number=2,)
    enable_hierarchical_resource_quota = proto.Field(proto.BOOL, number=3,)


class HierarchyControllerDeploymentState(proto.Message):
    r"""Deployment state for Hierarchy Controlle.

    Attributes:
        hnc (google.cloud.gkehub.configmanagement_v1.types.DeploymentState):
            The deployment state for open source HNC
            (e.g. v0.7.0-hc.0)
        extension (google.cloud.gkehub.configmanagement_v1.types.DeploymentState):
            The deployment state for Hierarchy Controller
            extension (e.g. v0.7.0-hc.1)
    """

    hnc = proto.Field(proto.ENUM, number=1, enum="DeploymentState",)
    extension = proto.Field(proto.ENUM, number=2, enum="DeploymentState",)


class HierarchyControllerVersion(proto.Message):
    r"""Version for Hierarchy Controlle.

    Attributes:
        hnc (str):
            Version for open source HNC
        extension (str):
            Version for Hierarchy Controller extension
    """

    hnc = proto.Field(proto.STRING, number=1,)
    extension = proto.Field(proto.STRING, number=2,)


class HierarchyControllerState(proto.Message):
    r"""State for Hierarchy Controlle.

    Attributes:
        version (google.cloud.gkehub.configmanagement_v1.types.HierarchyControllerVersion):
            The version for Hierarchy Controller
        state (google.cloud.gkehub.configmanagement_v1.types.HierarchyControllerDeploymentState):
            The deployment state for Hierarchy Controller
    """

    version = proto.Field(
        proto.MESSAGE, number=1, message="HierarchyControllerVersion",
    )
    state = proto.Field(
        proto.MESSAGE, number=2, message="HierarchyControllerDeploymentState",
    )


class OperatorState(proto.Message):
    r"""State information for an ACM's Operato.

    Attributes:
        version (str):
            The semenatic version number of the operator
        deployment_state (google.cloud.gkehub.configmanagement_v1.types.DeploymentState):
            The state of the Operator's deployment
        errors (Sequence[google.cloud.gkehub.configmanagement_v1.types.InstallError]):
            Install errors.
    """

    version = proto.Field(proto.STRING, number=1,)
    deployment_state = proto.Field(proto.ENUM, number=2, enum="DeploymentState",)
    errors = proto.RepeatedField(proto.MESSAGE, number=3, message="InstallError",)


class InstallError(proto.Message):
    r"""Errors pertaining to the installation of AC.

    Attributes:
        error_message (str):
            A string representing the user facing error
            message
    """

    error_message = proto.Field(proto.STRING, number=1,)


class ConfigSyncState(proto.Message):
    r"""State information for ConfigSyn.

    Attributes:
        version (google.cloud.gkehub.configmanagement_v1.types.ConfigSyncVersion):
            The version of ConfigSync deployed
        deployment_state (google.cloud.gkehub.configmanagement_v1.types.ConfigSyncDeploymentState):
            Information about the deployment of
            ConfigSync, including the version of the various
            Pods deployed
        sync_state (google.cloud.gkehub.configmanagement_v1.types.SyncState):
            The state of ConfigSync's process to sync
            configs to a cluster
    """

    version = proto.Field(proto.MESSAGE, number=1, message="ConfigSyncVersion",)
    deployment_state = proto.Field(
        proto.MESSAGE, number=2, message="ConfigSyncDeploymentState",
    )
    sync_state = proto.Field(proto.MESSAGE, number=3, message="SyncState",)


class ConfigSyncVersion(proto.Message):
    r"""Specific versioning information pertaining to ConfigSync's
    Pods

    Attributes:
        importer (str):
            Version of the deployed importer pod
        syncer (str):
            Version of the deployed syncer pod
        git_sync (str):
            Version of the deployed git-sync pod
        monitor (str):
            Version of the deployed monitor pod
        reconciler_manager (str):
            Version of the deployed reconciler-manager
            pod
        root_reconciler (str):
            Version of the deployed reconciler container
            in root-reconciler pod
    """

    importer = proto.Field(proto.STRING, number=1,)
    syncer = proto.Field(proto.STRING, number=2,)
    git_sync = proto.Field(proto.STRING, number=3,)
    monitor = proto.Field(proto.STRING, number=4,)
    reconciler_manager = proto.Field(proto.STRING, number=5,)
    root_reconciler = proto.Field(proto.STRING, number=6,)


class ConfigSyncDeploymentState(proto.Message):
    r"""The state of ConfigSync's deployment on a cluste.

    Attributes:
        importer (google.cloud.gkehub.configmanagement_v1.types.DeploymentState):
            Deployment state of the importer pod
        syncer (google.cloud.gkehub.configmanagement_v1.types.DeploymentState):
            Deployment state of the syncer pod
        git_sync (google.cloud.gkehub.configmanagement_v1.types.DeploymentState):
            Deployment state of the git-sync pod
        monitor (google.cloud.gkehub.configmanagement_v1.types.DeploymentState):
            Deployment state of the monitor pod
        reconciler_manager (google.cloud.gkehub.configmanagement_v1.types.DeploymentState):
            Deployment state of reconciler-manager pod
        root_reconciler (google.cloud.gkehub.configmanagement_v1.types.DeploymentState):
            Deployment state of root-reconciler
    """

    importer = proto.Field(proto.ENUM, number=1, enum="DeploymentState",)
    syncer = proto.Field(proto.ENUM, number=2, enum="DeploymentState",)
    git_sync = proto.Field(proto.ENUM, number=3, enum="DeploymentState",)
    monitor = proto.Field(proto.ENUM, number=4, enum="DeploymentState",)
    reconciler_manager = proto.Field(proto.ENUM, number=5, enum="DeploymentState",)
    root_reconciler = proto.Field(proto.ENUM, number=6, enum="DeploymentState",)


class SyncState(proto.Message):
    r"""State indicating an ACM's progress syncing configurations to
    a cluster

    Attributes:
        source_token (str):
            Token indicating the state of the repo.
        import_token (str):
            Token indicating the state of the importer.
        sync_token (str):
            Token indicating the state of the syncer.
        last_sync (str):
            Deprecated: use last_sync_time instead. Timestamp of when
            ACM last successfully synced the repo The time format is
            specified in https://golang.org/pkg/time/#Time.String
        last_sync_time (google.protobuf.timestamp_pb2.Timestamp):
            Timestamp type of when ACM last successfully
            synced the repo
        code (google.cloud.gkehub.configmanagement_v1.types.SyncState.SyncCode):
            Sync status code
        errors (Sequence[google.cloud.gkehub.configmanagement_v1.types.SyncError]):
            A list of errors resulting from problematic
            configs. This list will be truncated after 100
            errors, although it is unlikely for that many
            errors to simultaneously exist.
    """

    class SyncCode(proto.Enum):
        r"""An enum representing an ACM's status syncing configs to a
        cluster
        """
        SYNC_CODE_UNSPECIFIED = 0
        SYNCED = 1
        PENDING = 2
        ERROR = 3
        NOT_CONFIGURED = 4
        NOT_INSTALLED = 5
        UNAUTHORIZED = 6
        UNREACHABLE = 7

    source_token = proto.Field(proto.STRING, number=1,)
    import_token = proto.Field(proto.STRING, number=2,)
    sync_token = proto.Field(proto.STRING, number=3,)
    last_sync = proto.Field(proto.STRING, number=4,)
    last_sync_time = proto.Field(
        proto.MESSAGE, number=7, message=timestamp_pb2.Timestamp,
    )
    code = proto.Field(proto.ENUM, number=5, enum=SyncCode,)
    errors = proto.RepeatedField(proto.MESSAGE, number=6, message="SyncError",)


class SyncError(proto.Message):
    r"""An ACM created error representing a problem syncing
    configurations

    Attributes:
        code (str):
            An ACM defined error code
        error_message (str):
            A description of the error
        error_resources (Sequence[google.cloud.gkehub.configmanagement_v1.types.ErrorResource]):
            A list of config(s) associated with the
            error, if any
    """

    code = proto.Field(proto.STRING, number=1,)
    error_message = proto.Field(proto.STRING, number=2,)
    error_resources = proto.RepeatedField(
        proto.MESSAGE, number=3, message="ErrorResource",
    )


class ErrorResource(proto.Message):
    r"""Model for a config file in the git repo with an associated
    Sync error

    Attributes:
        source_path (str):
            Path in the git repo of the erroneous config
        resource_name (str):
            Metadata name of the resource that is causing
            an error
        resource_namespace (str):
            Namespace of the resource that is causing an
            error
        resource_gvk (google.cloud.gkehub.configmanagement_v1.types.GroupVersionKind):
            Group/version/kind of the resource that is
            causing an error
    """

    source_path = proto.Field(proto.STRING, number=1,)
    resource_name = proto.Field(proto.STRING, number=2,)
    resource_namespace = proto.Field(proto.STRING, number=3,)
    resource_gvk = proto.Field(proto.MESSAGE, number=4, message="GroupVersionKind",)


class GroupVersionKind(proto.Message):
    r"""A Kubernetes object's GV.

    Attributes:
        group (str):
            Kubernetes Group
        version (str):
            Kubernetes Version
        kind (str):
            Kubernetes Kind
    """

    group = proto.Field(proto.STRING, number=1,)
    version = proto.Field(proto.STRING, number=2,)
    kind = proto.Field(proto.STRING, number=3,)


class PolicyControllerState(proto.Message):
    r"""State for PolicyControllerState.

    Attributes:
        version (google.cloud.gkehub.configmanagement_v1.types.PolicyControllerVersion):
            The version of Gatekeeper Policy Controller
            deployed.
        deployment_state (google.cloud.gkehub.configmanagement_v1.types.GatekeeperDeploymentState):
            The state about the policy controller
            installation.
    """

    version = proto.Field(proto.MESSAGE, number=1, message="PolicyControllerVersion",)
    deployment_state = proto.Field(
        proto.MESSAGE, number=2, message="GatekeeperDeploymentState",
    )


class PolicyControllerVersion(proto.Message):
    r"""The build version of Gatekeeper Policy Controller is using.

    Attributes:
        version (str):
            The gatekeeper image tag that is composed of
            ACM version, git tag, build number.
    """

    version = proto.Field(proto.STRING, number=1,)


class GatekeeperDeploymentState(proto.Message):
    r"""State of Policy Controller installation.

    Attributes:
        gatekeeper_controller_manager_state (google.cloud.gkehub.configmanagement_v1.types.DeploymentState):
            Status of gatekeeper-controller-manager pod.
        gatekeeper_audit (google.cloud.gkehub.configmanagement_v1.types.DeploymentState):
            Status of gatekeeper-audit deployment.
    """

    gatekeeper_controller_manager_state = proto.Field(
        proto.ENUM, number=1, enum="DeploymentState",
    )
    gatekeeper_audit = proto.Field(proto.ENUM, number=2, enum="DeploymentState",)


__all__ = tuple(sorted(__protobuf__.manifest))
