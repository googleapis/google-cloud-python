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
import proto  # type: ignore

from google.cloud.support_v2.types import actor

__protobuf__ = proto.module(
    package="google.cloud.support.v2",
    manifest={
        "Comment",
    },
)


class Comment(proto.Message):
    r"""A comment associated with a support case.

    Attributes:
        name (str):
            Output only. The resource name for the
            comment.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when this comment was
            created.
        creator (google.cloud.support_v2.types.Actor):
            Output only. The user or Google Support agent
            created this comment.
        body (str):
            The full comment body. Maximum of 12800
            characters. This can contain rich text syntax.
        plain_text_body (str):
            Output only. DEPRECATED. An automatically
            generated plain text version of body with all
            rich text syntax stripped.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    creator: actor.Actor = proto.Field(
        proto.MESSAGE,
        number=3,
        message=actor.Actor,
    )
    body: str = proto.Field(
        proto.STRING,
        number=4,
    )
    plain_text_body: str = proto.Field(
        proto.STRING,
        number=5,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
