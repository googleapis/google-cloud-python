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
from typing import Optional

from google.cloud import documentai
from google.cloud.documentai_toolbox import constants
from PIL import Image


@dataclasses.dataclass
class Entity:
    """Represents a wrapped `documentai.Document.Entity`.

    Attributes:
        documentai_entity (google.cloud.documentai.Document.Entity):
            Required. The original `google.cloud.documentai.Document.Entity` object.
        page_offset (InitVar[int]):
            Optional. The start page of the shard containing the `documentai.Document.Entity`
            in the context of the full `documentai.Document`.
            `page_refs.page` is relative to the shard, not the full `documentai.Document`.
        type_ (str):
            Required. Entity type from a schema e.g. "Address".
        mention_text (str):
            Optional. Text value in the document e.g. "1600 Amphitheatre Pkwy".
            If the entity is not present in
            the document, this field will be empty.
        normalized_text (str):
            Optional. Normalized text value in the document e.g. "1970-01-01".
            If the entity is not present in
            the document, this field will be empty.
        start_page (int):
            Required. `Page` containing the `Entity` or the first page of the
            classification (for Splitter/Classifier processors).
        end_page (int):
            Required. Last page of the classification
            (for Splitter/Classifier processors). Default is `0` for other processors.
        normalized_vertices (List[documentai.NormalizedVertex]):
            Optional. Vertices for bounding box of `Entity`.
    """

    documentai_entity: documentai.Document.Entity = dataclasses.field(repr=False)
    page_offset: dataclasses.InitVar[Optional[int]] = 0

    type_: str = dataclasses.field(init=False)
    mention_text: str = dataclasses.field(init=False, default="")
    normalized_text: str = dataclasses.field(init=False, default="")

    start_page: int = dataclasses.field(init=False)
    # Only Populated for Splitter/Classifier Output
    end_page: int = dataclasses.field(init=False)

    def __post_init__(self, page_offset: int) -> None:
        self.type_ = self.documentai_entity.type_
        self.mention_text = self.documentai_entity.mention_text
        if (
            self.documentai_entity.normalized_value
            and self.documentai_entity.normalized_value.text
        ):
            self.normalized_text = self.documentai_entity.normalized_value.text

        page_refs = self.documentai_entity.page_anchor.page_refs
        if page_refs:
            self.start_page = int(page_refs[0].page) + page_offset
            self.end_page = int(page_refs[-1].page) + page_offset

    def crop_image(
        self, documentai_page: documentai.Document.Page
    ) -> Optional[Image.Image]:
        r"""Return image cropped from page image for detected entity.

        Args:
            documentai_page (documentai.Document):
                Required. The `Document.Page` containing the `Entity`.
        Returns:
            PIL.Image.Image:
                Image from `Document.Entity`. Returns `None` if there is no image.
        """
        if self.type_ not in constants.IMAGE_ENTITIES or self.mention_text:
            return None

        page_ref = self.documentai_entity.page_anchor.page_refs[0]

        if not documentai_page.image:
            raise ValueError("Document does not contain images.")

        doc_image = Image.open(BytesIO(documentai_page.image.content))
        w, h = doc_image.size
        vertices = [
            (int(v.x * w + 0.5), int(v.y * h + 0.5))
            for v in page_ref.bounding_poly.normalized_vertices
        ]
        (top, left), (bottom, right) = vertices[0], vertices[2]
        return doc_image.crop((top, left, bottom, right))
