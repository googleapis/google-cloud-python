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

import uuid

try:
    from google.api_core.gapic_v1.request import setup_request_id  # type: ignore
except ImportError:
    def setup_request_id(request, field_name: str, is_proto3_optional: bool):
        """Populate a UUID4 field in the request if it is not already set.

        Args:
            request (Union[google.protobuf.message.Message, dict]): The request object.
            field_name (str): The name of the field to populate.
            is_proto3_optional (bool): Whether the field is proto3 optional.
        """
        if request is None:
            return

        request_id_val = str(uuid.uuid4())

        if isinstance(request, dict):
            if is_proto3_optional:
                if field_name not in request or request[field_name] is None:
                    request[field_name] = request_id_val
            elif not request.get(field_name):
                request[field_name] = request_id_val
            return

        if is_proto3_optional:
            try:
                # Pure protobuf messages
                if not request.HasField(field_name):
                    setattr(request, field_name, request_id_val)
            except (AttributeError, ValueError):
                # Proto-plus messages or other objects
                if not getattr(request, field_name, None):
                    setattr(request, field_name, request_id_val)
        else:
            if not getattr(request, field_name, None):
                setattr(request, field_name, request_id_val)
