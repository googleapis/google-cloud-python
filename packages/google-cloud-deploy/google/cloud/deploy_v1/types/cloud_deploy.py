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
from google.type import date_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.deploy.v1",
    manifest={
        "SkaffoldSupportState",
        "DeliveryPipeline",
        "SerialPipeline",
        "Stage",
        "DeployParameters",
        "Strategy",
        "Standard",
        "Canary",
        "CanaryDeployment",
        "CustomCanaryDeployment",
        "KubernetesConfig",
        "CloudRunConfig",
        "RuntimeConfig",
        "PipelineReadyCondition",
        "TargetsPresentCondition",
        "TargetsTypeCondition",
        "PipelineCondition",
        "ListDeliveryPipelinesRequest",
        "ListDeliveryPipelinesResponse",
        "GetDeliveryPipelineRequest",
        "CreateDeliveryPipelineRequest",
        "UpdateDeliveryPipelineRequest",
        "DeleteDeliveryPipelineRequest",
        "Target",
        "ExecutionConfig",
        "DefaultPool",
        "PrivatePool",
        "GkeCluster",
        "AnthosCluster",
        "CloudRunLocation",
        "MultiTarget",
        "ListTargetsRequest",
        "ListTargetsResponse",
        "GetTargetRequest",
        "CreateTargetRequest",
        "UpdateTargetRequest",
        "DeleteTargetRequest",
        "Release",
        "BuildArtifact",
        "TargetArtifact",
        "DeployArtifact",
        "CloudRunRenderMetadata",
        "RenderMetadata",
        "ListReleasesRequest",
        "ListReleasesResponse",
        "GetReleaseRequest",
        "CreateReleaseRequest",
        "Rollout",
        "Metadata",
        "DeployJobRunMetadata",
        "CloudRunMetadata",
        "Phase",
        "DeploymentJobs",
        "ChildRolloutJobs",
        "Job",
        "DeployJob",
        "VerifyJob",
        "CreateChildRolloutJob",
        "AdvanceChildRolloutJob",
        "ListRolloutsRequest",
        "ListRolloutsResponse",
        "GetRolloutRequest",
        "CreateRolloutRequest",
        "OperationMetadata",
        "ApproveRolloutRequest",
        "ApproveRolloutResponse",
        "AdvanceRolloutRequest",
        "AdvanceRolloutResponse",
        "CancelRolloutRequest",
        "CancelRolloutResponse",
        "IgnoreJobRequest",
        "IgnoreJobResponse",
        "RetryJobRequest",
        "RetryJobResponse",
        "AbandonReleaseRequest",
        "AbandonReleaseResponse",
        "JobRun",
        "DeployJobRun",
        "VerifyJobRun",
        "CreateChildRolloutJobRun",
        "AdvanceChildRolloutJobRun",
        "ListJobRunsRequest",
        "ListJobRunsResponse",
        "GetJobRunRequest",
        "TerminateJobRunRequest",
        "TerminateJobRunResponse",
        "Config",
        "SkaffoldVersion",
        "GetConfigRequest",
    },
)


class SkaffoldSupportState(proto.Enum):
    r"""The support state of a specific Skaffold version.

    Values:
        SKAFFOLD_SUPPORT_STATE_UNSPECIFIED (0):
            Default value. This value is unused.
        SKAFFOLD_SUPPORT_STATE_SUPPORTED (1):
            This skaffold version is currently supported.
        SKAFFOLD_SUPPORT_STATE_MAINTENANCE_MODE (2):
            This skaffold version is in maintenance mode.
        SKAFFOLD_SUPPORT_STATE_UNSUPPORTED (3):
            This skaffold version is no longer supported.
    """
    SKAFFOLD_SUPPORT_STATE_UNSPECIFIED = 0
    SKAFFOLD_SUPPORT_STATE_SUPPORTED = 1
    SKAFFOLD_SUPPORT_STATE_MAINTENANCE_MODE = 2
    SKAFFOLD_SUPPORT_STATE_UNSUPPORTED = 3


class DeliveryPipeline(proto.Message):
    r"""A ``DeliveryPipeline`` resource in the Google Cloud Deploy API.

    A ``DeliveryPipeline`` defines a pipeline through which a Skaffold
    configuration can progress.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Optional. Name of the ``DeliveryPipeline``. Format is
            projects/{project}/
            locations/{location}/deliveryPipelines/[a-z][a-z0-9-]{0,62}.
        uid (str):
            Output only. Unique identifier of the ``DeliveryPipeline``.
        description (str):
            Description of the ``DeliveryPipeline``. Max length is 255
            characters.
        annotations (MutableMapping[str, str]):
            User annotations. These attributes can only
            be set and used by the user, and not by Google
            Cloud Deploy.
        labels (MutableMapping[str, str]):
            Labels are attributes that can be set and used by both the
            user and by Google Cloud Deploy. Labels must meet the
            following constraints:

            -  Keys and values can contain only lowercase letters,
               numeric characters, underscores, and dashes.
            -  All characters must use UTF-8 encoding, and international
               characters are allowed.
            -  Keys must start with a lowercase letter or international
               character.
            -  Each resource is limited to a maximum of 64 labels.

            Both keys and values are additionally constrained to be <=
            128 bytes.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time at which the pipeline was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Most recent time at which the
            pipeline was updated.
        serial_pipeline (google.cloud.deploy_v1.types.SerialPipeline):
            SerialPipeline defines a sequential set of stages for a
            ``DeliveryPipeline``.

            This field is a member of `oneof`_ ``pipeline``.
        condition (google.cloud.deploy_v1.types.PipelineCondition):
            Output only. Information around the state of
            the Delivery Pipeline.
        etag (str):
            This checksum is computed by the server based
            on the value of other fields, and may be sent on
            update and delete requests to ensure the client
            has an up-to-date value before proceeding.
        suspended (bool):
            When suspended, no new releases or rollouts
            can be created, but in-progress ones will
            complete.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=2,
    )
    description: str = proto.Field(
        proto.STRING,
        number=3,
    )
    annotations: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=4,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=5,
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
    serial_pipeline: "SerialPipeline" = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof="pipeline",
        message="SerialPipeline",
    )
    condition: "PipelineCondition" = proto.Field(
        proto.MESSAGE,
        number=11,
        message="PipelineCondition",
    )
    etag: str = proto.Field(
        proto.STRING,
        number=10,
    )
    suspended: bool = proto.Field(
        proto.BOOL,
        number=12,
    )


class SerialPipeline(proto.Message):
    r"""SerialPipeline defines a sequential set of stages for a
    ``DeliveryPipeline``.

    Attributes:
        stages (MutableSequence[google.cloud.deploy_v1.types.Stage]):
            Each stage specifies configuration for a ``Target``. The
            ordering of this list defines the promotion flow.
    """

    stages: MutableSequence["Stage"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Stage",
    )


class Stage(proto.Message):
    r"""Stage specifies a location to which to deploy.

    Attributes:
        target_id (str):
            The target_id to which this stage points. This field refers
            exclusively to the last segment of a target name. For
            example, this field would just be ``my-target`` (rather than
            ``projects/project/locations/location/targets/my-target``).
            The location of the ``Target`` is inferred to be the same as
            the location of the ``DeliveryPipeline`` that contains this
            ``Stage``.
        profiles (MutableSequence[str]):
            Skaffold profiles to use when rendering the manifest for
            this stage's ``Target``.
        strategy (google.cloud.deploy_v1.types.Strategy):
            Optional. The strategy to use for a ``Rollout`` to this
            stage.
        deploy_parameters (MutableSequence[google.cloud.deploy_v1.types.DeployParameters]):
            Optional. The deploy parameters to use for
            the target in this stage.
    """

    target_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    profiles: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )
    strategy: "Strategy" = proto.Field(
        proto.MESSAGE,
        number=5,
        message="Strategy",
    )
    deploy_parameters: MutableSequence["DeployParameters"] = proto.RepeatedField(
        proto.MESSAGE,
        number=6,
        message="DeployParameters",
    )


class DeployParameters(proto.Message):
    r"""DeployParameters contains deploy parameters information.

    Attributes:
        values (MutableMapping[str, str]):
            Required. Values are deploy parameters in
            key-value pairs.
        match_target_labels (MutableMapping[str, str]):
            Optional. Deploy parameters are applied to
            targets with match labels. If unspecified,
            deploy parameters are applied to all targets
            (including child targets of a multi-target).
    """

    values: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=1,
    )
    match_target_labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=2,
    )


class Strategy(proto.Message):
    r"""Strategy contains deployment strategy information.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        standard (google.cloud.deploy_v1.types.Standard):
            Standard deployment strategy executes a
            single deploy and allows verifying the
            deployment.

            This field is a member of `oneof`_ ``deployment_strategy``.
        canary (google.cloud.deploy_v1.types.Canary):
            Canary deployment strategy provides
            progressive percentage based deployments to a
            Target.

            This field is a member of `oneof`_ ``deployment_strategy``.
    """

    standard: "Standard" = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="deployment_strategy",
        message="Standard",
    )
    canary: "Canary" = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="deployment_strategy",
        message="Canary",
    )


class Standard(proto.Message):
    r"""Standard represents the standard deployment strategy.

    Attributes:
        verify (bool):
            Whether to verify a deployment.
    """

    verify: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


class Canary(proto.Message):
    r"""Canary represents the canary deployment strategy.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        runtime_config (google.cloud.deploy_v1.types.RuntimeConfig):
            Optional. Runtime specific configurations for
            the deployment strategy. The runtime
            configuration is used to determine how Cloud
            Deploy will split traffic to enable a
            progressive deployment.
        canary_deployment (google.cloud.deploy_v1.types.CanaryDeployment):
            Configures the progressive based deployment
            for a Target.

            This field is a member of `oneof`_ ``mode``.
        custom_canary_deployment (google.cloud.deploy_v1.types.CustomCanaryDeployment):
            Configures the progressive based deployment
            for a Target, but allows customizing at the
            phase level where a phase represents each of the
            percentage deployments.

            This field is a member of `oneof`_ ``mode``.
    """

    runtime_config: "RuntimeConfig" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="RuntimeConfig",
    )
    canary_deployment: "CanaryDeployment" = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="mode",
        message="CanaryDeployment",
    )
    custom_canary_deployment: "CustomCanaryDeployment" = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="mode",
        message="CustomCanaryDeployment",
    )


class CanaryDeployment(proto.Message):
    r"""CanaryDeployment represents the canary deployment
    configuration

    Attributes:
        percentages (MutableSequence[int]):
            Required. The percentage based deployments that will occur
            as a part of a ``Rollout``. List is expected in ascending
            order and each integer n is 0 <= n < 100.
        verify (bool):
            Whether to run verify tests after each
            percentage deployment.
    """

    percentages: MutableSequence[int] = proto.RepeatedField(
        proto.INT32,
        number=1,
    )
    verify: bool = proto.Field(
        proto.BOOL,
        number=2,
    )


class CustomCanaryDeployment(proto.Message):
    r"""CustomCanaryDeployment represents the custom canary
    deployment configuration.

    Attributes:
        phase_configs (MutableSequence[google.cloud.deploy_v1.types.CustomCanaryDeployment.PhaseConfig]):
            Required. Configuration for each phase in the
            canary deployment in the order executed.
    """

    class PhaseConfig(proto.Message):
        r"""PhaseConfig represents the configuration for a phase in the
        custom canary deployment.

        Attributes:
            phase_id (str):
                Required. The ID to assign to the ``Rollout`` phase. This
                value must consist of lower-case letters, numbers, and
                hyphens, start with a letter and end with a letter or a
                number, and have a max length of 63 characters. In other
                words, it must match the following regex:
                ``^[a-z]([a-z0-9-]{0,61}[a-z0-9])?$``.
            percentage (int):
                Required. Percentage deployment for the
                phase.
            profiles (MutableSequence[str]):
                Skaffold profiles to use when rendering the manifest for
                this phase. These are in addition to the profiles list
                specified in the ``DeliveryPipeline`` stage.
            verify (bool):
                Whether to run verify tests after the
                deployment.
        """

        phase_id: str = proto.Field(
            proto.STRING,
            number=1,
        )
        percentage: int = proto.Field(
            proto.INT32,
            number=2,
        )
        profiles: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=3,
        )
        verify: bool = proto.Field(
            proto.BOOL,
            number=4,
        )

    phase_configs: MutableSequence[PhaseConfig] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=PhaseConfig,
    )


class KubernetesConfig(proto.Message):
    r"""KubernetesConfig contains the Kubernetes runtime
    configuration.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        gateway_service_mesh (google.cloud.deploy_v1.types.KubernetesConfig.GatewayServiceMesh):
            Kubernetes Gateway API service mesh
            configuration.

            This field is a member of `oneof`_ ``service_definition``.
        service_networking (google.cloud.deploy_v1.types.KubernetesConfig.ServiceNetworking):
            Kubernetes Service networking configuration.

            This field is a member of `oneof`_ ``service_definition``.
    """

    class GatewayServiceMesh(proto.Message):
        r"""Information about the Kubernetes Gateway API service mesh
        configuration.

        Attributes:
            http_route (str):
                Required. Name of the Gateway API HTTPRoute.
            service (str):
                Required. Name of the Kubernetes Service.
            deployment (str):
                Required. Name of the Kubernetes Deployment
                whose traffic is managed by the specified
                HTTPRoute and Service.
            route_update_wait_time (google.protobuf.duration_pb2.Duration):
                Optional. The time to wait for route updates
                to propagate. The maximum configurable time is 3
                hours, in seconds format. If unspecified, there
                is no wait time.
        """

        http_route: str = proto.Field(
            proto.STRING,
            number=1,
        )
        service: str = proto.Field(
            proto.STRING,
            number=2,
        )
        deployment: str = proto.Field(
            proto.STRING,
            number=3,
        )
        route_update_wait_time: duration_pb2.Duration = proto.Field(
            proto.MESSAGE,
            number=4,
            message=duration_pb2.Duration,
        )

    class ServiceNetworking(proto.Message):
        r"""Information about the Kubernetes Service networking
        configuration.

        Attributes:
            service (str):
                Required. Name of the Kubernetes Service.
            deployment (str):
                Required. Name of the Kubernetes Deployment
                whose traffic is managed by the specified
                Service.
            disable_pod_overprovisioning (bool):
                Optional. Whether to disable Pod
                overprovisioning. If Pod overprovisioning is
                disabled then Cloud Deploy will limit the number
                of total Pods used for the deployment strategy
                to the number of Pods the Deployment has on the
                cluster.
        """

        service: str = proto.Field(
            proto.STRING,
            number=1,
        )
        deployment: str = proto.Field(
            proto.STRING,
            number=2,
        )
        disable_pod_overprovisioning: bool = proto.Field(
            proto.BOOL,
            number=3,
        )

    gateway_service_mesh: GatewayServiceMesh = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="service_definition",
        message=GatewayServiceMesh,
    )
    service_networking: ServiceNetworking = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="service_definition",
        message=ServiceNetworking,
    )


class CloudRunConfig(proto.Message):
    r"""CloudRunConfig contains the Cloud Run runtime configuration.

    Attributes:
        automatic_traffic_control (bool):
            Whether Cloud Deploy should update the
            traffic stanza in a Cloud Run Service on the
            user's behalf to facilitate traffic splitting.
            This is required to be true for
            CanaryDeployments, but optional for
            CustomCanaryDeployments.
    """

    automatic_traffic_control: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


class RuntimeConfig(proto.Message):
    r"""RuntimeConfig contains the runtime specific configurations
    for a deployment strategy.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        kubernetes (google.cloud.deploy_v1.types.KubernetesConfig):
            Kubernetes runtime configuration.

            This field is a member of `oneof`_ ``runtime_config``.
        cloud_run (google.cloud.deploy_v1.types.CloudRunConfig):
            Cloud Run runtime configuration.

            This field is a member of `oneof`_ ``runtime_config``.
    """

    kubernetes: "KubernetesConfig" = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="runtime_config",
        message="KubernetesConfig",
    )
    cloud_run: "CloudRunConfig" = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="runtime_config",
        message="CloudRunConfig",
    )


class PipelineReadyCondition(proto.Message):
    r"""PipelineReadyCondition contains information around the status
    of the Pipeline.

    Attributes:
        status (bool):
            True if the Pipeline is in a valid state. Otherwise at least
            one condition in ``PipelineCondition`` is in an invalid
            state. Iterate over those conditions and see which
            condition(s) has status = false to find out what is wrong
            with the Pipeline.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Last time the condition was updated.
    """

    status: bool = proto.Field(
        proto.BOOL,
        number=3,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )


class TargetsPresentCondition(proto.Message):
    r"""TargetsPresentCondition contains information on any Targets
    defined in the Delivery Pipeline that do not actually exist.

    Attributes:
        status (bool):
            True if there aren't any missing Targets.
        missing_targets (MutableSequence[str]):
            The list of Target names that do not exist. For example,
            projects/{project_id}/locations/{location_name}/targets/{target_name}.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Last time the condition was updated.
    """

    status: bool = proto.Field(
        proto.BOOL,
        number=1,
    )
    missing_targets: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )


class TargetsTypeCondition(proto.Message):
    r"""TargetsTypeCondition contains information on whether the
    Targets defined in the Delivery Pipeline are of the same type.

    Attributes:
        status (bool):
            True if the targets are all a comparable
            type. For example this is true if all targets
            are GKE clusters. This is false if some targets
            are Cloud Run targets and others are GKE
            clusters.
        error_details (str):
            Human readable error message.
    """

    status: bool = proto.Field(
        proto.BOOL,
        number=1,
    )
    error_details: str = proto.Field(
        proto.STRING,
        number=2,
    )


class PipelineCondition(proto.Message):
    r"""PipelineCondition contains all conditions relevant to a
    Delivery Pipeline.

    Attributes:
        pipeline_ready_condition (google.cloud.deploy_v1.types.PipelineReadyCondition):
            Details around the Pipeline's overall status.
        targets_present_condition (google.cloud.deploy_v1.types.TargetsPresentCondition):
            Details around targets enumerated in the
            pipeline.
        targets_type_condition (google.cloud.deploy_v1.types.TargetsTypeCondition):
            Details on the whether the targets enumerated
            in the pipeline are of the same type.
    """

    pipeline_ready_condition: "PipelineReadyCondition" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="PipelineReadyCondition",
    )
    targets_present_condition: "TargetsPresentCondition" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="TargetsPresentCondition",
    )
    targets_type_condition: "TargetsTypeCondition" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="TargetsTypeCondition",
    )


class ListDeliveryPipelinesRequest(proto.Message):
    r"""The request object for ``ListDeliveryPipelines``.

    Attributes:
        parent (str):
            Required. The parent, which owns this collection of
            pipelines. Format must be
            projects/{project_id}/locations/{location_name}.
        page_size (int):
            The maximum number of pipelines to return.
            The service may return fewer than this value. If
            unspecified, at most 50 pipelines will be
            returned. The maximum value is 1000; values
            above 1000 will be set to 1000.
        page_token (str):
            A page token, received from a previous
            ``ListDeliveryPipelines`` call. Provide this to retrieve the
            subsequent page.

            When paginating, all other provided parameters match the
            call that provided the page token.
        filter (str):
            Filter pipelines to be returned. See
            https://google.aip.dev/160 for more
            details.
        order_by (str):
            Field to sort by. See
            https://google.aip.dev/132#ordering for more
            details.
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
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )
    order_by: str = proto.Field(
        proto.STRING,
        number=5,
    )


class ListDeliveryPipelinesResponse(proto.Message):
    r"""The response object from ``ListDeliveryPipelines``.

    Attributes:
        delivery_pipelines (MutableSequence[google.cloud.deploy_v1.types.DeliveryPipeline]):
            The ``DeliveryPipeline`` objects.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
        unreachable (MutableSequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    delivery_pipelines: MutableSequence["DeliveryPipeline"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="DeliveryPipeline",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetDeliveryPipelineRequest(proto.Message):
    r"""The request object for ``GetDeliveryPipeline``

    Attributes:
        name (str):
            Required. Name of the ``DeliveryPipeline``. Format must be
            projects/{project_id}/locations/{location_name}/deliveryPipelines/{pipeline_name}.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateDeliveryPipelineRequest(proto.Message):
    r"""The request object for ``CreateDeliveryPipeline``.

    Attributes:
        parent (str):
            Required. The parent collection in which the
            ``DeliveryPipeline`` should be created. Format should be
            projects/{project_id}/locations/{location_name}.
        delivery_pipeline_id (str):
            Required. ID of the ``DeliveryPipeline``.
        delivery_pipeline (google.cloud.deploy_v1.types.DeliveryPipeline):
            Required. The ``DeliveryPipeline`` to create.
        request_id (str):
            Optional. A request ID to identify requests.
            Specify a unique request ID so that if you must
            retry your request, the server will know to
            ignore the request if it has already been
            completed. The server will guarantee that for at
            least 60 minutes since the first request.
            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
        validate_only (bool):
            Optional. If set to true, the request is
            validated and the user is provided with an
            expected result, but no actual change is made.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    delivery_pipeline_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    delivery_pipeline: "DeliveryPipeline" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="DeliveryPipeline",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=4,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=5,
    )


class UpdateDeliveryPipelineRequest(proto.Message):
    r"""The request object for ``UpdateDeliveryPipeline``.

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Field mask is used to specify the fields to be
            overwritten in the ``DeliveryPipeline`` resource by the
            update. The fields specified in the update_mask are relative
            to the resource, not the full request. A field will be
            overwritten if it is in the mask. If the user does not
            provide a mask then all fields will be overwritten.
        delivery_pipeline (google.cloud.deploy_v1.types.DeliveryPipeline):
            Required. The ``DeliveryPipeline`` to update.
        request_id (str):
            Optional. A request ID to identify requests.
            Specify a unique request ID so that if you must
            retry your request, the server will know to
            ignore the request if it has already been
            completed. The server will guarantee that for at
            least 60 minutes since the first request.
            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
        allow_missing (bool):
            Optional. If set to true, updating a ``DeliveryPipeline``
            that does not exist will result in the creation of a new
            ``DeliveryPipeline``.
        validate_only (bool):
            Optional. If set to true, the request is
            validated and the user is provided with an
            expected result, but no actual change is made.
    """

    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=1,
        message=field_mask_pb2.FieldMask,
    )
    delivery_pipeline: "DeliveryPipeline" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="DeliveryPipeline",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    allow_missing: bool = proto.Field(
        proto.BOOL,
        number=4,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=5,
    )


class DeleteDeliveryPipelineRequest(proto.Message):
    r"""The request object for ``DeleteDeliveryPipeline``.

    Attributes:
        name (str):
            Required. The name of the ``DeliveryPipeline`` to delete.
            Format should be
            projects/{project_id}/locations/{location_name}/deliveryPipelines/{pipeline_name}.
        request_id (str):
            Optional. A request ID to identify requests.
            Specify a unique request ID so that if you must
            retry your request, the server will know to
            ignore the request if it has already been
            completed. The server will guarantee that for at
            least 60 minutes after the first request.
            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
        allow_missing (bool):
            Optional. If set to true, then deleting an already deleted
            or non-existing ``DeliveryPipeline`` will succeed.
        validate_only (bool):
            Optional. If set, validate the request and
            preview the review, but do not actually post it.
        force (bool):
            Optional. If set to true, all child resources
            under this pipeline will also be deleted.
            Otherwise, the request will only work if the
            pipeline has no child resources.
        etag (str):
            Optional. This checksum is computed by the
            server based on the value of other fields, and
            may be sent on update and delete requests to
            ensure the client has an up-to-date value before
            proceeding.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    allow_missing: bool = proto.Field(
        proto.BOOL,
        number=3,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=4,
    )
    force: bool = proto.Field(
        proto.BOOL,
        number=6,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=5,
    )


class Target(proto.Message):
    r"""A ``Target`` resource in the Google Cloud Deploy API.

    A ``Target`` defines a location to which a Skaffold configuration
    can be deployed.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Optional. Name of the ``Target``. Format is
            projects/{project}/locations/{location}/targets/[a-z][a-z0-9-]{0,62}.
        target_id (str):
            Output only. Resource id of the ``Target``.
        uid (str):
            Output only. Unique identifier of the ``Target``.
        description (str):
            Optional. Description of the ``Target``. Max length is 255
            characters.
        annotations (MutableMapping[str, str]):
            Optional. User annotations. These attributes
            can only be set and used by the user, and not by
            Google Cloud Deploy. See
            https://google.aip.dev/128#annotations for more
            details such as format and size limitations.
        labels (MutableMapping[str, str]):
            Optional. Labels are attributes that can be set and used by
            both the user and by Google Cloud Deploy. Labels must meet
            the following constraints:

            -  Keys and values can contain only lowercase letters,
               numeric characters, underscores, and dashes.
            -  All characters must use UTF-8 encoding, and international
               characters are allowed.
            -  Keys must start with a lowercase letter or international
               character.
            -  Each resource is limited to a maximum of 64 labels.

            Both keys and values are additionally constrained to be <=
            128 bytes.
        require_approval (bool):
            Optional. Whether or not the ``Target`` requires approval.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time at which the ``Target`` was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Most recent time at which the ``Target`` was
            updated.
        gke (google.cloud.deploy_v1.types.GkeCluster):
            Optional. Information specifying a GKE
            Cluster.

            This field is a member of `oneof`_ ``deployment_target``.
        anthos_cluster (google.cloud.deploy_v1.types.AnthosCluster):
            Optional. Information specifying an Anthos
            Cluster.

            This field is a member of `oneof`_ ``deployment_target``.
        run (google.cloud.deploy_v1.types.CloudRunLocation):
            Optional. Information specifying a Cloud Run
            deployment target.

            This field is a member of `oneof`_ ``deployment_target``.
        multi_target (google.cloud.deploy_v1.types.MultiTarget):
            Optional. Information specifying a
            multiTarget.

            This field is a member of `oneof`_ ``deployment_target``.
        etag (str):
            Optional. This checksum is computed by the
            server based on the value of other fields, and
            may be sent on update and delete requests to
            ensure the client has an up-to-date value before
            proceeding.
        execution_configs (MutableSequence[google.cloud.deploy_v1.types.ExecutionConfig]):
            Configurations for all execution that relates to this
            ``Target``. Each ``ExecutionEnvironmentUsage`` value may
            only be used in a single configuration; using the same value
            multiple times is an error. When one or more configurations
            are specified, they must include the ``RENDER`` and
            ``DEPLOY`` ``ExecutionEnvironmentUsage`` values. When no
            configurations are specified, execution will use the default
            specified in ``DefaultPool``.
        deploy_parameters (MutableMapping[str, str]):
            Optional. The deploy parameters to use for
            this target.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    target_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=3,
    )
    description: str = proto.Field(
        proto.STRING,
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
        number=6,
    )
    require_approval: bool = proto.Field(
        proto.BOOL,
        number=13,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=8,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=9,
        message=timestamp_pb2.Timestamp,
    )
    gke: "GkeCluster" = proto.Field(
        proto.MESSAGE,
        number=15,
        oneof="deployment_target",
        message="GkeCluster",
    )
    anthos_cluster: "AnthosCluster" = proto.Field(
        proto.MESSAGE,
        number=17,
        oneof="deployment_target",
        message="AnthosCluster",
    )
    run: "CloudRunLocation" = proto.Field(
        proto.MESSAGE,
        number=18,
        oneof="deployment_target",
        message="CloudRunLocation",
    )
    multi_target: "MultiTarget" = proto.Field(
        proto.MESSAGE,
        number=19,
        oneof="deployment_target",
        message="MultiTarget",
    )
    etag: str = proto.Field(
        proto.STRING,
        number=12,
    )
    execution_configs: MutableSequence["ExecutionConfig"] = proto.RepeatedField(
        proto.MESSAGE,
        number=16,
        message="ExecutionConfig",
    )
    deploy_parameters: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=20,
    )


class ExecutionConfig(proto.Message):
    r"""Configuration of the environment to use when calling
    Skaffold.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        usages (MutableSequence[google.cloud.deploy_v1.types.ExecutionConfig.ExecutionEnvironmentUsage]):
            Required. Usages when this configuration
            should be applied.
        default_pool (google.cloud.deploy_v1.types.DefaultPool):
            Optional. Use default Cloud Build pool.

            This field is a member of `oneof`_ ``execution_environment``.
        private_pool (google.cloud.deploy_v1.types.PrivatePool):
            Optional. Use private Cloud Build pool.

            This field is a member of `oneof`_ ``execution_environment``.
        worker_pool (str):
            Optional. The resource name of the ``WorkerPool``, with the
            format
            ``projects/{project}/locations/{location}/workerPools/{worker_pool}``.
            If this optional field is unspecified, the default Cloud
            Build pool will be used.
        service_account (str):
            Optional. Google service account to use for execution. If
            unspecified, the project execution service account
            (<PROJECT_NUMBER>-compute@developer.gserviceaccount.com) is
            used.
        artifact_storage (str):
            Optional. Cloud Storage location in which to
            store execution outputs. This can either be a
            bucket ("gs://my-bucket") or a path within a
            bucket ("gs://my-bucket/my-dir").
            If unspecified, a default bucket located in the
            same region will be used.
        execution_timeout (google.protobuf.duration_pb2.Duration):
            Optional. Execution timeout for a Cloud Build
            Execution. This must be between 10m and 24h in
            seconds format. If unspecified, a default
            timeout of 1h is used.
    """

    class ExecutionEnvironmentUsage(proto.Enum):
        r"""Possible usages of this configuration.

        Values:
            EXECUTION_ENVIRONMENT_USAGE_UNSPECIFIED (0):
                Default value. This value is unused.
            RENDER (1):
                Use for rendering.
            DEPLOY (2):
                Use for deploying and deployment hooks.
            VERIFY (3):
                Use for deployment verification.
        """
        EXECUTION_ENVIRONMENT_USAGE_UNSPECIFIED = 0
        RENDER = 1
        DEPLOY = 2
        VERIFY = 3

    usages: MutableSequence[ExecutionEnvironmentUsage] = proto.RepeatedField(
        proto.ENUM,
        number=1,
        enum=ExecutionEnvironmentUsage,
    )
    default_pool: "DefaultPool" = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="execution_environment",
        message="DefaultPool",
    )
    private_pool: "PrivatePool" = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="execution_environment",
        message="PrivatePool",
    )
    worker_pool: str = proto.Field(
        proto.STRING,
        number=4,
    )
    service_account: str = proto.Field(
        proto.STRING,
        number=5,
    )
    artifact_storage: str = proto.Field(
        proto.STRING,
        number=6,
    )
    execution_timeout: duration_pb2.Duration = proto.Field(
        proto.MESSAGE,
        number=7,
        message=duration_pb2.Duration,
    )


class DefaultPool(proto.Message):
    r"""Execution using the default Cloud Build pool.

    Attributes:
        service_account (str):
            Optional. Google service account to use for execution. If
            unspecified, the project execution service account
            (<PROJECT_NUMBER>-compute@developer.gserviceaccount.com)
            will be used.
        artifact_storage (str):
            Optional. Cloud Storage location where
            execution outputs should be stored. This can
            either be a bucket ("gs://my-bucket") or a path
            within a bucket ("gs://my-bucket/my-dir").
            If unspecified, a default bucket located in the
            same region will be used.
    """

    service_account: str = proto.Field(
        proto.STRING,
        number=1,
    )
    artifact_storage: str = proto.Field(
        proto.STRING,
        number=2,
    )


class PrivatePool(proto.Message):
    r"""Execution using a private Cloud Build pool.

    Attributes:
        worker_pool (str):
            Required. Resource name of the Cloud Build worker pool to
            use. The format is
            ``projects/{project}/locations/{location}/workerPools/{pool}``.
        service_account (str):
            Optional. Google service account to use for execution. If
            unspecified, the project execution service account
            (<PROJECT_NUMBER>-compute@developer.gserviceaccount.com)
            will be used.
        artifact_storage (str):
            Optional. Cloud Storage location where
            execution outputs should be stored. This can
            either be a bucket ("gs://my-bucket") or a path
            within a bucket ("gs://my-bucket/my-dir").
            If unspecified, a default bucket located in the
            same region will be used.
    """

    worker_pool: str = proto.Field(
        proto.STRING,
        number=1,
    )
    service_account: str = proto.Field(
        proto.STRING,
        number=2,
    )
    artifact_storage: str = proto.Field(
        proto.STRING,
        number=3,
    )


class GkeCluster(proto.Message):
    r"""Information specifying a GKE Cluster.

    Attributes:
        cluster (str):
            Information specifying a GKE Cluster. Format is
            \`projects/{project_id}/locations/{location_id}/clusters/{cluster_id}.
        internal_ip (bool):
            Optional. If true, ``cluster`` is accessed using the private
            IP address of the control plane endpoint. Otherwise, the
            default IP address of the control plane endpoint is used.
            The default IP address is the private IP address for
            clusters with private control-plane endpoints and the public
            IP address otherwise.

            Only specify this option when ``cluster`` is a `private GKE
            cluster <https://cloud.google.com/kubernetes-engine/docs/concepts/private-cluster-concept>`__.
    """

    cluster: str = proto.Field(
        proto.STRING,
        number=1,
    )
    internal_ip: bool = proto.Field(
        proto.BOOL,
        number=2,
    )


class AnthosCluster(proto.Message):
    r"""Information specifying an Anthos Cluster.

    Attributes:
        membership (str):
            Membership of the GKE Hub-registered cluster to which to
            apply the Skaffold configuration. Format is
            ``projects/{project}/locations/{location}/memberships/{membership_name}``.
    """

    membership: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CloudRunLocation(proto.Message):
    r"""Information specifying where to deploy a Cloud Run Service.

    Attributes:
        location (str):
            Required. The location for the Cloud Run Service. Format
            must be ``projects/{project}/locations/{location}``.
    """

    location: str = proto.Field(
        proto.STRING,
        number=1,
    )


class MultiTarget(proto.Message):
    r"""Information specifying a multiTarget.

    Attributes:
        target_ids (MutableSequence[str]):
            Required. The target_ids of this multiTarget.
    """

    target_ids: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )


class ListTargetsRequest(proto.Message):
    r"""The request object for ``ListTargets``.

    Attributes:
        parent (str):
            Required. The parent, which owns this collection of targets.
            Format must be
            projects/{project_id}/locations/{location_name}.
        page_size (int):
            Optional. The maximum number of ``Target`` objects to
            return. The service may return fewer than this value. If
            unspecified, at most 50 ``Target`` objects will be returned.
            The maximum value is 1000; values above 1000 will be set to
            1000.
        page_token (str):
            Optional. A page token, received from a previous
            ``ListTargets`` call. Provide this to retrieve the
            subsequent page.

            When paginating, all other provided parameters match the
            call that provided the page token.
        filter (str):
            Optional. Filter targets to be returned. See
            https://google.aip.dev/160 for
            more details.
        order_by (str):
            Optional. Field to sort by. See
            https://google.aip.dev/132#ordering for
            more details.
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
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )
    order_by: str = proto.Field(
        proto.STRING,
        number=5,
    )


class ListTargetsResponse(proto.Message):
    r"""The response object from ``ListTargets``.

    Attributes:
        targets (MutableSequence[google.cloud.deploy_v1.types.Target]):
            The ``Target`` objects.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
        unreachable (MutableSequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    targets: MutableSequence["Target"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Target",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetTargetRequest(proto.Message):
    r"""The request object for ``GetTarget``.

    Attributes:
        name (str):
            Required. Name of the ``Target``. Format must be
            projects/{project_id}/locations/{location_name}/targets/{target_name}.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateTargetRequest(proto.Message):
    r"""The request object for ``CreateTarget``.

    Attributes:
        parent (str):
            Required. The parent collection in which the ``Target``
            should be created. Format should be
            projects/{project_id}/locations/{location_name}.
        target_id (str):
            Required. ID of the ``Target``.
        target (google.cloud.deploy_v1.types.Target):
            Required. The ``Target`` to create.
        request_id (str):
            Optional. A request ID to identify requests.
            Specify a unique request ID so that if you must
            retry your request, the server will know to
            ignore the request if it has already been
            completed. The server will guarantee that for at
            least 60 minutes since the first request.
            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
        validate_only (bool):
            Optional. If set to true, the request is
            validated and the user is provided with an
            expected result, but no actual change is made.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    target_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    target: "Target" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Target",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=4,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=5,
    )


class UpdateTargetRequest(proto.Message):
    r"""The request object for ``UpdateTarget``.

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Field mask is used to specify the fields to be
            overwritten in the Target resource by the update. The fields
            specified in the update_mask are relative to the resource,
            not the full request. A field will be overwritten if it is
            in the mask. If the user does not provide a mask then all
            fields will be overwritten.
        target (google.cloud.deploy_v1.types.Target):
            Required. The ``Target`` to update.
        request_id (str):
            Optional. A request ID to identify requests.
            Specify a unique request ID so that if you must
            retry your request, the server will know to
            ignore the request if it has already been
            completed. The server will guarantee that for at
            least 60 minutes since the first request.
            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
        allow_missing (bool):
            Optional. If set to true, updating a ``Target`` that does
            not exist will result in the creation of a new ``Target``.
        validate_only (bool):
            Optional. If set to true, the request is
            validated and the user is provided with an
            expected result, but no actual change is made.
    """

    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=1,
        message=field_mask_pb2.FieldMask,
    )
    target: "Target" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Target",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    allow_missing: bool = proto.Field(
        proto.BOOL,
        number=4,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=5,
    )


class DeleteTargetRequest(proto.Message):
    r"""The request object for ``DeleteTarget``.

    Attributes:
        name (str):
            Required. The name of the ``Target`` to delete. Format
            should be
            projects/{project_id}/locations/{location_name}/targets/{target_name}.
        request_id (str):
            Optional. A request ID to identify requests.
            Specify a unique request ID so that if you must
            retry your request, the server will know to
            ignore the request if it has already been
            completed. The server will guarantee that for at
            least 60 minutes after the first request.
            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
        allow_missing (bool):
            Optional. If set to true, then deleting an already deleted
            or non-existing ``Target`` will succeed.
        validate_only (bool):
            Optional. If set, validate the request and
            preview the review, but do not actually post it.
        etag (str):
            Optional. This checksum is computed by the
            server based on the value of other fields, and
            may be sent on update and delete requests to
            ensure the client has an up-to-date value before
            proceeding.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    allow_missing: bool = proto.Field(
        proto.BOOL,
        number=3,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=4,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=5,
    )


class Release(proto.Message):
    r"""A ``Release`` resource in the Google Cloud Deploy API.

    A ``Release`` defines a specific Skaffold configuration instance
    that can be deployed.

    Attributes:
        name (str):
            Optional. Name of the ``Release``. Format is
            projects/{project}/
            locations/{location}/deliveryPipelines/{deliveryPipeline}/
            releases/[a-z][a-z0-9-]{0,62}.
        uid (str):
            Output only. Unique identifier of the ``Release``.
        description (str):
            Description of the ``Release``. Max length is 255
            characters.
        annotations (MutableMapping[str, str]):
            User annotations. These attributes can only
            be set and used by the user, and not by Google
            Cloud Deploy. See
            https://google.aip.dev/128#annotations for more
            details such as format and size limitations.
        labels (MutableMapping[str, str]):
            Labels are attributes that can be set and used by both the
            user and by Google Cloud Deploy. Labels must meet the
            following constraints:

            -  Keys and values can contain only lowercase letters,
               numeric characters, underscores, and dashes.
            -  All characters must use UTF-8 encoding, and international
               characters are allowed.
            -  Keys must start with a lowercase letter or international
               character.
            -  Each resource is limited to a maximum of 64 labels.

            Both keys and values are additionally constrained to be <=
            128 bytes.
        abandoned (bool):
            Output only. Indicates whether this is an
            abandoned release.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time at which the ``Release`` was created.
        render_start_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time at which the render began.
        render_end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time at which the render
            completed.
        skaffold_config_uri (str):
            Cloud Storage URI of tar.gz archive
            containing Skaffold configuration.
        skaffold_config_path (str):
            Filepath of the Skaffold config inside of the
            config URI.
        build_artifacts (MutableSequence[google.cloud.deploy_v1.types.BuildArtifact]):
            List of artifacts to pass through to Skaffold
            command.
        delivery_pipeline_snapshot (google.cloud.deploy_v1.types.DeliveryPipeline):
            Output only. Snapshot of the parent pipeline
            taken at release creation time.
        target_snapshots (MutableSequence[google.cloud.deploy_v1.types.Target]):
            Output only. Snapshot of the targets taken at
            release creation time.
        render_state (google.cloud.deploy_v1.types.Release.RenderState):
            Output only. Current state of the render
            operation.
        etag (str):
            This checksum is computed by the server based
            on the value of other fields, and may be sent on
            update and delete requests to ensure the client
            has an up-to-date value before proceeding.
        skaffold_version (str):
            The Skaffold version to use when operating on
            this release, such as "1.20.0". Not all versions
            are valid; Google Cloud Deploy supports a
            specific set of versions.

            If unset, the most recent supported Skaffold
            version will be used.
        target_artifacts (MutableMapping[str, google.cloud.deploy_v1.types.TargetArtifact]):
            Output only. Map from target ID to the target
            artifacts created during the render operation.
        target_renders (MutableMapping[str, google.cloud.deploy_v1.types.Release.TargetRender]):
            Output only. Map from target ID to details of
            the render operation for that target.
        condition (google.cloud.deploy_v1.types.Release.ReleaseCondition):
            Output only. Information around the state of
            the Release.
        deploy_parameters (MutableMapping[str, str]):
            Optional. The deploy parameters to use for
            all targets in this release.
    """

    class RenderState(proto.Enum):
        r"""Valid states of the render operation.

        Values:
            RENDER_STATE_UNSPECIFIED (0):
                The render state is unspecified.
            SUCCEEDED (1):
                All rendering operations have completed
                successfully.
            FAILED (2):
                All rendering operations have completed, and
                one or more have failed.
            IN_PROGRESS (3):
                Rendering has started and is not complete.
        """
        RENDER_STATE_UNSPECIFIED = 0
        SUCCEEDED = 1
        FAILED = 2
        IN_PROGRESS = 3

    class TargetRender(proto.Message):
        r"""Details of rendering for a single target.

        Attributes:
            rendering_build (str):
                Output only. The resource name of the Cloud Build ``Build``
                object that is used to render the manifest for this target.
                Format is
                ``projects/{project}/locations/{location}/builds/{build}``.
            rendering_state (google.cloud.deploy_v1.types.Release.TargetRender.TargetRenderState):
                Output only. Current state of the render
                operation for this Target.
            metadata (google.cloud.deploy_v1.types.RenderMetadata):
                Output only. Metadata related to the ``Release`` render for
                this Target.
            failure_cause (google.cloud.deploy_v1.types.Release.TargetRender.FailureCause):
                Output only. Reason this render failed. This
                will always be unspecified while the render in
                progress.
            failure_message (str):
                Output only. Additional information about the
                render failure, if available.
        """

        class TargetRenderState(proto.Enum):
            r"""Valid states of the render operation.

            Values:
                TARGET_RENDER_STATE_UNSPECIFIED (0):
                    The render operation state is unspecified.
                SUCCEEDED (1):
                    The render operation has completed
                    successfully.
                FAILED (2):
                    The render operation has failed.
                IN_PROGRESS (3):
                    The render operation is in progress.
            """
            TARGET_RENDER_STATE_UNSPECIFIED = 0
            SUCCEEDED = 1
            FAILED = 2
            IN_PROGRESS = 3

        class FailureCause(proto.Enum):
            r"""Well-known rendering failures.

            Values:
                FAILURE_CAUSE_UNSPECIFIED (0):
                    No reason for failure is specified.
                CLOUD_BUILD_UNAVAILABLE (1):
                    Cloud Build is not available, either because it is not
                    enabled or because Google Cloud Deploy has insufficient
                    permissions. See `required
                    permission </deploy/docs/cloud-deploy-service-account#required_permissions>`__.
                EXECUTION_FAILED (2):
                    The render operation did not complete
                    successfully; check Cloud Build logs.
                CLOUD_BUILD_REQUEST_FAILED (3):
                    Cloud Build failed to fulfill Google Cloud Deploy's request.
                    See failure_message for additional details.
            """
            FAILURE_CAUSE_UNSPECIFIED = 0
            CLOUD_BUILD_UNAVAILABLE = 1
            EXECUTION_FAILED = 2
            CLOUD_BUILD_REQUEST_FAILED = 3

        rendering_build: str = proto.Field(
            proto.STRING,
            number=1,
        )
        rendering_state: "Release.TargetRender.TargetRenderState" = proto.Field(
            proto.ENUM,
            number=2,
            enum="Release.TargetRender.TargetRenderState",
        )
        metadata: "RenderMetadata" = proto.Field(
            proto.MESSAGE,
            number=6,
            message="RenderMetadata",
        )
        failure_cause: "Release.TargetRender.FailureCause" = proto.Field(
            proto.ENUM,
            number=4,
            enum="Release.TargetRender.FailureCause",
        )
        failure_message: str = proto.Field(
            proto.STRING,
            number=5,
        )

    class ReleaseReadyCondition(proto.Message):
        r"""ReleaseReadyCondition contains information around the status
        of the Release. If a release is not ready, you cannot create a
        rollout with the release.

        Attributes:
            status (bool):
                True if the Release is in a valid state. Otherwise at least
                one condition in ``ReleaseCondition`` is in an invalid
                state. Iterate over those conditions and see which
                condition(s) has status = false to find out what is wrong
                with the Release.
        """

        status: bool = proto.Field(
            proto.BOOL,
            number=1,
        )

    class SkaffoldSupportedCondition(proto.Message):
        r"""SkaffoldSupportedCondition contains information about when
        support for the release's version of skaffold ends.

        Attributes:
            status (bool):
                True if the version of skaffold used by this
                release is supported.
            skaffold_support_state (google.cloud.deploy_v1.types.SkaffoldSupportState):
                The skaffold support state for this release's
                version of skaffold.
            maintenance_mode_time (google.protobuf.timestamp_pb2.Timestamp):
                The time at which this release's version of
                skaffold will enter maintenance mode.
            support_expiration_time (google.protobuf.timestamp_pb2.Timestamp):
                The time at which this release's version of
                skaffold will no longer be supported.
        """

        status: bool = proto.Field(
            proto.BOOL,
            number=1,
        )
        skaffold_support_state: "SkaffoldSupportState" = proto.Field(
            proto.ENUM,
            number=2,
            enum="SkaffoldSupportState",
        )
        maintenance_mode_time: timestamp_pb2.Timestamp = proto.Field(
            proto.MESSAGE,
            number=3,
            message=timestamp_pb2.Timestamp,
        )
        support_expiration_time: timestamp_pb2.Timestamp = proto.Field(
            proto.MESSAGE,
            number=4,
            message=timestamp_pb2.Timestamp,
        )

    class ReleaseCondition(proto.Message):
        r"""ReleaseCondition contains all conditions relevant to a
        Release.

        Attributes:
            release_ready_condition (google.cloud.deploy_v1.types.Release.ReleaseReadyCondition):
                Details around the Releases's overall status.
            skaffold_supported_condition (google.cloud.deploy_v1.types.Release.SkaffoldSupportedCondition):
                Details around the support state of the
                release's skaffold version.
        """

        release_ready_condition: "Release.ReleaseReadyCondition" = proto.Field(
            proto.MESSAGE,
            number=1,
            message="Release.ReleaseReadyCondition",
        )
        skaffold_supported_condition: "Release.SkaffoldSupportedCondition" = (
            proto.Field(
                proto.MESSAGE,
                number=2,
                message="Release.SkaffoldSupportedCondition",
            )
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=2,
    )
    description: str = proto.Field(
        proto.STRING,
        number=3,
    )
    annotations: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=4,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=5,
    )
    abandoned: bool = proto.Field(
        proto.BOOL,
        number=23,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
    )
    render_start_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=7,
        message=timestamp_pb2.Timestamp,
    )
    render_end_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=8,
        message=timestamp_pb2.Timestamp,
    )
    skaffold_config_uri: str = proto.Field(
        proto.STRING,
        number=17,
    )
    skaffold_config_path: str = proto.Field(
        proto.STRING,
        number=9,
    )
    build_artifacts: MutableSequence["BuildArtifact"] = proto.RepeatedField(
        proto.MESSAGE,
        number=10,
        message="BuildArtifact",
    )
    delivery_pipeline_snapshot: "DeliveryPipeline" = proto.Field(
        proto.MESSAGE,
        number=11,
        message="DeliveryPipeline",
    )
    target_snapshots: MutableSequence["Target"] = proto.RepeatedField(
        proto.MESSAGE,
        number=12,
        message="Target",
    )
    render_state: RenderState = proto.Field(
        proto.ENUM,
        number=13,
        enum=RenderState,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=16,
    )
    skaffold_version: str = proto.Field(
        proto.STRING,
        number=19,
    )
    target_artifacts: MutableMapping[str, "TargetArtifact"] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=20,
        message="TargetArtifact",
    )
    target_renders: MutableMapping[str, TargetRender] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=22,
        message=TargetRender,
    )
    condition: ReleaseCondition = proto.Field(
        proto.MESSAGE,
        number=24,
        message=ReleaseCondition,
    )
    deploy_parameters: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=25,
    )


class BuildArtifact(proto.Message):
    r"""Description of an a image to use during Skaffold rendering.

    Attributes:
        image (str):
            Image name in Skaffold configuration.
        tag (str):
            Image tag to use. This will generally be the
            full path to an image, such as
            "gcr.io/my-project/busybox:1.2.3" or
            "gcr.io/my-project/busybox@sha256:abc123".
    """

    image: str = proto.Field(
        proto.STRING,
        number=3,
    )
    tag: str = proto.Field(
        proto.STRING,
        number=2,
    )


class TargetArtifact(proto.Message):
    r"""The artifacts produced by a target render operation.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        artifact_uri (str):
            Output only. URI of a directory containing
            the artifacts. This contains deployment
            configuration used by Skaffold during a rollout,
            and all paths are relative to this location.

            This field is a member of `oneof`_ ``uri``.
        skaffold_config_path (str):
            Output only. File path of the resolved
            Skaffold configuration relative to the URI.
        manifest_path (str):
            Output only. File path of the rendered
            manifest relative to the URI.
        phase_artifacts (MutableMapping[str, google.cloud.deploy_v1.types.TargetArtifact.PhaseArtifact]):
            Output only. Map from the phase ID to the phase artifacts
            for the ``Target``.
    """

    class PhaseArtifact(proto.Message):
        r"""Contains the paths to the artifacts, relative to the URI, for
        a phase.

        Attributes:
            skaffold_config_path (str):
                Output only. File path of the resolved
                Skaffold configuration relative to the URI.
            manifest_path (str):
                Output only. File path of the rendered
                manifest relative to the URI.
            job_manifests_path (str):
                Output only. File path of the directory of
                rendered job manifests relative to the URI. This
                is only set if it is applicable.
        """

        skaffold_config_path: str = proto.Field(
            proto.STRING,
            number=1,
        )
        manifest_path: str = proto.Field(
            proto.STRING,
            number=3,
        )
        job_manifests_path: str = proto.Field(
            proto.STRING,
            number=4,
        )

    artifact_uri: str = proto.Field(
        proto.STRING,
        number=4,
        oneof="uri",
    )
    skaffold_config_path: str = proto.Field(
        proto.STRING,
        number=2,
    )
    manifest_path: str = proto.Field(
        proto.STRING,
        number=3,
    )
    phase_artifacts: MutableMapping[str, PhaseArtifact] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=5,
        message=PhaseArtifact,
    )


class DeployArtifact(proto.Message):
    r"""The artifacts produced by a deploy operation.

    Attributes:
        artifact_uri (str):
            Output only. URI of a directory containing
            the artifacts. All paths are relative to this
            location.
        manifest_paths (MutableSequence[str]):
            Output only. File paths of the manifests
            applied during the deploy operation relative to
            the URI.
    """

    artifact_uri: str = proto.Field(
        proto.STRING,
        number=1,
    )
    manifest_paths: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )


class CloudRunRenderMetadata(proto.Message):
    r"""CloudRunRenderMetadata contains Cloud Run information associated
    with a ``Release`` render.

    Attributes:
        service (str):
            Output only. The name of the Cloud Run
            Service in the rendered manifest. Format is
            projects/{project}/locations/{location}/services/{service}.
    """

    service: str = proto.Field(
        proto.STRING,
        number=1,
    )


class RenderMetadata(proto.Message):
    r"""RenderMetadata includes information associated with a ``Release``
    render.

    Attributes:
        cloud_run (google.cloud.deploy_v1.types.CloudRunRenderMetadata):
            Output only. Metadata associated with
            rendering for Cloud Run.
    """

    cloud_run: "CloudRunRenderMetadata" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="CloudRunRenderMetadata",
    )


class ListReleasesRequest(proto.Message):
    r"""The request object for ``ListReleases``.

    Attributes:
        parent (str):
            Required. The ``DeliveryPipeline`` which owns this
            collection of ``Release`` objects.
        page_size (int):
            Optional. The maximum number of ``Release`` objects to
            return. The service may return fewer than this value. If
            unspecified, at most 50 ``Release`` objects will be
            returned. The maximum value is 1000; values above 1000 will
            be set to 1000.
        page_token (str):
            Optional. A page token, received from a previous
            ``ListReleases`` call. Provide this to retrieve the
            subsequent page.

            When paginating, all other provided parameters match the
            call that provided the page token.
        filter (str):
            Optional. Filter releases to be returned. See
            https://google.aip.dev/160
            for more details.
        order_by (str):
            Optional. Field to sort by. See
            https://google.aip.dev/132#ordering for
            more details.
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
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )
    order_by: str = proto.Field(
        proto.STRING,
        number=5,
    )


class ListReleasesResponse(proto.Message):
    r"""The response object from ``ListReleases``.

    Attributes:
        releases (MutableSequence[google.cloud.deploy_v1.types.Release]):
            The ``Release`` objects.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
        unreachable (MutableSequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    releases: MutableSequence["Release"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Release",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetReleaseRequest(proto.Message):
    r"""The request object for ``GetRelease``.

    Attributes:
        name (str):
            Required. Name of the ``Release``. Format must be
            projects/{project_id}/locations/{location_name}/deliveryPipelines/{pipeline_name}/releases/{release_name}.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateReleaseRequest(proto.Message):
    r"""The request object for ``CreateRelease``,

    Attributes:
        parent (str):
            Required. The parent collection in which the ``Release``
            should be created. Format should be
            projects/{project_id}/locations/{location_name}/deliveryPipelines/{pipeline_name}.
        release_id (str):
            Required. ID of the ``Release``.
        release (google.cloud.deploy_v1.types.Release):
            Required. The ``Release`` to create.
        request_id (str):
            Optional. A request ID to identify requests.
            Specify a unique request ID so that if you must
            retry your request, the server will know to
            ignore the request if it has already been
            completed. The server will guarantee that for at
            least 60 minutes since the first request.
            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
        validate_only (bool):
            Optional. If set to true, the request is
            validated and the user is provided with an
            expected result, but no actual change is made.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    release_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    release: "Release" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Release",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=4,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=5,
    )


class Rollout(proto.Message):
    r"""A ``Rollout`` resource in the Google Cloud Deploy API.

    A ``Rollout`` contains information around a specific deployment to a
    ``Target``.

    Attributes:
        name (str):
            Optional. Name of the ``Rollout``. Format is
            projects/{project}/
            locations/{location}/deliveryPipelines/{deliveryPipeline}/
            releases/{release}/rollouts/[a-z][a-z0-9-]{0,62}.
        uid (str):
            Output only. Unique identifier of the ``Rollout``.
        description (str):
            Description of the ``Rollout`` for user purposes. Max length
            is 255 characters.
        annotations (MutableMapping[str, str]):
            User annotations. These attributes can only
            be set and used by the user, and not by Google
            Cloud Deploy. See
            https://google.aip.dev/128#annotations for more
            details such as format and size limitations.
        labels (MutableMapping[str, str]):
            Labels are attributes that can be set and used by both the
            user and by Google Cloud Deploy. Labels must meet the
            following constraints:

            -  Keys and values can contain only lowercase letters,
               numeric characters, underscores, and dashes.
            -  All characters must use UTF-8 encoding, and international
               characters are allowed.
            -  Keys must start with a lowercase letter or international
               character.
            -  Each resource is limited to a maximum of 64 labels.

            Both keys and values are additionally constrained to be <=
            128 bytes.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time at which the ``Rollout`` was created.
        approve_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time at which the ``Rollout`` was approved.
        enqueue_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time at which the ``Rollout`` was enqueued.
        deploy_start_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time at which the ``Rollout`` started
            deploying.
        deploy_end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time at which the ``Rollout`` finished
            deploying.
        target_id (str):
            Required. The ID of Target to which this ``Rollout`` is
            deploying.
        approval_state (google.cloud.deploy_v1.types.Rollout.ApprovalState):
            Output only. Approval state of the ``Rollout``.
        state (google.cloud.deploy_v1.types.Rollout.State):
            Output only. Current state of the ``Rollout``.
        failure_reason (str):
            Output only. Additional information about the
            rollout failure, if available.
        deploying_build (str):
            Output only. The resource name of the Cloud Build ``Build``
            object that is used to deploy the Rollout. Format is
            ``projects/{project}/locations/{location}/builds/{build}``.
        etag (str):
            This checksum is computed by the server based
            on the value of other fields, and may be sent on
            update and delete requests to ensure the client
            has an up-to-date value before proceeding.
        deploy_failure_cause (google.cloud.deploy_v1.types.Rollout.FailureCause):
            Output only. The reason this rollout failed.
            This will always be unspecified while the
            rollout is in progress.
        phases (MutableSequence[google.cloud.deploy_v1.types.Phase]):
            Output only. The phases that represent the workflows of this
            ``Rollout``.
        metadata (google.cloud.deploy_v1.types.Metadata):
            Output only. Metadata contains information
            about the rollout.
        controller_rollout (str):
            Output only. Name of the ``ControllerRollout``. Format is
            projects/{project}/
            locations/{location}/deliveryPipelines/{deliveryPipeline}/
            releases/{release}/rollouts/[a-z][a-z0-9-]{0,62}.
    """

    class ApprovalState(proto.Enum):
        r"""Valid approval states of a ``Rollout``.

        Values:
            APPROVAL_STATE_UNSPECIFIED (0):
                The ``Rollout`` has an unspecified approval state.
            NEEDS_APPROVAL (1):
                The ``Rollout`` requires approval.
            DOES_NOT_NEED_APPROVAL (2):
                The ``Rollout`` does not require approval.
            APPROVED (3):
                The ``Rollout`` has been approved.
            REJECTED (4):
                The ``Rollout`` has been rejected.
        """
        APPROVAL_STATE_UNSPECIFIED = 0
        NEEDS_APPROVAL = 1
        DOES_NOT_NEED_APPROVAL = 2
        APPROVED = 3
        REJECTED = 4

    class State(proto.Enum):
        r"""Valid states of a ``Rollout``.

        Values:
            STATE_UNSPECIFIED (0):
                The ``Rollout`` has an unspecified state.
            SUCCEEDED (1):
                The ``Rollout`` has completed successfully.
            FAILED (2):
                The ``Rollout`` has failed.
            IN_PROGRESS (3):
                The ``Rollout`` is being deployed.
            PENDING_APPROVAL (4):
                The ``Rollout`` needs approval.
            APPROVAL_REJECTED (5):
                An approver rejected the ``Rollout``.
            PENDING (6):
                The ``Rollout`` is waiting for an earlier Rollout(s) to
                complete on this ``Target``.
            PENDING_RELEASE (7):
                The ``Rollout`` is waiting for the ``Release`` to be fully
                rendered.
            CANCELLING (8):
                The ``Rollout`` is in the process of being cancelled.
            CANCELLED (9):
                The ``Rollout`` has been cancelled.
            HALTED (10):
                The ``Rollout`` is halted.
        """
        STATE_UNSPECIFIED = 0
        SUCCEEDED = 1
        FAILED = 2
        IN_PROGRESS = 3
        PENDING_APPROVAL = 4
        APPROVAL_REJECTED = 5
        PENDING = 6
        PENDING_RELEASE = 7
        CANCELLING = 8
        CANCELLED = 9
        HALTED = 10

    class FailureCause(proto.Enum):
        r"""Well-known rollout failures.

        Values:
            FAILURE_CAUSE_UNSPECIFIED (0):
                No reason for failure is specified.
            CLOUD_BUILD_UNAVAILABLE (1):
                Cloud Build is not available, either because it is not
                enabled or because Cloud Deploy has insufficient
                permissions. See `required
                permission </deploy/docs/cloud-deploy-service-account#required_permissions>`__.
            EXECUTION_FAILED (2):
                The deploy operation did not complete
                successfully; check Cloud Build logs.
            DEADLINE_EXCEEDED (3):
                Deployment did not complete within the
                alloted time.
            RELEASE_FAILED (4):
                Release is in a failed state.
            RELEASE_ABANDONED (5):
                Release is abandoned.
            VERIFICATION_CONFIG_NOT_FOUND (6):
                No skaffold verify configuration was found.
            CLOUD_BUILD_REQUEST_FAILED (7):
                Cloud Build failed to fulfill Google Cloud Deploy's request.
                See failure_message for additional details.
        """
        FAILURE_CAUSE_UNSPECIFIED = 0
        CLOUD_BUILD_UNAVAILABLE = 1
        EXECUTION_FAILED = 2
        DEADLINE_EXCEEDED = 3
        RELEASE_FAILED = 4
        RELEASE_ABANDONED = 5
        VERIFICATION_CONFIG_NOT_FOUND = 6
        CLOUD_BUILD_REQUEST_FAILED = 7

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=2,
    )
    description: str = proto.Field(
        proto.STRING,
        number=3,
    )
    annotations: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=4,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=5,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
    )
    approve_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=7,
        message=timestamp_pb2.Timestamp,
    )
    enqueue_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=8,
        message=timestamp_pb2.Timestamp,
    )
    deploy_start_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=9,
        message=timestamp_pb2.Timestamp,
    )
    deploy_end_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=10,
        message=timestamp_pb2.Timestamp,
    )
    target_id: str = proto.Field(
        proto.STRING,
        number=18,
    )
    approval_state: ApprovalState = proto.Field(
        proto.ENUM,
        number=12,
        enum=ApprovalState,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=13,
        enum=State,
    )
    failure_reason: str = proto.Field(
        proto.STRING,
        number=14,
    )
    deploying_build: str = proto.Field(
        proto.STRING,
        number=17,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=16,
    )
    deploy_failure_cause: FailureCause = proto.Field(
        proto.ENUM,
        number=19,
        enum=FailureCause,
    )
    phases: MutableSequence["Phase"] = proto.RepeatedField(
        proto.MESSAGE,
        number=23,
        message="Phase",
    )
    metadata: "Metadata" = proto.Field(
        proto.MESSAGE,
        number=24,
        message="Metadata",
    )
    controller_rollout: str = proto.Field(
        proto.STRING,
        number=25,
    )


class Metadata(proto.Message):
    r"""Metadata includes information associated with a ``Rollout``.

    Attributes:
        cloud_run (google.cloud.deploy_v1.types.CloudRunMetadata):
            Output only. The name of the Cloud Run Service that is
            associated with a ``Rollout``.
    """

    cloud_run: "CloudRunMetadata" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="CloudRunMetadata",
    )


class DeployJobRunMetadata(proto.Message):
    r"""DeployJobRunMetadata surfaces information associated with a
    ``DeployJobRun`` to the user.

    Attributes:
        cloud_run (google.cloud.deploy_v1.types.CloudRunMetadata):
            Output only. The name of the Cloud Run Service that is
            associated with a ``DeployJobRun``.
    """

    cloud_run: "CloudRunMetadata" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="CloudRunMetadata",
    )


class CloudRunMetadata(proto.Message):
    r"""CloudRunMetadata contains information from a Cloud Run
    deployment.

    Attributes:
        service (str):
            Output only. The name of the Cloud Run Service that is
            associated with a ``Rollout``. Format is
            projects/{project}/locations/{location}/services/{service}.
        service_urls (MutableSequence[str]):
            Output only. The Cloud Run Service urls that are associated
            with a ``Rollout``.
        revision (str):
            Output only. The Cloud Run Revision id associated with a
            ``Rollout``.
    """

    service: str = proto.Field(
        proto.STRING,
        number=1,
    )
    service_urls: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )
    revision: str = proto.Field(
        proto.STRING,
        number=3,
    )


class Phase(proto.Message):
    r"""Phase represents a collection of jobs that are logically grouped
    together for a ``Rollout``.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        id (str):
            Output only. The ID of the Phase.
        state (google.cloud.deploy_v1.types.Phase.State):
            Output only. Current state of the Phase.
        skip_message (str):
            Output only. Additional information on why
            the Phase was skipped, if available.
        deployment_jobs (google.cloud.deploy_v1.types.DeploymentJobs):
            Output only. Deployment job composition.

            This field is a member of `oneof`_ ``jobs``.
        child_rollout_jobs (google.cloud.deploy_v1.types.ChildRolloutJobs):
            Output only. ChildRollout job composition.

            This field is a member of `oneof`_ ``jobs``.
    """

    class State(proto.Enum):
        r"""Valid states of a Phase.

        Values:
            STATE_UNSPECIFIED (0):
                The Phase has an unspecified state.
            PENDING (1):
                The Phase is waiting for an earlier Phase(s)
                to complete.
            IN_PROGRESS (2):
                The Phase is in progress.
            SUCCEEDED (3):
                The Phase has succeeded.
            FAILED (4):
                The Phase has failed.
            ABORTED (5):
                The Phase was aborted.
            SKIPPED (6):
                The Phase was skipped.
        """
        STATE_UNSPECIFIED = 0
        PENDING = 1
        IN_PROGRESS = 2
        SUCCEEDED = 3
        FAILED = 4
        ABORTED = 5
        SKIPPED = 6

    id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=3,
        enum=State,
    )
    skip_message: str = proto.Field(
        proto.STRING,
        number=6,
    )
    deployment_jobs: "DeploymentJobs" = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="jobs",
        message="DeploymentJobs",
    )
    child_rollout_jobs: "ChildRolloutJobs" = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="jobs",
        message="ChildRolloutJobs",
    )


class DeploymentJobs(proto.Message):
    r"""Deployment job composition.

    Attributes:
        deploy_job (google.cloud.deploy_v1.types.Job):
            Output only. The deploy Job. This is the
            deploy job in the phase.
        verify_job (google.cloud.deploy_v1.types.Job):
            Output only. The verify Job. Runs after a
            deploy if the deploy succeeds.
    """

    deploy_job: "Job" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="Job",
    )
    verify_job: "Job" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Job",
    )


class ChildRolloutJobs(proto.Message):
    r"""ChildRollouts job composition

    Attributes:
        create_rollout_jobs (MutableSequence[google.cloud.deploy_v1.types.Job]):
            Output only. List of CreateChildRolloutJobs
        advance_rollout_jobs (MutableSequence[google.cloud.deploy_v1.types.Job]):
            Output only. List of AdvanceChildRolloutJobs
    """

    create_rollout_jobs: MutableSequence["Job"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Job",
    )
    advance_rollout_jobs: MutableSequence["Job"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="Job",
    )


class Job(proto.Message):
    r"""Job represents an operation for a ``Rollout``.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        id (str):
            Output only. The ID of the Job.
        state (google.cloud.deploy_v1.types.Job.State):
            Output only. The current state of the Job.
        skip_message (str):
            Output only. Additional information on why
            the Job was skipped, if available.
        job_run (str):
            Output only. The name of the ``JobRun`` responsible for the
            most recent invocation of this Job.
        deploy_job (google.cloud.deploy_v1.types.DeployJob):
            Output only. A deploy Job.

            This field is a member of `oneof`_ ``job_type``.
        verify_job (google.cloud.deploy_v1.types.VerifyJob):
            Output only. A verify Job.

            This field is a member of `oneof`_ ``job_type``.
        create_child_rollout_job (google.cloud.deploy_v1.types.CreateChildRolloutJob):
            Output only. A createChildRollout Job.

            This field is a member of `oneof`_ ``job_type``.
        advance_child_rollout_job (google.cloud.deploy_v1.types.AdvanceChildRolloutJob):
            Output only. An advanceChildRollout Job.

            This field is a member of `oneof`_ ``job_type``.
    """

    class State(proto.Enum):
        r"""Valid states of a Job.

        Values:
            STATE_UNSPECIFIED (0):
                The Job has an unspecified state.
            PENDING (1):
                The Job is waiting for an earlier Phase(s) or
                Job(s) to complete.
            DISABLED (2):
                The Job is disabled.
            IN_PROGRESS (3):
                The Job is in progress.
            SUCCEEDED (4):
                The Job succeeded.
            FAILED (5):
                The Job failed.
            ABORTED (6):
                The Job was aborted.
            SKIPPED (7):
                The Job was skipped.
            IGNORED (8):
                The Job was ignored.
        """
        STATE_UNSPECIFIED = 0
        PENDING = 1
        DISABLED = 2
        IN_PROGRESS = 3
        SUCCEEDED = 4
        FAILED = 5
        ABORTED = 6
        SKIPPED = 7
        IGNORED = 8

    id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=2,
        enum=State,
    )
    skip_message: str = proto.Field(
        proto.STRING,
        number=8,
    )
    job_run: str = proto.Field(
        proto.STRING,
        number=3,
    )
    deploy_job: "DeployJob" = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="job_type",
        message="DeployJob",
    )
    verify_job: "VerifyJob" = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="job_type",
        message="VerifyJob",
    )
    create_child_rollout_job: "CreateChildRolloutJob" = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="job_type",
        message="CreateChildRolloutJob",
    )
    advance_child_rollout_job: "AdvanceChildRolloutJob" = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="job_type",
        message="AdvanceChildRolloutJob",
    )


class DeployJob(proto.Message):
    r"""A deploy Job."""


class VerifyJob(proto.Message):
    r"""A verify Job."""


class CreateChildRolloutJob(proto.Message):
    r"""A createChildRollout Job."""


class AdvanceChildRolloutJob(proto.Message):
    r"""An advanceChildRollout Job."""


class ListRolloutsRequest(proto.Message):
    r"""ListRolloutsRequest is the request object used by ``ListRollouts``.

    Attributes:
        parent (str):
            Required. The ``Release`` which owns this collection of
            ``Rollout`` objects.
        page_size (int):
            Optional. The maximum number of ``Rollout`` objects to
            return. The service may return fewer than this value. If
            unspecified, at most 50 ``Rollout`` objects will be
            returned. The maximum value is 1000; values above 1000 will
            be set to 1000.
        page_token (str):
            Optional. A page token, received from a previous
            ``ListRollouts`` call. Provide this to retrieve the
            subsequent page.

            When paginating, all other provided parameters match the
            call that provided the page token.
        filter (str):
            Optional. Filter rollouts to be returned. See
            https://google.aip.dev/160
            for more details.
        order_by (str):
            Optional. Field to sort by. See
            https://google.aip.dev/132#ordering for
            more details.
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
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )
    order_by: str = proto.Field(
        proto.STRING,
        number=5,
    )


class ListRolloutsResponse(proto.Message):
    r"""ListRolloutsResponse is the response object reutrned by
    ``ListRollouts``.

    Attributes:
        rollouts (MutableSequence[google.cloud.deploy_v1.types.Rollout]):
            The ``Rollout`` objects.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
        unreachable (MutableSequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    rollouts: MutableSequence["Rollout"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Rollout",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetRolloutRequest(proto.Message):
    r"""GetRolloutRequest is the request object used by ``GetRollout``.

    Attributes:
        name (str):
            Required. Name of the ``Rollout``. Format must be
            projects/{project_id}/locations/{location_name}/deliveryPipelines/{pipeline_name}/releases/{release_name}/rollouts/{rollout_name}.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateRolloutRequest(proto.Message):
    r"""CreateRolloutRequest is the request object used by
    ``CreateRollout``.

    Attributes:
        parent (str):
            Required. The parent collection in which the ``Rollout``
            should be created. Format should be
            projects/{project_id}/locations/{location_name}/deliveryPipelines/{pipeline_name}/releases/{release_name}.
        rollout_id (str):
            Required. ID of the ``Rollout``.
        rollout (google.cloud.deploy_v1.types.Rollout):
            Required. The ``Rollout`` to create.
        request_id (str):
            Optional. A request ID to identify requests.
            Specify a unique request ID so that if you must
            retry your request, the server will know to
            ignore the request if it has already been
            completed. The server will guarantee that for at
            least 60 minutes since the first request.
            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
        validate_only (bool):
            Optional. If set to true, the request is
            validated and the user is provided with an
            expected result, but no actual change is made.
        starting_phase_id (str):
            Optional. The starting phase ID for the ``Rollout``. If
            empty the ``Rollout`` will start at the first phase.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    rollout_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    rollout: "Rollout" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Rollout",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=4,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=5,
    )
    starting_phase_id: str = proto.Field(
        proto.STRING,
        number=7,
    )


class OperationMetadata(proto.Message):
    r"""Represents the metadata of the long-running operation.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation was
            created.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation finished
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
            Output only. Identifies whether the user has requested
            cancellation of the operation. Operations that have
            successfully been cancelled have [Operation.error][] value
            with a [google.rpc.Status.code][google.rpc.Status.code] of
            1, corresponding to ``Code.CANCELLED``.
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


class ApproveRolloutRequest(proto.Message):
    r"""The request object used by ``ApproveRollout``.

    Attributes:
        name (str):
            Required. Name of the Rollout. Format is
            projects/{project}/locations/{location}/deliveryPipelines/{deliveryPipeline}/
            releases/{release}/rollouts/{rollout}.
        approved (bool):
            Required. True = approve; false = reject
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    approved: bool = proto.Field(
        proto.BOOL,
        number=2,
    )


class ApproveRolloutResponse(proto.Message):
    r"""The response object from ``ApproveRollout``."""


class AdvanceRolloutRequest(proto.Message):
    r"""The request object used by ``AdvanceRollout``.

    Attributes:
        name (str):
            Required. Name of the Rollout. Format is
            projects/{project}/locations/{location}/deliveryPipelines/{deliveryPipeline}/
            releases/{release}/rollouts/{rollout}.
        phase_id (str):
            Required. The phase ID to advance the ``Rollout`` to.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    phase_id: str = proto.Field(
        proto.STRING,
        number=2,
    )


class AdvanceRolloutResponse(proto.Message):
    r"""The response object from ``AdvanceRollout``."""


class CancelRolloutRequest(proto.Message):
    r"""The request object used by ``CancelRollout``.

    Attributes:
        name (str):
            Required. Name of the Rollout. Format is
            projects/{project}/locations/{location}/deliveryPipelines/{deliveryPipeline}/
            releases/{release}/rollouts/{rollout}.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CancelRolloutResponse(proto.Message):
    r"""The response object from ``CancelRollout``."""


class IgnoreJobRequest(proto.Message):
    r"""The request object used by ``IgnoreJob``.

    Attributes:
        rollout (str):
            Required. Name of the Rollout. Format is
            projects/{project}/locations/{location}/deliveryPipelines/{deliveryPipeline}/
            releases/{release}/rollouts/{rollout}.
        phase_id (str):
            Required. The phase ID the Job to ignore
            belongs to.
        job_id (str):
            Required. The job ID for the Job to ignore.
    """

    rollout: str = proto.Field(
        proto.STRING,
        number=1,
    )
    phase_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    job_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class IgnoreJobResponse(proto.Message):
    r"""The response object from ``IgnoreJob``."""


class RetryJobRequest(proto.Message):
    r"""RetryJobRequest is the request object used by ``RetryJob``.

    Attributes:
        rollout (str):
            Required. Name of the Rollout. Format is
            projects/{project}/locations/{location}/deliveryPipelines/{deliveryPipeline}/
            releases/{release}/rollouts/{rollout}.
        phase_id (str):
            Required. The phase ID the Job to retry
            belongs to.
        job_id (str):
            Required. The job ID for the Job to retry.
    """

    rollout: str = proto.Field(
        proto.STRING,
        number=1,
    )
    phase_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    job_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class RetryJobResponse(proto.Message):
    r"""The response object from 'RetryJob'."""


class AbandonReleaseRequest(proto.Message):
    r"""The request object used by ``AbandonRelease``.

    Attributes:
        name (str):
            Required. Name of the Release. Format is
            projects/{project}/locations/{location}/deliveryPipelines/{deliveryPipeline}/
            releases/{release}.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class AbandonReleaseResponse(proto.Message):
    r"""The response object for ``AbandonRelease``."""


class JobRun(proto.Message):
    r"""A ``JobRun`` resource in the Google Cloud Deploy API.

    A ``JobRun`` contains information of a single ``Rollout`` job
    evaluation.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Optional. Name of the ``JobRun``. Format is
            projects/{project}/locations/{location}/
            deliveryPipelines/{deliveryPipeline}/releases/{releases}/rollouts/
            {rollouts}/jobRuns/{uuid}.
        uid (str):
            Output only. Unique identifier of the ``JobRun``.
        phase_id (str):
            Output only. ID of the ``Rollout`` phase this ``JobRun``
            belongs in.
        job_id (str):
            Output only. ID of the ``Rollout`` job this ``JobRun``
            corresponds to.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time at which the ``JobRun`` was created.
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time at which the ``JobRun`` was started.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time at which the ``JobRun`` ended.
        state (google.cloud.deploy_v1.types.JobRun.State):
            Output only. The current state of the ``JobRun``.
        deploy_job_run (google.cloud.deploy_v1.types.DeployJobRun):
            Output only. Information specific to a deploy ``JobRun``.

            This field is a member of `oneof`_ ``job_run``.
        verify_job_run (google.cloud.deploy_v1.types.VerifyJobRun):
            Output only. Information specific to a verify ``JobRun``.

            This field is a member of `oneof`_ ``job_run``.
        create_child_rollout_job_run (google.cloud.deploy_v1.types.CreateChildRolloutJobRun):
            Output only. Information specific to a createChildRollout
            ``JobRun``.

            This field is a member of `oneof`_ ``job_run``.
        advance_child_rollout_job_run (google.cloud.deploy_v1.types.AdvanceChildRolloutJobRun):
            Output only. Information specific to an advanceChildRollout
            ``JobRun``

            This field is a member of `oneof`_ ``job_run``.
        etag (str):
            Output only. This checksum is computed by the
            server based on the value of other fields, and
            may be sent on update and delete requests to
            ensure the client has an up-to-date value before
            proceeding.
    """

    class State(proto.Enum):
        r"""Valid states of a ``JobRun``.

        Values:
            STATE_UNSPECIFIED (0):
                The ``JobRun`` has an unspecified state.
            IN_PROGRESS (1):
                The ``JobRun`` is in progress.
            SUCCEEDED (2):
                The ``JobRun`` has succeeded.
            FAILED (3):
                The ``JobRun`` has failed.
            TERMINATING (4):
                The ``JobRun`` is terminating.
            TERMINATED (5):
                The ``JobRun`` was terminated.
        """
        STATE_UNSPECIFIED = 0
        IN_PROGRESS = 1
        SUCCEEDED = 2
        FAILED = 3
        TERMINATING = 4
        TERMINATED = 5

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=2,
    )
    phase_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    job_id: str = proto.Field(
        proto.STRING,
        number=4,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    start_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
    )
    end_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=7,
        message=timestamp_pb2.Timestamp,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=8,
        enum=State,
    )
    deploy_job_run: "DeployJobRun" = proto.Field(
        proto.MESSAGE,
        number=9,
        oneof="job_run",
        message="DeployJobRun",
    )
    verify_job_run: "VerifyJobRun" = proto.Field(
        proto.MESSAGE,
        number=10,
        oneof="job_run",
        message="VerifyJobRun",
    )
    create_child_rollout_job_run: "CreateChildRolloutJobRun" = proto.Field(
        proto.MESSAGE,
        number=12,
        oneof="job_run",
        message="CreateChildRolloutJobRun",
    )
    advance_child_rollout_job_run: "AdvanceChildRolloutJobRun" = proto.Field(
        proto.MESSAGE,
        number=13,
        oneof="job_run",
        message="AdvanceChildRolloutJobRun",
    )
    etag: str = proto.Field(
        proto.STRING,
        number=11,
    )


class DeployJobRun(proto.Message):
    r"""DeployJobRun contains information specific to a deploy ``JobRun``.

    Attributes:
        build (str):
            Output only. The resource name of the Cloud Build ``Build``
            object that is used to deploy. Format is
            projects/{project}/locations/{location}/builds/{build}.
        failure_cause (google.cloud.deploy_v1.types.DeployJobRun.FailureCause):
            Output only. The reason the deploy failed.
            This will always be unspecified while the deploy
            is in progress or if it succeeded.
        failure_message (str):
            Output only. Additional information about the
            deploy failure, if available.
        metadata (google.cloud.deploy_v1.types.DeployJobRunMetadata):
            Output only. Metadata containing information
            about the deploy job run.
        artifact (google.cloud.deploy_v1.types.DeployArtifact):
            Output only. The artifact of a deploy job
            run, if available.
    """

    class FailureCause(proto.Enum):
        r"""Well-known deploy failures.

        Values:
            FAILURE_CAUSE_UNSPECIFIED (0):
                No reason for failure is specified.
            CLOUD_BUILD_UNAVAILABLE (1):
                Cloud Build is not available, either because it is not
                enabled or because Google Cloud Deploy has insufficient
                permissions. See `Required
                permission </deploy/docs/cloud-deploy-service-account#required_permissions>`__.
            EXECUTION_FAILED (2):
                The deploy operation did not complete
                successfully; check Cloud Build logs.
            DEADLINE_EXCEEDED (3):
                The deploy build did not complete within the
                alloted time.
            MISSING_RESOURCES_FOR_CANARY (4):
                There were missing resources in the runtime
                environment required for a canary deployment.
                Check the Cloud Build logs for more information.
            CLOUD_BUILD_REQUEST_FAILED (5):
                Cloud Build failed to fulfill Google Cloud Deploy's request.
                See failure_message for additional details.
        """
        FAILURE_CAUSE_UNSPECIFIED = 0
        CLOUD_BUILD_UNAVAILABLE = 1
        EXECUTION_FAILED = 2
        DEADLINE_EXCEEDED = 3
        MISSING_RESOURCES_FOR_CANARY = 4
        CLOUD_BUILD_REQUEST_FAILED = 5

    build: str = proto.Field(
        proto.STRING,
        number=1,
    )
    failure_cause: FailureCause = proto.Field(
        proto.ENUM,
        number=2,
        enum=FailureCause,
    )
    failure_message: str = proto.Field(
        proto.STRING,
        number=3,
    )
    metadata: "DeployJobRunMetadata" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="DeployJobRunMetadata",
    )
    artifact: "DeployArtifact" = proto.Field(
        proto.MESSAGE,
        number=5,
        message="DeployArtifact",
    )


class VerifyJobRun(proto.Message):
    r"""VerifyJobRun contains information specific to a verify ``JobRun``.

    Attributes:
        build (str):
            Output only. The resource name of the Cloud Build ``Build``
            object that is used to verify. Format is
            projects/{project}/locations/{location}/builds/{build}.
        artifact_uri (str):
            Output only. URI of a directory containing
            the verify artifacts. This contains the Skaffold
            event log.
        event_log_path (str):
            Output only. File path of the Skaffold event
            log relative to the artifact URI.
        failure_cause (google.cloud.deploy_v1.types.VerifyJobRun.FailureCause):
            Output only. The reason the verify failed.
            This will always be unspecified while the verify
            is in progress or if it succeeded.
        failure_message (str):
            Output only. Additional information about the
            verify failure, if available.
    """

    class FailureCause(proto.Enum):
        r"""Well-known verify failures.

        Values:
            FAILURE_CAUSE_UNSPECIFIED (0):
                No reason for failure is specified.
            CLOUD_BUILD_UNAVAILABLE (1):
                Cloud Build is not available, either because it is not
                enabled or because Google Cloud Deploy has insufficient
                permissions. See `required
                permission </deploy/docs/cloud-deploy-service-account#required_permissions>`__.
            EXECUTION_FAILED (2):
                The verify operation did not complete
                successfully; check Cloud Build logs.
            DEADLINE_EXCEEDED (3):
                The verify build did not complete within the
                alloted time.
            VERIFICATION_CONFIG_NOT_FOUND (4):
                No Skaffold verify configuration was found.
            CLOUD_BUILD_REQUEST_FAILED (5):
                Cloud Build failed to fulfill Google Cloud Deploy's request.
                See failure_message for additional details.
        """
        FAILURE_CAUSE_UNSPECIFIED = 0
        CLOUD_BUILD_UNAVAILABLE = 1
        EXECUTION_FAILED = 2
        DEADLINE_EXCEEDED = 3
        VERIFICATION_CONFIG_NOT_FOUND = 4
        CLOUD_BUILD_REQUEST_FAILED = 5

    build: str = proto.Field(
        proto.STRING,
        number=1,
    )
    artifact_uri: str = proto.Field(
        proto.STRING,
        number=2,
    )
    event_log_path: str = proto.Field(
        proto.STRING,
        number=3,
    )
    failure_cause: FailureCause = proto.Field(
        proto.ENUM,
        number=4,
        enum=FailureCause,
    )
    failure_message: str = proto.Field(
        proto.STRING,
        number=5,
    )


class CreateChildRolloutJobRun(proto.Message):
    r"""CreateChildRolloutJobRun contains information specific to a
    createChildRollout ``JobRun``.

    Attributes:
        rollout (str):
            Output only. Name of the ``ChildRollout``. Format is
            projects/{project}/
            locations/{location}/deliveryPipelines/{deliveryPipeline}/
            releases/{release}/rollouts/[a-z][a-z0-9-]{0,62}.
        rollout_phase_id (str):
            Output only. The ID of the childRollout Phase
            initiated by this JobRun.
    """

    rollout: str = proto.Field(
        proto.STRING,
        number=1,
    )
    rollout_phase_id: str = proto.Field(
        proto.STRING,
        number=2,
    )


class AdvanceChildRolloutJobRun(proto.Message):
    r"""AdvanceChildRolloutJobRun contains information specific to a
    advanceChildRollout ``JobRun``.

    Attributes:
        rollout (str):
            Output only. Name of the ``ChildRollout``. Format is
            projects/{project}/
            locations/{location}/deliveryPipelines/{deliveryPipeline}/
            releases/{release}/rollouts/[a-z][a-z0-9-]{0,62}.
        rollout_phase_id (str):
            Output only. the ID of the ChildRollout's
            Phase.
    """

    rollout: str = proto.Field(
        proto.STRING,
        number=1,
    )
    rollout_phase_id: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ListJobRunsRequest(proto.Message):
    r"""ListJobRunsRequest is the request object used by ``ListJobRuns``.

    Attributes:
        parent (str):
            Required. The ``Rollout`` which owns this collection of
            ``JobRun`` objects.
        page_size (int):
            Optional. The maximum number of ``JobRun`` objects to
            return. The service may return fewer than this value. If
            unspecified, at most 50 ``JobRun`` objects will be returned.
            The maximum value is 1000; values above 1000 will be set to
            1000.
        page_token (str):
            Optional. A page token, received from a previous
            ``ListJobRuns`` call. Provide this to retrieve the
            subsequent page.

            When paginating, all other provided parameters match the
            call that provided the page token.
        filter (str):
            Optional. Filter results to be returned. See
            https://google.aip.dev/160 for
            more details.
        order_by (str):
            Optional. Field to sort by. See
            https://google.aip.dev/132#ordering for
            more details.
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
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )
    order_by: str = proto.Field(
        proto.STRING,
        number=5,
    )


class ListJobRunsResponse(proto.Message):
    r"""ListJobRunsResponse is the response object returned by
    ``ListJobRuns``.

    Attributes:
        job_runs (MutableSequence[google.cloud.deploy_v1.types.JobRun]):
            The ``JobRun`` objects.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
        unreachable (MutableSequence[str]):
            Locations that could not be reached
    """

    @property
    def raw_page(self):
        return self

    job_runs: MutableSequence["JobRun"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="JobRun",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetJobRunRequest(proto.Message):
    r"""GetJobRunRequest is the request object used by ``GetJobRun``.

    Attributes:
        name (str):
            Required. Name of the ``JobRun``. Format must be
            projects/{project_id}/locations/{location_name}/deliveryPipelines/{pipeline_name}/releases/{release_name}/rollouts/{rollout_name}/jobRuns/{job_run_name}.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class TerminateJobRunRequest(proto.Message):
    r"""The request object used by ``TerminateJobRun``.

    Attributes:
        name (str):
            Required. Name of the ``JobRun``. Format must be
            projects/{project}/locations/{location}/deliveryPipelines/{deliveryPipeline}/
            releases/{release}/rollouts/{rollout}/jobRuns/{jobRun}.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class TerminateJobRunResponse(proto.Message):
    r"""The response object from ``TerminateJobRun``."""


class Config(proto.Message):
    r"""Service-wide configuration.

    Attributes:
        name (str):
            Name of the configuration.
        supported_versions (MutableSequence[google.cloud.deploy_v1.types.SkaffoldVersion]):
            All supported versions of Skaffold.
        default_skaffold_version (str):
            Default Skaffold version that is assigned
            when a Release is created without specifying a
            Skaffold version.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    supported_versions: MutableSequence["SkaffoldVersion"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="SkaffoldVersion",
    )
    default_skaffold_version: str = proto.Field(
        proto.STRING,
        number=3,
    )


class SkaffoldVersion(proto.Message):
    r"""Details of a supported Skaffold version.

    Attributes:
        version (str):
            Release version number. For example,
            "1.20.3".
        maintenance_mode_time (google.protobuf.timestamp_pb2.Timestamp):
            The time at which this version of skaffold
            will enter maintenance mode.
        support_expiration_time (google.protobuf.timestamp_pb2.Timestamp):
            The time at which this version of skaffold
            will no longer be supported.
        support_end_date (google.type.date_pb2.Date):
            Date when this version is expected to no
            longer be supported.
    """

    version: str = proto.Field(
        proto.STRING,
        number=1,
    )
    maintenance_mode_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    support_expiration_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    support_end_date: date_pb2.Date = proto.Field(
        proto.MESSAGE,
        number=2,
        message=date_pb2.Date,
    )


class GetConfigRequest(proto.Message):
    r"""Request to get a configuration.

    Attributes:
        name (str):
            Required. Name of requested configuration.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
