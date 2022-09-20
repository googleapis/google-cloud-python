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

from google.cloud.documentai_toolbox.wrappers import PageWrapper
from google.cloud import documentai


def test_from_documentai_page():
    test_text = "Hello this is a test of from_documentai_page"

    test_text_segment = documentai.Document.TextAnchor.TextSegment(
        start_index=0, end_index=44
    )
    test_text_anchor = documentai.Document.TextAnchor(text_segments=[test_text_segment])
    test_layout = documentai.Document.Page.Layout(text_anchor=test_text_anchor)

    test_paragraph = documentai.Document.Page.Paragraph(layout=test_layout)

    test_entity = documentai.Document.Page(page_number=1, paragraphs=[test_paragraph])

    actual = PageWrapper.from_documentai_page(test_entity, test_text)

    assert actual.paragraphs[0] == test_text
