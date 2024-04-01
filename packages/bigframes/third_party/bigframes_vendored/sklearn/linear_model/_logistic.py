"""
Logistic Regression
"""

# Author: Gael Varoquaux <gael.varoquaux@normalesup.org>
#         Fabian Pedregosa <f@bianp.net>
#         Alexandre Gramfort <alexandre.gramfort@telecom-paristech.fr>
#         Manoj Kumar <manojkumarsivaraj334@gmail.com>
#         Lars Buitinck
#         Simon Wu <s8wu@uwaterloo.ca>
#         Arthur Mensch <arthur.mensch@m4x.org
# Original location: https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/linear_model/_logistic.py


from bigframes_vendored.sklearn.linear_model._base import (
    BaseEstimator,
    LinearClassifierMixin,
)

from bigframes import constants


class LogisticRegression(LinearClassifierMixin, BaseEstimator):
    """Logistic Regression (aka logit, MaxEnt) classifier.

    Args:
        optimize_strategy (str, default "auto_strategy"):
            The strategy to train logistic regression models. Possible values are
            "auto_strategy", "batch_gradient_descent", "normal_equation". Default
            to "auto_strategy".
        fit_intercept (default True):
            Default True. Specifies if a constant (a.k.a. bias or intercept)
            should be added to the decision function.
        class_weight (dict or 'balanced', default None):
            Default None. Weights associated with classes in the form
            ``{class_label: weight}``.If not given, all classes are supposed
            to have weight one. The "balanced" mode uses the values of y to
            automatically adjust weights inversely proportional to class
            frequencies in the input data as
            ``n_samples / (n_classes * np.bincount(y))``. Dict isn't
            supported.
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
        """Fit the model according to the given training data.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series):
                Series or DataFrame of shape (n_samples, n_features). Training vector,
                where `n_samples` is the number of samples and `n_features` is
                the number of features.

            y (bigframes.dataframe.DataFrame or bigframes.series.Series):
                DataFrame of shape (n_samples,). Target vector relative to X.


        Returns:
            LogisticRegression: Fitted Estimator.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
