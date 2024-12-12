# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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

from google.cloud.documentai_v1.types import barcode as gcd_barcode
from google.cloud.documentai_v1.types import geometry
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
from google.type import color_pb2  # type: ignore
from google.type import date_pb2  # type: ignore
from google.type import datetime_pb2  # type: ignore
from google.type import money_pb2  # type: ignore
from google.type import postal_address_pb2  # type: ignore


__protobuf__ = proto.module(
    package='google.cloud.documentai.v1',
    manifest={
        'Document',
    },
)


class Document(proto.Message):
    r"""Document represents the canonical document resource in
    Document AI. It is an interchange format that provides insights
    into documents and allows for collaboration between users and
    Document AI to iterate and optimize for quality.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        uri (str):
            Optional. Currently supports Google Cloud Storage URI of the
            form ``gs://bucket_name/object_name``. Object versioning is
            not supported. For more information, refer to `Google Cloud
            Storage Request
            URIs <https://cloud.google.com/storage/docs/reference-uris>`__.

            This field is a member of `oneof`_ ``source``.
        content (bytes):
            Optional. Inline document content, represented as a stream
            of bytes. Note: As with all ``bytes`` fields, protobuffers
            use a pure binary representation, whereas JSON
            representations use base64.

            This field is a member of `oneof`_ ``source``.
        mime_type (str):
            An IANA published `media type (MIME
            type) <https://www.iana.org/assignments/media-types/media-types.xhtml>`__.
        text (str):
            Optional. UTF-8 encoded text in reading order
            from the document.
        text_styles (MutableSequence[google.cloud.documentai_v1.types.Document.Style]):
            Styles for the
            [Document.text][google.cloud.documentai.v1.Document.text].
        pages (MutableSequence[google.cloud.documentai_v1.types.Document.Page]):
            Visual page layout for the
            [Document][google.cloud.documentai.v1.Document].
        entities (MutableSequence[google.cloud.documentai_v1.types.Document.Entity]):
            A list of entities detected on
            [Document.text][google.cloud.documentai.v1.Document.text].
            For document shards, entities in this list may cross shard
            boundaries.
        entity_relations (MutableSequence[google.cloud.documentai_v1.types.Document.EntityRelation]):
            Placeholder. Relationship among
            [Document.entities][google.cloud.documentai.v1.Document.entities].
        text_changes (MutableSequence[google.cloud.documentai_v1.types.Document.TextChange]):
            Placeholder. A list of text corrections made to
            [Document.text][google.cloud.documentai.v1.Document.text].
            This is usually used for annotating corrections to OCR
            mistakes. Text changes for a given revision may not overlap
            with each other.
        shard_info (google.cloud.documentai_v1.types.Document.ShardInfo):
            Information about the sharding if this
            document is sharded part of a larger document.
            If the document is not sharded, this message is
            not specified.
        error (google.rpc.status_pb2.Status):
            Any error that occurred while processing this
            document.
        revisions (MutableSequence[google.cloud.documentai_v1.types.Document.Revision]):
            Placeholder. Revision history of this
            document.
        document_layout (google.cloud.documentai_v1.types.Document.DocumentLayout):
            Parsed layout of the document.
        chunked_document (google.cloud.documentai_v1.types.Document.ChunkedDocument):
            Document chunked based on chunking config.
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
                [Document.text][google.cloud.documentai.v1.Document.text] in
                the overall document global text.
        """

        shard_index: int = proto.Field(
            proto.INT64,
            number=1,
        )
        shard_count: int = proto.Field(
            proto.INT64,
            number=2,
        )
        text_offset: int = proto.Field(
            proto.INT64,
            number=3,
        )

    class Style(proto.Message):
        r"""Annotation for common text style attributes. This adheres to
        CSS conventions as much as possible.

        Attributes:
            text_anchor (google.cloud.documentai_v1.types.Document.TextAnchor):
                Text anchor indexing into the
                [Document.text][google.cloud.documentai.v1.Document.text].
            color (google.type.color_pb2.Color):
                Text color.
            background_color (google.type.color_pb2.Color):
                Text background color.
            font_weight (str):
                `Font
                weight <https://www.w3schools.com/cssref/pr_font_weight.asp>`__.
                Possible values are ``normal``, ``bold``, ``bolder``, and
                ``lighter``.
            text_style (str):
                `Text
                style <https://www.w3schools.com/cssref/pr_font_font-style.asp>`__.
                Possible values are ``normal``, ``italic``, and ``oblique``.
            text_decoration (str):
                `Text
                decoration <https://www.w3schools.com/cssref/pr_text_text-decoration.asp>`__.
                Follows CSS standard.
            font_size (google.cloud.documentai_v1.types.Document.Style.FontSize):
                Font size.
            font_family (str):
                Font family such as ``Arial``, ``Times New Roman``.
                https://www.w3schools.com/cssref/pr_font_font-family.asp
        """

        class FontSize(proto.Message):
            r"""Font size with unit.

            Attributes:
                size (float):
                    Font size for the text.
                unit (str):
                    Unit for the font size. Follows CSS naming (such as ``in``,
                    ``px``, and ``pt``).
            """

            size: float = proto.Field(
                proto.FLOAT,
                number=1,
            )
            unit: str = proto.Field(
                proto.STRING,
                number=2,
            )

        text_anchor: 'Document.TextAnchor' = proto.Field(
            proto.MESSAGE,
            number=1,
            message='Document.TextAnchor',
        )
        color: color_pb2.Color = proto.Field(
            proto.MESSAGE,
            number=2,
            message=color_pb2.Color,
        )
        background_color: color_pb2.Color = proto.Field(
            proto.MESSAGE,
            number=3,
            message=color_pb2.Color,
        )
        font_weight: str = proto.Field(
            proto.STRING,
            number=4,
        )
        text_style: str = proto.Field(
            proto.STRING,
            number=5,
        )
        text_decoration: str = proto.Field(
            proto.STRING,
            number=6,
        )
        font_size: 'Document.Style.FontSize' = proto.Field(
            proto.MESSAGE,
            number=7,
            message='Document.Style.FontSize',
        )
        font_family: str = proto.Field(
            proto.STRING,
            number=8,
        )

    class Page(proto.Message):
        r"""A page in a [Document][google.cloud.documentai.v1.Document].

        Attributes:
            page_number (int):
                1-based index for current
                [Page][google.cloud.documentai.v1.Document.Page] in a parent
                [Document][google.cloud.documentai.v1.Document]. Useful when
                a page is taken out of a
                [Document][google.cloud.documentai.v1.Document] for
                individual processing.
            image (google.cloud.documentai_v1.types.Document.Page.Image):
                Rendered image for this page. This image is
                preprocessed to remove any skew, rotation, and
                distortions such that the annotation bounding
                boxes can be upright and axis-aligned.
            transforms (MutableSequence[google.cloud.documentai_v1.types.Document.Page.Matrix]):
                Transformation matrices that were applied to the original
                document image to produce
                [Page.image][google.cloud.documentai.v1.Document.Page.image].
            dimension (google.cloud.documentai_v1.types.Document.Page.Dimension):
                Physical dimension of the page.
            layout (google.cloud.documentai_v1.types.Document.Page.Layout):
                [Layout][google.cloud.documentai.v1.Document.Page.Layout]
                for the page.
            detected_languages (MutableSequence[google.cloud.documentai_v1.types.Document.Page.DetectedLanguage]):
                A list of detected languages together with
                confidence.
            blocks (MutableSequence[google.cloud.documentai_v1.types.Document.Page.Block]):
                A list of visually detected text blocks on
                the page. A block has a set of lines (collected
                into paragraphs) that have a common line-spacing
                and orientation.
            paragraphs (MutableSequence[google.cloud.documentai_v1.types.Document.Page.Paragraph]):
                A list of visually detected text paragraphs
                on the page. A collection of lines that a human
                would perceive as a paragraph.
            lines (MutableSequence[google.cloud.documentai_v1.types.Document.Page.Line]):
                A list of visually detected text lines on the
                page. A collection of tokens that a human would
                perceive as a line.
            tokens (MutableSequence[google.cloud.documentai_v1.types.Document.Page.Token]):
                A list of visually detected tokens on the
                page.
            visual_elements (MutableSequence[google.cloud.documentai_v1.types.Document.Page.VisualElement]):
                A list of detected non-text visual elements
                e.g. checkbox, signature etc. on the page.
            tables (MutableSequence[google.cloud.documentai_v1.types.Document.Page.Table]):
                A list of visually detected tables on the
                page.
            form_fields (MutableSequence[google.cloud.documentai_v1.types.Document.Page.FormField]):
                A list of visually detected form fields on
                the page.
            symbols (MutableSequence[google.cloud.documentai_v1.types.Document.Page.Symbol]):
                A list of visually detected symbols on the
                page.
            detected_barcodes (MutableSequence[google.cloud.documentai_v1.types.Document.Page.DetectedBarcode]):
                A list of detected barcodes.
            image_quality_scores (google.cloud.documentai_v1.types.Document.Page.ImageQualityScores):
                Image quality scores.
            provenance (google.cloud.documentai_v1.types.Document.Provenance):
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

            width: float = proto.Field(
                proto.FLOAT,
                number=1,
            )
            height: float = proto.Field(
                proto.FLOAT,
                number=2,
            )
            unit: str = proto.Field(
                proto.STRING,
                number=3,
            )

        class Image(proto.Message):
            r"""Rendered image contents for this page.

            Attributes:
                content (bytes):
                    Raw byte content of the image.
                mime_type (str):
                    Encoding `media type (MIME
                    type) <https://www.iana.org/assignments/media-types/media-types.xhtml>`__
                    for the image.
                width (int):
                    Width of the image in pixels.
                height (int):
                    Height of the image in pixels.
            """

            content: bytes = proto.Field(
                proto.BYTES,
                number=1,
            )
            mime_type: str = proto.Field(
                proto.STRING,
                number=2,
            )
            width: int = proto.Field(
                proto.INT32,
                number=3,
            )
            height: int = proto.Field(
                proto.INT32,
                number=4,
            )

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

            rows: int = proto.Field(
                proto.INT32,
                number=1,
            )
            cols: int = proto.Field(
                proto.INT32,
                number=2,
            )
            type_: int = proto.Field(
                proto.INT32,
                number=3,
            )
            data: bytes = proto.Field(
                proto.BYTES,
                number=4,
            )

        class Layout(proto.Message):
            r"""Visual element describing a layout unit on a page.

            Attributes:
                text_anchor (google.cloud.documentai_v1.types.Document.TextAnchor):
                    Text anchor indexing into the
                    [Document.text][google.cloud.documentai.v1.Document.text].
                confidence (float):
                    Confidence of the current
                    [Layout][google.cloud.documentai.v1.Document.Page.Layout]
                    within context of the object this layout is for. e.g.
                    confidence can be for a single token, a table, a visual
                    element, etc. depending on context. Range ``[0, 1]``.
                bounding_poly (google.cloud.documentai_v1.types.BoundingPoly):
                    The bounding polygon for the
                    [Layout][google.cloud.documentai.v1.Document.Page.Layout].
                orientation (google.cloud.documentai_v1.types.Document.Page.Layout.Orientation):
                    Detected orientation for the
                    [Layout][google.cloud.documentai.v1.Document.Page.Layout].
            """
            class Orientation(proto.Enum):
                r"""Detected human reading orientation.

                Values:
                    ORIENTATION_UNSPECIFIED (0):
                        Unspecified orientation.
                    PAGE_UP (1):
                        Orientation is aligned with page up.
                    PAGE_RIGHT (2):
                        Orientation is aligned with page right.
                        Turn the head 90 degrees clockwise from upright
                        to read.
                    PAGE_DOWN (3):
                        Orientation is aligned with page down.
                        Turn the head 180 degrees from upright to read.
                    PAGE_LEFT (4):
                        Orientation is aligned with page left.
                        Turn the head 90 degrees counterclockwise from
                        upright to read.
                """
                ORIENTATION_UNSPECIFIED = 0
                PAGE_UP = 1
                PAGE_RIGHT = 2
                PAGE_DOWN = 3
                PAGE_LEFT = 4

            text_anchor: 'Document.TextAnchor' = proto.Field(
                proto.MESSAGE,
                number=1,
                message='Document.TextAnchor',
            )
            confidence: float = proto.Field(
                proto.FLOAT,
                number=2,
            )
            bounding_poly: geometry.BoundingPoly = proto.Field(
                proto.MESSAGE,
                number=3,
                message=geometry.BoundingPoly,
            )
            orientation: 'Document.Page.Layout.Orientation' = proto.Field(
                proto.ENUM,
                number=4,
                enum='Document.Page.Layout.Orientation',
            )

        class Block(proto.Message):
            r"""A block has a set of lines (collected into paragraphs) that
            have a common line-spacing and orientation.

            Attributes:
                layout (google.cloud.documentai_v1.types.Document.Page.Layout):
                    [Layout][google.cloud.documentai.v1.Document.Page.Layout]
                    for [Block][google.cloud.documentai.v1.Document.Page.Block].
                detected_languages (MutableSequence[google.cloud.documentai_v1.types.Document.Page.DetectedLanguage]):
                    A list of detected languages together with
                    confidence.
                provenance (google.cloud.documentai_v1.types.Document.Provenance):
                    The history of this annotation.
            """

            layout: 'Document.Page.Layout' = proto.Field(
                proto.MESSAGE,
                number=1,
                message='Document.Page.Layout',
            )
            detected_languages: MutableSequence['Document.Page.DetectedLanguage'] = proto.RepeatedField(
                proto.MESSAGE,
                number=2,
                message='Document.Page.DetectedLanguage',
            )
            provenance: 'Document.Provenance' = proto.Field(
                proto.MESSAGE,
                number=3,
                message='Document.Provenance',
            )

        class Paragraph(proto.Message):
            r"""A collection of lines that a human would perceive as a
            paragraph.

            Attributes:
                layout (google.cloud.documentai_v1.types.Document.Page.Layout):
                    [Layout][google.cloud.documentai.v1.Document.Page.Layout]
                    for
                    [Paragraph][google.cloud.documentai.v1.Document.Page.Paragraph].
                detected_languages (MutableSequence[google.cloud.documentai_v1.types.Document.Page.DetectedLanguage]):
                    A list of detected languages together with
                    confidence.
                provenance (google.cloud.documentai_v1.types.Document.Provenance):
                    The  history of this annotation.
            """

            layout: 'Document.Page.Layout' = proto.Field(
                proto.MESSAGE,
                number=1,
                message='Document.Page.Layout',
            )
            detected_languages: MutableSequence['Document.Page.DetectedLanguage'] = proto.RepeatedField(
                proto.MESSAGE,
                number=2,
                message='Document.Page.DetectedLanguage',
            )
            provenance: 'Document.Provenance' = proto.Field(
                proto.MESSAGE,
                number=3,
                message='Document.Provenance',
            )

        class Line(proto.Message):
            r"""A collection of tokens that a human would perceive as a line.
            Does not cross column boundaries, can be horizontal, vertical,
            etc.

            Attributes:
                layout (google.cloud.documentai_v1.types.Document.Page.Layout):
                    [Layout][google.cloud.documentai.v1.Document.Page.Layout]
                    for [Line][google.cloud.documentai.v1.Document.Page.Line].
                detected_languages (MutableSequence[google.cloud.documentai_v1.types.Document.Page.DetectedLanguage]):
                    A list of detected languages together with
                    confidence.
                provenance (google.cloud.documentai_v1.types.Document.Provenance):
                    The  history of this annotation.
            """

            layout: 'Document.Page.Layout' = proto.Field(
                proto.MESSAGE,
                number=1,
                message='Document.Page.Layout',
            )
            detected_languages: MutableSequence['Document.Page.DetectedLanguage'] = proto.RepeatedField(
                proto.MESSAGE,
                number=2,
                message='Document.Page.DetectedLanguage',
            )
            provenance: 'Document.Provenance' = proto.Field(
                proto.MESSAGE,
                number=3,
                message='Document.Provenance',
            )

        class Token(proto.Message):
            r"""A detected token.

            Attributes:
                layout (google.cloud.documentai_v1.types.Document.Page.Layout):
                    [Layout][google.cloud.documentai.v1.Document.Page.Layout]
                    for [Token][google.cloud.documentai.v1.Document.Page.Token].
                detected_break (google.cloud.documentai_v1.types.Document.Page.Token.DetectedBreak):
                    Detected break at the end of a
                    [Token][google.cloud.documentai.v1.Document.Page.Token].
                detected_languages (MutableSequence[google.cloud.documentai_v1.types.Document.Page.DetectedLanguage]):
                    A list of detected languages together with
                    confidence.
                provenance (google.cloud.documentai_v1.types.Document.Provenance):
                    The history of this annotation.
                style_info (google.cloud.documentai_v1.types.Document.Page.Token.StyleInfo):
                    Text style attributes.
            """

            class DetectedBreak(proto.Message):
                r"""Detected break at the end of a
                [Token][google.cloud.documentai.v1.Document.Page.Token].

                Attributes:
                    type_ (google.cloud.documentai_v1.types.Document.Page.Token.DetectedBreak.Type):
                        Detected break type.
                """
                class Type(proto.Enum):
                    r"""Enum to denote the type of break found.

                    Values:
                        TYPE_UNSPECIFIED (0):
                            Unspecified break type.
                        SPACE (1):
                            A single whitespace.
                        WIDE_SPACE (2):
                            A wider whitespace.
                        HYPHEN (3):
                            A hyphen that indicates that a token has been
                            split across lines.
                    """
                    TYPE_UNSPECIFIED = 0
                    SPACE = 1
                    WIDE_SPACE = 2
                    HYPHEN = 3

                type_: 'Document.Page.Token.DetectedBreak.Type' = proto.Field(
                    proto.ENUM,
                    number=1,
                    enum='Document.Page.Token.DetectedBreak.Type',
                )

            class StyleInfo(proto.Message):
                r"""Font and other text style attributes.

                Attributes:
                    font_size (int):
                        Font size in points (``1`` point is ``¹⁄₇₂`` inches).
                    pixel_font_size (float):
                        Font size in pixels, equal to *unrounded
                        [font_size][google.cloud.documentai.v1.Document.Page.Token.StyleInfo.font_size]*

                        -  *resolution* ÷ ``72.0``.
                    letter_spacing (float):
                        Letter spacing in points.
                    font_type (str):
                        Name or style of the font.
                    bold (bool):
                        Whether the text is bold (equivalent to
                        [font_weight][google.cloud.documentai.v1.Document.Page.Token.StyleInfo.font_weight]
                        is at least ``700``).
                    italic (bool):
                        Whether the text is italic.
                    underlined (bool):
                        Whether the text is underlined.
                    strikeout (bool):
                        Whether the text is strikethrough. This
                        feature is not supported yet.
                    subscript (bool):
                        Whether the text is a subscript. This feature
                        is not supported yet.
                    superscript (bool):
                        Whether the text is a superscript. This
                        feature is not supported yet.
                    smallcaps (bool):
                        Whether the text is in small caps. This
                        feature is not supported yet.
                    font_weight (int):
                        TrueType weight on a scale ``100`` (thin) to ``1000``
                        (ultra-heavy). Normal is ``400``, bold is ``700``.
                    handwritten (bool):
                        Whether the text is handwritten.
                    text_color (google.type.color_pb2.Color):
                        Color of the text.
                    background_color (google.type.color_pb2.Color):
                        Color of the background.
                """

                font_size: int = proto.Field(
                    proto.INT32,
                    number=1,
                )
                pixel_font_size: float = proto.Field(
                    proto.DOUBLE,
                    number=2,
                )
                letter_spacing: float = proto.Field(
                    proto.DOUBLE,
                    number=3,
                )
                font_type: str = proto.Field(
                    proto.STRING,
                    number=4,
                )
                bold: bool = proto.Field(
                    proto.BOOL,
                    number=5,
                )
                italic: bool = proto.Field(
                    proto.BOOL,
                    number=6,
                )
                underlined: bool = proto.Field(
                    proto.BOOL,
                    number=7,
                )
                strikeout: bool = proto.Field(
                    proto.BOOL,
                    number=8,
                )
                subscript: bool = proto.Field(
                    proto.BOOL,
                    number=9,
                )
                superscript: bool = proto.Field(
                    proto.BOOL,
                    number=10,
                )
                smallcaps: bool = proto.Field(
                    proto.BOOL,
                    number=11,
                )
                font_weight: int = proto.Field(
                    proto.INT32,
                    number=12,
                )
                handwritten: bool = proto.Field(
                    proto.BOOL,
                    number=13,
                )
                text_color: color_pb2.Color = proto.Field(
                    proto.MESSAGE,
                    number=14,
                    message=color_pb2.Color,
                )
                background_color: color_pb2.Color = proto.Field(
                    proto.MESSAGE,
                    number=15,
                    message=color_pb2.Color,
                )

            layout: 'Document.Page.Layout' = proto.Field(
                proto.MESSAGE,
                number=1,
                message='Document.Page.Layout',
            )
            detected_break: 'Document.Page.Token.DetectedBreak' = proto.Field(
                proto.MESSAGE,
                number=2,
                message='Document.Page.Token.DetectedBreak',
            )
            detected_languages: MutableSequence['Document.Page.DetectedLanguage'] = proto.RepeatedField(
                proto.MESSAGE,
                number=3,
                message='Document.Page.DetectedLanguage',
            )
            provenance: 'Document.Provenance' = proto.Field(
                proto.MESSAGE,
                number=4,
                message='Document.Provenance',
            )
            style_info: 'Document.Page.Token.StyleInfo' = proto.Field(
                proto.MESSAGE,
                number=5,
                message='Document.Page.Token.StyleInfo',
            )

        class Symbol(proto.Message):
            r"""A detected symbol.

            Attributes:
                layout (google.cloud.documentai_v1.types.Document.Page.Layout):
                    [Layout][google.cloud.documentai.v1.Document.Page.Layout]
                    for
                    [Symbol][google.cloud.documentai.v1.Document.Page.Symbol].
                detected_languages (MutableSequence[google.cloud.documentai_v1.types.Document.Page.DetectedLanguage]):
                    A list of detected languages together with
                    confidence.
            """

            layout: 'Document.Page.Layout' = proto.Field(
                proto.MESSAGE,
                number=1,
                message='Document.Page.Layout',
            )
            detected_languages: MutableSequence['Document.Page.DetectedLanguage'] = proto.RepeatedField(
                proto.MESSAGE,
                number=2,
                message='Document.Page.DetectedLanguage',
            )

        class VisualElement(proto.Message):
            r"""Detected non-text visual elements e.g. checkbox, signature
            etc. on the page.

            Attributes:
                layout (google.cloud.documentai_v1.types.Document.Page.Layout):
                    [Layout][google.cloud.documentai.v1.Document.Page.Layout]
                    for
                    [VisualElement][google.cloud.documentai.v1.Document.Page.VisualElement].
                type_ (str):
                    Type of the
                    [VisualElement][google.cloud.documentai.v1.Document.Page.VisualElement].
                detected_languages (MutableSequence[google.cloud.documentai_v1.types.Document.Page.DetectedLanguage]):
                    A list of detected languages together with
                    confidence.
            """

            layout: 'Document.Page.Layout' = proto.Field(
                proto.MESSAGE,
                number=1,
                message='Document.Page.Layout',
            )
            type_: str = proto.Field(
                proto.STRING,
                number=2,
            )
            detected_languages: MutableSequence['Document.Page.DetectedLanguage'] = proto.RepeatedField(
                proto.MESSAGE,
                number=3,
                message='Document.Page.DetectedLanguage',
            )

        class Table(proto.Message):
            r"""A table representation similar to HTML table structure.

            Attributes:
                layout (google.cloud.documentai_v1.types.Document.Page.Layout):
                    [Layout][google.cloud.documentai.v1.Document.Page.Layout]
                    for [Table][google.cloud.documentai.v1.Document.Page.Table].
                header_rows (MutableSequence[google.cloud.documentai_v1.types.Document.Page.Table.TableRow]):
                    Header rows of the table.
                body_rows (MutableSequence[google.cloud.documentai_v1.types.Document.Page.Table.TableRow]):
                    Body rows of the table.
                detected_languages (MutableSequence[google.cloud.documentai_v1.types.Document.Page.DetectedLanguage]):
                    A list of detected languages together with
                    confidence.
                provenance (google.cloud.documentai_v1.types.Document.Provenance):
                    The history of this table.
            """

            class TableRow(proto.Message):
                r"""A row of table cells.

                Attributes:
                    cells (MutableSequence[google.cloud.documentai_v1.types.Document.Page.Table.TableCell]):
                        Cells that make up this row.
                """

                cells: MutableSequence['Document.Page.Table.TableCell'] = proto.RepeatedField(
                    proto.MESSAGE,
                    number=1,
                    message='Document.Page.Table.TableCell',
                )

            class TableCell(proto.Message):
                r"""A cell representation inside the table.

                Attributes:
                    layout (google.cloud.documentai_v1.types.Document.Page.Layout):
                        [Layout][google.cloud.documentai.v1.Document.Page.Layout]
                        for
                        [TableCell][google.cloud.documentai.v1.Document.Page.Table.TableCell].
                    row_span (int):
                        How many rows this cell spans.
                    col_span (int):
                        How many columns this cell spans.
                    detected_languages (MutableSequence[google.cloud.documentai_v1.types.Document.Page.DetectedLanguage]):
                        A list of detected languages together with
                        confidence.
                """

                layout: 'Document.Page.Layout' = proto.Field(
                    proto.MESSAGE,
                    number=1,
                    message='Document.Page.Layout',
                )
                row_span: int = proto.Field(
                    proto.INT32,
                    number=2,
                )
                col_span: int = proto.Field(
                    proto.INT32,
                    number=3,
                )
                detected_languages: MutableSequence['Document.Page.DetectedLanguage'] = proto.RepeatedField(
                    proto.MESSAGE,
                    number=4,
                    message='Document.Page.DetectedLanguage',
                )

            layout: 'Document.Page.Layout' = proto.Field(
                proto.MESSAGE,
                number=1,
                message='Document.Page.Layout',
            )
            header_rows: MutableSequence['Document.Page.Table.TableRow'] = proto.RepeatedField(
                proto.MESSAGE,
                number=2,
                message='Document.Page.Table.TableRow',
            )
            body_rows: MutableSequence['Document.Page.Table.TableRow'] = proto.RepeatedField(
                proto.MESSAGE,
                number=3,
                message='Document.Page.Table.TableRow',
            )
            detected_languages: MutableSequence['Document.Page.DetectedLanguage'] = proto.RepeatedField(
                proto.MESSAGE,
                number=4,
                message='Document.Page.DetectedLanguage',
            )
            provenance: 'Document.Provenance' = proto.Field(
                proto.MESSAGE,
                number=5,
                message='Document.Provenance',
            )

        class FormField(proto.Message):
            r"""A form field detected on the page.

            Attributes:
                field_name (google.cloud.documentai_v1.types.Document.Page.Layout):
                    [Layout][google.cloud.documentai.v1.Document.Page.Layout]
                    for the
                    [FormField][google.cloud.documentai.v1.Document.Page.FormField]
                    name. e.g. ``Address``, ``Email``, ``Grand total``,
                    ``Phone number``, etc.
                field_value (google.cloud.documentai_v1.types.Document.Page.Layout):
                    [Layout][google.cloud.documentai.v1.Document.Page.Layout]
                    for the
                    [FormField][google.cloud.documentai.v1.Document.Page.FormField]
                    value.
                name_detected_languages (MutableSequence[google.cloud.documentai_v1.types.Document.Page.DetectedLanguage]):
                    A list of detected languages for name
                    together with confidence.
                value_detected_languages (MutableSequence[google.cloud.documentai_v1.types.Document.Page.DetectedLanguage]):
                    A list of detected languages for value
                    together with confidence.
                value_type (str):
                    If the value is non-textual, this field represents the type.
                    Current valid values are:

                    -  blank (this indicates the ``field_value`` is normal text)
                    -  ``unfilled_checkbox``
                    -  ``filled_checkbox``
                corrected_key_text (str):
                    Created for Labeling UI to export key text. If corrections
                    were made to the text identified by the
                    ``field_name.text_anchor``, this field will contain the
                    correction.
                corrected_value_text (str):
                    Created for Labeling UI to export value text. If corrections
                    were made to the text identified by the
                    ``field_value.text_anchor``, this field will contain the
                    correction.
                provenance (google.cloud.documentai_v1.types.Document.Provenance):
                    The history of this annotation.
            """

            field_name: 'Document.Page.Layout' = proto.Field(
                proto.MESSAGE,
                number=1,
                message='Document.Page.Layout',
            )
            field_value: 'Document.Page.Layout' = proto.Field(
                proto.MESSAGE,
                number=2,
                message='Document.Page.Layout',
            )
            name_detected_languages: MutableSequence['Document.Page.DetectedLanguage'] = proto.RepeatedField(
                proto.MESSAGE,
                number=3,
                message='Document.Page.DetectedLanguage',
            )
            value_detected_languages: MutableSequence['Document.Page.DetectedLanguage'] = proto.RepeatedField(
                proto.MESSAGE,
                number=4,
                message='Document.Page.DetectedLanguage',
            )
            value_type: str = proto.Field(
                proto.STRING,
                number=5,
            )
            corrected_key_text: str = proto.Field(
                proto.STRING,
                number=6,
            )
            corrected_value_text: str = proto.Field(
                proto.STRING,
                number=7,
            )
            provenance: 'Document.Provenance' = proto.Field(
                proto.MESSAGE,
                number=8,
                message='Document.Provenance',
            )

        class DetectedBarcode(proto.Message):
            r"""A detected barcode.

            Attributes:
                layout (google.cloud.documentai_v1.types.Document.Page.Layout):
                    [Layout][google.cloud.documentai.v1.Document.Page.Layout]
                    for
                    [DetectedBarcode][google.cloud.documentai.v1.Document.Page.DetectedBarcode].
                barcode (google.cloud.documentai_v1.types.Barcode):
                    Detailed barcode information of the
                    [DetectedBarcode][google.cloud.documentai.v1.Document.Page.DetectedBarcode].
            """

            layout: 'Document.Page.Layout' = proto.Field(
                proto.MESSAGE,
                number=1,
                message='Document.Page.Layout',
            )
            barcode: gcd_barcode.Barcode = proto.Field(
                proto.MESSAGE,
                number=2,
                message=gcd_barcode.Barcode,
            )

        class DetectedLanguage(proto.Message):
            r"""Detected language for a structural component.

            Attributes:
                language_code (str):
                    The `BCP-47 language
                    code <https://www.unicode.org/reports/tr35/#Unicode_locale_identifier>`__,
                    such as ``en-US`` or ``sr-Latn``.
                confidence (float):
                    Confidence of detected language. Range ``[0, 1]``.
            """

            language_code: str = proto.Field(
                proto.STRING,
                number=1,
            )
            confidence: float = proto.Field(
                proto.FLOAT,
                number=2,
            )

        class ImageQualityScores(proto.Message):
            r"""Image quality scores for the page image.

            Attributes:
                quality_score (float):
                    The overall quality score. Range ``[0, 1]`` where ``1`` is
                    perfect quality.
                detected_defects (MutableSequence[google.cloud.documentai_v1.types.Document.Page.ImageQualityScores.DetectedDefect]):
                    A list of detected defects.
            """

            class DetectedDefect(proto.Message):
                r"""Image Quality Defects

                Attributes:
                    type_ (str):
                        Name of the defect type. Supported values are:

                        -  ``quality/defect_blurry``
                        -  ``quality/defect_noisy``
                        -  ``quality/defect_dark``
                        -  ``quality/defect_faint``
                        -  ``quality/defect_text_too_small``
                        -  ``quality/defect_document_cutoff``
                        -  ``quality/defect_text_cutoff``
                        -  ``quality/defect_glare``
                    confidence (float):
                        Confidence of detected defect. Range ``[0, 1]`` where ``1``
                        indicates strong confidence that the defect exists.
                """

                type_: str = proto.Field(
                    proto.STRING,
                    number=1,
                )
                confidence: float = proto.Field(
                    proto.FLOAT,
                    number=2,
                )

            quality_score: float = proto.Field(
                proto.FLOAT,
                number=1,
            )
            detected_defects: MutableSequence['Document.Page.ImageQualityScores.DetectedDefect'] = proto.RepeatedField(
                proto.MESSAGE,
                number=2,
                message='Document.Page.ImageQualityScores.DetectedDefect',
            )

        page_number: int = proto.Field(
            proto.INT32,
            number=1,
        )
        image: 'Document.Page.Image' = proto.Field(
            proto.MESSAGE,
            number=13,
            message='Document.Page.Image',
        )
        transforms: MutableSequence['Document.Page.Matrix'] = proto.RepeatedField(
            proto.MESSAGE,
            number=14,
            message='Document.Page.Matrix',
        )
        dimension: 'Document.Page.Dimension' = proto.Field(
            proto.MESSAGE,
            number=2,
            message='Document.Page.Dimension',
        )
        layout: 'Document.Page.Layout' = proto.Field(
            proto.MESSAGE,
            number=3,
            message='Document.Page.Layout',
        )
        detected_languages: MutableSequence['Document.Page.DetectedLanguage'] = proto.RepeatedField(
            proto.MESSAGE,
            number=4,
            message='Document.Page.DetectedLanguage',
        )
        blocks: MutableSequence['Document.Page.Block'] = proto.RepeatedField(
            proto.MESSAGE,
            number=5,
            message='Document.Page.Block',
        )
        paragraphs: MutableSequence['Document.Page.Paragraph'] = proto.RepeatedField(
            proto.MESSAGE,
            number=6,
            message='Document.Page.Paragraph',
        )
        lines: MutableSequence['Document.Page.Line'] = proto.RepeatedField(
            proto.MESSAGE,
            number=7,
            message='Document.Page.Line',
        )
        tokens: MutableSequence['Document.Page.Token'] = proto.RepeatedField(
            proto.MESSAGE,
            number=8,
            message='Document.Page.Token',
        )
        visual_elements: MutableSequence['Document.Page.VisualElement'] = proto.RepeatedField(
            proto.MESSAGE,
            number=9,
            message='Document.Page.VisualElement',
        )
        tables: MutableSequence['Document.Page.Table'] = proto.RepeatedField(
            proto.MESSAGE,
            number=10,
            message='Document.Page.Table',
        )
        form_fields: MutableSequence['Document.Page.FormField'] = proto.RepeatedField(
            proto.MESSAGE,
            number=11,
            message='Document.Page.FormField',
        )
        symbols: MutableSequence['Document.Page.Symbol'] = proto.RepeatedField(
            proto.MESSAGE,
            number=12,
            message='Document.Page.Symbol',
        )
        detected_barcodes: MutableSequence['Document.Page.DetectedBarcode'] = proto.RepeatedField(
            proto.MESSAGE,
            number=15,
            message='Document.Page.DetectedBarcode',
        )
        image_quality_scores: 'Document.Page.ImageQualityScores' = proto.Field(
            proto.MESSAGE,
            number=17,
            message='Document.Page.ImageQualityScores',
        )
        provenance: 'Document.Provenance' = proto.Field(
            proto.MESSAGE,
            number=16,
            message='Document.Provenance',
        )

    class Entity(proto.Message):
        r"""An entity that could be a phrase in the text or a property
        that belongs to the document. It is a known entity type, such as
        a person, an organization, or location.

        Attributes:
            text_anchor (google.cloud.documentai_v1.types.Document.TextAnchor):
                Optional. Provenance of the entity. Text anchor indexing
                into the
                [Document.text][google.cloud.documentai.v1.Document.text].
            type_ (str):
                Required. Entity type from a schema e.g. ``Address``.
            mention_text (str):
                Optional. Text value of the entity e.g.
                ``1600 Amphitheatre Pkwy``.
            mention_id (str):
                Optional. Deprecated. Use ``id`` field instead.
            confidence (float):
                Optional. Confidence of detected Schema entity. Range
                ``[0, 1]``.
            page_anchor (google.cloud.documentai_v1.types.Document.PageAnchor):
                Optional. Represents the provenance of this
                entity wrt. the location on the page where it
                was found.
            id (str):
                Optional. Canonical id. This will be a unique
                value in the entity list for this document.
            normalized_value (google.cloud.documentai_v1.types.Document.Entity.NormalizedValue):
                Optional. Normalized entity value. Absent if
                the extracted value could not be converted or
                the type (e.g. address) is not supported for
                certain parsers. This field is also only
                populated for certain supported document types.
            properties (MutableSequence[google.cloud.documentai_v1.types.Document.Entity]):
                Optional. Entities can be nested to form a
                hierarchical data structure representing the
                content in the document.
            provenance (google.cloud.documentai_v1.types.Document.Provenance):
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
                integer_value (int):
                    Integer value.

                    This field is a member of `oneof`_ ``structured_value``.
                float_value (float):
                    Float value.

                    This field is a member of `oneof`_ ``structured_value``.
                text (str):
                    Optional. An optional field to store a normalized string.
                    For some entity types, one of respective
                    ``structured_value`` fields may also be populated. Also not
                    all the types of ``structured_value`` will be normalized.
                    For example, some processors may not generate ``float`` or
                    ``integer`` normalized text by default.

                    Below are sample formats mapped to structured values.

                    -  Money/Currency type (``money_value``) is in the ISO 4217
                       text format.
                    -  Date type (``date_value``) is in the ISO 8601 text
                       format.
                    -  Datetime type (``datetime_value``) is in the ISO 8601
                       text format.
            """

            money_value: money_pb2.Money = proto.Field(
                proto.MESSAGE,
                number=2,
                oneof='structured_value',
                message=money_pb2.Money,
            )
            date_value: date_pb2.Date = proto.Field(
                proto.MESSAGE,
                number=3,
                oneof='structured_value',
                message=date_pb2.Date,
            )
            datetime_value: datetime_pb2.DateTime = proto.Field(
                proto.MESSAGE,
                number=4,
                oneof='structured_value',
                message=datetime_pb2.DateTime,
            )
            address_value: postal_address_pb2.PostalAddress = proto.Field(
                proto.MESSAGE,
                number=5,
                oneof='structured_value',
                message=postal_address_pb2.PostalAddress,
            )
            boolean_value: bool = proto.Field(
                proto.BOOL,
                number=6,
                oneof='structured_value',
            )
            integer_value: int = proto.Field(
                proto.INT32,
                number=7,
                oneof='structured_value',
            )
            float_value: float = proto.Field(
                proto.FLOAT,
                number=8,
                oneof='structured_value',
            )
            text: str = proto.Field(
                proto.STRING,
                number=1,
            )

        text_anchor: 'Document.TextAnchor' = proto.Field(
            proto.MESSAGE,
            number=1,
            message='Document.TextAnchor',
        )
        type_: str = proto.Field(
            proto.STRING,
            number=2,
        )
        mention_text: str = proto.Field(
            proto.STRING,
            number=3,
        )
        mention_id: str = proto.Field(
            proto.STRING,
            number=4,
        )
        confidence: float = proto.Field(
            proto.FLOAT,
            number=5,
        )
        page_anchor: 'Document.PageAnchor' = proto.Field(
            proto.MESSAGE,
            number=6,
            message='Document.PageAnchor',
        )
        id: str = proto.Field(
            proto.STRING,
            number=7,
        )
        normalized_value: 'Document.Entity.NormalizedValue' = proto.Field(
            proto.MESSAGE,
            number=9,
            message='Document.Entity.NormalizedValue',
        )
        properties: MutableSequence['Document.Entity'] = proto.RepeatedField(
            proto.MESSAGE,
            number=10,
            message='Document.Entity',
        )
        provenance: 'Document.Provenance' = proto.Field(
            proto.MESSAGE,
            number=11,
            message='Document.Provenance',
        )
        redacted: bool = proto.Field(
            proto.BOOL,
            number=12,
        )

    class EntityRelation(proto.Message):
        r"""Relationship between
        [Entities][google.cloud.documentai.v1.Document.Entity].

        Attributes:
            subject_id (str):
                Subject entity id.
            object_id (str):
                Object entity id.
            relation (str):
                Relationship description.
        """

        subject_id: str = proto.Field(
            proto.STRING,
            number=1,
        )
        object_id: str = proto.Field(
            proto.STRING,
            number=2,
        )
        relation: str = proto.Field(
            proto.STRING,
            number=3,
        )

    class TextAnchor(proto.Message):
        r"""Text reference indexing into the
        [Document.text][google.cloud.documentai.v1.Document.text].

        Attributes:
            text_segments (MutableSequence[google.cloud.documentai_v1.types.Document.TextAnchor.TextSegment]):
                The text segments from the
                [Document.text][google.cloud.documentai.v1.Document.text].
            content (str):
                Contains the content of the text span so that users do not
                have to look it up in the text_segments. It is always
                populated for formFields.
        """

        class TextSegment(proto.Message):
            r"""A text segment in the
            [Document.text][google.cloud.documentai.v1.Document.text]. The
            indices may be out of bounds which indicate that the text extends
            into another document shard for large sharded documents. See
            [ShardInfo.text_offset][google.cloud.documentai.v1.Document.ShardInfo.text_offset]

            Attributes:
                start_index (int):
                    [TextSegment][google.cloud.documentai.v1.Document.TextAnchor.TextSegment]
                    start UTF-8 char index in the
                    [Document.text][google.cloud.documentai.v1.Document.text].
                end_index (int):
                    [TextSegment][google.cloud.documentai.v1.Document.TextAnchor.TextSegment]
                    half open end UTF-8 char index in the
                    [Document.text][google.cloud.documentai.v1.Document.text].
            """

            start_index: int = proto.Field(
                proto.INT64,
                number=1,
            )
            end_index: int = proto.Field(
                proto.INT64,
                number=2,
            )

        text_segments: MutableSequence['Document.TextAnchor.TextSegment'] = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message='Document.TextAnchor.TextSegment',
        )
        content: str = proto.Field(
            proto.STRING,
            number=2,
        )

    class PageAnchor(proto.Message):
        r"""Referencing the visual context of the entity in the
        [Document.pages][google.cloud.documentai.v1.Document.pages]. Page
        anchors can be cross-page, consist of multiple bounding polygons and
        optionally reference specific layout element types.

        Attributes:
            page_refs (MutableSequence[google.cloud.documentai_v1.types.Document.PageAnchor.PageRef]):
                One or more references to visual page
                elements
        """

        class PageRef(proto.Message):
            r"""Represents a weak reference to a page element within a
            document.

            Attributes:
                page (int):
                    Required. Index into the
                    [Document.pages][google.cloud.documentai.v1.Document.pages]
                    element, for example using
                    ``[Document.pages][page_refs.page]`` to locate the related
                    page element. This field is skipped when its value is the
                    default ``0``. See
                    https://developers.google.com/protocol-buffers/docs/proto3#json.
                layout_type (google.cloud.documentai_v1.types.Document.PageAnchor.PageRef.LayoutType):
                    Optional. The type of the layout element that
                    is being referenced if any.
                layout_id (str):
                    Optional. Deprecated. Use
                    [PageRef.bounding_poly][google.cloud.documentai.v1.Document.PageAnchor.PageRef.bounding_poly]
                    instead.
                bounding_poly (google.cloud.documentai_v1.types.BoundingPoly):
                    Optional. Identifies the bounding polygon of a layout
                    element on the page. If ``layout_type`` is set, the bounding
                    polygon must be exactly the same to the layout element it's
                    referring to.
                confidence (float):
                    Optional. Confidence of detected page element, if
                    applicable. Range ``[0, 1]``.
            """
            class LayoutType(proto.Enum):
                r"""The type of layout that is being referenced.

                Values:
                    LAYOUT_TYPE_UNSPECIFIED (0):
                        Layout Unspecified.
                    BLOCK (1):
                        References a
                        [Page.blocks][google.cloud.documentai.v1.Document.Page.blocks]
                        element.
                    PARAGRAPH (2):
                        References a
                        [Page.paragraphs][google.cloud.documentai.v1.Document.Page.paragraphs]
                        element.
                    LINE (3):
                        References a
                        [Page.lines][google.cloud.documentai.v1.Document.Page.lines]
                        element.
                    TOKEN (4):
                        References a
                        [Page.tokens][google.cloud.documentai.v1.Document.Page.tokens]
                        element.
                    VISUAL_ELEMENT (5):
                        References a
                        [Page.visual_elements][google.cloud.documentai.v1.Document.Page.visual_elements]
                        element.
                    TABLE (6):
                        Refrrences a
                        [Page.tables][google.cloud.documentai.v1.Document.Page.tables]
                        element.
                    FORM_FIELD (7):
                        References a
                        [Page.form_fields][google.cloud.documentai.v1.Document.Page.form_fields]
                        element.
                """
                LAYOUT_TYPE_UNSPECIFIED = 0
                BLOCK = 1
                PARAGRAPH = 2
                LINE = 3
                TOKEN = 4
                VISUAL_ELEMENT = 5
                TABLE = 6
                FORM_FIELD = 7

            page: int = proto.Field(
                proto.INT64,
                number=1,
            )
            layout_type: 'Document.PageAnchor.PageRef.LayoutType' = proto.Field(
                proto.ENUM,
                number=2,
                enum='Document.PageAnchor.PageRef.LayoutType',
            )
            layout_id: str = proto.Field(
                proto.STRING,
                number=3,
            )
            bounding_poly: geometry.BoundingPoly = proto.Field(
                proto.MESSAGE,
                number=4,
                message=geometry.BoundingPoly,
            )
            confidence: float = proto.Field(
                proto.FLOAT,
                number=5,
            )

        page_refs: MutableSequence['Document.PageAnchor.PageRef'] = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message='Document.PageAnchor.PageRef',
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
            parents (MutableSequence[google.cloud.documentai_v1.types.Document.Provenance.Parent]):
                References to the original elements that are
                replaced.
            type_ (google.cloud.documentai_v1.types.Document.Provenance.OperationType):
                The type of provenance operation.
        """
        class OperationType(proto.Enum):
            r"""If a processor or agent does an explicit operation on
            existing elements.

            Values:
                OPERATION_TYPE_UNSPECIFIED (0):
                    Operation type unspecified. If no operation is specified a
                    provenance entry is simply used to match against a
                    ``parent``.
                ADD (1):
                    Add an element.
                REMOVE (2):
                    Remove an element identified by ``parent``.
                UPDATE (7):
                    Updates any fields within the given
                    provenance scope of the message. It overwrites
                    the fields rather than replacing them.  Use this
                    when you want to update a field value of an
                    entity without also updating all the child
                    properties.
                REPLACE (3):
                    Currently unused. Replace an element identified by
                    ``parent``.
                EVAL_REQUESTED (4):
                    Deprecated. Request human review for the element identified
                    by ``parent``.
                EVAL_APPROVED (5):
                    Deprecated. Element is reviewed and approved
                    at human review, confidence will be set to 1.0.
                EVAL_SKIPPED (6):
                    Deprecated. Element is skipped in the
                    validation process.
            """
            OPERATION_TYPE_UNSPECIFIED = 0
            ADD = 1
            REMOVE = 2
            UPDATE = 7
            REPLACE = 3
            EVAL_REQUESTED = 4
            EVAL_APPROVED = 5
            EVAL_SKIPPED = 6

        class Parent(proto.Message):
            r"""The parent element the current element is based on. Used for
            referencing/aligning, removal and replacement operations.

            Attributes:
                revision (int):
                    The index of the index into current revision's parent_ids
                    list.
                index (int):
                    The index of the parent item in the
                    corresponding item list (eg. list of entities,
                    properties within entities, etc.) in the parent
                    revision.
                id (int):
                    The id of the parent provenance.
            """

            revision: int = proto.Field(
                proto.INT32,
                number=1,
            )
            index: int = proto.Field(
                proto.INT32,
                number=3,
            )
            id: int = proto.Field(
                proto.INT32,
                number=2,
            )

        revision: int = proto.Field(
            proto.INT32,
            number=1,
        )
        id: int = proto.Field(
            proto.INT32,
            number=2,
        )
        parents: MutableSequence['Document.Provenance.Parent'] = proto.RepeatedField(
            proto.MESSAGE,
            number=3,
            message='Document.Provenance.Parent',
        )
        type_: 'Document.Provenance.OperationType' = proto.Field(
            proto.ENUM,
            number=4,
            enum='Document.Provenance.OperationType',
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
                Id of the revision, internally generated by
                doc proto storage. Unique within the context of
                the document.
            parent (MutableSequence[int]):
                The revisions that this revision is based on. This can
                include one or more parent (when documents are merged.) This
                field represents the index into the ``revisions`` field.
            parent_ids (MutableSequence[str]):
                The revisions that this revision is based on. Must include
                all the ids that have anything to do with this revision -
                eg. there are ``provenance.parent.revision`` fields that
                index into this field.
            create_time (google.protobuf.timestamp_pb2.Timestamp):
                The time that the revision was created,
                internally generated by doc proto storage at the
                time of create.
            human_review (google.cloud.documentai_v1.types.Document.Revision.HumanReview):
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

            state: str = proto.Field(
                proto.STRING,
                number=1,
            )
            state_message: str = proto.Field(
                proto.STRING,
                number=2,
            )

        agent: str = proto.Field(
            proto.STRING,
            number=4,
            oneof='source',
        )
        processor: str = proto.Field(
            proto.STRING,
            number=5,
            oneof='source',
        )
        id: str = proto.Field(
            proto.STRING,
            number=1,
        )
        parent: MutableSequence[int] = proto.RepeatedField(
            proto.INT32,
            number=2,
        )
        parent_ids: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=7,
        )
        create_time: timestamp_pb2.Timestamp = proto.Field(
            proto.MESSAGE,
            number=3,
            message=timestamp_pb2.Timestamp,
        )
        human_review: 'Document.Revision.HumanReview' = proto.Field(
            proto.MESSAGE,
            number=6,
            message='Document.Revision.HumanReview',
        )

    class TextChange(proto.Message):
        r"""This message is used for text changes aka. OCR corrections.

        Attributes:
            text_anchor (google.cloud.documentai_v1.types.Document.TextAnchor):
                Provenance of the correction. Text anchor indexing into the
                [Document.text][google.cloud.documentai.v1.Document.text].
                There can only be a single ``TextAnchor.text_segments``
                element. If the start and end index of the text segment are
                the same, the text change is inserted before that index.
            changed_text (str):
                The text that replaces the text identified in the
                ``text_anchor``.
            provenance (MutableSequence[google.cloud.documentai_v1.types.Document.Provenance]):
                The history of this annotation.
        """

        text_anchor: 'Document.TextAnchor' = proto.Field(
            proto.MESSAGE,
            number=1,
            message='Document.TextAnchor',
        )
        changed_text: str = proto.Field(
            proto.STRING,
            number=2,
        )
        provenance: MutableSequence['Document.Provenance'] = proto.RepeatedField(
            proto.MESSAGE,
            number=3,
            message='Document.Provenance',
        )

    class DocumentLayout(proto.Message):
        r"""Represents the parsed layout of a document as a collection of
        blocks that the document is divided into.

        Attributes:
            blocks (MutableSequence[google.cloud.documentai_v1.types.Document.DocumentLayout.DocumentLayoutBlock]):
                List of blocks in the document.
        """

        class DocumentLayoutBlock(proto.Message):
            r"""Represents a block. A block could be one of the various types
            (text, table, list) supported.

            This message has `oneof`_ fields (mutually exclusive fields).
            For each oneof, at most one member field can be set at the same time.
            Setting any member of the oneof automatically clears all other
            members.

            .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

            Attributes:
                text_block (google.cloud.documentai_v1.types.Document.DocumentLayout.DocumentLayoutBlock.LayoutTextBlock):
                    Block consisting of text content.

                    This field is a member of `oneof`_ ``block``.
                table_block (google.cloud.documentai_v1.types.Document.DocumentLayout.DocumentLayoutBlock.LayoutTableBlock):
                    Block consisting of table content/structure.

                    This field is a member of `oneof`_ ``block``.
                list_block (google.cloud.documentai_v1.types.Document.DocumentLayout.DocumentLayoutBlock.LayoutListBlock):
                    Block consisting of list content/structure.

                    This field is a member of `oneof`_ ``block``.
                block_id (str):
                    ID of the block.
                page_span (google.cloud.documentai_v1.types.Document.DocumentLayout.DocumentLayoutBlock.LayoutPageSpan):
                    Page span of the block.
            """

            class LayoutPageSpan(proto.Message):
                r"""Represents where the block starts and ends in the document.

                Attributes:
                    page_start (int):
                        Page where block starts in the document.
                    page_end (int):
                        Page where block ends in the document.
                """

                page_start: int = proto.Field(
                    proto.INT32,
                    number=1,
                )
                page_end: int = proto.Field(
                    proto.INT32,
                    number=2,
                )

            class LayoutTextBlock(proto.Message):
                r"""Represents a text type block.

                Attributes:
                    text (str):
                        Text content stored in the block.
                    type_ (str):
                        Type of the text in the block. Available options are:
                        ``paragraph``, ``subtitle``, ``heading-1``, ``heading-2``,
                        ``heading-3``, ``heading-4``, ``heading-5``, ``header``,
                        ``footer``.
                    blocks (MutableSequence[google.cloud.documentai_v1.types.Document.DocumentLayout.DocumentLayoutBlock]):
                        A text block could further have child blocks.
                        Repeated blocks support further hierarchies and
                        nested blocks.
                """

                text: str = proto.Field(
                    proto.STRING,
                    number=1,
                )
                type_: str = proto.Field(
                    proto.STRING,
                    number=2,
                )
                blocks: MutableSequence['Document.DocumentLayout.DocumentLayoutBlock'] = proto.RepeatedField(
                    proto.MESSAGE,
                    number=3,
                    message='Document.DocumentLayout.DocumentLayoutBlock',
                )

            class LayoutTableBlock(proto.Message):
                r"""Represents a table type block.

                Attributes:
                    header_rows (MutableSequence[google.cloud.documentai_v1.types.Document.DocumentLayout.DocumentLayoutBlock.LayoutTableRow]):
                        Header rows at the top of the table.
                    body_rows (MutableSequence[google.cloud.documentai_v1.types.Document.DocumentLayout.DocumentLayoutBlock.LayoutTableRow]):
                        Body rows containing main table content.
                    caption (str):
                        Table caption/title.
                """

                header_rows: MutableSequence['Document.DocumentLayout.DocumentLayoutBlock.LayoutTableRow'] = proto.RepeatedField(
                    proto.MESSAGE,
                    number=1,
                    message='Document.DocumentLayout.DocumentLayoutBlock.LayoutTableRow',
                )
                body_rows: MutableSequence['Document.DocumentLayout.DocumentLayoutBlock.LayoutTableRow'] = proto.RepeatedField(
                    proto.MESSAGE,
                    number=2,
                    message='Document.DocumentLayout.DocumentLayoutBlock.LayoutTableRow',
                )
                caption: str = proto.Field(
                    proto.STRING,
                    number=3,
                )

            class LayoutTableRow(proto.Message):
                r"""Represents a row in a table.

                Attributes:
                    cells (MutableSequence[google.cloud.documentai_v1.types.Document.DocumentLayout.DocumentLayoutBlock.LayoutTableCell]):
                        A table row is a list of table cells.
                """

                cells: MutableSequence['Document.DocumentLayout.DocumentLayoutBlock.LayoutTableCell'] = proto.RepeatedField(
                    proto.MESSAGE,
                    number=1,
                    message='Document.DocumentLayout.DocumentLayoutBlock.LayoutTableCell',
                )

            class LayoutTableCell(proto.Message):
                r"""Represents a cell in a table row.

                Attributes:
                    blocks (MutableSequence[google.cloud.documentai_v1.types.Document.DocumentLayout.DocumentLayoutBlock]):
                        A table cell is a list of blocks.
                        Repeated blocks support further hierarchies and
                        nested blocks.
                    row_span (int):
                        How many rows this cell spans.
                    col_span (int):
                        How many columns this cell spans.
                """

                blocks: MutableSequence['Document.DocumentLayout.DocumentLayoutBlock'] = proto.RepeatedField(
                    proto.MESSAGE,
                    number=1,
                    message='Document.DocumentLayout.DocumentLayoutBlock',
                )
                row_span: int = proto.Field(
                    proto.INT32,
                    number=2,
                )
                col_span: int = proto.Field(
                    proto.INT32,
                    number=3,
                )

            class LayoutListBlock(proto.Message):
                r"""Represents a list type block.

                Attributes:
                    list_entries (MutableSequence[google.cloud.documentai_v1.types.Document.DocumentLayout.DocumentLayoutBlock.LayoutListEntry]):
                        List entries that constitute a list block.
                    type_ (str):
                        Type of the list_entries (if exist). Available options are
                        ``ordered`` and ``unordered``.
                """

                list_entries: MutableSequence['Document.DocumentLayout.DocumentLayoutBlock.LayoutListEntry'] = proto.RepeatedField(
                    proto.MESSAGE,
                    number=1,
                    message='Document.DocumentLayout.DocumentLayoutBlock.LayoutListEntry',
                )
                type_: str = proto.Field(
                    proto.STRING,
                    number=2,
                )

            class LayoutListEntry(proto.Message):
                r"""Represents an entry in the list.

                Attributes:
                    blocks (MutableSequence[google.cloud.documentai_v1.types.Document.DocumentLayout.DocumentLayoutBlock]):
                        A list entry is a list of blocks.
                        Repeated blocks support further hierarchies and
                        nested blocks.
                """

                blocks: MutableSequence['Document.DocumentLayout.DocumentLayoutBlock'] = proto.RepeatedField(
                    proto.MESSAGE,
                    number=1,
                    message='Document.DocumentLayout.DocumentLayoutBlock',
                )

            text_block: 'Document.DocumentLayout.DocumentLayoutBlock.LayoutTextBlock' = proto.Field(
                proto.MESSAGE,
                number=2,
                oneof='block',
                message='Document.DocumentLayout.DocumentLayoutBlock.LayoutTextBlock',
            )
            table_block: 'Document.DocumentLayout.DocumentLayoutBlock.LayoutTableBlock' = proto.Field(
                proto.MESSAGE,
                number=3,
                oneof='block',
                message='Document.DocumentLayout.DocumentLayoutBlock.LayoutTableBlock',
            )
            list_block: 'Document.DocumentLayout.DocumentLayoutBlock.LayoutListBlock' = proto.Field(
                proto.MESSAGE,
                number=4,
                oneof='block',
                message='Document.DocumentLayout.DocumentLayoutBlock.LayoutListBlock',
            )
            block_id: str = proto.Field(
                proto.STRING,
                number=1,
            )
            page_span: 'Document.DocumentLayout.DocumentLayoutBlock.LayoutPageSpan' = proto.Field(
                proto.MESSAGE,
                number=5,
                message='Document.DocumentLayout.DocumentLayoutBlock.LayoutPageSpan',
            )

        blocks: MutableSequence['Document.DocumentLayout.DocumentLayoutBlock'] = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message='Document.DocumentLayout.DocumentLayoutBlock',
        )

    class ChunkedDocument(proto.Message):
        r"""Represents the chunks that the document is divided into.

        Attributes:
            chunks (MutableSequence[google.cloud.documentai_v1.types.Document.ChunkedDocument.Chunk]):
                List of chunks.
        """

        class Chunk(proto.Message):
            r"""Represents a chunk.

            Attributes:
                chunk_id (str):
                    ID of the chunk.
                source_block_ids (MutableSequence[str]):
                    Unused.
                content (str):
                    Text content of the chunk.
                page_span (google.cloud.documentai_v1.types.Document.ChunkedDocument.Chunk.ChunkPageSpan):
                    Page span of the chunk.
                page_headers (MutableSequence[google.cloud.documentai_v1.types.Document.ChunkedDocument.Chunk.ChunkPageHeader]):
                    Page headers associated with the chunk.
                page_footers (MutableSequence[google.cloud.documentai_v1.types.Document.ChunkedDocument.Chunk.ChunkPageFooter]):
                    Page footers associated with the chunk.
            """

            class ChunkPageSpan(proto.Message):
                r"""Represents where the chunk starts and ends in the document.

                Attributes:
                    page_start (int):
                        Page where chunk starts in the document.
                    page_end (int):
                        Page where chunk ends in the document.
                """

                page_start: int = proto.Field(
                    proto.INT32,
                    number=1,
                )
                page_end: int = proto.Field(
                    proto.INT32,
                    number=2,
                )

            class ChunkPageHeader(proto.Message):
                r"""Represents the page header associated with the chunk.

                Attributes:
                    text (str):
                        Header in text format.
                    page_span (google.cloud.documentai_v1.types.Document.ChunkedDocument.Chunk.ChunkPageSpan):
                        Page span of the header.
                """

                text: str = proto.Field(
                    proto.STRING,
                    number=1,
                )
                page_span: 'Document.ChunkedDocument.Chunk.ChunkPageSpan' = proto.Field(
                    proto.MESSAGE,
                    number=2,
                    message='Document.ChunkedDocument.Chunk.ChunkPageSpan',
                )

            class ChunkPageFooter(proto.Message):
                r"""Represents the page footer associated with the chunk.

                Attributes:
                    text (str):
                        Footer in text format.
                    page_span (google.cloud.documentai_v1.types.Document.ChunkedDocument.Chunk.ChunkPageSpan):
                        Page span of the footer.
                """

                text: str = proto.Field(
                    proto.STRING,
                    number=1,
                )
                page_span: 'Document.ChunkedDocument.Chunk.ChunkPageSpan' = proto.Field(
                    proto.MESSAGE,
                    number=2,
                    message='Document.ChunkedDocument.Chunk.ChunkPageSpan',
                )

            chunk_id: str = proto.Field(
                proto.STRING,
                number=1,
            )
            source_block_ids: MutableSequence[str] = proto.RepeatedField(
                proto.STRING,
                number=2,
            )
            content: str = proto.Field(
                proto.STRING,
                number=3,
            )
            page_span: 'Document.ChunkedDocument.Chunk.ChunkPageSpan' = proto.Field(
                proto.MESSAGE,
                number=4,
                message='Document.ChunkedDocument.Chunk.ChunkPageSpan',
            )
            page_headers: MutableSequence['Document.ChunkedDocument.Chunk.ChunkPageHeader'] = proto.RepeatedField(
                proto.MESSAGE,
                number=5,
                message='Document.ChunkedDocument.Chunk.ChunkPageHeader',
            )
            page_footers: MutableSequence['Document.ChunkedDocument.Chunk.ChunkPageFooter'] = proto.RepeatedField(
                proto.MESSAGE,
                number=6,
                message='Document.ChunkedDocument.Chunk.ChunkPageFooter',
            )

        chunks: MutableSequence['Document.ChunkedDocument.Chunk'] = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message='Document.ChunkedDocument.Chunk',
        )

    uri: str = proto.Field(
        proto.STRING,
        number=1,
        oneof='source',
    )
    content: bytes = proto.Field(
        proto.BYTES,
        number=2,
        oneof='source',
    )
    mime_type: str = proto.Field(
        proto.STRING,
        number=3,
    )
    text: str = proto.Field(
        proto.STRING,
        number=4,
    )
    text_styles: MutableSequence[Style] = proto.RepeatedField(
        proto.MESSAGE,
        number=5,
        message=Style,
    )
    pages: MutableSequence[Page] = proto.RepeatedField(
        proto.MESSAGE,
        number=6,
        message=Page,
    )
    entities: MutableSequence[Entity] = proto.RepeatedField(
        proto.MESSAGE,
        number=7,
        message=Entity,
    )
    entity_relations: MutableSequence[EntityRelation] = proto.RepeatedField(
        proto.MESSAGE,
        number=8,
        message=EntityRelation,
    )
    text_changes: MutableSequence[TextChange] = proto.RepeatedField(
        proto.MESSAGE,
        number=14,
        message=TextChange,
    )
    shard_info: ShardInfo = proto.Field(
        proto.MESSAGE,
        number=9,
        message=ShardInfo,
    )
    error: status_pb2.Status = proto.Field(
        proto.MESSAGE,
        number=10,
        message=status_pb2.Status,
    )
    revisions: MutableSequence[Revision] = proto.RepeatedField(
        proto.MESSAGE,
        number=13,
        message=Revision,
    )
    document_layout: DocumentLayout = proto.Field(
        proto.MESSAGE,
        number=17,
        message=DocumentLayout,
    )
    chunked_document: ChunkedDocument = proto.Field(
        proto.MESSAGE,
        number=18,
        message=ChunkedDocument,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
