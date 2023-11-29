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

from typing import Iterable, Mapping, Optional, Union

import google.cloud.bigquery

import bigframes.constants as constants
import bigframes.pandas as bpd


class BaseSqlGenerator:
    """Generate base SQL strings for ML. Model name isn't needed in this class."""

    # General methods
    def encode_value(self, v: Union[str, int, float, Iterable[str]]) -> str:
        """Encode a parameter value for SQL"""
        if isinstance(v, str):
            return f'"{v}"'
        elif isinstance(v, int) or isinstance(v, float):
            return f"{v}"
        elif isinstance(v, Iterable):
            inner = ", ".join([self.encode_value(x) for x in v])
            return f"[{inner}]"
        else:
            raise ValueError(f"Unexpected value type. {constants.FEEDBACK_LINK}")

    def build_parameters(self, **kwargs: Union[str, int, float, Iterable[str]]) -> str:
        """Encode a dict of values into a formatted Iterable of key-value pairs for SQL"""
        indent_str = "  "
        param_strs = [f"{k}={self.encode_value(v)}" for k, v in kwargs.items()]
        return "\n" + indent_str + f",\n{indent_str}".join(param_strs)

    def build_structs(self, **kwargs: Union[int, float]) -> str:
        """Encode a dict of values into a formatted STRUCT items for SQL"""
        indent_str = "  "
        param_strs = [f"{v} AS {k}" for k, v in kwargs.items()]
        return "\n" + indent_str + f",\n{indent_str}".join(param_strs)

    def build_expressions(self, *expr_sqls: str) -> str:
        """Encode a Iterable of SQL expressions into a formatted Iterable for SQL"""
        indent_str = "  "
        return "\n" + indent_str + f",\n{indent_str}".join(expr_sqls)

    def build_schema(self, **kwargs: str) -> str:
        """Encode a dict of values into a formatted schema type items for SQL"""
        indent_str = "  "
        param_strs = [f"{k} {v}" for k, v in kwargs.items()]
        return "\n" + indent_str + f",\n{indent_str}".join(param_strs)

    def options(self, **kwargs: Union[str, int, float, Iterable[str]]) -> str:
        """Encode the OPTIONS clause for BQML"""
        return f"OPTIONS({self.build_parameters(**kwargs)})"

    def struct_options(self, **kwargs: Union[int, float]) -> str:
        """Encode a BQ STRUCT as options."""
        return f"STRUCT({self.build_structs(**kwargs)})"

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
        return f"""ML.STANDARD_SCALER({numeric_expr_sql}) OVER() AS {name}"""

    def ml_max_abs_scaler(self, numeric_expr_sql: str, name: str) -> str:
        """Encode ML.MAX_ABS_SCALER for BQML"""
        return f"""ML.MAX_ABS_SCALER({numeric_expr_sql}) OVER() AS {name}"""

    def ml_min_max_scaler(self, numeric_expr_sql: str, name: str) -> str:
        """Encode ML.MIN_MAX_SCALER for BQML"""
        return f"""ML.MIN_MAX_SCALER({numeric_expr_sql}) OVER() AS {name}"""

    def ml_bucketize(
        self,
        numeric_expr_sql: str,
        array_split_points: Iterable[Union[int, float]],
        name: str,
    ) -> str:
        """Encode ML.MIN_MAX_SCALER for BQML"""
        return f"""ML.BUCKETIZE({numeric_expr_sql}, {array_split_points}, FALSE) AS {name}"""

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
        return f"""ML.ONE_HOT_ENCODER({numeric_expr_sql}, '{drop}', {top_k}, {frequency_threshold}) OVER() AS {name}"""

    def ml_label_encoder(
        self,
        numeric_expr_sql: str,
        top_k: int,
        frequency_threshold: int,
        name: str,
    ) -> str:
        """Encode ML.LABEL_ENCODER for BQML.
        https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-label-encoder for params."""
        return f"""ML.LABEL_ENCODER({numeric_expr_sql}, {top_k}, {frequency_threshold}) OVER() AS {name}"""


class ModelCreationSqlGenerator(BaseSqlGenerator):
    """Sql generator for creating a model entity. Model id is the standalone id without project id and dataset id."""

    def _model_id_sql(
        self,
        model_ref: google.cloud.bigquery.ModelReference,
    ):
        return f"`{model_ref.project}`.`{model_ref.dataset_id}`.`{model_ref.model_id}`"

    # Model create and alter
    def create_model(
        self,
        source_df: bpd.DataFrame,
        model_ref: google.cloud.bigquery.ModelReference,
        options: Mapping[str, Union[str, int, float, Iterable[str]]] = {},
        transforms: Optional[Iterable[str]] = None,
    ) -> str:
        """Encode the CREATE OR REPLACE MODEL statement for BQML"""
        source_sql = source_df.sql
        transform_sql = self.transform(*transforms) if transforms is not None else None
        options_sql = self.options(**options)

        parts = [f"CREATE OR REPLACE MODEL {self._model_id_sql(model_ref)}"]
        if transform_sql:
            parts.append(transform_sql)
        if options_sql:
            parts.append(options_sql)
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
        options_sql = self.options(**options)

        parts = [f"CREATE OR REPLACE MODEL {self._model_id_sql(model_ref)}"]
        if options_sql:
            parts.append(options_sql)
        return "\n".join(parts)


class ModelManipulationSqlGenerator(BaseSqlGenerator):
    """Sql generator for manipulating a model entity. Model name is the full model path of project_id.dataset_id.model_id."""

    def __init__(self, model_name: str):
        self._model_name = model_name

    def _source_sql(self, source_df: bpd.DataFrame) -> str:
        """Return DataFrame sql with index columns."""
        _source_sql, _, _ = source_df._to_sql_query(include_index=True)
        return _source_sql

    # Alter model
    def alter_model(
        self,
        options: Mapping[str, Union[str, int, float, Iterable[str]]] = {},
    ) -> str:
        """Encode the ALTER MODEL statement for BQML"""
        options_sql = self.options(**options)

        parts = [f"ALTER MODEL `{self._model_name}`"]
        parts.append(f"SET {options_sql}")
        return "\n".join(parts)

    # ML prediction TVFs
    def ml_predict(self, source_df: bpd.DataFrame) -> str:
        """Encode ML.PREDICT for BQML"""
        return f"""SELECT * FROM ML.PREDICT(MODEL `{self._model_name}`,
  ({self._source_sql(source_df)}))"""

    def ml_forecast(self) -> str:
        """Encode ML.FORECAST for BQML"""
        return f"""SELECT * FROM ML.FORECAST(MODEL `{self._model_name}`)"""

    def ml_generate_text(
        self, source_df: bpd.DataFrame, struct_options: Mapping[str, Union[int, float]]
    ) -> str:
        """Encode ML.GENERATE_TEXT for BQML"""
        struct_options_sql = self.struct_options(**struct_options)
        return f"""SELECT * FROM ML.GENERATE_TEXT(MODEL `{self._model_name}`,
  ({self._source_sql(source_df)}), {struct_options_sql})"""

    def ml_generate_text_embedding(
        self, source_df: bpd.DataFrame, struct_options: Mapping[str, Union[int, float]]
    ) -> str:
        """Encode ML.GENERATE_TEXT_EMBEDDING for BQML"""
        struct_options_sql = self.struct_options(**struct_options)
        return f"""SELECT * FROM ML.GENERATE_TEXT_EMBEDDING(MODEL `{self._model_name}`,
  ({self._source_sql(source_df)}), {struct_options_sql})"""

    # ML evaluation TVFs
    def ml_evaluate(self, source_df: Optional[bpd.DataFrame] = None) -> str:
        """Encode ML.EVALUATE for BQML"""
        if source_df is None:
            source_sql = None
        else:
            # Note: don't need index as evaluate returns a new table
            source_sql, _, _ = source_df._to_sql_query(include_index=False)

        if source_sql is None:
            return f"""SELECT * FROM ML.EVALUATE(MODEL `{self._model_name}`)"""
        else:
            return f"""SELECT * FROM ML.EVALUATE(MODEL `{self._model_name}`,
  ({source_sql}))"""

    def ml_centroids(self) -> str:
        """Encode ML.CENTROIDS for BQML"""
        return f"""SELECT * FROM ML.CENTROIDS(MODEL `{self._model_name}`)"""

    def ml_principal_components(self) -> str:
        """Encode ML.PRINCIPAL_COMPONENTS for BQML"""
        return f"""SELECT * FROM ML.PRINCIPAL_COMPONENTS(MODEL `{self._model_name}`)"""

    def ml_principal_component_info(self) -> str:
        """Encode ML.PRINCIPAL_COMPONENT_INFO for BQML"""
        return (
            f"""SELECT * FROM ML.PRINCIPAL_COMPONENT_INFO(MODEL `{self._model_name}`)"""
        )

    # ML transform TVF, that require a transform_only type model
    def ml_transform(self, source_df: bpd.DataFrame) -> str:
        """Encode ML.TRANSFORM for BQML"""
        return f"""SELECT * FROM ML.TRANSFORM(MODEL `{self._model_name}`,
  ({self._source_sql(source_df)}))"""
