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

"""For composing estimators together. This module is styled after Scikit-Learn's
pipeline module: https://scikit-learn.org/stable/modules/pipeline.html."""


from __future__ import annotations

from typing import cast, List, Optional, Tuple, Union

from google.cloud import bigquery

import bigframes
import bigframes.constants as constants
from bigframes.core import log_adapter
from bigframes.ml import base, compose, forecasting, loader, preprocessing, utils
import bigframes.pandas as bpd
import third_party.bigframes_vendored.sklearn.pipeline


@log_adapter.class_logger
class Pipeline(
    base.BaseEstimator,
    third_party.bigframes_vendored.sklearn.pipeline.Pipeline,
):
    __doc__ = third_party.bigframes_vendored.sklearn.pipeline.Pipeline.__doc__

    def __init__(self, steps: List[Tuple[str, base.BaseEstimator]]):
        self.steps = steps

        if len(steps) != 2:
            raise NotImplementedError(
                f"Currently only two step (transform, estimator) pipelines are supported. {constants.FEEDBACK_LINK}"
            )

        transform, estimator = steps[0][1], steps[1][1]
        if isinstance(
            transform,
            (
                compose.ColumnTransformer,
                preprocessing.StandardScaler,
                preprocessing.OneHotEncoder,
                preprocessing.MaxAbsScaler,
                preprocessing.MinMaxScaler,
                preprocessing.KBinsDiscretizer,
                preprocessing.LabelEncoder,
            ),
        ):
            self._transform = transform
        else:
            raise NotImplementedError(
                f"Transformer type {type(transform)} is not yet supported by Pipeline. {constants.FEEDBACK_LINK}"
            )

        if not isinstance(
            estimator,
            base.TrainablePredictor,
        ):
            raise NotImplementedError(
                f"Estimator type {type(estimator)} is not supported by Pipeline. {constants.FEEDBACK_LINK}"
            )

        # BQML doesn't support ARIMA_PLUS with transformers. b/298676367
        if isinstance(estimator, forecasting.ARIMAPlus):
            raise NotImplementedError(
                f"Estimator type {type(estimator)} is not supported by Pipeline. {constants.FEEDBACK_LINK}"
            )

        self._transform = transform
        self._estimator = estimator

    @classmethod
    def _from_bq(cls, session: bigframes.Session, bq_model: bigquery.Model) -> Pipeline:
        col_transformer = _extract_as_column_transformer(bq_model)
        transform = _merge_column_transformer(bq_model, col_transformer)

        estimator = loader._model_from_bq(session, bq_model)
        return cls([("transform", transform), ("estimator", estimator)])

    def fit(
        self,
        X: Union[bpd.DataFrame, bpd.Series],
        y: Optional[Union[bpd.DataFrame, bpd.Series]] = None,
    ) -> Pipeline:
        (X,) = utils.convert_to_dataframe(X)

        compiled_transforms = self._transform._compile_to_sql(X.columns.tolist(), X=X)
        transform_sqls = [transform_sql for transform_sql, _ in compiled_transforms]

        if y is not None:
            # If labels columns are present, they should pass through un-transformed
            (y,) = utils.convert_to_dataframe(y)
            transform_sqls.extend(y.columns.tolist())

        self._estimator._fit(X=X, y=y, transforms=transform_sqls)
        return self

    def predict(self, X: Union[bpd.DataFrame, bpd.Series]) -> bpd.DataFrame:
        return self._estimator.predict(X)

    def score(
        self,
        X: Union[bpd.DataFrame, bpd.Series],
        y: Optional[Union[bpd.DataFrame, bpd.Series]] = None,
    ) -> bpd.DataFrame:
        (X,) = utils.convert_to_dataframe(X)
        if y is not None:
            (y,) = utils.convert_to_dataframe(y)

        return self._estimator.score(X=X, y=y)

    def to_gbq(self, model_name: str, replace: bool = False) -> Pipeline:
        """Save the pipeline to BigQuery.

        Args:
            model_name (str):
                the name of the model(pipeline).
            replace (bool, default False):
                whether to replace if the model(pipeline) already exists. Default to False.

        Returns:
            Pipeline: saved model(pipeline)."""
        if not self._estimator._bqml_model:
            raise RuntimeError("A model must be fitted before it can be saved")

        new_model = self._estimator._bqml_model.copy(model_name, replace)

        return new_model.session.read_gbq_model(model_name)


def _extract_as_column_transformer(
    bq_model: bigquery.Model,
) -> compose.ColumnTransformer:
    """Extract transformers as ColumnTransformer obj from a BQ Model."""
    assert "transformColumns" in bq_model._properties

    transformers: List[
        Tuple[
            str,
            Union[
                preprocessing.OneHotEncoder,
                preprocessing.StandardScaler,
                preprocessing.MaxAbsScaler,
                preprocessing.MinMaxScaler,
                preprocessing.KBinsDiscretizer,
                preprocessing.LabelEncoder,
            ],
            Union[str, List[str]],
        ]
    ] = []
    for transform_col in bq_model._properties["transformColumns"]:
        # pass the columns that are not transformed
        if "transformSql" not in transform_col:
            continue

        transform_sql: str = cast(dict, transform_col)["transformSql"]
        if transform_sql.startswith("ML.STANDARD_SCALER"):
            transformers.append(
                (
                    "standard_scaler",
                    *preprocessing.StandardScaler._parse_from_sql(transform_sql),
                )
            )
        elif transform_sql.startswith("ML.ONE_HOT_ENCODER"):
            transformers.append(
                (
                    "ont_hot_encoder",
                    *preprocessing.OneHotEncoder._parse_from_sql(transform_sql),
                )
            )
        elif transform_sql.startswith("ML.MAX_ABS_SCALER"):
            transformers.append(
                (
                    "max_abs_scaler",
                    *preprocessing.MaxAbsScaler._parse_from_sql(transform_sql),
                )
            )
        elif transform_sql.startswith("ML.MIN_MAX_SCALER"):
            transformers.append(
                (
                    "min_max_scaler",
                    *preprocessing.MinMaxScaler._parse_from_sql(transform_sql),
                )
            )
        elif transform_sql.startswith("ML.BUCKETIZE"):
            transformers.append(
                (
                    "k_bins_discretizer",
                    *preprocessing.KBinsDiscretizer._parse_from_sql(transform_sql),
                )
            )
        elif transform_sql.startswith("ML.LABEL_ENCODER"):
            transformers.append(
                (
                    "label_encoder",
                    *preprocessing.LabelEncoder._parse_from_sql(transform_sql),
                )
            )
        else:
            raise NotImplementedError(
                f"Unsupported transformer type. {constants.FEEDBACK_LINK}"
            )

    return compose.ColumnTransformer(transformers=transformers)


def _merge_column_transformer(
    bq_model: bigquery.Model, column_transformer: compose.ColumnTransformer
) -> Union[
    compose.ColumnTransformer,
    preprocessing.StandardScaler,
    preprocessing.OneHotEncoder,
    preprocessing.MaxAbsScaler,
    preprocessing.MinMaxScaler,
    preprocessing.KBinsDiscretizer,
    preprocessing.LabelEncoder,
]:
    """Try to merge the column transformer to a simple transformer."""
    transformers = column_transformer.transformers_

    assert len(transformers) > 0
    _, transformer_0, column_0 = transformers[0]
    columns = [column_0]
    for _, transformer, column in transformers[1:]:
        # all transformers are the same
        if transformer != transformer_0:
            return column_transformer
        columns.append(column)
    # all feature columns are transformed
    if sorted(
        [cast(str, feature_column.name) for feature_column in bq_model.feature_columns]
    ) == sorted(columns):
        return transformer_0

    return column_transformer
