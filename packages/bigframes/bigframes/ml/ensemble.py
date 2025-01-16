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

"""Ensemble models. This module is styled after scikit-learn's ensemble module:
https://scikit-learn.org/stable/modules/ensemble.html"""

from __future__ import annotations

from typing import Dict, List, Literal, Optional

import bigframes_vendored.sklearn.ensemble._forest
import bigframes_vendored.xgboost.sklearn
from google.cloud import bigquery

from bigframes.core import log_adapter
import bigframes.dataframe
from bigframes.ml import base, core, globals, utils
import bigframes.session

_BQML_PARAMS_MAPPING = {
    "booster": "boosterType",
    "dart_normalized_type": "dartNormalizeType",
    "tree_method": "treeMethod",
    "colsample_bytree": "colsampleBytree",
    "colsample_bylevel": "colsampleBylevel",
    "colsample_bynode": "colsampleBynode",
    "gamma": "minSplitLoss",
    "subsample": "subsample",
    "reg_alpha": "l1Regularization",
    "reg_lambda": "l2Regularization",
    "learning_rate": "learnRate",
    "tol": "minRelativeProgress",
    "n_estimators": "numParallelTree",
    "min_tree_child_weight": "minTreeChildWeight",
    "max_depth": "maxTreeDepth",
    "max_iterations": "maxIterations",
    "enable_global_explain": "enableGlobalExplain",
    "xgboost_version": "xgboostVersion",
}


@log_adapter.class_logger
class XGBRegressor(
    base.SupervisedTrainableWithEvaluationPredictor,
    bigframes_vendored.xgboost.sklearn.XGBRegressor,
):
    __doc__ = bigframes_vendored.xgboost.sklearn.XGBRegressor.__doc__

    def __init__(
        self,
        n_estimators: int = 1,
        *,
        booster: Literal["gbtree", "dart"] = "gbtree",
        dart_normalized_type: Literal["tree", "forest"] = "tree",
        tree_method: Literal["auto", "exact", "approx", "hist"] = "auto",
        min_tree_child_weight: int = 1,
        colsample_bytree: float = 1.0,
        colsample_bylevel: float = 1.0,
        colsample_bynode: float = 1.0,
        gamma: float = 0.0,
        max_depth: int = 6,
        subsample: float = 1.0,
        reg_alpha: float = 0.0,
        reg_lambda: float = 1.0,
        learning_rate: float = 0.3,
        max_iterations: int = 20,
        tol: float = 0.01,
        enable_global_explain: bool = False,
        xgboost_version: Literal["0.9", "1.1"] = "0.9",
    ):
        self.n_estimators = n_estimators
        self.booster = booster
        self.dart_normalized_type = dart_normalized_type
        self.tree_method = tree_method
        self.min_tree_child_weight = min_tree_child_weight
        self.colsample_bytree = colsample_bytree
        self.colsample_bylevel = colsample_bylevel
        self.colsample_bynode = colsample_bynode
        self.gamma = gamma
        self.max_depth = max_depth
        self.subsample = subsample
        self.reg_alpha = reg_alpha
        self.reg_lambda = reg_lambda
        self.learning_rate = learning_rate
        self.max_iterations = max_iterations
        self.tol = tol
        self.enable_global_explain = enable_global_explain
        self.xgboost_version = xgboost_version
        self._bqml_model: Optional[core.BqmlModel] = None
        self._bqml_model_factory = globals.bqml_model_factory()

    @classmethod
    def _from_bq(
        cls, session: bigframes.session.Session, bq_model: bigquery.Model
    ) -> XGBRegressor:
        assert bq_model.model_type == "BOOSTED_TREE_REGRESSOR"

        kwargs = utils.retrieve_params_from_bq_model(
            cls, bq_model, _BQML_PARAMS_MAPPING
        )

        model = cls(**kwargs)
        model._bqml_model = core.BqmlModel(session, bq_model)
        return model

    @property
    def _bqml_options(self) -> Dict[str, str | int | bool | float | List[str]]:
        """The model options as they will be set for BQML"""
        return {
            "model_type": "BOOSTED_TREE_REGRESSOR",
            "data_split_method": "NO_SPLIT",
            "early_stop": True,
            "num_parallel_tree": self.n_estimators,
            "booster_type": self.booster,
            "tree_method": self.tree_method,
            "min_tree_child_weight": self.min_tree_child_weight,
            "colsample_bytree": self.colsample_bytree,
            "colsample_bylevel": self.colsample_bylevel,
            "colsample_bynode": self.colsample_bynode,
            "min_split_loss": self.gamma,
            "max_tree_depth": self.max_depth,
            "subsample": self.subsample,
            "l1_reg": self.reg_alpha,
            "l2_reg": self.reg_lambda,
            "learn_rate": self.learning_rate,
            "max_iterations": self.max_iterations,
            "min_rel_progress": self.tol,
            "enable_global_explain": self.enable_global_explain,
            "xgboost_version": self.xgboost_version,
        }

    def _fit(
        self,
        X: utils.ArrayType,
        y: utils.ArrayType,
        transforms: Optional[List[str]] = None,
        X_eval: Optional[utils.ArrayType] = None,
        y_eval: Optional[utils.ArrayType] = None,
    ) -> XGBRegressor:
        X, y = utils.batch_convert_to_dataframe(X, y)

        bqml_options = self._bqml_options

        if X_eval is not None and y_eval is not None:
            X_eval, y_eval = utils.batch_convert_to_dataframe(X_eval, y_eval)
            X, y, bqml_options = utils.combine_training_and_evaluation_data(
                X, y, X_eval, y_eval, bqml_options
            )

        self._bqml_model = self._bqml_model_factory.create_model(
            X,
            y,
            transforms=transforms,
            options=bqml_options,
        )
        return self

    def predict(
        self,
        X: utils.ArrayType,
    ) -> bigframes.dataframe.DataFrame:
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before predict")
        (X,) = utils.batch_convert_to_dataframe(X, session=self._bqml_model.session)

        return self._bqml_model.predict(X)

    def score(
        self,
        X: utils.ArrayType,
        y: utils.ArrayType,
    ):
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before score")

        X, y = utils.batch_convert_to_dataframe(X, y, session=self._bqml_model.session)

        input_data = (
            X.join(y, how="outer") if (X is not None) and (y is not None) else None
        )
        return self._bqml_model.evaluate(input_data)

    def to_gbq(self, model_name: str, replace: bool = False) -> XGBRegressor:
        """Save the model to BigQuery.

        Args:
            model_name (str):
                The name of the model.
            replace (bool, default False):
                Determine whether to replace if the model already exists. Default to False.

        Returns: Saved model."""
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before it can be saved")

        new_model = self._bqml_model.copy(model_name, replace)
        return new_model.session.read_gbq_model(model_name)


@log_adapter.class_logger
class XGBClassifier(
    base.SupervisedTrainableWithEvaluationPredictor,
    bigframes_vendored.xgboost.sklearn.XGBClassifier,
):

    __doc__ = bigframes_vendored.xgboost.sklearn.XGBClassifier.__doc__

    def __init__(
        self,
        n_estimators: int = 1,
        *,
        booster: Literal["gbtree", "dart"] = "gbtree",
        dart_normalized_type: Literal["tree", "forest"] = "tree",
        tree_method: Literal["auto", "exact", "approx", "hist"] = "auto",
        min_tree_child_weight: int = 1,
        colsample_bytree: float = 1.0,
        colsample_bylevel: float = 1.0,
        colsample_bynode: float = 1.0,
        gamma: float = 0.0,
        max_depth: int = 6,
        subsample: float = 1.0,
        reg_alpha: float = 0.0,
        reg_lambda: float = 1.0,
        learning_rate: float = 0.3,
        max_iterations: int = 20,
        tol: float = 0.01,
        enable_global_explain: bool = False,
        xgboost_version: Literal["0.9", "1.1"] = "0.9",
    ):
        self.n_estimators = n_estimators
        self.booster = booster
        self.dart_normalized_type = dart_normalized_type
        self.tree_method = tree_method
        self.min_tree_child_weight = min_tree_child_weight
        self.colsample_bytree = colsample_bytree
        self.colsample_bylevel = colsample_bylevel
        self.colsample_bynode = colsample_bynode
        self.gamma = gamma
        self.max_depth = max_depth
        self.subsample = subsample
        self.reg_alpha = reg_alpha
        self.reg_lambda = reg_lambda
        self.learning_rate = learning_rate
        self.max_iterations = max_iterations
        self.tol = tol
        self.enable_global_explain = enable_global_explain
        self.xgboost_version = xgboost_version
        self._bqml_model: Optional[core.BqmlModel] = None
        self._bqml_model_factory = globals.bqml_model_factory()

    @classmethod
    def _from_bq(
        cls, session: bigframes.session.Session, bq_model: bigquery.Model
    ) -> XGBClassifier:
        assert bq_model.model_type == "BOOSTED_TREE_CLASSIFIER"

        kwargs = utils.retrieve_params_from_bq_model(
            cls, bq_model, _BQML_PARAMS_MAPPING
        )

        model = cls(**kwargs)
        model._bqml_model = core.BqmlModel(session, bq_model)
        return model

    @property
    def _bqml_options(self) -> Dict[str, str | int | bool | float | List[str]]:
        """The model options as they will be set for BQML"""
        return {
            "model_type": "BOOSTED_TREE_CLASSIFIER",
            "data_split_method": "NO_SPLIT",
            "early_stop": True,
            "num_parallel_tree": self.n_estimators,
            "booster_type": self.booster,
            "tree_method": self.tree_method,
            "min_tree_child_weight": self.min_tree_child_weight,
            "colsample_bytree": self.colsample_bytree,
            "colsample_bylevel": self.colsample_bylevel,
            "colsample_bynode": self.colsample_bynode,
            "min_split_loss": self.gamma,
            "max_tree_depth": self.max_depth,
            "subsample": self.subsample,
            "l1_reg": self.reg_alpha,
            "l2_reg": self.reg_lambda,
            "learn_rate": self.learning_rate,
            "max_iterations": self.max_iterations,
            "min_rel_progress": self.tol,
            "enable_global_explain": self.enable_global_explain,
            "xgboost_version": self.xgboost_version,
        }

    def _fit(
        self,
        X: utils.ArrayType,
        y: utils.ArrayType,
        transforms: Optional[List[str]] = None,
        X_eval: Optional[utils.ArrayType] = None,
        y_eval: Optional[utils.ArrayType] = None,
    ) -> XGBClassifier:
        X, y = utils.batch_convert_to_dataframe(X, y)

        bqml_options = self._bqml_options

        if X_eval is not None and y_eval is not None:
            X_eval, y_eval = utils.batch_convert_to_dataframe(X_eval, y_eval)
            X, y, bqml_options = utils.combine_training_and_evaluation_data(
                X, y, X_eval, y_eval, bqml_options
            )

        self._bqml_model = self._bqml_model_factory.create_model(
            X,
            y,
            transforms=transforms,
            options=bqml_options,
        )
        return self

    def predict(self, X: utils.ArrayType) -> bigframes.dataframe.DataFrame:
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before predict")
        (X,) = utils.batch_convert_to_dataframe(X, session=self._bqml_model.session)

        return self._bqml_model.predict(X)

    def score(
        self,
        X: utils.ArrayType,
        y: utils.ArrayType,
    ):
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before score")

        X, y = utils.batch_convert_to_dataframe(X, y, session=self._bqml_model.session)

        input_data = (
            X.join(y, how="outer") if (X is not None) and (y is not None) else None
        )
        return self._bqml_model.evaluate(input_data)

    def to_gbq(self, model_name: str, replace: bool = False) -> XGBClassifier:
        """Save the model to BigQuery.

        Args:
            model_name (str):
                The name of the model.
            replace (bool, default False):
                Determine whether to replace if the model already exists. Default to False.

        Returns:
            XGBClassifier: Saved model."""
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before it can be saved")

        new_model = self._bqml_model.copy(model_name, replace)
        return new_model.session.read_gbq_model(model_name)


@log_adapter.class_logger
class RandomForestRegressor(
    base.SupervisedTrainableWithEvaluationPredictor,
    bigframes_vendored.sklearn.ensemble._forest.RandomForestRegressor,
):

    __doc__ = bigframes_vendored.sklearn.ensemble._forest.RandomForestRegressor.__doc__

    def __init__(
        self,
        n_estimators: int = 100,
        *,
        tree_method: Literal["auto", "exact", "approx", "hist"] = "auto",
        min_tree_child_weight: int = 1,
        colsample_bytree: float = 1.0,
        colsample_bylevel: float = 1.0,
        colsample_bynode: float = 0.8,
        gamma: float = 0.0,
        max_depth: int = 15,
        subsample: float = 0.8,
        reg_alpha: float = 0.0,
        reg_lambda: float = 1.0,
        tol: float = 0.01,
        enable_global_explain: bool = False,
        xgboost_version: Literal["0.9", "1.1"] = "0.9",
    ):
        self.n_estimators = n_estimators
        self.tree_method = tree_method
        self.min_tree_child_weight = min_tree_child_weight
        self.colsample_bytree = colsample_bytree
        self.colsample_bylevel = colsample_bylevel
        self.colsample_bynode = colsample_bynode
        self.gamma = gamma
        self.max_depth = max_depth
        self.subsample = subsample
        self.reg_alpha = reg_alpha
        self.reg_lambda = reg_lambda
        self.tol = tol
        self.enable_global_explain = enable_global_explain
        self.xgboost_version = xgboost_version
        self._bqml_model: Optional[core.BqmlModel] = None
        self._bqml_model_factory = globals.bqml_model_factory()

    @classmethod
    def _from_bq(
        cls, session: bigframes.session.Session, bq_model: bigquery.Model
    ) -> RandomForestRegressor:
        assert bq_model.model_type == "RANDOM_FOREST_REGRESSOR"

        kwargs = utils.retrieve_params_from_bq_model(
            cls, bq_model, _BQML_PARAMS_MAPPING
        )

        model = cls(**kwargs)
        model._bqml_model = core.BqmlModel(session, bq_model)
        return model

    @property
    def _bqml_options(self) -> Dict[str, str | int | bool | float | List[str]]:
        """The model options as they will be set for BQML"""
        return {
            "model_type": "RANDOM_FOREST_REGRESSOR",
            "early_stop": True,
            "num_parallel_tree": self.n_estimators,
            "tree_method": self.tree_method,
            "min_tree_child_weight": self.min_tree_child_weight,
            "colsample_bytree": self.colsample_bytree,
            "colsample_bylevel": self.colsample_bylevel,
            "colsample_bynode": self.colsample_bynode,
            "min_split_loss": self.gamma,
            "max_tree_depth": self.max_depth,
            "subsample": self.subsample,
            "l1_reg": self.reg_alpha,
            "l2_reg": self.reg_lambda,
            "min_rel_progress": self.tol,
            "data_split_method": "NO_SPLIT",
            "enable_global_explain": self.enable_global_explain,
            "xgboost_version": self.xgboost_version,
        }

    def _fit(
        self,
        X: utils.ArrayType,
        y: utils.ArrayType,
        transforms: Optional[List[str]] = None,
        X_eval: Optional[utils.ArrayType] = None,
        y_eval: Optional[utils.ArrayType] = None,
    ) -> RandomForestRegressor:
        X, y = utils.batch_convert_to_dataframe(X, y)

        bqml_options = self._bqml_options

        if X_eval is not None and y_eval is not None:
            X_eval, y_eval = utils.batch_convert_to_dataframe(X_eval, y_eval)
            X, y, bqml_options = utils.combine_training_and_evaluation_data(
                X, y, X_eval, y_eval, bqml_options
            )

        self._bqml_model = self._bqml_model_factory.create_model(
            X,
            y,
            transforms=transforms,
            options=bqml_options,
        )
        return self

    def predict(
        self,
        X: utils.ArrayType,
    ) -> bigframes.dataframe.DataFrame:
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before predict")
        (X,) = utils.batch_convert_to_dataframe(X, session=self._bqml_model.session)

        return self._bqml_model.predict(X)

    def score(
        self,
        X: utils.ArrayType,
        y: utils.ArrayType,
    ):
        """Calculate evaluation metrics of the model.

        .. note::

            Output matches that of the BigQuery ML.EVALUATE function.
            See: https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate#regression_models
            for the outputs relevant to this model type.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series):
                A BigQuery DataFrame as evaluation data.
            y (bigframes.dataframe.DataFrame or bigframes.series.Series):
                A BigQuery DataFrame as evaluation labels.

        Returns:
            bigframes.dataframe.DataFrame: The DataFrame as evaluation result.
        """
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before score")

        X, y = utils.batch_convert_to_dataframe(X, y, session=self._bqml_model.session)

        input_data = (
            X.join(y, how="outer") if (X is not None) and (y is not None) else None
        )
        return self._bqml_model.evaluate(input_data)

    def to_gbq(self, model_name: str, replace: bool = False) -> RandomForestRegressor:
        """Save the model to BigQuery.

        Args:
            model_name (str):
                The name of the model.
            replace (bool, default False):
                Determine whether to replace if the model already exists. Default to False.

        Returns:
            RandomForestRegressor: Saved model."""
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before it can be saved")

        new_model = self._bqml_model.copy(model_name, replace)
        return new_model.session.read_gbq_model(model_name)


@log_adapter.class_logger
class RandomForestClassifier(
    base.SupervisedTrainableWithEvaluationPredictor,
    bigframes_vendored.sklearn.ensemble._forest.RandomForestClassifier,
):

    __doc__ = bigframes_vendored.sklearn.ensemble._forest.RandomForestClassifier.__doc__

    def __init__(
        self,
        n_estimators: int = 100,
        *,
        tree_method: Literal["auto", "exact", "approx", "hist"] = "auto",
        min_tree_child_weight: int = 1,
        colsample_bytree: float = 1.0,
        colsample_bylevel: float = 1.0,
        colsample_bynode: float = 0.8,
        gamma: float = 0.00,
        max_depth: int = 15,
        subsample: float = 0.8,
        reg_alpha: float = 0.0,
        reg_lambda: float = 1.0,
        tol: float = 0.01,
        enable_global_explain: bool = False,
        xgboost_version: Literal["0.9", "1.1"] = "0.9",
    ):
        self.n_estimators = n_estimators
        self.tree_method = tree_method
        self.min_tree_child_weight = min_tree_child_weight
        self.colsample_bytree = colsample_bytree
        self.colsample_bylevel = colsample_bylevel
        self.colsample_bynode = colsample_bynode
        self.gamma = gamma
        self.max_depth = max_depth
        self.subsample = subsample
        self.reg_alpha = reg_alpha
        self.reg_lambda = reg_lambda
        self.tol = tol
        self.enable_global_explain = enable_global_explain
        self.xgboost_version = xgboost_version
        self._bqml_model: Optional[core.BqmlModel] = None
        self._bqml_model_factory = globals.bqml_model_factory()

    @classmethod
    def _from_bq(
        cls, session: bigframes.session.Session, bq_model: bigquery.Model
    ) -> RandomForestClassifier:
        assert bq_model.model_type == "RANDOM_FOREST_CLASSIFIER"

        kwargs = utils.retrieve_params_from_bq_model(
            cls, bq_model, _BQML_PARAMS_MAPPING
        )

        model = cls(**kwargs)
        model._bqml_model = core.BqmlModel(session, bq_model)
        return model

    @property
    def _bqml_options(self) -> Dict[str, str | int | bool | float | List[str]]:
        """The model options as they will be set for BQML"""
        return {
            "model_type": "RANDOM_FOREST_CLASSIFIER",
            "early_stop": True,
            "num_parallel_tree": self.n_estimators,
            "tree_method": self.tree_method,
            "min_tree_child_weight": self.min_tree_child_weight,
            "colsample_bytree": self.colsample_bytree,
            "colsample_bylevel": self.colsample_bylevel,
            "colsample_bynode": self.colsample_bynode,
            "min_split_loss": self.gamma,
            "max_tree_depth": self.max_depth,
            "subsample": self.subsample,
            "l1_reg": self.reg_alpha,
            "l2_reg": self.reg_lambda,
            "min_rel_progress": self.tol,
            "data_split_method": "NO_SPLIT",
            "enable_global_explain": self.enable_global_explain,
            "xgboost_version": self.xgboost_version,
        }

    def _fit(
        self,
        X: utils.ArrayType,
        y: utils.ArrayType,
        transforms: Optional[List[str]] = None,
        X_eval: Optional[utils.ArrayType] = None,
        y_eval: Optional[utils.ArrayType] = None,
    ) -> RandomForestClassifier:
        X, y = utils.batch_convert_to_dataframe(X, y)

        bqml_options = self._bqml_options

        if X_eval is not None and y_eval is not None:
            X_eval, y_eval = utils.batch_convert_to_dataframe(X_eval, y_eval)
            X, y, bqml_options = utils.combine_training_and_evaluation_data(
                X, y, X_eval, y_eval, bqml_options
            )

        self._bqml_model = self._bqml_model_factory.create_model(
            X,
            y,
            transforms=transforms,
            options=bqml_options,
        )
        return self

    def predict(
        self,
        X: utils.ArrayType,
    ) -> bigframes.dataframe.DataFrame:
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before predict")
        (X,) = utils.batch_convert_to_dataframe(X, session=self._bqml_model.session)

        return self._bqml_model.predict(X)

    def score(
        self,
        X: utils.ArrayType,
        y: utils.ArrayType,
    ):
        """Calculate evaluation metrics of the model.

        .. note::

            Output matches that of the BigQuery ML.EVALUATE function.
            See: https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate#classification_models
            for the outputs relevant to this model type.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series):
                A BigQuery DataFrame as evaluation data.
            y (bigframes.dataframe.DataFrame or bigframes.series.Series):
                A BigQuery DataFrame as evaluation labels.

        Returns:
            bigframes.dataframe.DataFrame: The DataFrame as evaluation result.
        """
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before score")

        X, y = utils.batch_convert_to_dataframe(X, y, session=self._bqml_model.session)

        input_data = (
            X.join(y, how="outer") if (X is not None) and (y is not None) else None
        )
        return self._bqml_model.evaluate(input_data)

    def to_gbq(self, model_name: str, replace: bool = False) -> RandomForestClassifier:
        """Save the model to BigQuery.

        Args:
            model_name (str):
                The name of the model.
            replace (bool, default False):
                Determine whether to replace if the model already exists. Default to False.

        Returns:
            RandomForestClassifier: Saved model."""
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before it can be saved")

        new_model = self._bqml_model.copy(model_name, replace)
        return new_model.session.read_gbq_model(model_name)
