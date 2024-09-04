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

import proto  # type: ignore


__protobuf__ = proto.module(
    package='google.cloud.discoveryengine.v1beta',
    manifest={
        'IndustryVertical',
        'SolutionType',
        'SearchUseCase',
        'SearchTier',
        'SearchAddOn',
        'Interval',
        'CustomAttribute',
        'UserInfo',
        'EmbeddingConfig',
        'DoubleList',
    },
)


class IndustryVertical(proto.Enum):
    r"""The industry vertical associated with the
    [DataStore][google.cloud.discoveryengine.v1beta.DataStore].

    Values:
        INDUSTRY_VERTICAL_UNSPECIFIED (0):
            Value used when unset.
        GENERIC (1):
            The generic vertical for documents that are
            not specific to any industry vertical.
        MEDIA (2):
            The media industry vertical.
        HEALTHCARE_FHIR (7):
            The healthcare FHIR vertical.
    """
    INDUSTRY_VERTICAL_UNSPECIFIED = 0
    GENERIC = 1
    MEDIA = 2
    HEALTHCARE_FHIR = 7


class SolutionType(proto.Enum):
    r"""The type of solution.

    Values:
        SOLUTION_TYPE_UNSPECIFIED (0):
            Default value.
        SOLUTION_TYPE_RECOMMENDATION (1):
            Used for Recommendations AI.
        SOLUTION_TYPE_SEARCH (2):
            Used for Discovery Search.
        SOLUTION_TYPE_CHAT (3):
            Used for use cases related to the Generative
            AI agent.
        SOLUTION_TYPE_GENERATIVE_CHAT (4):
            Used for use cases related to the Generative Chat agent.
            It's used for Generative chat engine only, the associated
            data stores must enrolled with ``SOLUTION_TYPE_CHAT``
            solution.
    """
    SOLUTION_TYPE_UNSPECIFIED = 0
    SOLUTION_TYPE_RECOMMENDATION = 1
    SOLUTION_TYPE_SEARCH = 2
    SOLUTION_TYPE_CHAT = 3
    SOLUTION_TYPE_GENERATIVE_CHAT = 4


class SearchUseCase(proto.Enum):
    r"""Defines a further subdivision of ``SolutionType``. Specifically
    applies to
    [SOLUTION_TYPE_SEARCH][google.cloud.discoveryengine.v1beta.SolutionType.SOLUTION_TYPE_SEARCH].

    Values:
        SEARCH_USE_CASE_UNSPECIFIED (0):
            Value used when unset. Will not occur in CSS.
        SEARCH_USE_CASE_SEARCH (1):
            Search use case. Expects the traffic has a non-empty
            [query][google.cloud.discoveryengine.v1beta.SearchRequest.query].
        SEARCH_USE_CASE_BROWSE (2):
            Browse use case. Expects the traffic has an empty
            [query][google.cloud.discoveryengine.v1beta.SearchRequest.query].
    """
    SEARCH_USE_CASE_UNSPECIFIED = 0
    SEARCH_USE_CASE_SEARCH = 1
    SEARCH_USE_CASE_BROWSE = 2


class SearchTier(proto.Enum):
    r"""Tiers of search features. Different tiers might have
    different pricing. To learn more, check the pricing
    documentation.

    Values:
        SEARCH_TIER_UNSPECIFIED (0):
            Default value when the enum is unspecified.
            This is invalid to use.
        SEARCH_TIER_STANDARD (1):
            Standard tier.
        SEARCH_TIER_ENTERPRISE (2):
            Enterprise tier.
    """
    SEARCH_TIER_UNSPECIFIED = 0
    SEARCH_TIER_STANDARD = 1
    SEARCH_TIER_ENTERPRISE = 2


class SearchAddOn(proto.Enum):
    r"""Add-on that provides additional functionality for search.

    Values:
        SEARCH_ADD_ON_UNSPECIFIED (0):
            Default value when the enum is unspecified.
            This is invalid to use.
        SEARCH_ADD_ON_LLM (1):
            Large language model add-on.
    """
    SEARCH_ADD_ON_UNSPECIFIED = 0
    SEARCH_ADD_ON_LLM = 1


class Interval(proto.Message):
    r"""A floating point interval.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        minimum (float):
            Inclusive lower bound.

            This field is a member of `oneof`_ ``min``.
        exclusive_minimum (float):
            Exclusive lower bound.

            This field is a member of `oneof`_ ``min``.
        maximum (float):
            Inclusive upper bound.

            This field is a member of `oneof`_ ``max``.
        exclusive_maximum (float):
            Exclusive upper bound.

            This field is a member of `oneof`_ ``max``.
    """

    minimum: float = proto.Field(
        proto.DOUBLE,
        number=1,
        oneof='min',
    )
    exclusive_minimum: float = proto.Field(
        proto.DOUBLE,
        number=2,
        oneof='min',
    )
    maximum: float = proto.Field(
        proto.DOUBLE,
        number=3,
        oneof='max',
    )
    exclusive_maximum: float = proto.Field(
        proto.DOUBLE,
        number=4,
        oneof='max',
    )


class CustomAttribute(proto.Message):
    r"""A custom attribute that is not explicitly modeled in a resource,
    e.g. [UserEvent][google.cloud.discoveryengine.v1beta.UserEvent].

    Attributes:
        text (MutableSequence[str]):
            The textual values of this custom attribute. For example,
            ``["yellow", "green"]`` when the key is "color".

            Empty string is not allowed. Otherwise, an
            ``INVALID_ARGUMENT`` error is returned.

            Exactly one of
            [CustomAttribute.text][google.cloud.discoveryengine.v1beta.CustomAttribute.text]
            or
            [CustomAttribute.numbers][google.cloud.discoveryengine.v1beta.CustomAttribute.numbers]
            should be set. Otherwise, an ``INVALID_ARGUMENT`` error is
            returned.
        numbers (MutableSequence[float]):
            The numerical values of this custom attribute. For example,
            ``[2.3, 15.4]`` when the key is "lengths_cm".

            Exactly one of
            [CustomAttribute.text][google.cloud.discoveryengine.v1beta.CustomAttribute.text]
            or
            [CustomAttribute.numbers][google.cloud.discoveryengine.v1beta.CustomAttribute.numbers]
            should be set. Otherwise, an ``INVALID_ARGUMENT`` error is
            returned.
    """

    text: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )
    numbers: MutableSequence[float] = proto.RepeatedField(
        proto.DOUBLE,
        number=2,
    )


class UserInfo(proto.Message):
    r"""Information of an end user.

    Attributes:
        user_id (str):
            Highly recommended for logged-in users. Unique identifier
            for logged-in user, such as a user name. Don't set for
            anonymous users.

            Always use a hashed value for this ID.

            Don't set the field to the same fixed ID for different
            users. This mixes the event history of those users together,
            which results in degraded model quality.

            The field must be a UTF-8 encoded string with a length limit
            of 128 characters. Otherwise, an ``INVALID_ARGUMENT`` error
            is returned.
        user_agent (str):
            User agent as included in the HTTP header.

            The field must be a UTF-8 encoded string with a length limit
            of 1,000 characters. Otherwise, an ``INVALID_ARGUMENT``
            error is returned.

            This should not be set when using the client side event
            reporting with GTM or JavaScript tag in
            [UserEventService.CollectUserEvent][google.cloud.discoveryengine.v1beta.UserEventService.CollectUserEvent]
            or if
            [UserEvent.direct_user_request][google.cloud.discoveryengine.v1beta.UserEvent.direct_user_request]
            is set.
    """

    user_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    user_agent: str = proto.Field(
        proto.STRING,
        number=2,
    )


class EmbeddingConfig(proto.Message):
    r"""Defines embedding config, used for bring your own embeddings
    feature.

    Attributes:
        field_path (str):
            Full field path in the schema mapped as
            embedding field.
    """

    field_path: str = proto.Field(
        proto.STRING,
        number=1,
    )


class DoubleList(proto.Message):
    r"""Double list.

    Attributes:
        values (MutableSequence[float]):
            Double values.
    """

    values: MutableSequence[float] = proto.RepeatedField(
        proto.DOUBLE,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
