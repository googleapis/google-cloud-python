"""Scikit-Learn Wrapper interface for XGBoost."""

from typing import Any

from bigframes import constants

from ..sklearn.base import BaseEstimator as XGBModelBase
from ..sklearn.base import ClassifierMixin as XGBClassifierBase
from ..sklearn.base import RegressorMixin as XGBRegressorBase


class XGBModel(XGBModelBase):
    def predict(self, X):
        """Predict using the XGB model.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series):
                Series or DataFrame of shape (n_samples, n_features). Samples.

        Returns:
            bigframes.dataframe.DataFrame: DataFrame of shape (n_samples, n_input_columns + n_prediction_columns). Returns predicted values.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def fit(self, X, y):
        """Fit gradient boosting model.

        Note that calling ``fit()`` multiple times will cause the model object to be
        re-fit from scratch. To resume training from a previous checkpoint, explicitly
        pass ``xgb_model`` argument.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series):
                Series or DataFrame of shape (n_samples, n_features). Training data.

            y (bigframes.dataframe.DataFrame or bigframes.series.Series):
                DataFrame of shape (n_samples,) or (n_samples, n_targets).
                Target values. Will be cast to X's dtype if necessary.

        Returns:
            XGBModel: Fitted Estimator.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)


class XGBClassifierMixIn:
    """MixIn for classification."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)


class XGBRegressor(XGBModel, XGBRegressorBase):
    """
    XGBoost regression model.

    Args:
        num_parallel_tree (Optional[int]):
            Number of parallel trees constructed during each iteration. Default to 1.
        booster (Optional[str]):
            Specify which booster to use: gbtree or dart. Default to "gbtree".
        dart_normalized_type (Optional[str]):
            Type of normalization algorithm for DART booster. Possible values: "TREE", "FOREST". Default to "TREE".
        tree_method (Optional[str]):
            Specify which tree method to use.  Default to "auto". If this parameter is set to
            default, XGBoost will choose the most conservative option available. Possible values: ""exact", "approx",
            "hist".
        min_child_weight (Optional[float]):
            Minimum sum of instance weight(hessian) needed in a child. Default to 1.
        colsample_bytree (Optional[float]):
            Subsample ratio of columns when constructing each tree. Default to 1.0.
        colsample_bylevel (Optional[float]):
            Subsample ratio of columns for each level. Default to 1.0.
        colsample_bynode (Optional[float]):
            Subsample ratio of columns for each split. Default to 1.0.
        gamma (Optional[float]):
            (min_split_loss) Minimum loss reduction required to make a further partition on a
            leaf node of the tree. Default to 0.0.
        max_depth (Optional[int]):
            Maximum tree depth for base learners. Default to 6.
        subsample (Optional[float]):
            Subsample ratio of the training instance. Default to 1.0.
        reg_alpha (Optional[float]):
            L1 regularization term on weights (xgb's alpha). Default to 0.0.
        reg_lambda (Optional[float]):
            L2 regularization term on weights (xgb's lambda). Default to 1.0.
        early_stop (Optional[bool]):
            Whether training should stop after the first iteration. Default to True.
        learning_rate (Optional[float]):
            Boosting learning rate (xgb's "eta"). Default to 0.3.
        max_iterations (Optional[int]):
            Maximum number of rounds for boosting. Default to 20.
        min_rel_progress (Optional[float]):
            Minimum relative loss improvement necessary to continue training when early_stop is set to True. Default to 0.01.
        enable_global_explain (Optional[bool]):
            Whether to compute global explanations using explainable AI to evaluate global feature importance to the model. Default to False.
        xgboost_version (Optional[str]):
            Specifies the Xgboost version for model training. Default to "0.9". Possible values: "0.9", "1.1".
    """


class XGBClassifier(XGBModel, XGBClassifierMixIn, XGBClassifierBase):
    """
    XGBoost classifier model.

    Args:
        num_parallel_tree (Optional[int]):
            Number of parallel trees constructed during each iteration. Default to 1.
        booster (Optional[str]):
            Specify which booster to use: gbtree or dart. Default to "gbtree".
        dart_normalized_type (Optional[str]):
            Type of normalization algorithm for DART booster. Possible values: "TREE", "FOREST". Default to "TREE".
        tree_method (Optional[str]):
            Specify which tree method to use.  Default to "auto". If this parameter is set to
            default, XGBoost will choose the most conservative option available. Possible values: ""exact", "approx",
            "hist".
        min_child_weight (Optional[float]):
            Minimum sum of instance weight(hessian) needed in a child. Default to 1.
        colsample_bytree (Optional[float]):
            Subsample ratio of columns when constructing each tree. Default to 1.0.
        colsample_bylevel (Optional[float]):
            Subsample ratio of columns for each level. Default to 1.0.
        colsample_bynode (Optional[float]):
            Subsample ratio of columns for each split. Default to 1.0.
        gamma (Optional[float]):
            (min_split_loss) Minimum loss reduction required to make a further partition on a
            leaf node of the tree. Default to 0.0.
        max_depth (Optional[int]):
            Maximum tree depth for base learners. Default to 6.
        subsample (Optional[float]):
            Subsample ratio of the training instance. Default to 1.0.
        reg_alpha (Optional[float]):
            L1 regularization term on weights (xgb's alpha). Default to 0.0.
        reg_lambda (Optional[float]):
            L2 regularization term on weights (xgb's lambda). Default to 1.0.
        early_stop (Optional[bool]):
            Whether training should stop after the first iteration. Default to True.
        learning_rate (Optional[float]):
            Boosting learning rate (xgb's "eta"). Default to 0.3.
        max_iterations (Optional[int]):
            Maximum number of rounds for boosting. Default to 20.
        min_rel_progress (Optional[float]):
            Minimum relative loss improvement necessary to continue training when early_stop is set to True. Default to 0.01.
        enable_global_explain (Optional[bool]):
            Whether to compute global explanations using explainable AI to evaluate global feature importance to the model. Default to False.
        xgboost_version (Optional[str]):
            Specifies the Xgboost version for model training. Default to "0.9". Possible values: "0.9", "1.1".
    """
