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

from google.cloud.ces_v1.types import schema

__protobuf__ = proto.module(
    package="google.cloud.ces.v1",
    manifest={
        "WidgetTool",
    },
)


class WidgetTool(proto.Message):
    r"""Represents a widget tool that the agent can invoke. When the
    tool is chosen by the agent, agent will return the widget to the
    client. The client is responsible for processing the widget and
    generating the next user query to continue the interaction with
    the agent.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        parameters (google.cloud.ces_v1.types.Schema):
            Optional. The input parameters of the widget
            tool.

            This field is a member of `oneof`_ ``input``.
        name (str):
            Required. The display name of the widget
            tool.
        description (str):
            Optional. The description of the widget tool.
        widget_type (google.cloud.ces_v1.types.WidgetTool.WidgetType):
            Optional. The type of the widget tool. If not
            specified, the default type will be CUSTOMIZED.
    """

    class WidgetType(proto.Enum):
        r"""All available widget types.
        New values may be added to this enum in the future.

        Values:
            WIDGET_TYPE_UNSPECIFIED (0):
                Unspecified widget type.
            CUSTOM (1):
                Custom widget type.
            PRODUCT_CAROUSEL (2):
                Product carousel widget.
            PRODUCT_DETAILS (3):
                Product details widget.
            QUICK_ACTIONS (4):
                Quick actions widget.
            PRODUCT_COMPARISON (5):
                Product comparison widget.
            ADVANCED_PRODUCT_DETAILS (6):
                Advanced product details widget.
            SHORT_FORM (7):
                Short form widget.
            OVERALL_SATISFACTION (8):
                Overall satisfaction widget.
            ORDER_SUMMARY (9):
                Order summary widget.
            APPOINTMENT_DETAILS (10):
                Appointment details widget.
        """

        WIDGET_TYPE_UNSPECIFIED = 0
        CUSTOM = 1
        PRODUCT_CAROUSEL = 2
        PRODUCT_DETAILS = 3
        QUICK_ACTIONS = 4
        PRODUCT_COMPARISON = 5
        ADVANCED_PRODUCT_DETAILS = 6
        SHORT_FORM = 7
        OVERALL_SATISFACTION = 8
        ORDER_SUMMARY = 9
        APPOINTMENT_DETAILS = 10

    parameters: schema.Schema = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="input",
        message=schema.Schema,
    )
    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    description: str = proto.Field(
        proto.STRING,
        number=2,
    )
    widget_type: WidgetType = proto.Field(
        proto.ENUM,
        number=3,
        enum=WidgetType,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
