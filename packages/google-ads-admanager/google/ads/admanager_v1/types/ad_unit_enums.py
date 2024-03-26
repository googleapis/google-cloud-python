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
    package="google.ads.admanager.v1",
    manifest={
        "AppliedAdsenseEnabledEnum",
    },
)


class AppliedAdsenseEnabledEnum(proto.Message):
    r"""Wrapper message for
    [AppliedAdsenseEnabled][google.ads.admanager.v1.AppliedAdsenseEnabledEnum.AppliedAdsenseEnabled]

    """

    class AppliedAdsenseEnabled(proto.Enum):
        r"""Specifies if serving ads from the AdSense content network is
        enabled.

        Values:
            APPLIED_ADSENSE_ENABLED_UNSPECIFIED (0):
                No adsense enabled setting applied directly;
                value will be inherited from parent or system
                default.
            TRUE (1):
                Serving ads from AdSense content network is
                enabled.
            FALSE (2):
                Serving ads from AdSense content network is
                disabled.
        """
        APPLIED_ADSENSE_ENABLED_UNSPECIFIED = 0
        TRUE = 1
        FALSE = 2


__all__ = tuple(sorted(__protobuf__.manifest))
