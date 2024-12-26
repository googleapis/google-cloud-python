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

    >>> from bigframes.ml.linear_model import LogisticRegression
    >>> import bigframes.pandas as bpd
    >>> bpd.options.display.progress_bar = None
    >>> X = bpd.DataFrame({ \
            "feature0": [20, 21, 19, 18], \
            "feature1": [0, 1, 1, 0], \
            "feature2": [0.2, 0.3, 0.4, 0.5]})
    >>> y = bpd.DataFrame({"outcome": [0, 0, 1, 1]})
    >>> # Create the LogisticRegression
    >>> model = LogisticRegression()
    >>> model.fit(X, y)
    LogisticRegression()
    >>> model.predict(X) # doctest:+SKIP
        predicted_outcome	predicted_outcome_probs	feature0	feature1	feature2
    0	0	[{'label': 1, 'prob': 3.1895929877221615e-07} ...	20	0	0.2
    1	0	[{'label': 1, 'prob': 5.662891265051953e-06} ...	21	1	0.3
    2	1	[{'label': 1, 'prob': 0.9999917826885262} {'l...	19	1	0.4
    3	1	[{'label': 1, 'prob': 0.9999999993659574} {'l...	18	0	0.5
    4 rows × 5 columns

    [4 rows x 5 columns in total]

    >>> # Score the model
    >>> score = model.score(X, y)
    >>> score  # doctest:+SKIP
        precision	recall	accuracy	f1_score	log_loss	roc_auc
    0	1.0	1.0	1.0	1.0	0.000004	1.0
    1 rows × 6 columns

    [1 rows x 6 columns in total]

    Args:
        optimize_strategy (str, default "auto_strategy"):
            The strategy to train logistic regression models. Possible values are
            "auto_strategy" and "batch_gradient_descent". The two are equilevant since
            "auto_strategy" will fall back to "batch_gradient_descent". The API is kept
            for consistency.
            Default to "auto_strategy".
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
            X (bigframes.dataframe.DataFrame or bigframes.series.Series or pandas.core.frame.DataFrame or pandas.core.series.Series):
                Series or DataFrame of shape (n_samples, n_features). Training vector,
                where `n_samples` is the number of samples and `n_features` is
                the number of features.

            y (bigframes.dataframe.DataFrame or bigframes.series.Series or pandas.core.frame.DataFrame or pandas.core.series.Series):
                DataFrame of shape (n_samples,). Target vector relative to X.

            X_eval (bigframes.dataframe.DataFrame or bigframes.series.Series or pandas.core.frame.DataFrame or pandas.core.series.Series):
                Series or DataFrame of shape (n_samples, n_features). Evaluation vector,
                where `n_samples` is the number of samples and `n_features` is
                the number of features.

            y_eval (bigframes.dataframe.DataFrame or bigframes.series.Series or pandas.core.frame.DataFrame or pandas.core.series.Series):
                DataFrame of shape (n_samples,). Target vector relative to X_eval.


        Returns:
            LogisticRegression: Fitted estimator.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
