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
            X:
                DataFrame of shape (n_samples, n_features). The data matrix for
                which we want to get the predictions.

        Returns:
            DataFrame of shape (n_samples,), containing the class labels for
            each sample.
        """
        raise NotImplementedError("abstract method")


class KMeans(_BaseKMeans):
    """K-Means clustering.

    Args:
        n_clusters: int, default=8
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
            X:
                DataFrame of shape (n_samples, n_features). Training data.
            y:  Ignored
                Not used, present here for API consistency by convention.

            transforms:
                An optional list of SQL expressions to apply over top of the
                model inputs as preprocessing. This preprocessing will be
                automatically reapplied to new input data (e.g. in .predict),
                and may contain steps (like ML.STANDARD_SCALER) that fit to the
                training data.

        Returns:
            Fitted Estimator.
        """
        raise NotImplementedError("abstract method")
