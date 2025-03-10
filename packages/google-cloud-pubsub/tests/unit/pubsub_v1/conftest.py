# Copyright 2021 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import pytest

from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry import trace
import google.auth.credentials


@pytest.fixture
def creds():
    """
    Provide test creds to unit tests so that they can run without
    GOOGLE_APPLICATION_CREDENTIALS set.
    """
    yield google.auth.credentials.AnonymousCredentials()


@pytest.fixture(scope="session", autouse=True)
def set_trace_provider():
    provider = TracerProvider()
    trace.set_tracer_provider(provider)


@pytest.fixture(scope="function")
def span_exporter():
    exporter = InMemorySpanExporter()
    processor = SimpleSpanProcessor(exporter)
    provider = trace.get_tracer_provider()
    provider.add_span_processor(processor)
    yield exporter


@pytest.fixture()
def modify_google_logger_propagation():
    """
    Allow propagation of logs to the root logger for tests
    that depend on the caplog fixture. Restore the default
    propagation setting after the test finishes.
    """
    logger = logging.getLogger("google")
    original_propagate = logger.propagate
    logger.propagate = True
    try:
        yield
    finally:
        logger.propagate = original_propagate
