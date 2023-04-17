# pylint: disable=protected-access
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


from google.cloud.documentai_toolbox import page
from google.cloud import documentai
import pytest


@pytest.fixture
def docproto():
    with open(
        "tests/unit/resources/0/toolbox_invoice_test-0.json", "r", encoding="utf-8"
    ) as f:
        return documentai.Document.from_json(f.read())


@pytest.fixture
def docproto_form_parser():
    with open(
        "tests/unit/resources/form_parser/pretrained-form-parser-v1.0-2020-09-23_full-output.json",
        "r",
        encoding="utf-8",
    ) as f:
        return documentai.Document.from_json(f.read())


def test_table_to_csv():
    header_rows = [
        ["This", "Is", "A", "Header", "Test"],
        ["", "", "A", "Sub", "Header"],
    ]
    body_rows = [["This", "Is", "A", "Body", "Test"], ["1", "2", "3", "4", "5"]]
    table = page.Table(
        documentai_table=None, header_rows=header_rows, body_rows=body_rows
    )
    contents = table.to_csv()

    assert (
        contents
        == """This,Is,A,Header,Test
,,A,Sub,Header
This,Is,A,Body,Test
1,2,3,4,5
"""
    )


def test_table_to_csv_with_empty_body_rows():
    header_rows = [["This", "Is", "A", "Header", "Test"]]
    table = page.Table(documentai_table=None, header_rows=header_rows, body_rows=[])

    contents = table.to_csv()

    assert (
        contents
        == """This,Is,A,Header,Test
"""
    )


def test_table_to_csv_with_empty_header_rows():
    body_rows = [["This"], ["Is"], ["A"], ["Body"], ["Test"]]
    table = page.Table(documentai_table=None, header_rows=[], body_rows=body_rows)

    contents = table.to_csv()

    assert (
        contents
        == """""
This
Is
A
Body
Test
"""
    )


def test_table_to_csv_with_empty_header_rows_and_single_body():
    body_rows = [["Body"]]
    table = page.Table(documentai_table=None, header_rows=[], body_rows=body_rows)

    contents = table.to_csv()

    assert (
        contents
        == """""
Body
"""
    )


def test_table_to_dataframe():
    header_rows = [
        ["This", "Is", "A", "Header", "Test"],
        ["", "", "A", "Sub", "Header"],
    ]
    body_rows = [["This", "Is", "A", "Body", "Test"], ["1", "2", "3", "4", "5"]]
    table = page.Table(
        documentai_table=None, header_rows=header_rows, body_rows=body_rows
    )
    contents = table.to_dataframe()

    assert len(contents.columns) == 5
    assert len(contents.values) == 2


def test_trim_text():
    input_text = "Sally\nWalker\n"
    output_text = page._trim_text(input_text)

    assert output_text == "Sally Walker"


def test_table_wrapper_from_documentai_table(docproto):
    docproto_page = docproto.pages[0]

    table = page._table_wrapper_from_documentai_table(
        documentai_table=docproto_page.tables[0], text=docproto.text
    )
    assert len(table.body_rows) == 6
    assert len(table.header_rows[0]) == 4


def test_header_for_table_rows_from_documentai_table_rows(docproto):
    docproto_page = docproto.pages[0]

    header_rows = page._table_rows_from_documentai_table_rows(
        table_rows=docproto_page.tables[0].header_rows, text=docproto.text
    )
    assert header_rows == [["Item Description", "Quantity", "Price", "Amount"]]


def test_body_for_table_rows_from_documentai_table_rows(docproto):
    docproto_page = docproto.pages[0]

    body_rows = page._table_rows_from_documentai_table_rows(
        table_rows=docproto_page.tables[0].body_rows, text=docproto.text
    )
    assert body_rows == [
        ["Tool A", "500", "$1.00", "$500.00"],
        ["Service B", "1", "$900.00", "$900.00"],
        ["Resource C", "50", "$12.00", "$600.00"],
        ["", "", "Subtotal", "$2000.00"],
        ["", "", "Tax", "$140.00"],
        ["", "", "BALANCE DUE", "$2140.00"],
    ]


def test_text_from_element_with_layout(docproto):
    docproto_page = docproto.pages[0]

    text = page._text_from_layout(
        layout=docproto_page.paragraphs[0].layout, text=docproto.text
    )

    assert text == "Invoice\n"


def test_get_blocks(docproto):
    docproto_blocks = docproto.pages[0].blocks

    blocks = page._get_blocks(blocks=docproto_blocks, text=docproto.text)

    assert len(blocks) == 31
    assert blocks[0].text == "Invoice\n"


def test_get_paragraphs(docproto):
    docproto_paragraphs = docproto.pages[0].paragraphs

    paragraphs = page._get_paragraphs(
        paragraphs=docproto_paragraphs, text=docproto.text
    )

    assert len(paragraphs) == 31
    assert paragraphs[0].text == "Invoice\n"


def test_get_lines(docproto):
    docproto_lines = docproto.pages[0].lines

    lines = page._get_lines(lines=docproto_lines, text=docproto.text)

    assert len(lines) == 37
    assert lines[36].text == "Supplies used for Project Q.\n"


def test_get_form_fields(docproto_form_parser):
    docproto_form_fields = docproto_form_parser.pages[0].form_fields

    form_fields = page._get_form_fields(
        form_fields=docproto_form_fields, text=docproto_form_parser.text
    )

    assert len(form_fields) == 17
    assert form_fields[4].field_name == "Occupation:"
    assert form_fields[4].field_value == "Software Engineer"


# Class init Tests


def test_FormField():
    docai_form_field = documentai.Document.Page.FormField()
    form_field = page.FormField(
        documentai_formfield=docai_form_field,
        field_name="Name:",
        field_value="Sally Walker",
    )
    assert form_field.field_name == "Name:"
    assert form_field.field_value == "Sally Walker"


def test_Block():
    docai_block = documentai.Document.Page.Block()
    block = page.Block(documentai_block=docai_block, text="test_block")

    assert block.text == "test_block"


def test_Paragraph():
    docai_paragraph = documentai.Document.Page.Paragraph()
    paragraph = page.Paragraph(
        documentai_paragraph=docai_paragraph, text="test_paragraph"
    )

    assert paragraph.text == "test_paragraph"


def test_Line():
    docai_line = documentai.Document.Page.Line()
    line = page.Line(documentai_line=docai_line, text="test_line")

    assert line.text == "test_line"


def test_Table():
    header_rows = [
        ["This", "Is", "A", "Header", "Test"],
        ["", "", "A", "Sub", "Header"],
    ]
    body_rows = [["This", "Is", "A", "Body", "Test"], ["1", "2", "3", "4", "5"]]
    table = page.Table(
        documentai_table=None, header_rows=header_rows, body_rows=body_rows
    )

    assert len(table.body_rows) == 2
    assert len(table.header_rows[0]) == 5


def test_Page(docproto):
    docproto_page = docproto.pages[0]
    wrapped_page = page.Page(documentai_page=docproto_page, text=docproto.text)

    assert len(wrapped_page.lines) == 37
    assert len(wrapped_page.paragraphs) == 31
    assert len(wrapped_page.blocks) == 31
    assert wrapped_page.lines[0].text == "Invoice\n"
    assert wrapped_page.paragraphs[30].text == "Supplies used for Project Q.\n"
    assert wrapped_page.blocks[30].text == "Supplies used for Project Q.\n"
