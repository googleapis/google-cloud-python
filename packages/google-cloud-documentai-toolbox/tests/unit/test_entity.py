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

from google.cloud import documentai
from google.cloud.documentai_toolbox import entity


def test_Entity():
    documentai_entity = documentai.Document.Entity(
        type_="some_entity_type", mention_text="some_mention_text"
    )
    wrapper_entity = entity.Entity(documentai_entity)

    assert wrapper_entity.type_ == "some_entity_type"
    assert wrapper_entity.mention_text == "some_mention_text"


def test_Entity_with_normalized_value():
    documentai_entity = documentai.Document.Entity(
        type_="another_entity_type",
        mention_text="another_mention_text",
        normalized_value=documentai.Document.Entity.NormalizedValue(
            text="normalized_text"
        ),
    )
    wrapper_entity = entity.Entity(documentai_entity)
    assert wrapper_entity.type_ == "another_entity_type"
    assert wrapper_entity.mention_text == "another_mention_text"
    assert wrapper_entity.normalized_text == "normalized_text"


def test_Entity_splitter():
    documentai_entity = documentai.Document.Entity(
        type_="invoice_statement",
        page_anchor=documentai.Document.PageAnchor(
            page_refs=[
                # page field is empty when its value is 0
                documentai.Document.PageAnchor.PageRef(),
                documentai.Document.PageAnchor.PageRef(page=1),
                documentai.Document.PageAnchor.PageRef(page=2),
            ]
        ),
    )
    wrapper_entity = entity.Entity(documentai_entity)
    assert wrapper_entity.type_ == "invoice_statement"
    assert wrapper_entity.start_page == 0
    assert wrapper_entity.end_page == 2
