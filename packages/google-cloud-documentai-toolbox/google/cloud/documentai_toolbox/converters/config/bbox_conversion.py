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

from typing import Callable
from intervaltree import intervaltree

from google.cloud import documentai
from google.cloud.documentai_v1.types import geometry


def _midpoint_in_bpoly(
    box_a: geometry.BoundingPoly, box_b: geometry.BoundingPoly
) -> bool:
    """Returns whether the midpoint in box_a is inside box_b."""

    # Calculate the midpoint of box_a.
    mid_x_a = (_get_norm_x_max(box_a) + _get_norm_x_min(box_a)) / 2.0
    mid_y_a = (_get_norm_y_max(box_a) + _get_norm_y_min(box_a)) / 2.0

    max_x_b = _get_norm_x_max(box_b)
    min_x_b = _get_norm_x_min(box_b)
    max_y_b = _get_norm_y_max(box_b)
    min_y_b = _get_norm_y_min(box_b)

    return min_x_b < mid_x_a < max_x_b and min_y_b < mid_y_a < max_y_b


def _merge_text_anchors(
    text_anchor_1: documentai.Document.TextAnchor,
    text_anchor_2: documentai.Document.TextAnchor,
) -> documentai.Document.TextAnchor:
    """Merges two TextAnchor objects into one ascending sorted TextAnchor."""
    merged_text_anchor = documentai.Document.TextAnchor()
    intervals = []
    for text_segment in text_anchor_1.text_segments:
        intervals.append(
            intervaltree.Interval(text_segment.start_index, text_segment.end_index)
        )
    for text_segment in text_anchor_2.text_segments:
        intervals.append(
            intervaltree.Interval(text_segment.start_index, text_segment.end_index)
        )

    interval_tree = intervaltree.IntervalTree(intervals)
    interval_tree.merge_overlaps(strict=False)
    ts = []
    for iv in sorted(interval_tree):
        ts.append(
            documentai.Document.TextAnchor.TextSegment(
                start_index=iv.begin, end_index=iv.end
            )
        )

    merged_text_anchor.text_segments = ts
    return merged_text_anchor


def _get_text_anchor_in_bbox(
    bbox: documentai.BoundingPoly,
    page: documentai.Document.Page,
    token_in_bounding_box_function: Callable[
        [documentai.BoundingPoly, documentai.BoundingPoly], bool
    ] = _midpoint_in_bpoly,
) -> documentai.Document.TextAnchor:
    """Gets mergedTextAnchor of Tokens in `page` that fall inside the `bbox`."""

    text_anchor = documentai.Document.TextAnchor()
    for token in page.tokens:
        if token_in_bounding_box_function(token.layout.bounding_poly, bbox):
            text_anchor = _merge_text_anchors(text_anchor, token.layout.text_anchor)
    return text_anchor


def _get_norm_x_max(bbox: geometry.BoundingPoly) -> float:
    return max([vertex.x for vertex in bbox.normalized_vertices])


def _get_norm_x_min(bbox: geometry.BoundingPoly) -> float:
    return min([vertex.x for vertex in bbox.normalized_vertices])


def _get_norm_y_max(bbox: geometry.BoundingPoly) -> float:
    return max([vertex.y for vertex in bbox.normalized_vertices])


def _get_norm_y_min(bbox: geometry.BoundingPoly) -> float:
    return min([vertex.y for vertex in bbox.normalized_vertices])


def _normalize_coordinates(x, y) -> float:
    return round(float(x / y), 9)


def _convert_to_pixels(x: float, conversion_rate: float) -> float:
    return x * conversion_rate


def _convert_bbox_units(
    coordinate, input_bbox_units, width=None, height=None, multiplier=1
) -> float:
    r"""Returns a converted coordinate.

    Args:
        coordinate (float):
            Required.The coordinate from document.proto
        input_bbox_units (str):
            Required. The bounding box units.
        width (float):
            Optional.
        height (float):
            Optional.
        multiplier (float):
            Optional.

    Returns:
        float:
            A converted coordinate.

    """
    final_coordinate = coordinate
    if input_bbox_units != "normalized":
        if input_bbox_units == "pxl":
            if width is None:
                final_coordinate = _normalize_coordinates(coordinate, height)
            else:
                final_coordinate = _normalize_coordinates(coordinate, width)
        if input_bbox_units == "inch":
            x = _convert_to_pixels(coordinate, 96)
            if width is None:
                final_coordinate = _normalize_coordinates(x, height)
            else:
                final_coordinate = _normalize_coordinates(x, width)
        if input_bbox_units == "cm":
            x = _convert_to_pixels(coordinate, 37.795)
            if width is None:
                final_coordinate = _normalize_coordinates(x, height)
            else:
                final_coordinate = _normalize_coordinates(x, width)

    return final_coordinate * multiplier


def _get_multiplier(
    docproto_coordinate: float, external_coordinate: float, input_bbox_units: str
) -> float:
    r"""Returns a multiplier to use when converting bounding boxes.

    Args:
        docproto_coordinate (float):
            Required.The coordinate from document.proto
        external_coordinate (float):
            Required.The coordinate from external annotations.
        input_bbox_units (str):
            Required. The bounding box units.
    Returns:
        float:
            multiplier to use when converting bounding boxes.

    """
    if input_bbox_units == "inch":
        converted = _convert_to_pixels(external_coordinate, 96)
        return docproto_coordinate / converted
    elif input_bbox_units == "cm":
        converted = _convert_to_pixels(external_coordinate, 37.795)
        return docproto_coordinate / converted
    else:
        return docproto_coordinate / external_coordinate


def _convert_bbox_to_docproto_bbox(block) -> geometry.BoundingPoly:
    r"""Returns a converted bounding box from Block.

    Args:
        block (Block):
            Required.
    Returns:
        geometry.BoundingPoly:
            A geometry.BoundingPoly from bounding box.

    """
    merged_bbox = geometry.BoundingPoly()
    x_multiplier = 1
    y_multiplier = 1
    coordinates = []
    nv = []

    # _convert_bbox_units should check if external_bbox is list or not
    coordinates_object = block.bounding_box
    if coordinates_object == []:
        return coordinates_object

    if block.page_width and block.page_height:
        x_multiplier = _get_multiplier(
            docproto_coordinate=block.docproto_width,
            external_coordinate=block.page_width,
            input_bbox_units=block.bounding_unit,
        )
        y_multiplier = _get_multiplier(
            docproto_coordinate=block.docproto_height,
            external_coordinate=block.page_height,
            input_bbox_units=block.bounding_unit,
        )

    if block.bounding_type == "1":
        # Type 1 : bounding box has 4 (x,y) coordinates

        if type(block.bounding_box) == list:
            for coordinate in coordinates_object:
                x = _convert_bbox_units(
                    coordinate[f"{block.bounding_x}"],
                    input_bbox_units=block.bounding_unit,
                    width=block.docproto_width,
                    multiplier=x_multiplier,
                )
                y = _convert_bbox_units(
                    coordinate[f"{block.bounding_y}"],
                    input_bbox_units=block.bounding_unit,
                    height=block.docproto_height,
                    multiplier=y_multiplier,
                )

                coordinates.append({"x": x, "y": y})

            coordinates_object = coordinates

    elif block.bounding_type == "2":
        # Type 2 : bounding box has 1 (x,y) coordinates for the top left corner
        #          and (width, height)
        original_x = coordinates_object[f"{block.bounding_x}"]
        original_y = coordinates_object[f"{block.bounding_y}"]

        x = _convert_bbox_units(
            original_x,
            input_bbox_units=block.bounding_unit,
            width=block.page_width,
            multiplier=x_multiplier,
        )
        y = _convert_bbox_units(
            original_y,
            input_bbox_units=block.bounding_unit,
            width=block.page_height,
            multiplier=y_multiplier,
        )

        # x_min_y_min
        coordinates.append({"x": x, "y": y})
        # x_max_y_min
        coordinates.append({"x": (x + block.bounding_width), "y": y})
        # x_max_y_max
        coordinates.append(
            {"x": (x + block.bounding_width), "y": (y + block.bounding_height)}
        )
        # x_min_y_max
        coordinates.append({"x": x, "y": (y + block.bounding_height)})

        coordinates_object = coordinates
    elif block.bounding_type == "3":
        # Type 2 : bounding box has 1 (x,y) coordinates for the top left corner
        #          and (width, height)
        for idx in range(0, len(block.bounding_box), 2):
            x = _convert_bbox_units(
                block.bounding_box[idx],
                input_bbox_units=block.bounding_unit,
                width=block.docproto_width,
                multiplier=x_multiplier,
            )
            y = _convert_bbox_units(
                block.bounding_box[idx + 1],
                input_bbox_units=block.bounding_unit,
                width=block.docproto_height,
                multiplier=y_multiplier,
            )

            coordinates.append({"x": x, "y": y})

        coordinates_object = coordinates

    for coordinates in coordinates_object:
        nv.append(documentai.NormalizedVertex(x=coordinates["x"], y=coordinates["y"]))

    merged_bbox.normalized_vertices = nv

    return merged_bbox
