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
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.enterpriseknowledgegraph_v1.types import job_state, operation_metadata

__protobuf__ = proto.module(
    package="google.cloud.enterpriseknowledgegraph.v1",
    manifest={
        "InputConfig",
        "BigQueryInputConfig",
        "OutputConfig",
        "ReconConfig",
        "ConnectedComponentsConfig",
        "AffinityClusteringConfig",
        "DeleteOperationMetadata",
        "CreateEntityReconciliationJobRequest",
        "GetEntityReconciliationJobRequest",
        "ListEntityReconciliationJobsRequest",
        "ListEntityReconciliationJobsResponse",
        "CancelEntityReconciliationJobRequest",
        "DeleteEntityReconciliationJobRequest",
        "EntityReconciliationJob",
    },
)


class InputConfig(proto.Message):
    r"""The desired input location and metadata.

    Attributes:
        bigquery_input_configs (Sequence[google.cloud.enterpriseknowledgegraph_v1.types.BigQueryInputConfig]):
            Set of input BigQuery tables.
        entity_type (google.cloud.enterpriseknowledgegraph_v1.types.InputConfig.EntityType):
            Entity type
        previous_result_bigquery_table (str):
            Optional. Provide the bigquery table containing the previous
            results if cluster ID stability is desired. Format is
            ``projects/*/datasets/*/tables/*``.
    """

    class EntityType(proto.Enum):
        r"""The type of entities we will support. Currently, we only
        support people, establishment, property, and product types. If
        the type is unspecified, it will be generic type.
        """
        ENTITY_TYPE_UNSPECIFIED = 0
        PEOPLE = 1
        ESTABLISHMENT = 2
        PROPERTY = 3
        PRODUCT = 4
        ORGANIZATION = 5
        LOCAL_BUSINESS = 6
        PERSON = 7

    bigquery_input_configs = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="BigQueryInputConfig",
    )
    entity_type = proto.Field(
        proto.ENUM,
        number=2,
        enum=EntityType,
    )
    previous_result_bigquery_table = proto.Field(
        proto.STRING,
        number=3,
    )


class BigQueryInputConfig(proto.Message):
    r"""The input config for BigQuery tables.

    Attributes:
        bigquery_table (str):
            Required. Format is ``projects/*/datasets/*/tables/*``.
        gcs_uri (str):
            Required. Schema mapping file
    """

    bigquery_table = proto.Field(
        proto.STRING,
        number=1,
    )
    gcs_uri = proto.Field(
        proto.STRING,
        number=2,
    )


class OutputConfig(proto.Message):
    r"""The desired output location and metadata.

    Attributes:
        bigquery_dataset (str):
            Format is “projects/\ */datasets/*\ ”.
    """

    bigquery_dataset = proto.Field(
        proto.STRING,
        number=1,
    )


class ReconConfig(proto.Message):
    r"""Recon configs

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        connected_components_config (google.cloud.enterpriseknowledgegraph_v1.types.ConnectedComponentsConfig):
            Configs for connected components.

            This field is a member of `oneof`_ ``clustering_config``.
        affinity_clustering_config (google.cloud.enterpriseknowledgegraph_v1.types.AffinityClusteringConfig):
            Configs for affinity clustering.

            This field is a member of `oneof`_ ``clustering_config``.
        options (google.cloud.enterpriseknowledgegraph_v1.types.ReconConfig.Options):
            Extra options that affect entity clustering
            behavior.
        model_config (google.cloud.enterpriseknowledgegraph_v1.types.ReconConfig.ModelConfig):
            Model Configs
    """

    class Options(proto.Message):
        r"""Options for experimental changes on entity clustering
        behavior.

        Attributes:
            enable_geocoding_separation (bool):
                If true, separate clusters by their
                geographic region (from geocoding). Uses the
                following entity features:
                - schema.org/addressLocality
                - schema.org/addressRegion
                - schema.org/addressCountry
                Warning: processing will no longer be
                regionalized!
        """

        enable_geocoding_separation = proto.Field(
            proto.BOOL,
            number=100,
        )

    class ModelConfig(proto.Message):
        r"""Model Configs

        Attributes:
            model_name (str):
                Model name. Refer to external documentation
                for valid names. If unspecified, it defaults to
                the one mentioned in the documentation.
            version_tag (str):
                Model version tag. Refer to external
                documentation for valid tags. If unspecified, it
                defaults to the one mentioned in the
                documentation.
        """

        model_name = proto.Field(
            proto.STRING,
            number=1,
        )
        version_tag = proto.Field(
            proto.STRING,
            number=2,
        )

    connected_components_config = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="clustering_config",
        message="ConnectedComponentsConfig",
    )
    affinity_clustering_config = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="clustering_config",
        message="AffinityClusteringConfig",
    )
    options = proto.Field(
        proto.MESSAGE,
        number=3,
        message=Options,
    )
    model_config = proto.Field(
        proto.MESSAGE,
        number=4,
        message=ModelConfig,
    )


class ConnectedComponentsConfig(proto.Message):
    r"""Options for connected components.

    Attributes:
        weight_threshold (float):
            Threshold used for connected components.
            Default value is 0.85.
    """

    weight_threshold = proto.Field(
        proto.FLOAT,
        number=1,
    )


class AffinityClusteringConfig(proto.Message):
    r"""Options for affinity clustering.

    Attributes:
        compression_round_count (int):
            Number of iterations to perform. Default
            value is 1.
    """

    compression_round_count = proto.Field(
        proto.INT64,
        number=1,
    )


class DeleteOperationMetadata(proto.Message):
    r"""Details of operations that perform deletes of any entities.

    Attributes:
        common_metadata (google.cloud.enterpriseknowledgegraph_v1.types.CommonOperationMetadata):
            The common part of the operation metadata.
    """

    common_metadata = proto.Field(
        proto.MESSAGE,
        number=1,
        message=operation_metadata.CommonOperationMetadata,
    )


class CreateEntityReconciliationJobRequest(proto.Message):
    r"""Request message for CreateEntityReconciliationJob.

    Attributes:
        parent (str):
            Required. The resource name of the Location to create the
            EntityReconciliationJob in. Format:
            ``projects/{project}/locations/{location}``
        entity_reconciliation_job (google.cloud.enterpriseknowledgegraph_v1.types.EntityReconciliationJob):
            Required. The EntityReconciliationJob to
            create.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    entity_reconciliation_job = proto.Field(
        proto.MESSAGE,
        number=2,
        message="EntityReconciliationJob",
    )


class GetEntityReconciliationJobRequest(proto.Message):
    r"""Request message for GetEntityReconciliationJob.

    Attributes:
        name (str):
            Required. The name of the EntityReconciliationJob resource.
            Format:
            ``projects/{project}/locations/{location}/entityReconciliationJobs/{entity_reconciliation_job}``
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class ListEntityReconciliationJobsRequest(proto.Message):
    r"""Request message for
    [EnterpriseKnowledgeGraphService.ListEntityReconciliationJobs][google.cloud.enterpriseknowledgegraph.v1.EnterpriseKnowledgeGraphService.ListEntityReconciliationJobs].

    Attributes:
        parent (str):
            Required. The name of the EntityReconciliationJob's parent
            resource. Format:
            ``projects/{project}/locations/{location}``
        filter (str):
            An expression for filtering the results of the request. For
            field names both snake_case and camelCase are supported.
        page_size (int):
            The standard list page size.
        page_token (str):
            The standard list page token.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    filter = proto.Field(
        proto.STRING,
        number=2,
    )
    page_size = proto.Field(
        proto.INT32,
        number=3,
    )
    page_token = proto.Field(
        proto.STRING,
        number=4,
    )


class ListEntityReconciliationJobsResponse(proto.Message):
    r"""Response message for
    [EnterpriseKnowledgeGraphService.ListEntityReconciliationJobs][google.cloud.enterpriseknowledgegraph.v1.EnterpriseKnowledgeGraphService.ListEntityReconciliationJobs].

    Attributes:
        entity_reconciliation_jobs (Sequence[google.cloud.enterpriseknowledgegraph_v1.types.EntityReconciliationJob]):
            A list of EntityReconciliationJobs that
            matches the specified filter in the request.
        next_page_token (str):
            The standard List next-page token.
    """

    @property
    def raw_page(self):
        return self

    entity_reconciliation_jobs = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="EntityReconciliationJob",
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class CancelEntityReconciliationJobRequest(proto.Message):
    r"""Request message for CancelEntityReconciliationJob.

    Attributes:
        name (str):
            Required. The name of the EntityReconciliationJob resource.
            Format:
            ``projects/{project}/locations/{location}/entityReconciliationJobs/{entity_reconciliation_job}``
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class DeleteEntityReconciliationJobRequest(proto.Message):
    r"""Request message for DeleteEntityReconciliationJob.

    Attributes:
        name (str):
            Required. The name of the EntityReconciliationJob resource.
            Format:
            ``projects/{project}/locations/{location}/entityReconciliationJobs/{entity_reconciliation_job}``
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class EntityReconciliationJob(proto.Message):
    r"""Entity reconciliation job message.

    Attributes:
        name (str):
            Output only. Resource name of the
            EntityReconciliationJob.
        input_config (google.cloud.enterpriseknowledgegraph_v1.types.InputConfig):
            Required. Information about the input
            BigQuery tables.
        output_config (google.cloud.enterpriseknowledgegraph_v1.types.OutputConfig):
            Required. The desired output location.
        state (google.cloud.enterpriseknowledgegraph_v1.types.JobState):
            Output only. The detailed state of the job.
        error (google.rpc.status_pb2.Status):
            Output only. Only populated when the job's state is
            JOB_STATE_FAILED or JOB_STATE_CANCELLED.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when the
            EntityReconciliationJob was created.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when the EntityReconciliationJob entered
            any of the following states: ``JOB_STATE_SUCCEEDED``,
            ``JOB_STATE_FAILED``, ``JOB_STATE_CANCELLED``.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when the
            EntityReconciliationJob was most recently
            updated.
        recon_config (google.cloud.enterpriseknowledgegraph_v1.types.ReconConfig):
            Optional. Recon configs to adjust the
            clustering behavior.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    input_config = proto.Field(
        proto.MESSAGE,
        number=2,
        message="InputConfig",
    )
    output_config = proto.Field(
        proto.MESSAGE,
        number=3,
        message="OutputConfig",
    )
    state = proto.Field(
        proto.ENUM,
        number=4,
        enum=job_state.JobState,
    )
    error = proto.Field(
        proto.MESSAGE,
        number=5,
        message=status_pb2.Status,
    )
    create_time = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
    )
    end_time = proto.Field(
        proto.MESSAGE,
        number=7,
        message=timestamp_pb2.Timestamp,
    )
    update_time = proto.Field(
        proto.MESSAGE,
        number=8,
        message=timestamp_pb2.Timestamp,
    )
    recon_config = proto.Field(
        proto.MESSAGE,
        number=9,
        message="ReconConfig",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
