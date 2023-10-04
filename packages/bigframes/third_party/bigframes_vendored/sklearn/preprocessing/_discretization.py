# Author: Henry Lin <hlin117@gmail.com>
#         Tom Dupré la Tour

# License: BSD

from bigframes import constants
from third_party.bigframes_vendored.sklearn.base import BaseEstimator, TransformerMixin


class KBinsDiscretizer(TransformerMixin, BaseEstimator):
    """
    Bin continuous data into intervals.

    Args:
        n_bins (int, default 5):
            The number of bins to produce. Raises ValueError if ``n_bins < 2``.
        strategy ({'uniform', 'quantile'}, default='quantile'):
            Strategy used to define the widths of the bins. 'uniform': All bins
            in each feature have identical widths. 'quantile': All bins in each
            feature have the same number of points. Only `uniform` is supported now.
    """

    def fit(self, X, y=None):
        """Fit the estimator.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series):
                The Dataframe or Series with training data.

            y (default None):
                Ignored.

        Returns:
            KBinsDiscretizer: Fitted scaler.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def transform(self, X):
        """Discretize the data.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series):
                The DataFrame or Series to be transformed.

        Returns:
            bigframes.dataframe.DataFrame: Transformed result."""
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
