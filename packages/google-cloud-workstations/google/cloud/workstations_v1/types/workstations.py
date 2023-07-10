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

from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.workstations.v1",
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
    r"""A grouping of workstation configurations and the associated
    workstations  in that region.

    Attributes:
        name (str):
            Full name of this resource.
        display_name (str):
            Human-readable name for this resource.
        uid (str):
            Output only. A system-assigned unique
            identified for this resource.
        reconciling (bool):
            Output only. Indicates whether this resource
            is currently being updated to match its intended
            state.
        annotations (MutableMapping[str, str]):
            Client-specified annotations.
        labels (MutableMapping[str, str]):
            Client-specified labels that are applied to
            the resource and that are also propagated to the
            underlying Compute Engine resources.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when this resource was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when this resource was most
            recently updated.
        delete_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when this resource was
            soft-deleted.
        etag (str):
            Checksum computed by the server. May be sent
            on update and delete requests to make sure that
            the client has an up-to-date value before
            proceeding.
        network (str):
            Immutable. Name of the Compute Engine network
            in which instances associated with this cluster
            will be created.
        subnetwork (str):
            Immutable. Name of the Compute Engine
            subnetwork in which instances associated with
            this cluster will be created. Must be part of
            the subnetwork specified for this cluster.
        control_plane_ip (str):
            Output only. The private IP address of the
            control plane for this cluster. Workstation VMs
            need access to this IP address to work with the
            service, so make sure that your firewall rules
            allow egress from the workstation VMs to this
            address.
        private_cluster_config (google.cloud.workstations_v1.types.WorkstationCluster.PrivateClusterConfig):
            Configuration for private cluster.
        degraded (bool):
            Output only. Whether this resource is in degraded mode, in
            which case it may require user action to restore full
            functionality. Details can be found in the ``conditions``
            field.
        conditions (MutableSequence[google.rpc.status_pb2.Status]):
            Output only. Status conditions describing the
            current resource state.
    """

    class PrivateClusterConfig(proto.Message):
        r"""Configuration options for private clusters.

        Attributes:
            enable_private_endpoint (bool):
                Immutable. Whether Workstations endpoint is
                private.
            cluster_hostname (str):
                Output only. Hostname for the workstation
                cluster. This field will be populated only when
                private endpoint is enabled. To access
                workstations in the cluster, create a new DNS
                zone mapping this domain name to an internal IP
                address and a forwarding rule mapping that
                address to the service attachment.
            service_attachment_uri (str):
                Output only. Service attachment URI for the workstation
                cluster. The service attachemnt is created when private
                endpoint is enabled. To access workstations in the cluster,
                configure access to the managed service using `Private
                Service
                Connect <https://cloud.google.com/vpc/docs/configure-private-service-connect-services>`__.
            allowed_projects (MutableSequence[str]):
                Additional projects that are allowed to
                attach to the workstation cluster's service
                attachment. By default, the workstation
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
    r"""A set of configuration options describing how a workstation
    will be run. Workstation configurations are intended to be
    shared across multiple workstations.

    Attributes:
        name (str):
            Full name of this resource.
        display_name (str):
            Human-readable name for this resource.
        uid (str):
            Output only. A system-assigned unique
            identified for this resource.
        reconciling (bool):
            Output only. Indicates whether this resource
            is currently being updated to match its intended
            state.
        annotations (MutableMapping[str, str]):
            Client-specified annotations.
        labels (MutableMapping[str, str]):
            Client-specified labels that are applied to
            the resource and that are also propagated to the
            underlying Compute Engine resources.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when this resource was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when this resource was most
            recently updated.
        delete_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when this resource was
            soft-deleted.
        etag (str):
            Checksum computed by the server. May be sent
            on update and delete requests to make sure that
            the client has an up-to-date value before
            proceeding.
        idle_timeout (google.protobuf.duration_pb2.Duration):
            How long to wait before automatically
            stopping an instance that hasn't received any
            user traffic. A value of 0 indicates that this
            instance should never time out due to idleness.
            Defaults to 20 minutes.
        running_timeout (google.protobuf.duration_pb2.Duration):
            How long to wait before automatically stopping a workstation
            after it started. A value of 0 indicates that workstations
            using this configuration should never time out. Must be
            greater than 0 and less than 24 hours if encryption_key is
            set. Defaults to 12 hours.
        host (google.cloud.workstations_v1.types.WorkstationConfig.Host):
            Runtime host for the workstation.
        persistent_directories (MutableSequence[google.cloud.workstations_v1.types.WorkstationConfig.PersistentDirectory]):
            Directories to persist across workstation
            sessions.
        container (google.cloud.workstations_v1.types.WorkstationConfig.Container):
            Container that will be run for each
            workstation using this configuration when that
            workstation is started.
        encryption_key (google.cloud.workstations_v1.types.WorkstationConfig.CustomerEncryptionKey):
            Immutable. Encrypts resources of this
            workstation configuration using a
            customer-managed encryption key.
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
            data on the persistent disk will be lost.
            If the encryption key is revoked, the
            workstation session will automatically be
            stopped within 7 hours.

            Immutable after the workstation configuration is
            created.
        degraded (bool):
            Output only. Whether this resource is degraded, in which
            case it may require user action to restore full
            functionality. See also the ``conditions`` field.
        conditions (MutableSequence[google.rpc.status_pb2.Status]):
            Output only. Status conditions describing the
            current resource state.
    """

    class Host(proto.Message):
        r"""Runtime host for a workstation.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            gce_instance (google.cloud.workstations_v1.types.WorkstationConfig.Host.GceInstance):
                Specifies a Compute Engine instance as the
                host.

                This field is a member of `oneof`_ ``config``.
        """

        class GceInstance(proto.Message):
            r"""A runtime using a Compute Engine instance.

            Attributes:
                machine_type (str):
                    The name of a Compute Engine machine type.
                service_account (str):
                    Email address of the service account used on
                    VM instances used to support this configuration.
                    If not set, VMs run with a Google-managed
                    service account. This service account must have
                    permission to pull the specified container
                    image; otherwise, the image must be publicly
                    accessible.
                tags (MutableSequence[str]):
                    Network tags to add to the Compute Engine
                    machines backing the Workstations.
                pool_size (int):
                    Number of instances to pool for faster
                    workstation startup.
                pooled_instances (int):
                    Output only. Number of instances currently
                    available in the pool for faster workstation
                    startup.
                disable_public_ip_addresses (bool):
                    Whether instances have no public IP address.
                enable_nested_virtualization (bool):
                    Whether to enable nested virtualization on
                    instances.
                shielded_instance_config (google.cloud.workstations_v1.types.WorkstationConfig.Host.GceInstance.GceShieldedInstanceConfig):
                    A set of Compute Engine Shielded instance
                    options.
                confidential_instance_config (google.cloud.workstations_v1.types.WorkstationConfig.Host.GceInstance.GceConfidentialInstanceConfig):
                    A set of Compute Engine Confidential VM
                    instance options.
                boot_disk_size_gb (int):
                    Size of the boot disk in GB. Defaults to 50.
            """

            class GceShieldedInstanceConfig(proto.Message):
                r"""A set of Compute Engine Shielded instance options.

                Attributes:
                    enable_secure_boot (bool):
                        Whether the instance has Secure Boot enabled.
                    enable_vtpm (bool):
                        Whether the instance has the vTPM enabled.
                    enable_integrity_monitoring (bool):
                        Whether the instance has integrity monitoring
                        enabled.
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
                        Whether the instance has confidential compute
                        enabled.
                """

                enable_confidential_compute: bool = proto.Field(
                    proto.BOOL,
                    number=1,
                )

            machine_type: str = proto.Field(
                proto.STRING,
                number=1,
            )
            service_account: str = proto.Field(
                proto.STRING,
                number=2,
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
            gce_pd (google.cloud.workstations_v1.types.WorkstationConfig.PersistentDirectory.GceRegionalPersistentDisk):
                A PersistentDirectory backed by a Compute
                Engine persistent disk.

                This field is a member of `oneof`_ ``directory_type``.
            mount_path (str):
                Location of this directory in the running
                workstation.
        """

        class GceRegionalPersistentDisk(proto.Message):
            r"""A PersistentDirectory backed by a Compute Engine regional
            persistent disk.

            Attributes:
                size_gb (int):
                    Size of the disk in GB. Must be empty if source_snapshot is
                    set. Defaults to 200.
                fs_type (str):
                    Type of file system that the disk should be formatted with.
                    The workstation image must support this file system type.
                    Must be empty if source_snapshot is set. Defaults to ext4.
                disk_type (str):
                    Type of the disk to use. Defaults to
                    pd-standard.
                source_snapshot (str):
                    Name of the snapshot to use as the source for the disk. If
                    set, size_gb and fs_type must be empty.
                reclaim_policy (google.cloud.workstations_v1.types.WorkstationConfig.PersistentDirectory.GceRegionalPersistentDisk.ReclaimPolicy):
                    What should happen to the disk after the
                    workstation is deleted. Defaults to DELETE.
            """

            class ReclaimPolicy(proto.Enum):
                r"""Value representing what should happen to the disk after the
                workstation is deleted.

                Values:
                    RECLAIM_POLICY_UNSPECIFIED (0):
                        Do not use.
                    DELETE (1):
                        The persistent disk will be deleted with the
                        workstation.
                    RETAIN (2):
                        The persistent disk will be remain after the
                        workstation is deleted, and the administrator
                        must manually delete the disk.
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

    class Container(proto.Message):
        r"""A Docker container.

        Attributes:
            image (str):
                Docker image defining the container. This
                image must be accessible by the service account
                specified in the workstation configuration.
            command (MutableSequence[str]):
                If set, overrides the default ENTRYPOINT
                specified by the image.
            args (MutableSequence[str]):
                Arguments passed to the entrypoint.
            env (MutableMapping[str, str]):
                Environment variables passed to the
                container's entrypoint.
            working_dir (str):
                If set, overrides the default DIR specified
                by the image.
            run_as_user (int):
                If set, overrides the USER specified in the
                image with the given uid.
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
        r"""A customer-managed encryption key for the Compute Engine
        resources of this workstation configuration.

        Attributes:
            kms_key (str):
                Immutable. The name of the Google Cloud KMS encryption key.
                For example,
                ``projects/PROJECT_ID/locations/REGION/keyRings/KEY_RING/cryptoKeys/KEY_NAME``.
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
    degraded: bool = proto.Field(
        proto.BOOL,
        number=15,
    )
    conditions: MutableSequence[status_pb2.Status] = proto.RepeatedField(
        proto.MESSAGE,
        number=16,
        message=status_pb2.Status,
    )


class Workstation(proto.Message):
    r"""A single instance of a developer workstation with its own
    persistent storage.

    Attributes:
        name (str):
            Full name of this resource.
        display_name (str):
            Human-readable name for this resource.
        uid (str):
            Output only. A system-assigned unique
            identified for this resource.
        reconciling (bool):
            Output only. Indicates whether this resource
            is currently being updated to match its intended
            state.
        annotations (MutableMapping[str, str]):
            Client-specified annotations.
        labels (MutableMapping[str, str]):
            Client-specified labels that are applied to
            the resource and that are also propagated to the
            underlying Compute Engine resources.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when this resource was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when this resource was most
            recently updated.
        delete_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when this resource was
            soft-deleted.
        etag (str):
            Checksum computed by the server. May be sent
            on update and delete requests to make sure that
            the client has an up-to-date value before
            proceeding.
        state (google.cloud.workstations_v1.types.Workstation.State):
            Output only. Current state of the
            workstation.
        host (str):
            Output only. Host to which clients can send HTTPS traffic
            that will be received by the workstation. Authorized traffic
            will be received to the workstation as HTTP on port 80. To
            send traffic to a different port, clients may prefix the
            host with the destination port in the format
            ``{port}-{host}``.
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
            Maximum number of items to return.
        page_token (str):
            next_page_token value returned from a previous List request,
            if any.
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
        workstation_clusters (MutableSequence[google.cloud.workstations_v1.types.WorkstationCluster]):
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
        workstation_cluster (google.cloud.workstations_v1.types.WorkstationCluster):
            Required. Workstation cluster to create.
        validate_only (bool):
            If set, validate the request and preview the
            review, but do not actually apply it.
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
        workstation_cluster (google.cloud.workstations_v1.types.WorkstationCluster):
            Required. Workstation cluster to update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Mask that specifies which fields in
            the workstation cluster should be updated.
        validate_only (bool):
            If set, validate the request and preview the
            review, but do not actually apply it.
        allow_missing (bool):
            If set, and the workstation cluster is not found, a new
            workstation cluster will be created. In this situation,
            update_mask is ignored.
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
            If set, validate the request and preview the
            review, but do not apply it.
        etag (str):
            If set, the request will be rejected if the
            latest version of the workstation cluster on the
            server does not have this ETag.
        force (bool):
            If set, any workstation configurations and
            workstations in the workstation cluster are also
            deleted. Otherwise, the request only works if
            the workstation cluster has no configurations or
            workstations.
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
            Maximum number of items to return.
        page_token (str):
            next_page_token value returned from a previous List request,
            if any.
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
        workstation_configs (MutableSequence[google.cloud.workstations_v1.types.WorkstationConfig]):
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
            Maximum number of items to return.
        page_token (str):
            next_page_token value returned from a previous List request,
            if any.
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
        workstation_configs (MutableSequence[google.cloud.workstations_v1.types.WorkstationConfig]):
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
        workstation_config (google.cloud.workstations_v1.types.WorkstationConfig):
            Required. Config to create.
        validate_only (bool):
            If set, validate the request and preview the
            review, but do not actually apply it.
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
        workstation_config (google.cloud.workstations_v1.types.WorkstationConfig):
            Required. Config to update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Mask specifying which fields in the
            workstation configuration should be updated.
        validate_only (bool):
            If set, validate the request and preview the
            review, but do not actually apply it.
        allow_missing (bool):
            If set and the workstation configuration is not found, a new
            workstation configuration will be created. In this
            situation, update_mask is ignored.
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
            If set, validate the request and preview the
            review, but do not actually apply it.
        etag (str):
            If set, the request is rejected if the latest
            version of the workstation configuration on the
            server does not have this ETag.
        force (bool):
            If set, any workstations in the workstation
            configuration are also deleted. Otherwise, the
            request works only if the workstation
            configuration has no workstations.
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
            Maximum number of items to return.
        page_token (str):
            next_page_token value returned from a previous List request,
            if any.
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
        workstations (MutableSequence[google.cloud.workstations_v1.types.Workstation]):
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


class ListUsableWorkstationsRequest(proto.Message):
    r"""Request message for ListUsableWorkstations.

    Attributes:
        parent (str):
            Required. Parent resource name.
        page_size (int):
            Maximum number of items to return.
        page_token (str):
            next_page_token value returned from a previous List request,
            if any.
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
        workstations (MutableSequence[google.cloud.workstations_v1.types.Workstation]):
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
        workstation (google.cloud.workstations_v1.types.Workstation):
            Required. Workstation to create.
        validate_only (bool):
            If set, validate the request and preview the
            review, but do not actually apply it.
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
        workstation (google.cloud.workstations_v1.types.Workstation):
            Required. Workstation to update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Mask specifying which fields in the
            workstation configuration should be updated.
        validate_only (bool):
            If set, validate the request and preview the
            review, but do not actually apply it.
        allow_missing (bool):
            If set and the workstation configuration is not found, a new
            workstation configuration is created. In this situation,
            update_mask is ignored.
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
            If set, validate the request and preview the
            review, but do not actually apply it.
        etag (str):
            If set, the request will be rejected if the
            latest version of the workstation on the server
            does not have this ETag.
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
            If set, validate the request and preview the
            review, but do not actually apply it.
        etag (str):
            If set, the request will be rejected if the
            latest version of the workstation on the server
            does not have this ETag.
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
            If set, validate the request and preview the
            review, but do not actually apply it.
        etag (str):
            If set, the request will be rejected if the
            latest version of the workstation on the server
            does not have this ETag.
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
