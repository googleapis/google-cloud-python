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

import types
from typing import Any, Dict, List, Optional, Tuple

from google.protobuf import json_format

from google.api_core import path_template


def transcode(
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
        query_params_json = json_format.MessageToDict(
            transcoded_request["query_params"],
            use_integers_for_enums=rest_numeric_enums,
        )

    if required_fields_default_values:
        for k, v in required_fields_default_values.items():
            if k not in query_params_json:
                query_params_json[k] = v

    if rest_numeric_enums:
        query_params_json["$alt"] = "json;enum-encoding=int"

    return transcoded_request, body_json, query_params_json


class RestTransportInterceptorMeta(type):
    """Metaclass for RestTransportInterceptor to allow class-level mocking of hooks."""

    def __getattr__(cls, name: str) -> Any:
        if name.startswith("pre_"):

            def _dummy(self, request, metadata):
                return request, metadata

            setattr(cls, name, _dummy)
            return _dummy
        elif name.startswith("post_") and name.endswith("_with_metadata"):

            def _dummy(self, response, metadata):
                return response, metadata

            setattr(cls, name, _dummy)
            return _dummy
        elif name.startswith("post_"):

            def _dummy(self, response):
                return response

            setattr(cls, name, _dummy)
            return _dummy
        raise AttributeError(f"type object '{cls.__name__}' has no attribute '{name}'")


class RestTransportInterceptor(metaclass=RestTransportInterceptorMeta):
    """Base class for REST transport interceptors."""

    def __getattr__(self, name: str) -> Any:
        try:
            cls_attr = getattr(self.__class__, name)
            return types.MethodType(cls_attr, self)
        except AttributeError:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'"
            )
