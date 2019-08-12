# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Wrappers for protocol buffer enum types."""

import enum


class Model(object):
    class DataSplitMethod(enum.IntEnum):
        """
        Indicates the method to split input data into multiple tables.

        Attributes:
          DATA_SPLIT_METHOD_UNSPECIFIED (int)
          RANDOM (int): Splits data randomly.
          CUSTOM (int): Splits data with the user provided tags.
          SEQUENTIAL (int): Splits data sequentially.
          NO_SPLIT (int): Data split will be skipped.
          AUTO_SPLIT (int): Splits data automatically: Uses NO\_SPLIT if the data size is small.
          Otherwise uses RANDOM.
        """

        DATA_SPLIT_METHOD_UNSPECIFIED = 0
        RANDOM = 1
        CUSTOM = 2
        SEQUENTIAL = 3
        NO_SPLIT = 4
        AUTO_SPLIT = 5

    class DistanceType(enum.IntEnum):
        """
        Distance metric used to compute the distance between two points.

        Attributes:
          DISTANCE_TYPE_UNSPECIFIED (int)
          EUCLIDEAN (int): Eculidean distance.
          COSINE (int): Cosine distance.
        """

        DISTANCE_TYPE_UNSPECIFIED = 0
        EUCLIDEAN = 1
        COSINE = 2

    class LearnRateStrategy(enum.IntEnum):
        """
        Indicates the learning rate optimization strategy to use.

        Attributes:
          LEARN_RATE_STRATEGY_UNSPECIFIED (int)
          LINE_SEARCH (int): Use line search to determine learning rate.
          CONSTANT (int): Use a constant learning rate.
        """

        LEARN_RATE_STRATEGY_UNSPECIFIED = 0
        LINE_SEARCH = 1
        CONSTANT = 2

    class LossType(enum.IntEnum):
        """
        Loss metric to evaluate model training performance.

        Attributes:
          LOSS_TYPE_UNSPECIFIED (int)
          MEAN_SQUARED_LOSS (int): Mean squared loss, used for linear regression.
          MEAN_LOG_LOSS (int): Mean log loss, used for logistic regression.
        """

        LOSS_TYPE_UNSPECIFIED = 0
        MEAN_SQUARED_LOSS = 1
        MEAN_LOG_LOSS = 2

    class ModelType(enum.IntEnum):
        """
        Indicates the type of the Model.

        Attributes:
          MODEL_TYPE_UNSPECIFIED (int)
          LINEAR_REGRESSION (int): Linear regression model.
          LOGISTIC_REGRESSION (int): Logistic regression based classification model.
          KMEANS (int): K-means clustering model.
          TENSORFLOW (int): [Beta] An imported TensorFlow model.
        """

        MODEL_TYPE_UNSPECIFIED = 0
        LINEAR_REGRESSION = 1
        LOGISTIC_REGRESSION = 2
        KMEANS = 3
        TENSORFLOW = 6

    class OptimizationStrategy(enum.IntEnum):
        """
        Indicates the optimization strategy used for training.

        Attributes:
          OPTIMIZATION_STRATEGY_UNSPECIFIED (int)
          BATCH_GRADIENT_DESCENT (int): Uses an iterative batch gradient descent algorithm.
          NORMAL_EQUATION (int): Uses a normal equation to solve linear regression problem.
        """

        OPTIMIZATION_STRATEGY_UNSPECIFIED = 0
        BATCH_GRADIENT_DESCENT = 1
        NORMAL_EQUATION = 2

    class KmeansEnums(object):
        class KmeansInitializationMethod(enum.IntEnum):
            """
            Indicates the method used to initialize the centroids for KMeans
            clustering algorithm.

            Attributes:
              KMEANS_INITIALIZATION_METHOD_UNSPECIFIED (int)
              RANDOM (int): Initializes the centroids randomly.
              CUSTOM (int): Initializes the centroids using data specified in
              kmeans\_initialization\_column.
            """

            KMEANS_INITIALIZATION_METHOD_UNSPECIFIED = 0
            RANDOM = 1
            CUSTOM = 2


class StandardSqlDataType(object):
    class TypeKind(enum.IntEnum):
        """
        Attributes:
          TYPE_KIND_UNSPECIFIED (int): Invalid type.
          INT64 (int): Encoded as a string in decimal format.
          BOOL (int): Encoded as a boolean "false" or "true".
          FLOAT64 (int): Encoded as a number, or string "NaN", "Infinity" or "-Infinity".
          STRING (int): Encoded as a string value.
          BYTES (int): Encoded as a base64 string per RFC 4648, section 4.
          TIMESTAMP (int): Encoded as an RFC 3339 timestamp with mandatory "Z" time zone string:
          1985-04-12T23:20:50.52Z
          DATE (int): Encoded as RFC 3339 full-date format string: 1985-04-12
          TIME (int): Encoded as RFC 3339 partial-time format string: 23:20:50.52
          DATETIME (int): Encoded as RFC 3339 full-date "T" partial-time: 1985-04-12T23:20:50.52
          GEOGRAPHY (int): Encoded as WKT
          NUMERIC (int): Encoded as a decimal string.
          ARRAY (int): Encoded as a list with types matching Type.array\_type.
          STRUCT (int): Encoded as a list with fields of type Type.struct\_type[i]. List is used
          because a JSON object cannot have duplicate field names.
        """

        TYPE_KIND_UNSPECIFIED = 0
        INT64 = 2
        BOOL = 5
        FLOAT64 = 7
        STRING = 8
        BYTES = 9
        TIMESTAMP = 19
        DATE = 10
        TIME = 20
        DATETIME = 21
        GEOGRAPHY = 22
        NUMERIC = 23
        ARRAY = 16
        STRUCT = 17
