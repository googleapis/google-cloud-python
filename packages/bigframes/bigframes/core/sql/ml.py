# Copyright 2025 Google LLC
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

import collections.abc
import json
from typing import Any, Dict, List, Mapping, Optional, Union

import bigframes.core.compile.googlesql as googlesql
import bigframes.core.sql


def create_model_ddl(
    model_name: str,
    *,
    replace: bool = False,
    if_not_exists: bool = False,
    transform: Optional[list[str]] = None,
    input_schema: Optional[Mapping[str, str]] = None,
    output_schema: Optional[Mapping[str, str]] = None,
    connection_name: Optional[str] = None,
    options: Optional[Mapping[str, Union[str, int, float, bool, list]]] = None,
    training_data: Optional[str] = None,
    custom_holiday: Optional[str] = None,
) -> str:
    """Encode the CREATE MODEL statement.

    See https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create for reference.
    """

    if replace:
        create = "CREATE OR REPLACE MODEL "
    elif if_not_exists:
        create = "CREATE MODEL IF NOT EXISTS "
    else:
        create = "CREATE MODEL "

    ddl = f"{create}{googlesql.identifier(model_name)}\n"

    # [TRANSFORM (select_list)]
    if transform:
        ddl += f"TRANSFORM ({', '.join(transform)})\n"

    # [INPUT (field_name field_type) OUTPUT (field_name field_type)]
    if input_schema:
        inputs = [f"{k} {v}" for k, v in input_schema.items()]
        ddl += f"INPUT ({', '.join(inputs)})\n"

    if output_schema:
        outputs = [f"{k} {v}" for k, v in output_schema.items()]
        ddl += f"OUTPUT ({', '.join(outputs)})\n"

    # [REMOTE WITH CONNECTION {connection_name | DEFAULT}]
    if connection_name:
        if connection_name.upper() == "DEFAULT":
            ddl += "REMOTE WITH CONNECTION DEFAULT\n"
        else:
            ddl += f"REMOTE WITH CONNECTION {googlesql.identifier(connection_name)}\n"

    # [OPTIONS(model_option_list)]
    if options:
        rendered_options = []
        for option_name, option_value in options.items():
            if isinstance(option_value, (list, tuple)):
                # Handle list options like model_registry="vertex_ai"
                # wait, usually options are key=value.
                # if value is list, it is [val1, val2]
                rendered_val = bigframes.core.sql.simple_literal(list(option_value))
            else:
                rendered_val = bigframes.core.sql.simple_literal(option_value)

            rendered_options.append(f"{option_name} = {rendered_val}")

        ddl += f"OPTIONS({', '.join(rendered_options)})\n"

    # [AS {query_statement | ( training_data AS (query_statement), custom_holiday AS (holiday_statement) )}]

    if training_data:
        if custom_holiday:
            # When custom_holiday is present, we need named clauses
            parts = []
            parts.append(f"training_data AS ({training_data})")
            parts.append(f"custom_holiday AS ({custom_holiday})")
            ddl += f"AS (\n  {', '.join(parts)}\n)"
        else:
            # Just training_data is treated as the query_statement
            ddl += f"AS {training_data}\n"

    return ddl


def _build_struct_sql(
    struct_options: Mapping[
        str,
        Union[str, int, float, bool, Mapping[str, str], List[str], Mapping[str, Any]],
    ]
) -> str:
    if not struct_options:
        return ""

    rendered_options = []
    for option_name, option_value in struct_options.items():
        if option_name == "model_params":
            json_str = json.dumps(option_value)
            # Escape single quotes for SQL string literal
            sql_json_str = json_str.replace("'", "''")
            rendered_val = f"JSON'{sql_json_str}'"
        elif isinstance(option_value, collections.abc.Mapping):
            struct_body = ", ".join(
                [
                    f"{bigframes.core.sql.simple_literal(v)} AS {k}"
                    for k, v in option_value.items()
                ]
            )
            rendered_val = f"STRUCT({struct_body})"
        elif isinstance(option_value, list):
            rendered_val = (
                "["
                + ", ".join(
                    [bigframes.core.sql.simple_literal(v) for v in option_value]
                )
                + "]"
            )
        elif isinstance(option_value, bool):
            rendered_val = str(option_value).lower()
        else:
            rendered_val = bigframes.core.sql.simple_literal(option_value)
        rendered_options.append(f"{rendered_val} AS {option_name}")
    return f", STRUCT({', '.join(rendered_options)})"


def evaluate(
    model_name: str,
    *,
    table: Optional[str] = None,
    perform_aggregation: Optional[bool] = None,
    horizon: Optional[int] = None,
    confidence_level: Optional[float] = None,
) -> str:
    """Encode the ML.EVAluate statement.
    See https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate for reference.
    """
    struct_options: Dict[str, Union[str, int, float, bool]] = {}
    if perform_aggregation is not None:
        struct_options["perform_aggregation"] = perform_aggregation
    if horizon is not None:
        struct_options["horizon"] = horizon
    if confidence_level is not None:
        struct_options["confidence_level"] = confidence_level

    sql = f"SELECT * FROM ML.EVALUATE(MODEL {googlesql.identifier(model_name)}"
    if table:
        sql += f", ({table})"

    sql += _build_struct_sql(struct_options)
    sql += ")\n"
    return sql


def predict(
    model_name: str,
    table: str,
    *,
    threshold: Optional[float] = None,
    keep_original_columns: Optional[bool] = None,
    trial_id: Optional[int] = None,
) -> str:
    """Encode the ML.PREDICT statement.
    See https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict for reference.
    """
    struct_options: Dict[str, Union[str, int, float, bool]] = {}
    if threshold is not None:
        struct_options["threshold"] = threshold
    if keep_original_columns is not None:
        struct_options["keep_original_columns"] = keep_original_columns
    if trial_id is not None:
        struct_options["trial_id"] = trial_id

    sql = (
        f"SELECT * FROM ML.PREDICT(MODEL {googlesql.identifier(model_name)}, ({table})"
    )
    sql += _build_struct_sql(struct_options)
    sql += ")\n"
    return sql


def explain_predict(
    model_name: str,
    table: str,
    *,
    top_k_features: Optional[int] = None,
    threshold: Optional[float] = None,
    integrated_gradients_num_steps: Optional[int] = None,
    approx_feature_contrib: Optional[bool] = None,
) -> str:
    """Encode the ML.EXPLAIN_PREDICT statement.
    See https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-explain-predict for reference.
    """
    struct_options: Dict[str, Union[str, int, float, bool]] = {}
    if top_k_features is not None:
        struct_options["top_k_features"] = top_k_features
    if threshold is not None:
        struct_options["threshold"] = threshold
    if integrated_gradients_num_steps is not None:
        struct_options[
            "integrated_gradients_num_steps"
        ] = integrated_gradients_num_steps
    if approx_feature_contrib is not None:
        struct_options["approx_feature_contrib"] = approx_feature_contrib

    sql = f"SELECT * FROM ML.EXPLAIN_PREDICT(MODEL {googlesql.identifier(model_name)}, ({table})"
    sql += _build_struct_sql(struct_options)
    sql += ")\n"
    return sql


def global_explain(
    model_name: str,
    *,
    class_level_explain: Optional[bool] = None,
) -> str:
    """Encode the ML.GLOBAL_EXPLAIN statement.
    See https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-global-explain for reference.
    """
    struct_options: Dict[str, Union[str, int, float, bool]] = {}
    if class_level_explain is not None:
        struct_options["class_level_explain"] = class_level_explain

    sql = f"SELECT * FROM ML.GLOBAL_EXPLAIN(MODEL {googlesql.identifier(model_name)}"
    sql += _build_struct_sql(struct_options)
    sql += ")\n"
    return sql


def transform(
    model_name: str,
    table: str,
) -> str:
    """Encode the ML.TRANSFORM statement.
    See https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-transform for reference.
    """
    sql = f"SELECT * FROM ML.TRANSFORM(MODEL {googlesql.identifier(model_name)}, ({table}))\n"
    return sql


def generate_text(
    model_name: str,
    table: str,
    *,
    temperature: Optional[float] = None,
    max_output_tokens: Optional[int] = None,
    top_k: Optional[int] = None,
    top_p: Optional[float] = None,
    flatten_json_output: Optional[bool] = None,
    stop_sequences: Optional[List[str]] = None,
    ground_with_google_search: Optional[bool] = None,
    request_type: Optional[str] = None,
) -> str:
    """Encode the ML.GENERATE_TEXT statement.
    See https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-generate-text for reference.
    """
    struct_options: Dict[
        str,
        Union[str, int, float, bool, Mapping[str, str], List[str], Mapping[str, Any]],
    ] = {}
    if temperature is not None:
        struct_options["temperature"] = temperature
    if max_output_tokens is not None:
        struct_options["max_output_tokens"] = max_output_tokens
    if top_k is not None:
        struct_options["top_k"] = top_k
    if top_p is not None:
        struct_options["top_p"] = top_p
    if flatten_json_output is not None:
        struct_options["flatten_json_output"] = flatten_json_output
    if stop_sequences is not None:
        struct_options["stop_sequences"] = stop_sequences
    if ground_with_google_search is not None:
        struct_options["ground_with_google_search"] = ground_with_google_search
    if request_type is not None:
        struct_options["request_type"] = request_type

    sql = f"SELECT * FROM ML.GENERATE_TEXT(MODEL {googlesql.identifier(model_name)}, ({table})"
    sql += _build_struct_sql(struct_options)
    sql += ")\n"
    return sql


def generate_embedding(
    model_name: str,
    table: str,
    *,
    flatten_json_output: Optional[bool] = None,
    task_type: Optional[str] = None,
    output_dimensionality: Optional[int] = None,
) -> str:
    """Encode the ML.GENERATE_EMBEDDING statement.
    See https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-generate-embedding for reference.
    """
    struct_options: Dict[
        str,
        Union[str, int, float, bool, Mapping[str, str], List[str], Mapping[str, Any]],
    ] = {}
    if flatten_json_output is not None:
        struct_options["flatten_json_output"] = flatten_json_output
    if task_type is not None:
        struct_options["task_type"] = task_type
    if output_dimensionality is not None:
        struct_options["output_dimensionality"] = output_dimensionality

    sql = f"SELECT * FROM ML.GENERATE_EMBEDDING(MODEL {googlesql.identifier(model_name)}, ({table})"
    sql += _build_struct_sql(struct_options)
    sql += ")\n"
    return sql
