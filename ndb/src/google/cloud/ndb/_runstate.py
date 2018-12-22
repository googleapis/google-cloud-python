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
    def __init__(self, client):
        self.client = client
        self.eventloop = None
        self.stub = None


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
def state_context(client):
    """Establish a context for a set of NDB calls.

    Called from :meth:`google.cloud.ndb.client.Client.context` which has more
    information.
    """
    state = State(client)
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
    :meth:`google.cloud.ndb.client.Client.context`.

    Returns:
        State: The state for the current context.

    Raises:
        .ContextError: If called outside of a context
            established by :meth:`google.cloud.ndb.client.Client.context`.
    """
    state = states.current()
    if state:
        return state

    raise exceptions.ContextError()
