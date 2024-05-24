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
_excluded_methods = ["__setattr__", "__getattr__"]

# Stack to track method calls
_call_stack: List = []


def class_logger(decorated_cls):
    """Decorator that adds logging functionality to each method of the class."""
    for attr_name, attr_value in decorated_cls.__dict__.items():
        if callable(attr_value) and (attr_name not in _excluded_methods):
            setattr(decorated_cls, attr_name, method_logger(attr_value, decorated_cls))
        elif isinstance(attr_value, property):
            setattr(
                decorated_cls, attr_name, property_logger(attr_value, decorated_cls)
            )
    return decorated_cls


def method_logger(method, decorated_cls):
    """Decorator that adds logging functionality to a method."""

    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        class_name = decorated_cls.__name__  # Access decorated class name
        api_method_name = str(method.__name__)
        full_method_name = f"{class_name.lower()}-{api_method_name}"

        # Track directly called methods
        if len(_call_stack) == 0:
            add_api_method(full_method_name)

        _call_stack.append(full_method_name)

        try:
            return method(*args, **kwargs)
        finally:
            _call_stack.pop()

    return wrapper


def property_logger(prop, decorated_cls):
    """Decorator that adds logging functionality to a property."""

    def shared_wrapper(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            class_name = decorated_cls.__name__
            property_name = f.__name__
            full_property_name = f"{class_name.lower()}-{property_name.lower()}"

            if len(_call_stack) == 0:
                add_api_method(full_property_name)

            _call_stack.append(full_property_name)
            try:
                return f(*args, **kwargs)
            finally:
                _call_stack.pop()

        return wrapped

    # Apply the wrapper to the getter, setter, and deleter
    return property(
        shared_wrapper(prop.fget),
        shared_wrapper(prop.fset) if prop.fset else None,
        shared_wrapper(prop.fdel) if prop.fdel else None,
    )


def add_api_method(api_method_name):
    global _lock
    global _api_methods
    with _lock:
        # Push the method to the front of the _api_methods list
        _api_methods.insert(0, api_method_name)
        # Keep the list length within the maximum limit (adjust MAX_LABELS_COUNT as needed)
        _api_methods = _api_methods[:MAX_LABELS_COUNT]


def get_and_reset_api_methods(dry_run: bool = False):
    global _lock
    with _lock:
        previous_api_methods = list(_api_methods)

        # dry_run might not make a job resource, so only reset the log on real queries.
        if not dry_run:
            _api_methods.clear()
    return previous_api_methods
