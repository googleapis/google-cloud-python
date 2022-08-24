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

from google.cloud.batch_v1.types import task
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.batch.v1",
    manifest={
        "Job",
        "LogsPolicy",
        "JobStatus",
        "JobNotification",
        "AllocationPolicy",
        "TaskGroup",
    },
)


class Job(proto.Message):
    r"""The Cloud Batch Job description.

    Attributes:
        name (str):
            Output only. Job name.
            For example:
            "projects/123456/locations/us-central1/jobs/job01".
        uid (str):
            Output only. A system generated unique ID (in
            UUID4 format) for the Job.
        priority (int):
            Priority of the Job. The valid value range is [0, 100). A
            job with higher priority value is more likely to run earlier
            if all other requirements are satisfied.
        task_groups (Sequence[google.cloud.batch_v1.types.TaskGroup]):
            Required. TaskGroups in the Job. Only one
            TaskGroup is supported now.
        allocation_policy (google.cloud.batch_v1.types.AllocationPolicy):
            Compute resource allocation for all
            TaskGroups in the Job.
        labels (Mapping[str, str]):
            Labels for the Job. Labels could be user provided or system
            generated. For example, "labels": { "department": "finance",
            "environment": "test" } You can assign up to 64 labels.
            `Google Compute Engine label
            restrictions <https://cloud.google.com/compute/docs/labeling-resources#restrictions>`__
            apply. Label names that start with "goog-" or "google-" are
            reserved.
        status (google.cloud.batch_v1.types.JobStatus):
            Output only. Job status. It is read only for
            users.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. When the Job was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The last time the Job was
            updated.
        logs_policy (google.cloud.batch_v1.types.LogsPolicy):
            Log preservation policy for the Job.
        notifications (Sequence[google.cloud.batch_v1.types.JobNotification]):
            Notification configurations.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    uid = proto.Field(
        proto.STRING,
        number=2,
    )
    priority = proto.Field(
        proto.INT64,
        number=3,
    )
    task_groups = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message="TaskGroup",
    )
    allocation_policy = proto.Field(
        proto.MESSAGE,
        number=7,
        message="AllocationPolicy",
    )
    labels = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=8,
    )
    status = proto.Field(
        proto.MESSAGE,
        number=9,
        message="JobStatus",
    )
    create_time = proto.Field(
        proto.MESSAGE,
        number=11,
        message=timestamp_pb2.Timestamp,
    )
    update_time = proto.Field(
        proto.MESSAGE,
        number=12,
        message=timestamp_pb2.Timestamp,
    )
    logs_policy = proto.Field(
        proto.MESSAGE,
        number=13,
        message="LogsPolicy",
    )
    notifications = proto.RepeatedField(
        proto.MESSAGE,
        number=14,
        message="JobNotification",
    )


class LogsPolicy(proto.Message):
    r"""LogsPolicy describes how outputs from a Job's Tasks
    (stdout/stderr) will be preserved.

    Attributes:
        destination (google.cloud.batch_v1.types.LogsPolicy.Destination):
            Where logs should be saved.
        logs_path (str):
            The path to which logs are saved when the
            destination = PATH. This can be a local file
            path on the VM, or under the mount point of a
            Persistent Disk or Filestore, or a Cloud Storage
            path.
    """

    class Destination(proto.Enum):
        r"""The destination (if any) for logs."""
        DESTINATION_UNSPECIFIED = 0
        CLOUD_LOGGING = 1
        PATH = 2

    destination = proto.Field(
        proto.ENUM,
        number=1,
        enum=Destination,
    )
    logs_path = proto.Field(
        proto.STRING,
        number=2,
    )


class JobStatus(proto.Message):
    r"""Job status.

    Attributes:
        state (google.cloud.batch_v1.types.JobStatus.State):
            Job state
        status_events (Sequence[google.cloud.batch_v1.types.StatusEvent]):
            Job status events
        task_groups (Mapping[str, google.cloud.batch_v1.types.JobStatus.TaskGroupStatus]):
            Aggregated task status for each TaskGroup in
            the Job. The map key is TaskGroup ID.
        run_duration (google.protobuf.duration_pb2.Duration):
            The duration of time that the Job spent in
            status RUNNING.
    """

    class State(proto.Enum):
        r"""Valid Job states."""
        STATE_UNSPECIFIED = 0
        QUEUED = 1
        SCHEDULED = 2
        RUNNING = 3
        SUCCEEDED = 4
        FAILED = 5
        DELETION_IN_PROGRESS = 6

    class InstanceStatus(proto.Message):
        r"""VM instance status.

        Attributes:
            machine_type (str):
                The Compute Engine machine type.
            provisioning_model (google.cloud.batch_v1.types.AllocationPolicy.ProvisioningModel):
                The VM instance provisioning model.
            task_pack (int):
                The max number of tasks can be assigned to
                this instance type.
        """

        machine_type = proto.Field(
            proto.STRING,
            number=1,
        )
        provisioning_model = proto.Field(
            proto.ENUM,
            number=2,
            enum="AllocationPolicy.ProvisioningModel",
        )
        task_pack = proto.Field(
            proto.INT64,
            number=3,
        )

    class TaskGroupStatus(proto.Message):
        r"""Aggregated task status for a TaskGroup.

        Attributes:
            counts (Mapping[str, int]):
                Count of task in each state in the TaskGroup.
                The map key is task state name.
            instances (Sequence[google.cloud.batch_v1.types.JobStatus.InstanceStatus]):
                Status of instances allocated for the
                TaskGroup.
        """

        counts = proto.MapField(
            proto.STRING,
            proto.INT64,
            number=1,
        )
        instances = proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message="JobStatus.InstanceStatus",
        )

    state = proto.Field(
        proto.ENUM,
        number=1,
        enum=State,
    )
    status_events = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=task.StatusEvent,
    )
    task_groups = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=4,
        message=TaskGroupStatus,
    )
    run_duration = proto.Field(
        proto.MESSAGE,
        number=5,
        message=duration_pb2.Duration,
    )


class JobNotification(proto.Message):
    r"""Notification configurations.

    Attributes:
        pubsub_topic (str):
            The Pub/Sub topic where notifications like the job state
            changes will be published. This topic exist in the same
            project as the job and billings will be charged to this
            project. If not specified, no Pub/Sub messages will be sent.
            Topic format: ``projects/{project}/topics/{topic}``.
        message (google.cloud.batch_v1.types.JobNotification.Message):
            The attribute requirements of messages to be
            sent to this Pub/Sub topic. Without this field,
            no message will be sent.
    """

    class Type(proto.Enum):
        r"""The message type."""
        TYPE_UNSPECIFIED = 0
        JOB_STATE_CHANGED = 1
        TASK_STATE_CHANGED = 2

    class Message(proto.Message):
        r"""Message details.
        Describe the attribute that a message should have.
        Without specified message attributes, no message will be sent by
        default.

        Attributes:
            type_ (google.cloud.batch_v1.types.JobNotification.Type):
                The message type.
            new_job_state (google.cloud.batch_v1.types.JobStatus.State):
                The new job state.
            new_task_state (google.cloud.batch_v1.types.TaskStatus.State):
                The new task state.
        """

        type_ = proto.Field(
            proto.ENUM,
            number=1,
            enum="JobNotification.Type",
        )
        new_job_state = proto.Field(
            proto.ENUM,
            number=2,
            enum="JobStatus.State",
        )
        new_task_state = proto.Field(
            proto.ENUM,
            number=3,
            enum=task.TaskStatus.State,
        )

    pubsub_topic = proto.Field(
        proto.STRING,
        number=1,
    )
    message = proto.Field(
        proto.MESSAGE,
        number=2,
        message=Message,
    )


class AllocationPolicy(proto.Message):
    r"""A Job's resource allocation policy describes when, where, and
    how compute resources should be allocated for the Job.

    Attributes:
        location (google.cloud.batch_v1.types.AllocationPolicy.LocationPolicy):
            Location where compute resources should be
            allocated for the Job.
        instances (Sequence[google.cloud.batch_v1.types.AllocationPolicy.InstancePolicyOrTemplate]):
            Describe instances that can be created by this
            AllocationPolicy. Only instances[0] is supported now.
        labels (Mapping[str, str]):
            Labels applied to all VM instances and other resources
            created by AllocationPolicy. Labels could be user provided
            or system generated. You can assign up to 64 labels. `Google
            Compute Engine label
            restrictions <https://cloud.google.com/compute/docs/labeling-resources#restrictions>`__
            apply. Label names that start with "goog-" or "google-" are
            reserved.
        network (google.cloud.batch_v1.types.AllocationPolicy.NetworkPolicy):
            The network policy.
    """

    class ProvisioningModel(proto.Enum):
        r"""Compute Engine VM instance provisioning model."""
        PROVISIONING_MODEL_UNSPECIFIED = 0
        STANDARD = 1
        SPOT = 2
        PREEMPTIBLE = 3

    class LocationPolicy(proto.Message):
        r"""

        Attributes:
            allowed_locations (Sequence[str]):
                A list of allowed location names represented by internal
                URLs. Each location can be a region or a zone. Only one
                region or multiple zones in one region is supported now. For
                example, ["regions/us-central1"] allow VMs in any zones in
                region us-central1. ["zones/us-central1-a",
                "zones/us-central1-c"] only allow VMs in zones us-central1-a
                and us-central1-c. All locations end up in different regions
                would cause errors. For example, ["regions/us-central1",
                "zones/us-central1-a", "zones/us-central1-b",
                "zones/us-west1-a"] contains 2 regions "us-central1" and
                "us-west1". An error is expected in this case.
        """

        allowed_locations = proto.RepeatedField(
            proto.STRING,
            number=1,
        )

    class Disk(proto.Message):
        r"""A new persistent disk or a local ssd.
        A VM can only have one local SSD setting but multiple local SSD
        partitions. https://cloud.google.com/compute/docs/disks#pdspecs.
        https://cloud.google.com/compute/docs/disks#localssds.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            image (str):
                Name of a public or custom image used as the
                data source.

                This field is a member of `oneof`_ ``data_source``.
            snapshot (str):
                Name of a snapshot used as the data source.

                This field is a member of `oneof`_ ``data_source``.
            type_ (str):
                Disk type as shown in ``gcloud compute disk-types list`` For
                example, "pd-ssd", "pd-standard", "pd-balanced",
                "local-ssd".
            size_gb (int):
                Disk size in GB. This field is ignored if ``data_source`` is
                ``disk`` or ``image``. If ``type`` is ``local-ssd``, size_gb
                should be a multiple of 375GB, otherwise, the final size
                will be the next greater multiple of 375 GB.
            disk_interface (str):
                Local SSDs are available through both "SCSI"
                and "NVMe" interfaces. If not indicated, "NVMe"
                will be the default one for local ssds. We only
                support "SCSI" for persistent disks now.
        """

        image = proto.Field(
            proto.STRING,
            number=4,
            oneof="data_source",
        )
        snapshot = proto.Field(
            proto.STRING,
            number=5,
            oneof="data_source",
        )
        type_ = proto.Field(
            proto.STRING,
            number=1,
        )
        size_gb = proto.Field(
            proto.INT64,
            number=2,
        )
        disk_interface = proto.Field(
            proto.STRING,
            number=6,
        )

    class AttachedDisk(proto.Message):
        r"""A new or an existing persistent disk or a local ssd attached
        to a VM instance.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            new_disk (google.cloud.batch_v1.types.AllocationPolicy.Disk):

                This field is a member of `oneof`_ ``attached``.
            existing_disk (str):
                Name of an existing PD.

                This field is a member of `oneof`_ ``attached``.
            device_name (str):
                Device name that the guest operating system
                will see. If not specified, this is default to
                the disk name.
        """

        new_disk = proto.Field(
            proto.MESSAGE,
            number=1,
            oneof="attached",
            message="AllocationPolicy.Disk",
        )
        existing_disk = proto.Field(
            proto.STRING,
            number=2,
            oneof="attached",
        )
        device_name = proto.Field(
            proto.STRING,
            number=3,
        )

    class Accelerator(proto.Message):
        r"""Accelerator describes Compute Engine accelerators to be
        attached to VMs.

        Attributes:
            type_ (str):
                The accelerator type. For example, "nvidia-tesla-t4". See
                ``gcloud compute accelerator-types list``.
            count (int):
                The number of accelerators of this type.
            install_gpu_drivers (bool):
                When true, Batch will install the GPU
                drivers. This field will be ignored if
                specified.
        """

        type_ = proto.Field(
            proto.STRING,
            number=1,
        )
        count = proto.Field(
            proto.INT64,
            number=2,
        )
        install_gpu_drivers = proto.Field(
            proto.BOOL,
            number=3,
        )

    class InstancePolicy(proto.Message):
        r"""InstancePolicy describes an instance type and resources
        attached to each VM created by this InstancePolicy.

        Attributes:
            machine_type (str):
                The Compute Engine machine type.
            min_cpu_platform (str):
                The minimum CPU platform. See
                ``https://cloud.google.com/compute/docs/instances/specify-min-cpu-platform``.
                Not yet implemented.
            provisioning_model (google.cloud.batch_v1.types.AllocationPolicy.ProvisioningModel):
                The provisioning model.
            accelerators (Sequence[google.cloud.batch_v1.types.AllocationPolicy.Accelerator]):
                The accelerators attached to each VM
                instance. Not yet implemented.
            disks (Sequence[google.cloud.batch_v1.types.AllocationPolicy.AttachedDisk]):
                Non-boot disks to be attached for each VM
                created by this InstancePolicy. New disks will
                be deleted when the attached VM is deleted.
        """

        machine_type = proto.Field(
            proto.STRING,
            number=2,
        )
        min_cpu_platform = proto.Field(
            proto.STRING,
            number=3,
        )
        provisioning_model = proto.Field(
            proto.ENUM,
            number=4,
            enum="AllocationPolicy.ProvisioningModel",
        )
        accelerators = proto.RepeatedField(
            proto.MESSAGE,
            number=5,
            message="AllocationPolicy.Accelerator",
        )
        disks = proto.RepeatedField(
            proto.MESSAGE,
            number=6,
            message="AllocationPolicy.AttachedDisk",
        )

    class InstancePolicyOrTemplate(proto.Message):
        r"""Either an InstancePolicy or an instance template.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            policy (google.cloud.batch_v1.types.AllocationPolicy.InstancePolicy):
                InstancePolicy.

                This field is a member of `oneof`_ ``policy_template``.
            instance_template (str):
                Name of an instance template used to create VMs. Named the
                field as 'instance_template' instead of 'template' to avoid
                c++ keyword conflict.

                This field is a member of `oneof`_ ``policy_template``.
        """

        policy = proto.Field(
            proto.MESSAGE,
            number=1,
            oneof="policy_template",
            message="AllocationPolicy.InstancePolicy",
        )
        instance_template = proto.Field(
            proto.STRING,
            number=2,
            oneof="policy_template",
        )

    class NetworkInterface(proto.Message):
        r"""A network interface.

        Attributes:
            network (str):
                The URL of the network resource.
            subnetwork (str):
                The URL of the Subnetwork resource.
            no_external_ip_address (bool):
                Default is false (with an external IP
                address). Required if no external public IP
                address is attached to the VM. If no external
                public IP address, additional configuration is
                required to allow the VM to access Google
                Services. See
                https://cloud.google.com/vpc/docs/configure-private-google-access
                and
                https://cloud.google.com/nat/docs/gce-example#create-nat
                for more information.
        """

        network = proto.Field(
            proto.STRING,
            number=1,
        )
        subnetwork = proto.Field(
            proto.STRING,
            number=2,
        )
        no_external_ip_address = proto.Field(
            proto.BOOL,
            number=3,
        )

    class NetworkPolicy(proto.Message):
        r"""NetworkPolicy describes VM instance network configurations.

        Attributes:
            network_interfaces (Sequence[google.cloud.batch_v1.types.AllocationPolicy.NetworkInterface]):
                Network configurations.
        """

        network_interfaces = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="AllocationPolicy.NetworkInterface",
        )

    location = proto.Field(
        proto.MESSAGE,
        number=1,
        message=LocationPolicy,
    )
    instances = proto.RepeatedField(
        proto.MESSAGE,
        number=8,
        message=InstancePolicyOrTemplate,
    )
    labels = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=6,
    )
    network = proto.Field(
        proto.MESSAGE,
        number=7,
        message=NetworkPolicy,
    )


class TaskGroup(proto.Message):
    r"""A TaskGroup contains one or multiple Tasks that share the
    same Runnable but with different runtime parameters.

    Attributes:
        name (str):
            Output only. TaskGroup name.
            The system generates this field based on parent
            Job name. For example:
            "projects/123456/locations/us-west1/jobs/job01/taskGroups/group01".
        task_spec (google.cloud.batch_v1.types.TaskSpec):
            Required. Tasks in the group share the same
            task spec.
        task_count (int):
            Number of Tasks in the TaskGroup.
            default is 1
        parallelism (int):
            Max number of tasks that can run in parallel. Default to
            min(task_count, 1000).
        task_environments (Sequence[google.cloud.batch_v1.types.Environment]):
            An array of environment variable mappings, which are passed
            to Tasks with matching indices. If task_environments is used
            then task_count should not be specified in the request (and
            will be ignored). Task count will be the length of
            task_environments.

            Tasks get a BATCH_TASK_INDEX and BATCH_TASK_COUNT
            environment variable, in addition to any environment
            variables set in task_environments, specifying the number of
            Tasks in the Task's parent TaskGroup, and the specific
            Task's index in the TaskGroup (0 through BATCH_TASK_COUNT -
            1).

            task_environments supports up to 200 entries.
        task_count_per_node (int):
            Max number of tasks that can be run on a VM
            at the same time. If not specified, the system
            will decide a value based on available compute
            resources on a VM and task requirements.
        require_hosts_file (bool):
            When true, Batch will populate a file with a list of all VMs
            assigned to the TaskGroup and set the BATCH_HOSTS_FILE
            environment variable to the path of that file. Defaults to
            false.
        permissive_ssh (bool):
            When true, Batch will configure SSH to allow
            passwordless login between VMs running the Batch
            tasks in the same TaskGroup.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    task_spec = proto.Field(
        proto.MESSAGE,
        number=3,
        message=task.TaskSpec,
    )
    task_count = proto.Field(
        proto.INT64,
        number=4,
    )
    parallelism = proto.Field(
        proto.INT64,
        number=5,
    )
    task_environments = proto.RepeatedField(
        proto.MESSAGE,
        number=9,
        message=task.Environment,
    )
    task_count_per_node = proto.Field(
        proto.INT64,
        number=10,
    )
    require_hosts_file = proto.Field(
        proto.BOOL,
        number=11,
    )
    permissive_ssh = proto.Field(
        proto.BOOL,
        number=12,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
