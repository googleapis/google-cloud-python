# Copyright 2019 Google LLC
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


_RETRYABLE_REASONS = frozenset(["DEADLINE_EXCEEDED", "UNAVAILABLE"])

_UNSTRUCTURED_RETRYABLE_TYPES = (
    exceptions.TooManyRequests,
    exceptions.InternalServerError,
)


def _should_retry(exc):
    """Predicate for determining when to retry.

    We retry if and only if the 'error status' is 'DEADLINE_EXCEEDED'
    or 'UNAVAILABLE'.
    """
    if hasattr(exc, "errors"):
        # Check for unstructured error returns
        return isinstance(exc, _UNSTRUCTURED_RETRYABLE_TYPES)

    if hasattr(exc, "error"):
        reason = exc.error["status"]
        return reason in _RETRYABLE_REASONS
    return False


DEFAULT_RETRY = retry.Retry(predicate=_should_retry)
"""The default retry object.

Any method with a ``retry`` parameter will be retried automatically,
with reasonable defaults. To disable retry, pass ``retry=None``.
To modify the default retry behavior, call a ``with_XXX`` method
on ``DEFAULT_RETRY``. For example, to change the deadline to 30 seconds,
pass ``retry=datastore.DEFAULT_RETRY.with_deadline(30)``.
"""
