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

    def predict(
        self, X=None, *, horizon: int = 3, confidence_level: float = 0.95
    ) -> bpd.DataFrame:
        """Predict the closest cluster for each sample in X.

        Args:
            X (default None):
                ignored, to be compatible with other APIs.
            horizon (int, default: 3):
                an int value that specifies the number of time points to forecast.
                The default value is 3, and the maximum value is 1000.
            confidence_level (float, default 0.95):
                a float value that specifies percentage of the future values that fall in the prediction interval.
                The valid input range is [0.0, 1.0).

        Returns:
            bigframes.dataframe.DataFrame: The predicted DataFrames. Which
                contains 2 columns "forecast_timestamp" and "forecast_value".
        """
        if horizon < 1 or horizon > 1000:
            raise ValueError(f"horizon must be [1, 1000], but is {horizon}.")
        if confidence_level < 0.0 or confidence_level >= 1.0:
            raise ValueError(
                f"confidence_level must be [0.0, 1.0), but is {confidence_level}."
            )

        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before predict")

        return self._bqml_model.forecast(
            options={"horizon": horizon, "confidence_level": confidence_level}
        )

    def detect_anomalies(
        self,
        X: Union[bpd.DataFrame, bpd.Series],
        *,
        anomaly_prob_threshold: float = 0.95,
    ) -> bpd.DataFrame:
        """Detect the anomaly data points of the input.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series):
                Series or a DataFrame to detect anomalies.
            anomaly_prob_threshold (float, default 0.95):
                Identifies the custom threshold to use for anomaly detection. The value must be in the range [0, 1), with a default value of 0.95.

        Returns:
            bigframes.dataframe.DataFrame: detected DataFrame."""
        if anomaly_prob_threshold < 0.0 or anomaly_prob_threshold >= 1.0:
            raise ValueError(
                f"anomaly_prob_threshold must be [0.0, 1.0), but is {anomaly_prob_threshold}."
            )

        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before detect_anomalies")

        (X,) = utils.convert_to_dataframe(X)

        return self._bqml_model.detect_anomalies(
            X, options={"anomaly_prob_threshold": anomaly_prob_threshold}
        )

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

    def summary(
        self,
        show_all_candidate_models: bool = False,
    ) -> bpd.DataFrame:
        """Summary of the evaluation metrics of the time series model.

        .. note::

            Output matches that of the BigQuery ML.ARIMA_EVALUATE function.
            See: https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-arima-evaluate
            for the outputs relevant to this model type.

        Args:
            show_all_candidate_models (bool, default to False):
                Whether to show evaluation metrics or an error message for either
                all candidate models or for only the best model with the lowest
                AIC. Default to False.

        Returns:
            bigframes.dataframe.DataFrame: A DataFrame as evaluation result.
        """
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before score")
        return self._bqml_model.arima_evaluate(show_all_candidate_models)

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
