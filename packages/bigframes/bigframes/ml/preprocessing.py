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
Scikit-Learn's preprocessing module: https://scikit-learn.org/stable/modules/preprocessing.html"""


import typing
from typing import List, Optional, Tuple

import bigframes
import bigframes.ml
import bigframes.ml.sql
import third_party.bigframes_vendored.sklearn.preprocessing._data
import third_party.bigframes_vendored.sklearn.preprocessing._encoder


class StandardScaler(
    third_party.bigframes_vendored.sklearn.preprocessing._data.StandardScaler,
    bigframes.ml.base.BaseEstimator,
):
    __doc__ = (
        third_party.bigframes_vendored.sklearn.preprocessing._data.StandardScaler.__doc__
    )

    def __init__(self):
        self._bqml_model: Optional[bigframes.ml.core.BqmlModel] = None

    def _compile_to_sql(self, columns: List[str]) -> List[Tuple[str, str]]:
        """Compile this transformer to a list of SQL expressions that can be included in
        a BQML TRANSFORM clause

        Args:
            columns: a list of column names to transform

        Returns: a list of tuples of (sql_expression, output_name)"""
        return [
            (
                bigframes.ml.sql.ml_standard_scaler(column, f"scaled_{column}"),
                f"scaled_{column}",
            )
            for column in columns
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


class OneHotEncoder(
    third_party.bigframes_vendored.sklearn.preprocessing._encoder.OneHotEncoder,
    bigframes.ml.base.BaseEstimator,
):
    __doc__ = (
        third_party.bigframes_vendored.sklearn.preprocessing._encoder.OneHotEncoder.__doc__
    )

    # All estimators must implement __init__ to document their parameters, even
    # if they don't have any
    def __init__(self):
        pass

    def _compile_to_sql(self, columns: List[str]) -> List[Tuple[str, str]]:
        """Compile this transformer to a list of SQL expressions that can be included in
        a BQML TRANSFORM clause

        Args:
            columns: a list of column names to transform

        Returns: a list of tuples of (sql_expression, output_name)"""
        return [
            (
                bigframes.ml.sql.ml_one_hot_encoder(column, f"onehotencoded_{column}"),
                f"onehotencoded_{column}",
            )
            for column in columns
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
