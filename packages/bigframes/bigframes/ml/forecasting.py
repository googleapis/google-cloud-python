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

"""Forcasting models."""

from __future__ import annotations

from typing import Dict, List, Optional, Union

from google.cloud import bigquery

import bigframes
from bigframes.core import log_adapter
from bigframes.ml import base, core, globals, utils
import bigframes.pandas as bpd


@log_adapter.class_logger
class ARIMAPlus(base.SupervisedTrainablePredictor):
    """Time Series ARIMA Plus model."""

    def __init__(self):
        self._bqml_model: Optional[core.BqmlModel] = None
        self._bqml_model_factory = globals.bqml_model_factory()

    @classmethod
    def _from_bq(cls, session: bigframes.Session, model: bigquery.Model) -> ARIMAPlus:
        assert model.model_type == "ARIMA_PLUS"

        kwargs: Dict[str, str | int | bool | float | List[str]] = {}

        new_arima_plus = cls(**kwargs)
        new_arima_plus._bqml_model = core.BqmlModel(session, model)
        return new_arima_plus

    @property
    def _bqml_options(self) -> Dict[str, str | int | bool | float | List[str]]:
        """The model options as they will be set for BQML."""
        return {"model_type": "ARIMA_PLUS"}

    def _fit(
        self,
        X: Union[bpd.DataFrame, bpd.Series],
        y: Union[bpd.DataFrame, bpd.Series],
        transforms: Optional[List[str]] = None,
    ):
        """Fit the model to training data.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series):
                A dataframe of training timestamp.

            y (bigframes.dataframe.DataFrame or bigframes.series.Series):
                Target values for training.
            transforms (Optional[List[str]], default None):
                Do not use. Internal param to be deprecated.
                Use bigframes.ml.pipeline instead.

        Returns:
            ARIMAPlus: Fitted estimator.
        """
        if X.columns.size != 1:
            raise ValueError(
                "Time series timestamp input X must only contain 1 column."
            )
        if y.columns.size != 1:
            raise ValueError("Time series data input y must only contain 1 column.")

        X, y = utils.convert_to_dataframe(X, y)

        self._bqml_model = self._bqml_model_factory.create_time_series_model(
            X,
            y,
            transforms=transforms,
            options=self._bqml_options,
        )

    def predict(self, X=None) -> bpd.DataFrame:
        """Predict the closest cluster for each sample in X.

        Args:
            X (default None):
                ignored, to be compatible with other APIs.

        Returns:
            bigframes.dataframe.DataFrame: The predicted DataFrames. Which
                contains 2 columns "forecast_timestamp" and "forecast_value".
        """
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before predict")

        return self._bqml_model.forecast()

    def score(
        self,
        X: Union[bpd.DataFrame, bpd.Series],
        y: Union[bpd.DataFrame, bpd.Series],
    ) -> bpd.DataFrame:
        """Calculate evaluation metrics of the model.

        .. note::

            Output matches that of the BigQuery ML.EVALUTE function.
            See: https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate#time_series_models
            for the outputs relevant to this model type.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series):
                A BigQuery DataFrame only contains 1 column as
                evaluation timestamp. The timestamp must be within the horizon
                of the model, which by default is 1000 data points.
            y (bigframes.dataframe.DataFrame or bigframes.series.Series):
                A BigQuery DataFrame only contains 1 column as
                evaluation numeric values.

        Returns:
            bigframes.dataframe.DataFrame: A DataFrame as evaluation result.
        """
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before score")
        X, y = utils.convert_to_dataframe(X, y)

        input_data = X.join(y, how="outer")
        return self._bqml_model.evaluate(input_data)

    def to_gbq(self, model_name: str, replace: bool = False) -> ARIMAPlus:
        """Save the model to BigQuery.

        Args:
            model_name (str):
                the name of the model.
            replace (bool, default False):
                whether to replace if the model already exists. Default to False.

        Returns:
            ARIMAPlus: saved model."""
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before it can be saved")

        new_model = self._bqml_model.copy(model_name, replace)
        return new_model.session.read_gbq_model(model_name)
