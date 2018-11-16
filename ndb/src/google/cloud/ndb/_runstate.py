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

"""Management of current running state."""

import contextlib
import threading

from google.cloud.ndb import exceptions


class State:
    eventloop = None


class LocalStates(threading.local):
    """Maintain a thread local stack of contextual state."""

    __slots__ = ("stack",)

    def __init__(self):
        self.stack = []

    def push(self, state):
        self.stack.append(state)

    def pop(self):
        return self.stack.pop(-1)

    def current(self):
        if self.stack:
            return self.stack[-1]


states = LocalStates()


@contextlib.contextmanager
def ndb_context():
    """Establish a context for a set of NDB calls.

    This function provides a context manager which establishes the runtime
    state for using NDB.

    For example:

    .. code-block:: python

        from google.cloud.ndb import ndb_context

        with ndb_context():
            # Use NDB for some stuff
            pass

    Use of a context is required--NDB can only be used inside a running
    context. The context is used to coordinate an event loop for asynchronous
    API calls, runtime caching policy, and other essential runtime state.

    Code within an asynchronous context should be single threaded. Internally,
    a :class:`threading.local` instance is used to track the current event
    loop.

    In a web application, it is recommended that a single context be used per
    HTTP request. This can typically be accomplished in a middleware layer.
    """
    state = State()
    states.push(state)
    yield

    # Finish up any work left to do on the event loop
    if state.eventloop is not None:
        state.eventloop.run()

    # This will pop the same state pushed above unless someone is severely
    # abusing our private data structure.
    states.pop()


def current():
    """Get the current context state.

    This function should be called within a context established by
    :func:`~google.cloud.ndb.ndb_context`.

    Returns:
        State: The state for the current context.

    Raises:
        .ContextError: If called outside of a context
            established by :func:`~google.cloud.ndb.ndb_context`.
    """
    state = states.current()
    if state:
        return state

    raise exceptions.ContextError()
