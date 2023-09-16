"""
Forest of trees-based ensemble methods.
Those methods include random forests and extremely randomized trees.
The module structure is the following:
- The ``BaseForest`` base class implements a common ``fit`` method for all
  the estimators in the module. The ``fit`` method of the base ``Forest``
  class calls the ``fit`` method of each sub-estimator on random samples
  (with replacement, a.k.a. bootstrap) of the training set.
  The init of the sub-estimator is further delegated to the
  ``BaseEnsemble`` constructor.
- The ``ForestClassifier`` and ``ForestRegressor`` base classes further
  implement the prediction logic by computing an average of the predicted
  outcomes of the sub-estimators.
- The ``RandomForestClassifier`` and ``RandomForestRegressor`` derived
  classes provide the user with concrete implementations of
  the forest ensemble method using classical, deterministic
  ``DecisionTreeClassifier`` and ``DecisionTreeRegressor`` as
  sub-estimator implementations.
- The ``ExtraTreesClassifier`` and ``ExtraTreesRegressor`` derived
  classes provide the user with concrete implementations of the
  forest ensemble method using the extremely randomized trees
  ``ExtraTreeClassifier`` and ``ExtraTreeRegressor`` as
  sub-estimator implementations.
Single and multi-output problems are both handled.
"""

# Authors: Gilles Louppe <g.louppe@gmail.com>
#          Brian Holt <bdholt1@gmail.com>
#          Joly Arnaud <arnaud.v.joly@gmail.com>
#          Fares Hedayati <fares.hedayati@gmail.com>
#
# License: BSD 3 clause

from abc import ABCMeta

from bigframes import constants

from ..base import BaseEstimator, ClassifierMixin, MetaEstimatorMixin, RegressorMixin


class BaseForest(MetaEstimatorMixin, BaseEstimator, metaclass=ABCMeta):
    """
    Base class for forests of trees.
    """

    def fit(self, X, y):
        """Build a forest of trees from the training set (X, y).

        Args:
            X:
                Series or DataFrame of shape (n_samples, n_features). Training data.

            y:
                Series or DataFrame of shape (n_samples,) or (n_samples, n_targets).
                Target values. Will be cast to X's dtype if necessary.


        Returns:
            Fitted Estimator.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)


class ForestRegressor(RegressorMixin, BaseForest, metaclass=ABCMeta):
    """
    Base class for forest of trees-based regressors.
    """

    def predict(self, X):
        """Predict regression target for X.

        The predicted regression target of an input sample is computed as the
        mean predicted regression targets of the trees in the forest.

        Args:
            X:
                Series or DataFrame of shape (n_samples, n_features). The data matrix for
                which we want to get the predictions.

        Returns:
            The predicted values.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)


class RandomForestRegressor(ForestRegressor):
    """A random forest regressor.

    A random forest is a meta estimator that fits a number of classifying
    decision trees on various sub-samples of the dataset and uses averaging
    to improve the predictive accuracy and control over-fitting.

    Args:
        num_parallel_tree: Optional[int]
            Number of parallel trees constructed during each iteration. Default to 100. Minimum value is 2.
        tree_method: Optional[str]
            Specify which tree method to use. Default to "auto". If this parameter is set to
            default, XGBoost will choose the most conservative option available. Possible values: ""exact", "approx",
            "hist".
        min_child_weight : Optional[float]
            Minimum sum of instance weight(hessian) needed in a child. Default to 1.
        colsample_bytree : Optional[float]
            Subsample ratio of columns when constructing each tree. Default to 1.0. The value should be between 0 and 1.
        colsample_bylevel : Optional[float]
            Subsample ratio of columns for each level. Default to 1.0. The value should be between 0 and 1.
        colsample_bynode : Optional[float]
            Subsample ratio of columns for each split. Default to 0.8. The value should be between 0 and 1.
        gamma : Optional[float]
            (min_split_loss) Minimum loss reduction required to make a further partition on a
            leaf node of the tree. Default to 0.0.
        max_depth :  Optional[int]
            Maximum tree depth for base learners. Default to 15. The value should be greater than 0 and less than 1.
        subsample : Optional[float]
            Subsample ratio of the training instance. Default to 0.8. The value should be greater than 0 and less than 1.
        reg_alpha : Optional[float]
            L1 regularization term on weights (xgb's alpha). Default to 0.0.
        reg_lambda : Optional[float]
            L2 regularization term on weights (xgb's lambda). Default to 1.0.
        early_stop: Optional[bool]
            Whether training should stop after the first iteration. Default to True.
        min_rel_progress: Optional[float]
            Minimum relative loss improvement necessary to continue training when early_stop is set to True. Default to 0.01.
        enable_global_explain: Optional[bool]
            Whether to compute global explanations using explainable AI to evaluate global feature importance to the model. Default to False.
        xgboost_version: Optional[str]
            Specifies the Xgboost version for model training.  Default to "0.9". Possible values: "0.9", "1.1".
    """


class ForestClassifier(ClassifierMixin, BaseForest, metaclass=ABCMeta):
    """
    Base class for forest of trees-based classifiers.
    """

    def predict(self, X):
        """Predict regression target for X.

        The predicted regression target of an input sample is computed as the
        mean predicted regression targets of the trees in the forest.

        Args:
            X:
                Series or DataFrame of shape (n_samples, n_features). The data matrix for
                which we want to get the predictions.

        Returns:
            The predicted values.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)


class RandomForestClassifier(ForestClassifier):
    """
    A random forest classifier.

    A random forest is a meta estimator that fits a number of decision tree
    classifiers on various sub-samples of the dataset and uses averaging to
    improve the predictive accuracy and control over-fitting.

    Args:
        num_parallel_tree: Optional[int]
            Number of parallel trees constructed during each iteration. Default to 100. Minimum value is 2.
        tree_method: Optional[str]
            Specify which tree method to use. Default to "auto". If this parameter is set to
            default, XGBoost will choose the most conservative option available. Possible values: ""exact", "approx",
            "hist".
        min_child_weight : Optional[float]
            Minimum sum of instance weight(hessian) needed in a child. Default to 1.
        colsample_bytree : Optional[float]
            Subsample ratio of columns when constructing each tree. Default to 1.0. The value should be between 0 and 1.
        colsample_bylevel : Optional[float]
            Subsample ratio of columns for each level. Default to 1.0. The value should be between 0 and 1.
        colsample_bynode : Optional[float]
            Subsample ratio of columns for each split. Default to 0.8. The value should be between 0 and 1.
        gamma : Optional[float]
            (min_split_loss) Minimum loss reduction required to make a further partition on a
            leaf node of the tree. Default to 0.0.
        max_depth :  Optional[int]
            Maximum tree depth for base learners. Default to 15. The value should be greater than 0 and less than 1.
        subsample : Optional[float]
            Subsample ratio of the training instance. Default to 0.8. The value should be greater than 0 and less than 1.
        reg_alpha : Optional[float]
            L1 regularization term on weights (xgb's alpha). Default to 0.0.
        reg_lambda : Optional[float]
            L2 regularization term on weights (xgb's lambda). Default to 1.0.
        early_stop: Optional[bool]
            Whether training should stop after the first iteration. Default to True.
        min_rel_progress: Optional[float]
            Minimum relative loss improvement necessary to continue training when early_stop is set to True. Default to 0.01.
        enable_global_explain: Optional[bool]
            Whether to compute global explanations using explainable AI to evaluate global feature importance to the model. Default to False.
        xgboost_version: Optional[str]
            Specifies the Xgboost version for model training.  Default to "0.9". Possible values: "0.9", "1.1".ß
    """
