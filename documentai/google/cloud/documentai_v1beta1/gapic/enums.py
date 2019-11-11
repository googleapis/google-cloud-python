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


class Document(object):
    class Page(object):
        class Layout(object):
            class Orientation(enum.IntEnum):
                """
                Detected human reading orientation.

                Attributes:
                  ORIENTATION_UNSPECIFIED (int): Unspecified orientation.
                  PAGE_UP (int): Orientation is aligned with page up.
                  PAGE_RIGHT (int): Orientation is aligned with page right.
                  Turn the head 90 degrees clockwise from upright to read.
                  PAGE_DOWN (int): Orientation is aligned with page down.
                  Turn the head 180 degrees from upright to read.
                  PAGE_LEFT (int): Orientation is aligned with page left.
                  Turn the head 90 degrees counterclockwise from upright to read.
                """

                ORIENTATION_UNSPECIFIED = 0
                PAGE_UP = 1
                PAGE_RIGHT = 2
                PAGE_DOWN = 3
                PAGE_LEFT = 4

        class Token(object):
            class DetectedBreak(object):
                class Type(enum.IntEnum):
                    """
                    Enum to denote the type of break found.

                    Attributes:
                      TYPE_UNSPECIFIED (int): Unspecified break type.
                      SPACE (int): A single whitespace.
                      WIDE_SPACE (int): A wider whitespace.
                      HYPHEN (int): A hyphen that indicates that a token has been split across lines.
                    """

                    TYPE_UNSPECIFIED = 0
                    SPACE = 1
                    WIDE_SPACE = 2
                    HYPHEN = 3


class OperationMetadata(object):
    class State(enum.IntEnum):
        """
        Attributes:
          STATE_UNSPECIFIED (int): The default value. This value is used if the state is omitted.
          ACCEPTED (int): Request is received.
          WAITING (int): Request operation is waiting for scheduling.
          RUNNING (int): Request is being processed.
          SUCCEEDED (int): The batch processing completed successfully.
          CANCELLED (int): The batch processing was cancelled.
          FAILED (int): The batch processing has failed.
        """

        STATE_UNSPECIFIED = 0
        ACCEPTED = 1
        WAITING = 2
        RUNNING = 3
        SUCCEEDED = 4
        CANCELLED = 5
        FAILED = 6
