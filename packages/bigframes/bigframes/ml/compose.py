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

"""Build composite transformers on heterogeneous data. This module is styled
after Scikit-Learn's compose module:
https://scikit-learn.org/stable/modules/classes.html#module-sklearn.compose."""

from __future__ import annotations

import typing
from typing import List, Optional, Tuple, Union

from bigframes import constants
from bigframes.core import log_adapter
from bigframes.ml import base, core, globals, preprocessing, utils
import bigframes.pandas as bpd
import third_party.bigframes_vendored.sklearn.compose._column_transformer

CompilablePreprocessorType = Union[
    preprocessing.OneHotEncoder,
    preprocessing.StandardScaler,
    preprocessing.MaxAbsScaler,
    preprocessing.MinMaxScaler,
    preprocessing.KBinsDiscretizer,
    preprocessing.LabelEncoder,
]


@log_adapter.class_logger
class ColumnTransformer(
    base.Transformer,
    third_party.bigframes_vendored.sklearn.compose._column_transformer.ColumnTransformer,
):
    __doc__ = (
        third_party.bigframes_vendored.sklearn.compose._column_transformer.ColumnTransformer.__doc__
    )

    def __init__(
        self,
        transformers: List[
            Tuple[
                str,
                CompilablePreprocessorType,
                Union[str, List[str]],
            ]
        ],
    ):
        # TODO: if any(transformers) has fitted raise warning
        self.transformers = transformers
        self._bqml_model: Optional[core.BqmlModel] = None
        self._bqml_model_factory = globals.bqml_model_factory()
        # call self.transformers_ to check chained transformers
        self.transformers_

    @property
    def transformers_(
        self,
    ) -> List[Tuple[str, CompilablePreprocessorType, str,]]:
        """The collection of transformers as tuples of (name, transformer, column)."""
        result: List[
            Tuple[
                str,
                CompilablePreprocessorType,
                str,
            ]
        ] = []

        column_set: set[str] = set()
        for entry in self.transformers:
            name, transformer, column_or_columns = entry
            columns = (
                column_or_columns
                if isinstance(column_or_columns, List)
                else [column_or_columns]
            )

            for column in columns:
                if column in column_set:
                    raise NotImplementedError(
                        f"Chained transformers on the same column isn't supported. {constants.FEEDBACK_LINK}"
                    )
                result.append((name, transformer, column))

        return result

    def _compile_to_sql(
        self,
        columns: List[str],
        X: bpd.DataFrame,
    ) -> List[Tuple[str, str]]:
        """Compile this transformer to a list of SQL expressions that can be included in
        a BQML TRANSFORM clause

        Args:
            columns (List[str]):
                a list of column names to transform
            X (bpd.DataFrame):
                The Dataframe with training data.

        Returns:
            a list of tuples of (sql_expression, output_name)"""
        return [
            transformer._compile_to_sql([column], X=X)[0]
            for column in columns
            for _, transformer, target_column in self.transformers_
            if column == target_column
        ]

    def fit(
        self,
        X: Union[bpd.DataFrame, bpd.Series],
        y=None,  # ignored
    ) -> ColumnTransformer:
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
