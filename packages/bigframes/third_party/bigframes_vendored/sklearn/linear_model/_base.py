"""
Generalized Linear Models.
"""

# Author: Alexandre Gramfort <alexandre.gramfort@inria.fr>
# Fabian Pedregosa <fabian.pedregosa@inria.fr>
# Olivier Grisel <olivier.grisel@ensta.org>
#         Vincent Michel <vincent.michel@inria.fr>
#         Peter Prettenhofer <peter.prettenhofer@gmail.com>
#         Mathieu Blondel <mathieu@mblondel.org>
#         Lars Buitinck
#         Maryan Morel <maryan.morel@polytechnique.edu>
#         Giorgio Patrini <giorgio.patrini@anu.edu.au>
#         Maria Telenczuk <https://github.com/maikia>
# License: BSD 3 clause
# Original location: https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/linear_model/_base.py

from abc import ABCMeta

from bigframes_vendored.sklearn.base import (
    BaseEstimator,
    ClassifierMixin,
    RegressorMixin,
)

from bigframes import constants


class LinearModel(BaseEstimator, metaclass=ABCMeta):
    def predict(self, X):
        """Predict using the linear model.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series or pandas.core.frame.DataFrame or pandas.core.series.Series):
                Series or DataFrame of shape (n_samples, n_features). Samples.

        Returns:
            bigframes.dataframe.DataFrame: DataFrame of shape (n_samples, n_input_columns + n_prediction_columns). Returns predicted values.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)


class LinearClassifierMixin(ClassifierMixin):
    def predict(self, X):
        """Predict class labels for samples in X.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series or pandas.core.frame.DataFrame or pandas.core.series.Series):
                Series or DataFrame of shape (n_samples, n_features). The data matrix for
                which we want to get the predictions.

        Returns:
            bigframes.dataframe.DataFrame: DataFrame of shape (n_samples, n_input_columns + n_prediction_columns). Returns predicted values.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)


class LinearRegression(RegressorMixin, LinearModel):
    """Ordinary least squares Linear Regression.

    LinearRegression fits a linear model with coefficients w = (w1, ..., wp)
    to minimize the residual sum of squares between the observed targets in
    the dataset, and the targets predicted by the linear approximation.

    **Examples:**

        >>> from bigframes.ml.linear_model import LinearRegression
        >>> import bigframes.pandas as bpd
        >>> bpd.options.display.progress_bar = None
        >>> X = bpd.DataFrame({ \
                "feature0": [20, 21, 19, 18], \
                "feature1": [0, 1, 1, 0], \
                "feature2": [0.2, 0.3, 0.4, 0.5]})
        >>> y = bpd.DataFrame({"outcome": [0, 0, 1, 1]})
        >>> # Create the linear model
        >>> model = LinearRegression()
        >>> model.fit(X, y)
        LinearRegression()

        >>> # Score the model
        >>> score = model.score(X, y)
        >>> print(score) # doctest:+SKIP
            mean_absolute_error  mean_squared_error  mean_squared_log_error  \
        0             0.022812            0.000602                 0.00035
            median_absolute_error  r2_score  explained_variance
        0               0.015077  0.997591            0.997591


    Args:
        optimize_strategy (str, default "auto_strategy"):
            The strategy to train linear regression models. Possible values are
            "auto_strategy", "batch_gradient_descent", "normal_equation". Default
            to "auto_strategy".
        fit_intercept (bool, default True):
            Default ``True``. Whether to calculate the intercept for this
            model. If set to False, no intercept will be used in calculations
            (i.e. data is expected to be centered).
        l1_reg (float or None, default None):
            The amount of L1 regularization applied. Default to None. Can't be set in "normal_equation" mode. If unset, value 0 is used.
        l2_reg (float, default 0.0):
            The amount of L2 regularization applied. Default to 0.
        max_iterations (int, default 20):
            The maximum number of training iterations or steps. Default to 20.
        warm_start (bool, default False):
            Determines whether to train a model with new training data, new model options, or both. Unless you explicitly override them, the initial options used to train the model are used for the warm start run. Default to False.
        learning_rate (float or None, default None):
            The learn rate for gradient descent when learning_rate_strategy='constant'. If unset, value 0.1 is used. If learning_rate_strategy='line_search', an error is returned.
        learning_rate_strategy (str, default "line_search"):
            The strategy for specifying the learning rate during training. Default to "line_search".
        tol (float, default 0.01):
            The minimum relative loss improvement that is necessary to continue training when EARLY_STOP is set to true. For example, a value of 0.01 specifies that each iteration must reduce the loss by 1% for training to continue. Default to 0.01.
        ls_init_learning_rate (float or None, default None):
            Sets the initial learning rate that learning_rate_strategy='line_search' uses. This option can only be used if line_search is specified. If unset, value 0.1 is used.
        calculate_p_values (bool, default False):
            Specifies whether to compute p-values and standard errors during training. Default to False.
        enable_global_explain (bool, default False):
            Whether to compute global explanations using explainable AI to evaluate global feature importance to the model. Default to False.
    """

    def fit(
        self,
        X,
        y,
    ):
        """Fit linear model.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series or pandas.core.frame.DataFrame or pandas.core.series.Series):
                Series or DataFrame of shape (n_samples, n_features). Training data.

            y (bigframes.dataframe.DataFrame or bigframes.series.Series or pandas.core.frame.DataFrame or pandas.core.series.Series):
                Series or DataFrame of shape (n_samples,) or (n_samples, n_targets).
                Target values. Will be cast to X's dtype if necessary.

            X_eval (bigframes.dataframe.DataFrame or bigframes.series.Series or pandas.core.frame.DataFrame or pandas.core.series.Series):
                Series or DataFrame of shape (n_samples, n_features). Evaluation data.

            y_eval (bigframes.dataframe.DataFrame or bigframes.series.Series or pandas.core.frame.DataFrame or pandas.core.series.Series):
                Series or DataFrame of shape (n_samples,) or (n_samples, n_targets).
                Evaluation target values. Will be cast to X_eval's dtype if necessary.

        Returns:
            LinearRegression: Fitted estimator.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
