# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
    r"""DataProfileResult defines the output of DataProfileScan.
    Each field of the table will have field type specific profile
    result.

    Attributes:
        row_count (int):
            The count of all rows in the sampled data.
            Return 0, if zero rows.
        profile (google.cloud.dataplex_v1.types.DataProfileResult.Profile):
            This represents the profile information per
            field.
        scanned_data (google.cloud.dataplex_v1.types.ScannedData):
            The data scanned for this profile.
    """

    class Profile(proto.Message):
        r"""Profile information describing the structure and layout of
        the data and contains the profile info.

        Attributes:
            fields (MutableSequence[google.cloud.dataplex_v1.types.DataProfileResult.Profile.Field]):
                The sequence of fields describing data in
                table entities.
        """

        class Field(proto.Message):
            r"""Represents a column field within a table schema.

            Attributes:
                name (str):
                    The name of the field.
                type_ (str):
                    The field data type. Possible values include:

                    -  STRING
                    -  BYTE
                    -  INT64
                    -  INT32
                    -  INT16
                    -  DOUBLE
                    -  FLOAT
                    -  DECIMAL
                    -  BOOLEAN
                    -  BINARY
                    -  TIMESTAMP
                    -  DATE
                    -  TIME
                    -  NULL
                    -  RECORD
                mode (str):
                    The mode of the field. Its value will be:
                    REQUIRED, if it is a required field.
                    NULLABLE, if it is an optional field.
                    REPEATED, if it is a repeated field.
                profile (google.cloud.dataplex_v1.types.DataProfileResult.Profile.Field.ProfileInfo):
                    The profile information for the corresponding
                    field.
            """

            class ProfileInfo(proto.Message):
                r"""ProfileInfo defines the profile information for each schema
                field type.

                This message has `oneof`_ fields (mutually exclusive fields).
                For each oneof, at most one member field can be set at the same time.
                Setting any member of the oneof automatically clears all other
                members.

                .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

                Attributes:
                    null_ratio (float):
                        The ratio of null rows against the rows in
                        the sampled data.
                    distinct_ratio (float):
                        The ratio of rows that are distinct against
                        the rows in the sampled data.
                    top_n_values (MutableSequence[google.cloud.dataplex_v1.types.DataProfileResult.Profile.Field.ProfileInfo.TopNValue]):
                        The array of top N values of the field in the
                        sampled data. Currently N is set as 10 or equal
                        to distinct values in the field, whichever is
                        smaller. This will be optional for complex
                        non-groupable data-types such as JSON, ARRAY,
                        JSON, STRUCT.
                    string_profile (google.cloud.dataplex_v1.types.DataProfileResult.Profile.Field.ProfileInfo.StringFieldInfo):
                        The corresponding string field profile.

                        This field is a member of `oneof`_ ``field_info``.
                    integer_profile (google.cloud.dataplex_v1.types.DataProfileResult.Profile.Field.ProfileInfo.IntegerFieldInfo):
                        The corresponding integer field profile.

                        This field is a member of `oneof`_ ``field_info``.
                    double_profile (google.cloud.dataplex_v1.types.DataProfileResult.Profile.Field.ProfileInfo.DoubleFieldInfo):
                        The corresponding double field profile.

                        This field is a member of `oneof`_ ``field_info``.
                """

                class StringFieldInfo(proto.Message):
                    r"""StringFieldInfo defines output info for any string type
                    field.

                    Attributes:
                        min_length (int):
                            The minimum length of the string field in the
                            sampled data. Optional if zero non-null rows.
                        max_length (int):
                            The maximum length of a string field in the
                            sampled data. Optional if zero non-null rows.
                        average_length (float):
                            The average length of a string field in the
                            sampled data. Optional if zero non-null rows.
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
                    r"""IntegerFieldInfo defines output for any integer type field.

                    Attributes:
                        average (float):
                            The average of non-null values of integer
                            field in the sampled data. Return NaN, if the
                            field has a NaN. Optional if zero non-null rows.
                        standard_deviation (float):
                            The standard deviation of non-null of integer
                            field in the sampled data. Return NaN, if the
                            field has a NaN. Optional if zero non-null rows.
                        min_ (int):
                            The minimum value of an integer field in the
                            sampled data. Return NaN, if the field has a
                            NaN. Optional if zero non-null rows.
                        quartiles (MutableSequence[int]):
                            A quartile divide the number of data points
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
                            below this point. So, here the quartiles is
                            provided as an ordered list of quartile values,
                            occurring in order Q1, median, Q3.
                        max_ (int):
                            The maximum value of an integer field in the
                            sampled data. Return NaN, if the field has a
                            NaN. Optional if zero non-null rows.
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
                    r"""DoubleFieldInfo defines output for any double type field.

                    Attributes:
                        average (float):
                            The average of non-null values of double
                            field in the sampled data. Return NaN, if the
                            field has a NaN. Optional if zero non-null rows.
                        standard_deviation (float):
                            The standard deviation of non-null of double
                            field in the sampled data. Return NaN, if the
                            field has a NaN. Optional if zero non-null rows.
                        min_ (float):
                            The minimum value of a double field in the
                            sampled data. Return NaN, if the field has a
                            NaN. Optional if zero non-null rows.
                        quartiles (MutableSequence[float]):
                            A quartile divide the numebr of data points
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
                            below this point. So, here the quartiles is
                            provided as an ordered list of quartile values,
                            occurring in order Q1, median, Q3.
                        max_ (float):
                            The maximum value of a double field in the
                            sampled data. Return NaN, if the field has a
                            NaN. Optional if zero non-null rows.
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
                    r"""The TopNValue defines the structure of output of top N values
                    of a field.

                    Attributes:
                        value (str):
                            The value is the string value of the actual
                            value from the field.
                        count (int):
                            The frequency count of the corresponding
                            value in the field.
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
