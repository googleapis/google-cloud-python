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


class Likelihood(enum.IntEnum):
    """
    A bucketized representation of likelihood, which is intended to give clients
    highly stable results across model upgrades.

    Attributes:
      UNKNOWN (int): Unknown likelihood.
      VERY_UNLIKELY (int): It is very unlikely that the image belongs to the specified vertical.
      UNLIKELY (int): It is unlikely that the image belongs to the specified vertical.
      POSSIBLE (int): It is possible that the image belongs to the specified vertical.
      LIKELY (int): It is likely that the image belongs to the specified vertical.
      VERY_LIKELY (int): It is very likely that the image belongs to the specified vertical.
    """

    UNKNOWN = 0
    VERY_UNLIKELY = 1
    UNLIKELY = 2
    POSSIBLE = 3
    LIKELY = 4
    VERY_LIKELY = 5


class ProductSearchCategory(enum.IntEnum):
    """
    Supported product search categories.

    Attributes:
      PRODUCT_SEARCH_CATEGORY_UNSPECIFIED (int): Default value used when a category is not specified.
      SHOES (int): Shoes category.
      BAGS (int): Bags category.
    """

    PRODUCT_SEARCH_CATEGORY_UNSPECIFIED = 0
    SHOES = 1
    BAGS = 2


class ProductSearchResultsView(enum.IntEnum):
    """
    Specifies the fields to include in product search results.

    Attributes:
      BASIC (int): Product search results contain only ``product_category`` and
      ``product_id``. Default value.
      FULL (int): Product search results contain ``product_category``, ``product_id``,
      ``image_uri``, and ``score``.
    """

    BASIC = 0
    FULL = 1


class BatchOperationMetadata(object):
    class State(enum.IntEnum):
        """
        Enumerates the possible states that the batch request can be in.

        Attributes:
          STATE_UNSPECIFIED (int): Invalid.
          PROCESSING (int): Request is actively being processed.
          SUCCESSFUL (int): The request is done and at least one item has been successfully
          processed.
          FAILED (int): The request is done and no item has been successfully processed.
          CANCELLED (int): The request is done after the longrunning.Operations.CancelOperation has
          been called by the user.  Any records that were processed before the
          cancel command are output as specified in the request.
        """

        STATE_UNSPECIFIED = 0
        PROCESSING = 1
        SUCCESSFUL = 2
        FAILED = 3
        CANCELLED = 4


class Block(object):
    class BlockType(enum.IntEnum):
        """
        Type of a block (text, image etc) as identified by OCR.

        Attributes:
          UNKNOWN (int): Unknown block type.
          TEXT (int): Regular text block.
          TABLE (int): Table block.
          PICTURE (int): Image block.
          RULER (int): Horizontal/vertical line box.
          BARCODE (int): Barcode block.
        """

        UNKNOWN = 0
        TEXT = 1
        TABLE = 2
        PICTURE = 3
        RULER = 4
        BARCODE = 5


class FaceAnnotation(object):
    class Landmark(object):
        class Type(enum.IntEnum):
            """
            Face landmark (feature) type. Left and right are defined from the
            vantage of the viewer of the image without considering mirror
            projections typical of photos. So, ``LEFT_EYE``, typically, is the
            person's right eye.

            Attributes:
              UNKNOWN_LANDMARK (int): Unknown face landmark detected. Should not be filled.
              LEFT_EYE (int): Left eye.
              RIGHT_EYE (int): Right eye.
              LEFT_OF_LEFT_EYEBROW (int): Left of left eyebrow.
              RIGHT_OF_LEFT_EYEBROW (int): Right of left eyebrow.
              LEFT_OF_RIGHT_EYEBROW (int): Left of right eyebrow.
              RIGHT_OF_RIGHT_EYEBROW (int): Right of right eyebrow.
              MIDPOINT_BETWEEN_EYES (int): Midpoint between eyes.
              NOSE_TIP (int): Nose tip.
              UPPER_LIP (int): Upper lip.
              LOWER_LIP (int): Lower lip.
              MOUTH_LEFT (int): Mouth left.
              MOUTH_RIGHT (int): Mouth right.
              MOUTH_CENTER (int): Mouth center.
              NOSE_BOTTOM_RIGHT (int): Nose, bottom right.
              NOSE_BOTTOM_LEFT (int): Nose, bottom left.
              NOSE_BOTTOM_CENTER (int): Nose, bottom center.
              LEFT_EYE_TOP_BOUNDARY (int): Left eye, top boundary.
              LEFT_EYE_RIGHT_CORNER (int): Left eye, right corner.
              LEFT_EYE_BOTTOM_BOUNDARY (int): Left eye, bottom boundary.
              LEFT_EYE_LEFT_CORNER (int): Left eye, left corner.
              RIGHT_EYE_TOP_BOUNDARY (int): Right eye, top boundary.
              RIGHT_EYE_RIGHT_CORNER (int): Right eye, right corner.
              RIGHT_EYE_BOTTOM_BOUNDARY (int): Right eye, bottom boundary.
              RIGHT_EYE_LEFT_CORNER (int): Right eye, left corner.
              LEFT_EYEBROW_UPPER_MIDPOINT (int): Left eyebrow, upper midpoint.
              RIGHT_EYEBROW_UPPER_MIDPOINT (int): Right eyebrow, upper midpoint.
              LEFT_EAR_TRAGION (int): Left ear tragion.
              RIGHT_EAR_TRAGION (int): Right ear tragion.
              LEFT_EYE_PUPIL (int): Left eye pupil.
              RIGHT_EYE_PUPIL (int): Right eye pupil.
              FOREHEAD_GLABELLA (int): Forehead glabella.
              CHIN_GNATHION (int): Chin gnathion.
              CHIN_LEFT_GONION (int): Chin left gonion.
              CHIN_RIGHT_GONION (int): Chin right gonion.
            """

            UNKNOWN_LANDMARK = 0
            LEFT_EYE = 1
            RIGHT_EYE = 2
            LEFT_OF_LEFT_EYEBROW = 3
            RIGHT_OF_LEFT_EYEBROW = 4
            LEFT_OF_RIGHT_EYEBROW = 5
            RIGHT_OF_RIGHT_EYEBROW = 6
            MIDPOINT_BETWEEN_EYES = 7
            NOSE_TIP = 8
            UPPER_LIP = 9
            LOWER_LIP = 10
            MOUTH_LEFT = 11
            MOUTH_RIGHT = 12
            MOUTH_CENTER = 13
            NOSE_BOTTOM_RIGHT = 14
            NOSE_BOTTOM_LEFT = 15
            NOSE_BOTTOM_CENTER = 16
            LEFT_EYE_TOP_BOUNDARY = 17
            LEFT_EYE_RIGHT_CORNER = 18
            LEFT_EYE_BOTTOM_BOUNDARY = 19
            LEFT_EYE_LEFT_CORNER = 20
            RIGHT_EYE_TOP_BOUNDARY = 21
            RIGHT_EYE_RIGHT_CORNER = 22
            RIGHT_EYE_BOTTOM_BOUNDARY = 23
            RIGHT_EYE_LEFT_CORNER = 24
            LEFT_EYEBROW_UPPER_MIDPOINT = 25
            RIGHT_EYEBROW_UPPER_MIDPOINT = 26
            LEFT_EAR_TRAGION = 27
            RIGHT_EAR_TRAGION = 28
            LEFT_EYE_PUPIL = 29
            RIGHT_EYE_PUPIL = 30
            FOREHEAD_GLABELLA = 31
            CHIN_GNATHION = 32
            CHIN_LEFT_GONION = 33
            CHIN_RIGHT_GONION = 34


class Feature(object):
    class Type(enum.IntEnum):
        """
        Type of Google Cloud Vision API feature to be extracted.

        Attributes:
          TYPE_UNSPECIFIED (int): Unspecified feature type.
          FACE_DETECTION (int): Run face detection.
          LANDMARK_DETECTION (int): Run landmark detection.
          LOGO_DETECTION (int): Run logo detection.
          LABEL_DETECTION (int): Run label detection.
          TEXT_DETECTION (int): Run text detection / optical character recognition (OCR). Text detection
          is optimized for areas of text within a larger image; if the image is a
          document, use ``DOCUMENT_TEXT_DETECTION`` instead.
          DOCUMENT_TEXT_DETECTION (int): Run dense text document OCR. Takes precedence when both
          ``DOCUMENT_TEXT_DETECTION`` and ``TEXT_DETECTION`` are present.
          SAFE_SEARCH_DETECTION (int): Run Safe Search to detect potentially unsafe
          or undesirable content.
          IMAGE_PROPERTIES (int): Compute a set of image properties, such as the
          image's dominant colors.
          CROP_HINTS (int): Run crop hints.
          WEB_DETECTION (int): Run web detection.
          PRODUCT_SEARCH (int): Run Product Search.
          OBJECT_LOCALIZATION (int): Run localizer for object detection.
        """

        TYPE_UNSPECIFIED = 0
        FACE_DETECTION = 1
        LANDMARK_DETECTION = 2
        LOGO_DETECTION = 3
        LABEL_DETECTION = 4
        TEXT_DETECTION = 5
        DOCUMENT_TEXT_DETECTION = 11
        SAFE_SEARCH_DETECTION = 6
        IMAGE_PROPERTIES = 7
        CROP_HINTS = 9
        WEB_DETECTION = 10
        PRODUCT_SEARCH = 12
        OBJECT_LOCALIZATION = 19


class OperationMetadata(object):
    class State(enum.IntEnum):
        """
        Batch operation states.

        Attributes:
          STATE_UNSPECIFIED (int): Invalid.
          CREATED (int): Request is received.
          RUNNING (int): Request is actively being processed.
          DONE (int): The batch processing is done.
          CANCELLED (int): The batch processing was cancelled.
        """

        STATE_UNSPECIFIED = 0
        CREATED = 1
        RUNNING = 2
        DONE = 3
        CANCELLED = 4


class TextAnnotation(object):
    class DetectedBreak(object):
        class BreakType(enum.IntEnum):
            """
            Enum to denote the type of break found. New line, space etc.

            Attributes:
              UNKNOWN (int): Unknown break label type.
              SPACE (int): Regular space.
              SURE_SPACE (int): Sure space (very wide).
              EOL_SURE_SPACE (int): Line-wrapping break.
              HYPHEN (int): End-line hyphen that is not present in text; does not co-occur with
              ``SPACE``, ``LEADER_SPACE``, or ``LINE_BREAK``.
              LINE_BREAK (int): Line break that ends a paragraph.
            """

            UNKNOWN = 0
            SPACE = 1
            SURE_SPACE = 2
            EOL_SURE_SPACE = 3
            HYPHEN = 4
            LINE_BREAK = 5
