# Copyright 2020 Google LLC
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

import logging
from contextlib import contextmanager
from google.api_core.exceptions import GoogleAPICallError  # type: ignore

logger = logging.getLogger(__name__)
try:
    from opentelemetry import trace  # type: ignore
    from opentelemetry.instrumentation.utils import http_status_to_status_code  # type: ignore
    from opentelemetry.trace.status import Status  # type: ignore

    HAS_OPENTELEMETRY = True
    _warned_telemetry = True

except ImportError:
    HAS_OPENTELEMETRY = False
    _warned_telemetry = False

_default_attributes = {
    "db.system": "BigQuery"
}  # static, default values assigned to all spans


@contextmanager
def create_span(name, attributes=None, client=None, job_ref=None):
    """Creates a ContextManager for a Span to be exported to the configured exporter.
    If no configuration exists yields None.

        Args:
            name (str): Name that will be set for the span being created
            attributes (Optional[dict]):
                Additional attributes that pertain to
                the specific API call (i.e. not a default attribute)
            client (Optional[google.cloud.bigquery.client.Client]):
                Pass in a Client object to extract any attributes that may be
                relevant to it and add them to the created spans.
            job_ref (Optional[google.cloud.bigquery.job._AsyncJob])
                Pass in a _AsyncJob object to extract any attributes that may be
                relevant to it and add them to the created spans.

        Yields:
            opentelemetry.trace.Span: Yields the newly created Span.

        Raises:
            google.api_core.exceptions.GoogleAPICallError:
                Raised if a span could not be yielded or issue with call to
                OpenTelemetry.
    """
    global _warned_telemetry
    final_attributes = _get_final_span_attributes(attributes, client, job_ref)
    if not HAS_OPENTELEMETRY:
        if not _warned_telemetry:
            logger.debug(
                "This service is instrumented using OpenTelemetry. "
                "OpenTelemetry or one of its components could not be imported; "
                "please add compatible versions of opentelemetry-api and "
                "opentelemetry-instrumentation packages in order to get BigQuery "
                "Tracing data."
            )
            _warned_telemetry = True

        yield None
        return
    tracer = trace.get_tracer(__name__)

    # yield new span value
    with tracer.start_as_current_span(name=name, attributes=final_attributes) as span:
        try:
            yield span
        except GoogleAPICallError as error:
            if error.code is not None:
                span.set_status(Status(http_status_to_status_code(error.code)))
            raise


def _get_final_span_attributes(attributes=None, client=None, job_ref=None):
    final_attributes = {}
    final_attributes.update(_default_attributes.copy())
    if client:
        client_attributes = _set_client_attributes(client)
        final_attributes.update(client_attributes)
    if job_ref:
        job_attributes = _set_job_attributes(job_ref)
        final_attributes.update(job_attributes)
    if attributes:
        final_attributes.update(attributes)
    return final_attributes


def _set_client_attributes(client):
    return {"db.name": client.project, "location": client.location}


def _set_job_attributes(job_ref):
    job_attributes = {
        "db.name": job_ref.project,
        "job_id": job_ref.job_id,
        "state": job_ref.state,
    }

    job_attributes["hasErrors"] = job_ref.error_result is not None

    if job_ref.created is not None:
        job_attributes["timeCreated"] = job_ref.created.isoformat()

    if job_ref.started is not None:
        job_attributes["timeStarted"] = job_ref.started.isoformat()

    if job_ref.ended is not None:
        job_attributes["timeEnded"] = job_ref.ended.isoformat()

    if job_ref.location is not None:
        job_attributes["location"] = job_ref.location

    if job_ref.parent_job_id is not None:
        job_attributes["parent_job_id"] = job_ref.parent_job_id

    if job_ref.num_child_jobs is not None:
        job_attributes["num_child_jobs"] = job_ref.num_child_jobs

    return job_attributes
