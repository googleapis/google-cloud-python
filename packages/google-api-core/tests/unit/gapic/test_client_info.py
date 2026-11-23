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

import pytest

try:
    import grpc  # noqa: F401
except ImportError:
    pytest.skip("No GRPC", allow_module_level=True)


from google.api_core.gapic_v1 import client_info


def test_to_grpc_metadata():
    info = client_info.ClientInfo()

    metadata = info.to_grpc_metadata()

    assert metadata == (client_info.METRICS_METADATA_KEY, info.to_user_agent())


def test_to_grpc_metadata_with_detected_agent(monkeypatch):
    monkeypatch.setenv("GEMINI_CLI", "1")
    info = client_info.ClientInfo(
        python_version="3.11.0",
        grpc_version="1.60.0",
        api_core_version="2.19.0",
        gapic_version="2.14.0",
    )

    key, value = info.to_grpc_metadata()

    assert key == "x-goog-api-client"
    assert (
        value == "gl-python/3.11.0 grpc/1.60.0 gax/2.19.0 gapic/2.14.0 agent/gemini_cli"
    )
