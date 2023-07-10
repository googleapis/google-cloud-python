# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from __future__ import annotations

from typing import MutableMapping, MutableSequence

import proto  # type: ignore

from google.cloud.dataplex_v1.types import processing

__protobuf__ = proto.module(
    package="google.cloud.dataplex.v1",
    manifest={
        "DataQualitySpec",
        "DataQualityResult",
        "DataQualityRuleResult",
        "DataQualityDimensionResult",
        "DataQualityRule",
    },
)


class DataQualitySpec(proto.Message):
    r"""DataQualityScan related setting.

    Attributes:
        rules (MutableSequence[google.cloud.dataplex_v1.types.DataQualityRule]):
            The list of rules to evaluate against a data
            source. At least one rule is required.
    """

    rules: MutableSequence["DataQualityRule"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="DataQualityRule",
    )


class DataQualityResult(proto.Message):
    r"""The output of a DataQualityScan.

    Attributes:
        passed (bool):
            Overall data quality result -- ``true`` if all rules passed.
        dimensions (MutableSequence[google.cloud.dataplex_v1.types.DataQualityDimensionResult]):
            A list of results at the dimension level.
        rules (MutableSequence[google.cloud.dataplex_v1.types.DataQualityRuleResult]):
            A list of all the rules in a job, and their
            results.
        row_count (int):
            The count of rows processed.
        scanned_data (google.cloud.dataplex_v1.types.ScannedData):
            The data scanned for this result.
    """

    passed: bool = proto.Field(
        proto.BOOL,
        number=5,
    )
    dimensions: MutableSequence["DataQualityDimensionResult"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="DataQualityDimensionResult",
    )
    rules: MutableSequence["DataQualityRuleResult"] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message="DataQualityRuleResult",
    )
    row_count: int = proto.Field(
        proto.INT64,
        number=4,
    )
    scanned_data: processing.ScannedData = proto.Field(
        proto.MESSAGE,
        number=7,
        message=processing.ScannedData,
    )


class DataQualityRuleResult(proto.Message):
    r"""DataQualityRuleResult provides a more detailed, per-rule view
    of the results.

    Attributes:
        rule (google.cloud.dataplex_v1.types.DataQualityRule):
            The rule specified in the DataQualitySpec, as
            is.
        passed (bool):
            Whether the rule passed or failed.
        evaluated_count (int):
            The number of rows a rule was evaluated against. This field
            is only valid for ColumnMap type rules.

            Evaluated count can be configured to either

            -  include all rows (default) - with ``null`` rows
               automatically failing rule evaluation, or
            -  exclude ``null`` rows from the ``evaluated_count``, by
               setting ``ignore_nulls = true``.
        passed_count (int):
            The number of rows which passed a rule
            evaluation. This field is only valid for
            ColumnMap type rules.
        null_count (int):
            The number of rows with null values in the
            specified column.
        pass_ratio (float):
            The ratio of **passed_count / evaluated_count**. This field
            is only valid for ColumnMap type rules.
        failing_rows_query (str):
            The query to find rows that did not pass this
            rule. Only applies to ColumnMap and RowCondition
            rules.
    """

    rule: "DataQualityRule" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="DataQualityRule",
    )
    passed: bool = proto.Field(
        proto.BOOL,
        number=7,
    )
    evaluated_count: int = proto.Field(
        proto.INT64,
        number=9,
    )
    passed_count: int = proto.Field(
        proto.INT64,
        number=8,
    )
    null_count: int = proto.Field(
        proto.INT64,
        number=5,
    )
    pass_ratio: float = proto.Field(
        proto.DOUBLE,
        number=6,
    )
    failing_rows_query: str = proto.Field(
        proto.STRING,
        number=10,
    )


class DataQualityDimensionResult(proto.Message):
    r"""DataQualityDimensionResult provides a more detailed,
    per-dimension view of the results.

    Attributes:
        passed (bool):
            Whether the dimension passed or failed.
    """

    passed: bool = proto.Field(
        proto.BOOL,
        number=3,
    )


class DataQualityRule(proto.Message):
    r"""A rule captures data quality intent about a data source.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        range_expectation (google.cloud.dataplex_v1.types.DataQualityRule.RangeExpectation):
            ColumnMap rule which evaluates whether each
            column value lies between a specified range.

            This field is a member of `oneof`_ ``rule_type``.
        non_null_expectation (google.cloud.dataplex_v1.types.DataQualityRule.NonNullExpectation):
            ColumnMap rule which evaluates whether each
            column value is null.

            This field is a member of `oneof`_ ``rule_type``.
        set_expectation (google.cloud.dataplex_v1.types.DataQualityRule.SetExpectation):
            ColumnMap rule which evaluates whether each
            column value is contained by a specified set.

            This field is a member of `oneof`_ ``rule_type``.
        regex_expectation (google.cloud.dataplex_v1.types.DataQualityRule.RegexExpectation):
            ColumnMap rule which evaluates whether each
            column value matches a specified regex.

            This field is a member of `oneof`_ ``rule_type``.
        uniqueness_expectation (google.cloud.dataplex_v1.types.DataQualityRule.UniquenessExpectation):
            ColumnAggregate rule which evaluates whether
            the column has duplicates.

            This field is a member of `oneof`_ ``rule_type``.
        statistic_range_expectation (google.cloud.dataplex_v1.types.DataQualityRule.StatisticRangeExpectation):
            ColumnAggregate rule which evaluates whether
            the column aggregate statistic lies between a
            specified range.

            This field is a member of `oneof`_ ``rule_type``.
        row_condition_expectation (google.cloud.dataplex_v1.types.DataQualityRule.RowConditionExpectation):
            Table rule which evaluates whether each row
            passes the specified condition.

            This field is a member of `oneof`_ ``rule_type``.
        table_condition_expectation (google.cloud.dataplex_v1.types.DataQualityRule.TableConditionExpectation):
            Table rule which evaluates whether the
            provided expression is true.

            This field is a member of `oneof`_ ``rule_type``.
        column (str):
            Optional. The unnested column which this rule
            is evaluated against.
        ignore_null (bool):
            Optional. Rows with ``null`` values will automatically fail
            a rule, unless ``ignore_null`` is ``true``. In that case,
            such ``null`` rows are trivially considered passing.

            Only applicable to ColumnMap rules.
        dimension (str):
            Required. The dimension a rule belongs to. Results are also
            aggregated at the dimension level. Supported dimensions are
            **["COMPLETENESS", "ACCURACY", "CONSISTENCY", "VALIDITY",
            "UNIQUENESS", "INTEGRITY"]**
        threshold (float):
            Optional. The minimum ratio of **passing_rows / total_rows**
            required to pass this rule, with a range of [0.0, 1.0].

            0 indicates default value (i.e. 1.0).
    """

    class RangeExpectation(proto.Message):
        r"""Evaluates whether each column value lies between a specified
        range.

        Attributes:
            min_value (str):
                Optional. The minimum column value allowed for a row to pass
                this validation. At least one of ``min_value`` and
                ``max_value`` need to be provided.
            max_value (str):
                Optional. The maximum column value allowed for a row to pass
                this validation. At least one of ``min_value`` and
                ``max_value`` need to be provided.
            strict_min_enabled (bool):
                Optional. Whether each value needs to be strictly greater
                than ('>') the minimum, or if equality is allowed.

                Only relevant if a ``min_value`` has been defined. Default =
                false.
            strict_max_enabled (bool):
                Optional. Whether each value needs to be strictly lesser
                than ('<') the maximum, or if equality is allowed.

                Only relevant if a ``max_value`` has been defined. Default =
                false.
        """

        min_value: str = proto.Field(
            proto.STRING,
            number=1,
        )
        max_value: str = proto.Field(
            proto.STRING,
            number=2,
        )
        strict_min_enabled: bool = proto.Field(
            proto.BOOL,
            number=3,
        )
        strict_max_enabled: bool = proto.Field(
            proto.BOOL,
            number=4,
        )

    class NonNullExpectation(proto.Message):
        r"""Evaluates whether each column value is null."""

    class SetExpectation(proto.Message):
        r"""Evaluates whether each column value is contained by a
        specified set.

        Attributes:
            values (MutableSequence[str]):
                Expected values for the column value.
        """

        values: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=1,
        )

    class RegexExpectation(proto.Message):
        r"""Evaluates whether each column value matches a specified
        regex.

        Attributes:
            regex (str):
                A regular expression the column value is
                expected to match.
        """

        regex: str = proto.Field(
            proto.STRING,
            number=1,
        )

    class UniquenessExpectation(proto.Message):
        r"""Evaluates whether the column has duplicates."""

    class StatisticRangeExpectation(proto.Message):
        r"""Evaluates whether the column aggregate statistic lies between
        a specified range.

        Attributes:
            statistic (google.cloud.dataplex_v1.types.DataQualityRule.StatisticRangeExpectation.ColumnStatistic):
                The aggregate metric to evaluate.
            min_value (str):
                The minimum column statistic value allowed for a row to pass
                this validation.

                At least one of ``min_value`` and ``max_value`` need to be
                provided.
            max_value (str):
                The maximum column statistic value allowed for a row to pass
                this validation.

                At least one of ``min_value`` and ``max_value`` need to be
                provided.
            strict_min_enabled (bool):
                Whether column statistic needs to be strictly greater than
                ('>') the minimum, or if equality is allowed.

                Only relevant if a ``min_value`` has been defined. Default =
                false.
            strict_max_enabled (bool):
                Whether column statistic needs to be strictly lesser than
                ('<') the maximum, or if equality is allowed.

                Only relevant if a ``max_value`` has been defined. Default =
                false.
        """

        class ColumnStatistic(proto.Enum):
            r"""The list of aggregate metrics a rule can be evaluated
            against.

            Values:
                STATISTIC_UNDEFINED (0):
                    Unspecified statistic type
                MEAN (1):
                    Evaluate the column mean
                MIN (2):
                    Evaluate the column min
                MAX (3):
                    Evaluate the column max
            """
            STATISTIC_UNDEFINED = 0
            MEAN = 1
            MIN = 2
            MAX = 3

        statistic: "DataQualityRule.StatisticRangeExpectation.ColumnStatistic" = (
            proto.Field(
                proto.ENUM,
                number=1,
                enum="DataQualityRule.StatisticRangeExpectation.ColumnStatistic",
            )
        )
        min_value: str = proto.Field(
            proto.STRING,
            number=2,
        )
        max_value: str = proto.Field(
            proto.STRING,
            number=3,
        )
        strict_min_enabled: bool = proto.Field(
            proto.BOOL,
            number=4,
        )
        strict_max_enabled: bool = proto.Field(
            proto.BOOL,
            number=5,
        )

    class RowConditionExpectation(proto.Message):
        r"""Evaluates whether each row passes the specified condition.
        The SQL expression needs to use BigQuery standard SQL syntax and
        should produce a boolean value per row as the result.

        Example: col1 >= 0 AND col2 < 10

        Attributes:
            sql_expression (str):
                The SQL expression.
        """

        sql_expression: str = proto.Field(
            proto.STRING,
            number=1,
        )

    class TableConditionExpectation(proto.Message):
        r"""Evaluates whether the provided expression is true.
        The SQL expression needs to use BigQuery standard SQL syntax and
        should produce a scalar boolean result.

        Example: MIN(col1) >= 0

        Attributes:
            sql_expression (str):
                The SQL expression.
        """

        sql_expression: str = proto.Field(
            proto.STRING,
            number=1,
        )

    range_expectation: RangeExpectation = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="rule_type",
        message=RangeExpectation,
    )
    non_null_expectation: NonNullExpectation = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="rule_type",
        message=NonNullExpectation,
    )
    set_expectation: SetExpectation = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="rule_type",
        message=SetExpectation,
    )
    regex_expectation: RegexExpectation = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="rule_type",
        message=RegexExpectation,
    )
    uniqueness_expectation: UniquenessExpectation = proto.Field(
        proto.MESSAGE,
        number=100,
        oneof="rule_type",
        message=UniquenessExpectation,
    )
    statistic_range_expectation: StatisticRangeExpectation = proto.Field(
        proto.MESSAGE,
        number=101,
        oneof="rule_type",
        message=StatisticRangeExpectation,
    )
    row_condition_expectation: RowConditionExpectation = proto.Field(
        proto.MESSAGE,
        number=200,
        oneof="rule_type",
        message=RowConditionExpectation,
    )
    table_condition_expectation: TableConditionExpectation = proto.Field(
        proto.MESSAGE,
        number=201,
        oneof="rule_type",
        message=TableConditionExpectation,
    )
    column: str = proto.Field(
        proto.STRING,
        number=500,
    )
    ignore_null: bool = proto.Field(
        proto.BOOL,
        number=501,
    )
    dimension: str = proto.Field(
        proto.STRING,
        number=502,
    )
    threshold: float = proto.Field(
        proto.DOUBLE,
        number=503,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
