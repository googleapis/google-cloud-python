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

from google.ads.admanager_v1.types import network_messages

__protobuf__ = proto.module(
    package="google.ads.admanager.v1",
    manifest={
        "GetNetworkRequest",
        "ListNetworksRequest",
        "ListNetworksResponse",
    },
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


class ListNetworksRequest(proto.Message):
    r"""Request object for ``ListNetworks`` method."""


class ListNetworksResponse(proto.Message):
    r"""Response object for ``ListNetworks`` method.

    Attributes:
        networks (MutableSequence[google.ads.admanager_v1.types.Network]):
            The ``Network``\ s a user has access to.
    """

    networks: MutableSequence[network_messages.Network] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=network_messages.Network,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
