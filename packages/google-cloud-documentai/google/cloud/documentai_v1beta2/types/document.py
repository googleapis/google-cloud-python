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

from google.cloud.documentai_v1beta2.types import geometry
from google.rpc import status_pb2  # type: ignore
from google.type import color_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.documentai.v1beta2", manifest={"Document",},
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
            Currently supports Google Cloud Storage URI of the form
            ``gs://bucket_name/object_name``. Object versioning is not
            supported. See `Google Cloud Storage Request
            URIs <https://cloud.google.com/storage/docs/reference-uris>`__
            for more info.

            This field is a member of `oneof`_ ``source``.
        content (bytes):
            Inline document content, represented as a stream of bytes.
            Note: As with all ``bytes`` fields, protobuffers use a pure
            binary representation, whereas JSON representations use
            base64.

            This field is a member of `oneof`_ ``source``.
        mime_type (str):
            An IANA published MIME type (also referred to
            as media type). For more information, see
            https://www.iana.org/assignments/media-
            types/media-types.xhtml.
        text (str):
            UTF-8 encoded text in reading order from the
            document.
        text_styles (Sequence[google.cloud.documentai_v1beta2.types.Document.Style]):
            Styles for the
            [Document.text][google.cloud.documentai.v1beta2.Document.text].
        pages (Sequence[google.cloud.documentai_v1beta2.types.Document.Page]):
            Visual page layout for the
            [Document][google.cloud.documentai.v1beta2.Document].
        entities (Sequence[google.cloud.documentai_v1beta2.types.Document.Entity]):
            A list of entities detected on
            [Document.text][google.cloud.documentai.v1beta2.Document.text].
            For document shards, entities in this list may cross shard
            boundaries.
        entity_relations (Sequence[google.cloud.documentai_v1beta2.types.Document.EntityRelation]):
            Relationship among
            [Document.entities][google.cloud.documentai.v1beta2.Document.entities].
        shard_info (google.cloud.documentai_v1beta2.types.Document.ShardInfo):
            Information about the sharding if this
            document is sharded part of a larger document.
            If the document is not sharded, this message is
            not specified.
        labels (Sequence[google.cloud.documentai_v1beta2.types.Document.Label]):
            [Label][google.cloud.documentai.v1beta2.Document.Label]s for
            this document.
        error (google.rpc.status_pb2.Status):
            Any error that occurred while processing this
            document.
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
                [Document.text][google.cloud.documentai.v1beta2.Document.text]
                in the overall document global text.
        """

        shard_index = proto.Field(proto.INT64, number=1,)
        shard_count = proto.Field(proto.INT64, number=2,)
        text_offset = proto.Field(proto.INT64, number=3,)

    class Label(proto.Message):
        r"""Label attaches schema information and/or other metadata to segments
        within a [Document][google.cloud.documentai.v1beta2.Document].
        Multiple [Label][google.cloud.documentai.v1beta2.Document.Label]s on
        a single field can denote either different labels, different
        instances of the same label created at different times, or some
        combination of both.


        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            automl_model (str):
                Label is generated AutoML model. This field stores the full
                resource name of the AutoML model.

                Format:
                ``projects/{project-id}/locations/{location-id}/models/{model-id}``

                This field is a member of `oneof`_ ``source``.
            name (str):
                Name of the label.
                When the label is generated from AutoML Text
                Classification model, this field represents the
                name of the category.
            confidence (float):
                Confidence score between 0 and 1 for label
                assignment.
        """

        automl_model = proto.Field(proto.STRING, number=2, oneof="source",)
        name = proto.Field(proto.STRING, number=1,)
        confidence = proto.Field(proto.FLOAT, number=3,)

    class Style(proto.Message):
        r"""Annotation for common text style attributes. This adheres to
        CSS conventions as much as possible.

        Attributes:
            text_anchor (google.cloud.documentai_v1beta2.types.Document.TextAnchor):
                Text anchor indexing into the
                [Document.text][google.cloud.documentai.v1beta2.Document.text].
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
            font_size (google.cloud.documentai_v1beta2.types.Document.Style.FontSize):
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
        r"""A page in a [Document][google.cloud.documentai.v1beta2.Document].

        Attributes:
            page_number (int):
                1-based index for current
                [Page][google.cloud.documentai.v1beta2.Document.Page] in a
                parent [Document][google.cloud.documentai.v1beta2.Document].
                Useful when a page is taken out of a
                [Document][google.cloud.documentai.v1beta2.Document] for
                individual processing.
            dimension (google.cloud.documentai_v1beta2.types.Document.Page.Dimension):
                Physical dimension of the page.
            layout (google.cloud.documentai_v1beta2.types.Document.Page.Layout):
                [Layout][google.cloud.documentai.v1beta2.Document.Page.Layout]
                for the page.
            detected_languages (Sequence[google.cloud.documentai_v1beta2.types.Document.Page.DetectedLanguage]):
                A list of detected languages together with
                confidence.
            blocks (Sequence[google.cloud.documentai_v1beta2.types.Document.Page.Block]):
                A list of visually detected text blocks on
                the page. A block has a set of lines (collected
                into paragraphs) that have a common line-spacing
                and orientation.
            paragraphs (Sequence[google.cloud.documentai_v1beta2.types.Document.Page.Paragraph]):
                A list of visually detected text paragraphs
                on the page. A collection of lines that a human
                would perceive as a paragraph.
            lines (Sequence[google.cloud.documentai_v1beta2.types.Document.Page.Line]):
                A list of visually detected text lines on the
                page. A collection of tokens that a human would
                perceive as a line.
            tokens (Sequence[google.cloud.documentai_v1beta2.types.Document.Page.Token]):
                A list of visually detected tokens on the
                page.
            visual_elements (Sequence[google.cloud.documentai_v1beta2.types.Document.Page.VisualElement]):
                A list of detected non-text visual elements
                e.g. checkbox, signature etc. on the page.
            tables (Sequence[google.cloud.documentai_v1beta2.types.Document.Page.Table]):
                A list of visually detected tables on the
                page.
            form_fields (Sequence[google.cloud.documentai_v1beta2.types.Document.Page.FormField]):
                A list of visually detected form fields on
                the page.
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

        class Layout(proto.Message):
            r"""Visual element describing a layout unit on a page.

            Attributes:
                text_anchor (google.cloud.documentai_v1beta2.types.Document.TextAnchor):
                    Text anchor indexing into the
                    [Document.text][google.cloud.documentai.v1beta2.Document.text].
                confidence (float):
                    Confidence of the current
                    [Layout][google.cloud.documentai.v1beta2.Document.Page.Layout]
                    within context of the object this layout is for. e.g.
                    confidence can be for a single token, a table, a visual
                    element, etc. depending on context. Range [0, 1].
                bounding_poly (google.cloud.documentai_v1beta2.types.BoundingPoly):
                    The bounding polygon for the
                    [Layout][google.cloud.documentai.v1beta2.Document.Page.Layout].
                orientation (google.cloud.documentai_v1beta2.types.Document.Page.Layout.Orientation):
                    Detected orientation for the
                    [Layout][google.cloud.documentai.v1beta2.Document.Page.Layout].
                id (str):
                    Optional. This is the identifier used by referencing
                    [PageAnchor][google.cloud.documentai.v1beta2.Document.PageAnchor]s.
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
            id = proto.Field(proto.STRING, number=5,)

        class Block(proto.Message):
            r"""A block has a set of lines (collected into paragraphs) that
            have a common line-spacing and orientation.

            Attributes:
                layout (google.cloud.documentai_v1beta2.types.Document.Page.Layout):
                    [Layout][google.cloud.documentai.v1beta2.Document.Page.Layout]
                    for
                    [Block][google.cloud.documentai.v1beta2.Document.Page.Block].
                detected_languages (Sequence[google.cloud.documentai_v1beta2.types.Document.Page.DetectedLanguage]):
                    A list of detected languages together with
                    confidence.
            """

            layout = proto.Field(
                proto.MESSAGE, number=1, message="Document.Page.Layout",
            )
            detected_languages = proto.RepeatedField(
                proto.MESSAGE, number=2, message="Document.Page.DetectedLanguage",
            )

        class Paragraph(proto.Message):
            r"""A collection of lines that a human would perceive as a
            paragraph.

            Attributes:
                layout (google.cloud.documentai_v1beta2.types.Document.Page.Layout):
                    [Layout][google.cloud.documentai.v1beta2.Document.Page.Layout]
                    for
                    [Paragraph][google.cloud.documentai.v1beta2.Document.Page.Paragraph].
                detected_languages (Sequence[google.cloud.documentai_v1beta2.types.Document.Page.DetectedLanguage]):
                    A list of detected languages together with
                    confidence.
            """

            layout = proto.Field(
                proto.MESSAGE, number=1, message="Document.Page.Layout",
            )
            detected_languages = proto.RepeatedField(
                proto.MESSAGE, number=2, message="Document.Page.DetectedLanguage",
            )

        class Line(proto.Message):
            r"""A collection of tokens that a human would perceive as a line.
            Does not cross column boundaries, can be horizontal, vertical,
            etc.

            Attributes:
                layout (google.cloud.documentai_v1beta2.types.Document.Page.Layout):
                    [Layout][google.cloud.documentai.v1beta2.Document.Page.Layout]
                    for
                    [Line][google.cloud.documentai.v1beta2.Document.Page.Line].
                detected_languages (Sequence[google.cloud.documentai_v1beta2.types.Document.Page.DetectedLanguage]):
                    A list of detected languages together with
                    confidence.
            """

            layout = proto.Field(
                proto.MESSAGE, number=1, message="Document.Page.Layout",
            )
            detected_languages = proto.RepeatedField(
                proto.MESSAGE, number=2, message="Document.Page.DetectedLanguage",
            )

        class Token(proto.Message):
            r"""A detected token.

            Attributes:
                layout (google.cloud.documentai_v1beta2.types.Document.Page.Layout):
                    [Layout][google.cloud.documentai.v1beta2.Document.Page.Layout]
                    for
                    [Token][google.cloud.documentai.v1beta2.Document.Page.Token].
                detected_break (google.cloud.documentai_v1beta2.types.Document.Page.Token.DetectedBreak):
                    Detected break at the end of a
                    [Token][google.cloud.documentai.v1beta2.Document.Page.Token].
                detected_languages (Sequence[google.cloud.documentai_v1beta2.types.Document.Page.DetectedLanguage]):
                    A list of detected languages together with
                    confidence.
            """

            class DetectedBreak(proto.Message):
                r"""Detected break at the end of a
                [Token][google.cloud.documentai.v1beta2.Document.Page.Token].

                Attributes:
                    type_ (google.cloud.documentai_v1beta2.types.Document.Page.Token.DetectedBreak.Type):
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

        class VisualElement(proto.Message):
            r"""Detected non-text visual elements e.g. checkbox, signature
            etc. on the page.

            Attributes:
                layout (google.cloud.documentai_v1beta2.types.Document.Page.Layout):
                    [Layout][google.cloud.documentai.v1beta2.Document.Page.Layout]
                    for
                    [VisualElement][google.cloud.documentai.v1beta2.Document.Page.VisualElement].
                type_ (str):
                    Type of the
                    [VisualElement][google.cloud.documentai.v1beta2.Document.Page.VisualElement].
                detected_languages (Sequence[google.cloud.documentai_v1beta2.types.Document.Page.DetectedLanguage]):
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
                layout (google.cloud.documentai_v1beta2.types.Document.Page.Layout):
                    [Layout][google.cloud.documentai.v1beta2.Document.Page.Layout]
                    for
                    [Table][google.cloud.documentai.v1beta2.Document.Page.Table].
                header_rows (Sequence[google.cloud.documentai_v1beta2.types.Document.Page.Table.TableRow]):
                    Header rows of the table.
                body_rows (Sequence[google.cloud.documentai_v1beta2.types.Document.Page.Table.TableRow]):
                    Body rows of the table.
                detected_languages (Sequence[google.cloud.documentai_v1beta2.types.Document.Page.DetectedLanguage]):
                    A list of detected languages together with
                    confidence.
            """

            class TableRow(proto.Message):
                r"""A row of table cells.

                Attributes:
                    cells (Sequence[google.cloud.documentai_v1beta2.types.Document.Page.Table.TableCell]):
                        Cells that make up this row.
                """

                cells = proto.RepeatedField(
                    proto.MESSAGE, number=1, message="Document.Page.Table.TableCell",
                )

            class TableCell(proto.Message):
                r"""A cell representation inside the table.

                Attributes:
                    layout (google.cloud.documentai_v1beta2.types.Document.Page.Layout):
                        [Layout][google.cloud.documentai.v1beta2.Document.Page.Layout]
                        for
                        [TableCell][google.cloud.documentai.v1beta2.Document.Page.Table.TableCell].
                    row_span (int):
                        How many rows this cell spans.
                    col_span (int):
                        How many columns this cell spans.
                    detected_languages (Sequence[google.cloud.documentai_v1beta2.types.Document.Page.DetectedLanguage]):
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
                field_name (google.cloud.documentai_v1beta2.types.Document.Page.Layout):
                    [Layout][google.cloud.documentai.v1beta2.Document.Page.Layout]
                    for the
                    [FormField][google.cloud.documentai.v1beta2.Document.Page.FormField]
                    name. e.g. ``Address``, ``Email``, ``Grand total``,
                    ``Phone number``, etc.
                field_value (google.cloud.documentai_v1beta2.types.Document.Page.Layout):
                    [Layout][google.cloud.documentai.v1beta2.Document.Page.Layout]
                    for the
                    [FormField][google.cloud.documentai.v1beta2.Document.Page.FormField]
                    value.
                name_detected_languages (Sequence[google.cloud.documentai_v1beta2.types.Document.Page.DetectedLanguage]):
                    A list of detected languages for name
                    together with confidence.
                value_detected_languages (Sequence[google.cloud.documentai_v1beta2.types.Document.Page.DetectedLanguage]):
                    A list of detected languages for value
                    together with confidence.
                value_type (str):
                    If the value is non-textual, this field represents the type.
                    Current valid values are:

                    -  blank (this indicates the field_value is normal text)
                    -  "unfilled_checkbox"
                    -  "filled_checkbox".
                corrected_key_text (str):
                    An internal field, created for Labeling UI to
                    export key text.
                corrected_value_text (str):
                    An internal field, created for Labeling UI to
                    export value text.
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
            corrected_key_text = proto.Field(proto.STRING, number=6,)
            corrected_value_text = proto.Field(proto.STRING, number=7,)

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

    class Entity(proto.Message):
        r"""A phrase in the text that is a known entity type, such as a
        person, an organization, or location.

        Attributes:
            text_anchor (google.cloud.documentai_v1beta2.types.Document.TextAnchor):
                Provenance of the entity. Text anchor indexing into the
                [Document.text][google.cloud.documentai.v1beta2.Document.text].
            type_ (str):
                Entity type from a schema e.g. ``Address``.
            mention_text (str):
                Text value in the document e.g. ``1600 Amphitheatre Pkwy``.
            mention_id (str):
                Deprecated. Use ``id`` field instead.
            confidence (float):
                Optional. Confidence of detected Schema entity. Range [0,
                1].
            page_anchor (google.cloud.documentai_v1beta2.types.Document.PageAnchor):
                Optional. Represents the provenance of this
                entity wrt. the location on the page where it
                was found.
            id (str):
                Optional. Canonical id. This will be a unique
                value in the entity list for this document.
            bounding_poly_for_demo_frontend (google.cloud.documentai_v1beta2.types.BoundingPoly):
                Optional. Temporary field to store the
                bounding poly for short-term POCs. Used by the
                frontend only. Do not use before you talk to
                ybo@ and lukasr@.
        """

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
        bounding_poly_for_demo_frontend = proto.Field(
            proto.MESSAGE, number=8, message=geometry.BoundingPoly,
        )

    class EntityRelation(proto.Message):
        r"""Relationship between
        [Entities][google.cloud.documentai.v1beta2.Document.Entity].

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
        [Document.text][google.cloud.documentai.v1beta2.Document.text].

        Attributes:
            text_segments (Sequence[google.cloud.documentai_v1beta2.types.Document.TextAnchor.TextSegment]):
                The text segments from the
                [Document.text][google.cloud.documentai.v1beta2.Document.text].
        """

        class TextSegment(proto.Message):
            r"""A text segment in the
            [Document.text][google.cloud.documentai.v1beta2.Document.text]. The
            indices may be out of bounds which indicate that the text extends
            into another document shard for large sharded documents. See
            [ShardInfo.text_offset][google.cloud.documentai.v1beta2.Document.ShardInfo.text_offset]

            Attributes:
                start_index (int):
                    [TextSegment][google.cloud.documentai.v1beta2.Document.TextAnchor.TextSegment]
                    start UTF-8 char index in the
                    [Document.text][google.cloud.documentai.v1beta2.Document.text].
                end_index (int):
                    [TextSegment][google.cloud.documentai.v1beta2.Document.TextAnchor.TextSegment]
                    half open end UTF-8 char index in the
                    [Document.text][google.cloud.documentai.v1beta2.Document.text].
            """

            start_index = proto.Field(proto.INT64, number=1,)
            end_index = proto.Field(proto.INT64, number=2,)

        text_segments = proto.RepeatedField(
            proto.MESSAGE, number=1, message="Document.TextAnchor.TextSegment",
        )

    class PageAnchor(proto.Message):
        r"""Referencing elements in
        [Document.pages][google.cloud.documentai.v1beta2.Document.pages].

        Attributes:
            page_refs (Sequence[google.cloud.documentai_v1beta2.types.Document.PageAnchor.PageRef]):
                One or more references to visual page
                elements
        """

        class PageRef(proto.Message):
            r"""Represents a weak reference to a page element within a
            document.

            Attributes:
                page (int):
                    Required. Index into the
                    [Document.pages][google.cloud.documentai.v1beta2.Document.pages]
                    element
                layout_type (google.cloud.documentai_v1beta2.types.Document.PageAnchor.PageRef.LayoutType):
                    Optional. The type of the layout element that
                    is being referenced.  If not specified the whole
                    page is assumed to be referenced.
                layout_id (str):
                    Optional. The
                    [Page.Layout.id][google.cloud.documentai.v1beta2.Document.Page.Layout.id]
                    on the page that this element references. If
                    [LayoutRef.type][] is specified this id must also be
                    specified.
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

        page_refs = proto.RepeatedField(
            proto.MESSAGE, number=1, message="Document.PageAnchor.PageRef",
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
    shard_info = proto.Field(proto.MESSAGE, number=9, message=ShardInfo,)
    labels = proto.RepeatedField(proto.MESSAGE, number=11, message=Label,)
    error = proto.Field(proto.MESSAGE, number=10, message=status_pb2.Status,)


__all__ = tuple(sorted(__protobuf__.manifest))
