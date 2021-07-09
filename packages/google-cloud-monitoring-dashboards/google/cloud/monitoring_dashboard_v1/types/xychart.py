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

from google.cloud.monitoring_dashboard_v1.types import metrics
from google.protobuf import duration_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.monitoring.dashboard.v1", manifest={"XyChart", "ChartOptions",},
)


class XyChart(proto.Message):
    r"""A chart that displays data on a 2D (X and Y axes) plane.
    Attributes:
        data_sets (Sequence[google.cloud.monitoring_dashboard_v1.types.XyChart.DataSet]):
            Required. The data displayed in this chart.
        timeshift_duration (google.protobuf.duration_pb2.Duration):
            The duration used to display a comparison
            chart. A comparison chart simultaneously shows
            values from two similar-length time periods
            (e.g., week-over-week metrics).
            The duration must be positive, and it can only
            be applied to charts with data sets of LINE plot
            type.
        thresholds (Sequence[google.cloud.monitoring_dashboard_v1.types.Threshold]):
            Threshold lines drawn horizontally across the
            chart.
        x_axis (google.cloud.monitoring_dashboard_v1.types.XyChart.Axis):
            The properties applied to the X axis.
        y_axis (google.cloud.monitoring_dashboard_v1.types.XyChart.Axis):
            The properties applied to the Y axis.
        chart_options (google.cloud.monitoring_dashboard_v1.types.ChartOptions):
            Display options for the chart.
    """

    class DataSet(proto.Message):
        r"""Groups a time series query definition with charting options.
        Attributes:
            time_series_query (google.cloud.monitoring_dashboard_v1.types.TimeSeriesQuery):
                Required. Fields for querying time series
                data from the Stackdriver metrics API.
            plot_type (google.cloud.monitoring_dashboard_v1.types.XyChart.DataSet.PlotType):
                How this data should be plotted on the chart.
            legend_template (str):
                A template string for naming ``TimeSeries`` in the resulting
                data set. This should be a string with interpolations of the
                form ``${label_name}``, which will resolve to the label's
                value.
            min_alignment_period (google.protobuf.duration_pb2.Duration):
                Optional. The lower bound on data point frequency for this
                data set, implemented by specifying the minimum alignment
                period to use in a time series query For example, if the
                data is published once every 10 minutes, the
                ``min_alignment_period`` should be at least 10 minutes. It
                would not make sense to fetch and align data at one minute
                intervals.
        """

        class PlotType(proto.Enum):
            r"""The types of plotting strategies for data sets."""
            PLOT_TYPE_UNSPECIFIED = 0
            LINE = 1
            STACKED_AREA = 2
            STACKED_BAR = 3
            HEATMAP = 4

        time_series_query = proto.Field(
            proto.MESSAGE, number=1, message=metrics.TimeSeriesQuery,
        )
        plot_type = proto.Field(proto.ENUM, number=2, enum="XyChart.DataSet.PlotType",)
        legend_template = proto.Field(proto.STRING, number=3,)
        min_alignment_period = proto.Field(
            proto.MESSAGE, number=4, message=duration_pb2.Duration,
        )

    class Axis(proto.Message):
        r"""A chart axis.
        Attributes:
            label (str):
                The label of the axis.
            scale (google.cloud.monitoring_dashboard_v1.types.XyChart.Axis.Scale):
                The axis scale. By default, a linear scale is
                used.
        """

        class Scale(proto.Enum):
            r"""Types of scales used in axes."""
            SCALE_UNSPECIFIED = 0
            LINEAR = 1
            LOG10 = 2

        label = proto.Field(proto.STRING, number=1,)
        scale = proto.Field(proto.ENUM, number=2, enum="XyChart.Axis.Scale",)

    data_sets = proto.RepeatedField(proto.MESSAGE, number=1, message=DataSet,)
    timeshift_duration = proto.Field(
        proto.MESSAGE, number=4, message=duration_pb2.Duration,
    )
    thresholds = proto.RepeatedField(
        proto.MESSAGE, number=5, message=metrics.Threshold,
    )
    x_axis = proto.Field(proto.MESSAGE, number=6, message=Axis,)
    y_axis = proto.Field(proto.MESSAGE, number=7, message=Axis,)
    chart_options = proto.Field(proto.MESSAGE, number=8, message="ChartOptions",)


class ChartOptions(proto.Message):
    r"""Options to control visual rendering of a chart.
    Attributes:
        mode (google.cloud.monitoring_dashboard_v1.types.ChartOptions.Mode):
            The chart mode.
    """

    class Mode(proto.Enum):
        r"""Chart mode options."""
        MODE_UNSPECIFIED = 0
        COLOR = 1
        X_RAY = 2
        STATS = 3

    mode = proto.Field(proto.ENUM, number=1, enum=Mode,)


__all__ = tuple(sorted(__protobuf__.manifest))
