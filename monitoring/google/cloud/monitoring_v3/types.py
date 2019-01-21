# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
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

from google.api import distribution_pb2
from google.api import http_pb2
from google.api import label_pb2
from google.api import metric_pb2 as api_metric_pb2
from google.api import monitored_resource_pb2
from google.cloud.monitoring_v3.proto import alert_pb2
from google.cloud.monitoring_v3.proto import alert_service_pb2
from google.cloud.monitoring_v3.proto import common_pb2
from google.cloud.monitoring_v3.proto import dropped_labels_pb2
from google.cloud.monitoring_v3.proto import group_pb2
from google.cloud.monitoring_v3.proto import group_service_pb2
from google.cloud.monitoring_v3.proto import metric_pb2 as proto_metric_pb2
from google.cloud.monitoring_v3.proto import metric_service_pb2
from google.cloud.monitoring_v3.proto import mutation_record_pb2
from google.cloud.monitoring_v3.proto import notification_pb2
from google.cloud.monitoring_v3.proto import notification_service_pb2
from google.cloud.monitoring_v3.proto import span_context_pb2
from google.cloud.monitoring_v3.proto import uptime_pb2
from google.cloud.monitoring_v3.proto import uptime_service_pb2
from google.protobuf import any_pb2
from google.protobuf import descriptor_pb2
from google.protobuf import duration_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2
from google.protobuf import struct_pb2
from google.protobuf import timestamp_pb2
from google.protobuf import wrappers_pb2
from google.rpc import status_pb2

_shared_modules = [
    distribution_pb2,
    http_pb2,
    label_pb2,
    api_metric_pb2,
    monitored_resource_pb2,
    any_pb2,
    descriptor_pb2,
    duration_pb2,
    empty_pb2,
    field_mask_pb2,
    struct_pb2,
    timestamp_pb2,
    wrappers_pb2,
    status_pb2,
]

_local_modules = [
    alert_pb2,
    alert_service_pb2,
    common_pb2,
    dropped_labels_pb2,
    group_pb2,
    group_service_pb2,
    proto_metric_pb2,
    metric_service_pb2,
    mutation_record_pb2,
    notification_pb2,
    notification_service_pb2,
    span_context_pb2,
    uptime_pb2,
    uptime_service_pb2,
]

names = []

for module in _shared_modules:
    for name, message in get_messages(module).items():
        setattr(sys.modules[__name__], name, message)
        names.append(name)
for module in _local_modules:
    for name, message in get_messages(module).items():
        message.__module__ = "google.cloud.monitoring_v3.types"
        setattr(sys.modules[__name__], name, message)
        names.append(name)

__all__ = tuple(sorted(names))
