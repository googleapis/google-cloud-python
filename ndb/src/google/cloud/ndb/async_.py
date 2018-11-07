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

"""Manage asynchronous context. """
import contextlib

from . import _eventloop

__all__ = ["async_context"]


@contextlib.contextmanager
def async_context():
    """Establish a context for a set of asynchronous API calls.

    This function provides a context manager which establishes the event loop
    that will be used for any asynchronous NDB calls that occur in the context.
    For example::

        from google.cloud.ndb import async_context

        with async_context():
            # Make some asynchronous calls
            pass

    Within the context, any calls to a ``*_async`` function or to an
    ``ndb.tasklet``, will be added to the event loop established by the
    context.  Upon exiting the context, execution will block until all
    asynchronous calls loaded onto the event loop have finished execution.

    Code within an ``async_context`` should be single threaded. Internally, a
    ``threading.local`` instance is used to track the current event loop.

    In the context of a web application, it is recommended that a single
    ``async_context`` be used per HTTP request. This can typically be
    accomplished in a middleware layer.
    """
    loop = _eventloop.contexts.push()
    yield
    _eventloop.contexts.pop()
    loop.run()
