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
        "DelegationTypeEnum",
        "McmEarningsProductTypeEnum",
    },
)


class DelegationTypeEnum(proto.Message):
    r"""Wrapper for
    [DelegationType][google.ads.admanager.v1.DelegationTypeEnum.DelegationType]

    """

    class DelegationType(proto.Enum):
        r"""The delegation type of the MCM child publisher.

        Values:
            DELEGATION_TYPE_UNSPECIFIED (0):
                No value specified
            MANAGE_ACCOUNT (1):
                Indicates the parent network gets complete
                access to the child network's account.
            MANAGE_INVENTORY (2):
                Indicates a subset of the ad requests from
                the child are delegated to the parent,
                determined by the tag on the child network's web
                pages. The parent network does not have access
                to the child network, as a subset of the
                inventory could be owned and operated by the
                child network.
        """

        DELEGATION_TYPE_UNSPECIFIED = 0
        MANAGE_ACCOUNT = 1
        MANAGE_INVENTORY = 2


class McmEarningsProductTypeEnum(proto.Message):
    r"""Wrapper for
    [McmEarningsProductType][google.ads.admanager.v1.McmEarningsProductTypeEnum.McmEarningsProductType]

    """

    class McmEarningsProductType(proto.Enum):
        r"""The syndication product type of the child's earnings in MCM.

        Values:
            MCM_EARNINGS_PRODUCT_TYPE_UNSPECIFIED (0):
                No value specified
            AD_EXCHANGE_CONTENT (1):
                Indicates the child network's earnings from
                Google Ad Exchange Content.
            AD_EXCHANGE_CONTENT_HOST (2):
                Indicates the child network's earnings from
                Google Ad Exchange Content made by a host.
            AD_EXCHANGE_GAMES (3):
                Indicates the child network's earnings from
                Google Ad Exchange Games.
            AD_EXCHANGE_GAMES_HOST (4):
                Indicates the child network's earnings from
                Google Ad Exchange Games made by a host.
            AD_EXCHANGE_MOBILE_CONTENT_APP (5):
                Indicates the child network's earnings from
                Google Ad Exchange Content Applications.
            AD_EXCHANGE_MOBILE_CONTENT_APP_HOST (6):
                Indicates the child network's earnings from
                Google Ad Exchange Content Applications made by
                a host.
            AD_EXCHANGE_VIDEO (7):
                Indicates the child network's earnings from
                Google Ad Exchange Video.
            AD_EXCHANGE_VIDEO_HOST (8):
                Indicates the child network's earnings from
                Google Ad Exchange Video made by a host.
            AD_EXCHANGE_RESERVATIONS (9):
                Indicates the child network's earnings from
                Ad Exchange Reservations deals (known externally
                as Programmatic Reservations).
            AD_EXCHANGE_PREFERRED_DEALS (10):
                Indicates the child network's earnings from
                Ad Exchange Preferred deals.
            OFFERWALL (11):
                Indicates the child network's earnings from
                Monteverdi Offerwall.
            BUYER_DIRECT (12):
                Indicates the child network's earnings from
                Agency Direct.
        """

        MCM_EARNINGS_PRODUCT_TYPE_UNSPECIFIED = 0
        AD_EXCHANGE_CONTENT = 1
        AD_EXCHANGE_CONTENT_HOST = 2
        AD_EXCHANGE_GAMES = 3
        AD_EXCHANGE_GAMES_HOST = 4
        AD_EXCHANGE_MOBILE_CONTENT_APP = 5
        AD_EXCHANGE_MOBILE_CONTENT_APP_HOST = 6
        AD_EXCHANGE_VIDEO = 7
        AD_EXCHANGE_VIDEO_HOST = 8
        AD_EXCHANGE_RESERVATIONS = 9
        AD_EXCHANGE_PREFERRED_DEALS = 10
        OFFERWALL = 11
        BUYER_DIRECT = 12


__all__ = tuple(sorted(__protobuf__.manifest))
