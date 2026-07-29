# Copyright 2025 Google LLC All rights reserved.
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

import os

import pytest

from google.cloud.spanner_v1.metrics.spanner_metrics_tracer_factory import (
    SpannerMetricsTracerFactory,
)

# Disable builtin metrics to avoid background thread noise and 401 errors in unit tests
os.environ["SPANNER_DISABLE_BUILTIN_METRICS"] = "true"


@pytest.fixture(autouse=True)
def reset_metrics_singletons(monkeypatch):
    # Reset singletons and env var before test to avoid state pollution
    monkeypatch.setenv("SPANNER_DISABLE_BUILTIN_METRICS", "true")
    SpannerMetricsTracerFactory._metrics_tracer_factory = None
    SpannerMetricsTracerFactory._current_metrics_tracer_ctx.set(None)
    yield
    # Reset singletons after test to ensure no leakage
    SpannerMetricsTracerFactory._metrics_tracer_factory = None
    SpannerMetricsTracerFactory._current_metrics_tracer_ctx.set(None)
