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
    package="google.cloud.automl.v1beta1",
    manifest={
        "DoubleRange",
    },
)


class DoubleRange(proto.Message):
    r"""A range between two double numbers.

    Attributes:
        start (float):
            Start of the range, inclusive.
        end (float):
            End of the range, exclusive.
    """

    start: float = proto.Field(
        proto.DOUBLE,
        number=1,
    )
    end: float = proto.Field(
        proto.DOUBLE,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
