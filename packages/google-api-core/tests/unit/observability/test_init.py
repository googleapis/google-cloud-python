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

"""Tests for google.api_core.observability.__init__."""

import importlib
import sys


def test_init_exports():
    import google.api_core.observability

    # Check if dependencies are available
    try:
        import grpc  # noqa: F401
        import opentelemetry.trace  # noqa: F401

        has_deps = True
    except ImportError:
        has_deps = False

    if has_deps:
        assert "OtelUnaryClientInterceptor" in google.api_core.observability.__all__
    else:
        assert google.api_core.observability.__all__ == []


def test_init_import_error_forced(monkeypatch):
    """Verifies behavior when tracing module fails to import, even if deps are present."""
    import google.api_core.observability

    # Poison the tracing module
    monkeypatch.setitem(sys.modules, "google.api_core.observability.tracing", None)

    # Reload observability, it should fail to import tracing and trigger except block
    importlib.reload(google.api_core.observability)

    assert google.api_core.observability.__all__ == []

    # Clean up
    monkeypatch.undo()
    importlib.reload(google.api_core.observability)
