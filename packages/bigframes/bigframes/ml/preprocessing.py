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
Scikit-Learn's preprocessing module: https://scikit-learn.org/stable/modules/preprocessing.html."""

from __future__ import annotations

import typing
from typing import Any, cast, List, Literal, Optional, Tuple, Union

from bigframes.core import log_adapter
from bigframes.ml import base, core, globals, utils
import bigframes.pandas as bpd
import third_party.bigframes_vendored.sklearn.preprocessing._data
import third_party.bigframes_vendored.sklearn.preprocessing._discretization
import third_party.bigframes_vendored.sklearn.preprocessing._encoder
import third_party.bigframes_vendored.sklearn.preprocessing._label


@log_adapter.class_logger
class StandardScaler(
    base.Transformer,
    third_party.bigframes_vendored.sklearn.preprocessing._data.StandardScaler,
):
    __doc__ = (
        third_party.bigframes_vendored.sklearn.preprocessing._data.StandardScaler.__doc__
    )

    def __init__(self):
        self._bqml_model: Optional[core.BqmlModel] = None
        self._bqml_model_factory = globals.bqml_model_factory()
        self._base_sql_generator = globals.base_sql_generator()

    # TODO(garrettwu): implement __hash__
    def __eq__(self, other: Any) -> bool:
        return type(other) is StandardScaler and self._bqml_model == other._bqml_model

    def _compile_to_sql(self, columns: List[str], X=None) -> List[Tuple[str, str]]:
        """Compile this transformer to a list of SQL expressions that can be included in
        a BQML TRANSFORM clause

        Args:
            columns:
                a list of column names to transform.
            X (default None):
                Ignored.

        Returns: a list of tuples of (sql_expression, output_name)"""
        return [
            (
                self._base_sql_generator.ml_standard_scaler(
                    column, f"standard_scaled_{column}"
                ),
                f"standard_scaled_{column}",
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
        return cls(), col_label

    def fit(
        self,
        X: Union[bpd.DataFrame, bpd.Series],
        y=None,  # ignored
    ) -> StandardScaler:
        (X,) = utils.convert_to_dataframe(X)

        compiled_transforms = self._compile_to_sql(X.columns.tolist())
        transform_sqls = [transform_sql for transform_sql, _ in compiled_transforms]

        self._bqml_model = self._bqml_model_factory.create_model(
            X,
            options={"model_type": "transform_only"},
            transforms=transform_sqls,
        )

        # The schema of TRANSFORM output is not available in the model API, so save it during fitting
        self._output_names = [name for _, name in compiled_transforms]
        return self

    def transform(self, X: Union[bpd.DataFrame, bpd.Series]) -> bpd.DataFrame:
        if not self._bqml_model:
            raise RuntimeError("Must be fitted before transform")

        (X,) = utils.convert_to_dataframe(X)

        df = self._bqml_model.transform(X)
        return typing.cast(
            bpd.DataFrame,
            df[self._output_names],
        )


@log_adapter.class_logger
class MaxAbsScaler(
    base.Transformer,
    third_party.bigframes_vendored.sklearn.preprocessing._data.MaxAbsScaler,
):
    __doc__ = (
        third_party.bigframes_vendored.sklearn.preprocessing._data.MaxAbsScaler.__doc__
    )

    def __init__(self):
        self._bqml_model: Optional[core.BqmlModel] = None
        self._bqml_model_factory = globals.bqml_model_factory()
        self._base_sql_generator = globals.base_sql_generator()

    # TODO(garrettwu): implement __hash__
    def __eq__(self, other: Any) -> bool:
        return type(other) is MaxAbsScaler and self._bqml_model == other._bqml_model

    def _compile_to_sql(self, columns: List[str], X=None) -> List[Tuple[str, str]]:
        """Compile this transformer to a list of SQL expressions that can be included in
        a BQML TRANSFORM clause

        Args:
            columns:
                a list of column names to transform.
            X (default None):
                Ignored.

        Returns: a list of tuples of (sql_expression, output_name)"""
        return [
            (
                self._base_sql_generator.ml_max_abs_scaler(
                    column, f"max_abs_scaled_{column}"
                ),
                f"max_abs_scaled_{column}",
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
        col_label = sql[sql.find("(") + 1 : sql.find(")")]
        return cls(), col_label

    def fit(
        self,
        X: Union[bpd.DataFrame, bpd.Series],
        y=None,  # ignored
    ) -> MaxAbsScaler:
        (X,) = utils.convert_to_dataframe(X)

        compiled_transforms = self._compile_to_sql(X.columns.tolist())
        transform_sqls = [transform_sql for transform_sql, _ in compiled_transforms]

        self._bqml_model = self._bqml_model_factory.create_model(
            X,
            options={"model_type": "transform_only"},
            transforms=transform_sqls,
        )

        # The schema of TRANSFORM output is not available in the model API, so save it during fitting
        self._output_names = [name for _, name in compiled_transforms]
        return self

    def transform(self, X: Union[bpd.DataFrame, bpd.Series]) -> bpd.DataFrame:
        if not self._bqml_model:
            raise RuntimeError("Must be fitted before transform")

        (X,) = utils.convert_to_dataframe(X)

        df = self._bqml_model.transform(X)
        return typing.cast(
            bpd.DataFrame,
            df[self._output_names],
        )


@log_adapter.class_logger
class MinMaxScaler(
    base.Transformer,
    third_party.bigframes_vendored.sklearn.preprocessing._data.MinMaxScaler,
):
    __doc__ = (
        third_party.bigframes_vendored.sklearn.preprocessing._data.MinMaxScaler.__doc__
    )

    def __init__(self):
        self._bqml_model: Optional[core.BqmlModel] = None
        self._bqml_model_factory = globals.bqml_model_factory()
        self._base_sql_generator = globals.base_sql_generator()

    # TODO(garrettwu): implement __hash__
    def __eq__(self, other: Any) -> bool:
        return type(other) is MinMaxScaler and self._bqml_model == other._bqml_model

    def _compile_to_sql(self, columns: List[str], X=None) -> List[Tuple[str, str]]:
        """Compile this transformer to a list of SQL expressions that can be included in
        a BQML TRANSFORM clause

        Args:
            columns:
                a list of column names to transform.
            X (default None):
                Ignored.

        Returns: a list of tuples of (sql_expression, output_name)"""
        return [
            (
                self._base_sql_generator.ml_min_max_scaler(
                    column, f"min_max_scaled_{column}"
                ),
                f"min_max_scaled_{column}",
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
        col_label = sql[sql.find("(") + 1 : sql.find(")")]
        return cls(), col_label

    def fit(
        self,
        X: Union[bpd.DataFrame, bpd.Series],
        y=None,  # ignored
    ) -> MinMaxScaler:
        (X,) = utils.convert_to_dataframe(X)

        compiled_transforms = self._compile_to_sql(X.columns.tolist())
        transform_sqls = [transform_sql for transform_sql, _ in compiled_transforms]

        self._bqml_model = self._bqml_model_factory.create_model(
            X,
            options={"model_type": "transform_only"},
            transforms=transform_sqls,
        )

        # The schema of TRANSFORM output is not available in the model API, so save it during fitting
        self._output_names = [name for _, name in compiled_transforms]
        return self

    def transform(self, X: Union[bpd.DataFrame, bpd.Series]) -> bpd.DataFrame:
        if not self._bqml_model:
            raise RuntimeError("Must be fitted before transform")

        (X,) = utils.convert_to_dataframe(X)

        df = self._bqml_model.transform(X)
        return typing.cast(
            bpd.DataFrame,
            df[self._output_names],
        )


@log_adapter.class_logger
class KBinsDiscretizer(
    base.Transformer,
    third_party.bigframes_vendored.sklearn.preprocessing._discretization.KBinsDiscretizer,
):
    __doc__ = (
        third_party.bigframes_vendored.sklearn.preprocessing._discretization.KBinsDiscretizer.__doc__
    )

    def __init__(
        self,
        n_bins: int = 5,
        strategy: Literal["uniform", "quantile"] = "quantile",
    ):
        if strategy != "uniform":
            raise NotImplementedError(
                f"Only strategy = 'uniform' is supported now, input is {strategy}."
            )
        if n_bins < 2:
            raise ValueError(
                f"n_bins has to be larger than or equal to 2, input is {n_bins}."
            )
        self.n_bins = n_bins
        self.strategy = strategy
        self._bqml_model: Optional[core.BqmlModel] = None
        self._bqml_model_factory = globals.bqml_model_factory()
        self._base_sql_generator = globals.base_sql_generator()

    # TODO(garrettwu): implement __hash__
    def __eq__(self, other: Any) -> bool:
        return (
            type(other) is KBinsDiscretizer
            and self.n_bins == other.n_bins
            and self._bqml_model == other._bqml_model
        )

    def _compile_to_sql(
        self,
        columns: List[str],
        X: bpd.DataFrame,
    ) -> List[Tuple[str, str]]:
        """Compile this transformer to a list of SQL expressions that can be included in
        a BQML TRANSFORM clause

        Args:
            columns:
                a list of column names to transform
            X:
                The Dataframe with training data.

        Returns: a list of tuples of (sql_expression, output_name)"""
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
            (
                self._base_sql_generator.ml_bucketize(
                    column, array_split_points[column], f"kbinsdiscretizer_{column}"
                ),
                f"kbinsdiscretizer_{column}",
            )
            for column in columns
        ]

    @classmethod
    def _parse_from_sql(cls, sql: str) -> tuple[KBinsDiscretizer, str]:
        """Parse SQL to tuple(KBinsDiscretizer, column_label).

        Args:
            sql: SQL string of format "ML.BUCKETIZE({col_label}, array_split_points, FALSE) OVER()"

        Returns:
            tuple(KBinsDiscretizer, column_label)"""
        s = sql[sql.find("(") + 1 : sql.find(")")]
        array_split_points = s[s.find("[") + 1 : s.find("]")]
        col_label = s[: s.find(",")]
        n_bins = array_split_points.count(",") + 2
        return cls(n_bins, "uniform"), col_label

    def fit(
        self,
        X: Union[bpd.DataFrame, bpd.Series],
        y=None,  # ignored
    ) -> KBinsDiscretizer:
        (X,) = utils.convert_to_dataframe(X)

        compiled_transforms = self._compile_to_sql(X.columns.tolist(), X)
        transform_sqls = [transform_sql for transform_sql, _ in compiled_transforms]

        self._bqml_model = self._bqml_model_factory.create_model(
            X,
            options={"model_type": "transform_only"},
            transforms=transform_sqls,
        )

        # The schema of TRANSFORM output is not available in the model API, so save it during fitting
        self._output_names = [name for _, name in compiled_transforms]
        return self

    def transform(self, X: Union[bpd.DataFrame, bpd.Series]) -> bpd.DataFrame:
        if not self._bqml_model:
            raise RuntimeError("Must be fitted before transform")

        (X,) = utils.convert_to_dataframe(X)

        df = self._bqml_model.transform(X)
        return typing.cast(
            bpd.DataFrame,
            df[self._output_names],
        )


@log_adapter.class_logger
class OneHotEncoder(
    base.Transformer,
    third_party.bigframes_vendored.sklearn.preprocessing._encoder.OneHotEncoder,
):
    # BQML max value https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-one-hot-encoder#syntax
    TOP_K_DEFAULT = 1000000
    FREQUENCY_THRESHOLD_DEFAULT = 0

    __doc__ = (
        third_party.bigframes_vendored.sklearn.preprocessing._encoder.OneHotEncoder.__doc__
    )

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

    # TODO(garrettwu): implement __hash__
    def __eq__(self, other: Any) -> bool:
        return (
            type(other) is OneHotEncoder
            and self._bqml_model == other._bqml_model
            and self.drop == other.drop
            and self.min_frequency == other.min_frequency
            and self.max_categories == other.max_categories
        )

    def _compile_to_sql(self, columns: List[str], X=None) -> List[Tuple[str, str]]:
        """Compile this transformer to a list of SQL expressions that can be included in
        a BQML TRANSFORM clause

        Args:
            columns:
                a list of column names to transform.
            X (default None):
                Ignored.

        Returns: a list of tuples of (sql_expression, output_name)"""

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
            (
                self._base_sql_generator.ml_one_hot_encoder(
                    column, drop, top_k, frequency_threshold, f"onehotencoded_{column}"
                ),
                f"onehotencoded_{column}",
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

        return cls(drop, min_frequency, max_categories), col_label

    def fit(
        self,
        X: Union[bpd.DataFrame, bpd.Series],
        y=None,  # ignored
    ) -> OneHotEncoder:
        (X,) = utils.convert_to_dataframe(X)

        compiled_transforms = self._compile_to_sql(X.columns.tolist())
        transform_sqls = [transform_sql for transform_sql, _ in compiled_transforms]

        self._bqml_model = self._bqml_model_factory.create_model(
            X,
            options={"model_type": "transform_only"},
            transforms=transform_sqls,
        )

        # The schema of TRANSFORM output is not available in the model API, so save it during fitting
        self._output_names = [name for _, name in compiled_transforms]
        return self

    def transform(self, X: Union[bpd.DataFrame, bpd.Series]) -> bpd.DataFrame:
        if not self._bqml_model:
            raise RuntimeError("Must be fitted before transform")

        (X,) = utils.convert_to_dataframe(X)

        df = self._bqml_model.transform(X)
        return typing.cast(
            bpd.DataFrame,
            df[self._output_names],
        )


@log_adapter.class_logger
class LabelEncoder(
    base.LabelTransformer,
    third_party.bigframes_vendored.sklearn.preprocessing._label.LabelEncoder,
):
    # BQML max value https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-one-hot-encoder#syntax
    TOP_K_DEFAULT = 1000000
    FREQUENCY_THRESHOLD_DEFAULT = 0

    __doc__ = (
        third_party.bigframes_vendored.sklearn.preprocessing._label.LabelEncoder.__doc__
    )

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

    # TODO(garrettwu): implement __hash__
    def __eq__(self, other: Any) -> bool:
        return (
            type(other) is LabelEncoder
            and self._bqml_model == other._bqml_model
            and self.min_frequency == other.min_frequency
            and self.max_categories == other.max_categories
        )

    def _compile_to_sql(self, columns: List[str], X=None) -> List[Tuple[str, str]]:
        """Compile this transformer to a list of SQL expressions that can be included in
        a BQML TRANSFORM clause

        Args:
            columns:
                a list of column names to transform.
            X (default None):
                Ignored.

        Returns: a list of tuples of (sql_expression, output_name)"""

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
            (
                self._base_sql_generator.ml_label_encoder(
                    column, top_k, frequency_threshold, f"labelencoded_{column}"
                ),
                f"labelencoded_{column}",
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

        return cls(min_frequency, max_categories), col_label

    def fit(
        self,
        y: Union[bpd.DataFrame, bpd.Series],
    ) -> LabelEncoder:
        (y,) = utils.convert_to_dataframe(y)

        compiled_transforms = self._compile_to_sql(y.columns.tolist())
        transform_sqls = [transform_sql for transform_sql, _ in compiled_transforms]

        self._bqml_model = self._bqml_model_factory.create_model(
            y,
            options={"model_type": "transform_only"},
            transforms=transform_sqls,
        )

        # The schema of TRANSFORM output is not available in the model API, so save it during fitting
        self._output_names = [name for _, name in compiled_transforms]
        return self

    def transform(self, y: Union[bpd.DataFrame, bpd.Series]) -> bpd.DataFrame:
        if not self._bqml_model:
            raise RuntimeError("Must be fitted before transform")

        (y,) = utils.convert_to_dataframe(y)

        df = self._bqml_model.transform(y)
        return typing.cast(
            bpd.DataFrame,
            df[self._output_names],
        )
