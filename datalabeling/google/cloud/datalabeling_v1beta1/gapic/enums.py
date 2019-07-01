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
    Specifies where is the answer from.

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
      IMAGE_CLASSIFICATION_ANNOTATION (int): Classification annotations in an image.
      IMAGE_BOUNDING_BOX_ANNOTATION (int): Bounding box annotations in an image.
      IMAGE_ORIENTED_BOUNDING_BOX_ANNOTATION (int): Oriented bounding box. The box does not have to be parallel to horizontal
      line.
      IMAGE_BOUNDING_POLY_ANNOTATION (int): Bounding poly annotations in an image.
      IMAGE_POLYLINE_ANNOTATION (int): Polyline annotations in an image.
      IMAGE_SEGMENTATION_ANNOTATION (int): Segmentation annotations in an image.
      VIDEO_SHOTS_CLASSIFICATION_ANNOTATION (int): Classification annotations in video shots.
      VIDEO_OBJECT_TRACKING_ANNOTATION (int): Video object tracking annotation.
      VIDEO_OBJECT_DETECTION_ANNOTATION (int): Video object detection annotation.
      VIDEO_EVENT_ANNOTATION (int): Video event annotation.
      TEXT_CLASSIFICATION_ANNOTATION (int): Classification for text.
      TEXT_ENTITY_EXTRACTION_ANNOTATION (int): Entity extraction for text.
      GENERAL_CLASSIFICATION_ANNOTATION (int): General classification.
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
      IMAGE (int)
      VIDEO (int)
      TEXT (int)
      GENERAL_DATA (int)
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
          SCHEDULED (int)
          RUNNING (int)
          PAUSED (int)
          STOPPED (int)
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
