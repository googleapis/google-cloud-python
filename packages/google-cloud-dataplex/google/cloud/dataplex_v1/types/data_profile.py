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
        "DataProfileSpec",
        "DataProfileResult",
    },
)


class DataProfileSpec(proto.Message):
    r"""DataProfileScan related setting."""


class DataProfileResult(proto.Message):
    r"""DataProfileResult defines the output of DataProfileScan. Each
    field of the table will have field type specific profile result.

    Attributes:
        row_count (int):
            The count of rows scanned.
        profile (google.cloud.dataplex_v1.types.DataProfileResult.Profile):
            The profile information per field.
        scanned_data (google.cloud.dataplex_v1.types.ScannedData):
            The data scanned for this result.
    """

    class Profile(proto.Message):
        r"""Contains name, type, mode and field type specific profile
        information.

        Attributes:
            fields (MutableSequence[google.cloud.dataplex_v1.types.DataProfileResult.Profile.Field]):
                List of fields with structural and profile
                information for each field.
        """

        class Field(proto.Message):
            r"""A field within a table.

            Attributes:
                name (str):
                    The name of the field.
                type_ (str):
                    The data type retrieved from the schema of the data source.
                    For instance, for a BigQuery native table, it is the
                    `BigQuery Table
                    Schema <https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#tablefieldschema>`__.
                    For a Dataplex Entity, it is the `Entity
                    Schema <https://cloud.google.com/dataplex/docs/reference/rpc/google.cloud.dataplex.v1#type_3>`__.
                mode (str):
                    The mode of the field. Possible values include:

                    -  REQUIRED, if it is a required field.
                    -  NULLABLE, if it is an optional field.
                    -  REPEATED, if it is a repeated field.
                profile (google.cloud.dataplex_v1.types.DataProfileResult.Profile.Field.ProfileInfo):
                    Profile information for the corresponding
                    field.
            """

            class ProfileInfo(proto.Message):
                r"""The profile information for each field type.

                This message has `oneof`_ fields (mutually exclusive fields).
                For each oneof, at most one member field can be set at the same time.
                Setting any member of the oneof automatically clears all other
                members.

                .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

                Attributes:
                    null_ratio (float):
                        Ratio of rows with null value against total
                        scanned rows.
                    distinct_ratio (float):
                        Ratio of rows with distinct values against
                        total scanned rows. Not available for complex
                        non-groupable field type RECORD and fields with
                        REPEATABLE mode.
                    top_n_values (MutableSequence[google.cloud.dataplex_v1.types.DataProfileResult.Profile.Field.ProfileInfo.TopNValue]):
                        The list of top N non-null values and number
                        of times they occur in the scanned data. N is 10
                        or equal to the number of distinct values in the
                        field, whichever is smaller. Not available for
                        complex non-groupable field type RECORD and
                        fields with REPEATABLE mode.
                    string_profile (google.cloud.dataplex_v1.types.DataProfileResult.Profile.Field.ProfileInfo.StringFieldInfo):
                        String type field information.

                        This field is a member of `oneof`_ ``field_info``.
                    integer_profile (google.cloud.dataplex_v1.types.DataProfileResult.Profile.Field.ProfileInfo.IntegerFieldInfo):
                        Integer type field information.

                        This field is a member of `oneof`_ ``field_info``.
                    double_profile (google.cloud.dataplex_v1.types.DataProfileResult.Profile.Field.ProfileInfo.DoubleFieldInfo):
                        Double type field information.

                        This field is a member of `oneof`_ ``field_info``.
                """

                class StringFieldInfo(proto.Message):
                    r"""The profile information for a string type field.

                    Attributes:
                        min_length (int):
                            Minimum length of non-null values in the
                            scanned data.
                        max_length (int):
                            Maximum length of non-null values in the
                            scanned data.
                        average_length (float):
                            Average length of non-null values in the
                            scanned data.
                    """

                    min_length: int = proto.Field(
                        proto.INT64,
                        number=1,
                    )
                    max_length: int = proto.Field(
                        proto.INT64,
                        number=2,
                    )
                    average_length: float = proto.Field(
                        proto.DOUBLE,
                        number=3,
                    )

                class IntegerFieldInfo(proto.Message):
                    r"""The profile information for an integer type field.

                    Attributes:
                        average (float):
                            Average of non-null values in the scanned
                            data. NaN, if the field has a NaN.
                        standard_deviation (float):
                            Standard deviation of non-null values in the
                            scanned data. NaN, if the field has a NaN.
                        min_ (int):
                            Minimum of non-null values in the scanned
                            data. NaN, if the field has a NaN.
                        quartiles (MutableSequence[int]):
                            A quartile divides the number of data points
                            into four parts, or quarters, of more-or-less
                            equal size. Three main quartiles used are: The
                            first quartile (Q1) splits off the lowest 25% of
                            data from the highest 75%. It is also known as
                            the lower or 25th empirical quartile, as 25% of
                            the data is below this point. The second
                            quartile (Q2) is the median of a data set. So,
                            50% of the data lies below this point. The third
                            quartile (Q3) splits off the highest 25% of data
                            from the lowest 75%. It is known as the upper or
                            75th empirical quartile, as 75% of the data lies
                            below this point. Here, the quartiles is
                            provided as an ordered list of quartile values
                            for the scanned data, occurring in order Q1,
                            median, Q3.
                        max_ (int):
                            Maximum of non-null values in the scanned
                            data. NaN, if the field has a NaN.
                    """

                    average: float = proto.Field(
                        proto.DOUBLE,
                        number=1,
                    )
                    standard_deviation: float = proto.Field(
                        proto.DOUBLE,
                        number=3,
                    )
                    min_: int = proto.Field(
                        proto.INT64,
                        number=4,
                    )
                    quartiles: MutableSequence[int] = proto.RepeatedField(
                        proto.INT64,
                        number=6,
                    )
                    max_: int = proto.Field(
                        proto.INT64,
                        number=5,
                    )

                class DoubleFieldInfo(proto.Message):
                    r"""The profile information for a double type field.

                    Attributes:
                        average (float):
                            Average of non-null values in the scanned
                            data. NaN, if the field has a NaN.
                        standard_deviation (float):
                            Standard deviation of non-null values in the
                            scanned data. NaN, if the field has a NaN.
                        min_ (float):
                            Minimum of non-null values in the scanned
                            data. NaN, if the field has a NaN.
                        quartiles (MutableSequence[float]):
                            A quartile divides the number of data points
                            into four parts, or quarters, of more-or-less
                            equal size. Three main quartiles used are: The
                            first quartile (Q1) splits off the lowest 25% of
                            data from the highest 75%. It is also known as
                            the lower or 25th empirical quartile, as 25% of
                            the data is below this point. The second
                            quartile (Q2) is the median of a data set. So,
                            50% of the data lies below this point. The third
                            quartile (Q3) splits off the highest 25% of data
                            from the lowest 75%. It is known as the upper or
                            75th empirical quartile, as 75% of the data lies
                            below this point. Here, the quartiles is
                            provided as an ordered list of quartile values
                            for the scanned data, occurring in order Q1,
                            median, Q3.
                        max_ (float):
                            Maximum of non-null values in the scanned
                            data. NaN, if the field has a NaN.
                    """

                    average: float = proto.Field(
                        proto.DOUBLE,
                        number=1,
                    )
                    standard_deviation: float = proto.Field(
                        proto.DOUBLE,
                        number=3,
                    )
                    min_: float = proto.Field(
                        proto.DOUBLE,
                        number=4,
                    )
                    quartiles: MutableSequence[float] = proto.RepeatedField(
                        proto.DOUBLE,
                        number=6,
                    )
                    max_: float = proto.Field(
                        proto.DOUBLE,
                        number=5,
                    )

                class TopNValue(proto.Message):
                    r"""Top N non-null values in the scanned data.

                    Attributes:
                        value (str):
                            String value of a top N non-null value.
                        count (int):
                            Count of the corresponding value in the
                            scanned data.
                    """

                    value: str = proto.Field(
                        proto.STRING,
                        number=1,
                    )
                    count: int = proto.Field(
                        proto.INT64,
                        number=2,
                    )

                null_ratio: float = proto.Field(
                    proto.DOUBLE,
                    number=2,
                )
                distinct_ratio: float = proto.Field(
                    proto.DOUBLE,
                    number=3,
                )
                top_n_values: MutableSequence[
                    "DataProfileResult.Profile.Field.ProfileInfo.TopNValue"
                ] = proto.RepeatedField(
                    proto.MESSAGE,
                    number=4,
                    message="DataProfileResult.Profile.Field.ProfileInfo.TopNValue",
                )
                string_profile: "DataProfileResult.Profile.Field.ProfileInfo.StringFieldInfo" = proto.Field(
                    proto.MESSAGE,
                    number=101,
                    oneof="field_info",
                    message="DataProfileResult.Profile.Field.ProfileInfo.StringFieldInfo",
                )
                integer_profile: "DataProfileResult.Profile.Field.ProfileInfo.IntegerFieldInfo" = proto.Field(
                    proto.MESSAGE,
                    number=102,
                    oneof="field_info",
                    message="DataProfileResult.Profile.Field.ProfileInfo.IntegerFieldInfo",
                )
                double_profile: "DataProfileResult.Profile.Field.ProfileInfo.DoubleFieldInfo" = proto.Field(
                    proto.MESSAGE,
                    number=103,
                    oneof="field_info",
                    message="DataProfileResult.Profile.Field.ProfileInfo.DoubleFieldInfo",
                )

            name: str = proto.Field(
                proto.STRING,
                number=1,
            )
            type_: str = proto.Field(
                proto.STRING,
                number=2,
            )
            mode: str = proto.Field(
                proto.STRING,
                number=3,
            )
            profile: "DataProfileResult.Profile.Field.ProfileInfo" = proto.Field(
                proto.MESSAGE,
                number=4,
                message="DataProfileResult.Profile.Field.ProfileInfo",
            )

        fields: MutableSequence[
            "DataProfileResult.Profile.Field"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message="DataProfileResult.Profile.Field",
        )

    row_count: int = proto.Field(
        proto.INT64,
        number=3,
    )
    profile: Profile = proto.Field(
        proto.MESSAGE,
        number=4,
        message=Profile,
    )
    scanned_data: processing.ScannedData = proto.Field(
        proto.MESSAGE,
        number=5,
        message=processing.ScannedData,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
