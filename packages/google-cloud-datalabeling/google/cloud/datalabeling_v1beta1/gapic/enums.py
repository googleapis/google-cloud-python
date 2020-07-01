# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
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


class AnnotationSentiment(enum.IntEnum):
    """
    Attributes:
      ANNOTATION_SENTIMENT_UNSPECIFIED (int)
      NEGATIVE (int): This annotation describes negatively about the data.
      POSITIVE (int): This label describes positively about the data.
    """

    ANNOTATION_SENTIMENT_UNSPECIFIED = 0
    NEGATIVE = 1
    POSITIVE = 2


class AnnotationSource(enum.IntEnum):
    """
    Specifies where the annotation comes from (whether it was provided by a
    human labeler or a different source).

    Attributes:
      ANNOTATION_SOURCE_UNSPECIFIED (int)
      OPERATOR (int): Answer is provided by a human contributor.
    """

    ANNOTATION_SOURCE_UNSPECIFIED = 0
    OPERATOR = 3


class AnnotationType(enum.IntEnum):
    """
    Attributes:
      ANNOTATION_TYPE_UNSPECIFIED (int)
      IMAGE_CLASSIFICATION_ANNOTATION (int): Classification annotations in an image. Allowed for continuous evaluation.
      IMAGE_BOUNDING_BOX_ANNOTATION (int): Bounding box annotations in an image. A form of image object detection.
      Allowed for continuous evaluation.
      IMAGE_ORIENTED_BOUNDING_BOX_ANNOTATION (int): Oriented bounding box. The box does not have to be parallel to horizontal
      line.
      IMAGE_BOUNDING_POLY_ANNOTATION (int): Bounding poly annotations in an image.
      IMAGE_POLYLINE_ANNOTATION (int): Polyline annotations in an image.
      IMAGE_SEGMENTATION_ANNOTATION (int): Segmentation annotations in an image.
      VIDEO_SHOTS_CLASSIFICATION_ANNOTATION (int): Classification annotations in video shots.
      VIDEO_OBJECT_TRACKING_ANNOTATION (int): Video object tracking annotation.
      VIDEO_OBJECT_DETECTION_ANNOTATION (int): Video object detection annotation.
      VIDEO_EVENT_ANNOTATION (int): Video event annotation.
      TEXT_CLASSIFICATION_ANNOTATION (int): Classification for text. Allowed for continuous evaluation.
      TEXT_ENTITY_EXTRACTION_ANNOTATION (int): Entity extraction for text.
      GENERAL_CLASSIFICATION_ANNOTATION (int): General classification. Allowed for continuous evaluation.
    """

    ANNOTATION_TYPE_UNSPECIFIED = 0
    IMAGE_CLASSIFICATION_ANNOTATION = 1
    IMAGE_BOUNDING_BOX_ANNOTATION = 2
    IMAGE_ORIENTED_BOUNDING_BOX_ANNOTATION = 13
    IMAGE_BOUNDING_POLY_ANNOTATION = 10
    IMAGE_POLYLINE_ANNOTATION = 11
    IMAGE_SEGMENTATION_ANNOTATION = 12
    VIDEO_SHOTS_CLASSIFICATION_ANNOTATION = 3
    VIDEO_OBJECT_TRACKING_ANNOTATION = 4
    VIDEO_OBJECT_DETECTION_ANNOTATION = 5
    VIDEO_EVENT_ANNOTATION = 6
    TEXT_CLASSIFICATION_ANNOTATION = 8
    TEXT_ENTITY_EXTRACTION_ANNOTATION = 9
    GENERAL_CLASSIFICATION_ANNOTATION = 14


class DataType(enum.IntEnum):
    """
    Attributes:
      DATA_TYPE_UNSPECIFIED (int)
      IMAGE (int): Allowed for continuous evaluation.
      VIDEO (int)
      TEXT (int): Allowed for continuous evaluation.
      GENERAL_DATA (int): Allowed for continuous evaluation.
    """

    DATA_TYPE_UNSPECIFIED = 0
    IMAGE = 1
    VIDEO = 2
    TEXT = 4
    GENERAL_DATA = 6


class StringAggregationType(enum.IntEnum):
    """
    Attributes:
      STRING_AGGREGATION_TYPE_UNSPECIFIED (int)
      MAJORITY_VOTE (int): Majority vote to aggregate answers.
      UNANIMOUS_VOTE (int): Unanimous answers will be adopted.
      NO_AGGREGATION (int): Preserve all answers by crowd compute.
    """

    STRING_AGGREGATION_TYPE_UNSPECIFIED = 0
    MAJORITY_VOTE = 1
    UNANIMOUS_VOTE = 2
    NO_AGGREGATION = 3


class EvaluationJob(object):
    class State(enum.IntEnum):
        """
        State of the job.

        Attributes:
          STATE_UNSPECIFIED (int)
          SCHEDULED (int): The job is scheduled to run at the ``configured interval``. You can
          ``pause`` or ``delete`` the job.

          When the job is in this state, it samples prediction input and output
          from your model version into your BigQuery table as predictions occur.
          RUNNING (int): The job is currently running. When the job runs, Data Labeling
          Service does several things:

          1. If you have configured your job to use Data Labeling Service for
             ground truth labeling, the service creates a ``Dataset`` and a
             labeling task for all data sampled since the last time the job ran.
             Human labelers provide ground truth labels for your data. Human
             labeling may take hours, or even days, depending on how much data has
             been sampled. The job remains in the ``RUNNING`` state during this
             time, and it can even be running multiple times in parallel if it
             gets triggered again (for example 24 hours later) before the earlier
             run has completed. When human labelers have finished labeling the
             data, the next step occurs. If you have configured your job to
             provide your own ground truth labels, Data Labeling Service still
             creates a ``Dataset`` for newly sampled data, but it expects that you
             have already added ground truth labels to the BigQuery table by this
             time. The next step occurs immediately.

          2. Data Labeling Service creates an ``Evaluation`` by comparing your
             model version's predictions with the ground truth labels.

          If the job remains in this state for a long time, it continues to sample
          prediction data into your BigQuery table and will run again at the next
          interval, even if it causes the job to run multiple times in parallel.
          PAUSED (int): The job is not sampling prediction input and output into your
          BigQuery table and it will not run according to its schedule. You can
          ``resume`` the job.
          STOPPED (int): The job has this state right before it is deleted.
        """

        STATE_UNSPECIFIED = 0
        SCHEDULED = 1
        RUNNING = 2
        PAUSED = 3
        STOPPED = 4


class LabelImageRequest(object):
    class Feature(enum.IntEnum):
        """
        Image labeling task feature.

        Attributes:
          FEATURE_UNSPECIFIED (int)
          CLASSIFICATION (int): Label whole image with one or more of labels.
          BOUNDING_BOX (int): Label image with bounding boxes for labels.
          ORIENTED_BOUNDING_BOX (int): Label oriented bounding box. The box does not have to be parallel to
          horizontal line.
          BOUNDING_POLY (int): Label images with bounding poly. A bounding poly is a plane figure that
          is bounded by a finite chain of straight line segments closing in a loop.
          POLYLINE (int): Label images with polyline. Polyline is formed by connected line segments
          which are not in closed form.
          SEGMENTATION (int): Label images with segmentation. Segmentation is different from bounding
          poly since it is more fine-grained, pixel level annotation.
        """

        FEATURE_UNSPECIFIED = 0
        CLASSIFICATION = 1
        BOUNDING_BOX = 2
        ORIENTED_BOUNDING_BOX = 6
        BOUNDING_POLY = 3
        POLYLINE = 4
        SEGMENTATION = 5


class LabelTextRequest(object):
    class Feature(enum.IntEnum):
        """
        Text labeling task feature.

        Attributes:
          FEATURE_UNSPECIFIED (int)
          TEXT_CLASSIFICATION (int): Label text content to one of more labels.
          TEXT_ENTITY_EXTRACTION (int): Label entities and their span in text.
        """

        FEATURE_UNSPECIFIED = 0
        TEXT_CLASSIFICATION = 1
        TEXT_ENTITY_EXTRACTION = 2


class LabelVideoRequest(object):
    class Feature(enum.IntEnum):
        """
        Video labeling task feature.

        Attributes:
          FEATURE_UNSPECIFIED (int)
          CLASSIFICATION (int): Label whole video or video segment with one or more labels.
          OBJECT_DETECTION (int): Label objects with bounding box on image frames extracted from the video.
          OBJECT_TRACKING (int): Label and track objects in video.
          EVENT (int): Label the range of video for the specified events.
        """

        FEATURE_UNSPECIFIED = 0
        CLASSIFICATION = 1
        OBJECT_DETECTION = 2
        OBJECT_TRACKING = 3
        EVENT = 4
