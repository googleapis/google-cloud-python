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

"""Helpers for preparing and structuring API requests.

This module provides utilities to preprocess request parameters and objects
before invoking API methods, such as automatically generating request IDs
if they are not already set.
"""

import uuid
from typing import Union

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
            if getattr(request, field_name, None) is None:
                setattr(request, field_name, str(uuid.uuid4()))
    else:
        if not getattr(request, field_name, None):
            setattr(request, field_name, str(uuid.uuid4()))
