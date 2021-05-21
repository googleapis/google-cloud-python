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

from google.cloud.automl_v1.types import geometry
from google.cloud.automl_v1.types import io
from google.cloud.automl_v1.types import text_segment as gca_text_segment


__protobuf__ = proto.module(
    package="google.cloud.automl.v1",
    manifest={
        "Image",
        "TextSnippet",
        "DocumentDimensions",
        "Document",
        "ExamplePayload",
    },
)


class Image(proto.Message):
    r"""A representation of an image.
    Only images up to 30MB in size are supported.

    Attributes:
        image_bytes (bytes):
            Image content represented as a stream of bytes. Note: As
            with all ``bytes`` fields, protobuffers use a pure binary
            representation, whereas JSON representations use base64.
        thumbnail_uri (str):
            Output only. HTTP URI to the thumbnail image.
    """

    image_bytes = proto.Field(proto.BYTES, number=1, oneof="data",)
    thumbnail_uri = proto.Field(proto.STRING, number=4,)


class TextSnippet(proto.Message):
    r"""A representation of a text snippet.
    Attributes:
        content (str):
            Required. The content of the text snippet as
            a string. Up to 250000 characters long.
        mime_type (str):
            Optional. The format of
            [content][google.cloud.automl.v1.TextSnippet.content].
            Currently the only two allowed values are "text/html" and
            "text/plain". If left blank, the format is automatically
            determined from the type of the uploaded
            [content][google.cloud.automl.v1.TextSnippet.content].
        content_uri (str):
            Output only. HTTP URI where you can download
            the content.
    """

    content = proto.Field(proto.STRING, number=1,)
    mime_type = proto.Field(proto.STRING, number=2,)
    content_uri = proto.Field(proto.STRING, number=4,)


class DocumentDimensions(proto.Message):
    r"""Message that describes dimension of a document.
    Attributes:
        unit (google.cloud.automl_v1.types.DocumentDimensions.DocumentDimensionUnit):
            Unit of the dimension.
        width (float):
            Width value of the document, works together
            with the unit.
        height (float):
            Height value of the document, works together
            with the unit.
    """

    class DocumentDimensionUnit(proto.Enum):
        r"""Unit of the document dimension."""
        DOCUMENT_DIMENSION_UNIT_UNSPECIFIED = 0
        INCH = 1
        CENTIMETER = 2
        POINT = 3

    unit = proto.Field(proto.ENUM, number=1, enum=DocumentDimensionUnit,)
    width = proto.Field(proto.FLOAT, number=2,)
    height = proto.Field(proto.FLOAT, number=3,)


class Document(proto.Message):
    r"""A structured text document e.g. a PDF.
    Attributes:
        input_config (google.cloud.automl_v1.types.DocumentInputConfig):
            An input config specifying the content of the
            document.
        document_text (google.cloud.automl_v1.types.TextSnippet):
            The plain text version of this document.
        layout (Sequence[google.cloud.automl_v1.types.Document.Layout]):
            Describes the layout of the document. Sorted by
            [page_number][].
        document_dimensions (google.cloud.automl_v1.types.DocumentDimensions):
            The dimensions of the page in the document.
        page_count (int):
            Number of pages in the document.
    """

    class Layout(proto.Message):
        r"""Describes the layout information of a
        [text_segment][google.cloud.automl.v1.Document.Layout.text_segment]
        in the document.

        Attributes:
            text_segment (google.cloud.automl_v1.types.TextSegment):
                Text Segment that represents a segment in
                [document_text][google.cloud.automl.v1p1beta.Document.document_text].
            page_number (int):
                Page number of the
                [text_segment][google.cloud.automl.v1.Document.Layout.text_segment]
                in the original document, starts from 1.
            bounding_poly (google.cloud.automl_v1.types.BoundingPoly):
                The position of the
                [text_segment][google.cloud.automl.v1.Document.Layout.text_segment]
                in the page. Contains exactly 4

                [normalized_vertices][google.cloud.automl.v1p1beta.BoundingPoly.normalized_vertices]
                and they are connected by edges in the order provided, which
                will represent a rectangle parallel to the frame. The
                [NormalizedVertex-s][google.cloud.automl.v1p1beta.NormalizedVertex]
                are relative to the page. Coordinates are based on top-left
                as point (0,0).
            text_segment_type (google.cloud.automl_v1.types.Document.Layout.TextSegmentType):
                The type of the
                [text_segment][google.cloud.automl.v1.Document.Layout.text_segment]
                in document.
        """

        class TextSegmentType(proto.Enum):
            r"""The type of TextSegment in the context of the original
            document.
            """
            TEXT_SEGMENT_TYPE_UNSPECIFIED = 0
            TOKEN = 1
            PARAGRAPH = 2
            FORM_FIELD = 3
            FORM_FIELD_NAME = 4
            FORM_FIELD_CONTENTS = 5
            TABLE = 6
            TABLE_HEADER = 7
            TABLE_ROW = 8
            TABLE_CELL = 9

        text_segment = proto.Field(
            proto.MESSAGE, number=1, message=gca_text_segment.TextSegment,
        )
        page_number = proto.Field(proto.INT32, number=2,)
        bounding_poly = proto.Field(
            proto.MESSAGE, number=3, message=geometry.BoundingPoly,
        )
        text_segment_type = proto.Field(
            proto.ENUM, number=4, enum="Document.Layout.TextSegmentType",
        )

    input_config = proto.Field(proto.MESSAGE, number=1, message=io.DocumentInputConfig,)
    document_text = proto.Field(proto.MESSAGE, number=2, message="TextSnippet",)
    layout = proto.RepeatedField(proto.MESSAGE, number=3, message=Layout,)
    document_dimensions = proto.Field(
        proto.MESSAGE, number=4, message="DocumentDimensions",
    )
    page_count = proto.Field(proto.INT32, number=5,)


class ExamplePayload(proto.Message):
    r"""Example data used for training or prediction.
    Attributes:
        image (google.cloud.automl_v1.types.Image):
            Example image.
        text_snippet (google.cloud.automl_v1.types.TextSnippet):
            Example text.
        document (google.cloud.automl_v1.types.Document):
            Example document.
    """

    image = proto.Field(proto.MESSAGE, number=1, oneof="payload", message="Image",)
    text_snippet = proto.Field(
        proto.MESSAGE, number=2, oneof="payload", message="TextSnippet",
    )
    document = proto.Field(
        proto.MESSAGE, number=4, oneof="payload", message="Document",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
