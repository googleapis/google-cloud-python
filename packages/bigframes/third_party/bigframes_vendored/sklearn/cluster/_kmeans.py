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

from bigframes import constants
from third_party.bigframes_vendored.sklearn.base import BaseEstimator


class _BaseKMeans(BaseEstimator, ABC):
    """Base class for KMeans and MiniBatchKMeans"""

    pass


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
    ):
        """Compute k-means clustering.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series):
                DataFrame of shape (n_samples, n_features). Training data.
            y (default None):
                Not used, present here for API consistency by convention.

        Returns:
            KMeans: Fitted Estimator.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def predict(
        self,
        X,
    ):
        """Predict the closest cluster each sample in X belongs to.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series):
                DataFrame of shape (n_samples, n_features). New data to predict.

        Returns:
            bigframes.dataframe.DataFrame: DataFrame of shape (n_samples, n_input_columns + n_prediction_columns). Returns predicted labels.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def score(
        self,
        X,
        y=None,
    ):
        """Calculate evaluation metrics of the model.

        .. note::

            Output matches that of the BigQuery ML.EVALUTE function.
            See: https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate#k-means_models
            for the outputs relevant to this model type.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series):
                DataFrame of shape (n_samples, n_features). New Data.
            y (default None)
                Not used, present here for API consistency by convention.

        Returns:
            bigframes.dataframe.DataFrame: DataFrame of the metrics.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def cluster_centers_(self):
        """Information of cluster centers.

        Returns:
            bigframes.dataframe.DataFrame: DataFrame of cluster centers, containing following columns:
                centroid_id: An integer that identifies the centroid.

                feature: The column name that contains the feature.

                numerical_value: If feature is numeric, the value of feature for the centroid that centroid_id identifies. If feature is not numeric, the value is NULL.

                categorical_value: An list of mappings containing information about categorical features. Each mapping contains the following fields:
                    categorical_value.category: The name of each category.

                    categorical_value.value: The value of categorical_value.category for the centroid that centroid_id identifies.

            The output contains one row per feature per centroid.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
