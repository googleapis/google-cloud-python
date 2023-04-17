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
from typing import List

from google.cloud import documentai
import pandas as pd


@dataclasses.dataclass
class Table:
    """Represents a wrapped documentai.Document.Page.Table.

    Attributes:
        documentai_table (google.cloud.documentai.Document.Page.Table):
            Required. The original google.cloud.documentai.Document.Page.Table object.
        body_rows (List[List[str]]):
            Required. A list of body rows.
        header_rows (List[List[str]]):
            Required. A list of header rows.
    """

    documentai_table: documentai.Document.Page.Table = dataclasses.field(repr=False)
    body_rows: List[List[str]] = dataclasses.field(repr=False)
    header_rows: List[List[str]] = dataclasses.field(repr=False)

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


def _table_wrapper_from_documentai_table(
    documentai_table: documentai.Document.Page.Table, text: str
) -> Table:
    r"""Returns a Table.

    Args:
        documentai_table (documentai.Document.Page.Table):
            Required. A documentai.Document.Page.Table.
        text (str):
            Required. UTF-8 encoded text in reading order
            from the document.

    Returns:
        Table:
            A Table.

    """

    header_rows = _table_rows_from_documentai_table_rows(
        table_rows=list(documentai_table.header_rows), text=text
    )
    body_rows = _table_rows_from_documentai_table_rows(
        table_rows=list(documentai_table.body_rows), text=text
    )

    return Table(
        documentai_table=documentai_table, body_rows=body_rows, header_rows=header_rows
    )


@dataclasses.dataclass
class Block:
    """Represents a wrapped documentai.Document.Page.Block.

    Attributes:
        documentai_block (google.cloud.documentai.Document.Page.Block):
            Required. The original google.cloud.documentai.Document.Page.Block object.
        text (str):
            Required. UTF-8 encoded text.
    """

    documentai_block: documentai.Document.Page.Block
    text: str


@dataclasses.dataclass
class Paragraph:
    """Represents a wrapped documentai.Document.Page.Paragraph.

    Attributes:
        documentai_paragraph (google.cloud.documentai.Document.Page.Paragraph):
            Required. The original google.cloud.documentai.Document.Page.Paragraph object.
        text (str):
            Required. UTF-8 encoded text.
    """

    documentai_paragraph: documentai.Document.Page.Paragraph
    text: str


@dataclasses.dataclass
class Line:
    """Represents a wrapped documentai.Document.Page.Line.

    Attributes:
        documentai_line (google.cloud.documentai.Document.Page.Line):
            Required. The original google.cloud.documentai.Document.Page.Line object.
        text (str):
            Required. UTF-8 encoded text.
    """

    documentai_line: documentai.Document.Page.Line
    text: str


@dataclasses.dataclass
class FormField:
    """Represents a wrapped documentai.Document.Page.FormField.

    Attributes:
        documentai_formfield (google.cloud.documentai.Document.Page.FormField):
            Required. The original google.cloud.documentai.Document.Page.FormField object.
        field_name (str):
            Required. The form field name
        field_value (str):
            Required. The form field value
    """

    documentai_formfield: documentai.Document.Page.FormField
    field_name: str
    field_value: str


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


def _get_blocks(blocks: List[documentai.Document.Page.Block], text: str) -> List[Block]:
    r"""Returns a list of Block.

    Args:
        blocks (List[documentai.Document.Page.Block]):
            Required. A list of documentai.Document.Page.Block objects.
        text (str):
            Required. UTF-8 encoded text in reading order
            from the document.
    Returns:
        List[Block]:
             A list of Blocks.
    """
    result = []

    for block in blocks:
        result.append(
            Block(
                documentai_block=block,
                text=_text_from_layout(layout=block.layout, text=text),
            )
        )

    return result


def _get_paragraphs(
    paragraphs: List[documentai.Document.Page.Paragraph], text: str
) -> List[Paragraph]:
    r"""Returns a list of Paragraph.

    Args:
        paragraphs (List[documentai.Document.Page.Paragraph]):
            Required. A list of documentai.Document.Page.Paragraph objects.
        text (str):
            Required. UTF-8 encoded text in reading order
            from the document.
    Returns:
        List[Paragraph]:
             A list of Paragraphs.
    """
    result = []

    for paragraph in paragraphs:
        result.append(
            Paragraph(
                documentai_paragraph=paragraph,
                text=_text_from_layout(layout=paragraph.layout, text=text),
            )
        )

    return result


def _get_lines(lines: List[documentai.Document.Page.Line], text: str) -> List[Line]:
    r"""Returns a list of Line.

    Args:
        lines (List[documentai.Document.Page.Line]):
            Required. A list of documentai.Document.Page.Line objects.
        text (str):
            Required. UTF-8 encoded text in reading order
            from the document.
    Returns:
        List[Line]:
            A list of Lines.
    """
    result = []

    for line in lines:
        result.append(
            Line(
                documentai_line=line,
                text=_text_from_layout(layout=line.layout, text=text),
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


def _get_form_fields(
    form_fields: List[documentai.Document.Page.FormField], text: str
) -> List[FormField]:
    r"""Returns a list of FormField.

    Args:
        form_fields (List[documentai.Document.Page.FormField]):
            Required. A list of documentai.Document.Page.FormField objects.
        text (str):
            Required. UTF-8 encoded text in reading order
            from the document.
    Returns:
        List[FormField]:
            A list of FormFields.
    """
    result = []

    for form_field in form_fields:
        result.append(
            FormField(
                documentai_formfield=form_field,
                field_name=_trim_text(_text_from_layout(form_field.field_name, text)),
                field_value=_trim_text(
                    _text_from_layout(form_field.field_value, text),
                ),
            )
        )

    return result


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


@dataclasses.dataclass
class Page:
    """Represents a wrapped documentai.Document.Page .

    Attributes:
        documentai_page (google.cloud.documentai.Document.Page):
            Required. The original google.cloud.documentai.Document.Page object.
        text: (str):
            Required. The full text of the Document containing the Page.
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

    documentai_page: documentai.Document.Page = dataclasses.field(repr=False)
    text: str = dataclasses.field(repr=False)

    form_fields: List[FormField] = dataclasses.field(init=False, repr=False)
    lines: List[Line] = dataclasses.field(init=False, repr=False)
    paragraphs: List[Paragraph] = dataclasses.field(init=False, repr=False)
    blocks: List[Block] = dataclasses.field(init=False, repr=False)
    tables: List[Table] = dataclasses.field(init=False, repr=False)

    def __post_init__(self):
        tables = []

        for table in self.documentai_page.tables:
            tables.append(
                _table_wrapper_from_documentai_table(
                    documentai_table=table, text=self.text
                )
            )

        self.form_fields = _get_form_fields(
            form_fields=self.documentai_page.form_fields, text=self.text
        )
        self.lines = _get_lines(lines=self.documentai_page.lines, text=self.text)
        self.paragraphs = _get_paragraphs(
            paragraphs=self.documentai_page.paragraphs, text=self.text
        )
        self.blocks = _get_blocks(blocks=self.documentai_page.blocks, text=self.text)
        self.tables = tables
