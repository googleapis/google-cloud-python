# Copyright 2026 Google LLC
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


@pytest.fixture(autouse=True)
def clean_universe_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure ambient workstation env vars never affect unit tests."""
    monkeypatch.delenv("GOOGLE_CLOUD_UNIVERSE_DOMAIN", raising=False)
    monkeypatch.delenv("GOOGLE_API_USE_MTLS_ENDPOINT", raising=False)
