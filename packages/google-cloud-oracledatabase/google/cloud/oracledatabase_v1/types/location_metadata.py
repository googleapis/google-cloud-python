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
    package="google.cloud.oracledatabase.v1",
    manifest={
        "LocationMetadata",
    },
)


class LocationMetadata(proto.Message):
    r"""Metadata for a given [Location][google.cloud.location.Location].

    Attributes:
        gcp_oracle_zones (MutableSequence[str]):
            Output only. Google Cloud Platform Oracle
            zones in a location.
    """

    gcp_oracle_zones: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
