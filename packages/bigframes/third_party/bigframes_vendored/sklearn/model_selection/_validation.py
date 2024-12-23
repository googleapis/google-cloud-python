"""
The :mod:`sklearn.model_selection._validation` module includes classes and
functions to validate the model.
"""

# Author: Alexandre Gramfort <alexandre.gramfort@inria.fr>
#         Gael Varoquaux <gael.varoquaux@normalesup.org>
#         Olivier Grisel <olivier.grisel@ensta.org>
#         Raghav RV <rvraghav93@gmail.com>
#         Michal Karbownik <michakarbownik@gmail.com>
# License: BSD 3 clause


def cross_validate(estimator, X, y=None, *, cv=None):
    """Evaluate metric(s) by cross-validation and also record fit/score times.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> from bigframes.ml.model_selection import cross_validate, KFold
        >>> from bigframes.ml.linear_model import LinearRegression
        >>> bpd.options.display.progress_bar = None
        >>> X = bpd.DataFrame({"feat0": [1, 3, 5], "feat1": [2, 4, 6]})
        >>> y = bpd.DataFrame({"label": [1, 2, 3]})
        >>> model = LinearRegression()
        >>> scores = cross_validate(model, X, y, cv=3) # doctest: +SKIP
        >>> for score in scores["test_score"]: # doctest: +SKIP
        ...   print(score["mean_squared_error"][0])
        ...
        5.218167286047954e-19
        2.726229944928669e-18
        1.6197635612324266e-17

    Args:
        estimator:
            bigframes.ml model that implements fit().
        The object to use to fit the data.

        X (bigframes.dataframe.DataFrame or bigframes.series.Series):
            The data to fit.

        y (bigframes.dataframe.DataFrame, bigframes.series.Series or None):
            The target variable to try to predict in the case of supe()rvised learning. Default to None.

        cv (int, bigframes.ml.model_selection.KFold or None):
            Determines the cross-validation splitting strategy.
            Possible inputs for cv are:

            - None, to use the default 5-fold cross validation,
            - int, to specify the number of folds in a `KFold`,
            - bigframes.ml.model_selection.KFold instance.

    Returns:
        Dict[str, List]: A dict of arrays containing the score/time arrays for each scorer is returned. The keys for this ``dict`` are:

            ``test_score``
                The score array for test scores on each cv split.
            ``fit_time``
                The time for fitting the estimator on the train
                set for each cv split.
            ``score_time``
                The time for scoring the estimator on the test set for each
                cv split."""
