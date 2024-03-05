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
    package="google.cloud.discoveryengine.v1",
    manifest={
        "SuggestionDenyListEntry",
    },
)


class SuggestionDenyListEntry(proto.Message):
    r"""Suggestion deny list entry identifying the phrase to block
    from suggestions and the applied operation for the phrase.

    Attributes:
        block_phrase (str):
            Required. Phrase to block from suggestions
            served. Can be maximum 125 characters.
        match_operator (google.cloud.discoveryengine_v1.types.SuggestionDenyListEntry.MatchOperator):
            Required. The match operator to apply for
            this phrase. Whether to block the exact phrase,
            or block any suggestions containing this phrase.
    """

    class MatchOperator(proto.Enum):
        r"""Operator for matching with the generated suggestions.

        Values:
            MATCH_OPERATOR_UNSPECIFIED (0):
                Default value. Should not be used
            EXACT_MATCH (1):
                If the suggestion is an exact match to the block_phrase,
                then block it.
            CONTAINS (2):
                If the suggestion contains the block_phrase, then block it.
        """
        MATCH_OPERATOR_UNSPECIFIED = 0
        EXACT_MATCH = 1
        CONTAINS = 2

    block_phrase: str = proto.Field(
        proto.STRING,
        number=1,
    )
    match_operator: MatchOperator = proto.Field(
        proto.ENUM,
        number=2,
        enum=MatchOperator,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
