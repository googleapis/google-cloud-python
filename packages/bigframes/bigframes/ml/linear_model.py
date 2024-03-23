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

from typing import Dict, List, Literal, Optional, Union

import bigframes_vendored.sklearn.linear_model._base
import bigframes_vendored.sklearn.linear_model._logistic
from google.cloud import bigquery

import bigframes
import bigframes.constants as constants
from bigframes.core import log_adapter
from bigframes.ml import base, core, globals, utils
import bigframes.pandas as bpd

_BQML_PARAMS_MAPPING = {
    "optimize_strategy": "optimizationStrategy",
    "fit_intercept": "fitIntercept",
    "l1_reg": "l1Regularization",
    "l2_reg": "l2Regularization",
    "max_iterations": "maxIterations",
    "learning_rate_strategy": "learnRateStrategy",
    "learning_rate": "learnRate",
    "tol": "minRelativeProgress",
    "ls_init_learning_rate": "initialLearnRate",
    "warm_start": "warmStart",
    "calculate_p_values": "calculatePValues",
    "enable_global_explain": "enableGlobalExplain",
    "category_encoding_method": "categoryEncodingMethod",
}


@log_adapter.class_logger
class LinearRegression(
    base.SupervisedTrainablePredictor,
    bigframes_vendored.sklearn.linear_model._base.LinearRegression,
):
    __doc__ = bigframes_vendored.sklearn.linear_model._base.LinearRegression.__doc__

    def __init__(
        self,
        *,
        optimize_strategy: Literal[
            "auto_strategy", "batch_gradient_descent", "normal_equation"
        ] = "auto_strategy",
        fit_intercept: bool = True,
        l1_reg: Optional[float] = None,
        l2_reg: float = 0.0,
        max_iterations: int = 20,
        warm_start: bool = False,
        learning_rate: Optional[float] = None,
        learning_rate_strategy: Literal["line_search", "constant"] = "line_search",
        tol: float = 0.01,
        ls_init_learning_rate: Optional[float] = None,
        calculate_p_values: bool = False,
        enable_global_explain: bool = False,
    ):
        self.optimize_strategy = optimize_strategy
        self.fit_intercept = fit_intercept
        self.l1_reg = l1_reg
        self.l2_reg = l2_reg
        self.max_iterations = max_iterations
        self.warm_start = warm_start
        self.learning_rate = learning_rate
        self.learning_rate_strategy = learning_rate_strategy
        self.tol = tol
        self.ls_init_learning_rate = ls_init_learning_rate
        self.calculate_p_values = calculate_p_values
        self.enable_global_explain = enable_global_explain
        self._bqml_model: Optional[core.BqmlModel] = None
        self._bqml_model_factory = globals.bqml_model_factory()

    @classmethod
    def _from_bq(
        cls, session: bigframes.Session, model: bigquery.Model
    ) -> LinearRegression:
        assert model.model_type == "LINEAR_REGRESSION"

        # TODO(bmil): construct a standard way to extract these properties
        kwargs = {}

        # See https://cloud.google.com/bigquery/docs/reference/rest/v2/models#trainingrun
        last_fitting = model.training_runs[-1]["trainingOptions"]

        dummy_linear = cls()
        for bf_param, bf_value in dummy_linear.__dict__.items():
            bqml_param = _BQML_PARAMS_MAPPING.get(bf_param)
            if bqml_param in last_fitting:
                # Convert types
                kwargs[bf_param] = (
                    float(last_fitting[bqml_param])
                    if bf_param in ["l1_reg", "learning_rate", "ls_init_learning_rate"]
                    else type(bf_value)(last_fitting[bqml_param])
                )

        new_linear_regression = cls(**kwargs)
        new_linear_regression._bqml_model = core.BqmlModel(session, model)
        return new_linear_regression

    @property
    def _bqml_options(self) -> dict:
        """The model options as they will be set for BQML"""
        options = {
            "model_type": "LINEAR_REG",
            "data_split_method": "NO_SPLIT",
            "optimize_strategy": self.optimize_strategy,
            "fit_intercept": self.fit_intercept,
            "l2_reg": self.l2_reg,
            "max_iterations": self.max_iterations,
            "learn_rate_strategy": self.learning_rate_strategy,
            "min_rel_progress": self.tol,
            "calculate_p_values": self.calculate_p_values,
            "enable_global_explain": self.enable_global_explain,
        }
        if self.l1_reg is not None:
            options["l1_reg"] = self.l1_reg
        if self.learning_rate is not None:
            options["learn_rate"] = self.learning_rate
        if self.ls_init_learning_rate is not None:
            options["ls_init_learn_rate"] = self.ls_init_learning_rate
        # Even presenting warm_start returns error for NORMAL_EQUATION optimizer
        if self.warm_start:
            options["warm_start"] = self.warm_start

        return options

    def _fit(
        self,
        X: Union[bpd.DataFrame, bpd.Series],
        y: Union[bpd.DataFrame, bpd.Series],
        transforms: Optional[List[str]] = None,
    ) -> LinearRegression:
        X, y = utils.convert_to_dataframe(X, y)

        self._bqml_model = self._bqml_model_factory.create_model(
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

        return self._bqml_model.predict(X)

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


@log_adapter.class_logger
class LogisticRegression(
    base.SupervisedTrainablePredictor,
    bigframes_vendored.sklearn.linear_model._logistic.LogisticRegression,
):
    __doc__ = (
        bigframes_vendored.sklearn.linear_model._logistic.LogisticRegression.__doc__
    )

    # TODO(ashleyxu) support class_weight in the constructor.
    def __init__(
        self,
        *,
        optimize_strategy: Literal[
            "auto_strategy", "batch_gradient_descent", "normal_equation"
        ] = "auto_strategy",
        fit_intercept: bool = True,
        l1_reg: Optional[float] = None,
        l2_reg: float = 0.0,
        max_iterations: int = 20,
        warm_start: bool = False,
        learning_rate: Optional[float] = None,
        learning_rate_strategy: Literal["line_search", "constant"] = "line_search",
        tol: float = 0.01,
        ls_init_learning_rate: Optional[float] = None,
        calculate_p_values: bool = False,
        enable_global_explain: bool = False,
        class_weight: Optional[Union[Literal["balanced"], Dict[str, float]]] = None,
    ):
        self.optimize_strategy = optimize_strategy
        self.fit_intercept = fit_intercept
        self.l1_reg = l1_reg
        self.l2_reg = l2_reg
        self.max_iterations = max_iterations
        self.warm_start = warm_start
        self.learning_rate = learning_rate
        self.learning_rate_strategy = learning_rate_strategy
        self.tol = tol
        self.ls_init_learning_rate = ls_init_learning_rate
        self.calculate_p_values = calculate_p_values
        self.enable_global_explain = enable_global_explain
        self.class_weight = class_weight
        self._auto_class_weight = class_weight == "balanced"
        self._bqml_model: Optional[core.BqmlModel] = None
        self._bqml_model_factory = globals.bqml_model_factory()

    @classmethod
    def _from_bq(
        cls, session: bigframes.Session, model: bigquery.Model
    ) -> LogisticRegression:
        assert model.model_type == "LOGISTIC_REGRESSION"

        kwargs = {}

        # See https://cloud.google.com/bigquery/docs/reference/rest/v2/models#trainingrun
        last_fitting = model.training_runs[-1]["trainingOptions"]
        dummy_logistic = cls()
        for bf_param, bf_value in dummy_logistic.__dict__.items():
            bqml_param = _BQML_PARAMS_MAPPING.get(bf_param)
            if bqml_param in last_fitting:
                # Convert types
                kwargs[bf_param] = (
                    float(last_fitting[bqml_param])
                    if bf_param in ["l1_reg", "learning_rate", "ls_init_learning_rate"]
                    else type(bf_value)(last_fitting[bqml_param])
                )
        if last_fitting["autoClassWeights"]:
            kwargs["class_weight"] = "balanced"
        # TODO(ashleyxu) support class_weight in the constructor.
        # if "labelClassWeights" in last_fitting:
        #     kwargs["class_weight"] = last_fitting["labelClassWeights"]

        new_logistic_regression = cls(**kwargs)
        new_logistic_regression._bqml_model = core.BqmlModel(session, model)
        return new_logistic_regression

    @property
    def _bqml_options(self) -> dict:
        """The model options as they will be set for BQML"""
        options = {
            "model_type": "LOGISTIC_REG",
            "data_split_method": "NO_SPLIT",
            "fit_intercept": self.fit_intercept,
            "auto_class_weights": self._auto_class_weight,
            "optimize_strategy": self.optimize_strategy,
            "l2_reg": self.l2_reg,
            "max_iterations": self.max_iterations,
            "learn_rate_strategy": self.learning_rate_strategy,
            "min_rel_progress": self.tol,
            "calculate_p_values": self.calculate_p_values,
            "enable_global_explain": self.enable_global_explain,
            # TODO(ashleyxu): support class_weight (struct array as dict in our API)
            # "class_weight": self.class_weight,
        }
        if self.l1_reg is not None:
            options["l1_reg"] = self.l1_reg
        if self.learning_rate is not None:
            options["learn_rate"] = self.learning_rate
        if self.ls_init_learning_rate is not None:
            options["ls_init_learn_rate"] = self.ls_init_learning_rate
        # Even presenting warm_start returns error for NORMAL_EQUATION optimizer
        if self.warm_start:
            options["warm_start"] = self.warm_start

        return options

    def _fit(
        self,
        X: Union[bpd.DataFrame, bpd.Series],
        y: Union[bpd.DataFrame, bpd.Series],
        transforms: Optional[List[str]] = None,
    ) -> LogisticRegression:
        """Fit model with transforms."""
        X, y = utils.convert_to_dataframe(X, y)

        self._bqml_model = self._bqml_model_factory.create_model(
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

        return self._bqml_model.predict(X)

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

        # TODO(ashleyxu): support class_weight (struct array as dict in our API)
        if self.class_weight not in (None, "balanced"):
            raise NotImplementedError(
                f"class_weight is not supported yet. {constants.FEEDBACK_LINK}"
            )

        new_model = self._bqml_model.copy(model_name, replace)
        return new_model.session.read_gbq_model(model_name)
