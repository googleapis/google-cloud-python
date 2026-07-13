# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import subprocess
import sys

import pytest

SCRIPT_PYTHON_315 = """
import sys
import google.api_core.gapic_v1

# The inner gapic_v1 modules should NOT be loaded yet
HEAVY_MODULES = [
    "google.api_core.gapic_v1.client_info",
    "google.api_core.gapic_v1.config",
    "google.api_core.gapic_v1.config_async",
    "google.api_core.gapic_v1.method",
    "google.api_core.gapic_v1.method_async",
    "google.api_core.gapic_v1.routing_header",
]

for mod in HEAVY_MODULES:
    if mod in sys.modules:
        print(f"FAILED: {mod} was eagerly loaded into sys.modules")
        sys.exit(1)

# Trigger reification
import google.api_core.gapic_v1.client_info
_ = google.api_core.gapic_v1.client_info.__name__

if "google.api_core.gapic_v1.client_info" not in sys.modules:
    print("FAILED: google.api_core.gapic_v1.client_info was not lazily loaded upon access")
    sys.exit(2)

sys.exit(0)
"""

SCRIPT_PRE_315 = """
import sys
import google.api_core.gapic_v1

HEAVY_MODULES = [
    "google.api_core.gapic_v1.client_info",
    "google.api_core.gapic_v1.config",
    "google.api_core.gapic_v1.config_async",
    "google.api_core.gapic_v1.method",
    "google.api_core.gapic_v1.method_async",
    "google.api_core.gapic_v1.routing_header",
]

for mod in HEAVY_MODULES:
    if mod not in sys.modules:
        print(f"FAILED: {mod} was not eagerly loaded into sys.modules")
        sys.exit(1)

sys.exit(0)
"""


@pytest.mark.skipif(sys.version_info < (3, 15), reason="PEP 810 requires Python 3.15+")
def test_lazy_imports_on_python_315():
    result = subprocess.run(
        [sys.executable, "-c", SCRIPT_PYTHON_315], capture_output=True, text=True
    )
    assert result.returncode == 0, f"Subprocess failed: {result.stdout}"


@pytest.mark.skipif(
    sys.version_info >= (3, 15), reason="Testing fallback behavior on < 3.15"
)
def test_fallback_eager_imports_pre_315():
    result = subprocess.run(
        [sys.executable, "-c", SCRIPT_PRE_315], capture_output=True, text=True
    )
    assert result.returncode == 0, f"Subprocess failed: {result.stdout}"
