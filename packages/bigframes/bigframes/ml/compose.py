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

"""Build composite transformers on heterogenous data. This module is styled
after Scikit-Learn's compose module:
https://scikit-learn.org/stable/modules/classes.html#module-sklearn.compose"""

from __future__ import annotations

import typing
from typing import List, Optional, Tuple, TYPE_CHECKING, Union

if TYPE_CHECKING:
    import bigframes

import bigframes.ml.base
import bigframes.ml.compose
import bigframes.ml.core
import bigframes.ml.preprocessing
import third_party.bigframes_vendored.sklearn.compose._column_transformer

CompilablePreprocessorType = Union[
    bigframes.ml.preprocessing.OneHotEncoder,
    bigframes.ml.preprocessing.StandardScaler,
]


class ColumnTransformer(
    third_party.bigframes_vendored.sklearn.compose._column_transformer.ColumnTransformer,
    bigframes.ml.base.BaseEstimator,
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
        self.transformers = transformers
        self._bqml_model: Optional[bigframes.ml.core.BqmlModel] = None

    @property
    def transformers_(
        self,
    ) -> List[Tuple[str, CompilablePreprocessorType, str,]]:
        """The collection of transformers as tuples of (name, transformer, column)"""
        result: List[
            Tuple[
                str,
                CompilablePreprocessorType,
                str,
            ]
        ] = []
        for entry in self.transformers:
            name, transformer, column_or_columns = entry
            if isinstance(column_or_columns, str):
                result.append((name, transformer, column_or_columns))
            else:
                for column in column_or_columns:
                    result.append((name, transformer, column))

        return result

    def _compile_to_sql(self, columns: List[str]) -> List[Tuple[str, str]]:
        """Compile this transformer to a list of SQL expressions that can be included in
        a BQML TRANSFORM clause

        Args:
            columns: a list of column names to transform

        Returns: a list of tuples of (sql_expression, output_name)"""
        return [
            transformer._compile_to_sql([column])[0]
            for column in columns
            for _, transformer, target_column in self.transformers_
            if column == target_column
        ]

    def fit(
        self,
        X: bigframes.dataframe.DataFrame,
    ):
        compiled_transforms = self._compile_to_sql(X.columns.tolist())
        transform_sqls = [transform_sql for transform_sql, _ in compiled_transforms]

        self._bqml_model = bigframes.ml.core.create_bqml_model(
            X,
            options={"model_type": "transform_only"},
            transforms=transform_sqls,
        )

        # The schema of TRANSFORM output is not available in the model API, so save it during fitting
        self._output_names = [name for _, name in compiled_transforms]

    def transform(
        self, X: bigframes.dataframe.DataFrame
    ) -> bigframes.dataframe.DataFrame:
        if not self._bqml_model:
            raise RuntimeError("Must be fitted before transform")

        df = self._bqml_model.transform(X)
        return typing.cast(
            bigframes.dataframe.DataFrame,
            df[self._output_names],
        )
