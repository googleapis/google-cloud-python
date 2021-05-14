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

from google.cloud.notebooks_v1beta1.types import environment
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.notebooks.v1beta1", manifest={"Instance",},
)


class Instance(proto.Message):
    r"""The definition of a notebook instance.
    Attributes:
        name (str):
            Output only. The name of this notebook instance. Format:
            ``projects/{project_id}/locations/{location}/instances/{instance_id}``
        vm_image (google.cloud.notebooks_v1beta1.types.VmImage):
            Use a Compute Engine VM image to start the
            notebook instance.
        container_image (google.cloud.notebooks_v1beta1.types.ContainerImage):
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
        machine_type (str):
            Required. The `Compute Engine machine
            type <https://cloud.google.com/compute/docs/machine-types>`__
            of this instance.
        accelerator_config (google.cloud.notebooks_v1beta1.types.Instance.AcceleratorConfig):
            The hardware accelerator used on this instance. If you use
            accelerators, make sure that your configuration has `enough
            vCPUs and memory to support the ``machine_type`` you have
            selected <https://cloud.google.com/compute/docs/gpus/#gpus-list>`__.
        state (google.cloud.notebooks_v1beta1.types.Instance.State):
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
        boot_disk_type (google.cloud.notebooks_v1beta1.types.Instance.DiskType):
            Input only. The type of the boot disk attached to this
            instance, defaults to standard persistent disk
            (``PD_STANDARD``).
        boot_disk_size_gb (int):
            Input only. The size of the boot disk in GB
            attached to this instance, up to a maximum of
            64000&nbsp;GB (64&nbsp;TB). The minimum
            recommended value is 100&nbsp;GB. If not
            specified, this defaults to 100.
        data_disk_type (google.cloud.notebooks_v1beta1.types.Instance.DiskType):
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
        disk_encryption (google.cloud.notebooks_v1beta1.types.Instance.DiskEncryption):
            Input only. Disk encryption method used on
            the boot and data disks, defaults to GMEK.
        kms_key (str):
            Input only. The KMS key used to encrypt the disks, only
            applicable if disk_encryption is CMEK. Format:
            ``projects/{project_id}/locations/{location}/keyRings/{key_ring_id}/cryptoKeys/{key_id}``

            Learn more about `using your own encryption
            keys <https://cloud.google.com/kms/docs/quickstart>`__.
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
        labels (Sequence[google.cloud.notebooks_v1beta1.types.Instance.LabelsEntry]):
            Labels to apply to this instance.
            These can be later modified by the setLabels
            method.
        metadata (Sequence[google.cloud.notebooks_v1beta1.types.Instance.MetadataEntry]):
            Custom metadata to apply to this instance.
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

    class AcceleratorConfig(proto.Message):
        r"""Definition of a hardware accelerator. Note that not all combinations
        of ``type`` and ``core_count`` are valid. Check `GPUs on Compute
        Engine </compute/docs/gpus/#gpus-list>`__ to find a valid
        combination. TPUs are not supported.

        Attributes:
            type_ (google.cloud.notebooks_v1beta1.types.Instance.AcceleratorType):
                Type of this accelerator.
            core_count (int):
                Count of cores of this accelerator.
        """

        type_ = proto.Field(proto.ENUM, number=1, enum="Instance.AcceleratorType",)
        core_count = proto.Field(proto.INT64, number=2,)

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
    no_public_ip = proto.Field(proto.BOOL, number=17,)
    no_proxy_access = proto.Field(proto.BOOL, number=18,)
    network = proto.Field(proto.STRING, number=19,)
    subnet = proto.Field(proto.STRING, number=20,)
    labels = proto.MapField(proto.STRING, proto.STRING, number=21,)
    metadata = proto.MapField(proto.STRING, proto.STRING, number=22,)
    create_time = proto.Field(
        proto.MESSAGE, number=23, message=timestamp_pb2.Timestamp,
    )
    update_time = proto.Field(
        proto.MESSAGE, number=24, message=timestamp_pb2.Timestamp,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
