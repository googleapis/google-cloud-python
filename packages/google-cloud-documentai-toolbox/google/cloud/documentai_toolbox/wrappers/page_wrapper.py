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

ElementWithLayout = Union[
    documentai.Document.Page.Paragraph,
    documentai.Document.Page.Line,
    documentai.Document.Page.Token,
]


def _text_from_element_with_layout(
    element_with_layout: List[ElementWithLayout], text: str
) -> List[str]:
    r"""Returns a list of strings extracted from the element with layout.

    Args:
        element_with_layout (List[ElementWithLayout]):
            Required. A element containing a layout object.

    Returns:
        List[str]:
            A list of strings extracted from the element with layout.

    """
    result = []
    # If a text segment spans several lines, it will
    # be stored in different text segments.
    for element in element_with_layout:
        result_text = ""
        for text_segment in element.layout.text_anchor.text_segments:
            start_index = int(text_segment.start_index)
            end_index = int(text_segment.end_index)
            result_text += text[start_index:end_index]
        result.append(text[start_index:end_index])
    return result


@dataclasses.dataclass
class PageWrapper:
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
    """

    _documentai_page: documentai.Document.Page = dataclasses.field(
        init=True, repr=False
    )
    lines: List[str] = dataclasses.field(init=True, repr=False)
    paragraphs: List[str] = dataclasses.field(init=True, repr=False)

    @classmethod
    def from_documentai_page(
        cls, documentai_page: documentai.Document.Page, text: str
    ) -> "PageWrapper":
        r"""Returns a PageWrapper from google.cloud.documentai.Document.Page.

        Args:
            documentai_page (google.cloud.documentai.Document.Page):
                Required. A single page object.
            text (str):
                Required. UTF-8 encoded text in reading order
                from the document.

        Returns:
            PageWrapper:
                A PageWrapper from google.cloud.documentai.Document.Page.

        """
        return PageWrapper(
            _documentai_page=documentai_page,
            lines=_text_from_element_with_layout(documentai_page.lines, text),
            paragraphs=_text_from_element_with_layout(documentai_page.paragraphs, text),
        )
