# Copyright 2018 Google LLC
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


class Likelihood(object):
    """
    Categorization of results based on how likely they are to represent a match,
    based on the number of elements they contain which imply a match.

    Attributes:
      LIKELIHOOD_UNSPECIFIED (int): Default value; information with all likelihoods is included.
      VERY_UNLIKELY (int): Few matching elements.
      UNLIKELY (int)
      POSSIBLE (int): Some matching elements.
      LIKELY (int)
      VERY_LIKELY (int): Many matching elements.
    """
    LIKELIHOOD_UNSPECIFIED = 0
    VERY_UNLIKELY = 1
    UNLIKELY = 2
    POSSIBLE = 3
    LIKELY = 4
    VERY_LIKELY = 5


class RelationalOperator(object):
    """
    Operators available for comparing the value of fields.

    Attributes:
      RELATIONAL_OPERATOR_UNSPECIFIED (int)
      EQUAL_TO (int): Equal.
      NOT_EQUAL_TO (int): Not equal to.
      GREATER_THAN (int): Greater than.
      LESS_THAN (int): Less than.
      GREATER_THAN_OR_EQUALS (int): Greater than or equals.
      LESS_THAN_OR_EQUALS (int): Less than or equals.
      EXISTS (int): Exists
    """
    RELATIONAL_OPERATOR_UNSPECIFIED = 0
    EQUAL_TO = 1
    NOT_EQUAL_TO = 2
    GREATER_THAN = 3
    LESS_THAN = 4
    GREATER_THAN_OR_EQUALS = 5
    LESS_THAN_OR_EQUALS = 6
    EXISTS = 7


class TimePartConfig(object):
    class TimePart(object):
        """
        Attributes:
          TIME_PART_UNSPECIFIED (int)
          YEAR (int): [000-9999]
          MONTH (int): [1-12]
          DAY_OF_MONTH (int): [1-31]
          DAY_OF_WEEK (int): [1-7]
          WEEK_OF_YEAR (int): [1-52]
          HOUR_OF_DAY (int): [0-24]
        """
        TIME_PART_UNSPECIFIED = 0
        YEAR = 1
        MONTH = 2
        DAY_OF_MONTH = 3
        DAY_OF_WEEK = 4
        WEEK_OF_YEAR = 5
        HOUR_OF_DAY = 6


class CharsToIgnore(object):
    class CharacterGroup(object):
        """
        Attributes:
          CHARACTER_GROUP_UNSPECIFIED (int)
          NUMERIC (int): 0-9
          ALPHA_UPPER_CASE (int): A-Z
          ALPHA_LOWER_CASE (int): a-z
          PUNCTUATION (int): US Punctuation, one of !\"#$%&'()*+,-./:;<=>?@[\]^_``{|}~
          WHITESPACE (int): Whitespace character, one of [ \t\n\x0B\f\r]
        """
        CHARACTER_GROUP_UNSPECIFIED = 0
        NUMERIC = 1
        ALPHA_UPPER_CASE = 2
        ALPHA_LOWER_CASE = 3
        PUNCTUATION = 4
        WHITESPACE = 5


class CryptoReplaceFfxFpeConfig(object):
    class FfxCommonNativeAlphabet(object):
        """
        These are commonly used subsets of the alphabet that the FFX mode
        natively supports. In the algorithm, the alphabet is selected using
        the \"radix\". Therefore each corresponds to particular radix.

        Attributes:
          FFX_COMMON_NATIVE_ALPHABET_UNSPECIFIED (int)
          NUMERIC (int): [0-9] (radix of 10)
          HEXADECIMAL (int): [0-9A-F] (radix of 16)
          UPPER_CASE_ALPHA_NUMERIC (int): [0-9A-Z] (radix of 36)
          ALPHA_NUMERIC (int): [0-9A-Za-z] (radix of 62)
        """
        FFX_COMMON_NATIVE_ALPHABET_UNSPECIFIED = 0
        NUMERIC = 1
        HEXADECIMAL = 2
        UPPER_CASE_ALPHA_NUMERIC = 3
        ALPHA_NUMERIC = 4


class RecordCondition(object):
    class Expressions(object):
        class LogicalOperator(object):
            """
            Attributes:
              LOGICAL_OPERATOR_UNSPECIFIED (int)
              AND (int)
            """
            LOGICAL_OPERATOR_UNSPECIFIED = 0
            AND = 1


class TransformationSummary(object):
    class TransformationResultCode(object):
        """
        Possible outcomes of transformations.

        Attributes:
          TRANSFORMATION_RESULT_CODE_UNSPECIFIED (int)
          SUCCESS (int)
          ERROR (int)
        """
        TRANSFORMATION_RESULT_CODE_UNSPECIFIED = 0
        SUCCESS = 1
        ERROR = 2
