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
from google.cloud.monitoring_dashboard_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.dashboards_service import (
    DashboardsServiceAsyncClient,
    DashboardsServiceClient,
)
from .types.alertchart import AlertChart
from .types.collapsible_group import CollapsibleGroup
from .types.common import Aggregation, PickTimeSeriesFilter, StatisticalTimeSeriesFilter
from .types.dashboard import Dashboard
from .types.dashboard_filter import DashboardFilter
from .types.dashboards_service import (
    CreateDashboardRequest,
    DeleteDashboardRequest,
    GetDashboardRequest,
    ListDashboardsRequest,
    ListDashboardsResponse,
    UpdateDashboardRequest,
)
from .types.error_reporting_panel import ErrorReportingPanel
from .types.incident_list import IncidentList
from .types.layouts import ColumnLayout, GridLayout, MosaicLayout, RowLayout
from .types.logs_panel import LogsPanel
from .types.metrics import (
    SparkChartType,
    Threshold,
    TimeSeriesFilter,
    TimeSeriesFilterRatio,
    TimeSeriesQuery,
)
from .types.piechart import PieChart
from .types.scorecard import Scorecard
from .types.section_header import SectionHeader
from .types.single_view_group import SingleViewGroup
from .types.table import TimeSeriesTable
from .types.table_display_options import TableDisplayOptions
from .types.text import Text
from .types.widget import Widget
from .types.xychart import ChartOptions, XyChart

__all__ = (
    "DashboardsServiceAsyncClient",
    "Aggregation",
    "AlertChart",
    "ChartOptions",
    "CollapsibleGroup",
    "ColumnLayout",
    "CreateDashboardRequest",
    "Dashboard",
    "DashboardFilter",
    "DashboardsServiceClient",
    "DeleteDashboardRequest",
    "ErrorReportingPanel",
    "GetDashboardRequest",
    "GridLayout",
    "IncidentList",
    "ListDashboardsRequest",
    "ListDashboardsResponse",
    "LogsPanel",
    "MosaicLayout",
    "PickTimeSeriesFilter",
    "PieChart",
    "RowLayout",
    "Scorecard",
    "SectionHeader",
    "SingleViewGroup",
    "SparkChartType",
    "StatisticalTimeSeriesFilter",
    "TableDisplayOptions",
    "Text",
    "Threshold",
    "TimeSeriesFilter",
    "TimeSeriesFilterRatio",
    "TimeSeriesQuery",
    "TimeSeriesTable",
    "UpdateDashboardRequest",
    "Widget",
    "XyChart",
)
