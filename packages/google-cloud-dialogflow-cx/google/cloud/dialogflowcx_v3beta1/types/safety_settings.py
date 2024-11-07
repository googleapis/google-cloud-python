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
    package="google.cloud.dialogflow.cx.v3beta1",
    manifest={
        "SafetySettings",
    },
)


class SafetySettings(proto.Message):
    r"""Settings for Generative Safety.

    Attributes:
        default_banned_phrase_match_strategy (google.cloud.dialogflowcx_v3beta1.types.SafetySettings.PhraseMatchStrategy):
            Optional. Default phrase match strategy for
            banned phrases.
        banned_phrases (MutableSequence[google.cloud.dialogflowcx_v3beta1.types.SafetySettings.Phrase]):
            Banned phrases for generated text.
    """

    class PhraseMatchStrategy(proto.Enum):
        r"""Strategy for matching phrases.

        Values:
            PHRASE_MATCH_STRATEGY_UNSPECIFIED (0):
                Unspecified, defaults to PARTIAL_MATCH.
            PARTIAL_MATCH (1):
                Text that contains the phrase as a substring
                will be matched, e.g. "foo" will match
                "afoobar".
            WORD_MATCH (2):
                Text that contains the tokenized words of the
                phrase will be matched, e.g. "foo" will match "a
                foo bar" and "foo bar", but not "foobar".
        """
        PHRASE_MATCH_STRATEGY_UNSPECIFIED = 0
        PARTIAL_MATCH = 1
        WORD_MATCH = 2

    class Phrase(proto.Message):
        r"""Text input which can be used for prompt or banned phrases.

        Attributes:
            text (str):
                Required. Text input which can be used for
                prompt or banned phrases.
            language_code (str):
                Required. Language code of the phrase.
        """

        text: str = proto.Field(
            proto.STRING,
            number=1,
        )
        language_code: str = proto.Field(
            proto.STRING,
            number=2,
        )

    default_banned_phrase_match_strategy: PhraseMatchStrategy = proto.Field(
        proto.ENUM,
        number=4,
        enum=PhraseMatchStrategy,
    )
    banned_phrases: MutableSequence[Phrase] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=Phrase,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
