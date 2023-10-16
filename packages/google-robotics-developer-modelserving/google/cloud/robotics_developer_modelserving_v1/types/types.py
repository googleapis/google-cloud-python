# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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

from google.cloud.robotics_developer_modelserving_v1.types import common

__protobuf__ = proto.module(
    package="google.robotics.developer.modelserving.v1",
    manifest={
        "ContentChunk",
        "Content",
        "Prompt",
        "Plan",
    },
)


class ContentChunk(proto.Message):
    r"""Content chunk used as model input or output.

    Attributes:
        mime_type (str):
            Optional. Mime type of the data. See
            https://www.iana.org/assignments/media-types/media-types.xhtml
            for the full list. Commonly used types that the
            models are expected to understand:

              text/plain: Generic text, e.g. user's input
            for an LLM.   jpeg: JPEG-encoded images.
        data (bytes):
            Required. Data.
    """

    mime_type: str = proto.Field(
        proto.STRING,
        number=1,
    )
    data: bytes = proto.Field(
        proto.BYTES,
        number=2,
    )


class Content(proto.Message):
    r"""Represents a multimodal data which may be streamed. It is an
    ordered sequence of chunks, where each chunk has a fixed
    modality.

    Attributes:
        chunks (MutableSequence[google.cloud.robotics_developer_modelserving_v1.types.ContentChunk]):
            Required. Data chunks.
    """

    chunks: MutableSequence["ContentChunk"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="ContentChunk",
    )


class Prompt(proto.Message):
    r"""Query prompt.

    Attributes:
        content (google.cloud.robotics_developer_modelserving_v1.types.Content):
            Optional. Multimodal query (text, images
            etc).
        extra_inputs (google.cloud.robotics_developer_modelserving_v1.types.ExtraInputs):
            Optional. Extra parameters passed to the
            model, e.g. 'temperature'.
        model_key (str):
            Required. Model key.
    """

    content: "Content" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="Content",
    )
    extra_inputs: common.ExtraInputs = proto.Field(
        proto.MESSAGE,
        number=2,
        message=common.ExtraInputs,
    )
    model_key: str = proto.Field(
        proto.STRING,
        number=3,
    )


class Plan(proto.Message):
    r"""Generated plan.

    Attributes:
        content (google.cloud.robotics_developer_modelserving_v1.types.Content):
            Resulting plan.
    """

    content: "Content" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="Content",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
