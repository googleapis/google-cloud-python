# Copyright 2018 Google LLC
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

from google.api_core import exceptions
from google.api_core import retry
from google.auth import exceptions as auth_exceptions  # type: ignore
import requests.exceptions


_RETRYABLE_REASONS = frozenset(
    ["rateLimitExceeded", "backendError", "internalError", "badGateway"]
)

_UNSTRUCTURED_RETRYABLE_TYPES = (
    ConnectionError,
    exceptions.TooManyRequests,
    exceptions.InternalServerError,
    exceptions.BadGateway,
    exceptions.ServiceUnavailable,
    requests.exceptions.ChunkedEncodingError,
    requests.exceptions.ConnectionError,
    requests.exceptions.Timeout,
    auth_exceptions.TransportError,
)

_DEFAULT_RETRY_DEADLINE = 10.0 * 60.0  # 10 minutes

# Ambiguous errors (e.g. internalError, backendError, rateLimitExceeded) retry
# until the full `_DEFAULT_RETRY_DEADLINE`. This is because the
# `jobs.getQueryResults` REST API translates a job failure into an HTTP error.
#
# TODO(https://github.com/googleapis/python-bigquery/issues/1903): Investigate
# if we can fail early for ambiguous errors in `QueryJob.result()`'s call to
# the `jobs.getQueryResult` API.
#
# We need `_DEFAULT_JOB_DEADLINE` to be some multiple of
# `_DEFAULT_RETRY_DEADLINE` to allow for a few retries after the retry
# timeout is reached.
#
# Note: This multiple should actually be a multiple of
# (2 * _DEFAULT_RETRY_DEADLINE). After an ambiguous exception, the first
# call from `job_retry()` refreshes the job state without actually restarting
# the query. The second `job_retry()` actually restarts the query. For a more
# detailed explanation, see the comments where we set `restart_query_job = True`
# in `QueryJob.result()`'s  inner `is_job_done()` function.
_DEFAULT_JOB_DEADLINE = 2.0 * (2.0 * _DEFAULT_RETRY_DEADLINE)


def _should_retry(exc):
    """Predicate for determining when to retry.

    We retry if and only if the 'reason' is 'backendError'
    or 'rateLimitExceeded'.
    """
    if not hasattr(exc, "errors") or len(exc.errors) == 0:
        # Check for unstructured error returns, e.g. from GFE
        return isinstance(exc, _UNSTRUCTURED_RETRYABLE_TYPES)

    reason = exc.errors[0]["reason"]
    return reason in _RETRYABLE_REASONS


DEFAULT_RETRY = retry.Retry(predicate=_should_retry, deadline=_DEFAULT_RETRY_DEADLINE)
"""The default retry object.

Any method with a ``retry`` parameter will be retried automatically,
with reasonable defaults. To disable retry, pass ``retry=None``.
To modify the default retry behavior, call a ``with_XXX`` method
on ``DEFAULT_RETRY``. For example, to change the deadline to 30 seconds,
pass ``retry=bigquery.DEFAULT_RETRY.with_deadline(30)``.
"""

# Note: Take care when updating DEFAULT_TIMEOUT to anything but None. We
# briefly had a default timeout, but even setting it at more than twice the
# theoretical server-side default timeout of 2 minutes was not enough for
# complex queries. See:
# https://github.com/googleapis/python-bigquery/issues/970#issuecomment-921934647
DEFAULT_TIMEOUT = None
"""The default API timeout.

This is the time to wait per request. To adjust the total wait time, set a
deadline on the retry object.
"""

job_retry_reasons = (
    "rateLimitExceeded",
    "backendError",
    "internalError",
    "jobRateLimitExceeded",
)


def _job_should_retry(exc):
    # Sometimes we have ambiguous errors, such as 'backendError' which could
    # be due to an API problem or a job problem. For these, make sure we retry
    # our is_job_done() function.
    #
    # Note: This won't restart the job unless we know for sure it's because of
    # the job status and set restart_query_job = True in that loop. This means
    # that we might end up calling this predicate twice for the same job
    # but from different paths: (1) from jobs.getQueryResults RetryError and
    # (2) from translating the job error from the body of a jobs.get response.
    #
    # Note: If we start retrying job types other than queries where we don't
    # call the problematic getQueryResults API to check the status, we need
    # to provide a different predicate, as there shouldn't be ambiguous
    # errors in those cases.
    if isinstance(exc, exceptions.RetryError):
        exc = exc.cause

    if not hasattr(exc, "errors") or len(exc.errors) == 0:
        return False

    reason = exc.errors[0]["reason"]
    return reason in job_retry_reasons


DEFAULT_JOB_RETRY = retry.Retry(
    predicate=_job_should_retry, deadline=_DEFAULT_JOB_DEADLINE
)
"""
The default job retry object.
"""
