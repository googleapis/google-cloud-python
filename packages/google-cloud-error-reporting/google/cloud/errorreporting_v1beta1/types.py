# Copyright 2018 Google LLC
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

from google.api import http_pb2
from google.api import label_pb2
from google.api import monitored_resource_pb2
from google.protobuf import descriptor_pb2
from google.protobuf import duration_pb2
from google.protobuf import timestamp_pb2

from google.api_core.protobuf_helpers import get_messages
from google.cloud.errorreporting_v1beta1.proto import common_pb2
from google.cloud.errorreporting_v1beta1.proto import error_group_service_pb2
from google.cloud.errorreporting_v1beta1.proto import error_stats_service_pb2
from google.cloud.errorreporting_v1beta1.proto import report_errors_service_pb2


_shared_modules = [
    http_pb2,
    label_pb2,
    monitored_resource_pb2,
    report_errors_service_pb2,
    descriptor_pb2,
    duration_pb2,
    timestamp_pb2,
]

_local_modules = [common_pb2, error_group_service_pb2, error_stats_service_pb2]

names = []

for module in _shared_modules:
    for name, message in get_messages(module).items():
        setattr(sys.modules[__name__], name, message)
        names.append(name)

for module in _local_modules:
    for name, message in get_messages(module).items():
        message.__module__ = "google.cloud.errorreporting_v1beta1.types"
        setattr(sys.modules[__name__], name, message)
        names.append(name)

__all__ = tuple(sorted(names))
