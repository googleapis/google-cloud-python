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
    package="google.ads.admanager.v1",
    manifest={
        "AdReviewCenterAdStatusEnum",
    },
)


class AdReviewCenterAdStatusEnum(proto.Message):
    r"""Wrapper message for
    [AdReviewCenterAdStatus][google.ads.admanager.v1.AdReviewCenterAdStatusEnum.AdReviewCenterAdStatus]

    """

    class AdReviewCenterAdStatus(proto.Enum):
        r"""Specifies the status of an AdReviewCenterAd.

        Values:
            AD_REVIEW_CENTER_AD_STATUS_UNSPECIFIED (0):
                Not specified value
            ALLOWED (1):
                This ad has been explicitly allowed to serve.
            BLOCKED (2):
                This ad has been explicitly blocked from
                serving.
            UNREVIEWED (3):
                This ad is allowed to serve by default and
                has not been reviewed.
        """

        AD_REVIEW_CENTER_AD_STATUS_UNSPECIFIED = 0
        ALLOWED = 1
        BLOCKED = 2
        UNREVIEWED = 3


__all__ = tuple(sorted(__protobuf__.manifest))
