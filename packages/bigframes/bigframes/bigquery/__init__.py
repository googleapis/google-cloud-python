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

"""
Access BigQuery-specific operations and namespaces within BigQuery DataFrames.

This module provides specialized functions and sub-modules that expose BigQuery's
advanced capabilities to DataFrames and Series. It acts as a bridge between the
pandas-compatible API and the full power of BigQuery SQL.

Key sub-modules include:

* :mod:`bigframes.bigquery.ai`: Generative and predictive AI functions (Gemini, BQML).
* :mod:`bigframes.bigquery.ml`: Direct access to BigQuery ML model operations.
* :mod:`bigframes.bigquery.obj`: Support for BigQuery object tables.

This module also provides direct access to optimized BigQuery functions for:

* **JSON Processing:** High-performance functions like ``json_extract``, ``json_value``,
  and ``parse_json`` for handling semi-structured data.
* **Geospatial Analysis:** Comprehensive geographic functions such as ``st_area``,
  ``st_distance``, and ``st_centroid`` (``ST_`` prefixed functions).
* **Array Operations:** Tools for working with BigQuery arrays, including ``array_agg``
  and ``array_length``.
* **Vector Search:** Integration with BigQuery's vector search and indexing
  capabilities for high-dimensional data.
* **Custom SQL:** The ``sql_scalar`` function allows embedding raw SQL snippets for
  advanced operations not yet directly mapped in the API.

By using these functions, you can leverage BigQuery's high-performance engine for
domain-specific tasks while maintaining a Python-centric development experience.

For the full list of BigQuery standard SQL functions, see:
https://cloud.google.com/bigquery/docs/reference/standard-sql/functions-reference
"""

import sys

from bigframes.bigquery import aead, ai, ml, obj
from bigframes.bigquery._operations.approx_agg import approx_top_count
from bigframes.bigquery._operations.array import array_agg
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
from bigframes.bigquery._operations.mathematical import (
    hparam_candidates,
    hparam_range,
    rand,
)
from bigframes.bigquery._operations.search import create_vector_index, vector_search
from bigframes.bigquery._operations.sql import sql_scalar
from bigframes.bigquery._operations.struct import struct
from bigframes.bigquery._operations.table import create_external_table
from bigframes.core.logging import log_adapter
from bigframes.operations.googlesql.global_namespace.aead_encryption import (
    deterministic_decrypt_bytes,
    deterministic_decrypt_string,
    deterministic_encrypt,
)
from bigframes.operations.googlesql.global_namespace.array import (
    array_concat,
    array_first,
    array_first_n,
    array_includes,
    array_includes_all,
    array_includes_any,
    array_is_distinct,
    array_last,
    array_length,
    array_reverse,
    array_slice,
    array_to_string,
    flatten,
    generate_array,
)
from bigframes.operations.googlesql.global_namespace.bit import (
    bit_count,
)
from bigframes.operations.googlesql.global_namespace.conversion import (
    bool_,
    double,
    float64,
    int64,
    parse_bignumeric,
    parse_numeric,
    string,
)
from bigframes.operations.googlesql.global_namespace.date import (
    current_date,
    date,
    date_add,
    date_diff,
    date_from_unix_date,
    date_sub,
    date_trunc,
    extract,
    format_date,
    generate_date_array,
    last_day,
    parse_date,
    unix_date,
)

_functions = [
    # approximate aggregate ops
    approx_top_count,
    # array ops
    array_agg,
    array_concat,
    array_first,
    array_first_n,
    array_includes,
    array_includes_all,
    array_includes_any,
    array_is_distinct,
    array_last,
    array_length,
    array_reverse,
    array_slice,
    array_to_string,
    flatten,
    generate_array,
    # bit ops
    bit_count,
    # conversion ops
    bool_,
    double,
    float64,
    int64,
    parse_bignumeric,
    parse_numeric,
    string,
    # date ops
    current_date,
    date,
    date_add,
    date_diff,
    date_from_unix_date,
    date_sub,
    date_trunc,
    extract,
    format_date,
    generate_date_array,
    last_day,
    parse_date,
    unix_date,
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
    # deterministic encryption ops
    deterministic_decrypt_bytes,
    deterministic_decrypt_string,
    deterministic_encrypt,
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
    # mathematical ops
    hparam_candidates,
    hparam_range,
    rand,
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
    "array_concat",
    "array_first",
    "array_first_n",
    "array_includes",
    "array_includes_all",
    "array_includes_any",
    "array_is_distinct",
    "array_last",
    "array_length",
    "array_reverse",
    "array_slice",
    "array_to_string",
    "flatten",
    "generate_array",
    # bit ops
    "bit_count",
    # conversion ops
    "bool_",
    "double",
    "float64",
    "int64",
    "parse_bignumeric",
    "parse_numeric",
    "string",
    # date ops
    "current_date",
    "date",
    "date_add",
    "date_diff",
    "date_from_unix_date",
    "date_sub",
    "date_trunc",
    "extract",
    "format_date",
    "generate_date_array",
    "last_day",
    "parse_date",
    "unix_date",
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
    # deterministic encryption ops
    "deterministic_decrypt_bytes",
    "deterministic_decrypt_string",
    "deterministic_encrypt",
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
    # mathematical ops
    "hparam_candidates",
    "hparam_range",
    "rand",
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
    "aead",
    "ai",
    "ml",
    "obj",
]
