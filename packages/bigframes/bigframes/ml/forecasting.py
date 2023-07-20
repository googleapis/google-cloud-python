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

from __future__ import annotations

from typing import cast, Dict, List, Optional, TYPE_CHECKING

from google.cloud import bigquery

if TYPE_CHECKING:
    import bigframes

import bigframes.ml.base
import bigframes.ml.core

_PREDICT_OUTPUT_COLUMNS = ["forecast_timestamp", "forecast_value"]


class ARIMAPlus(bigframes.ml.base.TrainablePredictor):
    """Time Series ARIMA Plus model."""

    def __init__(self):
        self._bqml_model: Optional[bigframes.ml.core.BqmlModel] = None

    @staticmethod
    def _from_bq(session: bigframes.Session, model: bigquery.Model) -> ARIMAPlus:
        assert model.model_type == "ARIMA_PLUS"

        kwargs: Dict[str, str | int | bool | float | List[str]] = {}

        new_arima_plus = ARIMAPlus(**kwargs)
        new_arima_plus._bqml_model = bigframes.ml.core.BqmlModel(session, model)
        return new_arima_plus

    @property
    def _bqml_options(self) -> Dict[str, str | int | bool | float | List[str]]:
        """The model options as they will be set for BQML."""
        return {"model_type": "ARIMA_PLUS"}

    def fit(
        self,
        X: bigframes.dataframe.DataFrame,
        y: bigframes.dataframe.DataFrame,
        transforms: Optional[List[str]] = None,
    ):
        """Fit the model to training data

        Args:
            X: A dataframe of training timestamp.

            y: Target values for training."""
        self._bqml_model = bigframes.ml.core.create_bqml_time_series_model(
            X,
            y,
            transforms=transforms,
            options=self._bqml_options,
        )

    def predict(self, X=None) -> bigframes.dataframe.DataFrame:
        """Predict the closest cluster for each sample in X.

        Args:
            X: ignored, to be compatible with other APIs.
        Returns:
            The predicted BigQuery DataFrames. Which contains 2 columns
            "forecast_timestamp" and "forecast_value".
        """
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before predict")

        return cast(
            bigframes.dataframe.DataFrame,
            self._bqml_model.forecast()[_PREDICT_OUTPUT_COLUMNS],
        )

    # Unlike regression models, time series forcasting can only evaluate with unseen data. X and y must be providee.
    def score(
        self,
        X: bigframes.dataframe.DataFrame,
        y: bigframes.dataframe.DataFrame,
    ) -> bigframes.dataframe.DataFrame:
        """Calculate evaluation metrics of the model.

        Args:
            X:
                A BigQuery DataFrames only contains 1 column as
                evaluation timestamp. The timestamp must be within the horizon
                of the model, which by default is 1000 data points.
            y:
                A BigQuery DataFrames only contains 1 column as
                evaluation numeric values.

        Returns:
            A BigQuery DataFrames as evaluation result.
        """
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before score")

        input_data = X.join(y, how="outer")
        return self._bqml_model.evaluate(input_data)

    def to_gbq(self, model_name: str, replace: bool = False) -> ARIMAPlus:
        """Save the model to Google Cloud BigQuey.

        Args:
            model_name: the name of the model.
            replace: whether to replace if the model already exists. Default to False.

        Returns: saved model."""
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before it can be saved")

        new_model = self._bqml_model.copy(model_name, replace)
        return new_model.session.read_gbq_model(model_name)
