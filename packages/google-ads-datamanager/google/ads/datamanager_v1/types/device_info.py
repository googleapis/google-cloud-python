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
    package="google.ads.datamanager.v1",
    manifest={
        "DeviceInfo",
    },
)


class DeviceInfo(proto.Message):
    r"""Information about the device being used (if any) when the
    event happened.

    Attributes:
        user_agent (str):
            Optional. The user-agent string of the device
            for the given context.
        ip_address (str):
            Optional. The IP address of the device for the given
            context.

            **Note:** Google Ads does not support IP address matching
            for end users in the European Economic Area (EEA), United
            Kingdom (UK), or Switzerland (CH). Add logic to
            conditionally exclude sharing IP addresses from users from
            these regions and ensure that you provide users with clear
            and comprehensive information about the data you collect on
            your sites, apps, and other properties and get consent where
            required by law or any applicable Google policies. See the
            `About offline conversion
            imports <https://support.google.com/google-ads/answer/2998031>`__
            page for more details.
    """

    user_agent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    ip_address: str = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
