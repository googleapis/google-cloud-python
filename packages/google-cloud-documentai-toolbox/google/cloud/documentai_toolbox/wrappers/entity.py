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
"""Wrappers for Document AI Entity type."""

import dataclasses

from google.cloud import documentai


@dataclasses.dataclass
class Entity:
    r"""Represents a wrapped documentai.Document.Entity.

    Attributes:
        documentai_entity (google.cloud.documentai.Document.Entity):
            Required. The original google.cloud.documentai.Document.Entity object.
        type_ (str):
            Required. Entity type from a schema e.g. "Address".
        mention_text (str):
            Optional. Text value in the document e.g. "1600 Amphitheatre Pkwy".
            If the entity is not present in
            the document, this field will be empty.
    """
    documentai_entity: documentai.Document.Entity = dataclasses.field(repr=False)
    type_: str = dataclasses.field(init=False)
    mention_text: str = dataclasses.field(init=False, default="")
    normalized_text: str = dataclasses.field(init=False, default="")
    # Only Populated for Splitter/Classifier Output
    start_page: int = dataclasses.field(init=False)
    end_page: int = dataclasses.field(init=False)

    def __post_init__(self):
        self.type_ = self.documentai_entity.type_
        self.mention_text = self.documentai_entity.mention_text
        if (
            self.documentai_entity.normalized_value
            and self.documentai_entity.normalized_value.text
        ):
            self.normalized_text = self.documentai_entity.normalized_value.text

        if self.documentai_entity.page_anchor.page_refs:
            self.start_page = int(self.documentai_entity.page_anchor.page_refs[0].page)
            self.end_page = int(self.documentai_entity.page_anchor.page_refs[-1].page)
