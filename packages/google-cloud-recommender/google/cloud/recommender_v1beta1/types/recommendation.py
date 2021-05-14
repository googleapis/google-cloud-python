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

from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.type import money_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.recommender.v1beta1",
    manifest={
        "Recommendation",
        "RecommendationContent",
        "OperationGroup",
        "Operation",
        "ValueMatcher",
        "CostProjection",
        "Impact",
        "RecommendationStateInfo",
    },
)


class Recommendation(proto.Message):
    r"""A recommendation along with a suggested action. E.g., a
    rightsizing recommendation for an underutilized VM, IAM role
    recommendations, etc

    Attributes:
        name (str):
            Name of recommendation.
        description (str):
            Free-form human readable summary in English.
            The maximum length is 500 characters.
        recommender_subtype (str):
            Contains an identifier for a subtype of recommendations
            produced for the same recommender. Subtype is a function of
            content and impact, meaning a new subtype might be added
            when significant changes to ``content`` or
            ``primary_impact.category`` are introduced. See the
            Recommenders section to see a list of subtypes for a given
            Recommender.

            Examples: For recommender = "google.iam.policy.Recommender",
            recommender_subtype can be one of
            "REMOVE_ROLE"/"REPLACE_ROLE".
        last_refresh_time (google.protobuf.timestamp_pb2.Timestamp):
            Last time this recommendation was refreshed
            by the system that created it in the first
            place.
        primary_impact (google.cloud.recommender_v1beta1.types.Impact):
            The primary impact that this recommendation
            can have while trying to optimize for one
            category.
        additional_impact (Sequence[google.cloud.recommender_v1beta1.types.Impact]):
            Optional set of additional impact that this
            recommendation may have when trying to optimize
            for the primary category. These may be positive
            or negative.
        content (google.cloud.recommender_v1beta1.types.RecommendationContent):
            Content of the recommendation describing
            recommended changes to resources.
        state_info (google.cloud.recommender_v1beta1.types.RecommendationStateInfo):
            Information for state. Contains state and
            metadata.
        etag (str):
            Fingerprint of the Recommendation. Provides
            optimistic locking when updating states.
        associated_insights (Sequence[google.cloud.recommender_v1beta1.types.Recommendation.InsightReference]):
            Insights that led to this recommendation.
    """

    class InsightReference(proto.Message):
        r"""Reference to an associated insight.
        Attributes:
            insight (str):
                Insight resource name, e.g.
                projects/[PROJECT_NUMBER]/locations/[LOCATION]/insightTypes/[INSIGHT_TYPE_ID]/insights/[INSIGHT_ID]
        """

        insight = proto.Field(proto.STRING, number=1,)

    name = proto.Field(proto.STRING, number=1,)
    description = proto.Field(proto.STRING, number=2,)
    recommender_subtype = proto.Field(proto.STRING, number=12,)
    last_refresh_time = proto.Field(
        proto.MESSAGE, number=4, message=timestamp_pb2.Timestamp,
    )
    primary_impact = proto.Field(proto.MESSAGE, number=5, message="Impact",)
    additional_impact = proto.RepeatedField(proto.MESSAGE, number=6, message="Impact",)
    content = proto.Field(proto.MESSAGE, number=7, message="RecommendationContent",)
    state_info = proto.Field(
        proto.MESSAGE, number=10, message="RecommendationStateInfo",
    )
    etag = proto.Field(proto.STRING, number=11,)
    associated_insights = proto.RepeatedField(
        proto.MESSAGE, number=14, message=InsightReference,
    )


class RecommendationContent(proto.Message):
    r"""Contains what resources are changing and how they are
    changing.

    Attributes:
        operation_groups (Sequence[google.cloud.recommender_v1beta1.types.OperationGroup]):
            Operations to one or more Google Cloud
            resources grouped in such a way that, all
            operations within one group are expected to be
            performed atomically and in an order.
    """

    operation_groups = proto.RepeatedField(
        proto.MESSAGE, number=2, message="OperationGroup",
    )


class OperationGroup(proto.Message):
    r"""Group of operations that need to be performed atomically.
    Attributes:
        operations (Sequence[google.cloud.recommender_v1beta1.types.Operation]):
            List of operations across one or more
            resources that belong to this group. Loosely
            based on RFC6902 and should be performed in the
            order they appear.
    """

    operations = proto.RepeatedField(proto.MESSAGE, number=1, message="Operation",)


class Operation(proto.Message):
    r"""Contains an operation for a resource loosely based on the JSON-PATCH
    format with support for:

    -  Custom filters for describing partial array patch.
    -  Extended path values for describing nested arrays.
    -  Custom fields for describing the resource for which the operation
       is being described.
    -  Allows extension to custom operations not natively supported by
       RFC6902. See https://tools.ietf.org/html/rfc6902 for details on
       the original RFC.

    Attributes:
        action (str):
            Type of this operation. Contains one of
            'and', 'remove', 'replace', 'move', 'copy',
            'test' and 'custom' operations. This field is
            case-insensitive and always populated.
        resource_type (str):
            Type of GCP resource being modified/tested.
            This field is always populated. Example:
            cloudresourcemanager.googleapis.com/Project,
            compute.googleapis.com/Instance
        resource (str):
            Contains the fully qualified resource name.
            This field is always populated. ex:
            //cloudresourcemanager.googleapis.com/projects/foo.
        path (str):
            Path to the target field being operated on.
            If the operation is at the resource level, then
            path should be "/". This field is always
            populated.
        source_resource (str):
            Can be set with action 'copy' to copy resource configuration
            across different resources of the same type. Example: A
            resource clone can be done via action = 'copy', path = "/",
            from = "/", source_resource = and resource_name = . This
            field is empty for all other values of ``action``.
        source_path (str):
            Can be set with action 'copy' or 'move' to indicate the
            source field within resource or source_resource, ignored if
            provided for other operation types.
        value (google.protobuf.struct_pb2.Value):
            Value for the ``path`` field. Will be set for
            actions:'add'/'replace'. Maybe set for action: 'test'.
            Either this or ``value_matcher`` will be set for 'test'
            operation. An exact match must be performed.
        value_matcher (google.cloud.recommender_v1beta1.types.ValueMatcher):
            Can be set for action 'test' for advanced matching for the
            value of 'path' field. Either this or ``value`` will be set
            for 'test' operation.
        path_filters (Sequence[google.cloud.recommender_v1beta1.types.Operation.PathFiltersEntry]):
            Set of filters to apply if ``path`` refers to array elements
            or nested array elements in order to narrow down to a single
            unique element that is being tested/modified. This is
            intended to be an exact match per filter. To perform
            advanced matching, use path_value_matchers.

            -  Example: ``{ "/versions/*/name" : "it-123"
               "/versions/*/targetSize/percent": 20 }``
            -  Example: ``{ "/bindings/*/role": "roles/owner"
               "/bindings/*/condition" : null }``
            -  Example: ``{ "/bindings/*/role": "roles/owner"
               "/bindings/*/members/*" : ["x@example.com",
               "y@example.com"] }`` When both path_filters and
               path_value_matchers are set, an implicit AND must be
               performed.
        path_value_matchers (Sequence[google.cloud.recommender_v1beta1.types.Operation.PathValueMatchersEntry]):
            Similar to path_filters, this contains set of filters to
            apply if ``path`` field referes to array elements. This is
            meant to support value matching beyond exact match. To
            perform exact match, use path_filters. When both
            path_filters and path_value_matchers are set, an implicit
            AND must be performed.
    """

    action = proto.Field(proto.STRING, number=1,)
    resource_type = proto.Field(proto.STRING, number=2,)
    resource = proto.Field(proto.STRING, number=3,)
    path = proto.Field(proto.STRING, number=4,)
    source_resource = proto.Field(proto.STRING, number=5,)
    source_path = proto.Field(proto.STRING, number=6,)
    value = proto.Field(
        proto.MESSAGE, number=7, oneof="path_value", message=struct_pb2.Value,
    )
    value_matcher = proto.Field(
        proto.MESSAGE, number=10, oneof="path_value", message="ValueMatcher",
    )
    path_filters = proto.MapField(
        proto.STRING, proto.MESSAGE, number=8, message=struct_pb2.Value,
    )
    path_value_matchers = proto.MapField(
        proto.STRING, proto.MESSAGE, number=11, message="ValueMatcher",
    )


class ValueMatcher(proto.Message):
    r"""Contains various matching options for values for a GCP
    resource field.

    Attributes:
        matches_pattern (str):
            To be used for full regex matching. The
            regular expression is using the Google RE2
            syntax
            (https://github.com/google/re2/wiki/Syntax), so
            to be used with RE2::FullMatch
    """

    matches_pattern = proto.Field(proto.STRING, number=1, oneof="match_variant",)


class CostProjection(proto.Message):
    r"""Contains metadata about how much money a recommendation can
    save or incur.

    Attributes:
        cost (google.type.money_pb2.Money):
            An approximate projection on amount saved or
            amount incurred. Negative cost units indicate
            cost savings and positive cost units indicate
            increase. See google.type.Money documentation
            for positive/negative units.
        duration (google.protobuf.duration_pb2.Duration):
            Duration for which this cost applies.
    """

    cost = proto.Field(proto.MESSAGE, number=1, message=money_pb2.Money,)
    duration = proto.Field(proto.MESSAGE, number=2, message=duration_pb2.Duration,)


class Impact(proto.Message):
    r"""Contains the impact a recommendation can have for a given
    category.

    Attributes:
        category (google.cloud.recommender_v1beta1.types.Impact.Category):
            Category that is being targeted.
        cost_projection (google.cloud.recommender_v1beta1.types.CostProjection):
            Use with CategoryType.COST
    """

    class Category(proto.Enum):
        r"""The category of the impact."""
        CATEGORY_UNSPECIFIED = 0
        COST = 1
        SECURITY = 2
        PERFORMANCE = 3
        MANAGEABILITY = 4

    category = proto.Field(proto.ENUM, number=1, enum=Category,)
    cost_projection = proto.Field(
        proto.MESSAGE, number=100, oneof="projection", message="CostProjection",
    )


class RecommendationStateInfo(proto.Message):
    r"""Information for state. Contains state and metadata.
    Attributes:
        state (google.cloud.recommender_v1beta1.types.RecommendationStateInfo.State):
            The state of the recommendation, Eg ACTIVE,
            SUCCEEDED, FAILED.
        state_metadata (Sequence[google.cloud.recommender_v1beta1.types.RecommendationStateInfo.StateMetadataEntry]):
            A map of metadata for the state, provided by
            user or automations systems.
    """

    class State(proto.Enum):
        r"""Represents Recommendation State."""
        STATE_UNSPECIFIED = 0
        ACTIVE = 1
        CLAIMED = 6
        SUCCEEDED = 3
        FAILED = 4
        DISMISSED = 5

    state = proto.Field(proto.ENUM, number=1, enum=State,)
    state_metadata = proto.MapField(proto.STRING, proto.STRING, number=2,)


__all__ = tuple(sorted(__protobuf__.manifest))
