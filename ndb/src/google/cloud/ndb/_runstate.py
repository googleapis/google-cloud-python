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

"""Management of current running context."""

import threading

from google.cloud.ndb import exceptions


class LocalContexts(threading.local):
    """Maintain a thread local stack of contexts."""

    __slots__ = ("stack",)

    def __init__(self):
        self.stack = []

    def push(self, context):
        self.stack.append(context)

    def pop(self):
        return self.stack.pop(-1)

    def current(self):
        if self.stack:
            return self.stack[-1]


contexts = LocalContexts()


def current():
    """Get the current context.

    This function should be called within a context established by
    :meth:`google.cloud.ndb.client.Client.context`.

    Returns:
        Context: The current context.

    Raises:
        .ContextError: If called outside of a context
            established by :meth:`google.cloud.ndb.client.Client.context`.
    """
    context = contexts.current()
    if context:
        return context

    raise exceptions.ContextError()
