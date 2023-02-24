# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
"""Document.proto converters."""

from typing import List
from google.cloud.vision import AnnotateFileResponse, ImageAnnotationContext
from google.cloud.vision import AnnotateImageResponse

from google.cloud.documentai_toolbox.wrappers import page

from google.cloud.documentai_toolbox.converters.vision_helpers import (
    _convert_document_page,
    _get_text_anchor_substring,
    PageInfo,
)


def _convert_to_vision_annotate_file_response(text: str, pages: List[page.Page]):
    """Convert OCR data from Document proto to AnnotateFileResponse proto (Vision API).

    Args:
        text (str):
            Contents of document.
         List[Page]:
            A list of Pages.

    Returns:
        AnnotateFileResponse proto with a TextAnnotation per page.
    """
    responses = []
    vision_file_response = AnnotateFileResponse()
    page_idx = 0
    while page_idx < len(pages):
        page_info = PageInfo(pages[page_idx].documentai_page, text)
        page_vision_annotation = _convert_document_page(page_info)
        page_vision_annotation.text = _get_text_anchor_substring(
            text, pages[page_idx].documentai_page.layout.text_anchor
        )
        responses.append(
            AnnotateImageResponse(
                full_text_annotation=page_vision_annotation,
                context=ImageAnnotationContext(page_number=page_idx + 1),
            )
        )
        page_idx += 1

    vision_file_response.responses = responses

    return vision_file_response
