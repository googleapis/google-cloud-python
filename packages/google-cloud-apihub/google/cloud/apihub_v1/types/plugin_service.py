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

from google.cloud.apihub_v1.types import common_fields

__protobuf__ = proto.module(
    package="google.cloud.apihub.v1",
    manifest={
        "Plugin",
        "GetPluginRequest",
        "EnablePluginRequest",
        "DisablePluginRequest",
    },
)


class Plugin(proto.Message):
    r"""A plugin resource in the API Hub.

    Attributes:
        name (str):
            Identifier. The name of the plugin. Format:
            ``projects/{project}/locations/{location}/plugins/{plugin}``
        display_name (str):
            Required. The display name of the plugin. Max
            length is 50 characters (Unicode code points).
        type_ (google.cloud.apihub_v1.types.AttributeValues):
            Required. The type of the API. This maps to the following
            system defined attribute:
            ``projects/{project}/locations/{location}/attributes/system-plugin-type``
            attribute. The number of allowed values for this attribute
            will be based on the cardinality of the attribute. The same
            can be retrieved via GetAttribute API. All values should be
            from the list of allowed values defined for the attribute.
        description (str):
            Optional. The plugin description. Max length
            is 2000 characters (Unicode code points).
        state (google.cloud.apihub_v1.types.Plugin.State):
            Output only. Represents the state of the
            plugin.
    """

    class State(proto.Enum):
        r"""Possible states a plugin can have. Note that this enum may
        receive new values in the future. Consumers are advised to
        always code against the enum values expecting new states can be
        added later on.

        Values:
            STATE_UNSPECIFIED (0):
                The default value. This value is used if the
                state is omitted.
            ENABLED (1):
                The plugin is enabled.
            DISABLED (2):
                The plugin is disabled.
        """
        STATE_UNSPECIFIED = 0
        ENABLED = 1
        DISABLED = 2

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    type_: common_fields.AttributeValues = proto.Field(
        proto.MESSAGE,
        number=3,
        message=common_fields.AttributeValues,
    )
    description: str = proto.Field(
        proto.STRING,
        number=4,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=5,
        enum=State,
    )


class GetPluginRequest(proto.Message):
    r"""The [GetPlugin][google.cloud.apihub.v1.ApiHubPlugin.GetPlugin]
    method's request.

    Attributes:
        name (str):
            Required. The name of the plugin to retrieve. Format:
            ``projects/{project}/locations/{location}/plugins/{plugin}``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class EnablePluginRequest(proto.Message):
    r"""The [EnablePlugin][google.cloud.apihub.v1.ApiHubPlugin.EnablePlugin]
    method's request.

    Attributes:
        name (str):
            Required. The name of the plugin to enable. Format:
            ``projects/{project}/locations/{location}/plugins/{plugin}``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class DisablePluginRequest(proto.Message):
    r"""The
    [DisablePlugin][google.cloud.apihub.v1.ApiHubPlugin.DisablePlugin]
    method's request.

    Attributes:
        name (str):
            Required. The name of the plugin to disable. Format:
            ``projects/{project}/locations/{location}/plugins/{plugin}``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
