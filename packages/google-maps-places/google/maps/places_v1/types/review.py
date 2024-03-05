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

from google.protobuf import timestamp_pb2  # type: ignore
from google.type import localized_text_pb2  # type: ignore
import proto  # type: ignore

from google.maps.places_v1.types import attribution

__protobuf__ = proto.module(
    package="google.maps.places.v1",
    manifest={
        "Review",
    },
)


class Review(proto.Message):
    r"""Information about a review of a place.

    Attributes:
        name (str):
            A reference representing this place review which may be used
            to look up this place review again (also called the API
            "resource" name: ``places/{place_id}/reviews/{review}``).
        relative_publish_time_description (str):
            A string of formatted recent time, expressing
            the review time relative to the current time in
            a form appropriate for the language and country.
        text (google.type.localized_text_pb2.LocalizedText):
            The localized text of the review.
        original_text (google.type.localized_text_pb2.LocalizedText):
            The review text in its original language.
        rating (float):
            A number between 1.0 and 5.0, also called the
            number of stars.
        author_attribution (google.maps.places_v1.types.AuthorAttribution):
            This review's author.
        publish_time (google.protobuf.timestamp_pb2.Timestamp):
            Timestamp for the review.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    relative_publish_time_description: str = proto.Field(
        proto.STRING,
        number=2,
    )
    text: localized_text_pb2.LocalizedText = proto.Field(
        proto.MESSAGE,
        number=9,
        message=localized_text_pb2.LocalizedText,
    )
    original_text: localized_text_pb2.LocalizedText = proto.Field(
        proto.MESSAGE,
        number=12,
        message=localized_text_pb2.LocalizedText,
    )
    rating: float = proto.Field(
        proto.DOUBLE,
        number=7,
    )
    author_attribution: attribution.AuthorAttribution = proto.Field(
        proto.MESSAGE,
        number=13,
        message=attribution.AuthorAttribution,
    )
    publish_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=14,
        message=timestamp_pb2.Timestamp,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
