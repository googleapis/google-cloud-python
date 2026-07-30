# -*- coding: utf-8 -*-
# Copyright 2026 Google LLC
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
"""A compatibility module for older versions of google-api-core."""

import json

from typing import Any, Dict, List, Optional, Tuple

from google.api_core import path_template
from google.protobuf import json_format

from typing import Union
import uuid

import google.protobuf.message


def setup_request_id(
    request: Union[google.protobuf.message.Message, dict, None],
    field_name: str,
    is_proto3_optional: bool,
) -> None:
    """Populate a UUID4 field in the request if it is not already set.

    This helper is used to ensure request idempotency by automatically
    generating a unique identifier (such as `request_id`) for requests
    that support it. If a request is retried, the same identifier can be
    sent on subsequent retries, allowing the server to recognize the retried
    request and prevent duplicate processing (e.g., creating duplicate
    resources).

    Args:
        request (Union[google.protobuf.message.Message, dict]): The
            request object.
        field_name (str): The name of the field to populate.
        is_proto3_optional (bool): Whether the field is proto3 optional.
    """
    if request is None:
        return

    if isinstance(request, dict):
        if is_proto3_optional:
            if field_name not in request or request[field_name] is None:
                request[field_name] = str(uuid.uuid4())
        elif not request.get(field_name):
            request[field_name] = str(uuid.uuid4())
        return

    if is_proto3_optional:
        try:
            # Pure protobuf messages
            if not request.HasField(field_name):
                setattr(request, field_name, str(uuid.uuid4()))
        except (AttributeError, ValueError):
            # Proto-plus messages or other objects
            if not getattr(request, field_name, None):
                setattr(request, field_name, str(uuid.uuid4()))
    else:
        if not getattr(request, field_name, None):
            setattr(request, field_name, str(uuid.uuid4()))

def transcode_request(
    http_options: List[Dict[str, str]],
    request: Any,
    required_fields_default_values: Optional[Dict[str, Any]] = None,
    rest_numeric_enums: bool = False,
) -> Tuple[Dict[str, Any], Optional[str], Dict[str, Any]]:
    """Transcodes a request into HTTP method, URI, body, and query parameters.

    Args:
        http_options (List[Dict[str, str]]): List of HTTP transcoding rules.
        request (Any): The protobuf or proto-plus request message.
        required_fields_default_values (Optional[Dict[str, Any]]): Dictionary
            of required fields default values to merge into query parameters if missing.
        rest_numeric_enums (bool): Whether to encode enums as integers.

    Returns:
        Tuple[Dict[str, Any], Optional[str], Dict[str, Any]]: A tuple containing:
            - The raw transcoded request dictionary (containing keys like 'uri', 'method').
            - The serialized request body JSON string, or None if no body.
            - The query parameters dictionary.
    """
    if request is None:
        raise TypeError("request cannot be None")

    # Convert proto-plus message to its underlying protobuf message if needed
    pb_request = getattr(request, "_pb", request)

    transcoded_request = path_template.transcode(http_options, pb_request)

    body_json = None
    if transcoded_request.get("body") is not None:
        body_json = json_format.MessageToJson(
            transcoded_request["body"],
            use_integers_for_enums=rest_numeric_enums,
        )

    query_params_json = {}
    if transcoded_request.get("query_params") is not None:
        query_params_json = json.loads(
            json_format.MessageToJson(
                transcoded_request["query_params"],
                use_integers_for_enums=rest_numeric_enums,
            )
        )

    # If required_fields_default_values is provided, we merge default values for missing
    # required fields into the query parameters.
    if required_fields_default_values:
        for k, v in required_fields_default_values.items():
            if k not in query_params_json:
                query_params_json[k] = v

    if rest_numeric_enums:
        query_params_json["$alt"] = "json;enum-encoding=int"

    return transcoded_request, body_json, query_params_json
