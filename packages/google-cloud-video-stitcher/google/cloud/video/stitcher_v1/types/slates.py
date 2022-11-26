# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from typing import MutableMapping, MutableSequence

import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.video.stitcher.v1",
    manifest={
        "Slate",
    },
)


class Slate(proto.Message):
    r"""Slate object

    Attributes:
        name (str):
            Output only. The name of the slate, in the form of
            ``projects/{project_number}/locations/{location}/slates/{id}``.
        uri (str):
            The URI to fetch the source content for the
            slate. This URI must return an MP4 video with at
            least one audio track.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    uri: str = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
