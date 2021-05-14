# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
import proto  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.dataqna.v1alpha", manifest={"AnnotatedString",},
)


class AnnotatedString(proto.Message):
    r"""Describes string annotation from both semantic and formatting
    perspectives. Example:

    User Query:

    top countries by population in Africa

    0 4 14 17 28 31 37

    Table Data:

    -  "country" - dimension
    -  "population" - metric
    -  "Africa" - value in the "continent" column

    text_formatted = ``"top countries by population in Africa"``

    html_formatted =
    ``"top <b>countries</b> by <b>population</b> in <i>Africa</i>"``

    ::

       markups = [
         {DIMENSION, 4, 12}, // 'countries'
         {METRIC, 17, 26}, // 'population'
         {FILTER, 31, 36}  // 'Africa'
       ]

    Note that html formattings for 'DIMENSION' and 'METRIC' are the
    same, while semantic markups are different.

    Attributes:
        text_formatted (str):
            Text version of the string.
        html_formatted (str):
            HTML version of the string annotation.
        markups (Sequence[google.cloud.dataqna_v1alpha.types.AnnotatedString.SemanticMarkup]):
            Semantic version of the string annotation.
    """

    class SemanticMarkupType(proto.Enum):
        r"""Semantic markup types."""
        MARKUP_TYPE_UNSPECIFIED = 0
        METRIC = 1
        DIMENSION = 2
        FILTER = 3
        UNUSED = 4
        BLOCKED = 5
        ROW = 6

    class SemanticMarkup(proto.Message):
        r"""Semantic markup denotes a substring (by index and length)
        with markup information.

        Attributes:
            type_ (google.cloud.dataqna_v1alpha.types.AnnotatedString.SemanticMarkupType):
                The semantic type of the markup substring.
            start_char_index (int):
                Unicode character index of the query.
            length (int):
                The length (number of unicode characters) of
                the markup substring.
        """

        type_ = proto.Field(
            proto.ENUM, number=1, enum="AnnotatedString.SemanticMarkupType",
        )
        start_char_index = proto.Field(proto.INT32, number=2,)
        length = proto.Field(proto.INT32, number=3,)

    text_formatted = proto.Field(proto.STRING, number=1,)
    html_formatted = proto.Field(proto.STRING, number=2,)
    markups = proto.RepeatedField(proto.MESSAGE, number=3, message=SemanticMarkup,)


__all__ = tuple(sorted(__protobuf__.manifest))
