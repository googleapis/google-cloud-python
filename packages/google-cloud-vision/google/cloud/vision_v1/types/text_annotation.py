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


from google.cloud.vision_v1.types import geometry


__protobuf__ = proto.module(
    package="google.cloud.vision.v1",
    manifest={"TextAnnotation", "Page", "Block", "Paragraph", "Word", "Symbol",},
)


class TextAnnotation(proto.Message):
    r"""TextAnnotation contains a structured representation of OCR extracted
    text. The hierarchy of an OCR extracted text structure is like this:
    TextAnnotation -> Page -> Block -> Paragraph -> Word -> Symbol Each
    structural component, starting from Page, may further have their own
    properties. Properties describe detected languages, breaks etc..
    Please refer to the
    [TextAnnotation.TextProperty][google.cloud.vision.v1.TextAnnotation.TextProperty]
    message definition below for more detail.

    Attributes:
        pages (Sequence[~.text_annotation.Page]):
            List of pages detected by OCR.
        text (str):
            UTF-8 text detected on the pages.
    """

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

        language_code = proto.Field(proto.STRING, number=1)

        confidence = proto.Field(proto.FLOAT, number=2)

    class DetectedBreak(proto.Message):
        r"""Detected start or end of a structural component.

        Attributes:
            type_ (~.text_annotation.TextAnnotation.DetectedBreak.BreakType):
                Detected break type.
            is_prefix (bool):
                True if break prepends the element.
        """

        class BreakType(proto.Enum):
            r"""Enum to denote the type of break found. New line, space etc."""
            UNKNOWN = 0
            SPACE = 1
            SURE_SPACE = 2
            EOL_SURE_SPACE = 3
            HYPHEN = 4
            LINE_BREAK = 5

        type_ = proto.Field(
            proto.ENUM, number=1, enum="TextAnnotation.DetectedBreak.BreakType",
        )

        is_prefix = proto.Field(proto.BOOL, number=2)

    class TextProperty(proto.Message):
        r"""Additional information detected on the structural component.

        Attributes:
            detected_languages (Sequence[~.text_annotation.TextAnnotation.DetectedLanguage]):
                A list of detected languages together with
                confidence.
            detected_break (~.text_annotation.TextAnnotation.DetectedBreak):
                Detected start or end of a text segment.
        """

        detected_languages = proto.RepeatedField(
            proto.MESSAGE, number=1, message="TextAnnotation.DetectedLanguage",
        )

        detected_break = proto.Field(
            proto.MESSAGE, number=2, message="TextAnnotation.DetectedBreak",
        )

    pages = proto.RepeatedField(proto.MESSAGE, number=1, message="Page",)

    text = proto.Field(proto.STRING, number=2)


class Page(proto.Message):
    r"""Detected page from OCR.

    Attributes:
        property (~.text_annotation.TextAnnotation.TextProperty):
            Additional information detected on the page.
        width (int):
            Page width. For PDFs the unit is points. For
            images (including TIFFs) the unit is pixels.
        height (int):
            Page height. For PDFs the unit is points. For
            images (including TIFFs) the unit is pixels.
        blocks (Sequence[~.text_annotation.Block]):
            List of blocks of text, images etc on this
            page.
        confidence (float):
            Confidence of the OCR results on the page. Range [0, 1].
    """

    property = proto.Field(
        proto.MESSAGE, number=1, message=TextAnnotation.TextProperty,
    )

    width = proto.Field(proto.INT32, number=2)

    height = proto.Field(proto.INT32, number=3)

    blocks = proto.RepeatedField(proto.MESSAGE, number=4, message="Block",)

    confidence = proto.Field(proto.FLOAT, number=5)


class Block(proto.Message):
    r"""Logical element on the page.

    Attributes:
        property (~.text_annotation.TextAnnotation.TextProperty):
            Additional information detected for the
            block.
        bounding_box (~.geometry.BoundingPoly):
            The bounding box for the block. The vertices are in the
            order of top-left, top-right, bottom-right, bottom-left.
            When a rotation of the bounding box is detected the rotation
            is represented as around the top-left corner as defined when
            the text is read in the 'natural' orientation. For example:

            -  when the text is horizontal it might look like:

               ::

                    0----1
                    |    |
                    3----2

            -  when it's rotated 180 degrees around the top-left corner
               it becomes:

               ::

                    2----3
                    |    |
                    1----0

               and the vertex order will still be (0, 1, 2, 3).
        paragraphs (Sequence[~.text_annotation.Paragraph]):
            List of paragraphs in this block (if this
            blocks is of type text).
        block_type (~.text_annotation.Block.BlockType):
            Detected block type (text, image etc) for
            this block.
        confidence (float):
            Confidence of the OCR results on the block. Range [0, 1].
    """

    class BlockType(proto.Enum):
        r"""Type of a block (text, image etc) as identified by OCR."""
        UNKNOWN = 0
        TEXT = 1
        TABLE = 2
        PICTURE = 3
        RULER = 4
        BARCODE = 5

    property = proto.Field(
        proto.MESSAGE, number=1, message=TextAnnotation.TextProperty,
    )

    bounding_box = proto.Field(proto.MESSAGE, number=2, message=geometry.BoundingPoly,)

    paragraphs = proto.RepeatedField(proto.MESSAGE, number=3, message="Paragraph",)

    block_type = proto.Field(proto.ENUM, number=4, enum=BlockType,)

    confidence = proto.Field(proto.FLOAT, number=5)


class Paragraph(proto.Message):
    r"""Structural unit of text representing a number of words in
    certain order.

    Attributes:
        property (~.text_annotation.TextAnnotation.TextProperty):
            Additional information detected for the
            paragraph.
        bounding_box (~.geometry.BoundingPoly):
            The bounding box for the paragraph. The vertices are in the
            order of top-left, top-right, bottom-right, bottom-left.
            When a rotation of the bounding box is detected the rotation
            is represented as around the top-left corner as defined when
            the text is read in the 'natural' orientation. For example:

            -  when the text is horizontal it might look like: 0----1 \|
               \| 3----2
            -  when it's rotated 180 degrees around the top-left corner
               it becomes: 2----3 \| \| 1----0 and the vertex order will
               still be (0, 1, 2, 3).
        words (Sequence[~.text_annotation.Word]):
            List of all words in this paragraph.
        confidence (float):
            Confidence of the OCR results for the paragraph. Range [0,
            1].
    """

    property = proto.Field(
        proto.MESSAGE, number=1, message=TextAnnotation.TextProperty,
    )

    bounding_box = proto.Field(proto.MESSAGE, number=2, message=geometry.BoundingPoly,)

    words = proto.RepeatedField(proto.MESSAGE, number=3, message="Word",)

    confidence = proto.Field(proto.FLOAT, number=4)


class Word(proto.Message):
    r"""A word representation.

    Attributes:
        property (~.text_annotation.TextAnnotation.TextProperty):
            Additional information detected for the word.
        bounding_box (~.geometry.BoundingPoly):
            The bounding box for the word. The vertices are in the order
            of top-left, top-right, bottom-right, bottom-left. When a
            rotation of the bounding box is detected the rotation is
            represented as around the top-left corner as defined when
            the text is read in the 'natural' orientation. For example:

            -  when the text is horizontal it might look like: 0----1 \|
               \| 3----2
            -  when it's rotated 180 degrees around the top-left corner
               it becomes: 2----3 \| \| 1----0 and the vertex order will
               still be (0, 1, 2, 3).
        symbols (Sequence[~.text_annotation.Symbol]):
            List of symbols in the word.
            The order of the symbols follows the natural
            reading order.
        confidence (float):
            Confidence of the OCR results for the word. Range [0, 1].
    """

    property = proto.Field(
        proto.MESSAGE, number=1, message=TextAnnotation.TextProperty,
    )

    bounding_box = proto.Field(proto.MESSAGE, number=2, message=geometry.BoundingPoly,)

    symbols = proto.RepeatedField(proto.MESSAGE, number=3, message="Symbol",)

    confidence = proto.Field(proto.FLOAT, number=4)


class Symbol(proto.Message):
    r"""A single symbol representation.

    Attributes:
        property (~.text_annotation.TextAnnotation.TextProperty):
            Additional information detected for the
            symbol.
        bounding_box (~.geometry.BoundingPoly):
            The bounding box for the symbol. The vertices are in the
            order of top-left, top-right, bottom-right, bottom-left.
            When a rotation of the bounding box is detected the rotation
            is represented as around the top-left corner as defined when
            the text is read in the 'natural' orientation. For example:

            -  when the text is horizontal it might look like: 0----1 \|
               \| 3----2
            -  when it's rotated 180 degrees around the top-left corner
               it becomes: 2----3 \| \| 1----0 and the vertex order will
               still be (0, 1, 2, 3).
        text (str):
            The actual UTF-8 representation of the
            symbol.
        confidence (float):
            Confidence of the OCR results for the symbol. Range [0, 1].
    """

    property = proto.Field(
        proto.MESSAGE, number=1, message=TextAnnotation.TextProperty,
    )

    bounding_box = proto.Field(proto.MESSAGE, number=2, message=geometry.BoundingPoly,)

    text = proto.Field(proto.STRING, number=3)

    confidence = proto.Field(proto.FLOAT, number=4)


__all__ = tuple(sorted(__protobuf__.manifest))
