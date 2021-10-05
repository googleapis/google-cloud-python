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

from google.cloud.notebooks_v1.types import environment
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.notebooks.v1",
    manifest={
        "Runtime",
        "RuntimeAcceleratorConfig",
        "EncryptionConfig",
        "LocalDisk",
        "LocalDiskInitializeParams",
        "RuntimeAccessConfig",
        "RuntimeSoftwareConfig",
        "RuntimeMetrics",
        "RuntimeShieldedInstanceConfig",
        "VirtualMachine",
        "VirtualMachineConfig",
    },
)


class Runtime(proto.Message):
    r"""The definition of a Runtime for a managed notebook instance.
    Attributes:
        name (str):
            Output only. The resource name of the runtime. Format:
            ``projects/{project}/locations/{location}/runtimes/{runtimeId}``
        virtual_machine (google.cloud.notebooks_v1.types.VirtualMachine):
            Use a Compute Engine VM image to start the
            managed notebook instance.
        state (google.cloud.notebooks_v1.types.Runtime.State):
            Output only. Runtime state.
        health_state (google.cloud.notebooks_v1.types.Runtime.HealthState):
            Output only. Runtime health_state.
        access_config (google.cloud.notebooks_v1.types.RuntimeAccessConfig):
            The config settings for accessing runtime.
        software_config (google.cloud.notebooks_v1.types.RuntimeSoftwareConfig):
            The config settings for software inside the
            runtime.
        metrics (google.cloud.notebooks_v1.types.RuntimeMetrics):
            Output only. Contains Runtime daemon metrics
            such as Service status and JupyterLab stats.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Runtime creation time.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Runtime update time.
    """

    class State(proto.Enum):
        r"""The definition of the states of this runtime."""
        STATE_UNSPECIFIED = 0
        STARTING = 1
        PROVISIONING = 2
        ACTIVE = 3
        STOPPING = 4
        STOPPED = 5
        DELETING = 6
        UPGRADING = 7
        INITIALIZING = 8

    class HealthState(proto.Enum):
        r"""The runtime substate."""
        HEALTH_STATE_UNSPECIFIED = 0
        HEALTHY = 1
        UNHEALTHY = 2

    name = proto.Field(proto.STRING, number=1,)
    virtual_machine = proto.Field(
        proto.MESSAGE, number=2, oneof="runtime_type", message="VirtualMachine",
    )
    state = proto.Field(proto.ENUM, number=3, enum=State,)
    health_state = proto.Field(proto.ENUM, number=4, enum=HealthState,)
    access_config = proto.Field(proto.MESSAGE, number=5, message="RuntimeAccessConfig",)
    software_config = proto.Field(
        proto.MESSAGE, number=6, message="RuntimeSoftwareConfig",
    )
    metrics = proto.Field(proto.MESSAGE, number=7, message="RuntimeMetrics",)
    create_time = proto.Field(
        proto.MESSAGE, number=20, message=timestamp_pb2.Timestamp,
    )
    update_time = proto.Field(
        proto.MESSAGE, number=21, message=timestamp_pb2.Timestamp,
    )


class RuntimeAcceleratorConfig(proto.Message):
    r"""Definition of the types of hardware accelerators that can be used.
    Definition of the types of hardware accelerators that can be used.
    See `Compute Engine
    AcceleratorTypes <https://cloud.google.com/compute/docs/reference/beta/acceleratorTypes>`__.
    Examples:

    -  ``nvidia-tesla-k80``
    -  ``nvidia-tesla-p100``
    -  ``nvidia-tesla-v100``
    -  ``nvidia-tesla-t4``
    -  ``nvidia-tesla-a100``

    Attributes:
        type_ (google.cloud.notebooks_v1.types.RuntimeAcceleratorConfig.AcceleratorType):
            Accelerator model.
        core_count (int):
            Count of cores of this accelerator.
    """

    class AcceleratorType(proto.Enum):
        r"""Type of this accelerator."""
        ACCELERATOR_TYPE_UNSPECIFIED = 0
        NVIDIA_TESLA_K80 = 1
        NVIDIA_TESLA_P100 = 2
        NVIDIA_TESLA_V100 = 3
        NVIDIA_TESLA_P4 = 4
        NVIDIA_TESLA_T4 = 5
        NVIDIA_TESLA_A100 = 6
        TPU_V2 = 7
        TPU_V3 = 8
        NVIDIA_TESLA_T4_VWS = 9
        NVIDIA_TESLA_P100_VWS = 10
        NVIDIA_TESLA_P4_VWS = 11

    type_ = proto.Field(proto.ENUM, number=1, enum=AcceleratorType,)
    core_count = proto.Field(proto.INT64, number=2,)


class EncryptionConfig(proto.Message):
    r"""Represents a custom encryption key configuration that can be
    applied to a resource. This will encrypt all disks in Virtual
    Machine.

    Attributes:
        kms_key (str):
            The Cloud KMS resource identifier of the customer-managed
            encryption key used to protect a resource, such as a disks.
            It has the following format:
            ``projects/{PROJECT_ID}/locations/{REGION}/keyRings/{KEY_RING_NAME}/cryptoKeys/{KEY_NAME}``
    """

    kms_key = proto.Field(proto.STRING, number=1,)


class LocalDisk(proto.Message):
    r"""An Local attached disk resource.
    Attributes:
        auto_delete (bool):
            Optional. Output only. Specifies whether the
            disk will be auto-deleted when the instance is
            deleted (but not when the disk is detached from
            the instance).
        boot (bool):
            Optional. Output only. Indicates that this is
            a boot disk. The virtual machine will use the
            first partition of the disk for its root
            filesystem.
        device_name (str):
            Optional. Output only. Specifies a unique device name of
            your choice that is reflected into the
            /dev/disk/by-id/google-\* tree of a Linux operating system
            running within the instance. This name can be used to
            reference the device for mounting, resizing, and so on, from
            within the instance.

            If not specified, the server chooses a default device name
            to apply to this disk, in the form persistent-disk-x, where
            x is a number assigned by Google Compute Engine. This field
            is only applicable for persistent disks.
        guest_os_features (Sequence[google.cloud.notebooks_v1.types.LocalDisk.RuntimeGuestOsFeature]):
            Output only. Indicates a list of features to
            enable on the guest operating system. Applicable
            only for bootable images. Read  Enabling guest
            operating system features to see a list of
            available options.
        index (int):
            Output only. A zero-based index to this disk,
            where 0 is reserved for the boot disk. If you
            have many disks attached to an instance, each
            disk would have a unique index number.
        initialize_params (google.cloud.notebooks_v1.types.LocalDiskInitializeParams):
            Input only. Specifies the parameters for a
            new disk that will be created alongside the new
            instance. Use initialization parameters to
            create boot disks or local SSDs attached to the
            new instance.
            This property is mutually exclusive with the
            source property; you can only define one or the
            other, but not both.
        interface (str):
            Specifies the disk interface to use for
            attaching this disk, which is either SCSI or
            NVME. The default is SCSI. Persistent disks must
            always use SCSI and the request will fail if you
            attempt to attach a persistent disk in any other
            format than SCSI. Local SSDs can use either NVME
            or SCSI. For performance characteristics of SCSI
            over NVMe, see Local SSD performance. Valid
            values:

            * NVME
            * SCSI
        kind (str):
            Output only. Type of the resource. Always
            compute#attachedDisk for attached disks.
        licenses (Sequence[str]):
            Output only. Any valid publicly visible
            licenses.
        mode (str):
            The mode in which to attach this disk, either READ_WRITE or
            READ_ONLY. If not specified, the default is to attach the
            disk in READ_WRITE mode. Valid values: READ_ONLY READ_WRITE
        source (str):
            Specifies a valid partial or full URL to an
            existing Persistent Disk resource.
        type_ (str):
            Specifies the type of the disk, either
            SCRATCH or PERSISTENT. If not specified, the
            default is PERSISTENT. Valid values:

            * PERSISTENT
            * SCRATCH
    """

    class RuntimeGuestOsFeature(proto.Message):
        r"""Optional. A list of features to enable on the guest operating
        system. Applicable only for bootable images. Read `Enabling guest
        operating system
        features <https://cloud.google.com/compute/docs/images/create-delete-deprecate-private-images#guest-os-features>`__
        to see a list of available options. Guest OS features for boot disk.

        Attributes:
            type_ (str):
                The ID of a supported feature. Read `Enabling guest
                operating system
                features <https://cloud.google.com/compute/docs/images/create-delete-deprecate-private-images#guest-os-features>`__
                to see a list of available options.

                Valid values:

                -  FEATURE_TYPE_UNSPECIFIED
                -  MULTI_IP_SUBNET
                -  SECURE_BOOT
                -  UEFI_COMPATIBLE
                -  VIRTIO_SCSI_MULTIQUEUE
                -  WINDOWS
        """

        type_ = proto.Field(proto.STRING, number=1,)

    auto_delete = proto.Field(proto.BOOL, number=1,)
    boot = proto.Field(proto.BOOL, number=2,)
    device_name = proto.Field(proto.STRING, number=3,)
    guest_os_features = proto.RepeatedField(
        proto.MESSAGE, number=4, message=RuntimeGuestOsFeature,
    )
    index = proto.Field(proto.INT32, number=5,)
    initialize_params = proto.Field(
        proto.MESSAGE, number=6, message="LocalDiskInitializeParams",
    )
    interface = proto.Field(proto.STRING, number=7,)
    kind = proto.Field(proto.STRING, number=8,)
    licenses = proto.RepeatedField(proto.STRING, number=9,)
    mode = proto.Field(proto.STRING, number=10,)
    source = proto.Field(proto.STRING, number=11,)
    type_ = proto.Field(proto.STRING, number=12,)


class LocalDiskInitializeParams(proto.Message):
    r"""Input only. Specifies the parameters for a new disk that will
    be created alongside the new instance. Use initialization
    parameters to create boot disks or local SSDs attached to the
    new runtime.
    This property is mutually exclusive with the source property;
    you can only define one or the other, but not both.

    Attributes:
        description (str):
            Optional. Provide this property when creating
            the disk.
        disk_name (str):
            Optional. Specifies the disk name. If not
            specified, the default is to use the name of the
            instance. If the disk with the instance name
            exists already in the given zone/region, a new
            name will be automatically generated.
        disk_size_gb (int):
            Optional. Specifies the size of the disk in
            base-2 GB. If not specified, the disk will be
            the same size as the image (usually 10GB). If
            specified, the size must be equal to or larger
            than 10GB. Default 100 GB.
        disk_type (google.cloud.notebooks_v1.types.LocalDiskInitializeParams.DiskType):
            Input only. The type of the boot disk attached to this
            instance, defaults to standard persistent disk
            (``PD_STANDARD``).
        labels (Sequence[google.cloud.notebooks_v1.types.LocalDiskInitializeParams.LabelsEntry]):
            Optional. Labels to apply to this disk. These
            can be later modified by the disks.setLabels
            method. This field is only applicable for
            persistent disks.
    """

    class DiskType(proto.Enum):
        r"""Possible disk types."""
        DISK_TYPE_UNSPECIFIED = 0
        PD_STANDARD = 1
        PD_SSD = 2
        PD_BALANCED = 3

    description = proto.Field(proto.STRING, number=1,)
    disk_name = proto.Field(proto.STRING, number=2,)
    disk_size_gb = proto.Field(proto.INT64, number=3,)
    disk_type = proto.Field(proto.ENUM, number=4, enum=DiskType,)
    labels = proto.MapField(proto.STRING, proto.STRING, number=5,)


class RuntimeAccessConfig(proto.Message):
    r"""Specifies the login configuration for Runtime
    Attributes:
        access_type (google.cloud.notebooks_v1.types.RuntimeAccessConfig.RuntimeAccessType):
            The type of access mode this instance.
        runtime_owner (str):
            The owner of this runtime after creation. Format:
            ``alias@example.com`` Currently supports one owner only.
        proxy_uri (str):
            Output only. The proxy endpoint that is used
            to access the runtime.
    """

    class RuntimeAccessType(proto.Enum):
        r"""Possible ways to access runtime. Authentication mode.
        Currently supports: Single User only.
        """
        RUNTIME_ACCESS_TYPE_UNSPECIFIED = 0
        SINGLE_USER = 1

    access_type = proto.Field(proto.ENUM, number=1, enum=RuntimeAccessType,)
    runtime_owner = proto.Field(proto.STRING, number=2,)
    proxy_uri = proto.Field(proto.STRING, number=3,)


class RuntimeSoftwareConfig(proto.Message):
    r"""Specifies the selection and configuration of software inside the
    runtime. The properties to set on runtime. Properties keys are
    specified in ``key:value`` format, for example:

    -  ``idle_shutdown: true``
    -  ``idle_shutdown_timeout: 180``
    -  ``report-system-health: true``

    Attributes:
        notebook_upgrade_schedule (str):
            Cron expression in UTC timezone, used to schedule instance
            auto upgrade. Please follow the `cron
            format <https://en.wikipedia.org/wiki/Cron>`__.
        enable_health_monitoring (bool):
            Verifies core internal services are running.
            Default: True
        idle_shutdown (bool):
            Runtime will automatically shutdown after
            idle_shutdown_time. Default: True
        idle_shutdown_timeout (int):
            Time in minutes to wait before shuting down
            runtime. Default: 180 minutes
        install_gpu_driver (bool):
            Install Nvidia Driver automatically.
        custom_gpu_driver_path (str):
            Specify a custom Cloud Storage path where the
            GPU driver is stored. If not specified, we'll
            automatically choose from official GPU drivers.
        post_startup_script (str):
            Path to a Bash script that automatically runs after a
            notebook instance fully boots up. The path must be a URL or
            Cloud Storage path (``gs://path-to-file/file-name``).
    """

    notebook_upgrade_schedule = proto.Field(proto.STRING, number=1,)
    enable_health_monitoring = proto.Field(proto.BOOL, number=2, optional=True,)
    idle_shutdown = proto.Field(proto.BOOL, number=3, optional=True,)
    idle_shutdown_timeout = proto.Field(proto.INT32, number=4,)
    install_gpu_driver = proto.Field(proto.BOOL, number=5,)
    custom_gpu_driver_path = proto.Field(proto.STRING, number=6,)
    post_startup_script = proto.Field(proto.STRING, number=7,)


class RuntimeMetrics(proto.Message):
    r"""Contains runtime daemon metrics, such as OS and kernels and
    sessions stats.

    Attributes:
        system_metrics (Sequence[google.cloud.notebooks_v1.types.RuntimeMetrics.SystemMetricsEntry]):
            Output only. The system metrics.
    """

    system_metrics = proto.MapField(proto.STRING, proto.STRING, number=1,)


class RuntimeShieldedInstanceConfig(proto.Message):
    r"""A set of Shielded Instance options. Check `Images using supported
    Shielded VM
    features <https://cloud.google.com/compute/docs/instances/modifying-shielded-vm>`__.
    Not all combinations are valid.

    Attributes:
        enable_secure_boot (bool):
            Defines whether the instance has Secure Boot
            enabled.
            Secure Boot helps ensure that the system only
            runs authentic software by verifying the digital
            signature of all boot components, and halting
            the boot process if signature verification
            fails. Disabled by default.
        enable_vtpm (bool):
            Defines whether the instance has the vTPM
            enabled. Enabled by default.
        enable_integrity_monitoring (bool):
            Defines whether the instance has integrity
            monitoring enabled.
            Enables monitoring and attestation of the boot
            integrity of the instance. The attestation is
            performed against the integrity policy baseline.
            This baseline is initially derived from the
            implicitly trusted boot image when the instance
            is created. Enabled by default.
    """

    enable_secure_boot = proto.Field(proto.BOOL, number=1,)
    enable_vtpm = proto.Field(proto.BOOL, number=2,)
    enable_integrity_monitoring = proto.Field(proto.BOOL, number=3,)


class VirtualMachine(proto.Message):
    r"""Runtime using Virtual Machine for computing.
    Attributes:
        instance_name (str):
            Output only. The user-friendly name of the
            Managed Compute Engine instance.
        instance_id (str):
            Output only. The unique identifier of the
            Managed Compute Engine instance.
        virtual_machine_config (google.cloud.notebooks_v1.types.VirtualMachineConfig):
            Virtual Machine configuration settings.
    """

    instance_name = proto.Field(proto.STRING, number=1,)
    instance_id = proto.Field(proto.STRING, number=2,)
    virtual_machine_config = proto.Field(
        proto.MESSAGE, number=3, message="VirtualMachineConfig",
    )


class VirtualMachineConfig(proto.Message):
    r"""The config settings for virtual machine.
    Attributes:
        zone (str):
            Output only. The zone where the virtual machine is located.
            If using regional request, the notebooks service will pick a
            location in the corresponding runtime region. On a get
            request, zone will always be present. Example:

            -  ``us-central1-b``
        machine_type (str):
            Required. The Compute Engine machine type used for runtimes.
            Short name is valid. Examples:

            -  ``n1-standard-2``
            -  ``e2-standard-8``
        container_images (Sequence[google.cloud.notebooks_v1.types.ContainerImage]):
            Optional. Use a list of container images to
            start the notebook instance.
        data_disk (google.cloud.notebooks_v1.types.LocalDisk):
            Required. Data disk option configuration
            settings.
        encryption_config (google.cloud.notebooks_v1.types.EncryptionConfig):
            Optional. Encryption settings for virtual
            machine data disk.
        shielded_instance_config (google.cloud.notebooks_v1.types.RuntimeShieldedInstanceConfig):
            Optional. Shielded VM Instance configuration
            settings.
        accelerator_config (google.cloud.notebooks_v1.types.RuntimeAcceleratorConfig):
            Optional. The Compute Engine accelerator
            configuration for this runtime.
        network (str):
            Optional. The Compute Engine network to be used for machine
            communications. Cannot be specified with subnetwork. If
            neither ``network`` nor ``subnet`` is specified, the
            "default" network of the project is used, if it exists.

            A full URL or partial URI. Examples:

            -  ``https://www.googleapis.com/compute/v1/projects/[project_id]/regions/global/default``
            -  ``projects/[project_id]/regions/global/default``

            Runtimes are managed resources inside Google Infrastructure.
            Runtimes support the following network configurations:

            -  Google Managed Network (Network & subnet are empty)
            -  Consumer Project VPC (network & subnet are required).
               Requires configuring Private Service Access.
            -  Shared VPC (network & subnet are required). Requires
               configuring Private Service Access.
        subnet (str):
            Optional. The Compute Engine subnetwork to be used for
            machine communications. Cannot be specified with network.

            A full URL or partial URI are valid. Examples:

            -  ``https://www.googleapis.com/compute/v1/projects/[project_id]/regions/us-east1/subnetworks/sub0``
            -  ``projects/[project_id]/regions/us-east1/subnetworks/sub0``
        internal_ip_only (bool):
            Optional. If true, runtime will only have internal IP
            addresses. By default, runtimes are not restricted to
            internal IP addresses, and will have ephemeral external IP
            addresses assigned to each vm. This ``internal_ip_only``
            restriction can only be enabled for subnetwork enabled
            networks, and all dependencies must be configured to be
            accessible without external IP addresses.
        tags (Sequence[str]):
            Optional. The Compute Engine tags to add to runtime (see
            `Tagging
            instances <https://cloud.google.com/compute/docs/label-or-tag-resources#tags>`__).
        guest_attributes (Sequence[google.cloud.notebooks_v1.types.VirtualMachineConfig.GuestAttributesEntry]):
            Output only. The Compute Engine guest attributes. (see
            `Project and instance guest
            attributes <https://cloud.google.com/compute/docs/storing-retrieving-metadata#guest_attributes>`__).
        metadata (Sequence[google.cloud.notebooks_v1.types.VirtualMachineConfig.MetadataEntry]):
            Optional. The Compute Engine metadata entries to add to
            virtual machine. (see `Project and instance
            metadata <https://cloud.google.com/compute/docs/storing-retrieving-metadata#project_and_instance_metadata>`__).
        labels (Sequence[google.cloud.notebooks_v1.types.VirtualMachineConfig.LabelsEntry]):
            Optional. The labels to associate with this runtime. Label
            **keys** must contain 1 to 63 characters, and must conform
            to `RFC 1035 <https://www.ietf.org/rfc/rfc1035.txt>`__.
            Label **values** may be empty, but, if present, must contain
            1 to 63 characters, and must conform to `RFC
            1035 <https://www.ietf.org/rfc/rfc1035.txt>`__. No more than
            32 labels can be associated with a cluster.
        nic_type (google.cloud.notebooks_v1.types.VirtualMachineConfig.NicType):
            Optional. The type of vNIC to be used on this
            interface. This may be gVNIC or VirtioNet.
    """

    class NicType(proto.Enum):
        r"""The type of vNIC driver. Default should be UNSPECIFIED_NIC_TYPE."""
        UNSPECIFIED_NIC_TYPE = 0
        VIRTIO_NET = 1
        GVNIC = 2

    zone = proto.Field(proto.STRING, number=1,)
    machine_type = proto.Field(proto.STRING, number=2,)
    container_images = proto.RepeatedField(
        proto.MESSAGE, number=3, message=environment.ContainerImage,
    )
    data_disk = proto.Field(proto.MESSAGE, number=4, message="LocalDisk",)
    encryption_config = proto.Field(
        proto.MESSAGE, number=5, message="EncryptionConfig",
    )
    shielded_instance_config = proto.Field(
        proto.MESSAGE, number=6, message="RuntimeShieldedInstanceConfig",
    )
    accelerator_config = proto.Field(
        proto.MESSAGE, number=7, message="RuntimeAcceleratorConfig",
    )
    network = proto.Field(proto.STRING, number=8,)
    subnet = proto.Field(proto.STRING, number=9,)
    internal_ip_only = proto.Field(proto.BOOL, number=10,)
    tags = proto.RepeatedField(proto.STRING, number=13,)
    guest_attributes = proto.MapField(proto.STRING, proto.STRING, number=14,)
    metadata = proto.MapField(proto.STRING, proto.STRING, number=15,)
    labels = proto.MapField(proto.STRING, proto.STRING, number=16,)
    nic_type = proto.Field(proto.ENUM, number=17, enum=NicType,)


__all__ = tuple(sorted(__protobuf__.manifest))
