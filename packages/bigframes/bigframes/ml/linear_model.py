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

"""Linear models. This module is styled after Scikit-Learn's linear_model module:
https://scikit-learn.org/stable/modules/linear_model.html"""

from __future__ import annotations

from typing import cast, Dict, List, Optional, TYPE_CHECKING

from google.cloud import bigquery

if TYPE_CHECKING:
    import bigframes

import bigframes.ml.base
import bigframes.ml.core
import third_party.bigframes_vendored.sklearn.linear_model._base
import third_party.bigframes_vendored.sklearn.linear_model._logistic


class LinearRegression(
    third_party.bigframes_vendored.sklearn.linear_model._base.LinearRegression,
    bigframes.ml.base.TrainablePredictor,
):
    __doc__ = (
        third_party.bigframes_vendored.sklearn.linear_model._base.LinearRegression.__doc__
    )

    def __init__(
        self,
        fit_intercept=True,
    ):
        self.fit_intercept = fit_intercept
        self._bqml_model: Optional[bigframes.ml.core.BqmlModel] = None

    @staticmethod
    def _from_bq(session: bigframes.Session, model: bigquery.Model) -> LinearRegression:
        assert model.model_type == "LINEAR_REGRESSION"

        # TODO(bmil): construct a standard way to extract these properties
        kwargs = {}

        # See https://cloud.google.com/bigquery/docs/reference/rest/v2/models#trainingrun
        last_fitting = model.training_runs[-1]["trainingOptions"]
        if "fitIntercept" in last_fitting:
            kwargs["fit_intercept"] = last_fitting["fitIntercept"]

        new_linear_regression = LinearRegression(**kwargs)
        new_linear_regression._bqml_model = bigframes.ml.core.BqmlModel(session, model)
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
        X: bigframes.dataframe.DataFrame,
        y: bigframes.dataframe.DataFrame,
        transforms: Optional[List[str]] = None,
    ):
        self._bqml_model = bigframes.ml.core.create_bqml_model(
            X,
            y,
            transforms=transforms,
            options=self._bqml_options,
        )

    def predict(
        self, X: bigframes.dataframe.DataFrame
    ) -> bigframes.dataframe.DataFrame:
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before predict")

        df = self._bqml_model.predict(X)
        return cast(
            bigframes.dataframe.DataFrame,
            df[
                [
                    cast(str, field.name)
                    for field in self._bqml_model.model.label_columns
                ]
            ],
        )

    def score(
        self,
        X: bigframes.dataframe.DataFrame,
        y: bigframes.dataframe.DataFrame,
    ) -> bigframes.dataframe.DataFrame:
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before score")

        input_data = (
            X.join(y, how="outer") if (X is not None) and (y is not None) else None
        )
        return self._bqml_model.evaluate(input_data)

    def to_gbq(self, model_name: str, replace: bool = False) -> LinearRegression:
        """Save the model to Google Cloud BigQuey.

        Args:
            model_name: the name of the model.
            replace: whether to replace if the model already exists. Default to False.

        Returns: saved model."""
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before it can be saved")

        new_model = self._bqml_model.copy(model_name, replace)
        return new_model.session.read_gbq_model(model_name)


class LogisticRegression(
    third_party.bigframes_vendored.sklearn.linear_model._logistic.LogisticRegression,
    bigframes.ml.base.TrainablePredictor,
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
        self._bqml_model: Optional[bigframes.ml.core.BqmlModel] = None

    @staticmethod
    def _from_bq(
        session: bigframes.Session, model: bigquery.Model
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

        new_logistic_regression = LogisticRegression(**kwargs)
        new_logistic_regression._bqml_model = bigframes.ml.core.BqmlModel(
            session, model
        )
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
        X: bigframes.dataframe.DataFrame,
        y: bigframes.dataframe.DataFrame,
        transforms: Optional[List[str]] = None,
    ):
        self._bqml_model = bigframes.ml.core.create_bqml_model(
            X,
            y,
            transforms=transforms,
            options=self._bqml_options,
        )

    def predict(
        self, X: bigframes.dataframe.DataFrame
    ) -> bigframes.dataframe.DataFrame:
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before predict")

        df = self._bqml_model.predict(X)
        return cast(
            bigframes.dataframe.DataFrame,
            df[
                [
                    cast(str, field.name)
                    for field in self._bqml_model.model.label_columns
                ]
            ],
        )

    def score(
        self,
        X: bigframes.dataframe.DataFrame,
        y: bigframes.dataframe.DataFrame,
    ) -> bigframes.dataframe.DataFrame:
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before score")

        input_data = (
            X.join(y, how="outer") if (X is not None) and (y is not None) else None
        )
        return self._bqml_model.evaluate(input_data)

    def to_gbq(self, model_name: str, replace: bool = False) -> LogisticRegression:
        """Save the model to Google Cloud BigQuey.

        Args:
            model_name: the name of the model.
            replace: whether to replace if the model already exists. Default to False.

        Returns: saved model."""
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before it can be saved")

        # TODO(ashleyxu): b/285162045 support auto_class_weights once the API is
        # fixed and enable the tests.
        if self.auto_class_weights is True:
            raise NotImplementedError("auto_class_weight is not supported yet.")

        new_model = self._bqml_model.copy(model_name, replace)
        return new_model.session.read_gbq_model(model_name)
