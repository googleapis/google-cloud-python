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

from __future__ import annotations

import inspect
import logging
import os
import textwrap
from typing import Tuple

import cloudpickle

logger = logging.getLogger(__name__)


# Protocol version 4 is available in python version 3.4 and above
# https://docs.python.org/3/library/pickle.html#data-stream-format
_pickle_protocol_version = 4


# Placeholder variables for testing.
input_types = ("STRING",)
output_type = "STRING"


# Convert inputs to BigQuery JSON. See:
# https://cloud.google.com/bigquery/docs/remote-functions#json_encoding_of_sql_data_type
# and
# https://cloud.google.com/bigquery/docs/reference/standard-sql/json_functions#to_json_string
def convert_call(input_types, call):
    for type_, arg in zip(input_types, call):
        yield convert_from_bq_json(type_, arg)


def convert_from_bq_json(type_, arg):
    import base64
    import collections

    converters = collections.defaultdict(lambda: (lambda value: value))  # type: ignore
    converters["BYTES"] = base64.b64decode
    converter = converters[type_]
    return converter(arg) if arg is not None else None


def convert_to_bq_json(type_, arg):
    import base64
    import collections

    converters = collections.defaultdict(lambda: (lambda value: value))  # type: ignore
    converters["BYTES"] = lambda value: base64.b64encode(value).decode("utf-8")
    converter = converters[type_]
    return converter(arg) if arg is not None else None


# get_pd_series is the inverse of Block._get_rows_as_json_values
# NOTE: Keep in sync with the list of supported types in DataFrame.apply.
def get_pd_series(row):
    import ast
    import base64
    import json
    from typing import Callable, cast

    import pandas as pd

    row_json = json.loads(row)
    col_names = row_json["names"]
    col_types = row_json["types"]
    col_values = row_json["values"]
    index_length = row_json["indexlength"]
    dtype = row_json["dtype"]

    # At this point we are assuming that col_names, col_types and col_values are
    # arrays of the same length, representing column names, types and values for
    # one row of data

    # column names are not necessarily strings
    # they are serialized as repr(name) at source
    evaluated_col_names = []
    for col_name in col_names:
        try:
            col_name = ast.literal_eval(col_name)
        except Exception as ex:
            raise NameError(f"Failed to evaluate column name from '{col_name}': {ex}")
        evaluated_col_names.append(col_name)
    col_names = evaluated_col_names

    # Supported converters for pandas to python types
    value_converters = {
        "boolean": lambda val: val == "true",
        "Int64": int,
        "Float64": float,
        "string": str,
        "binary[pyarrow]": base64.b64decode,
    }

    def convert_value(value, value_type):
        value_converter = cast(Callable, value_converters.get(value_type))
        if value_converter is None:
            raise ValueError(f"Don't know how to handle type '{value_type}'")
        if value is None:
            return None
        return value_converter(value)

    index_values = [
        pd.Series([convert_value(col_values[i], col_types[i])], dtype=col_types[i])[0]
        for i in range(index_length)
    ]

    data_col_names = col_names[index_length:]
    data_col_types = col_types[index_length:]
    data_col_values = col_values[index_length:]
    data_col_values = [
        pd.Series([convert_value(a, data_col_types[i])], dtype=data_col_types[i])[0]
        for i, a in enumerate(data_col_values)
    ]

    row_index = index_values[0] if len(index_values) == 1 else tuple(index_values)
    row_series = pd.Series(
        data_col_values, index=data_col_names, name=row_index, dtype=dtype
    )
    return row_series


def udf(*args):
    """Dummy function to use as a placeholder for function code in templates."""
    pass


# We want to build a cloud function that works for BQ remote functions,
# where we receive `calls` in json which is a batch of rows from BQ SQL.
# The number and the order of values in each row is expected to exactly
# match to the number and order of arguments in the udf , e.g. if the udf is
#   def foo(x: int, y: str):
#     ...
# then the http request body could look like
# {
#   ...
#   "calls" : [
#     [123, "hello"],
#     [456, "world"]
#   ]
#   ...
# }
# https://cloud.google.com/bigquery/docs/reference/standard-sql/remote-functions#input_format
def udf_http(request):
    global input_types, output_type
    import json
    import traceback

    from flask import jsonify

    try:
        request_json = request.get_json(silent=True)
        calls = request_json["calls"]
        replies = []
        for call in calls:
            reply = convert_to_bq_json(
                output_type, udf(*convert_call(input_types, call))
            )
            if type(reply) is list:
                # Since the BQ remote function does not support array yet,
                # return a json serialized version of the reply
                reply = json.dumps(reply)
            replies.append(reply)
        return_json = json.dumps({"replies": replies})
        return return_json
    except Exception:
        return jsonify({"errorMessage": traceback.format_exc()}), 400


def udf_http_row_processor(request):
    global output_type
    import json
    import math
    import traceback

    from flask import jsonify
    import pandas as pd

    try:
        request_json = request.get_json(silent=True)
        calls = request_json["calls"]
        replies = []
        for call in calls:
            reply = convert_to_bq_json(output_type, udf(get_pd_series(call[0])))
            if type(reply) is list:
                # Since the BQ remote function does not support array yet,
                # return a json serialized version of the reply.
                # Numpy types are not json serializable, so use their Python
                # values instead.
                reply = [val.item() if hasattr(val, "item") else val for val in reply]
                reply = json.dumps(reply)
            elif isinstance(reply, float) and (math.isnan(reply) or math.isinf(reply)):
                # Json serialization of the special float values (nan, inf, -inf)
                # is not in strict compliance of the JSON specification
                # https://docs.python.org/3/library/json.html#basic-usage.
                # Let's convert them to a quoted string representation ("NaN",
                # "Infinity", "-Infinity" respectively) which is handled by
                # BigQuery
                reply = json.dumps(reply)
            elif pd.isna(reply):
                # Pandas N/A values are not json serializable, so use a python
                # equivalent instead
                reply = None
            elif hasattr(reply, "item"):
                # Numpy types are not json serializable, so use its Python
                # value instead
                reply = reply.item()
            replies.append(reply)
        return_json = json.dumps({"replies": replies})
        return return_json
    except Exception:
        return jsonify({"errorMessage": traceback.format_exc()}), 400


def generate_udf_code(def_, directory):
    """Generate serialized code using cloudpickle given a udf."""
    udf_code_file_name = "udf.py"
    udf_pickle_file_name = "udf.cloudpickle"

    # original code, only for debugging purpose
    udf_code = textwrap.dedent(inspect.getsource(def_))
    udf_code_file_path = os.path.join(directory, udf_code_file_name)
    with open(udf_code_file_path, "w") as f:
        f.write(udf_code)

    # serialized udf
    udf_pickle_file_path = os.path.join(directory, udf_pickle_file_name)
    # TODO(b/345433300): try io.BytesIO to avoid writing to the file system
    with open(udf_pickle_file_path, "wb") as f:
        cloudpickle.dump(def_, f, protocol=_pickle_protocol_version)

    return udf_code_file_name, udf_pickle_file_name


def generate_cloud_function_main_code(
    def_,
    directory,
    *,
    input_types: Tuple[str],
    output_type: str,
    is_row_processor=False,
):
    """Get main.py code for the cloud function for the given user defined function."""

    # Pickle the udf with all its dependencies
    udf_code_file, udf_pickle_file = generate_udf_code(def_, directory)

    code_blocks = [
        f"""\
import cloudpickle

# original udf code is in {udf_code_file}
# serialized udf code is in {udf_pickle_file}
with open("{udf_pickle_file}", "rb") as f:
    udf = cloudpickle.load(f)

input_types = {repr(input_types)}
output_type = {repr(output_type)}
"""
    ]

    # For converting scalar outputs to the correct type.
    code_blocks.append(inspect.getsource(convert_to_bq_json))

    if is_row_processor:
        code_blocks.append(inspect.getsource(get_pd_series))
        handler_func_name = "udf_http_row_processor"
        code_blocks.append(inspect.getsource(udf_http_row_processor))
    else:
        code_blocks.append(inspect.getsource(convert_call))
        code_blocks.append(inspect.getsource(convert_from_bq_json))
        handler_func_name = "udf_http"
        code_blocks.append(inspect.getsource(udf_http))

    main_py = os.path.join(directory, "main.py")
    with open(main_py, "w") as f:
        f.writelines(code_blocks)
    logger.debug(f"Wrote {os.path.abspath(main_py)}:\n{open(main_py).read()}")

    return handler_func_name
