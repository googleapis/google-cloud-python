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

from google.cloud.logging_v2 import types
from google.cloud.logging_v2.gapic import config_service_v2_client
from google.cloud.logging_v2.gapic import enums
from google.cloud.logging_v2.gapic import logging_service_v2_client
from google.cloud.logging_v2.gapic import metrics_service_v2_client


class LoggingServiceV2Client(logging_service_v2_client.LoggingServiceV2Client):
    __doc__ = logging_service_v2_client.LoggingServiceV2Client.__doc__
    enums = enums


class ConfigServiceV2Client(config_service_v2_client.ConfigServiceV2Client):
    __doc__ = config_service_v2_client.ConfigServiceV2Client.__doc__
    enums = enums


class MetricsServiceV2Client(metrics_service_v2_client.MetricsServiceV2Client):
    __doc__ = metrics_service_v2_client.MetricsServiceV2Client.__doc__
    enums = enums


__all__ = (
    "enums",
    "types",
    "LoggingServiceV2Client",
    "ConfigServiceV2Client",
    "MetricsServiceV2Client",
)
