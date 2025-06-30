# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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

from google.ads.admanager_v1.types import custom_targeting_value_enums

__protobuf__ = proto.module(
    package="google.ads.admanager.v1",
    manifest={
        "CustomTargetingValue",
    },
)


class CustomTargetingValue(proto.Message):
    r"""The ``CustomTargetingValue`` resource.

    Attributes:
        name (str):
            Identifier. The resource name of the
            ``CustomTargetingValue``. Format:
            ``networks/{network_code}/customTargetingValues/{custom_targeting_value_id}``
        custom_targeting_key (str):
            Required. Immutable. The resource name of the
            ``CustomTargetingKey``. Format:
            ``networks/{network_code}/customTargetingKeys/{custom_targeting_key_id}``
        ad_tag_name (str):
            Immutable. Name of the ``CustomTargetingValue``. Values can
            contain up to 40 characters each. You can use alphanumeric
            characters and symbols other than the following: ", ', =, !,
            +, #, \*, ~, ;, ^, (, ), <, >, [, ]. Values are not
            data-specific; all values are treated as strings. For
            example, instead of using "age>=18 AND <=34", try "18-34".
        display_name (str):
            Optional. Descriptive name for the ``CustomTargetingValue``.
        match_type (google.ads.admanager_v1.types.CustomTargetingValueMatchTypeEnum.CustomTargetingValueMatchType):
            Required. Immutable. The way in which the
            CustomTargetingValue.name strings will be
            matched.
        status (google.ads.admanager_v1.types.CustomTargetingValueStatusEnum.CustomTargetingValueStatus):
            Output only. Status of the ``CustomTargetingValue``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    custom_targeting_key: str = proto.Field(
        proto.STRING,
        number=8,
    )
    ad_tag_name: str = proto.Field(
        proto.STRING,
        number=4,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=5,
    )
    match_type: custom_targeting_value_enums.CustomTargetingValueMatchTypeEnum.CustomTargetingValueMatchType = proto.Field(
        proto.ENUM,
        number=6,
        enum=custom_targeting_value_enums.CustomTargetingValueMatchTypeEnum.CustomTargetingValueMatchType,
    )
    status: custom_targeting_value_enums.CustomTargetingValueStatusEnum.CustomTargetingValueStatus = proto.Field(
        proto.ENUM,
        number=7,
        enum=custom_targeting_value_enums.CustomTargetingValueStatusEnum.CustomTargetingValueStatus,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
