# Copyright 2024 Google LLC
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

"""This module integrates BigQuery built-in functions for use with DataFrame objects,
such as array functions:
https://cloud.google.com/bigquery/docs/reference/standard-sql/array_functions. """

import sys

from bigframes.bigquery import ai, ml, obj
from bigframes.bigquery._operations.approx_agg import approx_top_count
from bigframes.bigquery._operations.array import (
    array_agg,
    array_length,
    array_to_string,
)
from bigframes.bigquery._operations.datetime import (
    unix_micros,
    unix_millis,
    unix_seconds,
)
from bigframes.bigquery._operations.geo import (
    st_area,
    st_buffer,
    st_centroid,
    st_convexhull,
    st_difference,
    st_distance,
    st_intersection,
    st_isclosed,
    st_length,
    st_regionstats,
    st_simplify,
)
from bigframes.bigquery._operations.io import load_data
from bigframes.bigquery._operations.json import (
    json_extract,
    json_extract_array,
    json_extract_string_array,
    json_keys,
    json_query,
    json_query_array,
    json_set,
    json_value,
    json_value_array,
    parse_json,
    to_json,
    to_json_string,
)
from bigframes.bigquery._operations.search import create_vector_index, vector_search
from bigframes.bigquery._operations.sql import sql_scalar
from bigframes.bigquery._operations.struct import struct
from bigframes.bigquery._operations.table import create_external_table
from bigframes.core.logging import log_adapter

_functions = [
    # approximate aggregate ops
    approx_top_count,
    # array ops
    array_agg,
    array_length,
    array_to_string,
    # datetime ops
    unix_micros,
    unix_millis,
    unix_seconds,
    # geo ops
    st_area,
    st_buffer,
    st_centroid,
    st_convexhull,
    st_difference,
    st_distance,
    st_intersection,
    st_isclosed,
    st_length,
    st_regionstats,
    st_simplify,
    # json ops
    json_extract,
    json_extract_array,
    json_extract_string_array,
    json_query,
    json_query_array,
    json_set,
    json_value,
    json_value_array,
    parse_json,
    to_json,
    to_json_string,
    # search ops
    create_vector_index,
    vector_search,
    # sql ops
    sql_scalar,
    # struct ops
    struct,
    # table ops
    create_external_table,
    # io ops
    load_data,
]

_module = sys.modules[__name__]
for f in _functions:
    _decorated_object = log_adapter.method_logger(f, custom_base_name="bigquery")
    setattr(_module, f.__name__, _decorated_object)
    del f

__all__ = [
    # approximate aggregate ops
    "approx_top_count",
    # array ops
    "array_agg",
    "array_length",
    "array_to_string",
    # datetime ops
    "unix_micros",
    "unix_millis",
    "unix_seconds",
    # geo ops
    "st_area",
    "st_buffer",
    "st_centroid",
    "st_convexhull",
    "st_difference",
    "st_distance",
    "st_intersection",
    "st_isclosed",
    "st_length",
    "st_regionstats",
    "st_simplify",
    # json ops
    "json_extract",
    "json_extract_array",
    "json_extract_string_array",
    "json_keys",
    "json_query",
    "json_query_array",
    "json_set",
    "json_value",
    "json_value_array",
    "parse_json",
    "to_json",
    "to_json_string",
    # search ops
    "create_vector_index",
    "vector_search",
    # sql ops
    "sql_scalar",
    # struct ops
    "struct",
    # table ops
    "create_external_table",
    # io ops
    "load_data",
    # Modules / SQL namespaces
    "ai",
    "ml",
    "obj",
]
