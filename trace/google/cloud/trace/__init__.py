# Copyright 2017 Google LLC
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

from __future__ import absolute_import

from pkg_resources import get_distribution

__version__ = get_distribution("google-cloud-trace").version

from google.cloud.trace.client import Client
from google.cloud.trace_v2 import types
from google.cloud.trace_v2.gapic import enums
from google.cloud.trace_v2.gapic import trace_service_client


class TraceServiceClient(trace_service_client.TraceServiceClient):
    __doc__ = trace_service_client.TraceServiceClient.__doc__
    enums = enums


__all__ = ("__version__", "enums", "types", "TraceServiceClient", "Client", "SCOPE")

SCOPE = Client.SCOPE
