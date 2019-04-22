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


class AnnotateAssessmentRequest(object):
    class Annotation(enum.IntEnum):
        """
        Enum that reprensents the types of annotations.

        Attributes:
          ANNOTATION_UNSPECIFIED (int): Default unspecified type.
          LEGITIMATE (int): Provides information that the event turned out to be legitimate.
          FRAUDULENT (int): Provides information that the event turned out to be fraudulent.
        """

        ANNOTATION_UNSPECIFIED = 0
        LEGITIMATE = 1
        FRAUDULENT = 2


class Assessment(object):
    class ClassificationReason(enum.IntEnum):
        """
        LINT.IfChange(classification\_reason) Reasons contributing to the risk
        analysis verdict.

        Attributes:
          CLASSIFICATION_REASON_UNSPECIFIED (int): Default unspecified type.
          AUTOMATION (int): The event appeared to be automated.
          UNEXPECTED_ENVIRONMENT (int): The event was not made from the proper context on the real site.
          UNEXPECTED_USAGE_PATTERNS (int): Browsing behavior leading up to the event was generated was out of the
          ordinary.
          PROVISIONAL_RISK_ANALYSIS (int): Too little traffic has been received from this site thus far to generate
          quality risk analysis.
        """

        CLASSIFICATION_REASON_UNSPECIFIED = 0
        AUTOMATION = 1
        UNEXPECTED_ENVIRONMENT = 2
        UNEXPECTED_USAGE_PATTERNS = 4
        PROVISIONAL_RISK_ANALYSIS = 5


class TokenProperties(object):
    class InvalidReason(enum.IntEnum):
        """
        Enum that represents the types of invalid token reasons.

        Attributes:
          INVALID_REASON_UNSPECIFIED (int): Default unspecified type.
          UNKNOWN_INVALID_REASON (int): If the failure reason was not accounted for.
          MALFORMED (int): The provided user verification token was malformed.
          EXPIRED (int): The user verification token had expired.
          DUPE (int): The user verification had already been seen.
          SITE_MISMATCH (int): The user verification token did not match the provided site secret.
          This may be a configuration error (e.g. development keys used in
          production) or end users trying to use verification tokens from other
          sites.
          MISSING (int): The user verification token was not present.  It is a required input.
        """

        INVALID_REASON_UNSPECIFIED = 0
        UNKNOWN_INVALID_REASON = 1
        MALFORMED = 2
        EXPIRED = 3
        DUPE = 4
        SITE_MISMATCH = 5
        MISSING = 6
