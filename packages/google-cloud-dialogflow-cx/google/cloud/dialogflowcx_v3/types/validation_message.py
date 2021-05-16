# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
import proto  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.dialogflow.cx.v3",
    manifest={"ValidationMessage", "ResourceName",},
)


class ValidationMessage(proto.Message):
    r"""Agent/flow validation message.
    Attributes:
        resource_type (google.cloud.dialogflowcx_v3.types.ValidationMessage.ResourceType):
            The type of the resources where the message
            is found.
        resources (Sequence[str]):
            The names of the resources where the message
            is found.
        resource_names (Sequence[google.cloud.dialogflowcx_v3.types.ResourceName]):
            The resource names of the resources where the
            message is found.
        severity (google.cloud.dialogflowcx_v3.types.ValidationMessage.Severity):
            Indicates the severity of the message.
        detail (str):
            The message detail.
    """

    class ResourceType(proto.Enum):
        r"""Resource types."""
        RESOURCE_TYPE_UNSPECIFIED = 0
        AGENT = 1
        INTENT = 2
        INTENT_TRAINING_PHRASE = 8
        INTENT_PARAMETER = 9
        INTENTS = 10
        INTENT_TRAINING_PHRASES = 11
        ENTITY_TYPE = 3
        ENTITY_TYPES = 12
        WEBHOOK = 4
        FLOW = 5
        PAGE = 6
        PAGES = 13
        TRANSITION_ROUTE_GROUP = 7

    class Severity(proto.Enum):
        r"""Severity level."""
        SEVERITY_UNSPECIFIED = 0
        INFO = 1
        WARNING = 2
        ERROR = 3

    resource_type = proto.Field(proto.ENUM, number=1, enum=ResourceType,)
    resources = proto.RepeatedField(proto.STRING, number=2,)
    resource_names = proto.RepeatedField(
        proto.MESSAGE, number=6, message="ResourceName",
    )
    severity = proto.Field(proto.ENUM, number=3, enum=Severity,)
    detail = proto.Field(proto.STRING, number=4,)


class ResourceName(proto.Message):
    r"""Resource name and display name.
    Attributes:
        name (str):
            Name.
        display_name (str):
            Display name.
    """

    name = proto.Field(proto.STRING, number=1,)
    display_name = proto.Field(proto.STRING, number=2,)


__all__ = tuple(sorted(__protobuf__.manifest))
