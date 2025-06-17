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

"""
Generates SQL queries needed for BigQuery DataFrames ML
"""

from typing import Iterable, Literal, Mapping, Optional, Union

import bigframes_vendored.constants as constants
import google.cloud.bigquery

import bigframes.core.compile.googlesql as sql_utils
import bigframes.core.sql as sql_vals

INDENT_STR = "  "


# TODO: Add proper escaping logic from core/compile module
class BaseSqlGenerator:
    """Generate base SQL strings for ML. Model name isn't needed in this class."""

    # General methods
    def encode_value(self, v: Union[str, int, float, Iterable[str]]) -> str:
        """Encode a parameter value for SQL"""
        if isinstance(v, (str, int, float)):
            return sql_vals.simple_literal(v)
        elif isinstance(v, Iterable):
            inner = ", ".join([self.encode_value(x) for x in v])
            return f"[{inner}]"
        else:
            raise ValueError(
                f"Unexpected value type {type(v)}. {constants.FEEDBACK_LINK}"
            )

    def build_parameters(self, **kwargs: Union[str, int, float, Iterable[str]]) -> str:
        """Encode a dict of values into a formatted Iterable of key-value pairs for SQL"""
        param_strs = [f"{k}={self.encode_value(v)}" for k, v in kwargs.items()]
        return "\n" + INDENT_STR + f",\n{INDENT_STR}".join(param_strs)

    def build_named_parameters(
        self, **kwargs: Union[str, int, float, Iterable[str]]
    ) -> str:
        param_strs = [f"{k} => {self.encode_value(v)}" for k, v in kwargs.items()]
        return "\n" + INDENT_STR + f",\n{INDENT_STR}".join(param_strs)

    def build_structs(self, **kwargs: Union[int, float, str, Mapping]) -> str:
        """Encode a dict of values into a formatted STRUCT items for SQL"""
        param_strs = []
        for k, v in kwargs.items():
            v_trans = self.build_schema(**v) if isinstance(v, Mapping) else v

            param_strs.append(
                f"{sql_vals.simple_literal(v_trans)} AS {sql_utils.identifier(k)}"
            )

        return "\n" + INDENT_STR + f",\n{INDENT_STR}".join(param_strs)

    def build_expressions(self, *expr_sqls: str) -> str:
        """Encode a Iterable of SQL expressions into a formatted Iterable for SQL"""
        return "\n" + INDENT_STR + f",\n{INDENT_STR}".join(expr_sqls)

    def build_schema(self, **kwargs: str) -> str:
        """Encode a dict of values into a formatted schema type items for SQL"""
        param_strs = [f"{sql_utils.identifier(k)} {v}" for k, v in kwargs.items()]
        return "\n" + INDENT_STR + f",\n{INDENT_STR}".join(param_strs)

    def options(self, **kwargs: Union[str, int, float, Iterable[str]]) -> str:
        """Encode the OPTIONS clause for BQML"""
        return f"OPTIONS({self.build_parameters(**kwargs)})"

    def struct_options(self, **kwargs: Union[int, float, Mapping]) -> str:
        """Encode a BQ STRUCT as options."""
        return f"STRUCT({self.build_structs(**kwargs)})"

    def struct_columns(self, columns: Iterable[str]) -> str:
        """Encode a BQ Table columns to a STRUCT."""
        columns_str = ", ".join(map(sql_utils.identifier, columns))
        return f"STRUCT({columns_str})"

    def input(self, **kwargs: str) -> str:
        """Encode a BQML INPUT clause."""
        return f"INPUT({self.build_schema(**kwargs)})"

    def output(self, **kwargs: str) -> str:
        """Encode a BQML OUTPUT clause."""
        return f"OUTPUT({self.build_schema(**kwargs)})"

    # Connection
    def connection(self, conn_name: str) -> str:
        """Encode the REMOTE WITH CONNECTION clause for BQML. conn_name is of the format <PROJECT_NUMBER/PROJECT_ID>.<REGION>.<CONNECTION_NAME>."""
        return f"REMOTE WITH CONNECTION `{conn_name}`"

    # Transformers
    def transform(self, *expr_sqls: str) -> str:
        """Encode the TRANSFORM clause for BQML"""
        return f"TRANSFORM({self.build_expressions(*expr_sqls)})"

    def ml_standard_scaler(self, numeric_expr_sql: str, name: str) -> str:
        """Encode ML.STANDARD_SCALER for BQML"""
        return f"""ML.STANDARD_SCALER({sql_utils.identifier(numeric_expr_sql)}) OVER() AS {sql_utils.identifier(name)}"""

    def ml_max_abs_scaler(self, numeric_expr_sql: str, name: str) -> str:
        """Encode ML.MAX_ABS_SCALER for BQML"""
        return f"""ML.MAX_ABS_SCALER({sql_utils.identifier(numeric_expr_sql)}) OVER() AS {sql_utils.identifier(name)}"""

    def ml_min_max_scaler(self, numeric_expr_sql: str, name: str) -> str:
        """Encode ML.MIN_MAX_SCALER for BQML"""
        return f"""ML.MIN_MAX_SCALER({sql_utils.identifier(numeric_expr_sql)}) OVER() AS {sql_utils.identifier(name)}"""

    def ml_imputer(
        self,
        col_name: str,
        strategy: str,
        name: str,
    ) -> str:
        """Encode ML.IMPUTER for BQML"""
        return f"""ML.IMPUTER({sql_utils.identifier(col_name)}, '{strategy}') OVER() AS {sql_utils.identifier(name)}"""

    def ml_bucketize(
        self,
        input_id: str,
        array_split_points: Iterable[Union[int, float]],
        output_id: str,
    ) -> str:
        """Encode ML.BUCKETIZE for BQML"""
        # Use Python value rather than Numpy value to serialization.
        points = [
            point.item() if hasattr(point, "item") else point
            for point in array_split_points
        ]
        return f"""ML.BUCKETIZE({sql_utils.identifier(input_id)}, {points}, FALSE) AS {sql_utils.identifier(output_id)}"""

    def ml_quantile_bucketize(
        self,
        numeric_expr_sql: str,
        num_bucket: int,
        name: str,
    ) -> str:
        """Encode ML.QUANTILE_BUCKETIZE for BQML"""
        return f"""ML.QUANTILE_BUCKETIZE({sql_utils.identifier(numeric_expr_sql)}, {num_bucket}) OVER() AS {sql_utils.identifier(name)}"""

    def ml_one_hot_encoder(
        self,
        numeric_expr_sql: str,
        drop: str,
        top_k: int,
        frequency_threshold: int,
        name: str,
    ) -> str:
        """Encode ML.ONE_HOT_ENCODER for BQML.
        https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-one-hot-encoder for params."""
        return f"""ML.ONE_HOT_ENCODER({sql_utils.identifier(numeric_expr_sql)}, '{drop}', {top_k}, {frequency_threshold}) OVER() AS {sql_utils.identifier(name)}"""

    def ml_label_encoder(
        self,
        numeric_expr_sql: str,
        top_k: int,
        frequency_threshold: int,
        name: str,
    ) -> str:
        """Encode ML.LABEL_ENCODER for BQML.
        https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-label-encoder for params."""
        return f"""ML.LABEL_ENCODER({sql_utils.identifier(numeric_expr_sql)}, {top_k}, {frequency_threshold}) OVER() AS {sql_utils.identifier(name)}"""

    def ml_polynomial_expand(
        self, columns: Iterable[str], degree: int, name: str
    ) -> str:
        """Encode ML.POLYNOMIAL_EXPAND.
        https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-polynomial-expand"""
        return f"""ML.POLYNOMIAL_EXPAND({self.struct_columns(columns)}, {degree}) AS {sql_utils.identifier(name)}"""

    def ml_distance(
        self,
        col_x: str,
        col_y: str,
        type: Literal["EUCLIDEAN", "MANHATTAN", "COSINE"],
        source_sql: str,
        name: str,
    ) -> str:
        """Encode ML.DISTANCE for BQML.
        https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-distance"""
        return f"""SELECT *, ML.DISTANCE({sql_utils.identifier(col_x)}, {sql_utils.identifier(col_y)}, '{type}') AS {sql_utils.identifier(name)} FROM ({source_sql})"""

    def ai_forecast(
        self,
        source_sql: str,
        options: Mapping[str, Union[int, float, bool, Iterable[str]]],
    ):
        """Encode AI.FORECAST.
        https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-forecast"""
        named_parameters_sql = self.build_named_parameters(**options)

        return f"""SELECT * FROM AI.FORECAST(({source_sql}),{named_parameters_sql})"""


class ModelCreationSqlGenerator(BaseSqlGenerator):
    """Sql generator for creating a model entity. Model id is the standalone id without project id and dataset id."""

    def _model_id_sql(
        self,
        model_ref: google.cloud.bigquery.ModelReference,
    ):
        return f"{sql_utils.identifier(model_ref.project)}.{sql_utils.identifier(model_ref.dataset_id)}.{sql_utils.identifier(model_ref.model_id)}"

    # Model create and alter
    def create_model(
        self,
        source_sql: str,
        model_ref: google.cloud.bigquery.ModelReference,
        options: Mapping[str, Union[str, int, float, Iterable[str]]] = {},
        transforms: Optional[Iterable[str]] = None,
    ) -> str:
        """Encode the CREATE OR REPLACE MODEL statement for BQML"""
        parts = [f"CREATE OR REPLACE MODEL {self._model_id_sql(model_ref)}"]
        if transforms:
            parts.append(self.transform(*transforms))
        if options:
            parts.append(self.options(**options))
        parts.append(f"AS {source_sql}")
        return "\n".join(parts)

    def create_llm_remote_model(
        self,
        source_sql: str,
        connection_name: str,
        model_ref: google.cloud.bigquery.ModelReference,
        options: Mapping[str, Union[str, int, float, Iterable[str]]] = {},
    ) -> str:
        """Encode the CREATE OR REPLACE MODEL statement for BQML"""
        parts = [f"CREATE OR REPLACE MODEL {self._model_id_sql(model_ref)}"]
        parts.append(self.connection(connection_name))
        if options:
            parts.append(self.options(**options))
        parts.append(f"AS {source_sql}")
        return "\n".join(parts)

    def create_remote_model(
        self,
        connection_name: str,
        model_ref: google.cloud.bigquery.ModelReference,
        input: Mapping[str, str] = {},
        output: Mapping[str, str] = {},
        options: Mapping[str, Union[str, int, float, Iterable[str]]] = {},
    ) -> str:
        """Encode the CREATE OR REPLACE MODEL statement for BQML remote model."""
        parts = [f"CREATE OR REPLACE MODEL {self._model_id_sql(model_ref)}"]
        if input:
            parts.append(self.input(**input))
        if output:
            parts.append(self.output(**output))
        parts.append(self.connection(connection_name))
        if options:
            parts.append(self.options(**options))
        return "\n".join(parts)

    def create_imported_model(
        self,
        model_ref: google.cloud.bigquery.ModelReference,
        options: Mapping[str, Union[str, int, float, Iterable[str]]] = {},
    ) -> str:
        """Encode the CREATE OR REPLACE MODEL statement for BQML remote model."""

        parts = [f"CREATE OR REPLACE MODEL {self._model_id_sql(model_ref)}"]
        if options:
            parts.append(self.options(**options))
        return "\n".join(parts)

    def create_xgboost_imported_model(
        self,
        model_ref: google.cloud.bigquery.ModelReference,
        input: Mapping[str, str] = {},
        output: Mapping[str, str] = {},
        options: Mapping[str, Union[str, int, float, Iterable[str]]] = {},
    ) -> str:
        """Encode the CREATE OR REPLACE MODEL statement for BQML remote model."""

        parts = [f"CREATE OR REPLACE MODEL {self._model_id_sql(model_ref)}"]
        if input:
            parts.append(self.input(**input))
        if output:
            parts.append(self.output(**output))
        if options:
            parts.append(self.options(**options))
        return "\n".join(parts)


class ModelManipulationSqlGenerator(BaseSqlGenerator):
    """Sql generator for manipulating a model entity. Model name is the full model path of project_id.dataset_id.model_id."""

    def __init__(self, model_ref: google.cloud.bigquery.ModelReference):
        self._model_ref = model_ref

    def _model_ref_sql(self) -> str:
        return f"{sql_utils.identifier(self._model_ref.project)}.{sql_utils.identifier(self._model_ref.dataset_id)}.{sql_utils.identifier(self._model_ref.model_id)}"

    # Alter model
    def alter_model(
        self,
        options: Mapping[str, Union[str, int, float, Iterable[str]]] = {},
    ) -> str:
        """Encode the ALTER MODEL statement for BQML"""
        options_sql = self.options(**options)

        parts = [f"ALTER MODEL {self._model_ref_sql()}"]
        parts.append(f"SET {options_sql}")
        return "\n".join(parts)

    # ML prediction TVFs
    def ml_recommend(self, source_sql: str) -> str:
        """Encode ML.RECOMMEND for BQML"""
        return f"""SELECT * FROM ML.RECOMMEND(MODEL {self._model_ref_sql()},
  ({source_sql}))"""

    def ml_predict(self, source_sql: str) -> str:
        """Encode ML.PREDICT for BQML"""
        return f"""SELECT * FROM ML.PREDICT(MODEL {self._model_ref_sql()},
  ({source_sql}))"""

    def ml_explain_predict(
        self, source_sql: str, struct_options: Mapping[str, Union[int, float]]
    ) -> str:
        """Encode ML.EXPLAIN_PREDICT for BQML"""
        struct_options_sql = self.struct_options(**struct_options)
        return f"""SELECT * FROM ML.EXPLAIN_PREDICT(MODEL {self._model_ref_sql()},
  ({source_sql}), {struct_options_sql})"""

    def ml_global_explain(self, struct_options) -> str:
        """Encode ML.GLOBAL_EXPLAIN for BQML"""
        struct_options_sql = self.struct_options(**struct_options)
        return f"""SELECT * FROM ML.GLOBAL_EXPLAIN(MODEL {self._model_ref_sql()},
  {struct_options_sql})"""

    def ml_forecast(self, struct_options: Mapping[str, Union[int, float]]) -> str:
        """Encode ML.FORECAST for BQML"""
        struct_options_sql = self.struct_options(**struct_options)
        return f"""SELECT * FROM ML.FORECAST(MODEL {self._model_ref_sql()},
  {struct_options_sql})"""

    def ml_explain_forecast(
        self, struct_options: Mapping[str, Union[int, float]]
    ) -> str:
        """Encode ML.EXPLAIN_FORECAST for BQML"""
        struct_options_sql = self.struct_options(**struct_options)
        return f"""SELECT * FROM ML.EXPLAIN_FORECAST(MODEL {self._model_ref_sql()},
  {struct_options_sql})"""

    def ml_generate_text(
        self, source_sql: str, struct_options: Mapping[str, Union[int, float]]
    ) -> str:
        """Encode ML.GENERATE_TEXT for BQML"""
        struct_options_sql = self.struct_options(**struct_options)
        return f"""SELECT * FROM ML.GENERATE_TEXT(MODEL {self._model_ref_sql()},
  ({source_sql}), {struct_options_sql})"""

    def ml_generate_embedding(
        self, source_sql: str, struct_options: Mapping[str, Union[int, float]]
    ) -> str:
        """Encode ML.GENERATE_EMBEDDING for BQML"""
        struct_options_sql = self.struct_options(**struct_options)
        return f"""SELECT * FROM ML.GENERATE_EMBEDDING(MODEL {self._model_ref_sql()},
  ({source_sql}), {struct_options_sql})"""

    def ml_detect_anomalies(
        self, source_sql: str, struct_options: Mapping[str, Union[int, float]]
    ) -> str:
        """Encode ML.DETECT_ANOMALIES for BQML"""
        struct_options_sql = self.struct_options(**struct_options)
        return f"""SELECT * FROM ML.DETECT_ANOMALIES(MODEL {self._model_ref_sql()},
  {struct_options_sql}, ({source_sql}))"""

    # ML evaluation TVFs
    def ml_evaluate(self, source_sql: Optional[str] = None) -> str:
        """Encode ML.EVALUATE for BQML"""
        if source_sql is None:
            return f"""SELECT * FROM ML.EVALUATE(MODEL {self._model_ref_sql()})"""
        else:
            return f"""SELECT * FROM ML.EVALUATE(MODEL {self._model_ref_sql()},
  ({source_sql}))"""

    def ml_arima_coefficients(self) -> str:
        """Encode ML.ARIMA_COEFFICIENTS for BQML"""
        return f"""SELECT * FROM ML.ARIMA_COEFFICIENTS(MODEL {self._model_ref_sql()})"""

    # ML evaluation TVFs
    def ml_llm_evaluate(self, source_sql: str, task_type: Optional[str] = None) -> str:
        """Encode ML.EVALUATE for BQML"""
        # Note: don't need index as evaluate returns a new table
        return f"""SELECT * FROM ML.EVALUATE(MODEL {self._model_ref_sql()},
            ({source_sql}), STRUCT("{task_type}" AS task_type))"""

    # ML evaluation TVFs
    def ml_arima_evaluate(self, show_all_candidate_models: bool = False) -> str:
        """Encode ML.ARMIA_EVALUATE for BQML"""
        return f"""SELECT * FROM ML.ARIMA_EVALUATE(MODEL {self._model_ref_sql()},
            STRUCT({show_all_candidate_models} AS show_all_candidate_models))"""

    def ml_centroids(self) -> str:
        """Encode ML.CENTROIDS for BQML"""
        return f"""SELECT * FROM ML.CENTROIDS(MODEL {self._model_ref_sql()})"""

    def ml_principal_components(self) -> str:
        """Encode ML.PRINCIPAL_COMPONENTS for BQML"""
        return (
            f"""SELECT * FROM ML.PRINCIPAL_COMPONENTS(MODEL {self._model_ref_sql()})"""
        )

    def ml_principal_component_info(self) -> str:
        """Encode ML.PRINCIPAL_COMPONENT_INFO for BQML"""
        return f"""SELECT * FROM ML.PRINCIPAL_COMPONENT_INFO(MODEL {self._model_ref_sql()})"""

    # ML transform TVF, that require a transform_only type model
    def ml_transform(self, source_sql: str) -> str:
        """Encode ML.TRANSFORM for BQML"""
        return f"""SELECT * FROM ML.TRANSFORM(MODEL {self._model_ref_sql()},
  ({source_sql}))"""

    def ai_generate_table(
        self,
        source_sql: str,
        struct_options: Mapping[str, Union[int, float, bool, Mapping]],
    ) -> str:
        """Encode AI.GENERATE_TABLE for BQML"""
        struct_options_sql = self.struct_options(**struct_options)
        return f"""SELECT * FROM AI.GENERATE_TABLE(MODEL {self._model_ref_sql()},
  ({source_sql}), {struct_options_sql})"""
