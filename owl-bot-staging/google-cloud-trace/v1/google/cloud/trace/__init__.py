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
from google.cloud.trace import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.trace_v1.services.trace_service.client import TraceServiceClient
from google.cloud.trace_v1.services.trace_service.async_client import TraceServiceAsyncClient

from google.cloud.trace_v1.types.trace import GetTraceRequest
from google.cloud.trace_v1.types.trace import ListTracesRequest
from google.cloud.trace_v1.types.trace import ListTracesResponse
from google.cloud.trace_v1.types.trace import PatchTracesRequest
from google.cloud.trace_v1.types.trace import Trace
from google.cloud.trace_v1.types.trace import Traces
from google.cloud.trace_v1.types.trace import TraceSpan

__all__ = ('TraceServiceClient',
    'TraceServiceAsyncClient',
    'GetTraceRequest',
    'ListTracesRequest',
    'ListTracesResponse',
    'PatchTracesRequest',
    'Trace',
    'Traces',
    'TraceSpan',
)
