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

from .services.metrics_scopes import MetricsScopesClient
from .services.metrics_scopes import MetricsScopesAsyncClient

from .types.metrics_scope import MetricsScope
from .types.metrics_scope import MonitoredProject
from .types.metrics_scopes import CreateMonitoredProjectRequest
from .types.metrics_scopes import DeleteMonitoredProjectRequest
from .types.metrics_scopes import GetMetricsScopeRequest
from .types.metrics_scopes import ListMetricsScopesByMonitoredProjectRequest
from .types.metrics_scopes import ListMetricsScopesByMonitoredProjectResponse
from .types.metrics_scopes import OperationMetadata

__all__ = (
    "MetricsScopesAsyncClient",
    "CreateMonitoredProjectRequest",
    "DeleteMonitoredProjectRequest",
    "GetMetricsScopeRequest",
    "ListMetricsScopesByMonitoredProjectRequest",
    "ListMetricsScopesByMonitoredProjectResponse",
    "MetricsScope",
    "MetricsScopesClient",
    "MonitoredProject",
    "OperationMetadata",
)
