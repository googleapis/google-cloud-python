# Authors: Andreas Mueller <amueller@ais.uni-bonn.de>
#          Joris Van den Bossche <jorisvandenbossche@gmail.com>
# License: BSD 3 clause

from third_party.bigframes_vendored.sklearn.base import BaseEstimator


class OneHotEncoder(BaseEstimator):
    """Encode categorical features as a one-hot format.

    The input to this transformer should be an array-like of integers or
    strings, denoting the values taken on by categorical (discrete) features.
    The features are encoded using a one-hot (aka 'one-of-K' or 'dummy')
    encoding scheme.

    Note that this method deviates from Scikit-Learn; instead of producing sparse
    binary columns, the encoding is a single column of STRUCT<index INT64, value DOUBLE>
    """

    def fit(self, X):
        """Fit OneHotEncoder to X.

        Args:
            X:
                A dataframe with training data.

        Returns:
                Fitted encoder.
        """
        raise NotImplementedError("abstract method")

    def transform(self, X):
        """Transform X using one-hot encoding.

        Args:
            X:
                The DataFrame to be transformed.

        Returns:
            Transformed result."""
        raise NotImplementedError("abstract method")
