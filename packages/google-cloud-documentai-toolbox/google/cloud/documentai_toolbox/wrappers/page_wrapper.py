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
    """Returns a list of texts from Document.page ."""
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

    This class hides away the complexity of documentai page message type and
    implements convenient methods for searching and extracting information within
    the Document.
    """

    lines: List[str]
    paragraphs: List[str]
    tokens: List[str]
    _documentai_page: documentai.Document.Page

    @classmethod
    def from_documentai_page(
        cls, documentai_page: documentai.Document.Page, text: str
    ) -> "PageWrapper":
        return PageWrapper(
            _text_from_element_with_layout(documentai_page.lines, text),
            _text_from_element_with_layout(documentai_page.paragraphs, text),
            _text_from_element_with_layout(documentai_page.tokens, text),
            documentai_page,
        )
