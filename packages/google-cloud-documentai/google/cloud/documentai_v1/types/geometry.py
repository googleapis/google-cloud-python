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

__protobuf__ = proto.module(
    package="google.cloud.documentai.v1",
    manifest={
        "Vertex",
        "NormalizedVertex",
        "BoundingPoly",
    },
)


class Vertex(proto.Message):
    r"""A vertex represents a 2D point in the image.
    NOTE: the vertex coordinates are in the same scale as the
    original image.

    Attributes:
        x (int):
            X coordinate.
        y (int):
            Y coordinate (starts from the top of the
            image).
    """

    x: int = proto.Field(
        proto.INT32,
        number=1,
    )
    y: int = proto.Field(
        proto.INT32,
        number=2,
    )


class NormalizedVertex(proto.Message):
    r"""A vertex represents a 2D point in the image.
    NOTE: the normalized vertex coordinates are relative to the
    original image and range from 0 to 1.

    Attributes:
        x (float):
            X coordinate.
        y (float):
            Y coordinate (starts from the top of the
            image).
    """

    x: float = proto.Field(
        proto.FLOAT,
        number=1,
    )
    y: float = proto.Field(
        proto.FLOAT,
        number=2,
    )


class BoundingPoly(proto.Message):
    r"""A bounding polygon for the detected image annotation.

    Attributes:
        vertices (MutableSequence[google.cloud.documentai_v1.types.Vertex]):
            The bounding polygon vertices.
        normalized_vertices (MutableSequence[google.cloud.documentai_v1.types.NormalizedVertex]):
            The bounding polygon normalized vertices.
    """

    vertices: MutableSequence["Vertex"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Vertex",
    )
    normalized_vertices: MutableSequence["NormalizedVertex"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="NormalizedVertex",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
