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

""""Low-level utilities used internally by ``ndb`."""


import threading


__all__ = []


def code_info(*args, **kwargs):
    raise NotImplementedError


DEBUG = True


def decorator(*args, **kwargs):
    raise NotImplementedError


def frame_info(*args, **kwargs):
    raise NotImplementedError


def func_info(*args, **kwargs):
    raise NotImplementedError


def gen_info(*args, **kwargs):
    raise NotImplementedError


def get_stack(*args, **kwargs):
    raise NotImplementedError


def logging_debug(*args, **kwargs):
    raise NotImplementedError


def positional(*args, **kwargs):
    raise NotImplementedError


threading_local = threading.local


def tweak_logging(*args, **kwargs):
    raise NotImplementedError


def wrapping(*args, **kwargs):
    raise NotImplementedError
