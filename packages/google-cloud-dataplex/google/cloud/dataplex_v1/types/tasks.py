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
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.dataplex_v1.types import resources

__protobuf__ = proto.module(
    package="google.cloud.dataplex.v1",
    manifest={
        "Task",
        "Job",
    },
)


class Task(proto.Message):
    r"""A task represents a user-visible job.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Output only. The relative resource name of the task, of the
            form:
            projects/{project_number}/locations/{location_id}/lakes/{lake_id}/
            tasks/{task_id}.
        uid (str):
            Output only. System generated globally unique
            ID for the task. This ID will be different if
            the task is deleted and re-created with the same
            name.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the task was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the task was last
            updated.
        description (str):
            Optional. Description of the task.
        display_name (str):
            Optional. User friendly display name.
        state (google.cloud.dataplex_v1.types.State):
            Output only. Current state of the task.
        labels (Mapping[str, str]):
            Optional. User-defined labels for the task.
        trigger_spec (google.cloud.dataplex_v1.types.Task.TriggerSpec):
            Required. Spec related to how often and when
            a task should be triggered.
        execution_spec (google.cloud.dataplex_v1.types.Task.ExecutionSpec):
            Required. Spec related to how a task is
            executed.
        spark (google.cloud.dataplex_v1.types.Task.SparkTaskConfig):
            Config related to running custom Spark tasks.

            This field is a member of `oneof`_ ``config``.
    """

    class InfrastructureSpec(proto.Message):
        r"""Configuration for the underlying infrastructure used to run
        workloads.


        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            batch (google.cloud.dataplex_v1.types.Task.InfrastructureSpec.BatchComputeResources):
                Compute resources needed for a Task when
                using Dataproc Serverless.

                This field is a member of `oneof`_ ``resources``.
            container_image (google.cloud.dataplex_v1.types.Task.InfrastructureSpec.ContainerImageRuntime):
                Container Image Runtime Configuration.

                This field is a member of `oneof`_ ``runtime``.
            vpc_network (google.cloud.dataplex_v1.types.Task.InfrastructureSpec.VpcNetwork):
                Vpc network.

                This field is a member of `oneof`_ ``network``.
        """

        class BatchComputeResources(proto.Message):
            r"""Batch compute resources associated with the task.

            Attributes:
                executors_count (int):
                    Optional. Total number of job executors.
                max_executors_count (int):
                    Optional. Max configurable executors. If max_executors_count
                    > executors_count, then auto-scaling is enabled.
            """

            executors_count = proto.Field(
                proto.INT32,
                number=1,
            )
            max_executors_count = proto.Field(
                proto.INT32,
                number=2,
            )

        class ContainerImageRuntime(proto.Message):
            r"""Container Image Runtime Configuration used with Batch
            execution.

            Attributes:
                java_jars (Sequence[str]):
                    Optional. A list of Java JARS to add to the classpath. Valid
                    input includes Cloud Storage URIs to Jar binaries. For
                    example, ``gs://bucket-name/my/path/to/file.jar``.
                python_packages (Sequence[str]):
                    Optional. A list of python packages to be installed. Valid
                    formats include Cloud Storage URI to a PIP installable
                    library. For example,
                    ``gs://bucket-name/my/path/to/lib.tar.gz``.
                properties (Mapping[str, str]):
                    Optional. Override to common configuration of open source
                    components installed on the Dataproc cluster. The properties
                    to set on daemon config files. Property keys are specified
                    in ``prefix:property`` format, for example
                    ``core:hadoop.tmp.dir``. For more information, see `Cluster
                    properties <https://cloud.google.com/dataproc/docs/concepts/cluster-properties>`__.
            """

            java_jars = proto.RepeatedField(
                proto.STRING,
                number=2,
            )
            python_packages = proto.RepeatedField(
                proto.STRING,
                number=3,
            )
            properties = proto.MapField(
                proto.STRING,
                proto.STRING,
                number=4,
            )

        class VpcNetwork(proto.Message):
            r"""Cloud VPC Network used to run the infrastructure.

            This message has `oneof`_ fields (mutually exclusive fields).
            For each oneof, at most one member field can be set at the same time.
            Setting any member of the oneof automatically clears all other
            members.

            .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

            Attributes:
                network (str):
                    Optional. The Cloud VPC network in which the
                    job is run. By default, the Cloud VPC network
                    named Default within the project is used.

                    This field is a member of `oneof`_ ``network_name``.
                sub_network (str):
                    Optional. The Cloud VPC sub-network in which
                    the job is run.

                    This field is a member of `oneof`_ ``network_name``.
                network_tags (Sequence[str]):
                    Optional. List of network tags to apply to
                    the job.
            """

            network = proto.Field(
                proto.STRING,
                number=1,
                oneof="network_name",
            )
            sub_network = proto.Field(
                proto.STRING,
                number=2,
                oneof="network_name",
            )
            network_tags = proto.RepeatedField(
                proto.STRING,
                number=3,
            )

        batch = proto.Field(
            proto.MESSAGE,
            number=52,
            oneof="resources",
            message="Task.InfrastructureSpec.BatchComputeResources",
        )
        container_image = proto.Field(
            proto.MESSAGE,
            number=101,
            oneof="runtime",
            message="Task.InfrastructureSpec.ContainerImageRuntime",
        )
        vpc_network = proto.Field(
            proto.MESSAGE,
            number=150,
            oneof="network",
            message="Task.InfrastructureSpec.VpcNetwork",
        )

    class TriggerSpec(proto.Message):
        r"""Task scheduling and trigger settings.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            type_ (google.cloud.dataplex_v1.types.Task.TriggerSpec.Type):
                Required. Immutable. Trigger type of the
                user-specified Task.
            start_time (google.protobuf.timestamp_pb2.Timestamp):
                Optional. The first run of the task will be after this time.
                If not specified, the task will run shortly after being
                submitted if ON_DEMAND and based on the schedule if
                RECURRING.
            disabled (bool):
                Optional. Prevent the task from executing.
                This does not cancel already running tasks. It
                is intended to temporarily disable RECURRING
                tasks.
            max_retries (int):
                Optional. Number of retry attempts before
                aborting. Set to zero to never attempt to retry
                a failed task.
            schedule (str):
                Optional. Cron schedule (https://en.wikipedia.org/wiki/Cron)
                for running tasks periodically. To explicitly set a timezone
                to the cron tab, apply a prefix in the cron tab:
                "CRON_TZ=${IANA_TIME_ZONE}" or "TZ=${IANA_TIME_ZONE}". The
                ${IANA_TIME_ZONE} may only be a valid string from IANA time
                zone database. For example, "CRON_TZ=America/New_York 1 \*
                \* \* \*", or "TZ=America/New_York 1 \* \* \* \*". This
                field is required for RECURRING tasks.

                This field is a member of `oneof`_ ``trigger``.
        """

        class Type(proto.Enum):
            r"""Determines how often and when the job will run."""
            TYPE_UNSPECIFIED = 0
            ON_DEMAND = 1
            RECURRING = 2

        type_ = proto.Field(
            proto.ENUM,
            number=5,
            enum="Task.TriggerSpec.Type",
        )
        start_time = proto.Field(
            proto.MESSAGE,
            number=6,
            message=timestamp_pb2.Timestamp,
        )
        disabled = proto.Field(
            proto.BOOL,
            number=4,
        )
        max_retries = proto.Field(
            proto.INT32,
            number=7,
        )
        schedule = proto.Field(
            proto.STRING,
            number=100,
            oneof="trigger",
        )

    class ExecutionSpec(proto.Message):
        r"""Execution related settings, like retry and service_account.

        Attributes:
            args (Mapping[str, str]):
                Optional. The arguments to pass to the task. The args can
                use placeholders of the format ${placeholder} as part of
                key/value string. These will be interpolated before passing
                the args to the driver. Currently supported placeholders:

                -  ${task_id}
                -  ${job_time} To pass positional args, set the key as
                   TASK_ARGS. The value should be a comma-separated string
                   of all the positional arguments. To use a delimiter other
                   than comma, refer to
                   https://cloud.google.com/sdk/gcloud/reference/topic/escaping.
                   In case of other keys being present in the args, then
                   TASK_ARGS will be passed as the last argument.
            service_account (str):
                Required. Service account to use to execute a
                task. If not provided, the default Compute
                service account for the project is used.
            max_job_execution_lifetime (google.protobuf.duration_pb2.Duration):
                Optional. The maximum duration after which
                the job execution is expired.
        """

        args = proto.MapField(
            proto.STRING,
            proto.STRING,
            number=4,
        )
        service_account = proto.Field(
            proto.STRING,
            number=5,
        )
        max_job_execution_lifetime = proto.Field(
            proto.MESSAGE,
            number=8,
            message=duration_pb2.Duration,
        )

    class SparkTaskConfig(proto.Message):
        r"""User-specified config for running a Spark task.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            main_jar_file_uri (str):
                The Cloud Storage URI of the jar file that contains the main
                class. The execution args are passed in as a sequence of
                named process arguments (``--key=value``).

                This field is a member of `oneof`_ ``driver``.
            main_class (str):
                The name of the driver's main class. The jar file that
                contains the class must be in the default CLASSPATH or
                specified in ``jar_file_uris``. The execution args are
                passed in as a sequence of named process arguments
                (``--key=value``).

                This field is a member of `oneof`_ ``driver``.
            python_script_file (str):
                The Gcloud Storage URI of the main Python file to use as the
                driver. Must be a .py file. The execution args are passed in
                as a sequence of named process arguments (``--key=value``).

                This field is a member of `oneof`_ ``driver``.
            sql_script_file (str):
                A reference to a query file. This can be the Cloud Storage
                URI of the query file or it can the path to a SqlScript
                Content. The execution args are used to declare a set of
                script variables (``set key="value";``).

                This field is a member of `oneof`_ ``driver``.
            sql_script (str):
                The query text. The execution args are used to declare a set
                of script variables (``set key="value";``).

                This field is a member of `oneof`_ ``driver``.
            file_uris (Sequence[str]):
                Optional. Cloud Storage URIs of files to be
                placed in the working directory of each
                executor.
            archive_uris (Sequence[str]):
                Optional. Cloud Storage URIs of archives to
                be extracted into the working directory of each
                executor. Supported file types: .jar, .tar,
                .tar.gz, .tgz, and .zip.
            infrastructure_spec (google.cloud.dataplex_v1.types.Task.InfrastructureSpec):
                Optional. Infrastructure specification for
                the execution.
        """

        main_jar_file_uri = proto.Field(
            proto.STRING,
            number=100,
            oneof="driver",
        )
        main_class = proto.Field(
            proto.STRING,
            number=101,
            oneof="driver",
        )
        python_script_file = proto.Field(
            proto.STRING,
            number=102,
            oneof="driver",
        )
        sql_script_file = proto.Field(
            proto.STRING,
            number=104,
            oneof="driver",
        )
        sql_script = proto.Field(
            proto.STRING,
            number=105,
            oneof="driver",
        )
        file_uris = proto.RepeatedField(
            proto.STRING,
            number=3,
        )
        archive_uris = proto.RepeatedField(
            proto.STRING,
            number=4,
        )
        infrastructure_spec = proto.Field(
            proto.MESSAGE,
            number=6,
            message="Task.InfrastructureSpec",
        )

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
    display_name = proto.Field(
        proto.STRING,
        number=6,
    )
    state = proto.Field(
        proto.ENUM,
        number=7,
        enum=resources.State,
    )
    labels = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=8,
    )
    trigger_spec = proto.Field(
        proto.MESSAGE,
        number=100,
        message=TriggerSpec,
    )
    execution_spec = proto.Field(
        proto.MESSAGE,
        number=101,
        message=ExecutionSpec,
    )
    spark = proto.Field(
        proto.MESSAGE,
        number=300,
        oneof="config",
        message=SparkTaskConfig,
    )


class Job(proto.Message):
    r"""A job represents an instance of a task.

    Attributes:
        name (str):
            Output only. The relative resource name of the job, of the
            form:
            ``projects/{project_number}/locations/{location_id}/lakes/{lake_id}/tasks/{task_id}/jobs/{job_id}``.
        uid (str):
            Output only. System generated globally unique
            ID for the job.
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the job was
            started.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the job ended.
        state (google.cloud.dataplex_v1.types.Job.State):
            Output only. Execution state for the job.
        retry_count (int):
            Output only. The number of times the job has
            been retried (excluding the initial attempt).
        service (google.cloud.dataplex_v1.types.Job.Service):
            Output only. The underlying service running a
            job.
        service_job (str):
            Output only. The full resource name for the
            job run under a particular service.
        message (str):
            Output only. Additional information about the
            current state.
    """

    class Service(proto.Enum):
        r""""""
        SERVICE_UNSPECIFIED = 0
        DATAPROC = 1

    class State(proto.Enum):
        r""""""
        STATE_UNSPECIFIED = 0
        RUNNING = 1
        CANCELLING = 2
        CANCELLED = 3
        SUCCEEDED = 4
        FAILED = 5
        ABORTED = 6

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    uid = proto.Field(
        proto.STRING,
        number=2,
    )
    start_time = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    end_time = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    state = proto.Field(
        proto.ENUM,
        number=5,
        enum=State,
    )
    retry_count = proto.Field(
        proto.UINT32,
        number=6,
    )
    service = proto.Field(
        proto.ENUM,
        number=7,
        enum=Service,
    )
    service_job = proto.Field(
        proto.STRING,
        number=8,
    )
    message = proto.Field(
        proto.STRING,
        number=9,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
