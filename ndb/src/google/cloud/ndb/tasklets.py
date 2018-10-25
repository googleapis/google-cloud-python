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

"""Provides a tasklet decorator and related helpers.

Tasklets are a way to write concurrently running functions without
threads.
"""


__all__ = [
    "add_flow_exception",
    "Future",
    "get_context",
    "get_return_value",
    "make_context",
    "make_default_context",
    "MultiFuture",
    "QueueFuture",
    "ReducingFuture",
    "Return",
    "SerialQueueFuture",
    "set_context",
    "sleep",
    "synctasklet",
    "tasklet",
    "toplevel",
]


def add_flow_exception(*args, **kwargs):
    raise NotImplementedError


class Future:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


def get_context(*args, **kwargs):
    raise NotImplementedError


def get_return_value(*args, **kwargs):
    raise NotImplementedError


def make_context(*args, **kwargs):
    raise NotImplementedError


def make_default_context(*args, **kwargs):
    raise NotImplementedError


class MultiFuture:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class QueueFuture:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class ReducingFuture:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


Return = StopIteration


class SerialQueueFuture:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


def set_context(*args, **kwargs):
    raise NotImplementedError


def sleep(*args, **kwargs):
    raise NotImplementedError


def synctasklet(*args, **kwargs):
    raise NotImplementedError


def tasklet(*args, **kwargs):
    raise NotImplementedError


def toplevel(*args, **kwargs):
    raise NotImplementedError
