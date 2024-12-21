# Authors: Nicolas Tresegnie <nicolas.tresegnie@gmail.com>
#          Sergey Feldman <sergeyfeldman@gmail.com>
# License: BSD 3 clause

from bigframes_vendored.sklearn.base import BaseEstimator, TransformerMixin

from bigframes import constants


class _BaseImputer(TransformerMixin, BaseEstimator):
    """Base class for all imputers."""


class SimpleImputer(_BaseImputer):
    """
    Univariate imputer for completing missing values with simple strategies.

    Replace missing values using a descriptive statistic (e.g. mean, median, or
    most frequent) along each column.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> from bigframes.ml.impute import SimpleImputer
        >>> bpd.options.display.progress_bar = None
        >>> X_train = bpd.DataFrame({"feat0": [7.0, 4.0, 10.0], "feat1": [2.0, None, 5.0], "feat2": [3.0, 6.0, 9.0]})
        >>> imp_mean = SimpleImputer().fit(X_train)
        >>> X_test = bpd.DataFrame({"feat0": [None, 4.0, 10.0], "feat1": [2.0, None, None], "feat2": [3.0, 6.0, 9.0]})
        >>> imp_mean.transform(X_test)
           imputer_feat0  imputer_feat1  imputer_feat2
        0            7.0            2.0            3.0
        1            4.0            3.5            6.0
        2           10.0            3.5            9.0
        <BLANKLINE>
        [3 rows x 3 columns]

    Args:
        strategy ({'mean', 'median', 'most_frequent'}, default='mean'):
            The imputation strategy. 'mean': replace missing values using the mean along
            the axis. 'median':replace missing values using the median along
            the axis. 'most_frequent', replace missing using the most frequent
            value along the axis.
    """

    def fit(self, X, y=None):
        """Fit the imputer on X.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series or pandas.core.frame.DataFrame or pandas.core.series.Series):
                The Dataframe or Series with training data.

            y (default None):
                Ignored.

        Returns:
            SimpleImputer: Fitted scaler.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def transform(self, X):
        """Impute all missing values in X.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series or pandas.core.frame.DataFrame or pandas.core.series.Series):
                The DataFrame or Series to be transformed.

        Returns:
            bigframes.dataframe.DataFrame: Transformed result."""
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
