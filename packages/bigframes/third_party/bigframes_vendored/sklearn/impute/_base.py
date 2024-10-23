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
