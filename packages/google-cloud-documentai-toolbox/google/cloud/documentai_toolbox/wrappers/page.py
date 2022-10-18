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
from typing import List, Union

from google.cloud import documentai
import pandas as pd

ElementWithLayout = Union[
    documentai.Document.Page.Paragraph,
    documentai.Document.Page.Line,
    documentai.Document.Page.Token,
    documentai.Document.Page.Table.TableCell,
]


@dataclasses.dataclass
class Table:
    """Represents a wrapped documentai.Document.Page.Table.

    Attributes:
        _documentai_table (google.cloud.documentai.Document.Page.Table):
            Required. The original google.cloud.documentai.Document.Page.Table object.
        body_rows (List[List[str]]):
            Required. A list of body rows.
        header_rows (List[List[str]]):
            Required. A list of headers.
    """

    _documentai_table: documentai.Document.Page.Table = dataclasses.field(
        init=True, repr=False
    )
    body_rows: List[List[str]] = dataclasses.field(init=True, repr=False)
    header_rows: List[List[str]] = dataclasses.field(init=True, repr=False)

    @classmethod
    def from_documentai_table(
        cls,
        documentai_table: documentai.Document.Page.Table,
        header_rows: List[List[str]],
        body_rows: List[List[str]],
    ) -> "Table":
        r"""Returns a Table from google.cloud.documentai.Document.Page.

        Args:
            documentai_table (google.cloud.documentai.Document.Page.Table):
                Required. A single table object.
            header_rows (List[List[str]]):
                Required. a list of header rows.
            body_rows (List[List[str]]):
                Required. a list of body rows.

        Returns:
            Table:
                A Table from google.cloud.documentai.Document.Page.Table.

        """
        return Table(
            _documentai_table=documentai_table,
            header_rows=header_rows,
            body_rows=body_rows,
        )

    def to_dataframe(self) -> pd.DataFrame:
        r"""Returns pd.DataFrame from documentai.table

        Returns:
            pd.DataFrame:
                The DataFrame of the table.

        """
        rows = self.body_rows if self.body_rows != [] else self.header_rows

        rows.append("\n")
        rows.append("\n")

        dataframe = pd.DataFrame(rows)
        if self.body_rows != [] and self.header_rows != []:
            dataframe.columns = self.header_rows

        return dataframe

    def to_csv(self, dataframe: pd.DataFrame) -> str:
        r"""Returns a csv str.

            .. code-block:: python

                from google.cloud.documentai_toolbox import Document

                def sample_table_to_csv():

                    #Wrap document from gcs_path
                    merged_document = Document('gs://abc/def/gh/1')

                    #Use first page
                    page = merged_document.pages[0]

                    #export the first table in page 1 to csv
                    dataframe = page.tables[0].to_dataframe()
                    csv_text = page.tables[0].to_csv(dataframe=dataframe)

                    print(csv_text)

        Args:
            dataframe (pd.Dataframe):
                Required. Two-dimensional, size-mutable, potentially heterogeneous tabular data.

        Returns:
            str:
                The table in csv format.

        """

        result_csv = dataframe.to_csv(index=False)

        return result_csv


def _table_wrapper_from_documentai_table(
    documentai_table: List[documentai.Document.Page.Table], text: str
) -> Table:
    r"""Returns a Table.

    Args:
        documentai_tables (List[documentai.Document.Page.Table]):
            Required. A list of documentai.Document.Page.Table.
        text (str):
            Required. UTF-8 encoded text in reading order
            from the document.

    Returns:
        Table:
            A Table.

    """

    header_rows = []
    body_rows = []

    header_rows = _table_row_from_documentai_table_row(
        documentai_table.header_rows, text
    )
    body_rows = _table_row_from_documentai_table_row(documentai_table.body_rows, text)

    result = Table.from_documentai_table(
        documentai_table=documentai_table, body_rows=body_rows, header_rows=header_rows
    )

    return result


def _table_row_from_documentai_table_row(
    table_rows: List[documentai.Document.Page.Table.TableRow], text: str
) -> List[str]:
    r"""Returns a list rows from table_rows.

    Args:
        table_rows (documentai.Document.Page.Table.TableRow):
            Required. A documentai.Document.Page.Table.TableRow.
        text (str):
            Required. UTF-8 encoded text in reading order
            from the document.

    Returns:
        List[str]:
            A list of table rows.
    """
    body_rows = []
    for row in table_rows:
        row_text = []

        for cell in row.cells:
            row_text.append(
                _text_from_element_with_layout(element_with_layout=cell, text=text)
            )

        body_rows.append([x.replace("\n", "") for x in row_text])
    return body_rows


def _text_from_element_with_layout(
    element_with_layout: ElementWithLayout, text: str
) -> str:
    r"""Returns a text from a single element.

    Args:
        element_with_layout (ElementWithLayout):
            Required. a element with layout attribute.
        text (str):
            Required. UTF-8 encoded text in reading order
            from the document.

    Returns:
        str:
            Text from a single element.
    """

    result_text = ""

    if element_with_layout.layout.text_anchor.text_segments == []:
        return ""
    else:
        for text_segment in element_with_layout.layout.text_anchor.text_segments:
            result_text += text[
                int(text_segment.start_index) : int(text_segment.end_index)
            ]

    return result_text


@dataclasses.dataclass
class Page:
    """Represents a wrapped documentai.Document.Page .

    Attributes:
        _documentai_page (google.cloud.documentai.Document.Page):
            Required.The original google.cloud.documentai.Document.Page object.
        lines (List[str]):
            Required.A list of visually detected text lines on the
            page. A collection of tokens that a human would
            perceive as a line.
        paragraphs (List[str]):
            Required.A list of visually detected text paragraphs
            on the page. A collection of lines that a human
            would perceive as a paragraph.
        tables (List[Table]):
            A list of visually detected tables on the
            page.
    """

    _documentai_page: documentai.Document.Page = dataclasses.field(
        init=True, repr=False
    )
    lines: List[str] = dataclasses.field(init=True, repr=False)
    paragraphs: List[str] = dataclasses.field(init=True, repr=False)
    tables: List[Table] = dataclasses.field(init=True, repr=False)

    @classmethod
    def from_documentai_page(
        cls, documentai_page: documentai.Document.Page, text: str
    ) -> "Page":
        r"""Returns a Page from google.cloud.documentai.Document.Page.

        Args:
            documentai_page (google.cloud.documentai.Document.Page):
                Required. A single page object.
            text (str):
                Required. UTF-8 encoded text in reading order
                from the document.
        Returns:
            Page:
                A Page from google.cloud.documentai.Document.Page.
        """

        lines = []
        paragraphs = []
        tables = []

        for line in documentai_page.lines:
            lines.append(
                _text_from_element_with_layout(element_with_layout=line, text=text)
            )

        for paragraph in documentai_page.paragraphs:
            paragraphs.append(
                _text_from_element_with_layout(element_with_layout=paragraph, text=text)
            )

        for table in documentai_page.tables:
            tables.append(
                _table_wrapper_from_documentai_table(documentai_table=table, text=text)
            )

        return Page(
            _documentai_page=documentai_page,
            lines=lines,
            paragraphs=paragraphs,
            tables=tables,
        )
