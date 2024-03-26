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
        "CompanyTypeEnum",
    },
)


class CompanyTypeEnum(proto.Message):
    r"""Wrapper message for
    [CompanyType][google.ads.admanager.v1.CompanyTypeEnum.CompanyType]

    """

    class CompanyType(proto.Enum):
        r"""The type of a company.

        Values:
            COMPANY_TYPE_UNSPECIFIED (0):
                No value specified
            ADVERTISER (1):
                A business entity that purchases ad
                inventory.
            HOUSE_ADVERTISER (2):
                A company representing the publisher's own
                advertiser for house ads.
            AGENCY (3):
                An organization that manages ad accounts and
                offers services, such as ad creation, placement,
                and management to advertisers.
            HOUSE_AGENCY (4):
                A company representing the publisher's own
                agency.
            AD_NETWORK (5):
                A company representing multiple advertisers
                and agencies.
            VIEWABILITY_PROVIDER (6):
                A third-party that measures creative
                viewability.
        """
        COMPANY_TYPE_UNSPECIFIED = 0
        ADVERTISER = 1
        HOUSE_ADVERTISER = 2
        AGENCY = 3
        HOUSE_AGENCY = 4
        AD_NETWORK = 5
        VIEWABILITY_PROVIDER = 6


__all__ = tuple(sorted(__protobuf__.manifest))
