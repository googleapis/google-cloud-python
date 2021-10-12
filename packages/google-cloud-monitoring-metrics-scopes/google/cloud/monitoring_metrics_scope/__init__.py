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

from google.cloud.monitoring_metrics_scope_v1.services.metrics_scopes.client import (
    MetricsScopesClient,
)
from google.cloud.monitoring_metrics_scope_v1.services.metrics_scopes.async_client import (
    MetricsScopesAsyncClient,
)

from google.cloud.monitoring_metrics_scope_v1.types.metrics_scope import MetricsScope
from google.cloud.monitoring_metrics_scope_v1.types.metrics_scope import (
    MonitoredProject,
)
from google.cloud.monitoring_metrics_scope_v1.types.metrics_scopes import (
    CreateMonitoredProjectRequest,
)
from google.cloud.monitoring_metrics_scope_v1.types.metrics_scopes import (
    DeleteMonitoredProjectRequest,
)
from google.cloud.monitoring_metrics_scope_v1.types.metrics_scopes import (
    GetMetricsScopeRequest,
)
from google.cloud.monitoring_metrics_scope_v1.types.metrics_scopes import (
    ListMetricsScopesByMonitoredProjectRequest,
)
from google.cloud.monitoring_metrics_scope_v1.types.metrics_scopes import (
    ListMetricsScopesByMonitoredProjectResponse,
)
from google.cloud.monitoring_metrics_scope_v1.types.metrics_scopes import (
    OperationMetadata,
)

__all__ = (
    "MetricsScopesClient",
    "MetricsScopesAsyncClient",
    "MetricsScope",
    "MonitoredProject",
    "CreateMonitoredProjectRequest",
    "DeleteMonitoredProjectRequest",
    "GetMetricsScopeRequest",
    "ListMetricsScopesByMonitoredProjectRequest",
    "ListMetricsScopesByMonitoredProjectResponse",
    "OperationMetadata",
)
