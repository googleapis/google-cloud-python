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

from bigframes_vendored.sklearn.base import BaseEstimator

from bigframes import constants


class _BaseKMeans(BaseEstimator, ABC):
    """Base class for KMeans and MiniBatchKMeans"""

    pass


class KMeans(_BaseKMeans):
    """K-Means clustering.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> bpd.options.display.progress_bar = None
        >>> from bigframes.ml.cluster import KMeans

        >>> X = bpd.DataFrame({"feat0": [1, 1, 1, 10, 10, 10], "feat1": [2, 4, 0, 2, 4, 0]})
        >>> kmeans = KMeans(n_clusters=2).fit(X)
        >>> kmeans.predict(bpd.DataFrame({"feat0": [0, 12], "feat1": [0, 3]}))["CENTROID_ID"] # doctest:+SKIP
        0    1
        1    2
        Name: CENTROID_ID, dtype: Int64

        >>> kmeans.cluster_centers_ # doctest:+SKIP
        centroid_id feature  numerical_value categorical_value
        0            1   feat0              5.5                []
        1            1   feat1              1.0                []
        2            2   feat0              5.5                []
        3            2   feat1              4.0                []

        [4 rows x 4 columns]

    Args:
        n_clusters (int, default 8):
            The number of clusters to form as well as the number of centroids to generate.
            Default to 8.

        init ("kmeans++", "random" or "custom", default "kmeans++"):
            The method of initializing the clusters. Default to "kmeans++"

            kmeas++: Initializes a number of centroids equal to the n_clusters value by using the k-means++ algorithm. Using this approach usually trains a better model than using random cluster initialization.
            random: Initializes the centroids by randomly selecting a number of data points equal to the n_clusters value from the input data.
            custom: Initializes the centroids using a provided column of type bool. Uses the rows with a value of True as the initial centroids. You specify the column to use by using the init_col option.

        init_col (str or None, default None):
            The name of the column to use to initialize the centroids. This column must have a type of bool. If this column contains a value of True for a given row, then uses that row as an initial centroid. The number of True rows in this column must be equal to the value you have specified for the n_clusters option.
            Only works with init method "custom". Default to None.

        distance_type ("euclidean" or "cosine", default "euclidean"):
            The type of metric to use to compute the distance between two points.
            Default to "euclidean".

        max_iter (int, default 20):
            The maximum number of training iterations, where one iteration represents a single pass of the entire training data. Default to 20.

        tol (float, default 0.01):
            The minimum relative loss improvement that is necessary to continue training. For example, a value of 0.01 specifies that each iteration must reduce the loss by 1% for training to continue.
            Default to 0.01.

        warm_start (bool, default False):
            Determines whether to train a model with new training data, new model options, or both. Unless you explicitly override them, the initial options used to train the model are used for the warm start run.
            Default to False.


    """

    def fit(
        self,
        X,
        y=None,
    ):
        """Compute k-means clustering.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series or pandas.core.frame.DataFrame or pandas.core.series.Series):
                DataFrame of shape (n_samples, n_features). Training data.
            y (default None):
                Not used, present here for API consistency by convention.

        Returns:
            KMeans: Fitted estimator.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def predict(
        self,
        X,
    ):
        """Predict the closest cluster each sample in X belongs to.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series or pandas.core.frame.DataFrame or pandas.core.series.Series):
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

            Output matches that of the BigQuery ML.EVALUATE function.
            See: https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate#k-means_models
            for the outputs relevant to this model type.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series or pandas.core.frame.DataFrame or pandas.core.series.Series):
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
