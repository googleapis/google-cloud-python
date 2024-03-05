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
    package="google.cloud.translation.v3",
    manifest={
        "GcsInputSource",
        "FileInputSource",
        "GcsOutputDestination",
    },
)


class GcsInputSource(proto.Message):
    r"""The Google Cloud Storage location for the input content.

    Attributes:
        input_uri (str):
            Required. Source data URI. For example,
            ``gs://my_bucket/my_object``.
    """

    input_uri: str = proto.Field(
        proto.STRING,
        number=1,
    )


class FileInputSource(proto.Message):
    r"""An inlined file.

    Attributes:
        mime_type (str):
            Required. The file's mime type.
        content (bytes):
            Required. The file's byte contents.
        display_name (str):
            Required. The file's display name.
    """

    mime_type: str = proto.Field(
        proto.STRING,
        number=1,
    )
    content: bytes = proto.Field(
        proto.BYTES,
        number=2,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=3,
    )


class GcsOutputDestination(proto.Message):
    r"""The Google Cloud Storage location for the output content.

    Attributes:
        output_uri_prefix (str):
            Required. Google Cloud Storage URI to output directory. For
            example, ``gs://bucket/directory``. The requesting user must
            have write permission to the bucket. The directory will be
            created if it doesn't exist.
    """

    output_uri_prefix: str = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
