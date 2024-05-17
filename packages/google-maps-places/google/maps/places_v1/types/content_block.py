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

from google.type import localized_text_pb2  # type: ignore
import proto  # type: ignore

from google.maps.places_v1.types import reference

__protobuf__ = proto.module(
    package="google.maps.places.v1",
    manifest={
        "ContentBlock",
    },
)


class ContentBlock(proto.Message):
    r"""A block of content that can be served individually.

    Attributes:
        topic (str):
            The topic of the content, for example
            "overview" or "restaurant".
        content (google.type.localized_text_pb2.LocalizedText):
            Content related to the topic.
        references (google.maps.places_v1.types.References):
            Experimental: See
            https://developers.google.com/maps/documentation/places/web-service/experimental/places-generative
            for more details.

            References that are related to this block of
            content.
    """

    topic: str = proto.Field(
        proto.STRING,
        number=1,
    )
    content: localized_text_pb2.LocalizedText = proto.Field(
        proto.MESSAGE,
        number=2,
        message=localized_text_pb2.LocalizedText,
    )
    references: reference.References = proto.Field(
        proto.MESSAGE,
        number=3,
        message=reference.References,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
