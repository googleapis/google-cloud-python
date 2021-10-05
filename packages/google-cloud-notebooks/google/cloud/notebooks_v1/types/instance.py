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
    package="google.cloud.notebooks.v1", manifest={"ReservationAffinity", "Instance",},
)


class ReservationAffinity(proto.Message):
    r"""Reservation Affinity for consuming Zonal reservation.

    Attributes:
        consume_reservation_type (google.cloud.notebooks_v1.types.ReservationAffinity.Type):
            Optional. Type of reservation to consume
        key (str):
            Optional. Corresponds to the label key of
            reservation resource.
        values (Sequence[str]):
            Optional. Corresponds to the label values of
            reservation resource.
    """

    class Type(proto.Enum):
        r"""Indicates whether to consume capacity from an reservation or
        not.
        """
        TYPE_UNSPECIFIED = 0
        NO_RESERVATION = 1
        ANY_RESERVATION = 2
        SPECIFIC_RESERVATION = 3

    consume_reservation_type = proto.Field(proto.ENUM, number=1, enum=Type,)
    key = proto.Field(proto.STRING, number=2,)
    values = proto.RepeatedField(proto.STRING, number=3,)


class Instance(proto.Message):
    r"""The definition of a notebook instance.

    Attributes:
        name (str):
            Output only. The name of this notebook instance. Format:
            ``projects/{project_id}/locations/{location}/instances/{instance_id}``
        vm_image (google.cloud.notebooks_v1.types.VmImage):
            Use a Compute Engine VM image to start the
            notebook instance.
        container_image (google.cloud.notebooks_v1.types.ContainerImage):
            Use a container image to start the notebook
            instance.
        post_startup_script (str):
            Path to a Bash script that automatically runs after a
            notebook instance fully boots up. The path must be a URL or
            Cloud Storage path (``gs://path-to-file/file-name``).
        proxy_uri (str):
            Output only. The proxy endpoint that is used
            to access the Jupyter notebook.
        instance_owners (Sequence[str]):
            Input only. The owner of this instance after creation.
            Format: ``alias@example.com``

            Currently supports one owner only. If not specified, all of
            the service account users of your VM instance's service
            account can use the instance.
        service_account (str):
            The service account on this instance, giving access to other
            Google Cloud services. You can use any service account
            within the same project, but you must have the service
            account user permission to use the instance.

            If not specified, the `Compute Engine default service
            account <https://cloud.google.com/compute/docs/access/service-accounts#default_service_account>`__
            is used.
        service_account_scopes (Sequence[str]):
            Optional. The URIs of service account scopes to be included
            in Compute Engine instances.

            If not specified, the following
            `scopes <https://cloud.google.com/compute/docs/access/service-accounts#accesscopesiam>`__
            are defined:

            -  https://www.googleapis.com/auth/cloud-platform
            -  https://www.googleapis.com/auth/userinfo.email If not
               using default scopes, you need at least:
               https://www.googleapis.com/auth/compute
        machine_type (str):
            Required. The `Compute Engine machine
            type </compute/docs/machine-types>`__ of this instance.
        accelerator_config (google.cloud.notebooks_v1.types.Instance.AcceleratorConfig):
            The hardware accelerator used on this instance. If you use
            accelerators, make sure that your configuration has `enough
            vCPUs and memory to support the ``machine_type`` you have
            selected </compute/docs/gpus/#gpus-list>`__.
        state (google.cloud.notebooks_v1.types.Instance.State):
            Output only. The state of this instance.
        install_gpu_driver (bool):
            Whether the end user authorizes Google Cloud
            to install GPU driver on this instance.
            If this field is empty or set to false, the GPU
            driver won't be installed. Only applicable to
            instances with GPUs.
        custom_gpu_driver_path (str):
            Specify a custom Cloud Storage path where the
            GPU driver is stored. If not specified, we'll
            automatically choose from official GPU drivers.
        boot_disk_type (google.cloud.notebooks_v1.types.Instance.DiskType):
            Input only. The type of the boot disk attached to this
            instance, defaults to standard persistent disk
            (``PD_STANDARD``).
        boot_disk_size_gb (int):
            Input only. The size of the boot disk in GB
            attached to this instance, up to a maximum of
            64000&nbsp;GB (64&nbsp;TB). The minimum
            recommended value is 100&nbsp;GB. If not
            specified, this defaults to 100.
        data_disk_type (google.cloud.notebooks_v1.types.Instance.DiskType):
            Input only. The type of the data disk attached to this
            instance, defaults to standard persistent disk
            (``PD_STANDARD``).
        data_disk_size_gb (int):
            Input only. The size of the data disk in GB
            attached to this instance, up to a maximum of
            64000&nbsp;GB (64&nbsp;TB). You can choose the
            size of the data disk based on how big your
            notebooks and data are. If not specified, this
            defaults to 100.
        no_remove_data_disk (bool):
            Input only. If true, the data disk will not
            be auto deleted when deleting the instance.
        disk_encryption (google.cloud.notebooks_v1.types.Instance.DiskEncryption):
            Input only. Disk encryption method used on
            the boot and data disks, defaults to GMEK.
        kms_key (str):
            Input only. The KMS key used to encrypt the disks, only
            applicable if disk_encryption is CMEK. Format:
            ``projects/{project_id}/locations/{location}/keyRings/{key_ring_id}/cryptoKeys/{key_id}``

            Learn more about `using your own encryption
            keys </kms/docs/quickstart>`__.
        disks (Sequence[google.cloud.notebooks_v1.types.Instance.Disk]):
            Output only. Attached disks to notebook
            instance.
        shielded_instance_config (google.cloud.notebooks_v1.types.Instance.ShieldedInstanceConfig):
            Optional. Shielded VM configuration. `Images using supported
            Shielded VM
            features <https://cloud.google.com/compute/docs/instances/modifying-shielded-vm>`__.
        no_public_ip (bool):
            If true, no public IP will be assigned to
            this instance.
        no_proxy_access (bool):
            If true, the notebook instance will not
            register with the proxy.
        network (str):
            The name of the VPC that this instance is in. Format:
            ``projects/{project_id}/global/networks/{network_id}``
        subnet (str):
            The name of the subnet that this instance is in. Format:
            ``projects/{project_id}/regions/{region}/subnetworks/{subnetwork_id}``
        labels (Sequence[google.cloud.notebooks_v1.types.Instance.LabelsEntry]):
            Labels to apply to this instance.
            These can be later modified by the setLabels
            method.
        metadata (Sequence[google.cloud.notebooks_v1.types.Instance.MetadataEntry]):
            Custom metadata to apply to this instance.
        tags (Sequence[str]):
            Optional. The Compute Engine tags to add to runtime (see
            `Tagging
            instances <https://cloud.google.com/compute/docs/label-or-tag-resources#tags>`__).
        upgrade_history (Sequence[google.cloud.notebooks_v1.types.Instance.UpgradeHistoryEntry]):
            The upgrade history of this instance.
        nic_type (google.cloud.notebooks_v1.types.Instance.NicType):
            Optional. The type of vNIC to be used on this
            interface. This may be gVNIC or VirtioNet.
        reservation_affinity (google.cloud.notebooks_v1.types.ReservationAffinity):
            Optional. The optional reservation affinity. Setting this
            field will apply the specified `Zonal Compute
            Reservation <https://cloud.google.com/compute/docs/instances/reserving-zonal-resources>`__
            to this notebook instance.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Instance creation time.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Instance update time.
    """

    class AcceleratorType(proto.Enum):
        r"""Definition of the types of hardware accelerators that can be
        used on this instance.
        """
        ACCELERATOR_TYPE_UNSPECIFIED = 0
        NVIDIA_TESLA_K80 = 1
        NVIDIA_TESLA_P100 = 2
        NVIDIA_TESLA_V100 = 3
        NVIDIA_TESLA_P4 = 4
        NVIDIA_TESLA_T4 = 5
        NVIDIA_TESLA_A100 = 11
        NVIDIA_TESLA_T4_VWS = 8
        NVIDIA_TESLA_P100_VWS = 9
        NVIDIA_TESLA_P4_VWS = 10
        TPU_V2 = 6
        TPU_V3 = 7

    class State(proto.Enum):
        r"""The definition of the states of this instance."""
        STATE_UNSPECIFIED = 0
        STARTING = 1
        PROVISIONING = 2
        ACTIVE = 3
        STOPPING = 4
        STOPPED = 5
        DELETED = 6
        UPGRADING = 7
        INITIALIZING = 8
        REGISTERING = 9

    class DiskType(proto.Enum):
        r"""Possible disk types for notebook instances."""
        DISK_TYPE_UNSPECIFIED = 0
        PD_STANDARD = 1
        PD_SSD = 2
        PD_BALANCED = 3

    class DiskEncryption(proto.Enum):
        r"""Definition of the disk encryption options."""
        DISK_ENCRYPTION_UNSPECIFIED = 0
        GMEK = 1
        CMEK = 2

    class NicType(proto.Enum):
        r"""The type of vNIC driver. Default should be UNSPECIFIED_NIC_TYPE."""
        UNSPECIFIED_NIC_TYPE = 0
        VIRTIO_NET = 1
        GVNIC = 2

    class AcceleratorConfig(proto.Message):
        r"""Definition of a hardware accelerator. Note that not all combinations
        of ``type`` and ``core_count`` are valid. Check `GPUs on Compute
        Engine </compute/docs/gpus/#gpus-list>`__ to find a valid
        combination. TPUs are not supported.

        Attributes:
            type_ (google.cloud.notebooks_v1.types.Instance.AcceleratorType):
                Type of this accelerator.
            core_count (int):
                Count of cores of this accelerator.
        """

        type_ = proto.Field(proto.ENUM, number=1, enum="Instance.AcceleratorType",)
        core_count = proto.Field(proto.INT64, number=2,)

    class Disk(proto.Message):
        r"""An instance-attached disk resource.

        Attributes:
            auto_delete (bool):
                Indicates whether the disk will be auto-
                eleted when the instance is deleted (but not
                when the disk is detached from the instance).
            boot (bool):
                Indicates that this is a boot disk. The
                virtual machine will use the first partition of
                the disk for its root filesystem.
            device_name (str):
                Indicates a unique device name of your choice that is
                reflected into the /dev/disk/by-id/google-\* tree of a Linux
                operating system running within the instance. This name can
                be used to reference the device for mounting, resizing, and
                so on, from within the instance.

                If not specified, the server chooses a default device name
                to apply to this disk, in the form persistent-disk-x, where
                x is a number assigned by Google Compute Engine.This field
                is only applicable for persistent disks.
            disk_size_gb (int):
                Indicates the size of the disk in base-2 GB.
            guest_os_features (Sequence[google.cloud.notebooks_v1.types.Instance.Disk.GuestOsFeature]):
                Indicates a list of features to enable on the
                guest operating system. Applicable only for
                bootable images. Read  Enabling guest operating
                system features to see a list of available
                options.
            index (int):
                A zero-based index to this disk, where 0 is
                reserved for the boot disk. If you have many
                disks attached to an instance, each disk would
                have a unique index number.
            interface (str):
                Indicates the disk interface to use for
                attaching this disk, which is either SCSI or
                NVME. The default is SCSI. Persistent disks must
                always use SCSI and the request will fail if you
                attempt to attach a persistent disk in any other
                format than SCSI. Local SSDs can use either NVME
                or SCSI. For performance characteristics of SCSI
                over NVMe, see Local SSD performance.
                Valid values:

                * NVME
                * SCSI
            kind (str):
                Type of the resource. Always
                compute#attachedDisk for attached disks.
            licenses (Sequence[str]):
                A list of publicly visible licenses. Reserved
                for Google's use. A License represents billing
                and aggregate usage data for public and
                marketplace images.
            mode (str):
                The mode in which to attach this disk, either READ_WRITE or
                READ_ONLY. If not specified, the default is to attach the
                disk in READ_WRITE mode. Valid values: READ_ONLY READ_WRITE
            source (str):
                Indicates a valid partial or full URL to an
                existing Persistent Disk resource.
            type_ (str):
                Indicates the type of the disk, either
                SCRATCH or PERSISTENT. Valid values:

                * PERSISTENT
                * SCRATCH
        """

        class GuestOsFeature(proto.Message):
            r"""Guest OS features for boot disk.

            Attributes:
                type_ (str):
                    The ID of a supported feature. Read Enabling guest operating
                    system features to see a list of available options. Valid
                    values: FEATURE_TYPE_UNSPECIFIED MULTI_IP_SUBNET SECURE_BOOT
                    UEFI_COMPATIBLE VIRTIO_SCSI_MULTIQUEUE WINDOWS
            """

            type_ = proto.Field(proto.STRING, number=1,)

        auto_delete = proto.Field(proto.BOOL, number=1,)
        boot = proto.Field(proto.BOOL, number=2,)
        device_name = proto.Field(proto.STRING, number=3,)
        disk_size_gb = proto.Field(proto.INT64, number=4,)
        guest_os_features = proto.RepeatedField(
            proto.MESSAGE, number=5, message="Instance.Disk.GuestOsFeature",
        )
        index = proto.Field(proto.INT64, number=6,)
        interface = proto.Field(proto.STRING, number=7,)
        kind = proto.Field(proto.STRING, number=8,)
        licenses = proto.RepeatedField(proto.STRING, number=9,)
        mode = proto.Field(proto.STRING, number=10,)
        source = proto.Field(proto.STRING, number=11,)
        type_ = proto.Field(proto.STRING, number=12,)

    class ShieldedInstanceConfig(proto.Message):
        r"""A set of Shielded Instance options. Check [Images using supported
        Shielded VM features] Not all combinations are valid.

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

    class UpgradeHistoryEntry(proto.Message):
        r"""The entry of VM image upgrade history.

        Attributes:
            snapshot (str):
                The snapshot of the boot disk of this
                notebook instance before upgrade.
            vm_image (str):
                The VM image before this instance upgrade.
            container_image (str):
                The container image before this instance
                upgrade.
            framework (str):
                The framework of this notebook instance.
            version (str):
                The version of the notebook instance before
                this upgrade.
            state (google.cloud.notebooks_v1.types.Instance.UpgradeHistoryEntry.State):
                The state of this instance upgrade history
                entry.
            create_time (google.protobuf.timestamp_pb2.Timestamp):
                The time that this instance upgrade history
                entry is created.
            target_image (str):
                Target VM Image. Format: ainotebooks-
                m/project/image-name/name.
            action (google.cloud.notebooks_v1.types.Instance.UpgradeHistoryEntry.Action):
                Action. Rolloback or Upgrade.
            target_version (str):
                Target VM Version, like m63.
        """

        class State(proto.Enum):
            r"""The definition of the states of this upgrade history entry."""
            STATE_UNSPECIFIED = 0
            STARTED = 1
            SUCCEEDED = 2
            FAILED = 3

        class Action(proto.Enum):
            r"""The definition of operations of this upgrade history entry."""
            ACTION_UNSPECIFIED = 0
            UPGRADE = 1
            ROLLBACK = 2

        snapshot = proto.Field(proto.STRING, number=1,)
        vm_image = proto.Field(proto.STRING, number=2,)
        container_image = proto.Field(proto.STRING, number=3,)
        framework = proto.Field(proto.STRING, number=4,)
        version = proto.Field(proto.STRING, number=5,)
        state = proto.Field(
            proto.ENUM, number=6, enum="Instance.UpgradeHistoryEntry.State",
        )
        create_time = proto.Field(
            proto.MESSAGE, number=7, message=timestamp_pb2.Timestamp,
        )
        target_image = proto.Field(proto.STRING, number=8,)
        action = proto.Field(
            proto.ENUM, number=9, enum="Instance.UpgradeHistoryEntry.Action",
        )
        target_version = proto.Field(proto.STRING, number=10,)

    name = proto.Field(proto.STRING, number=1,)
    vm_image = proto.Field(
        proto.MESSAGE, number=2, oneof="environment", message=environment.VmImage,
    )
    container_image = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="environment",
        message=environment.ContainerImage,
    )
    post_startup_script = proto.Field(proto.STRING, number=4,)
    proxy_uri = proto.Field(proto.STRING, number=5,)
    instance_owners = proto.RepeatedField(proto.STRING, number=6,)
    service_account = proto.Field(proto.STRING, number=7,)
    service_account_scopes = proto.RepeatedField(proto.STRING, number=31,)
    machine_type = proto.Field(proto.STRING, number=8,)
    accelerator_config = proto.Field(
        proto.MESSAGE, number=9, message=AcceleratorConfig,
    )
    state = proto.Field(proto.ENUM, number=10, enum=State,)
    install_gpu_driver = proto.Field(proto.BOOL, number=11,)
    custom_gpu_driver_path = proto.Field(proto.STRING, number=12,)
    boot_disk_type = proto.Field(proto.ENUM, number=13, enum=DiskType,)
    boot_disk_size_gb = proto.Field(proto.INT64, number=14,)
    data_disk_type = proto.Field(proto.ENUM, number=25, enum=DiskType,)
    data_disk_size_gb = proto.Field(proto.INT64, number=26,)
    no_remove_data_disk = proto.Field(proto.BOOL, number=27,)
    disk_encryption = proto.Field(proto.ENUM, number=15, enum=DiskEncryption,)
    kms_key = proto.Field(proto.STRING, number=16,)
    disks = proto.RepeatedField(proto.MESSAGE, number=28, message=Disk,)
    shielded_instance_config = proto.Field(
        proto.MESSAGE, number=30, message=ShieldedInstanceConfig,
    )
    no_public_ip = proto.Field(proto.BOOL, number=17,)
    no_proxy_access = proto.Field(proto.BOOL, number=18,)
    network = proto.Field(proto.STRING, number=19,)
    subnet = proto.Field(proto.STRING, number=20,)
    labels = proto.MapField(proto.STRING, proto.STRING, number=21,)
    metadata = proto.MapField(proto.STRING, proto.STRING, number=22,)
    tags = proto.RepeatedField(proto.STRING, number=32,)
    upgrade_history = proto.RepeatedField(
        proto.MESSAGE, number=29, message=UpgradeHistoryEntry,
    )
    nic_type = proto.Field(proto.ENUM, number=33, enum=NicType,)
    reservation_affinity = proto.Field(
        proto.MESSAGE, number=34, message="ReservationAffinity",
    )
    create_time = proto.Field(
        proto.MESSAGE, number=23, message=timestamp_pb2.Timestamp,
    )
    update_time = proto.Field(
        proto.MESSAGE, number=24, message=timestamp_pb2.Timestamp,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
