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

"""Linear models. This module is styled after scikit-learn's linear_model module:
https://scikit-learn.org/stable/modules/linear_model.html."""

from __future__ import annotations

from typing import cast, Dict, List, Optional, Union

from google.cloud import bigquery

import bigframes
import bigframes.constants as constants
from bigframes.ml import base, core, utils
import bigframes.pandas as bpd
import third_party.bigframes_vendored.sklearn.linear_model._base
import third_party.bigframes_vendored.sklearn.linear_model._logistic


class LinearRegression(
    third_party.bigframes_vendored.sklearn.linear_model._base.LinearRegression,
    base.TrainablePredictor,
):
    __doc__ = (
        third_party.bigframes_vendored.sklearn.linear_model._base.LinearRegression.__doc__
    )

    def __init__(
        self,
        fit_intercept=True,
    ):
        self.fit_intercept = fit_intercept
        self._bqml_model: Optional[core.BqmlModel] = None

    @classmethod
    def _from_bq(
        cls, session: bigframes.Session, model: bigquery.Model
    ) -> LinearRegression:
        assert model.model_type == "LINEAR_REGRESSION"

        # TODO(bmil): construct a standard way to extract these properties
        kwargs = {}

        # See https://cloud.google.com/bigquery/docs/reference/rest/v2/models#trainingrun
        last_fitting = model.training_runs[-1]["trainingOptions"]
        if "fitIntercept" in last_fitting:
            kwargs["fit_intercept"] = last_fitting["fitIntercept"]

        new_linear_regression = cls(**kwargs)
        new_linear_regression._bqml_model = core.BqmlModel(session, model)
        return new_linear_regression

    @property
    def _bqml_options(self) -> Dict[str, str | int | bool | float | List[str]]:
        """The model options as they will be set for BQML"""
        return {
            "model_type": "LINEAR_REG",
            "data_split_method": "NO_SPLIT",
            "fit_intercept": self.fit_intercept,
        }

    def fit(
        self,
        X: Union[bpd.DataFrame, bpd.Series],
        y: Union[bpd.DataFrame, bpd.Series],
        transforms: Optional[List[str]] = None,
    ) -> LinearRegression:
        X, y = utils.convert_to_dataframe(X, y)

        self._bqml_model = core.create_bqml_model(
            X,
            y,
            transforms=transforms,
            options=self._bqml_options,
        )
        return self

    def predict(self, X: Union[bpd.DataFrame, bpd.Series]) -> bpd.DataFrame:
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before predict")

        (X,) = utils.convert_to_dataframe(X)

        df = self._bqml_model.predict(X)
        return cast(
            bpd.DataFrame,
            df[
                [
                    cast(str, field.name)
                    for field in self._bqml_model.model.label_columns
                ]
            ],
        )

    def score(
        self,
        X: Union[bpd.DataFrame, bpd.Series],
        y: Union[bpd.DataFrame, bpd.Series],
    ) -> bpd.DataFrame:
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before score")

        X, y = utils.convert_to_dataframe(X, y)

        input_data = X.join(y, how="outer")
        return self._bqml_model.evaluate(input_data)

    def to_gbq(self, model_name: str, replace: bool = False) -> LinearRegression:
        """Save the model to BigQuery.

        Args:
            model_name (str):
                the name of the model.
            replace (bool, default False):
                whether to replace if the model already exists. Default to False.

        Returns:
            LinearRegression: saved model."""
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before it can be saved")

        new_model = self._bqml_model.copy(model_name, replace)
        return new_model.session.read_gbq_model(model_name)


class LogisticRegression(
    third_party.bigframes_vendored.sklearn.linear_model._logistic.LogisticRegression,
    base.TrainablePredictor,
):
    __doc__ = (
        third_party.bigframes_vendored.sklearn.linear_model._logistic.LogisticRegression.__doc__
    )

    # TODO(ashleyxu) support class_weights in the constructor.
    def __init__(
        self,
        fit_intercept: bool = True,
        auto_class_weights: bool = False,
    ):
        self.fit_intercept = fit_intercept
        self.auto_class_weights = auto_class_weights
        self._bqml_model: Optional[core.BqmlModel] = None

    @classmethod
    def _from_bq(
        cls, session: bigframes.Session, model: bigquery.Model
    ) -> LogisticRegression:
        assert model.model_type == "LOGISTIC_REGRESSION"

        kwargs = {}

        # See https://cloud.google.com/bigquery/docs/reference/rest/v2/models#trainingrun
        last_fitting = model.training_runs[-1]["trainingOptions"]
        if "fitIntercept" in last_fitting:
            kwargs["fit_intercept"] = last_fitting["fitIntercept"]
        # TODO(ashleyxu): b/285162045 support auto_class_weights once the API is
        # fixed and enable the tests.
        if "autoClassWeights" in last_fitting:
            kwargs["auto_class_weights"] = last_fitting["autoClassWeights"]
        # TODO(ashleyxu) support class_weights in the constructor.
        # if "labelClassWeights" in last_fitting:
        #     kwargs["class_weights"] = last_fitting["labelClassWeights"]

        new_logistic_regression = cls(**kwargs)
        new_logistic_regression._bqml_model = core.BqmlModel(session, model)
        return new_logistic_regression

    @property
    def _bqml_options(self) -> Dict[str, str | int | float | List[str]]:
        """The model options as they will be set for BQML"""
        return {
            "model_type": "LOGISTIC_REG",
            "data_split_method": "NO_SPLIT",
            "fit_intercept": self.fit_intercept,
            "auto_class_weights": self.auto_class_weights,
            # TODO(ashleyxu): support class_weights (struct array)
            # "class_weights": self.class_weights,
        }

    def fit(
        self,
        X: Union[bpd.DataFrame, bpd.Series],
        y: Union[bpd.DataFrame, bpd.Series],
        transforms: Optional[List[str]] = None,
    ) -> LogisticRegression:
        X, y = utils.convert_to_dataframe(X, y)

        self._bqml_model = core.create_bqml_model(
            X,
            y,
            transforms=transforms,
            options=self._bqml_options,
        )
        return self

    def predict(
        self,
        X: Union[bpd.DataFrame, bpd.Series],
    ) -> bpd.DataFrame:
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before predict")

        (X,) = utils.convert_to_dataframe(X)

        df = self._bqml_model.predict(X)
        return cast(
            bpd.DataFrame,
            df[
                [
                    cast(str, field.name)
                    for field in self._bqml_model.model.label_columns
                ]
            ],
        )

    def score(
        self,
        X: Union[bpd.DataFrame, bpd.Series],
        y: Union[bpd.DataFrame, bpd.Series],
    ) -> bpd.DataFrame:
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before score")

        X, y = utils.convert_to_dataframe(X, y)

        input_data = X.join(y, how="outer")
        return self._bqml_model.evaluate(input_data)

    def to_gbq(self, model_name: str, replace: bool = False) -> LogisticRegression:
        """Save the model to BigQuery.

        Args:
            model_name (str):
                the name of the model.
            replace (bool, default False):
                whether to replace if the model already exists. Default to False.

        Returns:
            LogisticRegression: saved model."""
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before it can be saved")

        # TODO(ashleyxu): b/285162045 support auto_class_weights once the API is
        # fixed and enable the tests.
        if self.auto_class_weights is True:
            raise NotImplementedError(
                f"auto_class_weight is not supported yet. {constants.FEEDBACK_LINK}"
            )

        new_model = self._bqml_model.copy(model_name, replace)
        return new_model.session.read_gbq_model(model_name)
