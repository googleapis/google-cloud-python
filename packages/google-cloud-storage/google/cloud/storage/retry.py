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

import requests

from google.api_core import exceptions
from google.api_core import retry

import json


_RETRYABLE_TYPES = (
    exceptions.TooManyRequests,  # 429
    exceptions.InternalServerError,  # 500
    exceptions.BadGateway,  # 502
    exceptions.ServiceUnavailable,  # 503
    exceptions.GatewayTimeout,  # 504
    requests.ConnectionError,
)

# Some retriable errors don't have their own custom exception in api_core.
_ADDITIONAL_RETRYABLE_STATUS_CODES = (408,)


def _should_retry(exc):
    """Predicate for determining when to retry."""
    if isinstance(exc, _RETRYABLE_TYPES):
        return True
    elif isinstance(exc, exceptions.GoogleAPICallError):
        return exc.code in _ADDITIONAL_RETRYABLE_STATUS_CODES
    else:
        return False


DEFAULT_RETRY = retry.Retry(predicate=_should_retry)
"""The default retry object.

This retry setting will retry all _RETRYABLE_TYPES and any status codes from
_ADDITIONAL_RETRYABLE_STATUS_CODES.

To modify the default retry behavior, create a new retry object modeled after
this one by calling it a ``with_XXX`` method. For example, to create a copy of
DEFAULT_RETRY with a deadline of 30 seconds, pass
``retry=DEFAULT_RETRY.with_deadline(30)``. See google-api-core reference
(https://googleapis.dev/python/google-api-core/latest/retry.html) for details.
"""


class ConditionalRetryPolicy(object):
    """A class for use when an API call is only conditionally safe to retry.

    This class is intended for use in inspecting the API call parameters of an
    API call to verify that any flags necessary to make the API call idempotent
    (such as specifying an ``if_generation_match`` or related flag) are present.

    It can be used in place of a ``retry.Retry`` object, in which case
    ``_http.Connection.api_request`` will pass the requested api call keyword
    arguments into the ``conditional_predicate`` and return the ``retry_policy``
    if the conditions are met.

    :type retry_policy: class:`google.api_core.retry.Retry`
    :param retry_policy: A retry object defining timeouts, persistence and which
        exceptions to retry.

    :type conditional_predicate: callable
    :param conditional_predicate: A callable that accepts exactly the number of
        arguments in ``required_kwargs``, in order, and returns True if the
        arguments have sufficient data to determine that the call is safe to
        retry (idempotent).

    :type required_kwargs: list(str)
    :param required_kwargs:
        A list of keyword argument keys that will be extracted from the API call
        and passed into the ``conditional predicate`` in order.
    """

    def __init__(self, retry_policy, conditional_predicate, required_kwargs):
        self.retry_policy = retry_policy
        self.conditional_predicate = conditional_predicate
        self.required_kwargs = required_kwargs

    def get_retry_policy_if_conditions_met(self, **kwargs):
        if self.conditional_predicate(*[kwargs[key] for key in self.required_kwargs]):
            return self.retry_policy
        return None


def is_generation_specified(query_params):
    """Return True if generation or if_generation_match is specified."""
    generation = query_params.get("generation") is not None
    if_generation_match = query_params.get("ifGenerationMatch") is not None
    return generation or if_generation_match


def is_metageneration_specified(query_params):
    """Return True if if_metageneration_match is specified."""
    if_metageneration_match = query_params.get("ifMetagenerationMatch") is not None
    return if_metageneration_match


def is_etag_in_json(data):
    """Return True if an etag is contained in the JSON body.

    Indended for use on calls with relatively short JSON payloads."""
    try:
        content = json.loads(data)
        if content.get("etag"):
            return True
    # Though this method should only be called when a JSON body is expected,
    # the retry policy should be robust to unexpected payloads.
    # In Python 3 a JSONDecodeError is possible, but it is a subclass of ValueError.
    except (ValueError, TypeError):
        pass
    return False


DEFAULT_RETRY_IF_GENERATION_SPECIFIED = ConditionalRetryPolicy(
    DEFAULT_RETRY, is_generation_specified, ["query_params"]
)
DEFAULT_RETRY_IF_METAGENERATION_SPECIFIED = ConditionalRetryPolicy(
    DEFAULT_RETRY, is_metageneration_specified, ["query_params"]
)
DEFAULT_RETRY_IF_ETAG_IN_JSON = ConditionalRetryPolicy(
    DEFAULT_RETRY, is_etag_in_json, ["data"]
)
