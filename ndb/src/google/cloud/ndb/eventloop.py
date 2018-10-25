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

"""Event loop for running callbacks.

This should handle both asynchronous ``ndb`` objects and arbitrary callbacks.
"""


__all__ = [
    "add_idle",
    "EventLoop",
    "get_event_loop",
    "queue_call",
    "queue_rpc",
    "run",
    "run0",
    "run1",
]


def add_idle(*args, **kwargs):
    raise NotImplementedError


class EventLoop:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


def get_event_loop(*args, **kwargs):
    raise NotImplementedError


def queue_call(*args, **kwargs):
    raise NotImplementedError


def queue_rpc(*args, **kwargs):
    raise NotImplementedError


def run(*args, **kwargs):
    raise NotImplementedError


def run0(*args, **kwargs):
    raise NotImplementedError


def run1(*args, **kwargs):
    raise NotImplementedError
