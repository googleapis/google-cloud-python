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


def test_table_to_csv(docproto):
    docproto_page = docproto.pages[0]
    table = page.Table(
        documentai_object=docproto_page.tables[0], document_text=docproto.text
    )

    contents = table.to_csv()

    assert (
        contents
        == """Item Description,Quantity,Price,Amount
Tool A,500,$1.00,$500.00
Service B,1,$900.00,$900.00
Resource C,50,$12.00,$600.00
,,Subtotal,$2000.00
,,Tax,$140.00
,,BALANCE DUE,$2140.00
"""
    )


def test_table_to_csv_with_empty_body_rows(docproto):
    docproto_page = docproto.pages[0]
    table = page.Table(
        documentai_object=docproto_page.tables[0], document_text=docproto.text
    )
    table.body_rows = None

    contents = table.to_csv()

    assert (
        contents
        == """Item Description,Quantity,Price,Amount
"""
    )


def test_table_to_csv_with_empty_header_rows(docproto):
    docproto_page = docproto.pages[0]
    table = page.Table(
        documentai_object=docproto_page.tables[0], document_text=docproto.text
    )
    table.header_rows = None

    contents = table.to_csv()

    assert (
        contents
        == """,,,
Tool A,500,$1.00,$500.00
Service B,1,$900.00,$900.00
Resource C,50,$12.00,$600.00
,,Subtotal,$2000.00
,,Tax,$140.00
,,BALANCE DUE,$2140.00
"""
    )


def test_table_to_csv_with_empty_header_rows_and_single_body(docproto):
    docproto_page = docproto.pages[0]
    table = page.Table(
        documentai_object=docproto_page.tables[0], document_text=docproto.text
    )
    table.header_rows = []
    table.body_rows = [[table.body_rows[0][0]]]

    contents = table.to_csv()
    assert (
        contents
        == """""
Tool A
"""
    )


def test_table_to_dataframe(docproto):
    docproto_page = docproto.pages[0]
    table = page.Table(
        documentai_object=docproto_page.tables[0], document_text=docproto.text
    )
    contents = table.to_dataframe()

    assert len(contents.columns) == 4
    assert len(contents.values) == 6


def test_trim_text():
    input_text = "Sally\nWalker\n"
    output_text = page._trim_text(input_text)

    assert output_text == "Sally Walker"


def test_text_from_element_with_layout(docproto):
    docproto_page = docproto.pages[0]

    text = page._text_from_layout(
        layout=docproto_page.paragraphs[0].layout, text=docproto.text
    )

    assert text == "Invoice\n"


def test_get_hocr_bounding_box(docproto):
    hocr_bounding_box_normalized = page._get_hocr_bounding_box(
        element_with_layout=docproto.pages[0],
        page_dimension=docproto.pages[0].dimension,
    )

    assert hocr_bounding_box_normalized == "bbox 0 0 1758 2275"

    hocr_bounding_box_with_vertices = page._get_hocr_bounding_box(
        element_with_layout=docproto.pages[0].blocks[0],
        page_dimension=docproto.pages[0].dimension,
    )

    assert hocr_bounding_box_with_vertices == "bbox 1310 220 1534 282"


# Class init Tests


def test_Table(docproto):
    docproto_page = docproto.pages[0]
    table = page.Table(
        documentai_object=docproto_page.tables[0], document_text=docproto.text
    )

    assert len(table.body_rows) == 6
    assert len(table.header_rows[0]) == 4


def test_FormField(docproto_form_parser):
    documentai_formfield = docproto_form_parser.pages[0].form_fields[4]
    form_field = page.FormField(
        documentai_object=documentai_formfield,
        document_text=docproto_form_parser.text,
    )

    assert form_field.field_name == "Occupation:"
    assert form_field.field_value == "Software Engineer"


def test_Block(docproto):
    wrapped_page = page.Page(
        documentai_object=docproto.pages[0], document_text=docproto.text
    )
    docai_block = docproto.pages[0].blocks[0]
    block = page.Block(documentai_object=docai_block, _page=wrapped_page)

    assert block.text == "Invoice\n"
    assert block.hocr_bounding_box == "bbox 1310 220 1534 282"
    # checking cached value
    assert block.text == "Invoice\n"
    assert block.hocr_bounding_box == "bbox 1310 220 1534 282"


def test_Paragraph(docproto):
    wrapped_page = page.Page(
        documentai_object=docproto.pages[0], document_text=docproto.text
    )
    docai_paragraph = docproto.pages[0].paragraphs[0]
    paragraph = page.Paragraph(documentai_object=docai_paragraph, _page=wrapped_page)

    assert paragraph.text == "Invoice\n"
    assert paragraph.hocr_bounding_box == "bbox 1310 220 1534 282"
    # checking cached value
    assert paragraph.text == "Invoice\n"
    assert paragraph.hocr_bounding_box == "bbox 1310 220 1534 282"


def test_Line(docproto):
    wrapped_page = page.Page(
        documentai_object=docproto.pages[0], document_text=docproto.text
    )
    docai_line = docproto.pages[0].lines[36]
    line = page.Line(documentai_object=docai_line, _page=wrapped_page)

    assert line.text == "Supplies used for Project Q.\n"
    assert line.hocr_bounding_box == "bbox 223 1781 620 1818"
    # checking cached value
    assert line.text == "Supplies used for Project Q.\n"
    assert line.hocr_bounding_box == "bbox 223 1781 620 1818"


def test_Token(docproto):
    wrapped_page = page.Page(
        documentai_object=docproto.pages[0], document_text=docproto.text
    )
    docai_token = docproto.pages[0].tokens[85]
    token = page.Token(documentai_object=docai_token, _page=wrapped_page)

    assert token.text == "Q.\n"
    assert token.hocr_bounding_box == "bbox 585 1781 620 1818"
    # checking cached value
    assert token.text == "Q.\n"
    assert token.hocr_bounding_box == "bbox 585 1781 620 1818"


def test_Page(docproto):
    docproto_page = docproto.pages[0]

    wrapped_page = page.Page(
        documentai_object=docproto_page, document_text=docproto.text
    )

    assert "Invoice" in wrapped_page.document_text
    assert wrapped_page.page_number == 1

    assert len(wrapped_page.lines) == 37
    assert len(wrapped_page.paragraphs) == 31
    assert len(wrapped_page.blocks) == 31
    assert len(wrapped_page.tokens) == 86
    assert len(wrapped_page.form_fields) == 13

    assert wrapped_page.lines[0].text == "Invoice\n"
    assert wrapped_page.lines[0].tokens[0].text == "Invoice\n"
    assert len(wrapped_page.lines[0].tokens) == 1

    assert wrapped_page.paragraphs[30].text == "Supplies used for Project Q.\n"
    assert len(wrapped_page.paragraphs[30].lines) == 1
    assert wrapped_page.paragraphs[30].lines[0].text == "Supplies used for Project Q.\n"
    assert wrapped_page.paragraphs[30].lines[0].tokens[0].text == "Supplies "

    assert wrapped_page.blocks[30].text == "Supplies used for Project Q.\n"

    assert (
        wrapped_page.blocks[30].paragraphs[0].text == "Supplies used for Project Q.\n"
    )
    assert (
        wrapped_page.blocks[30].paragraphs[0].lines[0].text
        == "Supplies used for Project Q.\n"
    )
    assert wrapped_page.blocks[30].paragraphs[0].lines[0].tokens[0].text == "Supplies "
    assert wrapped_page.tokens[85].text == "Q.\n"

    assert wrapped_page.hocr_bounding_box == "bbox 0 0 1758 2275"
    # checking cached value
    assert wrapped_page.hocr_bounding_box == "bbox 0 0 1758 2275"

    assert wrapped_page.form_fields[0].field_name == "BALANCE DUE"
    assert wrapped_page.form_fields[0].field_value == "$2140.00"
