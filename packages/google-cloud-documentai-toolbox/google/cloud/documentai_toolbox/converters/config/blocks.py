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

import dataclasses
from typing import List
import json
from types import SimpleNamespace

from google.cloud import documentai


@dataclasses.dataclass
class Block:
    r"""Represents a Block from OCR data.

    Attributes:
        bounding_box (str):
            Required.
        block_references:
            Optional.
        block_id:
            Optional.
        confidence:
            Optional.
        type_:
            Required.
        text:
            Required.
        page_number:
            Optional.
    """
    bounding_box: dataclasses.field(init=True, repr=False, default=None)
    block_references: dataclasses.field(init=False, repr=False, default=None)
    block_id: dataclasses.field(init=False, repr=False, default=None)
    confidence: dataclasses.field(init=False, repr=False, default=None)
    type_: dataclasses.field(init=True, repr=False, default=None)
    text: dataclasses.field(init=True, repr=False, default=None)
    page_number: dataclasses.field(init=False, repr=False, default=None)
    page_width: dataclasses.field(init=False, repr=False, default=None)
    page_height: dataclasses.field(init=False, repr=False, default=None)
    bounding_width: dataclasses.field(init=False, repr=False, default=None)
    bounding_height: dataclasses.field(init=False, repr=False, default=None)
    bounding_type: dataclasses.field(init=False, repr=False, default=None)
    bounding_unit: dataclasses.field(init=False, repr=False, default=None)
    bounding_x: dataclasses.field(init=False, repr=False, default=None)
    bounding_y: dataclasses.field(init=False, repr=False, default=None)
    docproto_width: dataclasses.field(init=False, repr=False, default=None)
    docproto_height: dataclasses.field(init=False, repr=False, default=None)

    @classmethod
    def create(
        self,
        type_,
        text,
        bounding_box=None,
        block_references=None,
        block_id=None,
        confidence=None,
        page_number=None,
        page_width=None,
        page_height=None,
        bounding_width=None,
        bounding_height=None,
        bounding_type=None,
        bounding_unit=None,
        bounding_x=None,
        bounding_y=None,
        docproto_width=None,
        docproto_height=None,
    ):
        return Block(
            bounding_box=bounding_box,
            block_references=block_references,
            block_id=block_id,
            confidence=confidence,
            type_=type_,
            text=text,
            page_number=page_number,
            page_width=page_width,
            page_height=page_height,
            bounding_width=bounding_width,
            bounding_height=bounding_height,
            bounding_type=bounding_type,
            bounding_unit=bounding_unit,
            bounding_x=bounding_x,
            bounding_y=bounding_y,
            docproto_width=docproto_width,
            docproto_height=docproto_height,
        )


def _get_target_object(json_data: any, target_object: str) -> SimpleNamespace:
    r"""Returns SimpleNamespace of target_object.

    Args:
        json_data (str):
            Required. data from JSON.loads .
        target_object (str):
            Required. The path to the target object.

    Returns:
        SimpleNamespace.

    """
    json_data_s = SimpleNamespace(**json_data)

    target_object_parts = target_object.split(".")

    if not hasattr(json_data_s, target_object_parts[0]):
        return None

    current_object = json_data_s
    for part in target_object_parts:
        if type(current_object) == dict:
            current_object = SimpleNamespace(**current_object)
        elif type(current_object) == list and part.isnumeric():
            current_object = current_object[int(part)]
            continue
        current_object = getattr(current_object, part)
    return current_object


def _load_blocks_from_schema(
    input_data: bytes, input_config: bytes, base_docproto: documentai.Document
) -> List[Block]:
    r"""Loads Blocks from original annotation data and provided config.

    Args:
        input_data (bytes):
            Required.The bytes of the annotated data.
        input_config (bytes):
            Required.The bytes of config data.
        base_docproto (bytes):
            Required. The bytes of the original pdf.

    Returns:
        List[Block]:
            From original annotation data and provided config.

    """
    objects = json.loads(input_data)
    schema_json = json.loads(input_config, object_hook=lambda d: SimpleNamespace(**d))

    entities = schema_json.entity_object
    type_ = schema_json.entity.type_

    mention_text = schema_json.entity.mention_text

    document_height = None
    document_width = None

    id_ = schema_json.entity.id if hasattr(schema_json.entity, "id") else None
    if hasattr(schema_json, "page"):
        document_height = (
            schema_json.page.height if hasattr(schema_json.page, "height") else None
        )
        document_width = (
            schema_json.page.width if hasattr(schema_json.page, "width") else None
        )

    confidence = (
        schema_json.entity.confidence
        if hasattr(schema_json.entity, "confidence")
        else None
    )
    page_number = (
        schema_json.entity.page_number
        if hasattr(schema_json.entity, "page_number")
        else None
    )
    normalized_vertices = (
        schema_json.entity.normalized_vertices.base
        if hasattr(schema_json.entity.normalized_vertices, "base")
        else None
    )
    bounding_width = (
        schema_json.entity.normalized_vertices.width
        if hasattr(schema_json.entity.normalized_vertices, "width")
        else None
    )
    bounding_height = (
        schema_json.entity.normalized_vertices.height
        if hasattr(schema_json.entity.normalized_vertices, "height")
        else None
    )
    bounding_type = (
        schema_json.entity.normalized_vertices.type
        if hasattr(schema_json.entity.normalized_vertices, "type")
        else None
    )
    bounding_unit = (
        schema_json.entity.normalized_vertices.unit
        if hasattr(schema_json.entity.normalized_vertices, "unit")
        else None
    )
    bounding_x = (
        schema_json.entity.normalized_vertices.x
        if hasattr(schema_json.entity.normalized_vertices, "x")
        else None
    )
    bounding_y = (
        schema_json.entity.normalized_vertices.y
        if hasattr(schema_json.entity.normalized_vertices, "y")
        else None
    )

    blocks = []
    ens = _get_target_object(objects, entities)
    for i in ens:
        entity = i

        block_text = ""

        if type_ == f"{entities}:self":
            block_type = i
            entity = _get_target_object(objects, f"{entities}.{i}")
        else:
            block_type = _get_target_object(entity, type_)

        if "||" in mention_text:
            text_commands = mention_text.split("||")
            for command in text_commands:
                if command in entity:
                    block_text = _get_target_object(entity, command)
                    continue
        else:
            block_text = _get_target_object(entity, mention_text)

        b = Block.create(
            type_=block_type,
            text=block_text,
        )

        b.bounding_box = _get_target_object(entity, normalized_vertices)

        if id_:
            b.id_ = _get_target_object(entity, id_)
        if confidence:
            b.confidence = _get_target_object(entity, confidence)
        if page_number and page_number in entity:
            b.page_number = _get_target_object(entity, page_number)
        if bounding_width:
            b.bounding_width = _get_target_object(b.bounding_box, bounding_width)
        if bounding_height:
            b.bounding_height = _get_target_object(b.bounding_box, bounding_height)
        if document_height:
            b.page_height = _get_target_object(objects, document_height)
        if document_width:
            b.page_width = _get_target_object(objects, document_width)
        if bounding_type:
            b.bounding_type = bounding_type
        if bounding_unit:
            b.bounding_unit = bounding_unit
        if bounding_x:
            b.bounding_x = bounding_x
        if bounding_y:
            b.bounding_y = bounding_y

        if b.page_number is None:
            b.page_number = 0

        b.docproto_width = base_docproto.pages[int(b.page_number)].dimension.width
        b.docproto_height = base_docproto.pages[int(b.page_number)].dimension.height

        blocks.append(b)
    return blocks
