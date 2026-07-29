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

import warnings

from .services.dashboards_service import DashboardsServiceClient
from .types.common import Aggregation, PickTimeSeriesFilter, StatisticalTimeSeriesFilter
from .types.dashboard import Dashboard
from .types.dashboards_service import (
    CreateDashboardRequest,
    DeleteDashboardRequest,
    GetDashboardRequest,
    ListDashboardsRequest,
    ListDashboardsResponse,
    UpdateDashboardRequest,
)
from .types.layouts import ColumnLayout, GridLayout, RowLayout
from .types.metrics import (
    SparkChartType,
    Threshold,
    TimeSeriesFilter,
    TimeSeriesFilterRatio,
    TimeSeriesQuery,
)
from .types.scorecard import Scorecard
from .types.text import Text
from .types.widget import Widget
from .types.xychart import ChartOptions, XyChart

__all__ = (
    "Aggregation",
    "ChartOptions",
    "ColumnLayout",
    "CreateDashboardRequest",
    "Dashboard",
    "DeleteDashboardRequest",
    "GetDashboardRequest",
    "GridLayout",
    "ListDashboardsRequest",
    "ListDashboardsResponse",
    "PickTimeSeriesFilter",
    "RowLayout",
    "Scorecard",
    "SparkChartType",
    "StatisticalTimeSeriesFilter",
    "Text",
    "Threshold",
    "TimeSeriesFilter",
    "TimeSeriesFilterRatio",
    "TimeSeriesQuery",
    "UpdateDashboardRequest",
    "Widget",
    "XyChart",
    "DashboardsServiceClient",
)

import_warning_message = (
    "The client in the `google.monitoring.dashboard` namespace is no longer updated. "
    "Please use the client in namespace `google.cloud.monitoring_dashboard` instead. "
    "In a future release, importing code from the `google.monitoring.dashboard` namespace "
    "may result in a RuntimeError. If you need to continue to use `google.monitoring.dashboard` "
    "after this date, please pin to a specific version of 'google-cloud-monitoring-dashboards'. "
    "If you have questions, please file an issue: "
    "https://github.com/googleapis/python-monitoring-dashboards/issues."
)

warnings.warn(import_warning_message, ImportWarning)
