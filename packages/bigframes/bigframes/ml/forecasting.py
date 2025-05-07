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

from typing import List, Optional

from google.cloud import bigquery

from bigframes.core import log_adapter
from bigframes.ml import base, core, globals, utils
import bigframes.pandas as bpd
import bigframes.session

_BQML_PARAMS_MAPPING = {
    "horizon": "horizon",
    "auto_arima": "autoArima",
    "auto_arima_max_order": "autoArimaMaxOrder",
    "auto_arima_min_order": "autoArimaMinOrder",
    "order": "nonSeasonalOrder",
    "data_frequency": "dataFrequency",
    "include_drift": "includeDrift",
    "holiday_region": "holidayRegion",
    "clean_spikes_and_dips": "cleanSpikesAndDips",
    "adjust_step_changes": "adjustStepChanges",
    "forecast_limit_upper_bound": "forecastLimitUpperBound",
    "forecast_limit_lower_bound": "forecastLimitLowerBound",
    "time_series_length_fraction": "timeSeriesLengthFraction",
    "min_time_series_length": "minTimeSeriesLength",
    "max_time_series_length": "maxTimeSeriesLength",
    "decompose_time_series": "decomposeTimeSeries",
    "trend_smoothing_window_size": "trendSmoothingWindowSize",
}


@log_adapter.class_logger
class ARIMAPlus(base.SupervisedTrainableWithIdColPredictor):
    """Time Series ARIMA Plus model.

    Args:
        horizon (int, default 1,000):
            The number of time points to forecast. Default to 1,000, max value 10,000.

        auto_arima (bool, default True):
            Determines whether the training process uses auto.ARIMA or not. If True, training automatically finds the best non-seasonal order (that is, the p, d, q tuple) and decides whether or not to include a linear drift term when d is 1.

        auto_arima_max_order (int or None, default None):
            The maximum value for the sum of non-seasonal p and q.

        auto_arima_min_order (int or None, default None):
            The minimum value for the sum of non-seasonal p and q.

        data_frequency (str, default "auto_frequency"):
            The data frequency of the input time series.
            Possible values are "auto_frequency", "per_minute", "hourly", "daily", "weekly", "monthly", "quarterly", "yearly"

        include_drift (bool, default False):
            Determines whether the model should include a linear drift term or not. The drift term is applicable when non-seasonal d is 1.

        holiday_region (str or None, default None):
            The geographical region based on which the holiday effect is applied in modeling. By default, holiday effect modeling isn't used.
            Possible values see https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series#holiday_region.

        clean_spikes_and_dips (bool, default True):
            Determines whether or not to perform automatic spikes and dips detection and cleanup in the model training pipeline. The spikes and dips are replaced with local linear interpolated values when they're detected.

        adjust_step_changes (bool, default True):
            Determines whether or not to perform automatic step change detection and adjustment in the model training pipeline.

        forecast_limit_upper_bound (float or None, default None):
            The upper bound of the forecasting values. When you specify the ``forecast_limit_upper_bound`` option, all of the forecast values must be less than the specified value.
            For example, if you set ``forecast_limit_upper_bound`` to 100, then all of the forecast values are less than 100.
            Also, all values greater than or equal to the ``forecast_limit_upper_bound`` value are excluded from modelling.
            The forecasting limit ensures that forecasts stay within limits.

        forecast_limit_lower_bound (float or None, default None):
            The lower bound of the forecasting values where the minimum value allowed is 0. When you specify the ``forecast_limit_lower_bound`` option, all of the forecast values must be greater than the specified value.
            For example, if you set ``forecast_limit_lower_bound`` to 0, then all of the forecast values are larger than 0. Also, all values less than or equal to the ``forecast_limit_lower_bound`` value are excluded from modelling.
            The forecasting limit ensures that forecasts stay within limits.

        time_series_length_fraction (float or None, default None):
            The fraction of the interpolated length of the time series that's used to model the time series trend component. All of the time points of the time series are used to model the non-trend component.

        min_time_series_length (int or None, default None):
            The minimum number of time points that are used in modeling the trend component of the time series.

        max_time_series_length (int or None, default None):
            The maximum number of time points in a time series that can be used in modeling the trend component of the time series.

        trend_smoothing_window_size (int or None, default None):
            The smoothing window size for the trend component.

        decompose_time_series (bool, default True):
            Determines whether the separate components of both the history and forecast parts of the time series (such as holiday effect and seasonal components) are saved in the model.
    """

    def __init__(
        self,
        *,
        horizon: int = 1000,
        auto_arima: bool = True,
        auto_arima_max_order: Optional[int] = None,
        auto_arima_min_order: Optional[int] = None,
        data_frequency: str = "auto_frequency",
        include_drift: bool = False,
        holiday_region: Optional[str] = None,
        clean_spikes_and_dips: bool = True,
        adjust_step_changes: bool = True,
        forecast_limit_lower_bound: Optional[float] = None,
        forecast_limit_upper_bound: Optional[float] = None,
        time_series_length_fraction: Optional[float] = None,
        min_time_series_length: Optional[int] = None,
        max_time_series_length: Optional[int] = None,
        trend_smoothing_window_size: Optional[int] = None,
        decompose_time_series: bool = True,
    ):
        self.horizon = horizon
        self.auto_arima = auto_arima
        self.auto_arima_max_order = auto_arima_max_order
        self.auto_arima_min_order = auto_arima_min_order
        self.data_frequency = data_frequency
        self.include_drift = include_drift
        self.holiday_region = holiday_region
        self.clean_spikes_and_dips = clean_spikes_and_dips
        self.adjust_step_changes = adjust_step_changes
        self.forecast_limit_upper_bound = forecast_limit_upper_bound
        self.forecast_limit_lower_bound = forecast_limit_lower_bound
        self.time_series_length_fraction = time_series_length_fraction
        self.min_time_series_length = min_time_series_length
        self.max_time_series_length = max_time_series_length
        self.trend_smoothing_window_size = trend_smoothing_window_size
        self.decompose_time_series = decompose_time_series
        # TODO(garrettwu) add order and seasonalities params, which need struct/array

        self._bqml_model: Optional[core.BqmlModel] = None
        self._bqml_model_factory = globals.bqml_model_factory()

    @classmethod
    def _from_bq(
        cls, session: bigframes.session.Session, bq_model: bigquery.Model
    ) -> ARIMAPlus:
        assert bq_model.model_type == "ARIMA_PLUS"

        kwargs = utils.retrieve_params_from_bq_model(
            cls, bq_model, _BQML_PARAMS_MAPPING
        )

        model = cls(**kwargs)
        model._bqml_model = core.BqmlModel(session, bq_model)
        return model

    @property
    def _bqml_options(self) -> dict:
        """The model options as they will be set for BQML."""
        options = {
            "model_type": "ARIMA_PLUS",
            "horizon": self.horizon,
            "auto_arima": self.auto_arima,
            "data_frequency": self.data_frequency,
            "clean_spikes_and_dips": self.clean_spikes_and_dips,
            "adjust_step_changes": self.adjust_step_changes,
            "decompose_time_series": self.decompose_time_series,
        }

        if self.auto_arima_max_order is not None:
            options["auto_arima_max_order"] = self.auto_arima_max_order
        if self.auto_arima_min_order is not None:
            options["auto_arima_min_order"] = self.auto_arima_min_order
        if self.holiday_region is not None:
            options["holiday_region"] = self.holiday_region
        if self.time_series_length_fraction is not None:
            options["time_series_length_fraction"] = self.time_series_length_fraction
        if self.min_time_series_length is not None:
            options["min_time_series_length"] = self.min_time_series_length
        if self.max_time_series_length is not None:
            options["max_time_series_length"] = self.max_time_series_length
        if self.trend_smoothing_window_size is not None:
            options["trend_smoothing_window_size"] = self.trend_smoothing_window_size

        if self.include_drift:
            options["include_drift"] = True
        if self.forecast_limit_upper_bound is not None:
            options["forecast_limit_upper_bound"] = self.forecast_limit_upper_bound
        if self.forecast_limit_lower_bound is not None:
            options["forecast_limit_lower_bound"] = self.forecast_limit_lower_bound

        return options

    def _fit(
        self,
        X: utils.ArrayType,
        y: utils.ArrayType,
        transforms: Optional[List[str]] = None,
        id_col: Optional[utils.ArrayType] = None,
    ) -> ARIMAPlus:
        """Fit the model to training data.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series,
            or pandas.core.frame.DataFrame or pandas.core.series.Series):
                A dataframe or series of trainging timestamp.
            y (bigframes.dataframe.DataFrame, or bigframes.series.Series,
            or pandas.core.frame.DataFrame, or pandas.core.series.Series):
                Target values for training.
            transforms (Optional[List[str]], default None):
                Do not use. Internal param to be deprecated.
                Use bigframes.ml.pipeline instead.
            id_col (Optional[bigframes.dataframe.DataFrame]
            or Optional[bigframes.series.Series]
            or Optional[pandas.core.frame.DataFrame]
            or Optional[pandas.core.frame.Series]
            or None, default None):
                An optional dataframe or series of training id col.

        Returns:
            ARIMAPlus: Fitted estimator.
        """
        X, y = utils.batch_convert_to_dataframe(X, y)

        if X.columns.size != 1:
            raise ValueError("Time series timestamp input X contain at least 1 column.")
        if y.columns.size != 1:
            raise ValueError("Time series data input y must only contain 1 column.")

        if id_col is not None:
            (id_col,) = utils.batch_convert_to_dataframe(id_col)

            if id_col.columns.size != 1:
                raise ValueError(
                    "Time series id input id_col must only contain 1 column."
                )

        self._bqml_model = self._bqml_model_factory.create_time_series_model(
            X,
            y,
            id_col=id_col,
            transforms=transforms,
            options=self._bqml_options,
        )
        return self

    def predict(
        self, X=None, *, horizon: int = 3, confidence_level: float = 0.95
    ) -> bpd.DataFrame:
        """Forecast time series at future horizon.

        .. note::

            Output matches that of the BigQuery ML.FORECAST function.
            See: https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-forecast

        Args:
            X (default None):
                ignored, to be compatible with other APIs.
            horizon (int, default: 3):
                an int value that specifies the number of time points to forecast.
                The default value is 3, and the maximum value is 1000.
            confidence_level (float, default 0.95):
                A float value that specifies percentage of the future values that fall in the prediction interval.
                The valid input range is [0.0, 1.0).

        Returns:
            bigframes.dataframe.DataFrame: The predicted DataFrames. Which
                contains 2 columns: "forecast_timestamp", "id" as optional, and "forecast_value".
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

    def predict_explain(
        self, X=None, *, horizon: int = 3, confidence_level: float = 0.95
    ) -> bpd.DataFrame:
        """Explain Forecast time series at future horizon.

        .. note::

            Output matches that of the BigQuery ML.EXPLAIN_FORECAST function.
            See: https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-explain-forecast

        Args:
            X (default None):
                ignored, to be compatible with other APIs.
            horizon (int, default: 3):
                an int value that specifies the number of time points to forecast.
                The default value is 3, and the maximum value is 1000.
            confidence_level (float, default 0.95):
                A float value that specifies percentage of the future values that fall in the prediction interval.
                The valid input range is [0.0, 1.0).

        Returns:
            bigframes.dataframe.DataFrame: The predicted DataFrames.
        """
        if horizon < 1:
            raise ValueError(f"horizon must be at least 1, but is {horizon}.")
        if confidence_level < 0.0 or confidence_level >= 1.0:
            raise ValueError(
                f"confidence_level must be [0.0, 1.0), but is {confidence_level}."
            )

        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before predict")

        return self._bqml_model.explain_forecast(
            options={"horizon": horizon, "confidence_level": confidence_level}
        )

    @property
    def coef_(
        self,
    ) -> bpd.DataFrame:
        """Inspect the coefficients of the model.

        ..note::

            Output matches that of the ML.ARIMA_COEFFICIENTS function.
            See: https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-arima-coefficients
            for the outputs relevant to this model type.

        Returns:
            bigframes.dataframe.DataFrame:
                A DataFrame with the coefficients for the model.
        """

        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before inspect coefficients")
        return self._bqml_model.arima_coefficients()

    def detect_anomalies(
        self,
        X: utils.ArrayType,
        *,
        anomaly_prob_threshold: float = 0.95,
    ) -> bpd.DataFrame:
        """Detect the anomaly data points of the input.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series or pandas.core.frame.DataFrame or pandas.core.series.Series):
                Series or a DataFrame to detect anomalies.
            anomaly_prob_threshold (float, default 0.95):
                Identifies the custom threshold to use for anomaly detection. The value must be in the range [0, 1), with a default value of 0.95.

        Returns:
            bigframes.dataframe.DataFrame: Detected DataFrame."""
        if anomaly_prob_threshold < 0.0 or anomaly_prob_threshold >= 1.0:
            raise ValueError(
                f"anomaly_prob_threshold must be [0.0, 1.0), but is {anomaly_prob_threshold}."
            )

        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before detect_anomalies")

        (X,) = utils.batch_convert_to_dataframe(X, session=self._bqml_model.session)

        return self._bqml_model.detect_anomalies(
            X, options={"anomaly_prob_threshold": anomaly_prob_threshold}
        )

    def score(
        self,
        X: utils.ArrayType,
        y: utils.ArrayType,
        id_col: Optional[utils.ArrayType] = None,
    ) -> bpd.DataFrame:
        """Calculate evaluation metrics of the model.

        .. note::

            Output matches that of the BigQuery ML.EVALUATE function.
            See: https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate#time_series_models
            for the outputs relevant to this model type.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series
            or pandas.core.frame.DataFrame or pandas.core.series.Series):
                A dataframe or series only contains 1 column as
                evaluation timestamp. The timestamp must be within the horizon
                of the model, which by default is 1000 data points.
            y (bigframes.dataframe.DataFrame or bigframes.series.Series
            or pandas.core.frame.DataFrame or pandas.core.series.Series):
                A dataframe or series only contains 1 column as
                evaluation numeric values.
            id_col (Optional[bigframes.dataframe.DataFrame]
            or Optional[bigframes.series.Series]
            or Optional[pandas.core.frame.DataFrame]
            or Optional[pandas.core.series.Series]
            or None, default None):
                An optional dataframe or series contains at least 1 column as
                evaluation id column.

        Returns:
            bigframes.dataframe.DataFrame: A DataFrame as evaluation result.
        """
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before score")
        X, y = utils.batch_convert_to_dataframe(X, y, session=self._bqml_model.session)

        input_data = X.join(y, how="outer")
        if id_col is not None:
            (id_col,) = utils.batch_convert_to_dataframe(id_col)
            input_data = input_data.join(id_col, how="outer")

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
                The name of the model.
            replace (bool, default False):
                Determine whether to replace if the model already exists. Default to False.

        Returns:
            ARIMAPlus: Saved model."""
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before it can be saved")

        new_model = self._bqml_model.copy(model_name, replace)
        return new_model.session.read_gbq_model(model_name)
