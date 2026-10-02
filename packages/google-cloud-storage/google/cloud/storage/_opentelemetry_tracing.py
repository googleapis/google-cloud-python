# Copyright 2024 Google LLC
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

"""Manages OpenTelemetry tracing span creation and handling. This is a PREVIEW FEATURE: Coverage and functionality may change."""

from __future__ import annotations

import logging
import os
from contextlib import contextmanager
from typing import TYPE_CHECKING, cast
from urllib.parse import urlparse

from google.api_core import (
    exceptions as api_exceptions,
)
from google.api_core import (
    retry as api_retry,
)

from google.cloud.storage import __version__
from google.cloud.storage.retry import ConditionalRetryPolicy

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator, Mapping
    from typing import Any

    from google.api_core.retry import Retry
    from opentelemetry.trace import Span

    from google.cloud.storage._types import AttributeValue
    from google.cloud.storage.client import Client


ENABLE_OTEL_TRACES_ENV_VAR = "ENABLE_GCS_PYTHON_CLIENT_OTEL_TRACES"
_DEFAULT_ENABLE_OTEL_TRACES_VALUE = False
DISABLE_BUCKET_MD_ENV_VAR = "DISABLE_GCS_PYTHON_CLIENT_OTEL_BUCKET_METADATA"


def _parse_bool_env(name: str, default: bool = False) -> bool:
    val = os.environ.get(name, None)
    if val is None:
        return default
    return str(val).strip().lower() in {"1", "true", "yes", "on"}


def _is_bucket_metadata_disabled() -> bool:
    return _parse_bool_env(DISABLE_BUCKET_MD_ENV_VAR, False)


enable_otel_traces = _parse_bool_env(
    ENABLE_OTEL_TRACES_ENV_VAR, _DEFAULT_ENABLE_OTEL_TRACES_VALUE
)
logger = logging.getLogger(__name__)


try:
    from opentelemetry import trace

    HAS_OPENTELEMETRY = True

except ImportError:
    logger.debug(
        "This service is instrumented using OpenTelemetry. "
        "OpenTelemetry or one of its components could not be imported; "
        "please add compatible versions of opentelemetry-api and "
        "opentelemetry-instrumentation packages in order to get Storage "
        "Tracing data."
    )
    HAS_OPENTELEMETRY = False

_default_attributes: dict[str, AttributeValue] = {
    "rpc.service": "CloudStorage",
    "rpc.system": "http",
    "user_agent.original": f"gcloud-python/{__version__}",
}

_cloud_trace_adoption_attrs = {
    "gcp.client.service": "storage",
    "gcp.client.version": __version__,
    "gcp.client.repo": "googleapis/python-storage",
}


@contextmanager
def create_trace_span(
    name: str,
    attributes: Mapping[str, AttributeValue] | None = None,
    client: Client | None = None,
    api_request: Mapping[str, Any] | None = None,
    retry: Retry | ConditionalRetryPolicy | None = None,
) -> Iterator[Span | None]:
    """Creates a context manager for a new span and set it as the current span
    in the configured tracer. If no configuration exists yields None."""
    if not HAS_OPENTELEMETRY or not enable_otel_traces:
        yield None
        return

    tracer = trace.get_tracer(__name__)
    final_attributes = _get_final_attributes(attributes, client, api_request, retry)
    # Yield new span.
    with tracer.start_as_current_span(
        name=name, kind=trace.SpanKind.CLIENT, attributes=final_attributes
    ) as span:
        try:
            yield span
        except api_exceptions.GoogleAPICallError as error:
            span.set_status(trace.Status(trace.StatusCode.ERROR))
            span.record_exception(error)
            raise


def _get_final_attributes(
    attributes: Mapping[str, AttributeValue] | None = None,
    client: Client | None = None,
    api_request: Mapping[str, Any] | None = None,
    retry: Retry | ConditionalRetryPolicy | None = None,
) -> dict[str, AttributeValue]:
    collected_attr: dict[str, AttributeValue] = _default_attributes.copy()
    collected_attr.update(_cloud_trace_adoption_attrs)
    if api_request:
        collected_attr.update(_set_api_request_attr(api_request, client))
    if isinstance(retry, api_retry.Retry):
        collected_attr.update(_set_retry_attr(retry))
    if isinstance(retry, ConditionalRetryPolicy):
        collected_attr.update(
            _set_retry_attr(retry.retry_policy, retry.conditional_predicate)
        )
    if attributes:
        collected_attr.update(attributes)
    final_attributes: dict[str, AttributeValue] = {
        k: v for k, v in collected_attr.items() if v is not None
    }
    return final_attributes


def _set_api_request_attr(
    request: Mapping[str, Any], client: Client | None
) -> dict[str, AttributeValue]:
    attr: dict[str, AttributeValue] = {}
    if request.get("method"):
        attr["http.request.method"] = request.get("method")
    if request.get("path"):
        full_url = cast("Client", client)._connection.build_api_url(request.get("path"))
        attr.update(_get_opentelemetry_attributes_from_url(full_url, strip_query=True))
    if "timeout" in request:
        attr["connect_timeout,read_timeout"] = str(request.get("timeout"))
    return attr


def _set_retry_attr(
    retry: Retry, conditional_predicate: Callable[..., bool] | None = None
) -> dict[str, str]:
    predicate = conditional_predicate if conditional_predicate else retry._predicate
    retry_info = f"multiplier{retry._multiplier}/deadline{retry._deadline}/max{retry._maximum}/initial{retry._initial}/predicate{predicate}"
    return {"retry": retry_info}


def _get_opentelemetry_attributes_from_url(
    url: str, strip_query: bool = True
) -> dict[str, AttributeValue]:
    """Helper to assemble OpenTelemetry span attributes from a URL."""
    u = urlparse(url)
    netloc = u.netloc
    # u.hostname is always lowercase. We parse netloc to preserve casing.
    # netloc format: [userinfo@]host[:port]
    if "@" in netloc:
        netloc = netloc.split("@", 1)[1]
    if ":" in netloc and not netloc.endswith("]"):  # Handle IPv6 literal
        netloc = netloc.split(":", 1)[0]

    attributes: dict[str, AttributeValue] = {
        "server.address": netloc,
        "server.port": u.port,
        "url.scheme": u.scheme,
        "url.path": u.path,
    }
    if not strip_query:
        attributes["url.query"] = u.query

    return attributes
