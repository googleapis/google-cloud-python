# Copyright 2020 Google LLC All rights reserved.
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

"""Manages OpenTelemetry trace creation and handling"""

from contextlib import contextmanager

from google.cloud.spanner_v1 import SpannerClient
from google.cloud.spanner_v1 import gapic_version

try:
    from opentelemetry import trace
    from opentelemetry.trace.status import Status, StatusCode
    from opentelemetry.semconv.attributes.otel_attributes import (
        OTEL_SCOPE_NAME,
        OTEL_SCOPE_VERSION,
    )

    HAS_OPENTELEMETRY_INSTALLED = True
except ImportError:
    HAS_OPENTELEMETRY_INSTALLED = False

TRACER_NAME = "cloud.google.com/python/spanner"
TRACER_VERSION = gapic_version.__version__


def get_tracer(tracer_provider=None):
    """
    get_tracer is a utility to unify and simplify retrieval of the tracer, without
    leaking implementation details given that retrieving a tracer requires providing
    the full qualified library name and version.
    When the tracer_provider is set, it'll retrieve the tracer from it, otherwise
    it'll fall back to the global tracer provider and use this library's specific semantics.
    """
    if not tracer_provider:
        # Acquire the global tracer provider.
        tracer_provider = trace.get_tracer_provider()

    return tracer_provider.get_tracer(TRACER_NAME, TRACER_VERSION)


@contextmanager
def trace_call(name, session, extra_attributes=None):
    if not HAS_OPENTELEMETRY_INSTALLED or not session:
        # Empty context manager. Users will have to check if the generated value is None or a span
        yield None
        return

    tracer = get_tracer()

    # Set base attributes that we know for every trace created
    attributes = {
        "db.type": "spanner",
        "db.url": SpannerClient.DEFAULT_ENDPOINT,
        "db.instance": session._database.name,
        "net.host.name": SpannerClient.DEFAULT_ENDPOINT,
        OTEL_SCOPE_NAME: TRACER_NAME,
        OTEL_SCOPE_VERSION: TRACER_VERSION,
    }

    if extra_attributes:
        attributes.update(extra_attributes)

    with tracer.start_as_current_span(
        name, kind=trace.SpanKind.CLIENT, attributes=attributes
    ) as span:
        try:
            yield span
        except Exception as error:
            span.set_status(Status(StatusCode.ERROR, str(error)))
            span.record_exception(error)
            raise
        else:
            span.set_status(Status(StatusCode.OK))
