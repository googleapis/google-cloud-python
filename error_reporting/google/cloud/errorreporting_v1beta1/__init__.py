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

from google.cloud.errorreporting_v1beta1 import types
from google.cloud.errorreporting_v1beta1.gapic import enums
from google.cloud.errorreporting_v1beta1.gapic import error_group_service_client
from google.cloud.errorreporting_v1beta1.gapic import error_stats_service_client
from google.cloud.errorreporting_v1beta1.gapic import report_errors_service_client


class ErrorGroupServiceClient(error_group_service_client.ErrorGroupServiceClient):
    __doc__ = error_group_service_client.ErrorGroupServiceClient.__doc__
    enums = enums


class ErrorStatsServiceClient(error_stats_service_client.ErrorStatsServiceClient):
    __doc__ = error_stats_service_client.ErrorStatsServiceClient.__doc__
    enums = enums


class ReportErrorsServiceClient(report_errors_service_client.ReportErrorsServiceClient):
    __doc__ = report_errors_service_client.ReportErrorsServiceClient.__doc__
    enums = enums


__all__ = (
    "enums",
    "types",
    "ErrorGroupServiceClient",
    "ErrorStatsServiceClient",
    "ReportErrorsServiceClient",
)
