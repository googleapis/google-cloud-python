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

from google.maps.places_v1.types import attribution

__protobuf__ = proto.module(
    package="google.maps.places.v1",
    manifest={
        "Photo",
    },
)


class Photo(proto.Message):
    r"""Information about a photo of a place.

    Attributes:
        name (str):
            Identifier. A reference representing this place photo which
            may be used to look up this place photo again (also called
            the API "resource" name:
            ``places/{place_id}/photos/{photo}``).
        width_px (int):
            The maximum available width, in pixels.
        height_px (int):
            The maximum available height, in pixels.
        author_attributions (MutableSequence[google.maps.places_v1.types.AuthorAttribution]):
            This photo's authors.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    width_px: int = proto.Field(
        proto.INT32,
        number=2,
    )
    height_px: int = proto.Field(
        proto.INT32,
        number=3,
    )
    author_attributions: MutableSequence[
        attribution.AuthorAttribution
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message=attribution.AuthorAttribution,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
