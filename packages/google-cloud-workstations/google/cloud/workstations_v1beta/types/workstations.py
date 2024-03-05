# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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

from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.workstations.v1beta",
    manifest={
        "WorkstationCluster",
        "WorkstationConfig",
        "Workstation",
        "GetWorkstationClusterRequest",
        "ListWorkstationClustersRequest",
        "ListWorkstationClustersResponse",
        "CreateWorkstationClusterRequest",
        "UpdateWorkstationClusterRequest",
        "DeleteWorkstationClusterRequest",
        "GetWorkstationConfigRequest",
        "ListWorkstationConfigsRequest",
        "ListWorkstationConfigsResponse",
        "ListUsableWorkstationConfigsRequest",
        "ListUsableWorkstationConfigsResponse",
        "CreateWorkstationConfigRequest",
        "UpdateWorkstationConfigRequest",
        "DeleteWorkstationConfigRequest",
        "GetWorkstationRequest",
        "ListWorkstationsRequest",
        "ListWorkstationsResponse",
        "ListUsableWorkstationsRequest",
        "ListUsableWorkstationsResponse",
        "CreateWorkstationRequest",
        "UpdateWorkstationRequest",
        "DeleteWorkstationRequest",
        "StartWorkstationRequest",
        "StopWorkstationRequest",
        "GenerateAccessTokenRequest",
        "GenerateAccessTokenResponse",
        "OperationMetadata",
    },
)


class WorkstationCluster(proto.Message):
    r"""A workstation cluster resource in the Cloud Workstations API.

    Defines a group of workstations in a particular region and the
    VPC network they're attached to.

    Attributes:
        name (str):
            Full name of this workstation cluster.
        display_name (str):
            Optional. Human-readable name for this
            workstation cluster.
        uid (str):
            Output only. A system-assigned unique
            identifier for this workstation cluster.
        reconciling (bool):
            Output only. Indicates whether this
            workstation cluster is currently being updated
            to match its intended state.
        annotations (MutableMapping[str, str]):
            Optional. Client-specified annotations.
        labels (MutableMapping[str, str]):
            Optional.
            `Labels <https://cloud.google.com/workstations/docs/label-resources>`__
            that are applied to the workstation cluster and that are
            also propagated to the underlying Compute Engine resources.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when this workstation
            cluster was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when this workstation
            cluster was most recently updated.
        delete_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when this workstation
            cluster was soft-deleted.
        etag (str):
            Optional. Checksum computed by the server.
            May be sent on update and delete requests to
            make sure that the client has an up-to-date
            value before proceeding.
        network (str):
            Immutable. Name of the Compute Engine network
            in which instances associated with this
            workstation cluster will be created.
        subnetwork (str):
            Immutable. Name of the Compute Engine
            subnetwork in which instances associated with
            this workstation cluster will be created. Must
            be part of the subnetwork specified for this
            workstation cluster.
        control_plane_ip (str):
            Output only. The private IP address of the
            control plane for this workstation cluster.
            Workstation VMs need access to this IP address
            to work with the service, so make sure that your
            firewall rules allow egress from the workstation
            VMs to this address.
        private_cluster_config (google.cloud.workstations_v1beta.types.WorkstationCluster.PrivateClusterConfig):
            Optional. Configuration for private
            workstation cluster.
        degraded (bool):
            Output only. Whether this workstation cluster is in degraded
            mode, in which case it may require user action to restore
            full functionality. Details can be found in
            [conditions][google.cloud.workstations.v1beta.WorkstationCluster.conditions].
        conditions (MutableSequence[google.rpc.status_pb2.Status]):
            Output only. Status conditions describing the
            workstation cluster's current state.
    """

    class PrivateClusterConfig(proto.Message):
        r"""Configuration options for private workstation clusters.

        Attributes:
            enable_private_endpoint (bool):
                Immutable. Whether Workstations endpoint is
                private.
            cluster_hostname (str):
                Output only. Hostname for the workstation
                cluster. This field will be populated only when
                private endpoint is enabled. To access
                workstations in the workstation cluster, create
                a new DNS zone mapping this domain name to an
                internal IP address and a forwarding rule
                mapping that address to the service attachment.
            service_attachment_uri (str):
                Output only. Service attachment URI for the workstation
                cluster. The service attachemnt is created when private
                endpoint is enabled. To access workstations in the
                workstation cluster, configure access to the managed service
                using `Private Service
                Connect <https://cloud.google.com/vpc/docs/configure-private-service-connect-services>`__.
            allowed_projects (MutableSequence[str]):
                Optional. Additional projects that are
                allowed to attach to the workstation cluster's
                service attachment. By default, the workstation
                cluster's project and the VPC host project (if
                different) are allowed.
        """

        enable_private_endpoint: bool = proto.Field(
            proto.BOOL,
            number=1,
        )
        cluster_hostname: str = proto.Field(
            proto.STRING,
            number=2,
        )
        service_attachment_uri: str = proto.Field(
            proto.STRING,
            number=3,
        )
        allowed_projects: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=4,
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=3,
    )
    reconciling: bool = proto.Field(
        proto.BOOL,
        number=4,
    )
    annotations: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=5,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=15,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=7,
        message=timestamp_pb2.Timestamp,
    )
    delete_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=8,
        message=timestamp_pb2.Timestamp,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=9,
    )
    network: str = proto.Field(
        proto.STRING,
        number=10,
    )
    subnetwork: str = proto.Field(
        proto.STRING,
        number=11,
    )
    control_plane_ip: str = proto.Field(
        proto.STRING,
        number=16,
    )
    private_cluster_config: PrivateClusterConfig = proto.Field(
        proto.MESSAGE,
        number=12,
        message=PrivateClusterConfig,
    )
    degraded: bool = proto.Field(
        proto.BOOL,
        number=13,
    )
    conditions: MutableSequence[status_pb2.Status] = proto.RepeatedField(
        proto.MESSAGE,
        number=14,
        message=status_pb2.Status,
    )


class WorkstationConfig(proto.Message):
    r"""A workstation configuration resource in the Cloud Workstations API.

    Workstation configurations act as templates for workstations. The
    workstation configuration defines details such as the workstation
    virtual machine (VM) instance type, persistent storage, container
    image defining environment, which IDE or Code Editor to use, and
    more. Administrators and platform teams can also use `Identity and
    Access Management
    (IAM) <https://cloud.google.com/iam/docs/overview>`__ rules to grant
    access to teams or to individual developers.

    Attributes:
        name (str):
            Full name of this workstation configuration.
        display_name (str):
            Optional. Human-readable name for this
            workstation configuration.
        uid (str):
            Output only. A system-assigned unique
            identifier for this workstation configuration.
        reconciling (bool):
            Output only. Indicates whether this
            workstation configuration is currently being
            updated to match its intended state.
        annotations (MutableMapping[str, str]):
            Optional. Client-specified annotations.
        labels (MutableMapping[str, str]):
            Optional.
            `Labels <https://cloud.google.com/workstations/docs/label-resources>`__
            that are applied to the workstation configuration and that
            are also propagated to the underlying Compute Engine
            resources.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when this workstation
            configuration was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when this workstation
            configuration was most recently updated.
        delete_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when this workstation
            configuration was soft-deleted.
        etag (str):
            Optional. Checksum computed by the server.
            May be sent on update and delete requests to
            make sure that the client has an up-to-date
            value before proceeding.
        idle_timeout (google.protobuf.duration_pb2.Duration):
            Optional. Number of seconds to wait before automatically
            stopping a workstation after it last received user traffic.

            A value of ``"0s"`` indicates that Cloud Workstations VMs
            created with this configuration should never time out due to
            idleness. Provide
            `duration <https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#duration>`__
            terminated by ``s`` for seconds—for example, ``"7200s"`` (2
            hours). The default is ``"1200s"`` (20 minutes).
        running_timeout (google.protobuf.duration_pb2.Duration):
            Optional. Number of seconds that a workstation can run until
            it is automatically shut down. We recommend that
            workstations be shut down daily to reduce costs and so that
            security updates can be applied upon restart. The
            [idle_timeout][google.cloud.workstations.v1beta.WorkstationConfig.idle_timeout]
            and
            [running_timeout][google.cloud.workstations.v1beta.WorkstationConfig.running_timeout]
            fields are independent of each other. Note that the
            [running_timeout][google.cloud.workstations.v1beta.WorkstationConfig.running_timeout]
            field shuts down VMs after the specified time, regardless of
            whether or not the VMs are idle.

            Provide duration terminated by ``s`` for seconds—for
            example, ``"54000s"`` (15 hours). Defaults to ``"43200s"``
            (12 hours). A value of ``"0s"`` indicates that workstations
            using this configuration should never time out. If
            [encryption_key][google.cloud.workstations.v1beta.WorkstationConfig.encryption_key]
            is set, it must be greater than ``"0s"`` and less than
            ``"86400s"`` (24 hours).

            Warning: A value of ``"0s"`` indicates that Cloud
            Workstations VMs created with this configuration have no
            maximum running time. This is strongly discouraged because
            you incur costs and will not pick up security updates.
        host (google.cloud.workstations_v1beta.types.WorkstationConfig.Host):
            Optional. Runtime host for the workstation.
        persistent_directories (MutableSequence[google.cloud.workstations_v1beta.types.WorkstationConfig.PersistentDirectory]):
            Optional. Directories to persist across
            workstation sessions.
        ephemeral_directories (MutableSequence[google.cloud.workstations_v1beta.types.WorkstationConfig.EphemeralDirectory]):
            Optional. Ephemeral directories which won't
            persist across workstation sessions.
        container (google.cloud.workstations_v1beta.types.WorkstationConfig.Container):
            Optional. Container that runs upon startup
            for each workstation using this workstation
            configuration.
        encryption_key (google.cloud.workstations_v1beta.types.WorkstationConfig.CustomerEncryptionKey):
            Immutable. Encrypts resources of this
            workstation configuration using a
            customer-managed encryption key (CMEK).

            If specified, the boot disk of the Compute
            Engine instance and the persistent disk are
            encrypted using this encryption key. If this
            field is not set, the disks are encrypted using
            a generated key. Customer-managed encryption
            keys do not protect disk metadata.

            If the customer-managed encryption key is
            rotated, when the workstation instance is
            stopped, the system attempts to recreate the
            persistent disk with the new version of the key.
            Be sure to keep older versions of the key until
            the persistent disk is recreated. Otherwise,
            data on the persistent disk might be lost.

            If the encryption key is revoked, the
            workstation session automatically stops within 7
            hours.

            Immutable after the workstation configuration is
            created.
        readiness_checks (MutableSequence[google.cloud.workstations_v1beta.types.WorkstationConfig.ReadinessCheck]):
            Optional. Readiness checks to perform when
            starting a workstation using this workstation
            configuration. Mark a workstation as running
            only after all specified readiness checks return
            200 status codes.
        replica_zones (MutableSequence[str]):
            Optional. Immutable. Specifies the zones used to replicate
            the VM and disk resources within the region. If set, exactly
            two zones within the workstation cluster's region must be
            specified—for example,
            ``['us-central1-a', 'us-central1-f']``. If this field is
            empty, two default zones within the region are used.

            Immutable after the workstation configuration is created.
        degraded (bool):
            Output only. Whether this resource is degraded, in which
            case it may require user action to restore full
            functionality. See also the
            [conditions][google.cloud.workstations.v1beta.WorkstationConfig.conditions]
            field.
        conditions (MutableSequence[google.rpc.status_pb2.Status]):
            Output only. Status conditions describing the
            current resource state.
        enable_audit_agent (bool):
            Optional. Whether to enable Linux ``auditd`` logging on the
            workstation. When enabled, a service account must also be
            specified that has ``logging.buckets.write`` permission on
            the project. Operating system audit logging is distinct from
            `Cloud Audit
            Logs <https://cloud.google.com/workstations/docs/audit-logging>`__.
    """

    class Host(proto.Message):
        r"""Runtime host for a workstation.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            gce_instance (google.cloud.workstations_v1beta.types.WorkstationConfig.Host.GceInstance):
                Specifies a Compute Engine instance as the
                host.

                This field is a member of `oneof`_ ``config``.
        """

        class GceInstance(proto.Message):
            r"""A runtime using a Compute Engine instance.

            Attributes:
                machine_type (str):
                    Optional. The type of machine to use for VM instances—for
                    example, ``"e2-standard-4"``. For more information about
                    machine types that Cloud Workstations supports, see the list
                    of `available machine
                    types <https://cloud.google.com/workstations/docs/available-machine-types>`__.
                service_account (str):
                    Optional. The email address of the service account for Cloud
                    Workstations VMs created with this configuration. When
                    specified, be sure that the service account has
                    ``logginglogEntries.create`` permission on the project so it
                    can write logs out to Cloud Logging. If using a custom
                    container image, the service account must have permissions
                    to pull the specified image.

                    If you as the administrator want to be able to ``ssh`` into
                    the underlying VM, you need to set this value to a service
                    account for which you have the ``iam.serviceAccounts.actAs``
                    permission. Conversely, if you don't want anyone to be able
                    to ``ssh`` into the underlying VM, use a service account
                    where no one has that permission.

                    If not set, VMs run with a service account provided by the
                    Cloud Workstations service, and the image must be publicly
                    accessible.
                service_account_scopes (MutableSequence[str]):
                    Optional. Scopes to grant to the
                    [service_account][google.cloud.workstations.v1beta.WorkstationConfig.Host.GceInstance.service_account].
                    Various scopes are automatically added based on feature
                    usage. When specified, users of workstations under this
                    configuration must have ``iam.serviceAccounts.actAs`` on the
                    service account.
                tags (MutableSequence[str]):
                    Optional. Network tags to add to the Compute Engine VMs
                    backing the workstations. This option applies `network
                    tags <https://cloud.google.com/vpc/docs/add-remove-network-tags>`__
                    to VMs created with this configuration. These network tags
                    enable the creation of `firewall
                    rules <https://cloud.google.com/workstations/docs/configure-firewall-rules>`__.
                pool_size (int):
                    Optional. The number of VMs that the system should keep idle
                    so that new workstations can be started quickly for new
                    users. Defaults to ``0`` in the API.
                pooled_instances (int):
                    Output only. Number of instances currently
                    available in the pool for faster workstation
                    startup.
                disable_public_ip_addresses (bool):
                    Optional. When set to true, disables public IP addresses for
                    VMs. If you disable public IP addresses, you must set up
                    Private Google Access or Cloud NAT on your network. If you
                    use Private Google Access and you use
                    ``private.googleapis.com`` or ``restricted.googleapis.com``
                    for Container Registry and Artifact Registry, make sure that
                    you set up DNS records for domains ``*.gcr.io`` and
                    ``*.pkg.dev``. Defaults to false (VMs have public IP
                    addresses).
                enable_nested_virtualization (bool):
                    Optional. Whether to enable nested virtualization on Cloud
                    Workstations VMs created under this workstation
                    configuration.

                    Nested virtualization lets you run virtual machine (VM)
                    instances inside your workstation. Before enabling nested
                    virtualization, consider the following important
                    considerations. Cloud Workstations instances are subject to
                    the `same restrictions as Compute Engine
                    instances <https://cloud.google.com/compute/docs/instances/nested-virtualization/overview#restrictions>`__:

                    -  **Organization policy**: projects, folders, or
                       organizations may be restricted from creating nested VMs
                       if the **Disable VM nested virtualization** constraint is
                       enforced in the organization policy. For more
                       information, see the Compute Engine section, `Checking
                       whether nested virtualization is
                       allowed <https://cloud.google.com/compute/docs/instances/nested-virtualization/managing-constraint#checking_whether_nested_virtualization_is_allowed>`__.
                    -  **Performance**: nested VMs might experience a 10% or
                       greater decrease in performance for workloads that are
                       CPU-bound and possibly greater than a 10% decrease for
                       workloads that are input/output bound.
                    -  **Machine Type**: nested virtualization can only be
                       enabled on workstation configurations that specify a
                       [machine_type][google.cloud.workstations.v1beta.WorkstationConfig.Host.GceInstance.machine_type]
                       in the N1 or N2 machine series.
                    -  **GPUs**: nested virtualization may not be enabled on
                       workstation configurations with accelerators.
                    -  **Operating System**: Because `Container-Optimized
                       OS <https://cloud.google.com/compute/docs/images/os-details#container-optimized_os_cos>`__
                       does not support nested virtualization, when nested
                       virtualization is enabled, the underlying Compute Engine
                       VM instances boot from an `Ubuntu
                       LTS <https://cloud.google.com/compute/docs/images/os-details#ubuntu_lts>`__
                       image.
                shielded_instance_config (google.cloud.workstations_v1beta.types.WorkstationConfig.Host.GceInstance.GceShieldedInstanceConfig):
                    Optional. A set of Compute Engine Shielded
                    instance options.
                confidential_instance_config (google.cloud.workstations_v1beta.types.WorkstationConfig.Host.GceInstance.GceConfidentialInstanceConfig):
                    Optional. A set of Compute Engine
                    Confidential VM instance options.
                boot_disk_size_gb (int):
                    Optional. The size of the boot disk for the VM in gigabytes
                    (GB). The minimum boot disk size is ``30`` GB. Defaults to
                    ``50`` GB.
                accelerators (MutableSequence[google.cloud.workstations_v1beta.types.WorkstationConfig.Host.GceInstance.Accelerator]):
                    Optional. A list of the type and count of
                    accelerator cards attached to the instance.
            """

            class GceShieldedInstanceConfig(proto.Message):
                r"""A set of Compute Engine Shielded instance options.

                Attributes:
                    enable_secure_boot (bool):
                        Optional. Whether the instance has Secure
                        Boot enabled.
                    enable_vtpm (bool):
                        Optional. Whether the instance has the vTPM
                        enabled.
                    enable_integrity_monitoring (bool):
                        Optional. Whether the instance has integrity
                        monitoring enabled.
                """

                enable_secure_boot: bool = proto.Field(
                    proto.BOOL,
                    number=1,
                )
                enable_vtpm: bool = proto.Field(
                    proto.BOOL,
                    number=2,
                )
                enable_integrity_monitoring: bool = proto.Field(
                    proto.BOOL,
                    number=3,
                )

            class GceConfidentialInstanceConfig(proto.Message):
                r"""A set of Compute Engine Confidential VM instance options.

                Attributes:
                    enable_confidential_compute (bool):
                        Optional. Whether the instance has
                        confidential compute enabled.
                """

                enable_confidential_compute: bool = proto.Field(
                    proto.BOOL,
                    number=1,
                )

            class Accelerator(proto.Message):
                r"""An accelerator card attached to the instance.

                Attributes:
                    type_ (str):
                        Optional. Type of accelerator resource to attach to the
                        instance, for example, ``"nvidia-tesla-p100"``.
                    count (int):
                        Optional. Number of accelerator cards exposed
                        to the instance.
                """

                type_: str = proto.Field(
                    proto.STRING,
                    number=1,
                )
                count: int = proto.Field(
                    proto.INT32,
                    number=2,
                )

            machine_type: str = proto.Field(
                proto.STRING,
                number=1,
            )
            service_account: str = proto.Field(
                proto.STRING,
                number=2,
            )
            service_account_scopes: MutableSequence[str] = proto.RepeatedField(
                proto.STRING,
                number=3,
            )
            tags: MutableSequence[str] = proto.RepeatedField(
                proto.STRING,
                number=4,
            )
            pool_size: int = proto.Field(
                proto.INT32,
                number=5,
            )
            pooled_instances: int = proto.Field(
                proto.INT32,
                number=12,
            )
            disable_public_ip_addresses: bool = proto.Field(
                proto.BOOL,
                number=6,
            )
            enable_nested_virtualization: bool = proto.Field(
                proto.BOOL,
                number=7,
            )
            shielded_instance_config: "WorkstationConfig.Host.GceInstance.GceShieldedInstanceConfig" = proto.Field(
                proto.MESSAGE,
                number=8,
                message="WorkstationConfig.Host.GceInstance.GceShieldedInstanceConfig",
            )
            confidential_instance_config: "WorkstationConfig.Host.GceInstance.GceConfidentialInstanceConfig" = proto.Field(
                proto.MESSAGE,
                number=10,
                message="WorkstationConfig.Host.GceInstance.GceConfidentialInstanceConfig",
            )
            boot_disk_size_gb: int = proto.Field(
                proto.INT32,
                number=9,
            )
            accelerators: MutableSequence[
                "WorkstationConfig.Host.GceInstance.Accelerator"
            ] = proto.RepeatedField(
                proto.MESSAGE,
                number=11,
                message="WorkstationConfig.Host.GceInstance.Accelerator",
            )

        gce_instance: "WorkstationConfig.Host.GceInstance" = proto.Field(
            proto.MESSAGE,
            number=1,
            oneof="config",
            message="WorkstationConfig.Host.GceInstance",
        )

    class PersistentDirectory(proto.Message):
        r"""A directory to persist across workstation sessions.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            gce_pd (google.cloud.workstations_v1beta.types.WorkstationConfig.PersistentDirectory.GceRegionalPersistentDisk):
                A PersistentDirectory backed by a Compute
                Engine persistent disk.

                This field is a member of `oneof`_ ``directory_type``.
            mount_path (str):
                Optional. Location of this directory in the
                running workstation.
        """

        class GceRegionalPersistentDisk(proto.Message):
            r"""A PersistentDirectory backed by a Compute Engine regional persistent
            disk. The
            [persistent_directories][google.cloud.workstations.v1beta.WorkstationConfig.persistent_directories]
            field is repeated, but it may contain only one entry. It creates a
            `persistent
            disk <https://cloud.google.com/compute/docs/disks/persistent-disks>`__
            that mounts to the workstation VM at ``/home`` when the session
            starts and detaches when the session ends. If this field is empty,
            workstations created with this configuration do not have a
            persistent home directory.

            Attributes:
                size_gb (int):
                    Optional. The GB capacity of a persistent home directory for
                    each workstation created with this configuration. Must be
                    empty if
                    [source_snapshot][google.cloud.workstations.v1beta.WorkstationConfig.PersistentDirectory.GceRegionalPersistentDisk.source_snapshot]
                    is set.

                    Valid values are ``10``, ``50``, ``100``, ``200``, ``500``,
                    or ``1000``. Defaults to ``200``. If less than ``200`` GB,
                    the
                    [disk_type][google.cloud.workstations.v1beta.WorkstationConfig.PersistentDirectory.GceRegionalPersistentDisk.disk_type]
                    must be ``"pd-balanced"`` or ``"pd-ssd"``.
                fs_type (str):
                    Optional. Type of file system that the disk should be
                    formatted with. The workstation image must support this file
                    system type. Must be empty if
                    [source_snapshot][google.cloud.workstations.v1beta.WorkstationConfig.PersistentDirectory.GceRegionalPersistentDisk.source_snapshot]
                    is set. Defaults to ``"ext4"``.
                disk_type (str):
                    Optional. The `type of the persistent
                    disk <https://cloud.google.com/compute/docs/disks#disk-types>`__
                    for the home directory. Defaults to ``"pd-standard"``.
                source_snapshot (str):
                    Optional. Name of the snapshot to use as the source for the
                    disk. If set,
                    [size_gb][google.cloud.workstations.v1beta.WorkstationConfig.PersistentDirectory.GceRegionalPersistentDisk.size_gb]
                    and
                    [fs_type][google.cloud.workstations.v1beta.WorkstationConfig.PersistentDirectory.GceRegionalPersistentDisk.fs_type]
                    must be empty.
                reclaim_policy (google.cloud.workstations_v1beta.types.WorkstationConfig.PersistentDirectory.GceRegionalPersistentDisk.ReclaimPolicy):
                    Optional. Whether the persistent disk should be deleted when
                    the workstation is deleted. Valid values are ``DELETE`` and
                    ``RETAIN``. Defaults to ``DELETE``.
            """

            class ReclaimPolicy(proto.Enum):
                r"""Value representing what should happen to the disk after the
                workstation is deleted.

                Values:
                    RECLAIM_POLICY_UNSPECIFIED (0):
                        Do not use.
                    DELETE (1):
                        Delete the persistent disk when deleting the
                        workstation.
                    RETAIN (2):
                        Keep the persistent disk when deleting the
                        workstation. An administrator must manually
                        delete the disk.
                """
                RECLAIM_POLICY_UNSPECIFIED = 0
                DELETE = 1
                RETAIN = 2

            size_gb: int = proto.Field(
                proto.INT32,
                number=1,
            )
            fs_type: str = proto.Field(
                proto.STRING,
                number=2,
            )
            disk_type: str = proto.Field(
                proto.STRING,
                number=3,
            )
            source_snapshot: str = proto.Field(
                proto.STRING,
                number=5,
            )
            reclaim_policy: "WorkstationConfig.PersistentDirectory.GceRegionalPersistentDisk.ReclaimPolicy" = proto.Field(
                proto.ENUM,
                number=4,
                enum="WorkstationConfig.PersistentDirectory.GceRegionalPersistentDisk.ReclaimPolicy",
            )

        gce_pd: "WorkstationConfig.PersistentDirectory.GceRegionalPersistentDisk" = proto.Field(
            proto.MESSAGE,
            number=2,
            oneof="directory_type",
            message="WorkstationConfig.PersistentDirectory.GceRegionalPersistentDisk",
        )
        mount_path: str = proto.Field(
            proto.STRING,
            number=1,
        )

    class EphemeralDirectory(proto.Message):
        r"""An ephemeral directory which won't persist across workstation
        sessions. It is freshly created on every workstation start
        operation.


        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            gce_pd (google.cloud.workstations_v1beta.types.WorkstationConfig.EphemeralDirectory.GcePersistentDisk):
                An EphemeralDirectory backed by a Compute
                Engine persistent disk.

                This field is a member of `oneof`_ ``directory_type``.
            mount_path (str):
                Required. Location of this directory in the
                running workstation.
        """

        class GcePersistentDisk(proto.Message):
            r"""An EphemeralDirectory is backed by a Compute Engine
            persistent disk.

            Attributes:
                disk_type (str):
                    Optional. Type of the disk to use. Defaults to
                    ``"pd-standard"``.
                source_snapshot (str):
                    Optional. Name of the snapshot to use as the source for the
                    disk. Must be empty if
                    [source_image][google.cloud.workstations.v1beta.WorkstationConfig.EphemeralDirectory.GcePersistentDisk.source_image]
                    is set. Updating
                    [source_snapshot][google.cloud.workstations.v1beta.WorkstationConfig.EphemeralDirectory.GcePersistentDisk.source_snapshot]
                    will update content in the ephemeral directory after the
                    workstation is restarted. This field is mutable.
                source_image (str):
                    Optional. Name of the disk image to use as the source for
                    the disk. Must be empty if
                    [source_snapshot][google.cloud.workstations.v1beta.WorkstationConfig.EphemeralDirectory.GcePersistentDisk.source_snapshot]
                    is set. Updating
                    [source_image][google.cloud.workstations.v1beta.WorkstationConfig.EphemeralDirectory.GcePersistentDisk.source_image]
                    will update content in the ephemeral directory after the
                    workstation is restarted. This field is mutable.
                read_only (bool):
                    Optional. Whether the disk is read only. If true, the disk
                    may be shared by multiple VMs and
                    [source_snapshot][google.cloud.workstations.v1beta.WorkstationConfig.EphemeralDirectory.GcePersistentDisk.source_snapshot]
                    must be set.
            """

            disk_type: str = proto.Field(
                proto.STRING,
                number=1,
            )
            source_snapshot: str = proto.Field(
                proto.STRING,
                number=2,
            )
            source_image: str = proto.Field(
                proto.STRING,
                number=3,
            )
            read_only: bool = proto.Field(
                proto.BOOL,
                number=4,
            )

        gce_pd: "WorkstationConfig.EphemeralDirectory.GcePersistentDisk" = proto.Field(
            proto.MESSAGE,
            number=3,
            oneof="directory_type",
            message="WorkstationConfig.EphemeralDirectory.GcePersistentDisk",
        )
        mount_path: str = proto.Field(
            proto.STRING,
            number=1,
        )

    class Container(proto.Message):
        r"""A Docker container.

        Attributes:
            image (str):
                Optional. A Docker container image that defines a custom
                environment.

                Cloud Workstations provides a number of `preconfigured
                images <https://cloud.google.com/workstations/docs/preconfigured-base-images>`__,
                but you can create your own `custom container
                images <https://cloud.google.com/workstations/docs/custom-container-images>`__.
                If using a private image, the
                ``host.gceInstance.serviceAccount`` field must be specified
                in the workstation configuration and must have permission to
                pull the specified image. Otherwise, the image must be
                publicly accessible.
            command (MutableSequence[str]):
                Optional. If set, overrides the default
                ENTRYPOINT specified by the image.
            args (MutableSequence[str]):
                Optional. Arguments passed to the entrypoint.
            env (MutableMapping[str, str]):
                Optional. Environment variables passed to the
                container's entrypoint.
            working_dir (str):
                Optional. If set, overrides the default DIR
                specified by the image.
            run_as_user (int):
                Optional. If set, overrides the USER
                specified in the image with the given uid.
        """

        image: str = proto.Field(
            proto.STRING,
            number=1,
        )
        command: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=2,
        )
        args: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=3,
        )
        env: MutableMapping[str, str] = proto.MapField(
            proto.STRING,
            proto.STRING,
            number=4,
        )
        working_dir: str = proto.Field(
            proto.STRING,
            number=5,
        )
        run_as_user: int = proto.Field(
            proto.INT32,
            number=6,
        )

    class CustomerEncryptionKey(proto.Message):
        r"""A customer-managed encryption key (CMEK) for the Compute Engine
        resources of the associated workstation configuration. Specify the
        name of your Cloud KMS encryption key and the default service
        account. We recommend that you use a separate service account and
        follow `Cloud KMS best
        practices <https://cloud.google.com/kms/docs/separation-of-duties>`__.

        Attributes:
            kms_key (str):
                Immutable. The name of the Google Cloud KMS encryption key.
                For example,
                ``"projects/PROJECT_ID/locations/REGION/keyRings/KEY_RING/cryptoKeys/KEY_NAME"``.
                The key must be in the same region as the workstation
                configuration.
            kms_key_service_account (str):
                Immutable. The service account to use with the specified KMS
                key. We recommend that you use a separate service account
                and follow KMS best practices. For more information, see
                `Separation of
                duties <https://cloud.google.com/kms/docs/separation-of-duties>`__
                and ``gcloud kms keys add-iam-policy-binding``
                ```--member`` <https://cloud.google.com/sdk/gcloud/reference/kms/keys/add-iam-policy-binding#--member>`__.
        """

        kms_key: str = proto.Field(
            proto.STRING,
            number=1,
        )
        kms_key_service_account: str = proto.Field(
            proto.STRING,
            number=2,
        )

    class ReadinessCheck(proto.Message):
        r"""A readiness check to be performed on a workstation.

        Attributes:
            path (str):
                Optional. Path to which the request should be
                sent.
            port (int):
                Optional. Port to which the request should be
                sent.
        """

        path: str = proto.Field(
            proto.STRING,
            number=1,
        )
        port: int = proto.Field(
            proto.INT32,
            number=2,
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=3,
    )
    reconciling: bool = proto.Field(
        proto.BOOL,
        number=4,
    )
    annotations: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=5,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=18,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=7,
        message=timestamp_pb2.Timestamp,
    )
    delete_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=8,
        message=timestamp_pb2.Timestamp,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=9,
    )
    idle_timeout: duration_pb2.Duration = proto.Field(
        proto.MESSAGE,
        number=10,
        message=duration_pb2.Duration,
    )
    running_timeout: duration_pb2.Duration = proto.Field(
        proto.MESSAGE,
        number=11,
        message=duration_pb2.Duration,
    )
    host: Host = proto.Field(
        proto.MESSAGE,
        number=12,
        message=Host,
    )
    persistent_directories: MutableSequence[PersistentDirectory] = proto.RepeatedField(
        proto.MESSAGE,
        number=13,
        message=PersistentDirectory,
    )
    ephemeral_directories: MutableSequence[EphemeralDirectory] = proto.RepeatedField(
        proto.MESSAGE,
        number=22,
        message=EphemeralDirectory,
    )
    container: Container = proto.Field(
        proto.MESSAGE,
        number=14,
        message=Container,
    )
    encryption_key: CustomerEncryptionKey = proto.Field(
        proto.MESSAGE,
        number=17,
        message=CustomerEncryptionKey,
    )
    readiness_checks: MutableSequence[ReadinessCheck] = proto.RepeatedField(
        proto.MESSAGE,
        number=19,
        message=ReadinessCheck,
    )
    replica_zones: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=23,
    )
    degraded: bool = proto.Field(
        proto.BOOL,
        number=15,
    )
    conditions: MutableSequence[status_pb2.Status] = proto.RepeatedField(
        proto.MESSAGE,
        number=16,
        message=status_pb2.Status,
    )
    enable_audit_agent: bool = proto.Field(
        proto.BOOL,
        number=20,
    )


class Workstation(proto.Message):
    r"""A single instance of a developer workstation with its own
    persistent storage.

    Attributes:
        name (str):
            Full name of this workstation.
        display_name (str):
            Optional. Human-readable name for this
            workstation.
        uid (str):
            Output only. A system-assigned unique
            identifier for this workstation.
        reconciling (bool):
            Output only. Indicates whether this
            workstation is currently being updated to match
            its intended state.
        annotations (MutableMapping[str, str]):
            Optional. Client-specified annotations.
        labels (MutableMapping[str, str]):
            Optional.
            `Labels <https://cloud.google.com/workstations/docs/label-resources>`__
            that are applied to the workstation and that are also
            propagated to the underlying Compute Engine resources.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when this workstation was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when this workstation was
            most recently updated.
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when this workstation was
            most recently successfully started, regardless
            of the workstation's initial state.
        delete_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when this workstation was
            soft-deleted.
        etag (str):
            Optional. Checksum computed by the server.
            May be sent on update and delete requests to
            make sure that the client has an up-to-date
            value before proceeding.
        state (google.cloud.workstations_v1beta.types.Workstation.State):
            Output only. Current state of the
            workstation.
        host (str):
            Output only. Host to which clients can send HTTPS traffic
            that will be received by the workstation. Authorized traffic
            will be received to the workstation as HTTP on port 80. To
            send traffic to a different port, clients may prefix the
            host with the destination port in the format
            ``{port}-{host}``.
        env (MutableMapping[str, str]):
            Optional. Environment variables passed to the
            workstation container's entrypoint.
    """

    class State(proto.Enum):
        r"""Whether a workstation is running and ready to receive user
        requests.

        Values:
            STATE_UNSPECIFIED (0):
                Do not use.
            STATE_STARTING (1):
                The workstation is not yet ready to accept
                requests from users but will be soon.
            STATE_RUNNING (2):
                The workstation is ready to accept requests
                from users.
            STATE_STOPPING (3):
                The workstation is being stopped.
            STATE_STOPPED (4):
                The workstation is stopped and will not be
                able to receive requests until it is started.
        """
        STATE_UNSPECIFIED = 0
        STATE_STARTING = 1
        STATE_RUNNING = 2
        STATE_STOPPING = 3
        STATE_STOPPED = 4

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=3,
    )
    reconciling: bool = proto.Field(
        proto.BOOL,
        number=4,
    )
    annotations: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=5,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=13,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=7,
        message=timestamp_pb2.Timestamp,
    )
    start_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=14,
        message=timestamp_pb2.Timestamp,
    )
    delete_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=8,
        message=timestamp_pb2.Timestamp,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=9,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=10,
        enum=State,
    )
    host: str = proto.Field(
        proto.STRING,
        number=11,
    )
    env: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=12,
    )


class GetWorkstationClusterRequest(proto.Message):
    r"""Request message for GetWorkstationCluster.

    Attributes:
        name (str):
            Required. Name of the requested resource.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListWorkstationClustersRequest(proto.Message):
    r"""Request message for ListWorkstationClusters.

    Attributes:
        parent (str):
            Required. Parent resource name.
        page_size (int):
            Optional. Maximum number of items to return.
        page_token (str):
            Optional. next_page_token value returned from a previous
            List request, if any.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ListWorkstationClustersResponse(proto.Message):
    r"""Response message for ListWorkstationClusters.

    Attributes:
        workstation_clusters (MutableSequence[google.cloud.workstations_v1beta.types.WorkstationCluster]):
            The requested workstation clusters.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
        unreachable (MutableSequence[str]):
            Unreachable resources.
    """

    @property
    def raw_page(self):
        return self

    workstation_clusters: MutableSequence["WorkstationCluster"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="WorkstationCluster",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class CreateWorkstationClusterRequest(proto.Message):
    r"""Message for creating a CreateWorkstationCluster.

    Attributes:
        parent (str):
            Required. Parent resource name.
        workstation_cluster_id (str):
            Required. ID to use for the workstation
            cluster.
        workstation_cluster (google.cloud.workstations_v1beta.types.WorkstationCluster):
            Required. Workstation cluster to create.
        validate_only (bool):
            Optional. If set, validate the request and
            preview the review, but do not actually apply
            it.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    workstation_cluster_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    workstation_cluster: "WorkstationCluster" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="WorkstationCluster",
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=4,
    )


class UpdateWorkstationClusterRequest(proto.Message):
    r"""Request message for UpdateWorkstationCluster.

    Attributes:
        workstation_cluster (google.cloud.workstations_v1beta.types.WorkstationCluster):
            Required. Workstation cluster to update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Mask that specifies which fields in
            the workstation cluster should be updated.
        validate_only (bool):
            Optional. If set, validate the request and
            preview the review, but do not actually apply
            it.
        allow_missing (bool):
            Optional. If set, and the workstation cluster is not found,
            a new workstation cluster will be created. In this
            situation, update_mask is ignored.
    """

    workstation_cluster: "WorkstationCluster" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="WorkstationCluster",
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=3,
    )
    allow_missing: bool = proto.Field(
        proto.BOOL,
        number=4,
    )


class DeleteWorkstationClusterRequest(proto.Message):
    r"""Message for deleting a workstation cluster.

    Attributes:
        name (str):
            Required. Name of the workstation cluster to
            delete.
        validate_only (bool):
            Optional. If set, validate the request and
            preview the review, but do not apply it.
        etag (str):
            Optional. If set, the request will be
            rejected if the latest version of the
            workstation cluster on the server does not have
            this ETag.
        force (bool):
            Optional. If set, any workstation
            configurations and workstations in the
            workstation cluster are also deleted. Otherwise,
            the request only works if the workstation
            cluster has no configurations or workstations.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=2,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=3,
    )
    force: bool = proto.Field(
        proto.BOOL,
        number=4,
    )


class GetWorkstationConfigRequest(proto.Message):
    r"""Request message for GetWorkstationConfig.

    Attributes:
        name (str):
            Required. Name of the requested resource.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListWorkstationConfigsRequest(proto.Message):
    r"""Request message for ListWorkstationConfigs.

    Attributes:
        parent (str):
            Required. Parent resource name.
        page_size (int):
            Optional. Maximum number of items to return.
        page_token (str):
            Optional. next_page_token value returned from a previous
            List request, if any.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ListWorkstationConfigsResponse(proto.Message):
    r"""Response message for ListWorkstationConfigs.

    Attributes:
        workstation_configs (MutableSequence[google.cloud.workstations_v1beta.types.WorkstationConfig]):
            The requested configs.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
        unreachable (MutableSequence[str]):
            Unreachable resources.
    """

    @property
    def raw_page(self):
        return self

    workstation_configs: MutableSequence["WorkstationConfig"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="WorkstationConfig",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class ListUsableWorkstationConfigsRequest(proto.Message):
    r"""Request message for ListUsableWorkstationConfigs.

    Attributes:
        parent (str):
            Required. Parent resource name.
        page_size (int):
            Optional. Maximum number of items to return.
        page_token (str):
            Optional. next_page_token value returned from a previous
            List request, if any.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ListUsableWorkstationConfigsResponse(proto.Message):
    r"""Response message for ListUsableWorkstationConfigs.

    Attributes:
        workstation_configs (MutableSequence[google.cloud.workstations_v1beta.types.WorkstationConfig]):
            The requested configs.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
        unreachable (MutableSequence[str]):
            Unreachable resources.
    """

    @property
    def raw_page(self):
        return self

    workstation_configs: MutableSequence["WorkstationConfig"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="WorkstationConfig",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class CreateWorkstationConfigRequest(proto.Message):
    r"""Message for creating a CreateWorkstationConfig.

    Attributes:
        parent (str):
            Required. Parent resource name.
        workstation_config_id (str):
            Required. ID to use for the workstation
            configuration.
        workstation_config (google.cloud.workstations_v1beta.types.WorkstationConfig):
            Required. Config to create.
        validate_only (bool):
            Optional. If set, validate the request and
            preview the review, but do not actually apply
            it.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    workstation_config_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    workstation_config: "WorkstationConfig" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="WorkstationConfig",
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=4,
    )


class UpdateWorkstationConfigRequest(proto.Message):
    r"""Request message for UpdateWorkstationConfig.

    Attributes:
        workstation_config (google.cloud.workstations_v1beta.types.WorkstationConfig):
            Required. Config to update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Mask specifying which fields in the
            workstation configuration should be updated.
        validate_only (bool):
            Optional. If set, validate the request and
            preview the review, but do not actually apply
            it.
        allow_missing (bool):
            Optional. If set and the workstation configuration is not
            found, a new workstation configuration will be created. In
            this situation, update_mask is ignored.
    """

    workstation_config: "WorkstationConfig" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="WorkstationConfig",
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=3,
    )
    allow_missing: bool = proto.Field(
        proto.BOOL,
        number=4,
    )


class DeleteWorkstationConfigRequest(proto.Message):
    r"""Message for deleting a workstation configuration.

    Attributes:
        name (str):
            Required. Name of the workstation
            configuration to delete.
        validate_only (bool):
            Optional. If set, validate the request and
            preview the review, but do not actually apply
            it.
        etag (str):
            Optional. If set, the request is rejected if
            the latest version of the workstation
            configuration on the server does not have this
            ETag.
        force (bool):
            Optional. If set, any workstations in the
            workstation configuration are also deleted.
            Otherwise, the request works only if the
            workstation configuration has no workstations.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=2,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=3,
    )
    force: bool = proto.Field(
        proto.BOOL,
        number=4,
    )


class GetWorkstationRequest(proto.Message):
    r"""Request message for GetWorkstation.

    Attributes:
        name (str):
            Required. Name of the requested resource.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListWorkstationsRequest(proto.Message):
    r"""Request message for ListWorkstations.

    Attributes:
        parent (str):
            Required. Parent resource name.
        page_size (int):
            Optional. Maximum number of items to return.
        page_token (str):
            Optional. next_page_token value returned from a previous
            List request, if any.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ListWorkstationsResponse(proto.Message):
    r"""Response message for ListWorkstations.

    Attributes:
        workstations (MutableSequence[google.cloud.workstations_v1beta.types.Workstation]):
            The requested workstations.
        next_page_token (str):
            Optional. Token to retrieve the next page of
            results, or empty if there are no more results
            in the list.
        unreachable (MutableSequence[str]):
            Optional. Unreachable resources.
    """

    @property
    def raw_page(self):
        return self

    workstations: MutableSequence["Workstation"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Workstation",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class ListUsableWorkstationsRequest(proto.Message):
    r"""Request message for ListUsableWorkstations.

    Attributes:
        parent (str):
            Required. Parent resource name.
        page_size (int):
            Optional. Maximum number of items to return.
        page_token (str):
            Optional. next_page_token value returned from a previous
            List request, if any.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ListUsableWorkstationsResponse(proto.Message):
    r"""Response message for ListUsableWorkstations.

    Attributes:
        workstations (MutableSequence[google.cloud.workstations_v1beta.types.Workstation]):
            The requested workstations.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
        unreachable (MutableSequence[str]):
            Unreachable resources.
    """

    @property
    def raw_page(self):
        return self

    workstations: MutableSequence["Workstation"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Workstation",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class CreateWorkstationRequest(proto.Message):
    r"""Message for creating a CreateWorkstation.

    Attributes:
        parent (str):
            Required. Parent resource name.
        workstation_id (str):
            Required. ID to use for the workstation.
        workstation (google.cloud.workstations_v1beta.types.Workstation):
            Required. Workstation to create.
        validate_only (bool):
            Optional. If set, validate the request and
            preview the review, but do not actually apply
            it.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    workstation_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    workstation: "Workstation" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Workstation",
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=4,
    )


class UpdateWorkstationRequest(proto.Message):
    r"""Request message for UpdateWorkstation.

    Attributes:
        workstation (google.cloud.workstations_v1beta.types.Workstation):
            Required. Workstation to update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Mask specifying which fields in the
            workstation configuration should be updated.
        validate_only (bool):
            Optional. If set, validate the request and
            preview the review, but do not actually apply
            it.
        allow_missing (bool):
            Optional. If set and the workstation configuration is not
            found, a new workstation configuration is created. In this
            situation, update_mask is ignored.
    """

    workstation: "Workstation" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="Workstation",
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=3,
    )
    allow_missing: bool = proto.Field(
        proto.BOOL,
        number=4,
    )


class DeleteWorkstationRequest(proto.Message):
    r"""Request message for DeleteWorkstation.

    Attributes:
        name (str):
            Required. Name of the workstation to delete.
        validate_only (bool):
            Optional. If set, validate the request and
            preview the review, but do not actually apply
            it.
        etag (str):
            Optional. If set, the request will be
            rejected if the latest version of the
            workstation on the server does not have this
            ETag.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=2,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=3,
    )


class StartWorkstationRequest(proto.Message):
    r"""Request message for StartWorkstation.

    Attributes:
        name (str):
            Required. Name of the workstation to start.
        validate_only (bool):
            Optional. If set, validate the request and
            preview the review, but do not actually apply
            it.
        etag (str):
            Optional. If set, the request will be
            rejected if the latest version of the
            workstation on the server does not have this
            ETag.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=2,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=3,
    )


class StopWorkstationRequest(proto.Message):
    r"""Request message for StopWorkstation.

    Attributes:
        name (str):
            Required. Name of the workstation to stop.
        validate_only (bool):
            Optional. If set, validate the request and
            preview the review, but do not actually apply
            it.
        etag (str):
            Optional. If set, the request will be
            rejected if the latest version of the
            workstation on the server does not have this
            ETag.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=2,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=3,
    )


class GenerateAccessTokenRequest(proto.Message):
    r"""Request message for GenerateAccessToken.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        expire_time (google.protobuf.timestamp_pb2.Timestamp):
            Desired expiration time of the access token.
            This value must be at most 24 hours in the
            future. If a value is not specified, the token's
            expiration time will be set to a default value
            of 1 hour in the future.

            This field is a member of `oneof`_ ``expiration``.
        ttl (google.protobuf.duration_pb2.Duration):
            Desired lifetime duration of the access
            token. This value must be at most 24 hours. If a
            value is not specified, the token's lifetime
            will be set to a default value of 1 hour.

            This field is a member of `oneof`_ ``expiration``.
        workstation (str):
            Required. Name of the workstation for which
            the access token should be generated.
    """

    expire_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="expiration",
        message=timestamp_pb2.Timestamp,
    )
    ttl: duration_pb2.Duration = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="expiration",
        message=duration_pb2.Duration,
    )
    workstation: str = proto.Field(
        proto.STRING,
        number=1,
    )


class GenerateAccessTokenResponse(proto.Message):
    r"""Response message for GenerateAccessToken.

    Attributes:
        access_token (str):
            The generated bearer access token. To use this token,
            include it in an Authorization header of an HTTP request
            sent to the associated workstation's hostname—for example,
            ``Authorization: Bearer <access_token>``.
        expire_time (google.protobuf.timestamp_pb2.Timestamp):
            Time at which the generated token will
            expire.
    """

    access_token: str = proto.Field(
        proto.STRING,
        number=1,
    )
    expire_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )


class OperationMetadata(proto.Message):
    r"""Metadata for long-running operations.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time that the operation was
            created.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time that the operation finished
            running.
        target (str):
            Output only. Server-defined resource path for
            the target of the operation.
        verb (str):
            Output only. Name of the verb executed by the
            operation.
        status_message (str):
            Output only. Human-readable status of the
            operation, if any.
        requested_cancellation (bool):
            Output only. Identifies whether the user has
            requested cancellation of the operation.
        api_version (str):
            Output only. API version used to start the
            operation.
    """

    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    end_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    target: str = proto.Field(
        proto.STRING,
        number=3,
    )
    verb: str = proto.Field(
        proto.STRING,
        number=4,
    )
    status_message: str = proto.Field(
        proto.STRING,
        number=5,
    )
    requested_cancellation: bool = proto.Field(
        proto.BOOL,
        number=6,
    )
    api_version: str = proto.Field(
        proto.STRING,
        number=7,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
