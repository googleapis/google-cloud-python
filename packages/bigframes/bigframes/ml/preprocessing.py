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

"""Transformers that prepare data for other estimators. This module is styled after
scikit-learn's preprocessing module: https://scikit-learn.org/stable/modules/preprocessing.html."""

from __future__ import annotations

import typing
from typing import cast, Iterable, List, Literal, Optional, Union

import bigframes_vendored.sklearn.preprocessing._data
import bigframes_vendored.sklearn.preprocessing._discretization
import bigframes_vendored.sklearn.preprocessing._encoder
import bigframes_vendored.sklearn.preprocessing._label
import bigframes_vendored.sklearn.preprocessing._polynomial

from bigframes.core import log_adapter
from bigframes.ml import base, core, globals, utils
import bigframes.pandas as bpd


@log_adapter.class_logger
class StandardScaler(
    base.Transformer,
    bigframes_vendored.sklearn.preprocessing._data.StandardScaler,
):
    __doc__ = bigframes_vendored.sklearn.preprocessing._data.StandardScaler.__doc__

    def __init__(self):
        self._bqml_model: Optional[core.BqmlModel] = None
        self._bqml_model_factory = globals.bqml_model_factory()
        self._base_sql_generator = globals.base_sql_generator()

    def _keys(self):
        return (self._bqml_model,)

    def _compile_to_sql(
        self, X: bpd.DataFrame, columns: Optional[Iterable[str]] = None
    ) -> List[str]:
        """Compile this transformer to a list of SQL expressions that can be included in
        a BQML TRANSFORM clause

        Args:
            X: DataFrame to transform.
            columns: transform columns. If None, transform all columns in X.

        Returns: a list of tuples sql_expr."""
        if columns is None:
            columns = X.columns
        return [
            self._base_sql_generator.ml_standard_scaler(
                column, f"standard_scaled_{column}"
            )
            for column in columns
        ]

    @classmethod
    def _parse_from_sql(cls, sql: str) -> tuple[StandardScaler, str]:
        """Parse SQL to tuple(StandardScaler, column_label).

        Args:
            sql: SQL string of format "ML.STANDARD_SCALER({col_label}) OVER()"

        Returns:
            tuple(StandardScaler, column_label)"""
        col_label = sql[sql.find("(") + 1 : sql.find(")")]
        return cls(), _unescape_id(col_label)

    def fit(
        self,
        X: utils.ArrayType,
        y=None,  # ignored
    ) -> StandardScaler:
        (X,) = utils.batch_convert_to_dataframe(X)

        transform_sqls = self._compile_to_sql(X)
        self._bqml_model = self._bqml_model_factory.create_model(
            X,
            options={"model_type": "transform_only"},
            transforms=transform_sqls,
        )

        self._extract_output_names()
        return self

    def transform(self, X: utils.ArrayType) -> bpd.DataFrame:
        if not self._bqml_model:
            raise RuntimeError("Must be fitted before transform")

        (X,) = utils.batch_convert_to_dataframe(X, session=self._bqml_model.session)

        df = self._bqml_model.transform(X)
        return typing.cast(
            bpd.DataFrame,
            df[self._output_names],
        )


@log_adapter.class_logger
class MaxAbsScaler(
    base.Transformer,
    bigframes_vendored.sklearn.preprocessing._data.MaxAbsScaler,
):
    __doc__ = bigframes_vendored.sklearn.preprocessing._data.MaxAbsScaler.__doc__

    def __init__(self):
        self._bqml_model: Optional[core.BqmlModel] = None
        self._bqml_model_factory = globals.bqml_model_factory()
        self._base_sql_generator = globals.base_sql_generator()

    def _keys(self):
        return (self._bqml_model,)

    def _compile_to_sql(
        self, X: bpd.DataFrame, columns: Optional[Iterable[str]] = None
    ) -> List[str]:
        """Compile this transformer to a list of SQL expressions that can be included in
        a BQML TRANSFORM clause

        Args:
            X: DataFrame to transform.
            columns: transform columns. If None, transform all columns in X.

        Returns: a list of tuples sql_expr."""
        if columns is None:
            columns = X.columns
        return [
            self._base_sql_generator.ml_max_abs_scaler(
                column, f"max_abs_scaled_{column}"
            )
            for column in columns
        ]

    @classmethod
    def _parse_from_sql(cls, sql: str) -> tuple[MaxAbsScaler, str]:
        """Parse SQL to tuple(MaxAbsScaler, column_label).

        Args:
            sql: SQL string of format "ML.MAX_ABS_SCALER({col_label}) OVER()"

        Returns:
            tuple(MaxAbsScaler, column_label)"""
        # TODO: Use real sql parser
        col_label = sql[sql.find("(") + 1 : sql.find(")")]
        return cls(), _unescape_id(col_label)

    def fit(
        self,
        X: utils.ArrayType,
        y=None,  # ignored
    ) -> MaxAbsScaler:
        (X,) = utils.batch_convert_to_dataframe(X)

        transform_sqls = self._compile_to_sql(X)
        self._bqml_model = self._bqml_model_factory.create_model(
            X,
            options={"model_type": "transform_only"},
            transforms=transform_sqls,
        )

        self._extract_output_names()
        return self

    def transform(self, X: utils.ArrayType) -> bpd.DataFrame:
        if not self._bqml_model:
            raise RuntimeError("Must be fitted before transform")

        (X,) = utils.batch_convert_to_dataframe(X, session=self._bqml_model.session)

        df = self._bqml_model.transform(X)
        return typing.cast(
            bpd.DataFrame,
            df[self._output_names],
        )


@log_adapter.class_logger
class MinMaxScaler(
    base.Transformer,
    bigframes_vendored.sklearn.preprocessing._data.MinMaxScaler,
):
    __doc__ = bigframes_vendored.sklearn.preprocessing._data.MinMaxScaler.__doc__

    def __init__(self):
        self._bqml_model: Optional[core.BqmlModel] = None
        self._bqml_model_factory = globals.bqml_model_factory()
        self._base_sql_generator = globals.base_sql_generator()

    def _keys(self):
        return (self._bqml_model,)

    def _compile_to_sql(
        self, X: bpd.DataFrame, columns: Optional[Iterable[str]] = None
    ) -> List[str]:
        """Compile this transformer to a list of SQL expressions that can be included in
        a BQML TRANSFORM clause

        Args:
            X: DataFrame to transform.
            columns: transform columns. If None, transform all columns in X.

        Returns: a list of tuples sql_expr."""
        if columns is None:
            columns = X.columns
        return [
            self._base_sql_generator.ml_min_max_scaler(
                column, f"min_max_scaled_{column}"
            )
            for column in columns
        ]

    @classmethod
    def _parse_from_sql(cls, sql: str) -> tuple[MinMaxScaler, str]:
        """Parse SQL to tuple(MinMaxScaler, column_label).

        Args:
            sql: SQL string of format "ML.MIN_MAX_SCALER({col_label}) OVER()"

        Returns:
            tuple(MinMaxScaler, column_label)"""
        # TODO: Use real sql parser
        col_label = sql[sql.find("(") + 1 : sql.find(")")]
        return cls(), _unescape_id(col_label)

    def fit(
        self,
        X: utils.ArrayType,
        y=None,  # ignored
    ) -> MinMaxScaler:
        (X,) = utils.batch_convert_to_dataframe(X)

        transform_sqls = self._compile_to_sql(X)
        self._bqml_model = self._bqml_model_factory.create_model(
            X,
            options={"model_type": "transform_only"},
            transforms=transform_sqls,
        )

        self._extract_output_names()
        return self

    def transform(self, X: utils.ArrayType) -> bpd.DataFrame:
        if not self._bqml_model:
            raise RuntimeError("Must be fitted before transform")

        (X,) = utils.batch_convert_to_dataframe(X, session=self._bqml_model.session)

        df = self._bqml_model.transform(X)
        return typing.cast(
            bpd.DataFrame,
            df[self._output_names],
        )


@log_adapter.class_logger
class KBinsDiscretizer(
    base.Transformer,
    bigframes_vendored.sklearn.preprocessing._discretization.KBinsDiscretizer,
):
    __doc__ = (
        bigframes_vendored.sklearn.preprocessing._discretization.KBinsDiscretizer.__doc__
    )

    def __init__(
        self,
        n_bins: int = 5,
        strategy: Literal["uniform", "quantile"] = "quantile",
    ):
        if n_bins < 2:
            raise ValueError(
                f"n_bins has to be larger than or equal to 2, input is {n_bins}."
            )
        self.n_bins = n_bins
        self.strategy = strategy
        self._bqml_model: Optional[core.BqmlModel] = None
        self._bqml_model_factory = globals.bqml_model_factory()
        self._base_sql_generator = globals.base_sql_generator()

    def _keys(self):
        return (self._bqml_model, self.n_bins, self.strategy)

    def _compile_to_sql(
        self, X: bpd.DataFrame, columns: Optional[Iterable[str]] = None
    ) -> List[str]:
        """Compile this transformer to a list of SQL expressions that can be included in
        a BQML TRANSFORM clause

        Args:
            X: DataFrame to transform.
            columns: transform columns. If None, transform all columns in X.

        Returns: a list of tuples sql_expr."""
        if columns is None:
            columns = X.columns
        array_split_points = {}
        if self.strategy == "uniform":
            for column in columns:
                min_value = X[column].min()
                max_value = X[column].max()

                bin_size = (max_value - min_value) / self.n_bins
                array_split_points[column] = [
                    min_value + i * bin_size for i in range(self.n_bins - 1)
                ]

            return [
                self._base_sql_generator.ml_bucketize(
                    column, array_split_points[column], f"kbinsdiscretizer_{column}"
                )
                for column in columns
            ]

        elif self.strategy == "quantile":

            return [
                self._base_sql_generator.ml_quantile_bucketize(
                    column, self.n_bins, f"kbinsdiscretizer_{column}"
                )
                for column in columns
            ]

        else:
            raise ValueError(
                f"strategy should be set 'quantile' or 'uniform', but your input is {self.strategy}."
            )

    @classmethod
    def _parse_from_sql(cls, sql: str) -> tuple[KBinsDiscretizer, str]:
        """Parse SQL to tuple(KBinsDiscretizer, column_label).

        Args:
            sql: SQL string of format "ML.BUCKETIZE({col_label}, array_split_points, FALSE)"
                or ML.QUANTILE_BUCKETIZE({col_label}, num_bucket) OVER()"

        Returns:
            tuple(KBinsDiscretizer, column_label)"""
        s = sql[sql.find("(") + 1 : sql.find(")")]
        col_label = s[: s.find(",")]

        if sql.startswith("ML.QUANTILE_BUCKETIZE"):
            num_bins = s.split(",")[1]
            return cls(int(num_bins), "quantile"), _unescape_id(col_label)
        else:
            array_split_points = s[s.find("[") + 1 : s.find("]")]
            n_bins = array_split_points.count(",") + 2
            return cls(n_bins, "uniform"), _unescape_id(col_label)

    def fit(
        self,
        X: utils.ArrayType,
        y=None,  # ignored
    ) -> KBinsDiscretizer:
        (X,) = utils.batch_convert_to_dataframe(X)

        transform_sqls = self._compile_to_sql(X)
        self._bqml_model = self._bqml_model_factory.create_model(
            X,
            options={"model_type": "transform_only"},
            transforms=transform_sqls,
        )

        self._extract_output_names()
        return self

    def transform(self, X: utils.ArrayType) -> bpd.DataFrame:
        if not self._bqml_model:
            raise RuntimeError("Must be fitted before transform")

        (X,) = utils.batch_convert_to_dataframe(X, session=self._bqml_model.session)

        df = self._bqml_model.transform(X)
        return typing.cast(
            bpd.DataFrame,
            df[self._output_names],
        )


@log_adapter.class_logger
class OneHotEncoder(
    base.Transformer,
    bigframes_vendored.sklearn.preprocessing._encoder.OneHotEncoder,
):
    # BQML max value https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-one-hot-encoder#syntax
    TOP_K_DEFAULT = 1000000
    FREQUENCY_THRESHOLD_DEFAULT = 0

    __doc__ = bigframes_vendored.sklearn.preprocessing._encoder.OneHotEncoder.__doc__

    # All estimators must implement __init__ to document their parameters, even
    # if they don't have any
    def __init__(
        self,
        drop: Optional[Literal["most_frequent"]] = None,
        min_frequency: Optional[int] = None,
        max_categories: Optional[int] = None,
    ):
        if max_categories is not None and max_categories < 2:
            raise ValueError(
                f"max_categories has to be larger than or equal to 2, input is {max_categories}."
            )
        self.drop = drop
        self.min_frequency = min_frequency
        self.max_categories = max_categories
        self._bqml_model: Optional[core.BqmlModel] = None
        self._bqml_model_factory = globals.bqml_model_factory()
        self._base_sql_generator = globals.base_sql_generator()

    def _keys(self):
        return (self._bqml_model, self.drop, self.min_frequency, self.max_categories)

    def _compile_to_sql(
        self, X: bpd.DataFrame, columns: Optional[Iterable[str]] = None
    ) -> List[str]:
        """Compile this transformer to a list of SQL expressions that can be included in
        a BQML TRANSFORM clause

        Args:
            X: DataFrame to transform.
            columns: transform columns. If None, transform all columns in X.

        Returns: a list of tuples sql_expr."""
        if columns is None:
            columns = X.columns
        drop = self.drop if self.drop is not None else "none"
        # minus one here since BQML's inplimentation always includes index 0, and top_k is on top of that.
        top_k = (
            (self.max_categories - 1)
            if self.max_categories is not None
            else OneHotEncoder.TOP_K_DEFAULT
        )
        frequency_threshold = (
            self.min_frequency
            if self.min_frequency is not None
            else OneHotEncoder.FREQUENCY_THRESHOLD_DEFAULT
        )
        return [
            self._base_sql_generator.ml_one_hot_encoder(
                column, drop, top_k, frequency_threshold, f"onehotencoded_{column}"
            )
            for column in columns
        ]

    @classmethod
    def _parse_from_sql(cls, sql: str) -> tuple[OneHotEncoder, str]:
        """Parse SQL to tuple(OneHotEncoder, column_label).

        Args:
            sql: SQL string of format "ML.ONE_HOT_ENCODER({col_label}, '{drop}', {top_k}, {frequency_threshold}) OVER() "

        Returns:
            tuple(OneHotEncoder, column_label)"""
        s = sql[sql.find("(") + 1 : sql.find(")")]
        col_label, drop_str, top_k, frequency_threshold = s.split(", ")
        drop = (
            cast(Literal["most_frequent"], "most_frequent")
            if drop_str.lower() == "'most_frequent'"
            else None
        )
        max_categories = int(top_k) + 1
        min_frequency = int(frequency_threshold)

        return cls(drop, min_frequency, max_categories), _unescape_id(col_label)

    def fit(
        self,
        X: utils.ArrayType,
        y=None,  # ignored
    ) -> OneHotEncoder:
        (X,) = utils.batch_convert_to_dataframe(X)

        transform_sqls = self._compile_to_sql(X)
        self._bqml_model = self._bqml_model_factory.create_model(
            X,
            options={"model_type": "transform_only"},
            transforms=transform_sqls,
        )

        self._extract_output_names()
        return self

    def transform(self, X: utils.ArrayType) -> bpd.DataFrame:
        if not self._bqml_model:
            raise RuntimeError("Must be fitted before transform")

        (X,) = utils.batch_convert_to_dataframe(X, session=self._bqml_model.session)

        df = self._bqml_model.transform(X)
        return typing.cast(
            bpd.DataFrame,
            df[self._output_names],
        )


@log_adapter.class_logger
class LabelEncoder(
    base.LabelTransformer,
    bigframes_vendored.sklearn.preprocessing._label.LabelEncoder,
):
    # BQML max value https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-one-hot-encoder#syntax
    TOP_K_DEFAULT = 1000000
    FREQUENCY_THRESHOLD_DEFAULT = 0

    __doc__ = bigframes_vendored.sklearn.preprocessing._label.LabelEncoder.__doc__

    # All estimators must implement __init__ to document their parameters, even
    # if they don't have any
    def __init__(
        self,
        min_frequency: Optional[int] = None,
        max_categories: Optional[int] = None,
    ):
        if max_categories is not None and max_categories < 2:
            raise ValueError(
                f"max_categories has to be larger than or equal to 2, input is {max_categories}."
            )
        self.min_frequency = min_frequency
        self.max_categories = max_categories
        self._bqml_model: Optional[core.BqmlModel] = None
        self._bqml_model_factory = globals.bqml_model_factory()
        self._base_sql_generator = globals.base_sql_generator()

    def _keys(self):
        return (self._bqml_model, self.min_frequency, self.max_categories)

    def _compile_to_sql(
        self, X: bpd.DataFrame, columns: Optional[Iterable[str]] = None
    ) -> List[str]:
        """Compile this transformer to a list of SQL expressions that can be included in
        a BQML TRANSFORM clause

        Args:
            X: DataFrame to transform.
            columns: transform columns. If None, transform all columns in X.

        Returns: a list of tuples sql_expr."""
        if columns is None:
            columns = X.columns

        # minus one here since BQML's inplimentation always includes index 0, and top_k is on top of that.
        top_k = (
            (self.max_categories - 1)
            if self.max_categories is not None
            else LabelEncoder.TOP_K_DEFAULT
        )
        frequency_threshold = (
            self.min_frequency
            if self.min_frequency is not None
            else LabelEncoder.FREQUENCY_THRESHOLD_DEFAULT
        )
        return [
            self._base_sql_generator.ml_label_encoder(
                column, top_k, frequency_threshold, f"labelencoded_{column}"
            )
            for column in columns
        ]

    @classmethod
    def _parse_from_sql(cls, sql: str) -> tuple[LabelEncoder, str]:
        """Parse SQL to tuple(LabelEncoder, column_label).

        Args:
            sql: SQL string of format "ML.LabelEncoder({col_label}, {top_k}, {frequency_threshold}) OVER() "

        Returns:
            tuple(LabelEncoder, column_label)"""
        s = sql[sql.find("(") + 1 : sql.find(")")]
        col_label, top_k, frequency_threshold = s.split(", ")
        max_categories = int(top_k) + 1
        min_frequency = int(frequency_threshold)

        return cls(min_frequency, max_categories), _unescape_id(col_label)

    def fit(
        self,
        y: utils.ArrayType,
    ) -> LabelEncoder:
        (y,) = utils.batch_convert_to_dataframe(y)

        transform_sqls = self._compile_to_sql(y)
        self._bqml_model = self._bqml_model_factory.create_model(
            y,
            options={"model_type": "transform_only"},
            transforms=transform_sqls,
        )

        self._extract_output_names()
        return self

    def transform(self, y: utils.ArrayType) -> bpd.DataFrame:
        if not self._bqml_model:
            raise RuntimeError("Must be fitted before transform")

        (y,) = utils.batch_convert_to_dataframe(y, session=self._bqml_model.session)

        df = self._bqml_model.transform(y)
        return typing.cast(
            bpd.DataFrame,
            df[self._output_names],
        )


@log_adapter.class_logger
class PolynomialFeatures(
    base.Transformer,
    bigframes_vendored.sklearn.preprocessing._polynomial.PolynomialFeatures,
):
    __doc__ = (
        bigframes_vendored.sklearn.preprocessing._polynomial.PolynomialFeatures.__doc__
    )

    def __init__(self, degree: int = 2):
        if degree not in range(1, 5):
            raise ValueError(f"degree has to be [1, 4], input is {degree}.")
        self.degree = degree
        self._bqml_model: Optional[core.BqmlModel] = None
        self._bqml_model_factory = globals.bqml_model_factory()
        self._base_sql_generator = globals.base_sql_generator()

    def _keys(self):
        return (self._bqml_model, self.degree)

    def _compile_to_sql(
        self, X: bpd.DataFrame, columns: Optional[Iterable[str]] = None
    ) -> List[str]:
        """Compile this transformer to a list of SQL expressions that can be included in
        a BQML TRANSFORM clause

        Args:
            X: DataFrame to transform.
            columns: transform columns. If None, transform all columns in X.

        Returns: a list of tuples sql_expr."""
        if columns is None:
            columns = X.columns
        output_name = "poly_feat"
        return [
            self._base_sql_generator.ml_polynomial_expand(
                columns, self.degree, output_name
            )
        ]

    @classmethod
    def _parse_from_sql(cls, sql: str) -> tuple[PolynomialFeatures, tuple[str, ...]]:
        """Parse SQL to tuple(PolynomialFeatures, column_labels).

        Args:
            sql: SQL string of format "ML.POLYNOMIAL_EXPAND(STRUCT(col_label0, col_label1, ...), degree)"

        Returns:
            tuple(MaxAbsScaler, column_label)"""
        col_labels = sql[sql.find("STRUCT(") + 7 : sql.find(")")].split(",")
        col_labels = [label.strip() for label in col_labels]
        degree = int(sql[sql.rfind(",") + 1 : sql.rfind(")")])
        return cls(degree), tuple(map(_unescape_id, col_labels))

    def fit(
        self,
        X: utils.ArrayType,
        y=None,  # ignored
    ) -> PolynomialFeatures:
        (X,) = utils.batch_convert_to_dataframe(X)

        transform_sqls = self._compile_to_sql(X)
        self._bqml_model = self._bqml_model_factory.create_model(
            X,
            options={"model_type": "transform_only"},
            transforms=transform_sqls,
        )

        self._extract_output_names()

        return self

    def transform(self, X: utils.ArrayType) -> bpd.DataFrame:
        if not self._bqml_model:
            raise RuntimeError("Must be fitted before transform")

        (X,) = utils.batch_convert_to_dataframe(X, session=self._bqml_model.session)

        df = self._bqml_model.transform(X)
        return typing.cast(
            bpd.DataFrame,
            df[self._output_names],
        )


def _unescape_id(id: str) -> str:
    """Very simple conversion to removed ` characters from ids.

    A proper sql parser should be used instead.
    """
    return id.removeprefix("`").removesuffix("`")


PreprocessingType = Union[
    OneHotEncoder,
    StandardScaler,
    MaxAbsScaler,
    MinMaxScaler,
    KBinsDiscretizer,
    LabelEncoder,
    PolynomialFeatures,
]
