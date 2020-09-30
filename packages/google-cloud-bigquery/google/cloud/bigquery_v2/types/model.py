# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import proto  # type: ignore


from google.cloud.bigquery_v2.types import encryption_config
from google.cloud.bigquery_v2.types import model_reference as gcb_model_reference
from google.cloud.bigquery_v2.types import standard_sql
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.bigquery.v2",
    manifest={
        "Model",
        "GetModelRequest",
        "PatchModelRequest",
        "DeleteModelRequest",
        "ListModelsRequest",
        "ListModelsResponse",
    },
)


class Model(proto.Message):
    r"""

    Attributes:
        etag (str):
            Output only. A hash of this resource.
        model_reference (~.gcb_model_reference.ModelReference):
            Required. Unique identifier for this model.
        creation_time (int):
            Output only. The time when this model was
            created, in millisecs since the epoch.
        last_modified_time (int):
            Output only. The time when this model was
            last modified, in millisecs since the epoch.
        description (str):
            Optional. A user-friendly description of this
            model.
        friendly_name (str):
            Optional. A descriptive name for this model.
        labels (Sequence[~.gcb_model.Model.LabelsEntry]):
            The labels associated with this model. You
            can use these to organize and group your models.
            Label keys and values can be no longer than 63
            characters, can only contain lowercase letters,
            numeric characters, underscores and dashes.
            International characters are allowed. Label
            values are optional. Label keys must start with
            a letter and each label in the list must have a
            different key.
        expiration_time (int):
            Optional. The time when this model expires,
            in milliseconds since the epoch. If not present,
            the model will persist indefinitely. Expired
            models will be deleted and their storage
            reclaimed.  The defaultTableExpirationMs
            property of the encapsulating dataset can be
            used to set a default expirationTime on newly
            created models.
        location (str):
            Output only. The geographic location where
            the model resides. This value is inherited from
            the dataset.
        encryption_configuration (~.encryption_config.EncryptionConfiguration):
            Custom encryption configuration (e.g., Cloud
            KMS keys). This shows the encryption
            configuration of the model data while stored in
            BigQuery storage.
        model_type (~.gcb_model.Model.ModelType):
            Output only. Type of the model resource.
        training_runs (Sequence[~.gcb_model.Model.TrainingRun]):
            Output only. Information for all training runs in increasing
            order of start_time.
        feature_columns (Sequence[~.standard_sql.StandardSqlField]):
            Output only. Input feature columns that were
            used to train this model.
        label_columns (Sequence[~.standard_sql.StandardSqlField]):
            Output only. Label columns that were used to train this
            model. The output of the model will have a `predicted_`
            prefix to these columns.
    """

    class ModelType(proto.Enum):
        r"""Indicates the type of the Model."""
        MODEL_TYPE_UNSPECIFIED = 0
        LINEAR_REGRESSION = 1
        LOGISTIC_REGRESSION = 2
        KMEANS = 3
        TENSORFLOW = 6

    class LossType(proto.Enum):
        r"""Loss metric to evaluate model training performance."""
        LOSS_TYPE_UNSPECIFIED = 0
        MEAN_SQUARED_LOSS = 1
        MEAN_LOG_LOSS = 2

    class DistanceType(proto.Enum):
        r"""Distance metric used to compute the distance between two
        points.
        """
        DISTANCE_TYPE_UNSPECIFIED = 0
        EUCLIDEAN = 1
        COSINE = 2

    class DataSplitMethod(proto.Enum):
        r"""Indicates the method to split input data into multiple
        tables.
        """
        DATA_SPLIT_METHOD_UNSPECIFIED = 0
        RANDOM = 1
        CUSTOM = 2
        SEQUENTIAL = 3
        NO_SPLIT = 4
        AUTO_SPLIT = 5

    class LearnRateStrategy(proto.Enum):
        r"""Indicates the learning rate optimization strategy to use."""
        LEARN_RATE_STRATEGY_UNSPECIFIED = 0
        LINE_SEARCH = 1
        CONSTANT = 2

    class OptimizationStrategy(proto.Enum):
        r"""Indicates the optimization strategy used for training."""
        OPTIMIZATION_STRATEGY_UNSPECIFIED = 0
        BATCH_GRADIENT_DESCENT = 1
        NORMAL_EQUATION = 2

    class KmeansEnums(proto.Message):
        r""""""

        class KmeansInitializationMethod(proto.Enum):
            r"""Indicates the method used to initialize the centroids for
            KMeans clustering algorithm.
            """
            KMEANS_INITIALIZATION_METHOD_UNSPECIFIED = 0
            RANDOM = 1
            CUSTOM = 2

    class RegressionMetrics(proto.Message):
        r"""Evaluation metrics for regression and explicit feedback type
        matrix factorization models.

        Attributes:
            mean_absolute_error (~.wrappers.DoubleValue):
                Mean absolute error.
            mean_squared_error (~.wrappers.DoubleValue):
                Mean squared error.
            mean_squared_log_error (~.wrappers.DoubleValue):
                Mean squared log error.
            median_absolute_error (~.wrappers.DoubleValue):
                Median absolute error.
            r_squared (~.wrappers.DoubleValue):
                R^2 score.
        """

        mean_absolute_error = proto.Field(
            proto.MESSAGE, number=1, message=wrappers.DoubleValue,
        )

        mean_squared_error = proto.Field(
            proto.MESSAGE, number=2, message=wrappers.DoubleValue,
        )

        mean_squared_log_error = proto.Field(
            proto.MESSAGE, number=3, message=wrappers.DoubleValue,
        )

        median_absolute_error = proto.Field(
            proto.MESSAGE, number=4, message=wrappers.DoubleValue,
        )

        r_squared = proto.Field(proto.MESSAGE, number=5, message=wrappers.DoubleValue,)

    class AggregateClassificationMetrics(proto.Message):
        r"""Aggregate metrics for classification/classifier models. For
        multi-class models, the metrics are either macro-averaged or
        micro-averaged. When macro-averaged, the metrics are calculated
        for each label and then an unweighted average is taken of those
        values. When micro-averaged, the metric is calculated globally
        by counting the total number of correctly predicted rows.

        Attributes:
            precision (~.wrappers.DoubleValue):
                Precision is the fraction of actual positive
                predictions that had positive actual labels. For
                multiclass this is a macro-averaged metric
                treating each class as a binary classifier.
            recall (~.wrappers.DoubleValue):
                Recall is the fraction of actual positive
                labels that were given a positive prediction.
                For multiclass this is a macro-averaged metric.
            accuracy (~.wrappers.DoubleValue):
                Accuracy is the fraction of predictions given
                the correct label. For multiclass this is a
                micro-averaged metric.
            threshold (~.wrappers.DoubleValue):
                Threshold at which the metrics are computed.
                For binary classification models this is the
                positive class threshold. For multi-class
                classfication models this is the confidence
                threshold.
            f1_score (~.wrappers.DoubleValue):
                The F1 score is an average of recall and
                precision. For multiclass this is a macro-
                averaged metric.
            log_loss (~.wrappers.DoubleValue):
                Logarithmic Loss. For multiclass this is a
                macro-averaged metric.
            roc_auc (~.wrappers.DoubleValue):
                Area Under a ROC Curve. For multiclass this
                is a macro-averaged metric.
        """

        precision = proto.Field(proto.MESSAGE, number=1, message=wrappers.DoubleValue,)

        recall = proto.Field(proto.MESSAGE, number=2, message=wrappers.DoubleValue,)

        accuracy = proto.Field(proto.MESSAGE, number=3, message=wrappers.DoubleValue,)

        threshold = proto.Field(proto.MESSAGE, number=4, message=wrappers.DoubleValue,)

        f1_score = proto.Field(proto.MESSAGE, number=5, message=wrappers.DoubleValue,)

        log_loss = proto.Field(proto.MESSAGE, number=6, message=wrappers.DoubleValue,)

        roc_auc = proto.Field(proto.MESSAGE, number=7, message=wrappers.DoubleValue,)

    class BinaryClassificationMetrics(proto.Message):
        r"""Evaluation metrics for binary classification/classifier
        models.

        Attributes:
            aggregate_classification_metrics (~.gcb_model.Model.AggregateClassificationMetrics):
                Aggregate classification metrics.
            binary_confusion_matrix_list (Sequence[~.gcb_model.Model.BinaryClassificationMetrics.BinaryConfusionMatrix]):
                Binary confusion matrix at multiple
                thresholds.
            positive_label (str):
                Label representing the positive class.
            negative_label (str):
                Label representing the negative class.
        """

        class BinaryConfusionMatrix(proto.Message):
            r"""Confusion matrix for binary classification models.

            Attributes:
                positive_class_threshold (~.wrappers.DoubleValue):
                    Threshold value used when computing each of
                    the following metric.
                true_positives (~.wrappers.Int64Value):
                    Number of true samples predicted as true.
                false_positives (~.wrappers.Int64Value):
                    Number of false samples predicted as true.
                true_negatives (~.wrappers.Int64Value):
                    Number of true samples predicted as false.
                false_negatives (~.wrappers.Int64Value):
                    Number of false samples predicted as false.
                precision (~.wrappers.DoubleValue):
                    The fraction of actual positive predictions
                    that had positive actual labels.
                recall (~.wrappers.DoubleValue):
                    The fraction of actual positive labels that
                    were given a positive prediction.
                f1_score (~.wrappers.DoubleValue):
                    The equally weighted average of recall and
                    precision.
                accuracy (~.wrappers.DoubleValue):
                    The fraction of predictions given the correct
                    label.
            """

            positive_class_threshold = proto.Field(
                proto.MESSAGE, number=1, message=wrappers.DoubleValue,
            )

            true_positives = proto.Field(
                proto.MESSAGE, number=2, message=wrappers.Int64Value,
            )

            false_positives = proto.Field(
                proto.MESSAGE, number=3, message=wrappers.Int64Value,
            )

            true_negatives = proto.Field(
                proto.MESSAGE, number=4, message=wrappers.Int64Value,
            )

            false_negatives = proto.Field(
                proto.MESSAGE, number=5, message=wrappers.Int64Value,
            )

            precision = proto.Field(
                proto.MESSAGE, number=6, message=wrappers.DoubleValue,
            )

            recall = proto.Field(proto.MESSAGE, number=7, message=wrappers.DoubleValue,)

            f1_score = proto.Field(
                proto.MESSAGE, number=8, message=wrappers.DoubleValue,
            )

            accuracy = proto.Field(
                proto.MESSAGE, number=9, message=wrappers.DoubleValue,
            )

        aggregate_classification_metrics = proto.Field(
            proto.MESSAGE, number=1, message="Model.AggregateClassificationMetrics",
        )

        binary_confusion_matrix_list = proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message="Model.BinaryClassificationMetrics.BinaryConfusionMatrix",
        )

        positive_label = proto.Field(proto.STRING, number=3)

        negative_label = proto.Field(proto.STRING, number=4)

    class MultiClassClassificationMetrics(proto.Message):
        r"""Evaluation metrics for multi-class classification/classifier
        models.

        Attributes:
            aggregate_classification_metrics (~.gcb_model.Model.AggregateClassificationMetrics):
                Aggregate classification metrics.
            confusion_matrix_list (Sequence[~.gcb_model.Model.MultiClassClassificationMetrics.ConfusionMatrix]):
                Confusion matrix at different thresholds.
        """

        class ConfusionMatrix(proto.Message):
            r"""Confusion matrix for multi-class classification models.

            Attributes:
                confidence_threshold (~.wrappers.DoubleValue):
                    Confidence threshold used when computing the
                    entries of the confusion matrix.
                rows (Sequence[~.gcb_model.Model.MultiClassClassificationMetrics.ConfusionMatrix.Row]):
                    One row per actual label.
            """

            class Entry(proto.Message):
                r"""A single entry in the confusion matrix.

                Attributes:
                    predicted_label (str):
                        The predicted label. For confidence_threshold > 0, we will
                        also add an entry indicating the number of items under the
                        confidence threshold.
                    item_count (~.wrappers.Int64Value):
                        Number of items being predicted as this
                        label.
                """

                predicted_label = proto.Field(proto.STRING, number=1)

                item_count = proto.Field(
                    proto.MESSAGE, number=2, message=wrappers.Int64Value,
                )

            class Row(proto.Message):
                r"""A single row in the confusion matrix.

                Attributes:
                    actual_label (str):
                        The original label of this row.
                    entries (Sequence[~.gcb_model.Model.MultiClassClassificationMetrics.ConfusionMatrix.Entry]):
                        Info describing predicted label distribution.
                """

                actual_label = proto.Field(proto.STRING, number=1)

                entries = proto.RepeatedField(
                    proto.MESSAGE,
                    number=2,
                    message="Model.MultiClassClassificationMetrics.ConfusionMatrix.Entry",
                )

            confidence_threshold = proto.Field(
                proto.MESSAGE, number=1, message=wrappers.DoubleValue,
            )

            rows = proto.RepeatedField(
                proto.MESSAGE,
                number=2,
                message="Model.MultiClassClassificationMetrics.ConfusionMatrix.Row",
            )

        aggregate_classification_metrics = proto.Field(
            proto.MESSAGE, number=1, message="Model.AggregateClassificationMetrics",
        )

        confusion_matrix_list = proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message="Model.MultiClassClassificationMetrics.ConfusionMatrix",
        )

    class ClusteringMetrics(proto.Message):
        r"""Evaluation metrics for clustering models.

        Attributes:
            davies_bouldin_index (~.wrappers.DoubleValue):
                Davies-Bouldin index.
            mean_squared_distance (~.wrappers.DoubleValue):
                Mean of squared distances between each sample
                to its cluster centroid.
            clusters (Sequence[~.gcb_model.Model.ClusteringMetrics.Cluster]):
                [Beta] Information for all clusters.
        """

        class Cluster(proto.Message):
            r"""Message containing the information about one cluster.

            Attributes:
                centroid_id (int):
                    Centroid id.
                feature_values (Sequence[~.gcb_model.Model.ClusteringMetrics.Cluster.FeatureValue]):
                    Values of highly variant features for this
                    cluster.
                count (~.wrappers.Int64Value):
                    Count of training data rows that were
                    assigned to this cluster.
            """

            class FeatureValue(proto.Message):
                r"""Representative value of a single feature within the cluster.

                Attributes:
                    feature_column (str):
                        The feature column name.
                    numerical_value (~.wrappers.DoubleValue):
                        The numerical feature value. This is the
                        centroid value for this feature.
                    categorical_value (~.gcb_model.Model.ClusteringMetrics.Cluster.FeatureValue.CategoricalValue):
                        The categorical feature value.
                """

                class CategoricalValue(proto.Message):
                    r"""Representative value of a categorical feature.

                    Attributes:
                        category_counts (Sequence[~.gcb_model.Model.ClusteringMetrics.Cluster.FeatureValue.CategoricalValue.CategoryCount]):
                            Counts of all categories for the categorical feature. If
                            there are more than ten categories, we return top ten (by
                            count) and return one more CategoryCount with category
                            "*OTHER*" and count as aggregate counts of remaining
                            categories.
                    """

                    class CategoryCount(proto.Message):
                        r"""Represents the count of a single category within the cluster.

                        Attributes:
                            category (str):
                                The name of category.
                            count (~.wrappers.Int64Value):
                                The count of training samples matching the
                                category within the cluster.
                        """

                        category = proto.Field(proto.STRING, number=1)

                        count = proto.Field(
                            proto.MESSAGE, number=2, message=wrappers.Int64Value,
                        )

                    category_counts = proto.RepeatedField(
                        proto.MESSAGE,
                        number=1,
                        message="Model.ClusteringMetrics.Cluster.FeatureValue.CategoricalValue.CategoryCount",
                    )

                feature_column = proto.Field(proto.STRING, number=1)

                numerical_value = proto.Field(
                    proto.MESSAGE,
                    number=2,
                    oneof="value",
                    message=wrappers.DoubleValue,
                )

                categorical_value = proto.Field(
                    proto.MESSAGE,
                    number=3,
                    oneof="value",
                    message="Model.ClusteringMetrics.Cluster.FeatureValue.CategoricalValue",
                )

            centroid_id = proto.Field(proto.INT64, number=1)

            feature_values = proto.RepeatedField(
                proto.MESSAGE,
                number=2,
                message="Model.ClusteringMetrics.Cluster.FeatureValue",
            )

            count = proto.Field(proto.MESSAGE, number=3, message=wrappers.Int64Value,)

        davies_bouldin_index = proto.Field(
            proto.MESSAGE, number=1, message=wrappers.DoubleValue,
        )

        mean_squared_distance = proto.Field(
            proto.MESSAGE, number=2, message=wrappers.DoubleValue,
        )

        clusters = proto.RepeatedField(
            proto.MESSAGE, number=3, message="Model.ClusteringMetrics.Cluster",
        )

    class EvaluationMetrics(proto.Message):
        r"""Evaluation metrics of a model. These are either computed on
        all training data or just the eval data based on whether eval
        data was used during training. These are not present for
        imported models.

        Attributes:
            regression_metrics (~.gcb_model.Model.RegressionMetrics):
                Populated for regression models and explicit
                feedback type matrix factorization models.
            binary_classification_metrics (~.gcb_model.Model.BinaryClassificationMetrics):
                Populated for binary
                classification/classifier models.
            multi_class_classification_metrics (~.gcb_model.Model.MultiClassClassificationMetrics):
                Populated for multi-class
                classification/classifier models.
            clustering_metrics (~.gcb_model.Model.ClusteringMetrics):
                Populated for clustering models.
        """

        regression_metrics = proto.Field(
            proto.MESSAGE, number=1, oneof="metrics", message="Model.RegressionMetrics",
        )

        binary_classification_metrics = proto.Field(
            proto.MESSAGE,
            number=2,
            oneof="metrics",
            message="Model.BinaryClassificationMetrics",
        )

        multi_class_classification_metrics = proto.Field(
            proto.MESSAGE,
            number=3,
            oneof="metrics",
            message="Model.MultiClassClassificationMetrics",
        )

        clustering_metrics = proto.Field(
            proto.MESSAGE, number=4, oneof="metrics", message="Model.ClusteringMetrics",
        )

    class TrainingRun(proto.Message):
        r"""Information about a single training query run for the model.

        Attributes:
            training_options (~.gcb_model.Model.TrainingRun.TrainingOptions):
                Options that were used for this training run,
                includes user specified and default options that
                were used.
            start_time (~.timestamp.Timestamp):
                The start time of this training run.
            results (Sequence[~.gcb_model.Model.TrainingRun.IterationResult]):
                Output of each iteration run, results.size() <=
                max_iterations.
            evaluation_metrics (~.gcb_model.Model.EvaluationMetrics):
                The evaluation metrics over training/eval
                data that were computed at the end of training.
        """

        class TrainingOptions(proto.Message):
            r"""

            Attributes:
                max_iterations (int):
                    The maximum number of iterations in training.
                    Used only for iterative training algorithms.
                loss_type (~.gcb_model.Model.LossType):
                    Type of loss function used during training
                    run.
                learn_rate (float):
                    Learning rate in training. Used only for
                    iterative training algorithms.
                l1_regularization (~.wrappers.DoubleValue):
                    L1 regularization coefficient.
                l2_regularization (~.wrappers.DoubleValue):
                    L2 regularization coefficient.
                min_relative_progress (~.wrappers.DoubleValue):
                    When early_stop is true, stops training when accuracy
                    improvement is less than 'min_relative_progress'. Used only
                    for iterative training algorithms.
                warm_start (~.wrappers.BoolValue):
                    Whether to train a model from the last
                    checkpoint.
                early_stop (~.wrappers.BoolValue):
                    Whether to stop early when the loss doesn't improve
                    significantly any more (compared to min_relative_progress).
                    Used only for iterative training algorithms.
                input_label_columns (Sequence[str]):
                    Name of input label columns in training data.
                data_split_method (~.gcb_model.Model.DataSplitMethod):
                    The data split type for training and
                    evaluation, e.g. RANDOM.
                data_split_eval_fraction (float):
                    The fraction of evaluation data over the
                    whole input data. The rest of data will be used
                    as training data. The format should be double.
                    Accurate to two decimal places.
                    Default value is 0.2.
                data_split_column (str):
                    The column to split data with. This column won't be used as
                    a feature.

                    1. When data_split_method is CUSTOM, the corresponding
                       column should be boolean. The rows with true value tag
                       are eval data, and the false are training data.
                    2. When data_split_method is SEQ, the first
                       DATA_SPLIT_EVAL_FRACTION rows (from smallest to largest)
                       in the corresponding column are used as training data,
                       and the rest are eval data. It respects the order in
                       Orderable data types:
                       https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#data-type-properties
                learn_rate_strategy (~.gcb_model.Model.LearnRateStrategy):
                    The strategy to determine learn rate for the
                    current iteration.
                initial_learn_rate (float):
                    Specifies the initial learning rate for the
                    line search learn rate strategy.
                label_class_weights (Sequence[~.gcb_model.Model.TrainingRun.TrainingOptions.LabelClassWeightsEntry]):
                    Weights associated with each label class, for
                    rebalancing the training data. Only applicable
                    for classification models.
                distance_type (~.gcb_model.Model.DistanceType):
                    Distance type for clustering models.
                num_clusters (int):
                    Number of clusters for clustering models.
                model_uri (str):
                    [Beta] Google Cloud Storage URI from which the model was
                    imported. Only applicable for imported models.
                optimization_strategy (~.gcb_model.Model.OptimizationStrategy):
                    Optimization strategy for training linear
                    regression models.
                kmeans_initialization_method (~.gcb_model.Model.KmeansEnums.KmeansInitializationMethod):
                    The method used to initialize the centroids
                    for kmeans algorithm.
                kmeans_initialization_column (str):
                    The column used to provide the initial centroids for kmeans
                    algorithm when kmeans_initialization_method is CUSTOM.
            """

            max_iterations = proto.Field(proto.INT64, number=1)

            loss_type = proto.Field(proto.ENUM, number=2, enum="Model.LossType",)

            learn_rate = proto.Field(proto.DOUBLE, number=3)

            l1_regularization = proto.Field(
                proto.MESSAGE, number=4, message=wrappers.DoubleValue,
            )

            l2_regularization = proto.Field(
                proto.MESSAGE, number=5, message=wrappers.DoubleValue,
            )

            min_relative_progress = proto.Field(
                proto.MESSAGE, number=6, message=wrappers.DoubleValue,
            )

            warm_start = proto.Field(
                proto.MESSAGE, number=7, message=wrappers.BoolValue,
            )

            early_stop = proto.Field(
                proto.MESSAGE, number=8, message=wrappers.BoolValue,
            )

            input_label_columns = proto.RepeatedField(proto.STRING, number=9)

            data_split_method = proto.Field(
                proto.ENUM, number=10, enum="Model.DataSplitMethod",
            )

            data_split_eval_fraction = proto.Field(proto.DOUBLE, number=11)

            data_split_column = proto.Field(proto.STRING, number=12)

            learn_rate_strategy = proto.Field(
                proto.ENUM, number=13, enum="Model.LearnRateStrategy",
            )

            initial_learn_rate = proto.Field(proto.DOUBLE, number=16)

            label_class_weights = proto.MapField(proto.STRING, proto.DOUBLE, number=17)

            distance_type = proto.Field(
                proto.ENUM, number=20, enum="Model.DistanceType",
            )

            num_clusters = proto.Field(proto.INT64, number=21)

            model_uri = proto.Field(proto.STRING, number=22)

            optimization_strategy = proto.Field(
                proto.ENUM, number=23, enum="Model.OptimizationStrategy",
            )

            kmeans_initialization_method = proto.Field(
                proto.ENUM,
                number=33,
                enum="Model.KmeansEnums.KmeansInitializationMethod",
            )

            kmeans_initialization_column = proto.Field(proto.STRING, number=34)

        class IterationResult(proto.Message):
            r"""Information about a single iteration of the training run.

            Attributes:
                index (~.wrappers.Int32Value):
                    Index of the iteration, 0 based.
                duration_ms (~.wrappers.Int64Value):
                    Time taken to run the iteration in
                    milliseconds.
                training_loss (~.wrappers.DoubleValue):
                    Loss computed on the training data at the end
                    of iteration.
                eval_loss (~.wrappers.DoubleValue):
                    Loss computed on the eval data at the end of
                    iteration.
                learn_rate (float):
                    Learn rate used for this iteration.
                cluster_infos (Sequence[~.gcb_model.Model.TrainingRun.IterationResult.ClusterInfo]):
                    Information about top clusters for clustering
                    models.
            """

            class ClusterInfo(proto.Message):
                r"""Information about a single cluster for clustering model.

                Attributes:
                    centroid_id (int):
                        Centroid id.
                    cluster_radius (~.wrappers.DoubleValue):
                        Cluster radius, the average distance from
                        centroid to each point assigned to the cluster.
                    cluster_size (~.wrappers.Int64Value):
                        Cluster size, the total number of points
                        assigned to the cluster.
                """

                centroid_id = proto.Field(proto.INT64, number=1)

                cluster_radius = proto.Field(
                    proto.MESSAGE, number=2, message=wrappers.DoubleValue,
                )

                cluster_size = proto.Field(
                    proto.MESSAGE, number=3, message=wrappers.Int64Value,
                )

            index = proto.Field(proto.MESSAGE, number=1, message=wrappers.Int32Value,)

            duration_ms = proto.Field(
                proto.MESSAGE, number=4, message=wrappers.Int64Value,
            )

            training_loss = proto.Field(
                proto.MESSAGE, number=5, message=wrappers.DoubleValue,
            )

            eval_loss = proto.Field(
                proto.MESSAGE, number=6, message=wrappers.DoubleValue,
            )

            learn_rate = proto.Field(proto.DOUBLE, number=7)

            cluster_infos = proto.RepeatedField(
                proto.MESSAGE,
                number=8,
                message="Model.TrainingRun.IterationResult.ClusterInfo",
            )

        training_options = proto.Field(
            proto.MESSAGE, number=1, message="Model.TrainingRun.TrainingOptions",
        )

        start_time = proto.Field(proto.MESSAGE, number=8, message=timestamp.Timestamp,)

        results = proto.RepeatedField(
            proto.MESSAGE, number=6, message="Model.TrainingRun.IterationResult",
        )

        evaluation_metrics = proto.Field(
            proto.MESSAGE, number=7, message="Model.EvaluationMetrics",
        )

    etag = proto.Field(proto.STRING, number=1)

    model_reference = proto.Field(
        proto.MESSAGE, number=2, message=gcb_model_reference.ModelReference,
    )

    creation_time = proto.Field(proto.INT64, number=5)

    last_modified_time = proto.Field(proto.INT64, number=6)

    description = proto.Field(proto.STRING, number=12)

    friendly_name = proto.Field(proto.STRING, number=14)

    labels = proto.MapField(proto.STRING, proto.STRING, number=15)

    expiration_time = proto.Field(proto.INT64, number=16)

    location = proto.Field(proto.STRING, number=13)

    encryption_configuration = proto.Field(
        proto.MESSAGE, number=17, message=encryption_config.EncryptionConfiguration,
    )

    model_type = proto.Field(proto.ENUM, number=7, enum=ModelType,)

    training_runs = proto.RepeatedField(proto.MESSAGE, number=9, message=TrainingRun,)

    feature_columns = proto.RepeatedField(
        proto.MESSAGE, number=10, message=standard_sql.StandardSqlField,
    )

    label_columns = proto.RepeatedField(
        proto.MESSAGE, number=11, message=standard_sql.StandardSqlField,
    )


class GetModelRequest(proto.Message):
    r"""

    Attributes:
        project_id (str):
            Required. Project ID of the requested model.
        dataset_id (str):
            Required. Dataset ID of the requested model.
        model_id (str):
            Required. Model ID of the requested model.
    """

    project_id = proto.Field(proto.STRING, number=1)

    dataset_id = proto.Field(proto.STRING, number=2)

    model_id = proto.Field(proto.STRING, number=3)


class PatchModelRequest(proto.Message):
    r"""

    Attributes:
        project_id (str):
            Required. Project ID of the model to patch.
        dataset_id (str):
            Required. Dataset ID of the model to patch.
        model_id (str):
            Required. Model ID of the model to patch.
        model (~.gcb_model.Model):
            Required. Patched model.
            Follows RFC5789 patch semantics. Missing fields
            are not updated. To clear a field, explicitly
            set to default value.
    """

    project_id = proto.Field(proto.STRING, number=1)

    dataset_id = proto.Field(proto.STRING, number=2)

    model_id = proto.Field(proto.STRING, number=3)

    model = proto.Field(proto.MESSAGE, number=4, message=Model,)


class DeleteModelRequest(proto.Message):
    r"""

    Attributes:
        project_id (str):
            Required. Project ID of the model to delete.
        dataset_id (str):
            Required. Dataset ID of the model to delete.
        model_id (str):
            Required. Model ID of the model to delete.
    """

    project_id = proto.Field(proto.STRING, number=1)

    dataset_id = proto.Field(proto.STRING, number=2)

    model_id = proto.Field(proto.STRING, number=3)


class ListModelsRequest(proto.Message):
    r"""

    Attributes:
        project_id (str):
            Required. Project ID of the models to list.
        dataset_id (str):
            Required. Dataset ID of the models to list.
        max_results (~.wrappers.UInt32Value):
            The maximum number of results to return in a
            single response page. Leverage the page tokens
            to iterate through the entire collection.
        page_token (str):
            Page token, returned by a previous call to
            request the next page of results
    """

    project_id = proto.Field(proto.STRING, number=1)

    dataset_id = proto.Field(proto.STRING, number=2)

    max_results = proto.Field(proto.MESSAGE, number=3, message=wrappers.UInt32Value,)

    page_token = proto.Field(proto.STRING, number=4)


class ListModelsResponse(proto.Message):
    r"""

    Attributes:
        models (Sequence[~.gcb_model.Model]):
            Models in the requested dataset. Only the following fields
            are populated: model_reference, model_type, creation_time,
            last_modified_time and labels.
        next_page_token (str):
            A token to request the next page of results.
    """

    @property
    def raw_page(self):
        return self

    models = proto.RepeatedField(proto.MESSAGE, number=1, message=Model,)

    next_page_token = proto.Field(proto.STRING, number=2)


__all__ = tuple(sorted(__protobuf__.manifest))
