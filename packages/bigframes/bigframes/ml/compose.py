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
after scikit-Learn's compose module:
https://scikit-learn.org/stable/modules/classes.html#module-sklearn.compose."""

from __future__ import annotations

import re
import types
import typing
from typing import cast, List, Optional, Tuple, Union

import bigframes_vendored.sklearn.compose._column_transformer
from google.cloud import bigquery

from bigframes import constants
from bigframes.core import log_adapter
from bigframes.ml import base, core, globals, preprocessing, utils
import bigframes.pandas as bpd

_BQML_TRANSFROM_TYPE_MAPPING = types.MappingProxyType(
    {
        "ML.STANDARD_SCALER": preprocessing.StandardScaler,
        "ML.ONE_HOT_ENCODER": preprocessing.OneHotEncoder,
        "ML.MAX_ABS_SCALER": preprocessing.MaxAbsScaler,
        "ML.MIN_MAX_SCALER": preprocessing.MinMaxScaler,
        "ML.BUCKETIZE": preprocessing.KBinsDiscretizer,
        "ML.LABEL_ENCODER": preprocessing.LabelEncoder,
    }
)


@log_adapter.class_logger
class ColumnTransformer(
    base.Transformer,
    bigframes_vendored.sklearn.compose._column_transformer.ColumnTransformer,
):
    __doc__ = (
        bigframes_vendored.sklearn.compose._column_transformer.ColumnTransformer.__doc__
    )

    def __init__(
        self,
        transformers: List[
            Tuple[
                str,
                preprocessing.PreprocessingType,
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
    ) -> List[Tuple[str, preprocessing.PreprocessingType, str,]]:
        """The collection of transformers as tuples of (name, transformer, column)."""
        result: List[
            Tuple[
                str,
                preprocessing.PreprocessingType,
                str,
            ]
        ] = []

        for entry in self.transformers:
            name, transformer, column_or_columns = entry
            columns = (
                column_or_columns
                if isinstance(column_or_columns, List)
                else [column_or_columns]
            )

            for column in columns:
                result.append((name, transformer, column))

        return result

    @classmethod
    def _extract_from_bq_model(
        cls,
        bq_model: bigquery.Model,
    ) -> ColumnTransformer:
        """Extract transformers as ColumnTransformer obj from a BQ Model. Keep the _bqml_model field as None."""
        assert "transformColumns" in bq_model._properties

        transformers: List[
            Tuple[
                str,
                preprocessing.PreprocessingType,
                Union[str, List[str]],
            ]
        ] = []

        def camel_to_snake(name):
            name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
            return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()

        output_names = []
        for transform_col in bq_model._properties["transformColumns"]:
            transform_col_dict = cast(dict, transform_col)
            # pass the columns that are not transformed
            if "transformSql" not in transform_col_dict:
                continue
            transform_sql: str = transform_col_dict["transformSql"]
            if not transform_sql.startswith("ML."):
                continue

            output_names.append(transform_col_dict["name"])
            found_transformer = False
            for prefix in _BQML_TRANSFROM_TYPE_MAPPING:
                if transform_sql.startswith(prefix):
                    transformer_cls = _BQML_TRANSFROM_TYPE_MAPPING[prefix]
                    transformers.append(
                        (
                            camel_to_snake(transformer_cls.__name__),
                            *transformer_cls._parse_from_sql(transform_sql),  # type: ignore
                        )
                    )

                    found_transformer = True
                    break
            if not found_transformer:
                raise NotImplementedError(
                    f"Unsupported transformer type. {constants.FEEDBACK_LINK}"
                )

        transformer = cls(transformers=transformers)
        transformer._output_names = output_names

        return transformer

    def _merge(
        self, bq_model: bigquery.Model
    ) -> Union[ColumnTransformer, preprocessing.PreprocessingType,]:
        """Try to merge the column transformer to a simple transformer. Depends on all the columns in bq_model are transformed with the same transformer."""
        transformers = self.transformers_

        assert len(transformers) > 0
        _, transformer_0, column_0 = transformers[0]
        columns = [column_0]
        for _, transformer, column in transformers[1:]:
            # all transformers are the same
            if transformer != transformer_0:
                return self
            columns.append(column)
        # all feature columns are transformed
        if sorted(
            [
                cast(str, feature_column.name)
                for feature_column in bq_model.feature_columns
            ]
        ) == sorted(columns):
            transformer_0._output_names = self._output_names
            return transformer_0

        return self

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
