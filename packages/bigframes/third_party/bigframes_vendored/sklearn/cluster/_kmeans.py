"""K-means clustering."""

# Authors: Gael Varoquaux <gael.varoquaux@normalesup.org>
#          Thomas Rueckstiess <ruecksti@in.tum.de>
#          James Bergstra <james.bergstra@umontreal.ca>
#          Jan Schlueter <scikit-learn@jan-schlueter.de>
#          Nelle Varoquaux
#          Peter Prettenhofer <peter.prettenhofer@gmail.com>
#          Olivier Grisel <olivier.grisel@ensta.org>
#          Mathieu Blondel <mathieu@mblondel.org>
#          Robert Layton <robertlayton@gmail.com>
# License: BSD 3 clause

from abc import ABC
from typing import List, Optional

from third_party.bigframes_vendored.sklearn.base import BaseEstimator


class _BaseKMeans(BaseEstimator, ABC):
    """Base class for KMeans and MiniBatchKMeans"""

    def predict(self, X):
        """Predict the closest cluster each sample in X belongs to.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series):
                Series or DataFrame of shape (n_samples, n_features). The data matrix for
                which we want to get the predictions.

        Returns:
            bigframes.dataframe.DataFrame: DataFrame of shape (n_samples,), containing the
                class labels for each sample.
        """
        raise NotImplementedError("abstract method")


class KMeans(_BaseKMeans):
    """K-Means clustering.

    Args:
        n_clusters (int, default 8):
            The number of clusters to form as well as the number of centroids to generate.
            Default to 8.
    """

    def fit(
        self,
        X,
        y=None,
        transforms: Optional[List[str]] = None,
    ):
        """Compute k-means clustering.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series):
                DataFrame of shape (n_samples, n_features). Training data.
            y (default None):
                Not used, present here for API consistency by convention.
            transforms (Optional[List[str]], default None):
                Do not use. Internal param to be deprecated.
                Use bigframes.ml.pipeline instead.


        Returns:
            KMeans: Fitted Estimator.
        """
        raise NotImplementedError("abstract method")

    def predict(
        self,
        X,
    ):
        """Predict the closest cluster each sample in X belongs to.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series):
                DataFrame of shape (n_samples, n_features). New data to predict.
            y: (default None)
                Not used, present here for API consistency by convention.

        Returns:
            bigframes.dataframe.DataFrame: DataFrame of the cluster each sample belongs to.
        """
        raise NotImplementedError("abstract method")

    def score(
        self,
        X,
        y=None,
    ):
        """Metrics of the model.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series):
                DataFrame of shape (n_samples, n_features). New Data.
            y (default None)
                Not used, present here for API consistency by convention.

        Returns:
            bigframes.dataframe.DataFrame: DataFrame of the metrics.
        """
        raise NotImplementedError("abstract method")
