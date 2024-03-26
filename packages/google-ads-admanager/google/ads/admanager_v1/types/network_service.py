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
        "Network",
        "GetNetworkRequest",
    },
)


class Network(proto.Message):
    r"""The Network resource.

    Attributes:
        name (str):
            Identifier. The resource name of the Network. Format:
            networks/{network_code}
        display_name (str):
            Optional. Display name for Network.
        network_code (str):
            Output only. Network Code.
        property_code (str):
            Output only. Property code.
        time_zone (str):
            Output only. Time zone associated with the
            delivery of orders and reporting.
        currency_code (str):
            Output only. Primary currency code, in
            ISO-4217 format.
        secondary_currency_codes (MutableSequence[str]):
            Optional. Currency codes that can be used as
            an alternative to the primary currency code for
            trafficking Line Items.
        effective_root_ad_unit (str):
            Output only. Top most `Ad
            Unit <google.ads.admanager.v1.AdUnit>`__ to which descendant
            Ad Units can be added. Format:
            networks/{network_code}/adUnit/{ad_unit_id}
        test_network (bool):
            Output only. Whether this is a test network.
        network_id (int):
            Output only. Network ID.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    network_code: str = proto.Field(
        proto.STRING,
        number=3,
    )
    property_code: str = proto.Field(
        proto.STRING,
        number=4,
    )
    time_zone: str = proto.Field(
        proto.STRING,
        number=5,
    )
    currency_code: str = proto.Field(
        proto.STRING,
        number=6,
    )
    secondary_currency_codes: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=7,
    )
    effective_root_ad_unit: str = proto.Field(
        proto.STRING,
        number=8,
    )
    test_network: bool = proto.Field(
        proto.BOOL,
        number=10,
    )
    network_id: int = proto.Field(
        proto.INT64,
        number=11,
    )


class GetNetworkRequest(proto.Message):
    r"""Request to get Network

    Attributes:
        name (str):
            Required. Resource name of Network. Format:
            networks/{network_code}
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
