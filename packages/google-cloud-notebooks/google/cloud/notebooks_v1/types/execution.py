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
    package="google.cloud.notebooks.v1", manifest={"ExecutionTemplate", "Execution",},
)


class ExecutionTemplate(proto.Message):
    r"""The description a notebook execution workload.
    Attributes:
        scale_tier (google.cloud.notebooks_v1.types.ExecutionTemplate.ScaleTier):
            Required. Scale tier of the hardware used for
            notebook execution. DEPRECATED Will be
            discontinued. As right now only CUSTOM is
            supported.
        master_type (str):
            Specifies the type of virtual machine to use for your
            training job's master worker. You must specify this field
            when ``scaleTier`` is set to ``CUSTOM``.

            You can use certain Compute Engine machine types directly in
            this field. The following types are supported:

            -  ``n1-standard-4``
            -  ``n1-standard-8``
            -  ``n1-standard-16``
            -  ``n1-standard-32``
            -  ``n1-standard-64``
            -  ``n1-standard-96``
            -  ``n1-highmem-2``
            -  ``n1-highmem-4``
            -  ``n1-highmem-8``
            -  ``n1-highmem-16``
            -  ``n1-highmem-32``
            -  ``n1-highmem-64``
            -  ``n1-highmem-96``
            -  ``n1-highcpu-16``
            -  ``n1-highcpu-32``
            -  ``n1-highcpu-64``
            -  ``n1-highcpu-96``

            Alternatively, you can use the following legacy machine
            types:

            -  ``standard``
            -  ``large_model``
            -  ``complex_model_s``
            -  ``complex_model_m``
            -  ``complex_model_l``
            -  ``standard_gpu``
            -  ``complex_model_m_gpu``
            -  ``complex_model_l_gpu``
            -  ``standard_p100``
            -  ``complex_model_m_p100``
            -  ``standard_v100``
            -  ``large_model_v100``
            -  ``complex_model_m_v100``
            -  ``complex_model_l_v100``

            Finally, if you want to use a TPU for training, specify
            ``cloud_tpu`` in this field. Learn more about the [special
            configuration options for training with TPU.
        accelerator_config (google.cloud.notebooks_v1.types.ExecutionTemplate.SchedulerAcceleratorConfig):
            Configuration (count and accelerator type)
            for hardware running notebook execution.
        labels (Sequence[google.cloud.notebooks_v1.types.ExecutionTemplate.LabelsEntry]):
            Labels for execution.
            If execution is scheduled, a field included will
            be 'nbs-scheduled'. Otherwise, it is an
            immediate execution, and an included field will
            be 'nbs-immediate'. Use fields to efficiently
            index between various types of executions.
        input_notebook_file (str):
            Path to the notebook file to execute. Must be in a Google
            Cloud Storage bucket. Format:
            ``gs://{project_id}/{folder}/{notebook_file_name}`` Ex:
            ``gs://notebook_user/scheduled_notebooks/sentiment_notebook.ipynb``
        container_image_uri (str):
            Container Image URI to a DLVM
            Example: 'gcr.io/deeplearning-platform-
            release/base-cu100' More examples can be found
            at:
            https://cloud.google.com/ai-platform/deep-
            learning-containers/docs/choosing-container
        output_notebook_folder (str):
            Path to the notebook folder to write to. Must be in a Google
            Cloud Storage bucket path. Format:
            ``gs://{project_id}/{folder}`` Ex:
            ``gs://notebook_user/scheduled_notebooks``
        params_yaml_file (str):
            Parameters to be overridden in the notebook during
            execution. Ref
            https://papermill.readthedocs.io/en/latest/usage-parameterize.html
            on how to specifying parameters in the input notebook and
            pass them here in an YAML file. Ex:
            ``gs://notebook_user/scheduled_notebooks/sentiment_notebook_params.yaml``
        parameters (str):
            Parameters used within the 'input_notebook_file' notebook.
        service_account (str):
            The email address of a service account to use when running
            the execution. You must have the
            ``iam.serviceAccounts.actAs`` permission for the specified
            service account.
        job_type (google.cloud.notebooks_v1.types.ExecutionTemplate.JobType):
            The type of Job to be used on this execution.
        dataproc_parameters (google.cloud.notebooks_v1.types.ExecutionTemplate.DataprocParameters):
            Parameters used in Dataproc JobType
            executions.
    """

    class ScaleTier(proto.Enum):
        r"""Required. Specifies the machine types, the number of replicas
        for workers and parameter servers.
        """
        SCALE_TIER_UNSPECIFIED = 0
        BASIC = 1
        STANDARD_1 = 2
        PREMIUM_1 = 3
        BASIC_GPU = 4
        BASIC_TPU = 5
        CUSTOM = 6

    class SchedulerAcceleratorType(proto.Enum):
        r"""Hardware accelerator types for AI Platform Training jobs."""
        SCHEDULER_ACCELERATOR_TYPE_UNSPECIFIED = 0
        NVIDIA_TESLA_K80 = 1
        NVIDIA_TESLA_P100 = 2
        NVIDIA_TESLA_V100 = 3
        NVIDIA_TESLA_P4 = 4
        NVIDIA_TESLA_T4 = 5
        TPU_V2 = 6
        TPU_V3 = 7

    class JobType(proto.Enum):
        r"""The backend used for this execution."""
        JOB_TYPE_UNSPECIFIED = 0
        VERTEX_AI = 1
        DATAPROC = 2

    class SchedulerAcceleratorConfig(proto.Message):
        r"""Definition of a hardware accelerator. Note that not all combinations
        of ``type`` and ``core_count`` are valid. Check GPUs on Compute
        Engine to find a valid combination. TPUs are not supported.

        Attributes:
            type_ (google.cloud.notebooks_v1.types.ExecutionTemplate.SchedulerAcceleratorType):
                Type of this accelerator.
            core_count (int):
                Count of cores of this accelerator.
        """

        type_ = proto.Field(
            proto.ENUM, number=1, enum="ExecutionTemplate.SchedulerAcceleratorType",
        )
        core_count = proto.Field(proto.INT64, number=2,)

    class DataprocParameters(proto.Message):
        r"""Parameters used in Dataproc JobType executions.
        Attributes:
            cluster (str):
                URI for cluster used to run Dataproc execution. Format:
                ``projects/{PROJECT_ID}/regions/{REGION}/clusters/{CLUSTER_NAME}``
        """

        cluster = proto.Field(proto.STRING, number=1,)

    scale_tier = proto.Field(proto.ENUM, number=1, enum=ScaleTier,)
    master_type = proto.Field(proto.STRING, number=2,)
    accelerator_config = proto.Field(
        proto.MESSAGE, number=3, message=SchedulerAcceleratorConfig,
    )
    labels = proto.MapField(proto.STRING, proto.STRING, number=4,)
    input_notebook_file = proto.Field(proto.STRING, number=5,)
    container_image_uri = proto.Field(proto.STRING, number=6,)
    output_notebook_folder = proto.Field(proto.STRING, number=7,)
    params_yaml_file = proto.Field(proto.STRING, number=8,)
    parameters = proto.Field(proto.STRING, number=9,)
    service_account = proto.Field(proto.STRING, number=10,)
    job_type = proto.Field(proto.ENUM, number=11, enum=JobType,)
    dataproc_parameters = proto.Field(
        proto.MESSAGE, number=12, oneof="job_parameters", message=DataprocParameters,
    )


class Execution(proto.Message):
    r"""The definition of a single executed notebook.
    Attributes:
        execution_template (google.cloud.notebooks_v1.types.ExecutionTemplate):
            execute metadata including name, hardware
            spec, region, labels, etc.
        name (str):
            Output only. The resource name of the execute. Format:
            ``projects/{project_id}/locations/{location}/execution/{execution_id}``
        display_name (str):
            Output only. Name used for UI purposes. Name can only
            contain alphanumeric characters and underscores '_'.
        description (str):
            A brief description of this execution.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time the Execution was
            instantiated.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time the Execution was last
            updated.
        state (google.cloud.notebooks_v1.types.Execution.State):
            Output only. State of the underlying AI
            Platform job.
        output_notebook_file (str):
            Output notebook file generated by this
            execution
        job_uri (str):
            Output only. The URI of the external job used
            to execute the notebook.
    """

    class State(proto.Enum):
        r"""Enum description of the state of the underlying AIP job."""
        STATE_UNSPECIFIED = 0
        QUEUED = 1
        PREPARING = 2
        RUNNING = 3
        SUCCEEDED = 4
        FAILED = 5
        CANCELLING = 6
        CANCELLED = 7
        EXPIRED = 9
        INITIALIZING = 10

    execution_template = proto.Field(
        proto.MESSAGE, number=1, message="ExecutionTemplate",
    )
    name = proto.Field(proto.STRING, number=2,)
    display_name = proto.Field(proto.STRING, number=3,)
    description = proto.Field(proto.STRING, number=4,)
    create_time = proto.Field(proto.MESSAGE, number=5, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=6, message=timestamp_pb2.Timestamp,)
    state = proto.Field(proto.ENUM, number=7, enum=State,)
    output_notebook_file = proto.Field(proto.STRING, number=8,)
    job_uri = proto.Field(proto.STRING, number=9,)


__all__ = tuple(sorted(__protobuf__.manifest))
