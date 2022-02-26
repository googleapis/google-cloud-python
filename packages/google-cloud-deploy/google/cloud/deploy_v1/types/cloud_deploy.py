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

from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.type import date_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.deploy.v1",
    manifest={
        "DeliveryPipeline",
        "SerialPipeline",
        "Stage",
        "PipelineReadyCondition",
        "TargetsPresentCondition",
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
        "ListTargetsRequest",
        "ListTargetsResponse",
        "GetTargetRequest",
        "CreateTargetRequest",
        "UpdateTargetRequest",
        "DeleteTargetRequest",
        "Release",
        "BuildArtifact",
        "TargetArtifact",
        "ListReleasesRequest",
        "ListReleasesResponse",
        "GetReleaseRequest",
        "CreateReleaseRequest",
        "Rollout",
        "ListRolloutsRequest",
        "ListRolloutsResponse",
        "GetRolloutRequest",
        "CreateRolloutRequest",
        "OperationMetadata",
        "ApproveRolloutRequest",
        "ApproveRolloutResponse",
        "Config",
        "SkaffoldVersion",
        "GetConfigRequest",
    },
)


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
        annotations (Sequence[google.cloud.deploy_v1.types.DeliveryPipeline.AnnotationsEntry]):
            User annotations. These attributes can only
            be set and used by the user, and not by Google
            Cloud Deploy. See
            https://google.aip.dev/128#annotations for more
            details such as format and size limitations.
        labels (Sequence[google.cloud.deploy_v1.types.DeliveryPipeline.LabelsEntry]):
            Labels are attributes that can be set and used by both the
            user and by Google Cloud Deploy. Labels must meet the
            following constraints: Each resource is limited to 64
            labels. Keys must conform to the regexp:
            ``[a-zA-Z][a-zA-Z0-9_-]{0,62}``. Values must conform to the
            regexp: ``[a-zA-Z0-9_-]{0,63}``. Both keys and values are
            additionally constrained to be <= 128 bytes in size.
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
    """

    name = proto.Field(proto.STRING, number=1,)
    uid = proto.Field(proto.STRING, number=2,)
    description = proto.Field(proto.STRING, number=3,)
    annotations = proto.MapField(proto.STRING, proto.STRING, number=4,)
    labels = proto.MapField(proto.STRING, proto.STRING, number=5,)
    create_time = proto.Field(proto.MESSAGE, number=6, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=7, message=timestamp_pb2.Timestamp,)
    serial_pipeline = proto.Field(
        proto.MESSAGE, number=8, oneof="pipeline", message="SerialPipeline",
    )
    condition = proto.Field(proto.MESSAGE, number=11, message="PipelineCondition",)
    etag = proto.Field(proto.STRING, number=10,)


class SerialPipeline(proto.Message):
    r"""SerialPipeline defines a sequential set of stages for a
    ``DeliveryPipeline``.

    Attributes:
        stages (Sequence[google.cloud.deploy_v1.types.Stage]):
            Each stage specifies configuration for a ``Target``. The
            ordering of this list defines the promotion flow.
    """

    stages = proto.RepeatedField(proto.MESSAGE, number=1, message="Stage",)


class Stage(proto.Message):
    r"""Stage specifies a location to which to deploy.

    Attributes:
        target_id (str):
            The target_id to which this stage points. This field refers
            exclusively to the last segment of a target name. For
            example, this field would just be ``my-target`` (rather than
            ``projects/project/deliveryPipelines/pipeline/targets/my-target``).
            The parent ``DeliveryPipeline`` of the ``Target`` is
            inferred to be the parent ``DeliveryPipeline`` of the
            ``Release`` in which this ``Stage`` lives.
        profiles (Sequence[str]):
            Skaffold profiles to use when rendering the manifest for
            this stage's ``Target``.
    """

    target_id = proto.Field(proto.STRING, number=1,)
    profiles = proto.RepeatedField(proto.STRING, number=2,)


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

    status = proto.Field(proto.BOOL, number=3,)
    update_time = proto.Field(proto.MESSAGE, number=4, message=timestamp_pb2.Timestamp,)


class TargetsPresentCondition(proto.Message):
    r"""TargetsPresentCondition contains information on any Targets
    defined in the Delivery Pipeline that do not actually exist.

    Attributes:
        status (bool):
            True if there aren't any missing Targets.
        missing_targets (Sequence[str]):
            The list of Target names that are missing. For example,
            projects/{project_id}/locations/{location_name}/targets/{target_name}.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Last time the condition was updated.
    """

    status = proto.Field(proto.BOOL, number=1,)
    missing_targets = proto.RepeatedField(proto.STRING, number=2,)
    update_time = proto.Field(proto.MESSAGE, number=4, message=timestamp_pb2.Timestamp,)


class PipelineCondition(proto.Message):
    r"""PipelineCondition contains all conditions relevant to a
    Delivery Pipeline.

    Attributes:
        pipeline_ready_condition (google.cloud.deploy_v1.types.PipelineReadyCondition):
            Details around the Pipeline's overall status.
        targets_present_condition (google.cloud.deploy_v1.types.TargetsPresentCondition):
            Detalis around targets enumerated in the
            pipeline.
    """

    pipeline_ready_condition = proto.Field(
        proto.MESSAGE, number=1, message="PipelineReadyCondition",
    )
    targets_present_condition = proto.Field(
        proto.MESSAGE, number=3, message="TargetsPresentCondition",
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
            Filter builds to be returned. See
            https://google.aip.dev/160 for more details.
        order_by (str):
            Field to sort by. See
            https://google.aip.dev/132#ordering for more
            details.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    filter = proto.Field(proto.STRING, number=4,)
    order_by = proto.Field(proto.STRING, number=5,)


class ListDeliveryPipelinesResponse(proto.Message):
    r"""The response object from ``ListDeliveryPipelines``.

    Attributes:
        delivery_pipelines (Sequence[google.cloud.deploy_v1.types.DeliveryPipeline]):
            The ``DeliveryPipeline`` objects.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
        unreachable (Sequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    delivery_pipelines = proto.RepeatedField(
        proto.MESSAGE, number=1, message="DeliveryPipeline",
    )
    next_page_token = proto.Field(proto.STRING, number=2,)
    unreachable = proto.RepeatedField(proto.STRING, number=3,)


class GetDeliveryPipelineRequest(proto.Message):
    r"""The request object for ``GetDeliveryPipeline``

    Attributes:
        name (str):
            Required. Name of the ``DeliveryPipeline``. Format must be
            projects/{project_id}/locations/{location_name}/deliveryPipelines/{pipeline_name}.
    """

    name = proto.Field(proto.STRING, number=1,)


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

    parent = proto.Field(proto.STRING, number=1,)
    delivery_pipeline_id = proto.Field(proto.STRING, number=2,)
    delivery_pipeline = proto.Field(
        proto.MESSAGE, number=3, message="DeliveryPipeline",
    )
    request_id = proto.Field(proto.STRING, number=4,)
    validate_only = proto.Field(proto.BOOL, number=5,)


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

    update_mask = proto.Field(
        proto.MESSAGE, number=1, message=field_mask_pb2.FieldMask,
    )
    delivery_pipeline = proto.Field(
        proto.MESSAGE, number=2, message="DeliveryPipeline",
    )
    request_id = proto.Field(proto.STRING, number=3,)
    allow_missing = proto.Field(proto.BOOL, number=4,)
    validate_only = proto.Field(proto.BOOL, number=5,)


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

    name = proto.Field(proto.STRING, number=1,)
    request_id = proto.Field(proto.STRING, number=2,)
    allow_missing = proto.Field(proto.BOOL, number=3,)
    validate_only = proto.Field(proto.BOOL, number=4,)
    force = proto.Field(proto.BOOL, number=6,)
    etag = proto.Field(proto.STRING, number=5,)


class Target(proto.Message):
    r"""A ``Target`` resource in the Google Cloud Deploy API.

    A ``Target`` defines a location to which a Skaffold configuration
    can be deployed.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Optional. Name of the ``Target``. Format is
            projects/{project}/locations/{location}/
            deliveryPipelines/{deliveryPipeline}/targets/[a-z][a-z0-9-]{0,62}.
        target_id (str):
            Output only. Resource id of the ``Target``.
        uid (str):
            Output only. Unique identifier of the ``Target``.
        description (str):
            Optional. Description of the ``Target``. Max length is 255
            characters.
        annotations (Sequence[google.cloud.deploy_v1.types.Target.AnnotationsEntry]):
            Optional. User annotations. These attributes
            can only be set and used by the user, and not by
            Google Cloud Deploy. See
            https://google.aip.dev/128#annotations for more
            details such as format and size limitations.
        labels (Sequence[google.cloud.deploy_v1.types.Target.LabelsEntry]):
            Optional. Labels are attributes that can be set and used by
            both the user and by Google Cloud Deploy. Labels must meet
            the following constraints: Each resource is limited to 64
            labels. Keys must conform to the regexp:
            ``[a-zA-Z][a-zA-Z0-9_-]{0,62}``. Values must conform to the
            regexp: ``[a-zA-Z0-9_-]{0,63}``. Both keys and values are
            additionally constrained to be <= 128 bytes in size.
        require_approval (bool):
            Optional. Whether or not the ``Target`` requires approval.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time at which the ``Target`` was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Most recent time at which the ``Target`` was
            updated.
        gke (google.cloud.deploy_v1.types.GkeCluster):
            Information specifying a GKE Cluster.

            This field is a member of `oneof`_ ``deployment_target``.
        etag (str):
            Optional. This checksum is computed by the
            server based on the value of other fields, and
            may be sent on update and delete requests to
            ensure the client has an up-to-date value before
            proceeding.
        execution_configs (Sequence[google.cloud.deploy_v1.types.ExecutionConfig]):
            Configurations for all execution that relates to this
            ``Target``. Each ``ExecutionEnvironmentUsage`` value may
            only be used in a single configuration; using the same value
            multiple times is an error. When one or more configurations
            are specified, they must include the ``RENDER`` and
            ``DEPLOY`` ``ExecutionEnvironmentUsage`` values. When no
            configurations are specified, execution will use the default
            specified in ``DefaultPool``.
    """

    name = proto.Field(proto.STRING, number=1,)
    target_id = proto.Field(proto.STRING, number=2,)
    uid = proto.Field(proto.STRING, number=3,)
    description = proto.Field(proto.STRING, number=4,)
    annotations = proto.MapField(proto.STRING, proto.STRING, number=5,)
    labels = proto.MapField(proto.STRING, proto.STRING, number=6,)
    require_approval = proto.Field(proto.BOOL, number=13,)
    create_time = proto.Field(proto.MESSAGE, number=8, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=9, message=timestamp_pb2.Timestamp,)
    gke = proto.Field(
        proto.MESSAGE, number=15, oneof="deployment_target", message="GkeCluster",
    )
    etag = proto.Field(proto.STRING, number=12,)
    execution_configs = proto.RepeatedField(
        proto.MESSAGE, number=16, message="ExecutionConfig",
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
        usages (Sequence[google.cloud.deploy_v1.types.ExecutionConfig.ExecutionEnvironmentUsage]):
            Required. Usages when this configuration
            should be applied.
        default_pool (google.cloud.deploy_v1.types.DefaultPool):
            Optional. Use default Cloud Build pool.

            This field is a member of `oneof`_ ``execution_environment``.
        private_pool (google.cloud.deploy_v1.types.PrivatePool):
            Optional. Use private Cloud Build pool.

            This field is a member of `oneof`_ ``execution_environment``.
    """

    class ExecutionEnvironmentUsage(proto.Enum):
        r"""Possible usages of this configuration."""
        EXECUTION_ENVIRONMENT_USAGE_UNSPECIFIED = 0
        RENDER = 1
        DEPLOY = 2

    usages = proto.RepeatedField(proto.ENUM, number=1, enum=ExecutionEnvironmentUsage,)
    default_pool = proto.Field(
        proto.MESSAGE, number=2, oneof="execution_environment", message="DefaultPool",
    )
    private_pool = proto.Field(
        proto.MESSAGE, number=3, oneof="execution_environment", message="PrivatePool",
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

    service_account = proto.Field(proto.STRING, number=1,)
    artifact_storage = proto.Field(proto.STRING, number=2,)


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

    worker_pool = proto.Field(proto.STRING, number=1,)
    service_account = proto.Field(proto.STRING, number=2,)
    artifact_storage = proto.Field(proto.STRING, number=3,)


class GkeCluster(proto.Message):
    r"""Information specifying a GKE Cluster.

    Attributes:
        cluster (str):
            Information specifying a GKE Cluster. Format is
            \`projects/{project_id}/locations/{location_id}/clusters/{cluster_id}.
    """

    cluster = proto.Field(proto.STRING, number=1,)


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
            Optional. Filter builds to be returned. See
            https://google.aip.dev/160 for more details.
        order_by (str):
            Optional. Field to sort by. See
            https://google.aip.dev/132#ordering for more
            details.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    filter = proto.Field(proto.STRING, number=4,)
    order_by = proto.Field(proto.STRING, number=5,)


class ListTargetsResponse(proto.Message):
    r"""The response object from ``ListTargets``.

    Attributes:
        targets (Sequence[google.cloud.deploy_v1.types.Target]):
            The ``Target`` objects.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
        unreachable (Sequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    targets = proto.RepeatedField(proto.MESSAGE, number=1, message="Target",)
    next_page_token = proto.Field(proto.STRING, number=2,)
    unreachable = proto.RepeatedField(proto.STRING, number=3,)


class GetTargetRequest(proto.Message):
    r"""The request object for ``GetTarget``.

    Attributes:
        name (str):
            Required. Name of the ``Target``. Format must be
            projects/{project_id}/locations/{location_name}/targets/{target_name}.
    """

    name = proto.Field(proto.STRING, number=1,)


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

    parent = proto.Field(proto.STRING, number=1,)
    target_id = proto.Field(proto.STRING, number=2,)
    target = proto.Field(proto.MESSAGE, number=3, message="Target",)
    request_id = proto.Field(proto.STRING, number=4,)
    validate_only = proto.Field(proto.BOOL, number=5,)


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

    update_mask = proto.Field(
        proto.MESSAGE, number=1, message=field_mask_pb2.FieldMask,
    )
    target = proto.Field(proto.MESSAGE, number=2, message="Target",)
    request_id = proto.Field(proto.STRING, number=3,)
    allow_missing = proto.Field(proto.BOOL, number=4,)
    validate_only = proto.Field(proto.BOOL, number=5,)


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
            Optional. If set to true, then deleting an
            already deleted or non-existing DeliveryPipeline
            will succeed.
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

    name = proto.Field(proto.STRING, number=1,)
    request_id = proto.Field(proto.STRING, number=2,)
    allow_missing = proto.Field(proto.BOOL, number=3,)
    validate_only = proto.Field(proto.BOOL, number=4,)
    etag = proto.Field(proto.STRING, number=5,)


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
        annotations (Sequence[google.cloud.deploy_v1.types.Release.AnnotationsEntry]):
            User annotations. These attributes can only
            be set and used by the user, and not by Google
            Cloud Deploy. See
            https://google.aip.dev/128#annotations for more
            details such as format and size limitations.
        labels (Sequence[google.cloud.deploy_v1.types.Release.LabelsEntry]):
            Labels are attributes that can be set and used by both the
            user and by Google Cloud Deploy. Labels must meet the
            following constraints: Each resource is limited to 64
            labels. Keys must conform to the regexp:
            ``[a-zA-Z][a-zA-Z0-9_-]{0,62}``. Values must conform to the
            regexp: ``[a-zA-Z0-9_-]{0,63}``. Both keys and values are
            additionally constrained to be <= 128 bytes in size.
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
        build_artifacts (Sequence[google.cloud.deploy_v1.types.BuildArtifact]):
            List of artifacts to pass through to Skaffold
            command.
        delivery_pipeline_snapshot (google.cloud.deploy_v1.types.DeliveryPipeline):
            Output only. Snapshot of the parent pipeline
            taken at release creation time.
        target_snapshots (Sequence[google.cloud.deploy_v1.types.Target]):
            Output only. Snapshot of the parent
            pipeline's targets taken at release creation
            time.
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
        target_artifacts (Sequence[google.cloud.deploy_v1.types.Release.TargetArtifactsEntry]):
            Output only. Map from target ID to the target
            artifacts created during the render operation.
        target_renders (Sequence[google.cloud.deploy_v1.types.Release.TargetRendersEntry]):
            Output only. Map from target ID to details of
            the render operation for that target.
    """

    class RenderState(proto.Enum):
        r"""Valid states of the render operation."""
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
        """

        class TargetRenderState(proto.Enum):
            r"""Valid states of the render operation."""
            TARGET_RENDER_STATE_UNSPECIFIED = 0
            SUCCEEDED = 1
            FAILED = 2
            IN_PROGRESS = 3

        rendering_build = proto.Field(proto.STRING, number=1,)
        rendering_state = proto.Field(
            proto.ENUM, number=2, enum="Release.TargetRender.TargetRenderState",
        )

    name = proto.Field(proto.STRING, number=1,)
    uid = proto.Field(proto.STRING, number=2,)
    description = proto.Field(proto.STRING, number=3,)
    annotations = proto.MapField(proto.STRING, proto.STRING, number=4,)
    labels = proto.MapField(proto.STRING, proto.STRING, number=5,)
    create_time = proto.Field(proto.MESSAGE, number=6, message=timestamp_pb2.Timestamp,)
    render_start_time = proto.Field(
        proto.MESSAGE, number=7, message=timestamp_pb2.Timestamp,
    )
    render_end_time = proto.Field(
        proto.MESSAGE, number=8, message=timestamp_pb2.Timestamp,
    )
    skaffold_config_uri = proto.Field(proto.STRING, number=17,)
    skaffold_config_path = proto.Field(proto.STRING, number=9,)
    build_artifacts = proto.RepeatedField(
        proto.MESSAGE, number=10, message="BuildArtifact",
    )
    delivery_pipeline_snapshot = proto.Field(
        proto.MESSAGE, number=11, message="DeliveryPipeline",
    )
    target_snapshots = proto.RepeatedField(proto.MESSAGE, number=12, message="Target",)
    render_state = proto.Field(proto.ENUM, number=13, enum=RenderState,)
    etag = proto.Field(proto.STRING, number=16,)
    skaffold_version = proto.Field(proto.STRING, number=19,)
    target_artifacts = proto.MapField(
        proto.STRING, proto.MESSAGE, number=20, message="TargetArtifact",
    )
    target_renders = proto.MapField(
        proto.STRING, proto.MESSAGE, number=22, message=TargetRender,
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

    image = proto.Field(proto.STRING, number=3,)
    tag = proto.Field(proto.STRING, number=2,)


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
    """

    artifact_uri = proto.Field(proto.STRING, number=4, oneof="uri",)
    skaffold_config_path = proto.Field(proto.STRING, number=2,)
    manifest_path = proto.Field(proto.STRING, number=3,)


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
            Optional. Filter builds to be returned. See
            https://google.aip.dev/160 for more details.
        order_by (str):
            Optional. Field to sort by. See
            https://google.aip.dev/132#ordering for more
            details.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    filter = proto.Field(proto.STRING, number=4,)
    order_by = proto.Field(proto.STRING, number=5,)


class ListReleasesResponse(proto.Message):
    r"""The response object from ``ListReleases``.

    Attributes:
        releases (Sequence[google.cloud.deploy_v1.types.Release]):
            The ``Release`` objects.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
        unreachable (Sequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    releases = proto.RepeatedField(proto.MESSAGE, number=1, message="Release",)
    next_page_token = proto.Field(proto.STRING, number=2,)
    unreachable = proto.RepeatedField(proto.STRING, number=3,)


class GetReleaseRequest(proto.Message):
    r"""The request object for ``GetRelease``.

    Attributes:
        name (str):
            Required. Name of the ``Release``. Format must be
            projects/{project_id}/locations/{location_name}/deliveryPipelines/{pipeline_name}/releases/{release_name}.
    """

    name = proto.Field(proto.STRING, number=1,)


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

    parent = proto.Field(proto.STRING, number=1,)
    release_id = proto.Field(proto.STRING, number=2,)
    release = proto.Field(proto.MESSAGE, number=3, message="Release",)
    request_id = proto.Field(proto.STRING, number=4,)
    validate_only = proto.Field(proto.BOOL, number=5,)


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
        annotations (Sequence[google.cloud.deploy_v1.types.Rollout.AnnotationsEntry]):
            User annotations. These attributes can only
            be set and used by the user, and not by Google
            Cloud Deploy. See
            https://google.aip.dev/128#annotations for more
            details such as format and size limitations.
        labels (Sequence[google.cloud.deploy_v1.types.Rollout.LabelsEntry]):
            Labels are attributes that can be set and used by both the
            user and by Google Cloud Deploy. Labels must meet the
            following constraints: Each resource is limited to 64
            labels. Keys must conform to the regexp:
            ``[a-zA-Z][a-zA-Z0-9_-]{0,62}``. Values must conform to the
            regexp: ``[a-zA-Z0-9_-]{0,63}``. Both keys and values are
            additionally constrained to be <= 128 bytes in size.
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
            Output only. Reason the build failed. Empty
            if the build succeeded.
        deploying_build (str):
            Output only. The resource name of the Cloud Build ``Build``
            object that is used to deploy the Rollout. Format is
            ``projects/{project}/locations/{location}/builds/{build}``.
        etag (str):
            This checksum is computed by the server based
            on the value of other fields, and may be sent on
            update and delete requests to ensure the client
            has an up-to-date value before proceeding.
    """

    class ApprovalState(proto.Enum):
        r"""Valid approval states of a ``Rollout``."""
        APPROVAL_STATE_UNSPECIFIED = 0
        NEEDS_APPROVAL = 1
        DOES_NOT_NEED_APPROVAL = 2
        APPROVED = 3
        REJECTED = 4

    class State(proto.Enum):
        r"""Valid states of a ``Rollout``."""
        STATE_UNSPECIFIED = 0
        SUCCEEDED = 1
        FAILED = 2
        IN_PROGRESS = 3
        PENDING_APPROVAL = 4
        APPROVAL_REJECTED = 5
        PENDING = 6
        PENDING_RELEASE = 7

    name = proto.Field(proto.STRING, number=1,)
    uid = proto.Field(proto.STRING, number=2,)
    description = proto.Field(proto.STRING, number=3,)
    annotations = proto.MapField(proto.STRING, proto.STRING, number=4,)
    labels = proto.MapField(proto.STRING, proto.STRING, number=5,)
    create_time = proto.Field(proto.MESSAGE, number=6, message=timestamp_pb2.Timestamp,)
    approve_time = proto.Field(
        proto.MESSAGE, number=7, message=timestamp_pb2.Timestamp,
    )
    enqueue_time = proto.Field(
        proto.MESSAGE, number=8, message=timestamp_pb2.Timestamp,
    )
    deploy_start_time = proto.Field(
        proto.MESSAGE, number=9, message=timestamp_pb2.Timestamp,
    )
    deploy_end_time = proto.Field(
        proto.MESSAGE, number=10, message=timestamp_pb2.Timestamp,
    )
    target_id = proto.Field(proto.STRING, number=18,)
    approval_state = proto.Field(proto.ENUM, number=12, enum=ApprovalState,)
    state = proto.Field(proto.ENUM, number=13, enum=State,)
    failure_reason = proto.Field(proto.STRING, number=14,)
    deploying_build = proto.Field(proto.STRING, number=17,)
    etag = proto.Field(proto.STRING, number=16,)


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
            Optional. Filter builds to be returned. See
            https://google.aip.dev/160 for more details.
        order_by (str):
            Optional. Field to sort by. See
            https://google.aip.dev/132#ordering for more
            details.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    filter = proto.Field(proto.STRING, number=4,)
    order_by = proto.Field(proto.STRING, number=5,)


class ListRolloutsResponse(proto.Message):
    r"""ListRolloutsResponse is the response object reutrned by
    ``ListRollouts``.

    Attributes:
        rollouts (Sequence[google.cloud.deploy_v1.types.Rollout]):
            The ``Rollout`` objects.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
        unreachable (Sequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    rollouts = proto.RepeatedField(proto.MESSAGE, number=1, message="Rollout",)
    next_page_token = proto.Field(proto.STRING, number=2,)
    unreachable = proto.RepeatedField(proto.STRING, number=3,)


class GetRolloutRequest(proto.Message):
    r"""GetRolloutRequest is the request object used by ``GetRollout``.

    Attributes:
        name (str):
            Required. Name of the ``Rollout``. Format must be
            projects/{project_id}/locations/{location_name}/deliveryPipelines/{pipeline_name}/releases/{release_name}/rollouts/{rollout_name}.
    """

    name = proto.Field(proto.STRING, number=1,)


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
    """

    parent = proto.Field(proto.STRING, number=1,)
    rollout_id = proto.Field(proto.STRING, number=2,)
    rollout = proto.Field(proto.MESSAGE, number=3, message="Rollout",)
    request_id = proto.Field(proto.STRING, number=4,)
    validate_only = proto.Field(proto.BOOL, number=5,)


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

    create_time = proto.Field(proto.MESSAGE, number=1, message=timestamp_pb2.Timestamp,)
    end_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)
    target = proto.Field(proto.STRING, number=3,)
    verb = proto.Field(proto.STRING, number=4,)
    status_message = proto.Field(proto.STRING, number=5,)
    requested_cancellation = proto.Field(proto.BOOL, number=6,)
    api_version = proto.Field(proto.STRING, number=7,)


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

    name = proto.Field(proto.STRING, number=1,)
    approved = proto.Field(proto.BOOL, number=2,)


class ApproveRolloutResponse(proto.Message):
    r"""The response object from ``ApproveRollout``.
    """


class Config(proto.Message):
    r"""Service-wide configuration.

    Attributes:
        name (str):
            Name of the configuration.
        supported_versions (Sequence[google.cloud.deploy_v1.types.SkaffoldVersion]):
            Output only. All supported versions of
            Skaffold.
        default_skaffold_version (str):
            Output only. Default Skaffold version that is
            assigned when a Release is created without
            specifying a Skaffold version.
    """

    name = proto.Field(proto.STRING, number=1,)
    supported_versions = proto.RepeatedField(
        proto.MESSAGE, number=2, message="SkaffoldVersion",
    )
    default_skaffold_version = proto.Field(proto.STRING, number=3,)


class SkaffoldVersion(proto.Message):
    r"""Details of a supported Skaffold version.

    Attributes:
        version (str):
            Release version number. For example,
            "1.20.3".
        support_end_date (google.type.date_pb2.Date):
            Date when this version is expected to no
            longer be supported.
    """

    version = proto.Field(proto.STRING, number=1,)
    support_end_date = proto.Field(proto.MESSAGE, number=2, message=date_pb2.Date,)


class GetConfigRequest(proto.Message):
    r"""Request to get a configuration.

    Attributes:
        name (str):
            Required. Name of requested configuration.
    """

    name = proto.Field(proto.STRING, number=1,)


__all__ = tuple(sorted(__protobuf__.manifest))
