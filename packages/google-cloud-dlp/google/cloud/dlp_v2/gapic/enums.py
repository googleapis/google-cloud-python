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


class ContentOption(enum.IntEnum):
    """
    Options describing which parts of the provided content should be scanned.

    Attributes:
      CONTENT_UNSPECIFIED (int): Includes entire content of a file or a data stream.
      CONTENT_TEXT (int): Text content within the data, excluding any metadata.
      CONTENT_IMAGE (int): Images found in the data.
    """

    CONTENT_UNSPECIFIED = 0
    CONTENT_TEXT = 1
    CONTENT_IMAGE = 2


class DayOfWeek(enum.IntEnum):
    """
    Represents a day of week.

    Attributes:
      DAY_OF_WEEK_UNSPECIFIED (int): The unspecified day-of-week.
      MONDAY (int): The day-of-week of Monday.
      TUESDAY (int): The day-of-week of Tuesday.
      WEDNESDAY (int): The day-of-week of Wednesday.
      THURSDAY (int): The day-of-week of Thursday.
      FRIDAY (int): The day-of-week of Friday.
      SATURDAY (int): The day-of-week of Saturday.
      SUNDAY (int): The day-of-week of Sunday.
    """

    DAY_OF_WEEK_UNSPECIFIED = 0
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


class DlpJobType(enum.IntEnum):
    """
    An enum to represent the various types of DLP jobs.

    Attributes:
      DLP_JOB_TYPE_UNSPECIFIED (int): Unused
      INSPECT_JOB (int): The job inspected Google Cloud for sensitive data.
      RISK_ANALYSIS_JOB (int): The job executed a Risk Analysis computation.
    """

    DLP_JOB_TYPE_UNSPECIFIED = 0
    INSPECT_JOB = 1
    RISK_ANALYSIS_JOB = 2


class FileType(enum.IntEnum):
    """
    Definitions of file type groups to scan.

    Attributes:
      FILE_TYPE_UNSPECIFIED (int): Includes all files.
      BINARY_FILE (int): Includes all file extensions not covered by text file types.
      TEXT_FILE (int): Included file extensions:
        asc, brf, c, cc, cpp, csv, cxx, c++, cs, css, dart, eml, go, h, hh, hpp,
        hxx, h++, hs, html, htm, shtml, shtm, xhtml, lhs, ini, java, js, json,
        ocaml, md, mkd, markdown, m, ml, mli, pl, pm, php, phtml, pht, py, pyw,
        rb, rbw, rs, rc, scala, sh, sql, tex, txt, text, tsv, vcard, vcs, wml,
        xml, xsl, xsd, yml, yaml.
      IMAGE (int): Included file extensions: bmp, gif, jpg, jpeg, jpe, png.
      bytes_limit_per_file has no effect on image files. Image inspection is
      restricted to 'global', 'us', 'asia', and 'europe'.
      WORD (int): Included file extensions:
        docx, dotx, docm, dotm
      PDF (int): Included file extensions:
        pdf
      AVRO (int): Included file extensions:
        avro
    """

    FILE_TYPE_UNSPECIFIED = 0
    BINARY_FILE = 1
    TEXT_FILE = 2
    IMAGE = 3
    WORD = 5
    PDF = 6
    AVRO = 7


class InfoTypeSupportedBy(enum.IntEnum):
    """
    Parts of the APIs which use certain infoTypes.

    Attributes:
      ENUM_TYPE_UNSPECIFIED (int): Unused.
      INSPECT (int): Supported by the inspect operations.
      RISK_ANALYSIS (int): Supported by the risk analysis operations.
    """

    ENUM_TYPE_UNSPECIFIED = 0
    INSPECT = 1
    RISK_ANALYSIS = 2


class Likelihood(enum.IntEnum):
    """
    Categorization of results based on how likely they are to represent a match,
    based on the number of elements they contain which imply a match.

    Attributes:
      LIKELIHOOD_UNSPECIFIED (int): Default value; same as POSSIBLE.
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


class MatchingType(enum.IntEnum):
    """
    Type of the match which can be applied to different ways of matching, like
    Dictionary, regular expression and intersecting with findings of another
    info type.

    Attributes:
      MATCHING_TYPE_UNSPECIFIED (int): Invalid.
      MATCHING_TYPE_FULL_MATCH (int): Full match.

      - Dictionary: join of Dictionary results matched complete finding quote
      - Regex: all regex matches fill a finding quote start to end
      - Exclude info type: completely inside affecting info types findings
      MATCHING_TYPE_PARTIAL_MATCH (int): Partial match.

      - Dictionary: at least one of the tokens in the finding matches
      - Regex: substring of the finding matches
      - Exclude info type: intersects with affecting info types findings
      MATCHING_TYPE_INVERSE_MATCH (int): Inverse match.

      - Dictionary: no tokens in the finding match the dictionary
      - Regex: finding doesn't match the regex
      - Exclude info type: no intersection with affecting info types findings
    """

    MATCHING_TYPE_UNSPECIFIED = 0
    MATCHING_TYPE_FULL_MATCH = 1
    MATCHING_TYPE_PARTIAL_MATCH = 2
    MATCHING_TYPE_INVERSE_MATCH = 3


class MetadataType(enum.IntEnum):
    """
    Type of metadata containing the finding.

    Attributes:
      METADATATYPE_UNSPECIFIED (int): Unused
      STORAGE_METADATA (int): General file metadata provided by GCS.
    """

    METADATATYPE_UNSPECIFIED = 0
    STORAGE_METADATA = 2


class RelationalOperator(enum.IntEnum):
    """
    Operators available for comparing the value of fields.

    Attributes:
      RELATIONAL_OPERATOR_UNSPECIFIED (int): Unused
      EQUAL_TO (int): Equal. Attempts to match even with incompatible types.
      NOT_EQUAL_TO (int): Not equal to. Attempts to match even with incompatible types.
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


class StoredInfoTypeState(enum.IntEnum):
    """
    State of a StoredInfoType version.

    Attributes:
      STORED_INFO_TYPE_STATE_UNSPECIFIED (int): Unused
      PENDING (int): StoredInfoType version is being created.
      READY (int): StoredInfoType version is ready for use.
      FAILED (int): StoredInfoType creation failed. All relevant error messages are
      returned in the ``StoredInfoTypeVersion`` message.
      INVALID (int): StoredInfoType is no longer valid because artifacts stored in
      user-controlled storage were modified. To fix an invalid StoredInfoType,
      use the ``UpdateStoredInfoType`` method to create a new version.
    """

    STORED_INFO_TYPE_STATE_UNSPECIFIED = 0
    PENDING = 1
    READY = 2
    FAILED = 3
    INVALID = 4


class BigQueryOptions(object):
    class SampleMethod(enum.IntEnum):
        """
        How to sample rows if not all rows are scanned. Meaningful only when
        used in conjunction with either rows_limit or rows_limit_percent. If not
        specified, scanning would start from the top.

        Attributes:
          SAMPLE_METHOD_UNSPECIFIED (int)
          TOP (int): Scan from the top (default).
          RANDOM_START (int): Randomly pick the row to start scanning. The scanned rows are contiguous.
        """

        SAMPLE_METHOD_UNSPECIFIED = 0
        TOP = 1
        RANDOM_START = 2


class ByteContentItem(object):
    class BytesType(enum.IntEnum):
        """
        The type of data being sent for inspection.

        Attributes:
          BYTES_TYPE_UNSPECIFIED (int): Unused
          IMAGE (int): Any image type.
          IMAGE_JPEG (int): jpeg
          IMAGE_BMP (int): bmp
          IMAGE_PNG (int): png
          IMAGE_SVG (int): svg
          TEXT_UTF8 (int): plain text
          WORD_DOCUMENT (int): docx, docm, dotx, dotm
          PDF (int): pdf
          AVRO (int): avro
        """

        BYTES_TYPE_UNSPECIFIED = 0
        IMAGE = 6
        IMAGE_JPEG = 1
        IMAGE_BMP = 2
        IMAGE_PNG = 3
        IMAGE_SVG = 4
        TEXT_UTF8 = 5
        WORD_DOCUMENT = 7
        PDF = 8
        AVRO = 11


class CharsToIgnore(object):
    class CommonCharsToIgnore(enum.IntEnum):
        """
        Convenience enum for indication common characters to not transform.

        Attributes:
          COMMON_CHARS_TO_IGNORE_UNSPECIFIED (int): Unused.
          NUMERIC (int): 0-9
          ALPHA_UPPER_CASE (int): A-Z
          ALPHA_LOWER_CASE (int): a-z
          PUNCTUATION (int): US Punctuation, one of !"#$%&'()*+,-./:;<=>?@[]^_`{|}~
          WHITESPACE (int): Whitespace character
        """

        COMMON_CHARS_TO_IGNORE_UNSPECIFIED = 0
        NUMERIC = 1
        ALPHA_UPPER_CASE = 2
        ALPHA_LOWER_CASE = 3
        PUNCTUATION = 4
        WHITESPACE = 5


class CloudStorageOptions(object):
    class SampleMethod(enum.IntEnum):
        """
        How to sample bytes if not all bytes are scanned. Meaningful only
        when used in conjunction with bytes_limit_per_file. If not specified,
        scanning would start from the top.

        Attributes:
          SAMPLE_METHOD_UNSPECIFIED (int)
          TOP (int): Scan from the top (default).
          RANDOM_START (int): For each file larger than bytes_limit_per_file, randomly pick the
          offset to start scanning. The scanned bytes are contiguous.
        """

        SAMPLE_METHOD_UNSPECIFIED = 0
        TOP = 1
        RANDOM_START = 2


class CryptoReplaceFfxFpeConfig(object):
    class FfxCommonNativeAlphabet(enum.IntEnum):
        """
        These are commonly used subsets of the alphabet that the FFX mode
        natively supports. In the algorithm, the alphabet is selected using
        the "radix". Therefore each corresponds to particular radix.

        Attributes:
          FFX_COMMON_NATIVE_ALPHABET_UNSPECIFIED (int): Unused.
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


class CustomInfoType(object):
    class ExclusionType(enum.IntEnum):
        """
        Attributes:
          EXCLUSION_TYPE_UNSPECIFIED (int): A finding of this custom info type will not be excluded from results.
          EXCLUSION_TYPE_EXCLUDE (int): A finding of this custom info type will be excluded from final results,
          but can still affect rule execution.
        """

        EXCLUSION_TYPE_UNSPECIFIED = 0
        EXCLUSION_TYPE_EXCLUDE = 1


class DlpJob(object):
    class JobState(enum.IntEnum):
        """
        Possible states of a job. New items may be added.

        Attributes:
          JOB_STATE_UNSPECIFIED (int): Unused.
          PENDING (int): The job has not yet started.
          RUNNING (int): The job is currently running. Once a job has finished it will transition
          to FAILED or DONE.
          DONE (int): The job is no longer running.
          CANCELED (int): The job was canceled before it could complete.
          FAILED (int): The job had an error and did not complete.
          ACTIVE (int): The job is currently accepting findings via hybridInspect.
          A hybrid job in ACTIVE state may continue to have findings added to it
          through calling of hybridInspect. After the job has finished no more
          calls to hybridInspect may be made. ACTIVE jobs can transition to DONE.
        """

        JOB_STATE_UNSPECIFIED = 0
        PENDING = 1
        RUNNING = 2
        DONE = 3
        CANCELED = 4
        FAILED = 5
        ACTIVE = 6


class JobTrigger(object):
    class Status(enum.IntEnum):
        """
        Whether the trigger is currently active. If PAUSED or CANCELLED, no jobs
        will be created with this configuration. The service may automatically
        pause triggers experiencing frequent errors. To restart a job, set the
        status to HEALTHY after correcting user errors.

        Attributes:
          STATUS_UNSPECIFIED (int): Unused.
          HEALTHY (int): Trigger is healthy.
          PAUSED (int): Trigger is temporarily paused.
          CANCELLED (int): Trigger is cancelled and can not be resumed.
        """

        STATUS_UNSPECIFIED = 0
        HEALTHY = 1
        PAUSED = 2
        CANCELLED = 3


class OutputStorageConfig(object):
    class OutputSchema(enum.IntEnum):
        """
        Predefined schemas for storing findings.
        Only for use with external storage.

        Attributes:
          OUTPUT_SCHEMA_UNSPECIFIED (int): Unused.
          BASIC_COLUMNS (int): Basic schema including only ``info_type``, ``quote``, ``certainty``,
          and ``timestamp``.
          GCS_COLUMNS (int): Schema tailored to findings from scanning Google Cloud Storage.
          DATASTORE_COLUMNS (int): Schema tailored to findings from scanning Google Datastore.
          BIG_QUERY_COLUMNS (int): Schema tailored to findings from scanning Google BigQuery.
          ALL_COLUMNS (int): Schema containing all columns.
        """

        OUTPUT_SCHEMA_UNSPECIFIED = 0
        BASIC_COLUMNS = 1
        GCS_COLUMNS = 2
        DATASTORE_COLUMNS = 3
        BIG_QUERY_COLUMNS = 4
        ALL_COLUMNS = 5


class RecordCondition(object):
    class Expressions(object):
        class LogicalOperator(enum.IntEnum):
            """
            Logical operators for conditional checks.

            Attributes:
              LOGICAL_OPERATOR_UNSPECIFIED (int): Unused
              AND (int): Conditional AND
            """

            LOGICAL_OPERATOR_UNSPECIFIED = 0
            AND = 1


class TimePartConfig(object):
    class TimePart(enum.IntEnum):
        """
        Components that make up time.

        Attributes:
          TIME_PART_UNSPECIFIED (int): Unused
          YEAR (int): [0-9999]
          MONTH (int): [1-12]
          DAY_OF_MONTH (int): [1-31]
          DAY_OF_WEEK (int): [1-7]
          WEEK_OF_YEAR (int): [1-53]
          HOUR_OF_DAY (int): [0-23]
        """

        TIME_PART_UNSPECIFIED = 0
        YEAR = 1
        MONTH = 2
        DAY_OF_MONTH = 3
        DAY_OF_WEEK = 4
        WEEK_OF_YEAR = 5
        HOUR_OF_DAY = 6


class TransformationSummary(object):
    class TransformationResultCode(enum.IntEnum):
        """
        Possible outcomes of transformations.

        Attributes:
          TRANSFORMATION_RESULT_CODE_UNSPECIFIED (int): Unused
          SUCCESS (int): Transformation completed without an error.
          ERROR (int): Transformation had an error.
        """

        TRANSFORMATION_RESULT_CODE_UNSPECIFIED = 0
        SUCCESS = 1
        ERROR = 2
