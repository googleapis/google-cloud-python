# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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

from google.cloud.monitoring_dashboard_v1.types import alertchart
from google.cloud.monitoring_dashboard_v1.types import (
    collapsible_group as gmd_collapsible_group,
)
from google.cloud.monitoring_dashboard_v1.types import logs_panel as gmd_logs_panel
from google.cloud.monitoring_dashboard_v1.types import scorecard as gmd_scorecard
from google.cloud.monitoring_dashboard_v1.types import table
from google.cloud.monitoring_dashboard_v1.types import text as gmd_text
from google.cloud.monitoring_dashboard_v1.types import xychart
from google.protobuf import empty_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.monitoring.dashboard.v1",
    manifest={
        "Widget",
    },
)


class Widget(proto.Message):
    r"""Widget contains a single dashboard component and
    configuration of how to present the component in the dashboard.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        title (str):
            Optional. The title of the widget.
        xy_chart (google.cloud.monitoring_dashboard_v1.types.XyChart):
            A chart of time series data.

            This field is a member of `oneof`_ ``content``.
        scorecard (google.cloud.monitoring_dashboard_v1.types.Scorecard):
            A scorecard summarizing time series data.

            This field is a member of `oneof`_ ``content``.
        text (google.cloud.monitoring_dashboard_v1.types.Text):
            A raw string or markdown displaying textual
            content.

            This field is a member of `oneof`_ ``content``.
        blank (google.protobuf.empty_pb2.Empty):
            A blank space.

            This field is a member of `oneof`_ ``content``.
        alert_chart (google.cloud.monitoring_dashboard_v1.types.AlertChart):
            A chart of alert policy data.

            This field is a member of `oneof`_ ``content``.
        time_series_table (google.cloud.monitoring_dashboard_v1.types.TimeSeriesTable):
            A widget that displays time series data in a
            tabular format.

            This field is a member of `oneof`_ ``content``.
        collapsible_group (google.cloud.monitoring_dashboard_v1.types.CollapsibleGroup):
            A widget that groups the other widgets. All
            widgets that are within the area spanned by the
            grouping widget are considered member widgets.

            This field is a member of `oneof`_ ``content``.
        logs_panel (google.cloud.monitoring_dashboard_v1.types.LogsPanel):
            A widget that shows a stream of logs.

            This field is a member of `oneof`_ ``content``.
    """

    title = proto.Field(
        proto.STRING,
        number=1,
    )
    xy_chart = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="content",
        message=xychart.XyChart,
    )
    scorecard = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="content",
        message=gmd_scorecard.Scorecard,
    )
    text = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="content",
        message=gmd_text.Text,
    )
    blank = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="content",
        message=empty_pb2.Empty,
    )
    alert_chart = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="content",
        message=alertchart.AlertChart,
    )
    time_series_table = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof="content",
        message=table.TimeSeriesTable,
    )
    collapsible_group = proto.Field(
        proto.MESSAGE,
        number=9,
        oneof="content",
        message=gmd_collapsible_group.CollapsibleGroup,
    )
    logs_panel = proto.Field(
        proto.MESSAGE,
        number=10,
        oneof="content",
        message=gmd_logs_panel.LogsPanel,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
