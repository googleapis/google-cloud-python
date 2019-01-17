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
      SHOT_CHANGE_DETECTION (int): Shot change detection.
      EXPLICIT_CONTENT_DETECTION (int): Explicit content detection.
      FACE_DETECTION (int): Human face detection and tracking.
      SPEECH_TRANSCRIPTION (int): Speech transcription.
    """

    FEATURE_UNSPECIFIED = 0
    LABEL_DETECTION = 1
    SHOT_CHANGE_DETECTION = 2
    EXPLICIT_CONTENT_DETECTION = 3
    FACE_DETECTION = 4
    SPEECH_TRANSCRIPTION = 6


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


class Likelihood(enum.IntEnum):
    """
    Bucketized representation of likelihood.

    Attributes:
      LIKELIHOOD_UNSPECIFIED (int): Unspecified likelihood.
      VERY_UNLIKELY (int): Very unlikely.
      UNLIKELY (int): Unlikely.
      POSSIBLE (int): Possible.
      LIKELY (int): Likely.
      VERY_LIKELY (int): Very likely.
    """

    LIKELIHOOD_UNSPECIFIED = 0
    VERY_UNLIKELY = 1
    UNLIKELY = 2
    POSSIBLE = 3
    LIKELY = 4
    VERY_LIKELY = 5
