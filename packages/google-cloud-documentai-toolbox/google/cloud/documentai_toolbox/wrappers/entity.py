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

from io import BytesIO

from google.cloud import documentai
from google.cloud.documentai_toolbox import constants
from PIL import Image


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

    # Only Populated for Identity Documents
    image: Image.Image = dataclasses.field(init=False, default=None)

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

    def crop_image(self, documentai_document: documentai.Document):
        r"""Return image cropped from page image for detected entity.

        Args:
            documentai_document (documentai.Document):
                Required. The `Document` containing the `Entity`.
        Returns:
            PIL.Image.Image:
                Image from `Document.Entity`. Returns `None` if there is no image.
        """
        if self.type_ not in constants.IMAGE_ENTITIES or self.mention_text:
            return

        page_ref = self.documentai_entity.page_anchor.page_refs[0]
        doc_page = documentai_document.pages[page_ref.page]
        image_content = doc_page.image.content

        doc_image = Image.open(BytesIO(image_content))
        w, h = doc_image.size
        vertices = [
            (int(v.x * w + 0.5), int(v.y * h + 0.5))
            for v in page_ref.bounding_poly.normalized_vertices
        ]
        (top, left), (bottom, right) = vertices[0], vertices[2]
        self.image = doc_image.crop((top, left, bottom, right))
