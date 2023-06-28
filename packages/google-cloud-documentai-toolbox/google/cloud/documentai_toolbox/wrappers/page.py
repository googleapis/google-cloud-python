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
"""Wrappers for Document AI Page type."""

import dataclasses
import html
from typing import List, Optional, Tuple, Union

from google.cloud.documentai_toolbox.constants import ElementWithLayout

from google.cloud import documentai
import pandas as pd

ChildrenElements = Union[
    List["Paragraph"],
    List["Block"],
    List["Token"],
    List["Line"],
]


@dataclasses.dataclass
class Table:
    """Represents a wrapped documentai.Document.Page.Table.

    Attributes:
        documentai_object (google.cloud.documentai.Document.Page.Table):
            Required. The original google.cloud.documentai.Document.Page.Table object.
        document_text (str):
            Required. UTF-8 encoded text in reading order from the document.
        body_rows (List[List[str]]):
            Required. A list of body rows.
        header_rows (List[List[str]]):
            Required. A list of header rows.
    """

    documentai_object: documentai.Document.Page.Table = dataclasses.field(repr=False)
    document_text: dataclasses.InitVar[str]

    body_rows: List[List[str]] = dataclasses.field(init=False, repr=False)
    header_rows: List[List[str]] = dataclasses.field(init=False, repr=False)

    def __post_init__(self, document_text) -> None:
        self.header_rows = _table_rows_from_documentai_table_rows(
            table_rows=list(self.documentai_object.header_rows), text=document_text
        )
        self.body_rows = _table_rows_from_documentai_table_rows(
            table_rows=list(self.documentai_object.body_rows), text=document_text
        )

    def to_dataframe(self) -> pd.DataFrame:
        r"""Returns pd.DataFrame from documentai.table

        Returns:
            pd.DataFrame:
                The DataFrame of the table.

        """
        if not self.body_rows:
            return pd.DataFrame(columns=self.header_rows)

        dataframe = pd.DataFrame(self.body_rows)
        if self.header_rows:
            dataframe.columns = self.header_rows
        else:
            dataframe.columns = [None] * len(self.body_rows[0])

        return dataframe

    def to_csv(self) -> str:
        r"""Returns a csv str.

            .. code-block:: python

                from google.cloud.documentai_toolbox import Document

                def sample_table_to_csv():

                    #Wrap document from gcs_path
                    merged_document = Document('gs://abc/def/gh/1')

                    #Use first page
                    page = merged_document.pages[0]

                    #export the first table in page 1 to csv
                    csv_text = page.tables[0].to_csv()

                    print(csv_text)

        Args:
            dataframe (pd.Dataframe):
                Required. Two-dimensional, size-mutable, potentially heterogeneous tabular data.

        Returns:
            str:
                The table in csv format.

        """
        return self.to_dataframe().to_csv(index=False)


@dataclasses.dataclass
class Token:
    """Represents a wrapped documentai.Document.Page.
    .

    Attributes:
        documentai_object (google.cloud.documentai.Document.Page.Token):
            Required. The original google.cloud.documentai.Document.Page.Token object.
        _page (Page):
                    Required. The Page object.
    """

    documentai_object: documentai.Document.Page.Token = dataclasses.field(default=None)
    _page: "Page" = dataclasses.field(default=None)

    _text: Optional[str] = dataclasses.field(init=False, default=None)
    _hocr_bounding_box: Optional[str] = dataclasses.field(init=False, default=None)

    @property
    def text(self):
        if self._text is None:
            self._text = _text_from_layout(
                layout=self.documentai_object.layout, text=self._page.text
            )
        return self._text

    @property
    def hocr_bounding_box(self):
        if self._hocr_bounding_box is None:
            self._hocr_bounding_box = _get_hocr_bounding_box(
                element_with_layout=self.documentai_object,
                dimension=self._page.documentai_object.dimension,
            )
        return self._hocr_bounding_box


@dataclasses.dataclass
class Line:
    """Represents a wrapped documentai.Document.Page.Line.

    Attributes:
        documentai_object (google.cloud.documentai.Document.Page.Line):
            Required. The original google.cloud.documentai.Document.Page.Line object.
        _page (Page):
            Required. The Page object.
    """

    documentai_object: documentai.Document.Page.Line = dataclasses.field(repr=False)
    _page: "Page" = dataclasses.field(repr=False)

    tokens: List[Token] = dataclasses.field(
        init=False, repr=False, default_factory=list
    )
    _text: Optional[str] = dataclasses.field(init=False, default=None)
    _hocr_bounding_box: Optional[str] = dataclasses.field(init=False, default=None)

    def __post_init__(self):
        self.tokens = _get_children_of_element(
            self.documentai_object, self._page.tokens
        )

    @property
    def text(self):
        if self._text is None:
            self._text = _text_from_layout(
                layout=self.documentai_object.layout, text=self._page.text
            )
        return self._text

    @property
    def hocr_bounding_box(self):
        if self._hocr_bounding_box is None:
            self._hocr_bounding_box = _get_hocr_bounding_box(
                element_with_layout=self.documentai_object,
                dimension=self._page.documentai_object.dimension,
            )
        return self._hocr_bounding_box


@dataclasses.dataclass
class FormField:
    """Represents a wrapped documentai.Document.Page.FormField.

    Attributes:
        documentai_object (google.cloud.documentai.Document.Page.FormField):
            Required. The original google.cloud.documentai.Document.Page.FormField object.
        document_text (str):
            Required. UTF-8 encoded text in reading order from the document.
        field_name (str):
            Required. The form field name
        field_value (str):
            Required. The form field value
    """

    documentai_object: documentai.Document.Page.FormField
    document_text: dataclasses.InitVar[str]

    field_name: str = dataclasses.field(init=False)
    field_value: str = dataclasses.field(init=False)

    def __post_init__(self, document_text) -> None:
        self.field_name = _trim_text(
            _text_from_layout(self.documentai_object.field_name, document_text)
        )
        self.field_value = _trim_text(
            _text_from_layout(self.documentai_object.field_value, document_text)
        )


@dataclasses.dataclass
class Paragraph:
    """Represents a wrapped documentai.Document.Page.Paragraph.

    Attributes:
        documentai_object (google.cloud.documentai.Document.Page.Paragraph):
            Required. The original google.cloud.documentai.Document.Page.Paragraph object.
        _page (Page):
            Required. The Page object.
    """

    documentai_object: documentai.Document.Page.Paragraph = dataclasses.field(
        repr=False
    )
    _page: "Page" = dataclasses.field(repr=False)

    lines: List[Line] = dataclasses.field(init=False, repr=False)
    _text: Optional[str] = dataclasses.field(init=False, default=None)
    _hocr_bounding_box: Optional[str] = dataclasses.field(init=False, default=None)

    def __post_init__(self):
        self.lines = _get_children_of_element(self.documentai_object, self._page.lines)

    @property
    def text(self):
        if self._text is None:
            self._text = _text_from_layout(
                layout=self.documentai_object.layout, text=self._page.text
            )
        return self._text

    @property
    def hocr_bounding_box(self):
        if self._hocr_bounding_box is None:
            self._hocr_bounding_box = _get_hocr_bounding_box(
                element_with_layout=self.documentai_object,
                dimension=self._page.documentai_object.dimension,
            )
        return self._hocr_bounding_box


@dataclasses.dataclass
class Block:
    """Represents a wrapped documentai.Document.Page.Block.

    Attributes:
        documentai_object (google.cloud.documentai.Document.Page.Block):
            Required. The original google.cloud.documentai.Document.Page.Block object.
        _page (Page):
            Required. The Page object.
    """

    documentai_object: documentai.Document.Page.Block = dataclasses.field(repr=False)
    _page: "Page" = dataclasses.field(repr=False)

    paragraphs: List[Paragraph] = dataclasses.field(init=False, repr=False)
    _text: Optional[str] = dataclasses.field(init=False, default=None)
    _hocr_bounding_box: Optional[str] = dataclasses.field(init=False, default=None)

    def __post_init__(self):
        self.paragraphs = _get_children_of_element(
            self.documentai_object, self._page.paragraphs
        )

    @property
    def text(self):
        if self._text is None:
            self._text = _text_from_layout(
                layout=self.documentai_object.layout, text=self._page.text
            )
        return self._text

    @property
    def hocr_bounding_box(self):
        if self._hocr_bounding_box is None:
            self._hocr_bounding_box = _get_hocr_bounding_box(
                element_with_layout=self.documentai_object,
                dimension=self._page.documentai_object.dimension,
            )
        return self._hocr_bounding_box


def _table_rows_from_documentai_table_rows(
    table_rows: List[documentai.Document.Page.Table.TableRow], text: str
) -> List[List[str]]:
    r"""Returns a list of rows from table_rows.

    Args:
        table_rows (List[documentai.Document.Page.Table.TableRow]):
            Required. A documentai.Document.Page.Table.TableRow.
        text (str):
            Required. UTF-8 encoded text in reading order
            from the document.

    Returns:
        List[List[str]]:
            A list of table rows.
    """
    body_rows: List[List[str]] = []
    for row in table_rows:
        row_text = []

        for cell in row.cells:
            row_text.append(
                _text_from_layout(layout=cell.layout, text=text).replace("\n", "")
            )

        body_rows.append(row_text)
    return body_rows


def _get_xy(
    element: ElementWithLayout,
    dimension: documentai.Document.Page.Dimension,
    normalized: bool = False,
    min: bool = False,
) -> Tuple[int, int]:
    r"""Returns hocr xy coordinates corresponding to elements bounding box.

    Args:
        element (ElementWithLayout):
            Required. an element with layout fields.
        dimension (documentai.Document.Page.Dimension):
            Required. Page dimension.
        normalized (Boolean):
            Required. Wether element.layout.bounding_poly is normalized
        min (Boolean):
            Required. Wether xy should be min

    Returns:
        Tuple[int, int]:
            hocr xy coordinates corresponding to elements bounding box.
    """
    index = 0 if min else 2
    if not normalized:
        return (
            element.layout.bounding_poly.vertices[index].x,
            element.layout.bounding_poly.vertices[index].y,
        )
    return (
        element.layout.bounding_poly.vertices[index].x * dimension.width,
        element.layout.bounding_poly.vertices[index].y * dimension.height,
    )


def _get_hocr_bounding_box(
    element_with_layout: ElementWithLayout,
    dimension: documentai.Document.Page.Dimension,
) -> str:
    r"""Returns a hOCR bounding box string.

    Args:
        element_with_layout (ElementWithLayout):
            Required. an element with layout fields.
        dimension (documentai.Document.Page.Dimension):
            Required. Page dimension.

    Returns:
        str:
            hOCR bounding box sring.
    """

    if element_with_layout.layout.bounding_poly.vertices:
        min_x, min_y = _get_xy(element_with_layout, dimension, False, True)
        max_x, max_y = _get_xy(element_with_layout, dimension, False, False)
    else:
        min_x, min_y = _get_xy(element_with_layout, dimension, True, True)
        max_x, max_y = _get_xy(element_with_layout, dimension, True, False)

    return f"bbox {min_x} {min_y} {max_x} {max_y}"


def _text_from_layout(layout: documentai.Document.Page.Layout, text: str) -> str:
    r"""Returns a text from a single layout element.

    Args:
        layout (documentai.Document.Page.Layout):
            Required. an element with layout fields.
        text (str):
            Required. UTF-8 encoded text in reading order
            from the document.

    Returns:
        str:
            Text from a single element.
    """

    result_text = ""

    for text_segment in layout.text_anchor.text_segments:
        result_text += text[int(text_segment.start_index) : int(text_segment.end_index)]

    return result_text


def _get_children_of_element(element: ElementWithLayout, children: ChildrenElements):
    r"""Returns a list of children inside element.

    Args:
        element (ElementWithLayout):
            Required. A element in a page.
        children (ChildrenElements):
            Required. List of wrapped children.

    Returns:
        List[ChildrenElements]:
            A list of wrapped children that are inside a element.
    """
    start_index = element.layout.text_anchor.text_segments[0].start_index
    end_index = element.layout.text_anchor.text_segments[0].end_index

    return [
        child
        for child in children
        if child.documentai_object.layout.text_anchor.text_segments[0].start_index
        >= start_index
        if child.documentai_object.layout.text_anchor.text_segments[0].end_index
        <= end_index
    ]


def _get_blocks(
    blocks: List[documentai.Document.Page.Block], page: "Page"
) -> List[Block]:
    r"""Returns a list of wrapped Blocks.

    Args:
        blocks (List[documentai.Document.Page.Block]):
            Required. A list of documentai.Document.Page.Block objects.
        page (Page):
            Required. The Page object.

    Returns:
        List[Block]:
             A list of wrapped Blocks.
    """
    result = []

    for block in blocks:
        result.append(
            Block(
                documentai_object=block,
                _page=page,
            )
        )

    return result


def _get_paragraphs(
    paragraphs: List[documentai.Document.Page.Paragraph],
    page: "Page",
) -> List[Paragraph]:
    r"""Returns a list of wrapped Paragraphs.

    Args:
        paragraphs (List[documentai.Document.Page.Paragraph]):
            Required. A list of documentai.Document.Page.Paragraph objects.
        page (Page):
            Required. The Page object.

    Returns:
        List[Paragraph]:
             A list of wrapped Paragraphs.
    """
    result = []

    for paragraph in paragraphs:
        result.append(
            Paragraph(
                documentai_object=paragraph,
                _page=page,
            )
        )

    return result


def _get_tokens(
    tokens: List[documentai.Document.Page.Token], page: "Page"
) -> List[Token]:
    r"""Returns a list of wrapped tokens.

    Args:
        tokens (List[documentai.Document.Page.Token]):
            Required. A list of documentai.Document.Page.Token.
        page (Page):
            Required. The Page object.

    Returns:
        List[Token]:
            A list of wrapped tokens.
    """
    result = []

    for token in tokens:
        result.append(
            Token(
                documentai_object=token,
                _page=page,
            )
        )

    return result


def _get_lines(lines: List[documentai.Document.Page.Line], page: "Page") -> List[Line]:
    r"""Returns a list of wrapped lines.

    Args:
        lines (List[documentai.Document.Page.Line]):
            Required. A list of documentai.Document.Page.Line objects.
        page (Page):
            Required. The Page object.

    Returns:
        List[Line]:
            A list of wrapped Lines.
    """

    result = []

    for line in lines:
        result.append(
            Line(
                documentai_object=line,
                _page=page,
            )
        )

    return result


def _trim_text(text: str) -> str:
    r"""Remove extra space characters from text (blank, newline, tab, etc.)

    Args:
        text (str):
            Required. UTF-8 encoded text in reading order
            from the document.
    Returns:
        str:
            Text without trailing spaces/newlines
    """
    return text.strip().replace("\n", " ")


@dataclasses.dataclass
class Page:
    """Represents a wrapped documentai.Document.Page .

    Attributes:
        documentai_object (google.cloud.documentai.Document.Page):
            Required. The original google.cloud.documentai.Document.Page object.
        document_text (str):
            Required. The full text of the `Document` containing the `Page`.
        text (str):
            Required. UTF-8 encoded text of the page.
        page_number (int):
            Required. The page number of the `Page`.
        form_fields (List[FormField]):
            Required. A list of visually detected form fields on the
            page.
        lines (List[Line]):
            Required. A list of visually detected text lines on the
            page. A collection of tokens that a human would
            perceive as a line.
        paragraphs (List[Paragraph]):
            Required. A list of visually detected text paragraphs
            on the page. A collection of lines that a human
            would perceive as a paragraph.
        blocks (List[Block]):
            Required. A list of visually detected text blocks
            on the page. A collection of lines that a human
            would perceive as a block.
        tables (List[Table]):
            Required. A list of visually detected tables on the
            page.
    """

    documentai_object: documentai.Document.Page = dataclasses.field(repr=False)
    document_text: str = dataclasses.field(repr=False)

    text: str = dataclasses.field(init=False, repr=False)
    page_number: int = dataclasses.field(init=False, repr=False)
    form_fields: List[FormField] = dataclasses.field(init=False, repr=False)
    lines: List[Line] = dataclasses.field(init=False, repr=False)
    paragraphs: List[Paragraph] = dataclasses.field(init=False, repr=False)
    blocks: List[Block] = dataclasses.field(init=False, repr=False)
    tables: List[Table] = dataclasses.field(init=False, repr=False)
    _hocr_bounding_box: Optional[str] = dataclasses.field(init=False, default=None)

    def __post_init__(self):
        """
        Order of Init
        Token
        Line
        Paragraph,
        Block
        """

        self.text = _text_from_layout(
            self.documentai_object.layout, text=self.document_text
        )
        self.page_number = int(self.documentai_object.page_number)

        self.tables = [
            Table(documentai_object=table, document_text=self.document_text)
            for table in self.documentai_object.tables
        ]

        self.form_fields = [
            FormField(documentai_object=form_field, document_text=self.document_text)
            for form_field in self.documentai_object.form_fields
        ]

        self.tokens = _get_tokens(tokens=self.documentai_object.tokens, page=self)
        self.lines = _get_lines(lines=self.documentai_object.lines, page=self)
        self.paragraphs = _get_paragraphs(
            paragraphs=self.documentai_object.paragraphs, page=self
        )
        self.blocks = _get_blocks(
            blocks=self.documentai_object.blocks,
            page=self,
        )

    def to_hocr(self):
        r"""Exports a string hOCR version of the documentai.Document.Page.

        The format for the id of the object follows as such:
            object_{page_index}_...

        For example words will have the following id format:
            word_{page_index}_{block_index}_{paragraph_index}_{line_index}_{word_index}

        Args:

        Returns:
            str:
                A string hOCR version of the documentai.Document.Page.
        """
        f = ""
        pidx = self.documentai_object.page_number
        f += f"<div class='ocr_page' lang='unknown' title='{self.hocr_bounding_box}'>"
        for bidx, block in enumerate(self.blocks):
            f += f"<span class='ocr_carea' id='block_{pidx}_{bidx}' title='{block.hocr_bounding_box}'>"
            for paridx, paragraph in enumerate(block.paragraphs):
                f += f"<span class='ocr_par' id='par_{pidx}_{bidx}_{paridx}' title='{paragraph.hocr_bounding_box}'>"
                for lidx, line in enumerate(paragraph.lines):
                    line_text = html.escape(line.text)
                    f += f"<span class='ocr_line' id='line_{pidx}_{bidx}_{paridx}_{lidx}' title='{line.hocr_bounding_box}'>{line_text}</span>"
                    for tidx, token in enumerate(line.tokens):
                        word_text = html.escape(token.text)
                        f += f"<span class='ocrx_word' id='word_{pidx}_{bidx}_{paridx}_{lidx}_{tidx}' title='{token.hocr_bounding_box}'>{word_text}</span>"
                f += "</span>"
            f += "</span>"
        f += "</div>"
        return f

    @property
    def hocr_bounding_box(self):
        if self._hocr_bounding_box is None:
            self._hocr_bounding_box = _get_hocr_bounding_box(
                element_with_layout=self.documentai_object,
                dimension=self.documentai_object.dimension,
            )
        return self._hocr_bounding_box
