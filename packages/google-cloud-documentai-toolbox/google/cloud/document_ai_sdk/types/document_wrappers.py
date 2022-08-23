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
"""Python wrappers for Document AI message types."""

from dataclasses import dataclass, field
import re
from typing import List

from google.cloud import documentai
from google.cloud.document_ai_sdk.services import (
    page_wrapper_service,
    document_wrapper_service,
)


@dataclass
class PageWrapper:
    """Represents a wrapped documentai.Document.Page .

    This class hides away the complexity of documentai message types and
    implements convenient methods for searching and extracting information within
    the Document.
    """

    shards: List[documentai.Document]

    _lines: List[str] = field(init=False, repr=False, default_factory=lambda: [])
    _paragraphs: List[str] = field(init=False, repr=False, default_factory=lambda: [])
    _tokens: List[str] = field(init=False, repr=False, default_factory=lambda: [])

    def __post_init__(self):
        self._lines = page_wrapper_service._get_lines(self.shards)
        self._paragraphs = page_wrapper_service._get_paragraphs(self.shards)
        self._tokens = page_wrapper_service._get_tokens(self.shards)

    def get_text_on_page(self, page_number: int) -> List[str]:
        return self._paragraphs[page_number - 1]

    def search_pages(self, regex: str) -> List[str]:
        res = []
        for paragraph in self._paragraphs:
            for text in paragraph:
                res.extend(re.findall(regex, text))

        return res


@dataclass
class DocumentWrapper:
    """Represents a wrapped Document.

    A single Document protobuf message might be written as several JSON files on
    GCS by Document AI's BatchProcessDocuments method.  This class hides away the
    shards from the users and implements convenient methods for searching and
    extracting information within the Document.
    """

    _gcs_prefix: str = field(init=False, repr=True)
    gcs_prefix: str

    _shards: List[documentai.Document] = field(init=False, repr=False)
    pages: PageWrapper = field(init=False, repr=False)

    def __post_init__(self):
        self._shards = document_wrapper_service._read_output(self._gcs_prefix)
        self.pages = PageWrapper(shards=self._shards)

    @property
    def gcs_prefix(self):
        return self._gcs_prefix

    @gcs_prefix.setter
    def gcs_prefix(self, gcs_prefix: str):
        self._gcs_prefix = gcs_prefix
