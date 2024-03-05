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

from google.rpc import status_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.dataflow_v1beta3.types import environment as gd_environment
from google.cloud.dataflow_v1beta3.types import jobs

__protobuf__ = proto.module(
    package="google.dataflow.v1beta3",
    manifest={
        "ParameterType",
        "LaunchFlexTemplateResponse",
        "ContainerSpec",
        "LaunchFlexTemplateParameter",
        "FlexTemplateRuntimeEnvironment",
        "LaunchFlexTemplateRequest",
        "RuntimeEnvironment",
        "ParameterMetadata",
        "TemplateMetadata",
        "SDKInfo",
        "RuntimeMetadata",
        "CreateJobFromTemplateRequest",
        "GetTemplateRequest",
        "GetTemplateResponse",
        "LaunchTemplateParameters",
        "LaunchTemplateRequest",
        "LaunchTemplateResponse",
        "InvalidTemplateParameters",
        "DynamicTemplateLaunchParams",
    },
)


class ParameterType(proto.Enum):
    r"""ParameterType specifies what kind of input we need for this
    parameter.

    Values:
        DEFAULT (0):
            Default input type.
        TEXT (1):
            The parameter specifies generic text input.
        GCS_READ_BUCKET (2):
            The parameter specifies a Cloud Storage
            Bucket to read from.
        GCS_WRITE_BUCKET (3):
            The parameter specifies a Cloud Storage
            Bucket to write to.
        GCS_READ_FILE (4):
            The parameter specifies a Cloud Storage file
            path to read from.
        GCS_WRITE_FILE (5):
            The parameter specifies a Cloud Storage file
            path to write to.
        GCS_READ_FOLDER (6):
            The parameter specifies a Cloud Storage
            folder path to read from.
        GCS_WRITE_FOLDER (7):
            The parameter specifies a Cloud Storage
            folder to write to.
        PUBSUB_TOPIC (8):
            The parameter specifies a Pub/Sub Topic.
        PUBSUB_SUBSCRIPTION (9):
            The parameter specifies a Pub/Sub
            Subscription.
    """
    DEFAULT = 0
    TEXT = 1
    GCS_READ_BUCKET = 2
    GCS_WRITE_BUCKET = 3
    GCS_READ_FILE = 4
    GCS_WRITE_FILE = 5
    GCS_READ_FOLDER = 6
    GCS_WRITE_FOLDER = 7
    PUBSUB_TOPIC = 8
    PUBSUB_SUBSCRIPTION = 9


class LaunchFlexTemplateResponse(proto.Message):
    r"""Response to the request to launch a job from Flex Template.

    Attributes:
        job (google.cloud.dataflow_v1beta3.types.Job):
            The job that was launched, if the request was
            not a dry run and the job was successfully
            launched.
    """

    job: jobs.Job = proto.Field(
        proto.MESSAGE,
        number=1,
        message=jobs.Job,
    )


class ContainerSpec(proto.Message):
    r"""Container Spec.

    Attributes:
        image (str):
            Name of the docker container image. E.g.,
            gcr.io/project/some-image
        metadata (google.cloud.dataflow_v1beta3.types.TemplateMetadata):
            Metadata describing a template including
            description and validation rules.
        sdk_info (google.cloud.dataflow_v1beta3.types.SDKInfo):
            Required. SDK info of the Flex Template.
        default_environment (google.cloud.dataflow_v1beta3.types.FlexTemplateRuntimeEnvironment):
            Default runtime environment for the job.
    """

    image: str = proto.Field(
        proto.STRING,
        number=1,
    )
    metadata: "TemplateMetadata" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="TemplateMetadata",
    )
    sdk_info: "SDKInfo" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="SDKInfo",
    )
    default_environment: "FlexTemplateRuntimeEnvironment" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="FlexTemplateRuntimeEnvironment",
    )


class LaunchFlexTemplateParameter(proto.Message):
    r"""Launch FlexTemplate Parameter.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        job_name (str):
            Required. The job name to use for the created
            job. For update job request, job name should be
            same as the existing running job.
        container_spec (google.cloud.dataflow_v1beta3.types.ContainerSpec):
            Spec about the container image to launch.

            This field is a member of `oneof`_ ``template``.
        container_spec_gcs_path (str):
            Cloud Storage path to a file with json
            serialized ContainerSpec as content.

            This field is a member of `oneof`_ ``template``.
        parameters (MutableMapping[str, str]):
            The parameters for FlexTemplate. Ex. {"num_workers":"5"}
        launch_options (MutableMapping[str, str]):
            Launch options for this flex template job.
            This is a common set of options across languages
            and templates. This should not be used to pass
            job parameters.
        environment (google.cloud.dataflow_v1beta3.types.FlexTemplateRuntimeEnvironment):
            The runtime environment for the FlexTemplate
            job
        update (bool):
            Set this to true if you are sending a request
            to update a running streaming job. When set, the
            job name should be the same as the running job.
        transform_name_mappings (MutableMapping[str, str]):
            Use this to pass transform_name_mappings for streaming
            update jobs. Ex:{"oldTransformName":"newTransformName",...}'
    """

    job_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    container_spec: "ContainerSpec" = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="template",
        message="ContainerSpec",
    )
    container_spec_gcs_path: str = proto.Field(
        proto.STRING,
        number=5,
        oneof="template",
    )
    parameters: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=2,
    )
    launch_options: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=6,
    )
    environment: "FlexTemplateRuntimeEnvironment" = proto.Field(
        proto.MESSAGE,
        number=7,
        message="FlexTemplateRuntimeEnvironment",
    )
    update: bool = proto.Field(
        proto.BOOL,
        number=8,
    )
    transform_name_mappings: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=9,
    )


class FlexTemplateRuntimeEnvironment(proto.Message):
    r"""The environment values to be set at runtime for flex
    template.

    Attributes:
        num_workers (int):
            The initial number of Google Compute Engine
            instances for the job.
        max_workers (int):
            The maximum number of Google Compute Engine
            instances to be made available to your pipeline
            during execution, from 1 to 1000.
        zone (str):
            The Compute Engine `availability
            zone <https://cloud.google.com/compute/docs/regions-zones/regions-zones>`__
            for launching worker instances to run your pipeline. In the
            future, worker_zone will take precedence.
        service_account_email (str):
            The email address of the service account to
            run the job as.
        temp_location (str):
            The Cloud Storage path to use for temporary files. Must be a
            valid Cloud Storage URL, beginning with ``gs://``.
        machine_type (str):
            The machine type to use for the job. Defaults
            to the value from the template if not specified.
        additional_experiments (MutableSequence[str]):
            Additional experiment flags for the job.
        network (str):
            Network to which VMs will be assigned.  If
            empty or unspecified, the service will use the
            network "default".
        subnetwork (str):
            Subnetwork to which VMs will be assigned, if desired. You
            can specify a subnetwork using either a complete URL or an
            abbreviated path. Expected to be of the form
            "https://www.googleapis.com/compute/v1/projects/HOST_PROJECT_ID/regions/REGION/subnetworks/SUBNETWORK"
            or "regions/REGION/subnetworks/SUBNETWORK". If the
            subnetwork is located in a Shared VPC network, you must use
            the complete URL.
        additional_user_labels (MutableMapping[str, str]):
            Additional user labels to be specified for the job. Keys and
            values must follow the restrictions specified in the
            `labeling
            restrictions <https://cloud.google.com/compute/docs/labeling-resources#restrictions>`__
            page. An object containing a list of "key": value pairs.
            Example: { "name": "wrench", "mass": "1kg", "count": "3" }.
        kms_key_name (str):
            Name for the Cloud KMS key for the job.
            Key format is:

            projects/<project>/locations/<location>/keyRings/<keyring>/cryptoKeys/<key>
        ip_configuration (google.cloud.dataflow_v1beta3.types.WorkerIPAddressConfiguration):
            Configuration for VM IPs.
        worker_region (str):
            The Compute Engine region
            (https://cloud.google.com/compute/docs/regions-zones/regions-zones)
            in which worker processing should occur, e.g. "us-west1".
            Mutually exclusive with worker_zone. If neither
            worker_region nor worker_zone is specified, default to the
            control plane's region.
        worker_zone (str):
            The Compute Engine zone
            (https://cloud.google.com/compute/docs/regions-zones/regions-zones)
            in which worker processing should occur, e.g. "us-west1-a".
            Mutually exclusive with worker_region. If neither
            worker_region nor worker_zone is specified, a zone in the
            control plane's region is chosen based on available
            capacity. If both ``worker_zone`` and ``zone`` are set,
            ``worker_zone`` takes precedence.
        enable_streaming_engine (bool):
            Whether to enable Streaming Engine for the
            job.
        flexrs_goal (google.cloud.dataflow_v1beta3.types.FlexResourceSchedulingGoal):
            Set FlexRS goal for the job.
            https://cloud.google.com/dataflow/docs/guides/flexrs
        staging_location (str):
            The Cloud Storage path for staging local files. Must be a
            valid Cloud Storage URL, beginning with ``gs://``.
        sdk_container_image (str):
            Docker registry location of container image
            to use for the 'worker harness. Default is the
            container for the version of the SDK. Note this
            field is only valid for portable pipelines.
        disk_size_gb (int):
            Worker disk size, in gigabytes.
        autoscaling_algorithm (google.cloud.dataflow_v1beta3.types.AutoscalingAlgorithm):
            The algorithm to use for autoscaling
        dump_heap_on_oom (bool):
            If true, save a heap dump before killing a
            thread or process which is GC thrashing or out
            of memory. The location of the heap file will
            either be echoed back to the user, or the user
            will be given the opportunity to download the
            heap file.
        save_heap_dumps_to_gcs_path (str):
            Cloud Storage bucket (directory) to upload heap dumps to the
            given location. Enabling this implies that heap dumps should
            be generated on OOM (dump_heap_on_oom is set to true).
        launcher_machine_type (str):
            The machine type to use for launching the
            job. The default is n1-standard-1.
    """

    num_workers: int = proto.Field(
        proto.INT32,
        number=1,
    )
    max_workers: int = proto.Field(
        proto.INT32,
        number=2,
    )
    zone: str = proto.Field(
        proto.STRING,
        number=3,
    )
    service_account_email: str = proto.Field(
        proto.STRING,
        number=4,
    )
    temp_location: str = proto.Field(
        proto.STRING,
        number=5,
    )
    machine_type: str = proto.Field(
        proto.STRING,
        number=6,
    )
    additional_experiments: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=7,
    )
    network: str = proto.Field(
        proto.STRING,
        number=8,
    )
    subnetwork: str = proto.Field(
        proto.STRING,
        number=9,
    )
    additional_user_labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=10,
    )
    kms_key_name: str = proto.Field(
        proto.STRING,
        number=11,
    )
    ip_configuration: gd_environment.WorkerIPAddressConfiguration = proto.Field(
        proto.ENUM,
        number=12,
        enum=gd_environment.WorkerIPAddressConfiguration,
    )
    worker_region: str = proto.Field(
        proto.STRING,
        number=13,
    )
    worker_zone: str = proto.Field(
        proto.STRING,
        number=14,
    )
    enable_streaming_engine: bool = proto.Field(
        proto.BOOL,
        number=15,
    )
    flexrs_goal: gd_environment.FlexResourceSchedulingGoal = proto.Field(
        proto.ENUM,
        number=16,
        enum=gd_environment.FlexResourceSchedulingGoal,
    )
    staging_location: str = proto.Field(
        proto.STRING,
        number=17,
    )
    sdk_container_image: str = proto.Field(
        proto.STRING,
        number=18,
    )
    disk_size_gb: int = proto.Field(
        proto.INT32,
        number=20,
    )
    autoscaling_algorithm: gd_environment.AutoscalingAlgorithm = proto.Field(
        proto.ENUM,
        number=21,
        enum=gd_environment.AutoscalingAlgorithm,
    )
    dump_heap_on_oom: bool = proto.Field(
        proto.BOOL,
        number=22,
    )
    save_heap_dumps_to_gcs_path: str = proto.Field(
        proto.STRING,
        number=23,
    )
    launcher_machine_type: str = proto.Field(
        proto.STRING,
        number=24,
    )


class LaunchFlexTemplateRequest(proto.Message):
    r"""A request to launch a Cloud Dataflow job from a FlexTemplate.

    Attributes:
        project_id (str):
            Required. The ID of the Cloud Platform
            project that the job belongs to.
        launch_parameter (google.cloud.dataflow_v1beta3.types.LaunchFlexTemplateParameter):
            Required. Parameter to launch a job form Flex
            Template.
        location (str):
            Required. The [regional endpoint]
            (https://cloud.google.com/dataflow/docs/concepts/regional-endpoints)
            to which to direct the request. E.g., us-central1, us-west1.
        validate_only (bool):
            If true, the request is validated but not
            actually executed. Defaults to false.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    launch_parameter: "LaunchFlexTemplateParameter" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="LaunchFlexTemplateParameter",
    )
    location: str = proto.Field(
        proto.STRING,
        number=3,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=4,
    )


class RuntimeEnvironment(proto.Message):
    r"""The environment values to set at runtime.

    Attributes:
        num_workers (int):
            The initial number of Google Compute Engine
            instnaces for the job.
        max_workers (int):
            The maximum number of Google Compute Engine
            instances to be made available to your pipeline
            during execution, from 1 to 1000.
        zone (str):
            The Compute Engine `availability
            zone <https://cloud.google.com/compute/docs/regions-zones/regions-zones>`__
            for launching worker instances to run your pipeline. In the
            future, worker_zone will take precedence.
        service_account_email (str):
            The email address of the service account to
            run the job as.
        temp_location (str):
            The Cloud Storage path to use for temporary files. Must be a
            valid Cloud Storage URL, beginning with ``gs://``.
        bypass_temp_dir_validation (bool):
            Whether to bypass the safety checks for the
            job's temporary directory. Use with caution.
        machine_type (str):
            The machine type to use for the job. Defaults
            to the value from the template if not specified.
        additional_experiments (MutableSequence[str]):
            Additional experiment flags for the job, specified with the
            ``--experiments`` option.
        network (str):
            Network to which VMs will be assigned.  If
            empty or unspecified, the service will use the
            network "default".
        subnetwork (str):
            Subnetwork to which VMs will be assigned, if desired. You
            can specify a subnetwork using either a complete URL or an
            abbreviated path. Expected to be of the form
            "https://www.googleapis.com/compute/v1/projects/HOST_PROJECT_ID/regions/REGION/subnetworks/SUBNETWORK"
            or "regions/REGION/subnetworks/SUBNETWORK". If the
            subnetwork is located in a Shared VPC network, you must use
            the complete URL.
        additional_user_labels (MutableMapping[str, str]):
            Additional user labels to be specified for the job. Keys and
            values should follow the restrictions specified in the
            `labeling
            restrictions <https://cloud.google.com/compute/docs/labeling-resources#restrictions>`__
            page. An object containing a list of "key": value pairs.
            Example: { "name": "wrench", "mass": "1kg", "count": "3" }.
        kms_key_name (str):
            Name for the Cloud KMS key for the job.
            Key format is:

            projects/<project>/locations/<location>/keyRings/<keyring>/cryptoKeys/<key>
        ip_configuration (google.cloud.dataflow_v1beta3.types.WorkerIPAddressConfiguration):
            Configuration for VM IPs.
        worker_region (str):
            The Compute Engine region
            (https://cloud.google.com/compute/docs/regions-zones/regions-zones)
            in which worker processing should occur, e.g. "us-west1".
            Mutually exclusive with worker_zone. If neither
            worker_region nor worker_zone is specified, default to the
            control plane's region.
        worker_zone (str):
            The Compute Engine zone
            (https://cloud.google.com/compute/docs/regions-zones/regions-zones)
            in which worker processing should occur, e.g. "us-west1-a".
            Mutually exclusive with worker_region. If neither
            worker_region nor worker_zone is specified, a zone in the
            control plane's region is chosen based on available
            capacity. If both ``worker_zone`` and ``zone`` are set,
            ``worker_zone`` takes precedence.
        enable_streaming_engine (bool):
            Whether to enable Streaming Engine for the
            job.
    """

    num_workers: int = proto.Field(
        proto.INT32,
        number=11,
    )
    max_workers: int = proto.Field(
        proto.INT32,
        number=1,
    )
    zone: str = proto.Field(
        proto.STRING,
        number=2,
    )
    service_account_email: str = proto.Field(
        proto.STRING,
        number=3,
    )
    temp_location: str = proto.Field(
        proto.STRING,
        number=4,
    )
    bypass_temp_dir_validation: bool = proto.Field(
        proto.BOOL,
        number=5,
    )
    machine_type: str = proto.Field(
        proto.STRING,
        number=6,
    )
    additional_experiments: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=7,
    )
    network: str = proto.Field(
        proto.STRING,
        number=8,
    )
    subnetwork: str = proto.Field(
        proto.STRING,
        number=9,
    )
    additional_user_labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=10,
    )
    kms_key_name: str = proto.Field(
        proto.STRING,
        number=12,
    )
    ip_configuration: gd_environment.WorkerIPAddressConfiguration = proto.Field(
        proto.ENUM,
        number=14,
        enum=gd_environment.WorkerIPAddressConfiguration,
    )
    worker_region: str = proto.Field(
        proto.STRING,
        number=15,
    )
    worker_zone: str = proto.Field(
        proto.STRING,
        number=16,
    )
    enable_streaming_engine: bool = proto.Field(
        proto.BOOL,
        number=17,
    )


class ParameterMetadata(proto.Message):
    r"""Metadata for a specific parameter.

    Attributes:
        name (str):
            Required. The name of the parameter.
        label (str):
            Required. The label to display for the
            parameter.
        help_text (str):
            Required. The help text to display for the
            parameter.
        is_optional (bool):
            Optional. Whether the parameter is optional.
            Defaults to false.
        regexes (MutableSequence[str]):
            Optional. Regexes that the parameter must
            match.
        param_type (google.cloud.dataflow_v1beta3.types.ParameterType):
            Optional. The type of the parameter.
            Used for selecting input picker.
        custom_metadata (MutableMapping[str, str]):
            Optional. Additional metadata for describing
            this parameter.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    label: str = proto.Field(
        proto.STRING,
        number=2,
    )
    help_text: str = proto.Field(
        proto.STRING,
        number=3,
    )
    is_optional: bool = proto.Field(
        proto.BOOL,
        number=4,
    )
    regexes: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=5,
    )
    param_type: "ParameterType" = proto.Field(
        proto.ENUM,
        number=6,
        enum="ParameterType",
    )
    custom_metadata: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=7,
    )


class TemplateMetadata(proto.Message):
    r"""Metadata describing a template.

    Attributes:
        name (str):
            Required. The name of the template.
        description (str):
            Optional. A description of the template.
        parameters (MutableSequence[google.cloud.dataflow_v1beta3.types.ParameterMetadata]):
            The parameters for the template.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    description: str = proto.Field(
        proto.STRING,
        number=2,
    )
    parameters: MutableSequence["ParameterMetadata"] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message="ParameterMetadata",
    )


class SDKInfo(proto.Message):
    r"""SDK Information.

    Attributes:
        language (google.cloud.dataflow_v1beta3.types.SDKInfo.Language):
            Required. The SDK Language.
        version (str):
            Optional. The SDK version.
    """

    class Language(proto.Enum):
        r"""SDK Language.

        Values:
            UNKNOWN (0):
                UNKNOWN Language.
            JAVA (1):
                Java.
            PYTHON (2):
                Python.
        """
        UNKNOWN = 0
        JAVA = 1
        PYTHON = 2

    language: Language = proto.Field(
        proto.ENUM,
        number=1,
        enum=Language,
    )
    version: str = proto.Field(
        proto.STRING,
        number=2,
    )


class RuntimeMetadata(proto.Message):
    r"""RuntimeMetadata describing a runtime environment.

    Attributes:
        sdk_info (google.cloud.dataflow_v1beta3.types.SDKInfo):
            SDK Info for the template.
        parameters (MutableSequence[google.cloud.dataflow_v1beta3.types.ParameterMetadata]):
            The parameters for the template.
    """

    sdk_info: "SDKInfo" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="SDKInfo",
    )
    parameters: MutableSequence["ParameterMetadata"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="ParameterMetadata",
    )


class CreateJobFromTemplateRequest(proto.Message):
    r"""A request to create a Cloud Dataflow job from a template.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        project_id (str):
            Required. The ID of the Cloud Platform
            project that the job belongs to.
        job_name (str):
            Required. The job name to use for the created
            job.
        gcs_path (str):
            Required. A Cloud Storage path to the template from which to
            create the job. Must be a valid Cloud Storage URL, beginning
            with ``gs://``.

            This field is a member of `oneof`_ ``template``.
        parameters (MutableMapping[str, str]):
            The runtime parameters to pass to the job.
        environment (google.cloud.dataflow_v1beta3.types.RuntimeEnvironment):
            The runtime environment for the job.
        location (str):
            The [regional endpoint]
            (https://cloud.google.com/dataflow/docs/concepts/regional-endpoints)
            to which to direct the request.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    job_name: str = proto.Field(
        proto.STRING,
        number=4,
    )
    gcs_path: str = proto.Field(
        proto.STRING,
        number=2,
        oneof="template",
    )
    parameters: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=3,
    )
    environment: "RuntimeEnvironment" = proto.Field(
        proto.MESSAGE,
        number=5,
        message="RuntimeEnvironment",
    )
    location: str = proto.Field(
        proto.STRING,
        number=6,
    )


class GetTemplateRequest(proto.Message):
    r"""A request to retrieve a Cloud Dataflow job template.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        project_id (str):
            Required. The ID of the Cloud Platform
            project that the job belongs to.
        gcs_path (str):
            Required. A Cloud Storage path to the
            template from which to create the job.
            Must be valid Cloud Storage URL, beginning with
            'gs://'.

            This field is a member of `oneof`_ ``template``.
        view (google.cloud.dataflow_v1beta3.types.GetTemplateRequest.TemplateView):
            The view to retrieve. Defaults to METADATA_ONLY.
        location (str):
            The [regional endpoint]
            (https://cloud.google.com/dataflow/docs/concepts/regional-endpoints)
            to which to direct the request.
    """

    class TemplateView(proto.Enum):
        r"""The various views of a template that may be retrieved.

        Values:
            METADATA_ONLY (0):
                Template view that retrieves only the
                metadata associated with the template.
        """
        METADATA_ONLY = 0

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    gcs_path: str = proto.Field(
        proto.STRING,
        number=2,
        oneof="template",
    )
    view: TemplateView = proto.Field(
        proto.ENUM,
        number=3,
        enum=TemplateView,
    )
    location: str = proto.Field(
        proto.STRING,
        number=4,
    )


class GetTemplateResponse(proto.Message):
    r"""The response to a GetTemplate request.

    Attributes:
        status (google.rpc.status_pb2.Status):
            The status of the get template request. Any problems with
            the request will be indicated in the error_details.
        metadata (google.cloud.dataflow_v1beta3.types.TemplateMetadata):
            The template metadata describing the template
            name, available parameters, etc.
        template_type (google.cloud.dataflow_v1beta3.types.GetTemplateResponse.TemplateType):
            Template Type.
        runtime_metadata (google.cloud.dataflow_v1beta3.types.RuntimeMetadata):
            Describes the runtime metadata with SDKInfo
            and available parameters.
    """

    class TemplateType(proto.Enum):
        r"""Template Type.

        Values:
            UNKNOWN (0):
                Unknown Template Type.
            LEGACY (1):
                Legacy Template.
            FLEX (2):
                Flex Template.
        """
        UNKNOWN = 0
        LEGACY = 1
        FLEX = 2

    status: status_pb2.Status = proto.Field(
        proto.MESSAGE,
        number=1,
        message=status_pb2.Status,
    )
    metadata: "TemplateMetadata" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="TemplateMetadata",
    )
    template_type: TemplateType = proto.Field(
        proto.ENUM,
        number=3,
        enum=TemplateType,
    )
    runtime_metadata: "RuntimeMetadata" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="RuntimeMetadata",
    )


class LaunchTemplateParameters(proto.Message):
    r"""Parameters to provide to the template being launched.

    Attributes:
        job_name (str):
            Required. The job name to use for the created
            job.
        parameters (MutableMapping[str, str]):
            The runtime parameters to pass to the job.
        environment (google.cloud.dataflow_v1beta3.types.RuntimeEnvironment):
            The runtime environment for the job.
        update (bool):
            If set, replace the existing pipeline with
            the name specified by jobName with this
            pipeline, preserving state.
        transform_name_mapping (MutableMapping[str, str]):
            Only applicable when updating a pipeline. Map
            of transform name prefixes of the job to be
            replaced to the corresponding name prefixes of
            the new job.
    """

    job_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    parameters: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=2,
    )
    environment: "RuntimeEnvironment" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="RuntimeEnvironment",
    )
    update: bool = proto.Field(
        proto.BOOL,
        number=4,
    )
    transform_name_mapping: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=5,
    )


class LaunchTemplateRequest(proto.Message):
    r"""A request to launch a template.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        project_id (str):
            Required. The ID of the Cloud Platform
            project that the job belongs to.
        validate_only (bool):
            If true, the request is validated but not
            actually executed. Defaults to false.
        gcs_path (str):
            A Cloud Storage path to the template from
            which to create the job.
            Must be valid Cloud Storage URL, beginning with
            'gs://'.

            This field is a member of `oneof`_ ``template``.
        dynamic_template (google.cloud.dataflow_v1beta3.types.DynamicTemplateLaunchParams):
            Params for launching a dynamic template.

            This field is a member of `oneof`_ ``template``.
        launch_parameters (google.cloud.dataflow_v1beta3.types.LaunchTemplateParameters):
            The parameters of the template to launch.
            This should be part of the body of the POST
            request.
        location (str):
            The [regional endpoint]
            (https://cloud.google.com/dataflow/docs/concepts/regional-endpoints)
            to which to direct the request.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=2,
    )
    gcs_path: str = proto.Field(
        proto.STRING,
        number=3,
        oneof="template",
    )
    dynamic_template: "DynamicTemplateLaunchParams" = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="template",
        message="DynamicTemplateLaunchParams",
    )
    launch_parameters: "LaunchTemplateParameters" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="LaunchTemplateParameters",
    )
    location: str = proto.Field(
        proto.STRING,
        number=5,
    )


class LaunchTemplateResponse(proto.Message):
    r"""Response to the request to launch a template.

    Attributes:
        job (google.cloud.dataflow_v1beta3.types.Job):
            The job that was launched, if the request was
            not a dry run and the job was successfully
            launched.
    """

    job: jobs.Job = proto.Field(
        proto.MESSAGE,
        number=1,
        message=jobs.Job,
    )


class InvalidTemplateParameters(proto.Message):
    r"""Used in the error_details field of a google.rpc.Status message, this
    indicates problems with the template parameter.

    Attributes:
        parameter_violations (MutableSequence[google.cloud.dataflow_v1beta3.types.InvalidTemplateParameters.ParameterViolation]):
            Describes all parameter violations in a
            template request.
    """

    class ParameterViolation(proto.Message):
        r"""A specific template-parameter violation.

        Attributes:
            parameter (str):
                The parameter that failed to validate.
            description (str):
                A description of why the parameter failed to
                validate.
        """

        parameter: str = proto.Field(
            proto.STRING,
            number=1,
        )
        description: str = proto.Field(
            proto.STRING,
            number=2,
        )

    parameter_violations: MutableSequence[ParameterViolation] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=ParameterViolation,
    )


class DynamicTemplateLaunchParams(proto.Message):
    r"""Params which should be passed when launching a dynamic
    template.

    Attributes:
        gcs_path (str):
            Path to dynamic template spec file on Cloud
            Storage. The file must be a Json serialized
            DynamicTemplateFieSpec object.
        staging_location (str):
            Cloud Storage path for staging dependencies. Must be a valid
            Cloud Storage URL, beginning with ``gs://``.
    """

    gcs_path: str = proto.Field(
        proto.STRING,
        number=1,
    )
    staging_location: str = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
