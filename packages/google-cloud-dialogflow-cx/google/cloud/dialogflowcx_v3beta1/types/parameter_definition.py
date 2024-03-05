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
    package="google.cloud.dialogflow.cx.v3beta1",
    manifest={
        "ParameterDefinition",
    },
)


class ParameterDefinition(proto.Message):
    r"""Defines the properties of a parameter.
    Used to define parameters used in the agent and the input /
    output parameters for each fulfillment.
    (-- Next Id: 4 --)
    (-- api-linter: core::0123::resource-annotation=disabled
    aip.dev/not-precedent: ParameterDefinition is not an exposed
    resource.     --)

    Attributes:
        name (str):
            Name of parameter.
        type_ (google.cloud.dialogflowcx_v3beta1.types.ParameterDefinition.ParameterType):
            Type of parameter.
        description (str):
            Human-readable description of the parameter.
            Limited to 300 characters.
    """

    class ParameterType(proto.Enum):
        r"""Parameter types are used for validation. These types are consistent
        with [google.protobuf.Value][].

        Values:
            PARAMETER_TYPE_UNSPECIFIED (0):
                Not specified. No validation will be
                performed.
            STRING (1):
                Represents any string value.
            NUMBER (2):
                Represents any number value.
            BOOLEAN (3):
                Represents a boolean value.
            NULL (4):
                Represents a null value.
            OBJECT (5):
                Represents any object value.
            LIST (6):
                Represents a repeated value.
        """
        PARAMETER_TYPE_UNSPECIFIED = 0
        STRING = 1
        NUMBER = 2
        BOOLEAN = 3
        NULL = 4
        OBJECT = 5
        LIST = 6

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    type_: ParameterType = proto.Field(
        proto.ENUM,
        number=2,
        enum=ParameterType,
    )
    description: str = proto.Field(
        proto.STRING,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
