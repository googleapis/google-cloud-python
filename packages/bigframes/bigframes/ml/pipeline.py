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

"""For composing estimators together. This module is styled after scikit-learn's
pipeline module: https://scikit-learn.org/stable/modules/pipeline.html."""


from __future__ import annotations

from typing import List, Optional, Tuple

import bigframes_vendored.constants as constants
import bigframes_vendored.sklearn.pipeline
from google.cloud import bigquery

from bigframes.core import log_adapter
import bigframes.dataframe
from bigframes.ml import (
    base,
    compose,
    forecasting,
    impute,
    loader,
    preprocessing,
    utils,
)
import bigframes.session


@log_adapter.class_logger
class Pipeline(
    base.BaseEstimator,
    bigframes_vendored.sklearn.pipeline.Pipeline,
):
    __doc__ = bigframes_vendored.sklearn.pipeline.Pipeline.__doc__

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
                preprocessing.PolynomialFeatures,
                impute.SimpleImputer,
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
    def _from_bq(
        cls, session: bigframes.session.Session, bq_model: bigquery.Model
    ) -> Pipeline:
        col_transformer = compose.ColumnTransformer._extract_from_bq_model(bq_model)
        transform = col_transformer._merge(bq_model)

        estimator = loader._model_from_bq(session, bq_model)
        return cls([("transform", transform), ("estimator", estimator)])

    def fit(
        self,
        X: utils.BigFramesArrayType,
        y: Optional[utils.BigFramesArrayType] = None,
    ) -> Pipeline:
        (X,) = utils.batch_convert_to_dataframe(X)

        transform_sqls = self._transform._compile_to_sql(X)
        if y is not None:
            # If labels columns are present, they should pass through un-transformed
            (y,) = utils.batch_convert_to_dataframe(y)
            transform_sqls.extend(y.columns.tolist())

        self._estimator._fit(X=X, y=y, transforms=transform_sqls)
        return self

    def predict(self, X: utils.ArrayType) -> bigframes.dataframe.DataFrame:
        return self._estimator.predict(X)

    def score(
        self,
        X: utils.BigFramesArrayType,
        y: Optional[utils.BigFramesArrayType] = None,
    ) -> bigframes.dataframe.DataFrame:
        (X,) = utils.batch_convert_to_dataframe(X)
        if y is not None:
            (y,) = utils.batch_convert_to_dataframe(y)

        return self._estimator.score(X=X, y=y)

    def to_gbq(self, model_name: str, replace: bool = False) -> Pipeline:
        """Save the pipeline to BigQuery.

        Args:
            model_name (str):
                The name of the model(pipeline).
            replace (bool, default False):
                Whether to replace if the model(pipeline) already exists. Default to False.

        Returns:
            Pipeline: Saved model(pipeline)."""
        if not self._estimator._bqml_model:
            raise RuntimeError("A model must be fitted before it can be saved")

        new_model = self._estimator._bqml_model.copy(model_name, replace)

        return new_model.session.read_gbq_model(model_name)
