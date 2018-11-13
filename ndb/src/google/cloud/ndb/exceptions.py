# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Classes representing legacy Google App Engine exceptions.

Unless otherwise noted, these are meant to act as shims for the exception
types defined in the ``google.appengine.api.datastore_errors`` module in
legacy Google App Engine runtime.
"""


__all__ = [
    "Error",
    "AsyncContextError",
    "BadValueError",
    "BadArgumentError",
    "Rollback",
    "BadFilterError",
]


class Error(Exception):
    """Base datastore error type."""


class AsyncContextError(Error):
    """Indicates an async call being made without a context.

    Raised whenever an asynchronous call is made outside of a context
    established by :func:`google.cloud.ndb.async_context`.
    """

    def __init__(self):
        super(AsyncContextError, self).__init__(
            "No currently running event loop. Asynchronous calls must be made "
            "in context established by google.cloud.ndb.async_context."
        )


class BadValueError(Error):
    """Indicates a property value or filter value is invalid.

    Raised by ``Entity.__setitem__()``, ``Query.__setitem__()``, ``Get()``,
    and others.
    """


class BadArgumentError(Error):
    """Indicates an invalid argument was passed.

    Raised by ``Query.Order()``, ``Iterator.Next()``, and others.
    """


class Rollback(Error):
    """Allows a transaction to be rolled back instead of committed.

    Note that *any* exception raised by a transaction function will cause a
    rollback. Hence, this exception type is purely for convenience.
    """


class BadQueryError(Error):
    """Raised by Query when a query or query string is invalid."""


class BadFilterError(Error):
    """Indicates a filter value is invalid.

    Raised by ``Query.__setitem__()`` and ``Query.Run()`` when a filter string
    is invalid.
    """

    def __init__(self, filter):
        self.filter = filter
        message = "invalid filter: {}.".format(self.filter).encode("utf-8")
        super(BadFilterError, self).__init__(message)
