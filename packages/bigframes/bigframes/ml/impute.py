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

"""Transformers for missing value imputation. This module is styled after
scikit-learn's preprocessing module: https://scikit-learn.org/stable/modules/impute.html."""

from __future__ import annotations

import typing
from typing import Iterable, List, Literal, Optional

import bigframes_vendored.sklearn.impute._base

from bigframes.core import log_adapter
from bigframes.ml import base, core, globals, utils
import bigframes.pandas as bpd


@log_adapter.class_logger
class SimpleImputer(
    base.Transformer,
    bigframes_vendored.sklearn.impute._base.SimpleImputer,
):

    __doc__ = bigframes_vendored.sklearn.impute._base.SimpleImputer.__doc__

    def __init__(
        self,
        strategy: Literal["mean", "median", "most_frequent"] = "mean",
    ):
        self.strategy = strategy
        self._bqml_model: Optional[core.BqmlModel] = None
        self._bqml_model_factory = globals.bqml_model_factory()
        self._base_sql_generator = globals.base_sql_generator()

    def _keys(self):
        return (self._bqml_model, self.strategy)

    def _compile_to_sql(
        self,
        X: bpd.DataFrame,
        columns: Optional[Iterable[str]] = None,
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
            self._base_sql_generator.ml_imputer(
                column, self.strategy, f"imputer_{column}"
            )
            for column in columns
        ]

    @classmethod
    def _parse_from_sql(cls, sql: str) -> tuple[SimpleImputer, str]:
        """Parse SQL to tuple(SimpleImputer, column_label).

        Args:
            sql: SQL string of format "ML.IMPUTER({col_label}, {strategy}) OVER()"

        Returns:
            tuple(SimpleImputer, column_label)"""
        s = sql[sql.find("(") + 1 : sql.find(")")]
        col_label, strategy = s.split(", ")
        return cls(strategy[1:-1]), _unescape_id(col_label)  # type: ignore[arg-type]

    def fit(
        self,
        X: utils.ArrayType,
        y=None,  # ignored
    ) -> SimpleImputer:
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
