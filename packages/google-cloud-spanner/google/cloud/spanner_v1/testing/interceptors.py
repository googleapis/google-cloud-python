# Copyright 2023     Google LLC All rights reserved.
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

from collections import defaultdict
from grpc_interceptor import ClientInterceptor
from google.api_core.exceptions import Aborted


class MethodCountInterceptor(ClientInterceptor):
    """Test interceptor that counts number of times a method is being called."""

    def __init__(self):
        self._counts = defaultdict(int)

    def intercept(self, method, request_or_iterator, call_details):
        """Count number of times a method is being called."""
        self._counts[call_details.method] += 1
        return method(request_or_iterator, call_details)

    def reset(self):
        self._counts = defaultdict(int)


class MethodAbortInterceptor(ClientInterceptor):
    """Test interceptor that throws Aborted exception for a specific method."""

    def __init__(self):
        self._method_to_abort = None
        self._count = 0
        self._max_raise_count = 1
        self._connection = None

    def intercept(self, method, request_or_iterator, call_details):
        if (
            self._count < self._max_raise_count
            and call_details.method == self._method_to_abort
        ):
            self._count += 1
            if self._connection is not None:
                self._connection._transaction.rollback()
            raise Aborted("Thrown from ClientInterceptor for testing")
        return method(request_or_iterator, call_details)

    def set_method_to_abort(self, method_to_abort, connection=None, max_raise_count=1):
        self._method_to_abort = method_to_abort
        self._count = 0
        self._max_raise_count = max_raise_count
        self._connection = connection

    def reset(self):
        """Reset the interceptor to the original state."""
        self._method_to_abort = None
        self._count = 0
        self._connection = None
