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

__lazy_modules__ = {
    f"{__name__}.client_info",
    f"{__name__}.config",
    f"{__name__}.config_async",
    f"{__name__}.method",
    f"{__name__}.method_async",
    f"{__name__}.routing_header",
}

from google.api_core.gapic_v1 import client_info
from google.api_core.gapic_v1 import config
from google.api_core.gapic_v1 import config_async
from google.api_core.gapic_v1 import method
from google.api_core.gapic_v1 import method_async
from google.api_core.gapic_v1 import routing_header

__all__ = [
    "client_info",
    "config",
    "config_async",
    "method",
    "method_async",
    "routing_header",
]
