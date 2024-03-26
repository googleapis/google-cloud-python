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

from google.ads.admanager_v1.types import applied_label
from google.ads.admanager_v1.types import size as gaa_size

__protobuf__ = proto.module(
    package="google.ads.admanager.v1",
    manifest={
        "CreativePlaceholder",
    },
)


class CreativePlaceholder(proto.Message):
    r"""Describes a slot that a creative is expected to fill. This is
    used in forecasting and to validate that the correct creatives
    are associated with the line item.

    Attributes:
        size (google.ads.admanager_v1.types.Size):
            Required. The size that the creative is
            expected to have.
        companion_sizes (MutableSequence[google.ads.admanager_v1.types.Size]):
            The companions that the creative is expected to have. This
            attribute can only be set if the line item it belongs to has
            an
            [EnvironmentType][google.ads.admanager.v1.EnvironmentTypeEnum.EnvironmentType]
            of VIDEO_PLAYER or
            [roadblocking_type][LineItem.roadblocking_type] of
            CREATIVE_SET.
        expected_creative_count (int):
            Expected number of creatives that will be
            uploaded corresponding to this creative
            placeholder.  This estimate is used to improve
            the accuracy of forecasting; for example, if
            label frequency capping limits the number of
            times a creative may be served.
        applied_labels (MutableSequence[google.ads.admanager_v1.types.AppliedLabel]):
            Set of labels applied directly to this
            CreativePlaceholder.
        amp_only (bool):
            Indicates if the expected creative of this
            placeholder has an AMP only variant. This is
            used to improve the accuracy of forecasting and
            has no effect on serving.
        creative_targeting_display_name (str):
            The display name of the creative targeting
            that this CreativePlaceholder represents.
    """

    size: gaa_size.Size = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gaa_size.Size,
    )
    companion_sizes: MutableSequence[gaa_size.Size] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=gaa_size.Size,
    )
    expected_creative_count: int = proto.Field(
        proto.INT32,
        number=3,
    )
    applied_labels: MutableSequence[applied_label.AppliedLabel] = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message=applied_label.AppliedLabel,
    )
    amp_only: bool = proto.Field(
        proto.BOOL,
        number=5,
    )
    creative_targeting_display_name: str = proto.Field(
        proto.STRING,
        number=6,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
