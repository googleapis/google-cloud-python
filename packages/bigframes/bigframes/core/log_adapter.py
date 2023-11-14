# Copyright 2023 Google LLC
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

import functools
import threading
from typing import List

_lock = threading.Lock()
MAX_LABELS_COUNT = 64
_api_methods: List = []


def class_logger(decorated_cls):
    """Decorator that adds logging functionality to each method of the class."""
    for attr_name, attr_value in decorated_cls.__dict__.items():
        if callable(attr_value):
            setattr(decorated_cls, attr_name, method_logger(attr_value))
    return decorated_cls


def method_logger(method):
    """Decorator that adds logging functionality to a method."""

    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        api_method_name = str(method.__name__)
        # Track regular and "dunder" methods
        if api_method_name.startswith("__") or not api_method_name.startswith("_"):
            add_api_method(api_method_name)
        return method(*args, **kwargs)

    return wrapper


def add_api_method(api_method_name):
    global _lock
    global _api_methods
    with _lock:
        # Push the method to the front of the _api_methods list
        _api_methods.insert(0, api_method_name)
        # Keep the list length within the maximum limit (adjust MAX_LABELS_COUNT as needed)
        _api_methods = _api_methods[:MAX_LABELS_COUNT]


def get_and_reset_api_methods():
    global _lock
    with _lock:
        previous_api_methods = list(_api_methods)
        _api_methods.clear()
    return previous_api_methods
