# -*- coding: utf-8 -*-
import proto  # type: ignore


from google.cloud.recommender_v1beta1.types import recommendation


__protobuf__ = proto.module(
    package="google.cloud.recommender.v1beta1",
    manifest={
        "ListRecommendationsRequest",
        "ListRecommendationsResponse",
        "GetRecommendationRequest",
        "MarkRecommendationClaimedRequest",
        "MarkRecommendationSucceededRequest",
        "MarkRecommendationFailedRequest",
    },
)


class ListRecommendationsRequest(proto.Message):
    r"""Request for the ``ListRecommendations`` method.

    Attributes:
        parent (str):
            Required. The container resource on which to execute the
            request. Acceptable formats:

            1.

            "projects/[PROJECT_NUMBER]/locations/[LOCATION]/recommenders/[RECOMMENDER_ID]",

            LOCATION here refers to GCP Locations:
            https://cloud.google.com/about/locations/
        page_size (int):
            Optional. The maximum number of results to
            return from this request. Non-positive values
            are ignored. If not specified, the server will
            determine the number of results to return.
        page_token (str):
            Optional. If present, retrieves the next batch of results
            from the preceding call to this method. ``page_token`` must
            be the value of ``next_page_token`` from the previous
            response. The values of other method parameters must be
            identical to those in the previous call.
        filter (str):
            Filter expression to restrict the recommendations returned.
            Supported filter fields: state_info.state Eg:
            \`state_info.state:"DISMISSED" or state_info.state:"FAILED".
    """
    parent = proto.Field(proto.STRING, number=1)
    page_size = proto.Field(proto.INT32, number=2)
    page_token = proto.Field(proto.STRING, number=3)
    filter = proto.Field(proto.STRING, number=5)


class ListRecommendationsResponse(proto.Message):
    r"""Response to the ``ListRecommendations`` method.

    Attributes:
        recommendations (Sequence[~.recommendation.Recommendation]):
            The set of recommendations for the ``parent`` resource.
        next_page_token (str):
            A token that can be used to request the next
            page of results. This field is empty if there
            are no additional results.
    """
    recommendations = proto.RepeatedField(
        proto.MESSAGE, number=1, message=recommendation.Recommendation
    )
    next_page_token = proto.Field(proto.STRING, number=2)


class GetRecommendationRequest(proto.Message):
    r"""Request to the ``GetRecommendation`` method.

    Attributes:
        name (str):
            Name of the recommendation.
    """
    name = proto.Field(proto.STRING, number=1)


class MarkRecommendationClaimedRequest(proto.Message):
    r"""Request for the ``MarkRecommendationClaimed`` Method.

    Attributes:
        name (str):
            Name of the recommendation.
        state_metadata (Sequence[~.recommender_service.MarkRecommendationClaimedRequest.StateMetadataEntry]):
            State properties to include with this state. Overwrites any
            existing ``state_metadata``.
        etag (str):
            Fingerprint of the Recommendation. Provides
            optimistic locking.
    """

    class StateMetadataEntry(proto.Message):
        r"""

        Attributes:
            key (str):

            value (str):

        """
        key = proto.Field(proto.STRING, number=1)
        value = proto.Field(proto.STRING, number=2)

    name = proto.Field(proto.STRING, number=1)
    state_metadata = proto.RepeatedField(
        proto.MESSAGE, number=2, message=StateMetadataEntry
    )
    etag = proto.Field(proto.STRING, number=3)


class MarkRecommendationSucceededRequest(proto.Message):
    r"""Request for the ``MarkRecommendationSucceeded`` Method.

    Attributes:
        name (str):
            Name of the recommendation.
        state_metadata (Sequence[~.recommender_service.MarkRecommendationSucceededRequest.StateMetadataEntry]):
            State properties to include with this state. Overwrites any
            existing ``state_metadata``.
        etag (str):
            Fingerprint of the Recommendation. Provides
            optimistic locking.
    """

    class StateMetadataEntry(proto.Message):
        r"""

        Attributes:
            key (str):

            value (str):

        """
        key = proto.Field(proto.STRING, number=1)
        value = proto.Field(proto.STRING, number=2)

    name = proto.Field(proto.STRING, number=1)
    state_metadata = proto.RepeatedField(
        proto.MESSAGE, number=2, message=StateMetadataEntry
    )
    etag = proto.Field(proto.STRING, number=3)


class MarkRecommendationFailedRequest(proto.Message):
    r"""Request for the ``MarkRecommendationFailed`` Method.

    Attributes:
        name (str):
            Name of the recommendation.
        state_metadata (Sequence[~.recommender_service.MarkRecommendationFailedRequest.StateMetadataEntry]):
            State properties to include with this state. Overwrites any
            existing ``state_metadata``.
        etag (str):
            Fingerprint of the Recommendation. Provides
            optimistic locking.
    """

    class StateMetadataEntry(proto.Message):
        r"""

        Attributes:
            key (str):

            value (str):

        """
        key = proto.Field(proto.STRING, number=1)
        value = proto.Field(proto.STRING, number=2)

    name = proto.Field(proto.STRING, number=1)
    state_metadata = proto.RepeatedField(
        proto.MESSAGE, number=2, message=StateMetadataEntry
    )
    etag = proto.Field(proto.STRING, number=3)


__all__ = tuple(sorted(__protobuf__.manifest))
