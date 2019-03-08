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


class Feature(enum.IntEnum):
    """
    Video annotation feature.

    Attributes:
      FEATURE_UNSPECIFIED (int): Unspecified.
      LABEL_DETECTION (int): Label detection. Detect objects, such as dog or flower.
      FACE_DETECTION (int): Human face detection and tracking.
      SHOT_CHANGE_DETECTION (int): Shot change detection.
      SAFE_SEARCH_DETECTION (int): Safe search detection.
    """

    FEATURE_UNSPECIFIED = 0
    LABEL_DETECTION = 1
    FACE_DETECTION = 2
    SHOT_CHANGE_DETECTION = 3
    SAFE_SEARCH_DETECTION = 4


class LabelDetectionMode(enum.IntEnum):
    """
    Label detection mode.

    Attributes:
      LABEL_DETECTION_MODE_UNSPECIFIED (int): Unspecified.
      SHOT_MODE (int): Detect shot-level labels.
      FRAME_MODE (int): Detect frame-level labels.
      SHOT_AND_FRAME_MODE (int): Detect both shot-level and frame-level labels.
    """

    LABEL_DETECTION_MODE_UNSPECIFIED = 0
    SHOT_MODE = 1
    FRAME_MODE = 2
    SHOT_AND_FRAME_MODE = 3


class LabelLevel(enum.IntEnum):
    """
    Label level (scope).

    Attributes:
      LABEL_LEVEL_UNSPECIFIED (int): Unspecified.
      VIDEO_LEVEL (int): Video-level. Corresponds to the whole video.
      SEGMENT_LEVEL (int): Segment-level. Corresponds to one of ``AnnotateSpec.segments``.
      SHOT_LEVEL (int): Shot-level. Corresponds to a single shot (i.e. a series of frames
      without a major camera position or background change).
      FRAME_LEVEL (int): Frame-level. Corresponds to a single video frame.
    """

    LABEL_LEVEL_UNSPECIFIED = 0
    VIDEO_LEVEL = 1
    SEGMENT_LEVEL = 2
    SHOT_LEVEL = 3
    FRAME_LEVEL = 4


class Likelihood(enum.IntEnum):
    """
    Bucketized representation of likelihood.

    Attributes:
      UNKNOWN (int): Unknown likelihood.
      VERY_UNLIKELY (int): Very unlikely.
      UNLIKELY (int): Unlikely.
      POSSIBLE (int): Possible.
      LIKELY (int): Likely.
      VERY_LIKELY (int): Very likely.
    """

    UNKNOWN = 0
    VERY_UNLIKELY = 1
    UNLIKELY = 2
    POSSIBLE = 3
    LIKELY = 4
    VERY_LIKELY = 5
