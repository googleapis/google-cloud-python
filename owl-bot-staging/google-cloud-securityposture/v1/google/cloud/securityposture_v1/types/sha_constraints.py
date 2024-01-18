# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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

from google.cloud.securityposture_v1.types import sha_custom_config


__protobuf__ = proto.module(
    package='google.cloud.securityposture.v1',
    manifest={
        'EnablementState',
        'SecurityHealthAnalyticsModule',
        'SecurityHealthAnalyticsCustomModule',
    },
)


class EnablementState(proto.Enum):
    r"""Possible enablement states of a service or module.

    Values:
        ENABLEMENT_STATE_UNSPECIFIED (0):
            Default value. This value is unused.
        ENABLED (1):
            State is enabled.
        DISABLED (2):
            State is disabled.
    """
    ENABLEMENT_STATE_UNSPECIFIED = 0
    ENABLED = 1
    DISABLED = 2


class SecurityHealthAnalyticsModule(proto.Message):
    r"""Message for Security Health Analytics built-in detector.

    Attributes:
        module_name (str):
            Required. The name of the module eg:
            BIGQUERY_TABLE_CMEK_DISABLED.
        module_enablement_state (google.cloud.securityposture_v1.types.EnablementState):
            The state of enablement for the module at its
            level of the resource hierarchy.
    """

    module_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    module_enablement_state: 'EnablementState' = proto.Field(
        proto.ENUM,
        number=2,
        enum='EnablementState',
    )


class SecurityHealthAnalyticsCustomModule(proto.Message):
    r"""Message for SHA Custom Module

    Attributes:
        id (str):
            Output only. Immutable. The id of the custom
            module. The id is server-generated and is not
            user settable. It will be a numeric id
            containing 1-20 digits.
        display_name (str):
            Optional. The display name of the Security
            Health Analytics custom module. This display
            name becomes the finding category for all
            findings that are returned by this custom
            module. The display name must be between 1 and
            128 characters, start with a lowercase letter,
            and contain alphanumeric characters or
            underscores only.
        config (google.cloud.securityposture_v1.types.CustomConfig):
            Required. custom module details
        module_enablement_state (google.cloud.securityposture_v1.types.EnablementState):
            The state of enablement for the module at its
            level of the resource hierarchy.
    """

    id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    config: sha_custom_config.CustomConfig = proto.Field(
        proto.MESSAGE,
        number=3,
        message=sha_custom_config.CustomConfig,
    )
    module_enablement_state: 'EnablementState' = proto.Field(
        proto.ENUM,
        number=4,
        enum='EnablementState',
    )


__all__ = tuple(sorted(__protobuf__.manifest))
