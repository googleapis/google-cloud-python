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

from google.cloud.documentai_v1beta3.types import geometry
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
from google.type import color_pb2  # type: ignore
from google.type import date_pb2  # type: ignore
from google.type import datetime_pb2  # type: ignore
from google.type import money_pb2  # type: ignore
from google.type import postal_address_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.documentai.v1beta3", manifest={"Document",},
)


class Document(proto.Message):
    r"""Document represents the canonical document resource in
    Document Understanding AI.
    It is an interchange format that provides insights into
    documents and allows for collaboration between users and
    Document Understanding AI to iterate and optimize for quality.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        uri (str):
            Optional. Currently supports Google Cloud Storage URI of the
            form ``gs://bucket_name/object_name``. Object versioning is
            not supported. See `Google Cloud Storage Request
            URIs <https://cloud.google.com/storage/docs/reference-uris>`__
            for more info.

            This field is a member of `oneof`_ ``source``.
        content (bytes):
            Optional. Inline document content, represented as a stream
            of bytes. Note: As with all ``bytes`` fields, protobuffers
            use a pure binary representation, whereas JSON
            representations use base64.

            This field is a member of `oneof`_ ``source``.
        mime_type (str):
            An IANA published MIME type (also referred to
            as media type). For more information, see
            https://www.iana.org/assignments/media-
            types/media-types.xhtml.
        text (str):
            Optional. UTF-8 encoded text in reading order
            from the document.
        text_styles (Sequence[google.cloud.documentai_v1beta3.types.Document.Style]):
            Styles for the
            [Document.text][google.cloud.documentai.v1beta3.Document.text].
        pages (Sequence[google.cloud.documentai_v1beta3.types.Document.Page]):
            Visual page layout for the
            [Document][google.cloud.documentai.v1beta3.Document].
        entities (Sequence[google.cloud.documentai_v1beta3.types.Document.Entity]):
            A list of entities detected on
            [Document.text][google.cloud.documentai.v1beta3.Document.text].
            For document shards, entities in this list may cross shard
            boundaries.
        entity_relations (Sequence[google.cloud.documentai_v1beta3.types.Document.EntityRelation]):
            Relationship among
            [Document.entities][google.cloud.documentai.v1beta3.Document.entities].
        text_changes (Sequence[google.cloud.documentai_v1beta3.types.Document.TextChange]):
            A list of text corrections made to [Document.text]. This is
            usually used for annotating corrections to OCR mistakes.
            Text changes for a given revision may not overlap with each
            other.
        shard_info (google.cloud.documentai_v1beta3.types.Document.ShardInfo):
            Information about the sharding if this
            document is sharded part of a larger document.
            If the document is not sharded, this message is
            not specified.
        error (google.rpc.status_pb2.Status):
            Any error that occurred while processing this
            document.
        revisions (Sequence[google.cloud.documentai_v1beta3.types.Document.Revision]):
            Revision history of this document.
    """

    class ShardInfo(proto.Message):
        r"""For a large document, sharding may be performed to produce
        several document shards. Each document shard contains this field
        to detail which shard it is.

        Attributes:
            shard_index (int):
                The 0-based index of this shard.
            shard_count (int):
                Total number of shards.
            text_offset (int):
                The index of the first character in
                [Document.text][google.cloud.documentai.v1beta3.Document.text]
                in the overall document global text.
        """

        shard_index = proto.Field(proto.INT64, number=1,)
        shard_count = proto.Field(proto.INT64, number=2,)
        text_offset = proto.Field(proto.INT64, number=3,)

    class Style(proto.Message):
        r"""Annotation for common text style attributes. This adheres to
        CSS conventions as much as possible.

        Attributes:
            text_anchor (google.cloud.documentai_v1beta3.types.Document.TextAnchor):
                Text anchor indexing into the
                [Document.text][google.cloud.documentai.v1beta3.Document.text].
            color (google.type.color_pb2.Color):
                Text color.
            background_color (google.type.color_pb2.Color):
                Text background color.
            font_weight (str):
                Font weight. Possible values are normal, bold, bolder, and
                lighter. https://www.w3schools.com/cssref/pr_font_weight.asp
            text_style (str):
                Text style. Possible values are normal, italic, and oblique.
                https://www.w3schools.com/cssref/pr_font_font-style.asp
            text_decoration (str):
                Text decoration. Follows CSS standard.
                https://www.w3schools.com/cssref/pr_text_text-decoration.asp
            font_size (google.cloud.documentai_v1beta3.types.Document.Style.FontSize):
                Font size.
        """

        class FontSize(proto.Message):
            r"""Font size with unit.

            Attributes:
                size (float):
                    Font size for the text.
                unit (str):
                    Unit for the font size. Follows CSS naming
                    (in, px, pt, etc.).
            """

            size = proto.Field(proto.FLOAT, number=1,)
            unit = proto.Field(proto.STRING, number=2,)

        text_anchor = proto.Field(
            proto.MESSAGE, number=1, message="Document.TextAnchor",
        )
        color = proto.Field(proto.MESSAGE, number=2, message=color_pb2.Color,)
        background_color = proto.Field(
            proto.MESSAGE, number=3, message=color_pb2.Color,
        )
        font_weight = proto.Field(proto.STRING, number=4,)
        text_style = proto.Field(proto.STRING, number=5,)
        text_decoration = proto.Field(proto.STRING, number=6,)
        font_size = proto.Field(
            proto.MESSAGE, number=7, message="Document.Style.FontSize",
        )

    class Page(proto.Message):
        r"""A page in a [Document][google.cloud.documentai.v1beta3.Document].

        Attributes:
            page_number (int):
                1-based index for current
                [Page][google.cloud.documentai.v1beta3.Document.Page] in a
                parent [Document][google.cloud.documentai.v1beta3.Document].
                Useful when a page is taken out of a
                [Document][google.cloud.documentai.v1beta3.Document] for
                individual processing.
            image (google.cloud.documentai_v1beta3.types.Document.Page.Image):
                Rendered image for this page. This image is
                preprocessed to remove any skew, rotation, and
                distortions such that the annotation bounding
                boxes can be upright and axis-aligned.
            transforms (Sequence[google.cloud.documentai_v1beta3.types.Document.Page.Matrix]):
                Transformation matrices that were applied to the original
                document image to produce
                [Page.image][google.cloud.documentai.v1beta3.Document.Page.image].
            dimension (google.cloud.documentai_v1beta3.types.Document.Page.Dimension):
                Physical dimension of the page.
            layout (google.cloud.documentai_v1beta3.types.Document.Page.Layout):
                [Layout][google.cloud.documentai.v1beta3.Document.Page.Layout]
                for the page.
            detected_languages (Sequence[google.cloud.documentai_v1beta3.types.Document.Page.DetectedLanguage]):
                A list of detected languages together with
                confidence.
            blocks (Sequence[google.cloud.documentai_v1beta3.types.Document.Page.Block]):
                A list of visually detected text blocks on
                the page. A block has a set of lines (collected
                into paragraphs) that have a common line-spacing
                and orientation.
            paragraphs (Sequence[google.cloud.documentai_v1beta3.types.Document.Page.Paragraph]):
                A list of visually detected text paragraphs
                on the page. A collection of lines that a human
                would perceive as a paragraph.
            lines (Sequence[google.cloud.documentai_v1beta3.types.Document.Page.Line]):
                A list of visually detected text lines on the
                page. A collection of tokens that a human would
                perceive as a line.
            tokens (Sequence[google.cloud.documentai_v1beta3.types.Document.Page.Token]):
                A list of visually detected tokens on the
                page.
            visual_elements (Sequence[google.cloud.documentai_v1beta3.types.Document.Page.VisualElement]):
                A list of detected non-text visual elements
                e.g. checkbox, signature etc. on the page.
            tables (Sequence[google.cloud.documentai_v1beta3.types.Document.Page.Table]):
                A list of visually detected tables on the
                page.
            form_fields (Sequence[google.cloud.documentai_v1beta3.types.Document.Page.FormField]):
                A list of visually detected form fields on
                the page.
            provenance (google.cloud.documentai_v1beta3.types.Document.Provenance):
                The history of this page.
        """

        class Dimension(proto.Message):
            r"""Dimension for the page.

            Attributes:
                width (float):
                    Page width.
                height (float):
                    Page height.
                unit (str):
                    Dimension unit.
            """

            width = proto.Field(proto.FLOAT, number=1,)
            height = proto.Field(proto.FLOAT, number=2,)
            unit = proto.Field(proto.STRING, number=3,)

        class Image(proto.Message):
            r"""Rendered image contents for this page.

            Attributes:
                content (bytes):
                    Raw byte content of the image.
                mime_type (str):
                    Encoding mime type for the image.
                width (int):
                    Width of the image in pixels.
                height (int):
                    Height of the image in pixels.
            """

            content = proto.Field(proto.BYTES, number=1,)
            mime_type = proto.Field(proto.STRING, number=2,)
            width = proto.Field(proto.INT32, number=3,)
            height = proto.Field(proto.INT32, number=4,)

        class Matrix(proto.Message):
            r"""Representation for transformation matrix, intended to be
            compatible and used with OpenCV format for image manipulation.

            Attributes:
                rows (int):
                    Number of rows in the matrix.
                cols (int):
                    Number of columns in the matrix.
                type_ (int):
                    This encodes information about what data type the matrix
                    uses. For example, 0 (CV_8U) is an unsigned 8-bit image. For
                    the full list of OpenCV primitive data types, please refer
                    to
                    https://docs.opencv.org/4.3.0/d1/d1b/group__core__hal__interface.html
                data (bytes):
                    The matrix data.
            """

            rows = proto.Field(proto.INT32, number=1,)
            cols = proto.Field(proto.INT32, number=2,)
            type_ = proto.Field(proto.INT32, number=3,)
            data = proto.Field(proto.BYTES, number=4,)

        class Layout(proto.Message):
            r"""Visual element describing a layout unit on a page.

            Attributes:
                text_anchor (google.cloud.documentai_v1beta3.types.Document.TextAnchor):
                    Text anchor indexing into the
                    [Document.text][google.cloud.documentai.v1beta3.Document.text].
                confidence (float):
                    Confidence of the current
                    [Layout][google.cloud.documentai.v1beta3.Document.Page.Layout]
                    within context of the object this layout is for. e.g.
                    confidence can be for a single token, a table, a visual
                    element, etc. depending on context. Range [0, 1].
                bounding_poly (google.cloud.documentai_v1beta3.types.BoundingPoly):
                    The bounding polygon for the
                    [Layout][google.cloud.documentai.v1beta3.Document.Page.Layout].
                orientation (google.cloud.documentai_v1beta3.types.Document.Page.Layout.Orientation):
                    Detected orientation for the
                    [Layout][google.cloud.documentai.v1beta3.Document.Page.Layout].
            """

            class Orientation(proto.Enum):
                r"""Detected human reading orientation."""
                ORIENTATION_UNSPECIFIED = 0
                PAGE_UP = 1
                PAGE_RIGHT = 2
                PAGE_DOWN = 3
                PAGE_LEFT = 4

            text_anchor = proto.Field(
                proto.MESSAGE, number=1, message="Document.TextAnchor",
            )
            confidence = proto.Field(proto.FLOAT, number=2,)
            bounding_poly = proto.Field(
                proto.MESSAGE, number=3, message=geometry.BoundingPoly,
            )
            orientation = proto.Field(
                proto.ENUM, number=4, enum="Document.Page.Layout.Orientation",
            )

        class Block(proto.Message):
            r"""A block has a set of lines (collected into paragraphs) that
            have a common line-spacing and orientation.

            Attributes:
                layout (google.cloud.documentai_v1beta3.types.Document.Page.Layout):
                    [Layout][google.cloud.documentai.v1beta3.Document.Page.Layout]
                    for
                    [Block][google.cloud.documentai.v1beta3.Document.Page.Block].
                detected_languages (Sequence[google.cloud.documentai_v1beta3.types.Document.Page.DetectedLanguage]):
                    A list of detected languages together with
                    confidence.
                provenance (google.cloud.documentai_v1beta3.types.Document.Provenance):
                    The history of this annotation.
            """

            layout = proto.Field(
                proto.MESSAGE, number=1, message="Document.Page.Layout",
            )
            detected_languages = proto.RepeatedField(
                proto.MESSAGE, number=2, message="Document.Page.DetectedLanguage",
            )
            provenance = proto.Field(
                proto.MESSAGE, number=3, message="Document.Provenance",
            )

        class Paragraph(proto.Message):
            r"""A collection of lines that a human would perceive as a
            paragraph.

            Attributes:
                layout (google.cloud.documentai_v1beta3.types.Document.Page.Layout):
                    [Layout][google.cloud.documentai.v1beta3.Document.Page.Layout]
                    for
                    [Paragraph][google.cloud.documentai.v1beta3.Document.Page.Paragraph].
                detected_languages (Sequence[google.cloud.documentai_v1beta3.types.Document.Page.DetectedLanguage]):
                    A list of detected languages together with
                    confidence.
                provenance (google.cloud.documentai_v1beta3.types.Document.Provenance):
                    The  history of this annotation.
            """

            layout = proto.Field(
                proto.MESSAGE, number=1, message="Document.Page.Layout",
            )
            detected_languages = proto.RepeatedField(
                proto.MESSAGE, number=2, message="Document.Page.DetectedLanguage",
            )
            provenance = proto.Field(
                proto.MESSAGE, number=3, message="Document.Provenance",
            )

        class Line(proto.Message):
            r"""A collection of tokens that a human would perceive as a line.
            Does not cross column boundaries, can be horizontal, vertical,
            etc.

            Attributes:
                layout (google.cloud.documentai_v1beta3.types.Document.Page.Layout):
                    [Layout][google.cloud.documentai.v1beta3.Document.Page.Layout]
                    for
                    [Line][google.cloud.documentai.v1beta3.Document.Page.Line].
                detected_languages (Sequence[google.cloud.documentai_v1beta3.types.Document.Page.DetectedLanguage]):
                    A list of detected languages together with
                    confidence.
                provenance (google.cloud.documentai_v1beta3.types.Document.Provenance):
                    The  history of this annotation.
            """

            layout = proto.Field(
                proto.MESSAGE, number=1, message="Document.Page.Layout",
            )
            detected_languages = proto.RepeatedField(
                proto.MESSAGE, number=2, message="Document.Page.DetectedLanguage",
            )
            provenance = proto.Field(
                proto.MESSAGE, number=3, message="Document.Provenance",
            )

        class Token(proto.Message):
            r"""A detected token.

            Attributes:
                layout (google.cloud.documentai_v1beta3.types.Document.Page.Layout):
                    [Layout][google.cloud.documentai.v1beta3.Document.Page.Layout]
                    for
                    [Token][google.cloud.documentai.v1beta3.Document.Page.Token].
                detected_break (google.cloud.documentai_v1beta3.types.Document.Page.Token.DetectedBreak):
                    Detected break at the end of a
                    [Token][google.cloud.documentai.v1beta3.Document.Page.Token].
                detected_languages (Sequence[google.cloud.documentai_v1beta3.types.Document.Page.DetectedLanguage]):
                    A list of detected languages together with
                    confidence.
                provenance (google.cloud.documentai_v1beta3.types.Document.Provenance):
                    The  history of this annotation.
            """

            class DetectedBreak(proto.Message):
                r"""Detected break at the end of a
                [Token][google.cloud.documentai.v1beta3.Document.Page.Token].

                Attributes:
                    type_ (google.cloud.documentai_v1beta3.types.Document.Page.Token.DetectedBreak.Type):
                        Detected break type.
                """

                class Type(proto.Enum):
                    r"""Enum to denote the type of break found."""
                    TYPE_UNSPECIFIED = 0
                    SPACE = 1
                    WIDE_SPACE = 2
                    HYPHEN = 3

                type_ = proto.Field(
                    proto.ENUM, number=1, enum="Document.Page.Token.DetectedBreak.Type",
                )

            layout = proto.Field(
                proto.MESSAGE, number=1, message="Document.Page.Layout",
            )
            detected_break = proto.Field(
                proto.MESSAGE, number=2, message="Document.Page.Token.DetectedBreak",
            )
            detected_languages = proto.RepeatedField(
                proto.MESSAGE, number=3, message="Document.Page.DetectedLanguage",
            )
            provenance = proto.Field(
                proto.MESSAGE, number=4, message="Document.Provenance",
            )

        class VisualElement(proto.Message):
            r"""Detected non-text visual elements e.g. checkbox, signature
            etc. on the page.

            Attributes:
                layout (google.cloud.documentai_v1beta3.types.Document.Page.Layout):
                    [Layout][google.cloud.documentai.v1beta3.Document.Page.Layout]
                    for
                    [VisualElement][google.cloud.documentai.v1beta3.Document.Page.VisualElement].
                type_ (str):
                    Type of the
                    [VisualElement][google.cloud.documentai.v1beta3.Document.Page.VisualElement].
                detected_languages (Sequence[google.cloud.documentai_v1beta3.types.Document.Page.DetectedLanguage]):
                    A list of detected languages together with
                    confidence.
            """

            layout = proto.Field(
                proto.MESSAGE, number=1, message="Document.Page.Layout",
            )
            type_ = proto.Field(proto.STRING, number=2,)
            detected_languages = proto.RepeatedField(
                proto.MESSAGE, number=3, message="Document.Page.DetectedLanguage",
            )

        class Table(proto.Message):
            r"""A table representation similar to HTML table structure.

            Attributes:
                layout (google.cloud.documentai_v1beta3.types.Document.Page.Layout):
                    [Layout][google.cloud.documentai.v1beta3.Document.Page.Layout]
                    for
                    [Table][google.cloud.documentai.v1beta3.Document.Page.Table].
                header_rows (Sequence[google.cloud.documentai_v1beta3.types.Document.Page.Table.TableRow]):
                    Header rows of the table.
                body_rows (Sequence[google.cloud.documentai_v1beta3.types.Document.Page.Table.TableRow]):
                    Body rows of the table.
                detected_languages (Sequence[google.cloud.documentai_v1beta3.types.Document.Page.DetectedLanguage]):
                    A list of detected languages together with
                    confidence.
            """

            class TableRow(proto.Message):
                r"""A row of table cells.

                Attributes:
                    cells (Sequence[google.cloud.documentai_v1beta3.types.Document.Page.Table.TableCell]):
                        Cells that make up this row.
                """

                cells = proto.RepeatedField(
                    proto.MESSAGE, number=1, message="Document.Page.Table.TableCell",
                )

            class TableCell(proto.Message):
                r"""A cell representation inside the table.

                Attributes:
                    layout (google.cloud.documentai_v1beta3.types.Document.Page.Layout):
                        [Layout][google.cloud.documentai.v1beta3.Document.Page.Layout]
                        for
                        [TableCell][google.cloud.documentai.v1beta3.Document.Page.Table.TableCell].
                    row_span (int):
                        How many rows this cell spans.
                    col_span (int):
                        How many columns this cell spans.
                    detected_languages (Sequence[google.cloud.documentai_v1beta3.types.Document.Page.DetectedLanguage]):
                        A list of detected languages together with
                        confidence.
                """

                layout = proto.Field(
                    proto.MESSAGE, number=1, message="Document.Page.Layout",
                )
                row_span = proto.Field(proto.INT32, number=2,)
                col_span = proto.Field(proto.INT32, number=3,)
                detected_languages = proto.RepeatedField(
                    proto.MESSAGE, number=4, message="Document.Page.DetectedLanguage",
                )

            layout = proto.Field(
                proto.MESSAGE, number=1, message="Document.Page.Layout",
            )
            header_rows = proto.RepeatedField(
                proto.MESSAGE, number=2, message="Document.Page.Table.TableRow",
            )
            body_rows = proto.RepeatedField(
                proto.MESSAGE, number=3, message="Document.Page.Table.TableRow",
            )
            detected_languages = proto.RepeatedField(
                proto.MESSAGE, number=4, message="Document.Page.DetectedLanguage",
            )

        class FormField(proto.Message):
            r"""A form field detected on the page.

            Attributes:
                field_name (google.cloud.documentai_v1beta3.types.Document.Page.Layout):
                    [Layout][google.cloud.documentai.v1beta3.Document.Page.Layout]
                    for the
                    [FormField][google.cloud.documentai.v1beta3.Document.Page.FormField]
                    name. e.g. ``Address``, ``Email``, ``Grand total``,
                    ``Phone number``, etc.
                field_value (google.cloud.documentai_v1beta3.types.Document.Page.Layout):
                    [Layout][google.cloud.documentai.v1beta3.Document.Page.Layout]
                    for the
                    [FormField][google.cloud.documentai.v1beta3.Document.Page.FormField]
                    value.
                name_detected_languages (Sequence[google.cloud.documentai_v1beta3.types.Document.Page.DetectedLanguage]):
                    A list of detected languages for name
                    together with confidence.
                value_detected_languages (Sequence[google.cloud.documentai_v1beta3.types.Document.Page.DetectedLanguage]):
                    A list of detected languages for value
                    together with confidence.
                value_type (str):
                    If the value is non-textual, this field represents the type.
                    Current valid values are:

                    -  blank (this indicates the field_value is normal text)
                    -  "unfilled_checkbox"
                    -  "filled_checkbox".
                provenance (google.cloud.documentai_v1beta3.types.Document.Provenance):
                    The history of this annotation.
            """

            field_name = proto.Field(
                proto.MESSAGE, number=1, message="Document.Page.Layout",
            )
            field_value = proto.Field(
                proto.MESSAGE, number=2, message="Document.Page.Layout",
            )
            name_detected_languages = proto.RepeatedField(
                proto.MESSAGE, number=3, message="Document.Page.DetectedLanguage",
            )
            value_detected_languages = proto.RepeatedField(
                proto.MESSAGE, number=4, message="Document.Page.DetectedLanguage",
            )
            value_type = proto.Field(proto.STRING, number=5,)
            provenance = proto.Field(
                proto.MESSAGE, number=8, message="Document.Provenance",
            )

        class DetectedLanguage(proto.Message):
            r"""Detected language for a structural component.

            Attributes:
                language_code (str):
                    The BCP-47 language code, such as "en-US" or "sr-Latn". For
                    more information, see
                    http://www.unicode.org/reports/tr35/#Unicode_locale_identifier.
                confidence (float):
                    Confidence of detected language. Range [0, 1].
            """

            language_code = proto.Field(proto.STRING, number=1,)
            confidence = proto.Field(proto.FLOAT, number=2,)

        page_number = proto.Field(proto.INT32, number=1,)
        image = proto.Field(proto.MESSAGE, number=13, message="Document.Page.Image",)
        transforms = proto.RepeatedField(
            proto.MESSAGE, number=14, message="Document.Page.Matrix",
        )
        dimension = proto.Field(
            proto.MESSAGE, number=2, message="Document.Page.Dimension",
        )
        layout = proto.Field(proto.MESSAGE, number=3, message="Document.Page.Layout",)
        detected_languages = proto.RepeatedField(
            proto.MESSAGE, number=4, message="Document.Page.DetectedLanguage",
        )
        blocks = proto.RepeatedField(
            proto.MESSAGE, number=5, message="Document.Page.Block",
        )
        paragraphs = proto.RepeatedField(
            proto.MESSAGE, number=6, message="Document.Page.Paragraph",
        )
        lines = proto.RepeatedField(
            proto.MESSAGE, number=7, message="Document.Page.Line",
        )
        tokens = proto.RepeatedField(
            proto.MESSAGE, number=8, message="Document.Page.Token",
        )
        visual_elements = proto.RepeatedField(
            proto.MESSAGE, number=9, message="Document.Page.VisualElement",
        )
        tables = proto.RepeatedField(
            proto.MESSAGE, number=10, message="Document.Page.Table",
        )
        form_fields = proto.RepeatedField(
            proto.MESSAGE, number=11, message="Document.Page.FormField",
        )
        provenance = proto.Field(
            proto.MESSAGE, number=16, message="Document.Provenance",
        )

    class Entity(proto.Message):
        r"""A phrase in the text that is a known entity type, such as a
        person, an organization, or location.

        Attributes:
            text_anchor (google.cloud.documentai_v1beta3.types.Document.TextAnchor):
                Optional. Provenance of the entity. Text anchor indexing
                into the
                [Document.text][google.cloud.documentai.v1beta3.Document.text].
            type_ (str):
                Entity type from a schema e.g. ``Address``.
            mention_text (str):
                Optional. Text value in the document e.g.
                ``1600 Amphitheatre Pkwy``.
            mention_id (str):
                Optional. Deprecated. Use ``id`` field instead.
            confidence (float):
                Optional. Confidence of detected Schema entity. Range [0,
                1].
            page_anchor (google.cloud.documentai_v1beta3.types.Document.PageAnchor):
                Optional. Represents the provenance of this
                entity wrt. the location on the page where it
                was found.
            id (str):
                Optional. Canonical id. This will be a unique
                value in the entity list for this document.
            normalized_value (google.cloud.documentai_v1beta3.types.Document.Entity.NormalizedValue):
                Optional. Normalized entity value. Absent if
                the extracted value could not be converted or
                the type (e.g. address) is not supported for
                certain parsers. This field is also only
                populated for certain supported document types.
            properties (Sequence[google.cloud.documentai_v1beta3.types.Document.Entity]):
                Optional. Entities can be nested to form a
                hierarchical data structure representing the
                content in the document.
            provenance (google.cloud.documentai_v1beta3.types.Document.Provenance):
                Optional. The history of this annotation.
            redacted (bool):
                Optional. Whether the entity will be redacted
                for de-identification purposes.
        """

        class NormalizedValue(proto.Message):
            r"""Parsed and normalized entity value.

            This message has `oneof`_ fields (mutually exclusive fields).
            For each oneof, at most one member field can be set at the same time.
            Setting any member of the oneof automatically clears all other
            members.

            .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

            Attributes:
                money_value (google.type.money_pb2.Money):
                    Money value. See also:
                    https://github.com/googleapis/googleapis/blob/master/google/type/money.proto

                    This field is a member of `oneof`_ ``structured_value``.
                date_value (google.type.date_pb2.Date):
                    Date value. Includes year, month, day. See
                    also:
                    https://github.com/googleapis/googleapis/blob/master/google/type/date.proto

                    This field is a member of `oneof`_ ``structured_value``.
                datetime_value (google.type.datetime_pb2.DateTime):
                    DateTime value. Includes date, time, and
                    timezone. See also:
                    https://github.com/googleapis/googleapis/blob/master/google/type/datetime.proto

                    This field is a member of `oneof`_ ``structured_value``.
                address_value (google.type.postal_address_pb2.PostalAddress):
                    Postal address. See also:
                    https://github.com/googleapis/googleapis/blob/master/google/type/postal_address.proto

                    This field is a member of `oneof`_ ``structured_value``.
                boolean_value (bool):
                    Boolean value. Can be used for entities with
                    binary values, or for checkboxes.

                    This field is a member of `oneof`_ ``structured_value``.
                text (str):
                    Required. Normalized entity value stored as a string. This
                    field is populated for supported document type (e.g.
                    Invoice). For some entity types, one of respective
                    'structured_value' fields may also be populated.

                    -  Money/Currency type (``money_value``) is in the ISO 4217
                       text format.
                    -  Date type (``date_value``) is in the ISO 8601 text
                       format.
                    -  Datetime type (``datetime_value``) is in the ISO 8601
                       text format.
            """

            money_value = proto.Field(
                proto.MESSAGE,
                number=2,
                oneof="structured_value",
                message=money_pb2.Money,
            )
            date_value = proto.Field(
                proto.MESSAGE,
                number=3,
                oneof="structured_value",
                message=date_pb2.Date,
            )
            datetime_value = proto.Field(
                proto.MESSAGE,
                number=4,
                oneof="structured_value",
                message=datetime_pb2.DateTime,
            )
            address_value = proto.Field(
                proto.MESSAGE,
                number=5,
                oneof="structured_value",
                message=postal_address_pb2.PostalAddress,
            )
            boolean_value = proto.Field(proto.BOOL, number=6, oneof="structured_value",)
            text = proto.Field(proto.STRING, number=1,)

        text_anchor = proto.Field(
            proto.MESSAGE, number=1, message="Document.TextAnchor",
        )
        type_ = proto.Field(proto.STRING, number=2,)
        mention_text = proto.Field(proto.STRING, number=3,)
        mention_id = proto.Field(proto.STRING, number=4,)
        confidence = proto.Field(proto.FLOAT, number=5,)
        page_anchor = proto.Field(
            proto.MESSAGE, number=6, message="Document.PageAnchor",
        )
        id = proto.Field(proto.STRING, number=7,)
        normalized_value = proto.Field(
            proto.MESSAGE, number=9, message="Document.Entity.NormalizedValue",
        )
        properties = proto.RepeatedField(
            proto.MESSAGE, number=10, message="Document.Entity",
        )
        provenance = proto.Field(
            proto.MESSAGE, number=11, message="Document.Provenance",
        )
        redacted = proto.Field(proto.BOOL, number=12,)

    class EntityRelation(proto.Message):
        r"""Relationship between
        [Entities][google.cloud.documentai.v1beta3.Document.Entity].

        Attributes:
            subject_id (str):
                Subject entity id.
            object_id (str):
                Object entity id.
            relation (str):
                Relationship description.
        """

        subject_id = proto.Field(proto.STRING, number=1,)
        object_id = proto.Field(proto.STRING, number=2,)
        relation = proto.Field(proto.STRING, number=3,)

    class TextAnchor(proto.Message):
        r"""Text reference indexing into the
        [Document.text][google.cloud.documentai.v1beta3.Document.text].

        Attributes:
            text_segments (Sequence[google.cloud.documentai_v1beta3.types.Document.TextAnchor.TextSegment]):
                The text segments from the
                [Document.text][google.cloud.documentai.v1beta3.Document.text].
            content (str):
                Contains the content of the text span so that users do not
                have to look it up in the text_segments.
        """

        class TextSegment(proto.Message):
            r"""A text segment in the
            [Document.text][google.cloud.documentai.v1beta3.Document.text]. The
            indices may be out of bounds which indicate that the text extends
            into another document shard for large sharded documents. See
            [ShardInfo.text_offset][google.cloud.documentai.v1beta3.Document.ShardInfo.text_offset]

            Attributes:
                start_index (int):
                    [TextSegment][google.cloud.documentai.v1beta3.Document.TextAnchor.TextSegment]
                    start UTF-8 char index in the
                    [Document.text][google.cloud.documentai.v1beta3.Document.text].
                end_index (int):
                    [TextSegment][google.cloud.documentai.v1beta3.Document.TextAnchor.TextSegment]
                    half open end UTF-8 char index in the
                    [Document.text][google.cloud.documentai.v1beta3.Document.text].
            """

            start_index = proto.Field(proto.INT64, number=1,)
            end_index = proto.Field(proto.INT64, number=2,)

        text_segments = proto.RepeatedField(
            proto.MESSAGE, number=1, message="Document.TextAnchor.TextSegment",
        )
        content = proto.Field(proto.STRING, number=2,)

    class PageAnchor(proto.Message):
        r"""Referencing the visual context of the entity in the
        [Document.pages][google.cloud.documentai.v1beta3.Document.pages].
        Page anchors can be cross-page, consist of multiple bounding
        polygons and optionally reference specific layout element types.

        Attributes:
            page_refs (Sequence[google.cloud.documentai_v1beta3.types.Document.PageAnchor.PageRef]):
                One or more references to visual page
                elements
        """

        class PageRef(proto.Message):
            r"""Represents a weak reference to a page element within a
            document.

            Attributes:
                page (int):
                    Required. Index into the
                    [Document.pages][google.cloud.documentai.v1beta3.Document.pages]
                    element, for example using [Document.pages][page_refs.page]
                    to locate the related page element. This field is skipped
                    when its value is the default 0. See
                    https://developers.google.com/protocol-buffers/docs/proto3#json.
                layout_type (google.cloud.documentai_v1beta3.types.Document.PageAnchor.PageRef.LayoutType):
                    Optional. The type of the layout element that
                    is being referenced if any.
                layout_id (str):
                    Optional. Deprecated. Use
                    [PageRef.bounding_poly][google.cloud.documentai.v1beta3.Document.PageAnchor.PageRef.bounding_poly]
                    instead.
                bounding_poly (google.cloud.documentai_v1beta3.types.BoundingPoly):
                    Optional. Identifies the bounding polygon of
                    a layout element on the page.
                confidence (float):
                    Optional. Confidence of detected page element, if
                    applicable. Range [0, 1].
            """

            class LayoutType(proto.Enum):
                r"""The type of layout that is being referenced."""
                LAYOUT_TYPE_UNSPECIFIED = 0
                BLOCK = 1
                PARAGRAPH = 2
                LINE = 3
                TOKEN = 4
                VISUAL_ELEMENT = 5
                TABLE = 6
                FORM_FIELD = 7

            page = proto.Field(proto.INT64, number=1,)
            layout_type = proto.Field(
                proto.ENUM, number=2, enum="Document.PageAnchor.PageRef.LayoutType",
            )
            layout_id = proto.Field(proto.STRING, number=3,)
            bounding_poly = proto.Field(
                proto.MESSAGE, number=4, message=geometry.BoundingPoly,
            )
            confidence = proto.Field(proto.FLOAT, number=5,)

        page_refs = proto.RepeatedField(
            proto.MESSAGE, number=1, message="Document.PageAnchor.PageRef",
        )

    class Provenance(proto.Message):
        r"""Structure to identify provenance relationships between
        annotations in different revisions.

        Attributes:
            revision (int):
                The index of the revision that produced this
                element.
            id (int):
                The Id of this operation.  Needs to be unique
                within the scope of the revision.
            parents (Sequence[google.cloud.documentai_v1beta3.types.Document.Provenance.Parent]):
                References to the original elements that are
                replaced.
            type_ (google.cloud.documentai_v1beta3.types.Document.Provenance.OperationType):
                The type of provenance operation.
        """

        class OperationType(proto.Enum):
            r"""If a processor or agent does an explicit operation on
            existing elements.
            """
            OPERATION_TYPE_UNSPECIFIED = 0
            ADD = 1
            REMOVE = 2
            REPLACE = 3
            EVAL_REQUESTED = 4
            EVAL_APPROVED = 5
            EVAL_SKIPPED = 6

        class Parent(proto.Message):
            r"""Structure for referencing parent provenances.  When an
            element replaces one of more other elements parent references
            identify the elements that are replaced.

            Attributes:
                revision (int):
                    The index of the [Document.revisions] identifying the parent
                    revision.
                index (int):
                    The index of the parent revisions
                    corresponding collection of items (eg. list of
                    entities, properties within entities, etc.)
                id (int):
                    The id of the parent provenance.
            """

            revision = proto.Field(proto.INT32, number=1,)
            index = proto.Field(proto.INT32, number=3,)
            id = proto.Field(proto.INT32, number=2,)

        revision = proto.Field(proto.INT32, number=1,)
        id = proto.Field(proto.INT32, number=2,)
        parents = proto.RepeatedField(
            proto.MESSAGE, number=3, message="Document.Provenance.Parent",
        )
        type_ = proto.Field(
            proto.ENUM, number=4, enum="Document.Provenance.OperationType",
        )

    class Revision(proto.Message):
        r"""Contains past or forward revisions of this document.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            agent (str):
                If the change was made by a person specify
                the name or id of that person.

                This field is a member of `oneof`_ ``source``.
            processor (str):
                If the annotation was made by processor
                identify the processor by its resource name.

                This field is a member of `oneof`_ ``source``.
            id (str):
                Id of the revision.  Unique within the
                context of the document.
            parent (Sequence[int]):
                The revisions that this revision is based on. This can
                include one or more parent (when documents are merged.) This
                field represents the index into the ``revisions`` field.
            create_time (google.protobuf.timestamp_pb2.Timestamp):
                The time that the revision was created.
            human_review (google.cloud.documentai_v1beta3.types.Document.Revision.HumanReview):
                Human Review information of this revision.
        """

        class HumanReview(proto.Message):
            r"""Human Review information of the document.

            Attributes:
                state (str):
                    Human review state. e.g. ``requested``, ``succeeded``,
                    ``rejected``.
                state_message (str):
                    A message providing more details about the current state of
                    processing. For example, the rejection reason when the state
                    is ``rejected``.
            """

            state = proto.Field(proto.STRING, number=1,)
            state_message = proto.Field(proto.STRING, number=2,)

        agent = proto.Field(proto.STRING, number=4, oneof="source",)
        processor = proto.Field(proto.STRING, number=5, oneof="source",)
        id = proto.Field(proto.STRING, number=1,)
        parent = proto.RepeatedField(proto.INT32, number=2,)
        create_time = proto.Field(
            proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,
        )
        human_review = proto.Field(
            proto.MESSAGE, number=6, message="Document.Revision.HumanReview",
        )

    class TextChange(proto.Message):
        r"""This message is used for text changes aka. OCR corrections.

        Attributes:
            text_anchor (google.cloud.documentai_v1beta3.types.Document.TextAnchor):
                Provenance of the correction. Text anchor indexing into the
                [Document.text][google.cloud.documentai.v1beta3.Document.text].
                There can only be a single ``TextAnchor.text_segments``
                element. If the start and end index of the text segment are
                the same, the text change is inserted before that index.
            changed_text (str):
                The text that replaces the text identified in the
                ``text_anchor``.
            provenance (Sequence[google.cloud.documentai_v1beta3.types.Document.Provenance]):
                The history of this annotation.
        """

        text_anchor = proto.Field(
            proto.MESSAGE, number=1, message="Document.TextAnchor",
        )
        changed_text = proto.Field(proto.STRING, number=2,)
        provenance = proto.RepeatedField(
            proto.MESSAGE, number=3, message="Document.Provenance",
        )

    uri = proto.Field(proto.STRING, number=1, oneof="source",)
    content = proto.Field(proto.BYTES, number=2, oneof="source",)
    mime_type = proto.Field(proto.STRING, number=3,)
    text = proto.Field(proto.STRING, number=4,)
    text_styles = proto.RepeatedField(proto.MESSAGE, number=5, message=Style,)
    pages = proto.RepeatedField(proto.MESSAGE, number=6, message=Page,)
    entities = proto.RepeatedField(proto.MESSAGE, number=7, message=Entity,)
    entity_relations = proto.RepeatedField(
        proto.MESSAGE, number=8, message=EntityRelation,
    )
    text_changes = proto.RepeatedField(proto.MESSAGE, number=14, message=TextChange,)
    shard_info = proto.Field(proto.MESSAGE, number=9, message=ShardInfo,)
    error = proto.Field(proto.MESSAGE, number=10, message=status_pb2.Status,)
    revisions = proto.RepeatedField(proto.MESSAGE, number=13, message=Revision,)


__all__ = tuple(sorted(__protobuf__.manifest))
