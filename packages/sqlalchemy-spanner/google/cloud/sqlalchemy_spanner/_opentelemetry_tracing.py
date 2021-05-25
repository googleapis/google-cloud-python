# Copyright 2021 Google LLC All rights reserved.
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

from google.api_core.exceptions import GoogleAPICallError
from google.cloud.spanner_v1 import SpannerClient
from google.cloud.spanner_dbapi.exceptions import IntegrityError
from google.cloud.spanner_dbapi.exceptions import InterfaceError
from google.cloud.spanner_dbapi.exceptions import OperationalError
from google.cloud.spanner_dbapi.exceptions import ProgrammingError

try:
    from opentelemetry import trace
    from opentelemetry.trace.status import Status, StatusCanonicalCode
    from opentelemetry.instrumentation.utils import http_status_to_canonical_code

    HAS_OPENTELEMETRY_INSTALLED = True
except ImportError:
    HAS_OPENTELEMETRY_INSTALLED = False


@contextmanager
def trace_call(name, extra_attributes=None):
    if not HAS_OPENTELEMETRY_INSTALLED:
        # Empty context manager. Users will have to check if the generated value
        # is None or a span
        yield None
        return

    tracer = trace.get_tracer(__name__)
    # Set base attributes that we know for every trace created
    attributes = {
        "db.type": "spanner",
        "db.url": SpannerClient.DEFAULT_ENDPOINT,
        "net.host.name": SpannerClient.DEFAULT_ENDPOINT,
    }

    if extra_attributes:
        attributes.update(extra_attributes)

    with tracer.start_as_current_span(
        name, kind=trace.SpanKind.CLIENT, attributes=attributes
    ) as span:
        try:
            yield span
        except (ValueError, InterfaceError) as e:
            span.set_status(Status(StatusCanonicalCode.UNKNOWN, e.args[0]))
        except GoogleAPICallError as error:
            if error.code is not None:
                span.set_status(Status(http_status_to_canonical_code(error.code)))
            elif error.grpc_status_code is not None:
                span.set_status(
                    # OpenTelemetry's StatusCanonicalCode maps 1-1 with grpc status
                    # codes
                    Status(StatusCanonicalCode(error.grpc_status_code.value[0]))
                )
            raise
        except (IntegrityError, ProgrammingError, OperationalError) as e:
            span.set_status(
                Status(http_status_to_canonical_code(e.args[0].code), e.args[0].message)
            )
