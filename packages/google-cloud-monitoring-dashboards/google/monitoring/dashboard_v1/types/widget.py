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


from google.monitoring.dashboard_v1.types import scorecard as gmd_scorecard
from google.monitoring.dashboard_v1.types import text as gmd_text
from google.monitoring.dashboard_v1.types import xychart
from google.protobuf import empty_pb2 as empty  # type: ignore


__protobuf__ = proto.module(
    package="google.monitoring.dashboard.v1", manifest={"Widget",},
)


class Widget(proto.Message):
    r"""Widget contains a single dashboard component and
    configuration of how to present the component in the dashboard.

    Attributes:
        title (str):
            Optional. The title of the widget.
        xy_chart (~.xychart.XyChart):
            A chart of time series data.
        scorecard (~.gmd_scorecard.Scorecard):
            A scorecard summarizing time series data.
        text (~.gmd_text.Text):
            A raw string or markdown displaying textual
            content.
        blank (~.empty.Empty):
            A blank space.
    """

    title = proto.Field(proto.STRING, number=1)

    xy_chart = proto.Field(
        proto.MESSAGE, number=2, oneof="content", message=xychart.XyChart,
    )

    scorecard = proto.Field(
        proto.MESSAGE, number=3, oneof="content", message=gmd_scorecard.Scorecard,
    )

    text = proto.Field(proto.MESSAGE, number=4, oneof="content", message=gmd_text.Text,)

    blank = proto.Field(proto.MESSAGE, number=5, oneof="content", message=empty.Empty,)


__all__ = tuple(sorted(__protobuf__.manifest))
