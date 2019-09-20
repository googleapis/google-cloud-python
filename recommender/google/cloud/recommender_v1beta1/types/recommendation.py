# -*- coding: utf-8 -*-
import proto  # type: ignore


from google.protobuf import duration_pb2 as gp_duration  # type: ignore
from google.protobuf import struct_pb2 as struct  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from google.type import money_pb2 as money  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.recommender.v1beta1",
    manifest={
        "Recommendation",
        "RecommendationContent",
        "OperationGroup",
        "Operation",
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

            A project recommendation is represented as
            projects/[PROJECT_NUMBER]/locations/[LOCATION]/recommenders/[RECOMMENDER_ID]/recommendations/[RECOMMENDATION_ID]
        description (str):
            Free-form human readable summary in English.
            The maximum length is 500 characters.
        recommender_subtype (str):
            Contains an identifier for a subtype of recommendations
            produced for the same recommender. Subtype is a function of
            content and impact, meaning a new subtype will be added when
            either content or primary impact category changes.

            Examples: For recommender =
            "google.iam.policy.RoleRecommender", recommender_subtype can
            be one of "REMOVE_ROLE"/"REPLACE_ROLE".
        last_refresh_time (~.timestamp.Timestamp):
            Last time this recommendation was refreshed
            by the system that created it in the first
            place.
        primary_impact (~.recommendation.Impact):
            The primary impact that this recommendation
            can have while trying to optimize for one
            category.
        additional_impact (Sequence[~.recommendation.Impact]):
            Optional set of additional impact that this
            recommendation may have when trying to optimize
            for the primary category. These may be positive
            or negative.
        content (~.recommendation.RecommendationContent):
            Content of the recommendation describing
            recommended changes to resources.
        state_info (~.recommendation.RecommendationStateInfo):
            Information for state. Contains state and
            metadata.
        etag (str):
            Fingerprint of the Recommendation. Provides
            optimistic locking when updating states.
    """
    name = proto.Field(proto.STRING, number=1)
    description = proto.Field(proto.STRING, number=2)
    recommender_subtype = proto.Field(proto.STRING, number=12)
    last_refresh_time = proto.Field(
        proto.MESSAGE, number=4, message=timestamp.Timestamp
    )
    primary_impact = proto.Field(proto.MESSAGE, number=5, message="Impact")
    additional_impact = proto.RepeatedField(proto.MESSAGE, number=6, message="Impact")
    content = proto.Field(proto.MESSAGE, number=7, message="RecommendationContent")
    state_info = proto.Field(
        proto.MESSAGE, number=10, message="RecommendationStateInfo"
    )
    etag = proto.Field(proto.STRING, number=11)


class RecommendationContent(proto.Message):
    r"""Contains what resources are changing and how they are
    changing.

    Attributes:
        operation_groups (Sequence[~.recommendation.OperationGroup]):
            Operations to one or more Google Cloud
            resources grouped in such a way that, all
            operations within one group are expected to be
            performed atomically and in an order.
    """
    operation_groups = proto.RepeatedField(
        proto.MESSAGE, number=2, message="OperationGroup"
    )


class OperationGroup(proto.Message):
    r"""Group of operations that need to be performed atomically.

    Attributes:
        operations (Sequence[~.recommendation.Operation]):
            List of operations across one or more
            resources that belong to this group. Loosely
            based on RFC6902 and should be performed in the
            order they appear.
    """
    operations = proto.RepeatedField(proto.MESSAGE, number=1, message="Operation")


class Operation(proto.Message):
    r"""Contains an operation for a resource inspired by the JSON-PATCH
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
            'test' and custom operations. This field is
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
        value (~.struct.Value):
            Value for the ``path`` field. Set if action is
            'add'/'replace'/'test'.
        path_filters (Sequence[~.recommendation.Operation.PathFiltersEntry]):
            Set of filters to apply if ``path`` refers to array elements
            or nested array elements in order to narrow down to a single
            unique element that is being tested/modified. Note that this
            is intended to be an exact match per filter. ``Example: {
            "/versions/*/name" : "it-123"
            "/versions/*/targetSize/percent": 20 }`` ``Example: {
            "/bindings/*/role": "roles/admin" "/bindings/*/condition" :
            null }`` ``Example: { "/bindings/*/role": "roles/admin"
            "/bindings/*/members/*" : ["x@google.com", "y@google.com"] }``
    """

    class PathFiltersEntry(proto.Message):
        r"""

        Attributes:
            key (str):

            value (~.struct.Value):

        """
        key = proto.Field(proto.STRING, number=1)
        value = proto.Field(proto.MESSAGE, number=2, message=struct.Value)

    action = proto.Field(proto.STRING, number=1)
    resource_type = proto.Field(proto.STRING, number=2)
    resource = proto.Field(proto.STRING, number=3)
    path = proto.Field(proto.STRING, number=4)
    source_resource = proto.Field(proto.STRING, number=5)
    source_path = proto.Field(proto.STRING, number=6)
    value = proto.Field(proto.MESSAGE, number=7, message=struct.Value)
    path_filters = proto.RepeatedField(
        proto.MESSAGE, number=8, message=PathFiltersEntry
    )


class CostProjection(proto.Message):
    r"""Contains metadata about how much money a recommendation can
    save or incur.

    Attributes:
        cost (~.money.Money):
            An approximate projection on amount saved or
            amount incurred. Negative cost units indicate
            cost savings and positive cost units indicate
            increase. See google.type.Money documentation
            for positive/negative units.
        duration (~.gp_duration.Duration):
            Duration for which this cost applies.
    """
    cost = proto.Field(proto.MESSAGE, number=1, message=money.Money)
    duration = proto.Field(proto.MESSAGE, number=2, message=gp_duration.Duration)


class Impact(proto.Message):
    r"""Contains the impact a recommendation can have for a given
    category.

    Attributes:
        category (~.recommendation.Impact.Category):
            Category that is being targeted.
        cost_projection (~.recommendation.CostProjection):
            Use with CategoryType.COST
    """

    class Category(proto.Enum):
        r"""The category of the impact."""
        CATEGORY_UNSPECIFIED = 0
        COST = 1
        SECURITY = 2
        PERFORMANCE = 3

    category = proto.Field(proto.ENUM, number=1, enum=Category)
    cost_projection = proto.Field(proto.MESSAGE, number=100, message=CostProjection)


class RecommendationStateInfo(proto.Message):
    r"""Information for state. Contains state and metadata.

    Attributes:
        state (~.recommendation.RecommendationStateInfo.State):
            The state of the recommendation, Eg ACTIVE,
            SUCCEEDED, FAILED.
        state_metadata (Sequence[~.recommendation.RecommendationStateInfo.StateMetadataEntry]):
            A map of metadata for the state, provided by
            user or automations systems.
    """

    class State(proto.Enum):
        r"""Represents Recommendation State"""
        STATE_UNSPECIFIED = 0
        ACTIVE = 1
        CLAIMED = 6
        SUCCEEDED = 3
        FAILED = 4
        DISMISSED = 5

    class StateMetadataEntry(proto.Message):
        r"""

        Attributes:
            key (str):

            value (str):

        """
        key = proto.Field(proto.STRING, number=1)
        value = proto.Field(proto.STRING, number=2)

    state = proto.Field(proto.ENUM, number=1, enum=State)
    state_metadata = proto.RepeatedField(
        proto.MESSAGE, number=2, message=StateMetadataEntry
    )


__all__ = tuple(sorted(__protobuf__.manifest))
