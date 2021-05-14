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


__protobuf__ = proto.module(
    package="google.cloud.recommender.v1", manifest={"Insight", "InsightStateInfo",},
)


class Insight(proto.Message):
    r"""An insight along with the information used to derive the
    insight. The insight may have associated recomendations as well.

    Attributes:
        name (str):
            Name of the insight.
        description (str):
            Free-form human readable summary in English.
            The maximum length is 500 characters.
        target_resources (Sequence[str]):
            Fully qualified resource names that this
            insight is targeting.
        insight_subtype (str):
            Insight subtype. Insight content schema will
            be stable for a given subtype.
        content (google.protobuf.struct_pb2.Struct):
            A struct of custom fields to explain the
            insight. Example: "grantedPermissionsCount":
            "1000".
        last_refresh_time (google.protobuf.timestamp_pb2.Timestamp):
            Timestamp of the latest data used to generate
            the insight.
        observation_period (google.protobuf.duration_pb2.Duration):
            Observation period that led to the insight. The source data
            used to generate the insight ends at last_refresh_time and
            begins at (last_refresh_time - observation_period).
        state_info (google.cloud.recommender_v1.types.InsightStateInfo):
            Information state and metadata.
        category (google.cloud.recommender_v1.types.Insight.Category):
            Category being targeted by the insight.
        etag (str):
            Fingerprint of the Insight. Provides
            optimistic locking when updating states.
        associated_recommendations (Sequence[google.cloud.recommender_v1.types.Insight.RecommendationReference]):
            Recommendations derived from this insight.
    """

    class Category(proto.Enum):
        r"""Insight category."""
        CATEGORY_UNSPECIFIED = 0
        COST = 1
        SECURITY = 2
        PERFORMANCE = 3
        MANAGEABILITY = 4

    class RecommendationReference(proto.Message):
        r"""Reference to an associated recommendation.
        Attributes:
            recommendation (str):
                Recommendation resource name, e.g.
                projects/[PROJECT_NUMBER]/locations/[LOCATION]/recommenders/[RECOMMENDER_ID]/recommendations/[RECOMMENDATION_ID]
        """

        recommendation = proto.Field(proto.STRING, number=1,)

    name = proto.Field(proto.STRING, number=1,)
    description = proto.Field(proto.STRING, number=2,)
    target_resources = proto.RepeatedField(proto.STRING, number=9,)
    insight_subtype = proto.Field(proto.STRING, number=10,)
    content = proto.Field(proto.MESSAGE, number=3, message=struct_pb2.Struct,)
    last_refresh_time = proto.Field(
        proto.MESSAGE, number=4, message=timestamp_pb2.Timestamp,
    )
    observation_period = proto.Field(
        proto.MESSAGE, number=5, message=duration_pb2.Duration,
    )
    state_info = proto.Field(proto.MESSAGE, number=6, message="InsightStateInfo",)
    category = proto.Field(proto.ENUM, number=7, enum=Category,)
    etag = proto.Field(proto.STRING, number=11,)
    associated_recommendations = proto.RepeatedField(
        proto.MESSAGE, number=8, message=RecommendationReference,
    )


class InsightStateInfo(proto.Message):
    r"""Information related to insight state.
    Attributes:
        state (google.cloud.recommender_v1.types.InsightStateInfo.State):
            Insight state.
        state_metadata (Sequence[google.cloud.recommender_v1.types.InsightStateInfo.StateMetadataEntry]):
            A map of metadata for the state, provided by
            user or automations systems.
    """

    class State(proto.Enum):
        r"""Represents insight state."""
        STATE_UNSPECIFIED = 0
        ACTIVE = 1
        ACCEPTED = 2
        DISMISSED = 3

    state = proto.Field(proto.ENUM, number=1, enum=State,)
    state_metadata = proto.MapField(proto.STRING, proto.STRING, number=2,)


__all__ = tuple(sorted(__protobuf__.manifest))
