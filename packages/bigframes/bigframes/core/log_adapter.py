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
import inspect
import threading
from typing import List, Optional

from google.cloud import bigquery
import pandas

_lock = threading.Lock()

# The limit is 64 (https://cloud.google.com/bigquery/docs/labels-intro#requirements),
# but leave a few spare for internal labels to be added.
# See internal issue 386825477.
MAX_LABELS_COUNT = 64 - 8
PANDAS_API_TRACKING_TASK = "pandas_api_tracking"
PANDAS_PARAM_TRACKING_TASK = "pandas_param_tracking"
LOG_OVERRIDE_NAME = "__log_override_name__"

_api_methods: List = []
_excluded_methods = ["__setattr__", "__getattr__"]

# Stack to track method calls
_call_stack: List = []


def submit_pandas_labels(
    bq_client: Optional[bigquery.Client],
    base_name: str,
    method_name: str,
    args=(),
    kwargs={},
    task: str = PANDAS_API_TRACKING_TASK,
):
    """
    Submits usage of API to BigQuery using a simulated failed query.

    This function is designed to capture and log details about the usage of pandas methods,
    including class and method names, the count of positional arguments, and any keyword
    arguments that match the method's signature. To avoid incurring costs, it simulates a
    query execution using a query with syntax errors.

    Args:
        bq_client (bigquery.Client): The client used to interact with BigQuery.
        base_name (str): The name of the pandas class/module being used.
        method_name (str): The name of the method being invoked.
        args (tuple): The positional arguments passed to the method.
        kwargs (dict): The keyword arguments passed to the method.
        task (str): The specific task type for the logging event:
                    - 'PANDAS_API_TRACKING_TASK': Indicates that the unimplemented feature is a method.
                    - 'PANDAS_PARAM_TRACKING_TASK': Indicates that the unimplemented feature is a
                      parameter of a method.
    """
    if bq_client is None or (
        method_name.startswith("_") and not method_name.startswith("__")
    ):
        return

    labels_dict = {
        "task": task,
        "class_name": base_name.lower(),
        "method_name": method_name.lower(),
        "args_count": len(args),
    }

    # getattr(pandas, "pandas") returns pandas
    # so we can also use this for pandas.function
    if hasattr(pandas, base_name):
        base = getattr(pandas, base_name)
    else:
        return

    # Omit __call__, because its not implemented on the actual instances of
    # DataFrame/Series, only as the constructor.
    if method_name != "__call__" and hasattr(base, method_name):
        method = getattr(base, method_name)
    else:
        return

    if kwargs:
        # Iterate through the keyword arguments and add them to the labels dictionary if they
        # are parameters that are implemented in pandas and the maximum label count has not been reached.
        signature = inspect.signature(method)
        param_names = [param.name for param in signature.parameters.values()]

        idx = 0
        for key in kwargs.keys():
            if len(labels_dict) >= MAX_LABELS_COUNT:
                break
            if key in param_names:
                labels_dict[f"kwargs_{idx}"] = key.lower()
                idx += 1

    # If this log is for tracking unimplemented parameters and no keyword arguments were
    # provided, skip logging.
    if len(labels_dict) == 4 and task == PANDAS_PARAM_TRACKING_TASK:
        return

    # Run a query with syntax error to avoid cost.
    query = "SELECT COUNT(x FROM data_table—"
    job_config = bigquery.QueryJobConfig(labels=labels_dict)
    bq_client.query(query, job_config=job_config)


def class_logger(decorated_cls=None):
    """Decorator that adds logging functionality to each method of the class."""

    def wrap(cls):
        for attr_name, attr_value in cls.__dict__.items():
            if callable(attr_value) and (attr_name not in _excluded_methods):
                if isinstance(attr_value, staticmethod):
                    setattr(
                        cls,
                        attr_name,
                        staticmethod(method_logger(attr_value)),
                    )
                else:
                    setattr(
                        cls,
                        attr_name,
                        method_logger(attr_value),
                    )
            elif isinstance(attr_value, property):
                setattr(
                    cls,
                    attr_name,
                    property_logger(attr_value),
                )
        return cls

    if decorated_cls is None:
        # The logger is used with parentheses
        return wrap

    # The logger is used without parentheses
    return wrap(decorated_cls)


def method_logger(method, /, *, custom_base_name: Optional[str] = None):
    """Decorator that adds logging functionality to a method."""

    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        api_method_name = getattr(method, LOG_OVERRIDE_NAME, method.__name__)
        if custom_base_name is None:
            qualname_parts = getattr(method, "__qualname__", method.__name__).split(".")
            class_name = qualname_parts[-2] if len(qualname_parts) > 1 else ""
            base_name = (
                class_name if class_name else "_".join(method.__module__.split(".")[1:])
            )
        else:
            base_name = custom_base_name

        full_method_name = f"{base_name.lower()}-{api_method_name}"
        # Track directly called methods
        if len(_call_stack) == 0:
            add_api_method(full_method_name)

        _call_stack.append(full_method_name)

        try:
            return method(*args, **kwargs)
        except (NotImplementedError, TypeError) as e:
            # Log method parameters that are implemented in pandas but either missing (TypeError)
            # or not fully supported (NotImplementedError) in BigFrames.
            # Logging is currently supported only when we can access the bqclient through
            # _block.session.bqclient.
            if len(_call_stack) == 1:
                submit_pandas_labels(
                    _get_bq_client(*args, **kwargs),
                    base_name,
                    api_method_name,
                    args,
                    kwargs,
                    task=PANDAS_PARAM_TRACKING_TASK,
                )
            raise e
        finally:
            _call_stack.pop()

    return wrapper


def property_logger(prop):
    """Decorator that adds logging functionality to a property."""

    def shared_wrapper(prop):
        @functools.wraps(prop)
        def wrapped(*args, **kwargs):
            qualname_parts = getattr(prop, "__qualname__", prop.__name__).split(".")
            class_name = qualname_parts[-2] if len(qualname_parts) > 1 else ""
            property_name = prop.__name__
            full_property_name = f"{class_name.lower()}-{property_name.lower()}"

            if len(_call_stack) == 0:
                add_api_method(full_property_name)

            _call_stack.append(full_property_name)
            try:
                return prop(*args, **kwargs)
            finally:
                _call_stack.pop()

        return wrapped

    # Apply the wrapper to the getter, setter, and deleter
    return property(
        shared_wrapper(prop.fget),
        shared_wrapper(prop.fset) if prop.fset else None,
        shared_wrapper(prop.fdel) if prop.fdel else None,
    )


def log_name_override(name: str):
    """
    Attaches a custom name to be used by logger.
    """

    def wrapper(func):
        setattr(func, LOG_OVERRIDE_NAME, name)
        return func

    return wrapper


def add_api_method(api_method_name):
    global _lock
    global _api_methods
    with _lock:
        # Push the method to the front of the _api_methods list
        _api_methods.insert(0, api_method_name.replace("<", "").replace(">", ""))
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


def _get_bq_client(*args, **kwargs):
    # Assumes that on BigFrames API errors (TypeError/NotImplementedError),
    # an input arg (likely the first, e.g., 'self') has `_block.session.bqclient`
    for argv in args:
        if hasattr(argv, "_block"):
            return argv._block.session.bqclient

    for kwargv in kwargs.values():
        if hasattr(kwargv, "_block"):
            return kwargv._block.session.bqclient

    return None
