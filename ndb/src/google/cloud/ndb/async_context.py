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

    TODO
    """
    loop = _eventloop.contexts.push()
    yield
    _eventloop.contexts.pop()
    loop.run()
