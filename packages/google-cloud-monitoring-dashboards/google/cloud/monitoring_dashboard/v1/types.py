# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import absolute_import
import sys

from google.api_core.protobuf_helpers import get_messages

from google.cloud.monitoring_dashboard.v1.proto import common_pb2
from google.cloud.monitoring_dashboard.v1.proto import dashboard_pb2
from google.cloud.monitoring_dashboard.v1.proto import dashboards_service_pb2
from google.cloud.monitoring_dashboard.v1.proto import layouts_pb2
from google.cloud.monitoring_dashboard.v1.proto import metrics_pb2
from google.cloud.monitoring_dashboard.v1.proto import scorecard_pb2
from google.cloud.monitoring_dashboard.v1.proto import text_pb2
from google.cloud.monitoring_dashboard.v1.proto import widget_pb2
from google.cloud.monitoring_dashboard.v1.proto import xychart_pb2
from google.protobuf import duration_pb2
from google.protobuf import empty_pb2


_shared_modules = [duration_pb2, empty_pb2]

_local_modules = [
    common_pb2,
    dashboard_pb2,
    dashboards_service_pb2,
    layouts_pb2,
    metrics_pb2,
    scorecard_pb2,
    text_pb2,
    widget_pb2,
    xychart_pb2,
]

names = []

for module in _shared_modules:  # pragma: NO COVER
    for name, message in get_messages(module).items():
        setattr(sys.modules[__name__], name, message)
        names.append(name)
for module in _local_modules:
    for name, message in get_messages(module).items():
        message.__module__ = "google.cloud.monitoring_dashboard.v1.types"
        setattr(sys.modules[__name__], name, message)
        names.append(name)


__all__ = tuple(sorted(names))
