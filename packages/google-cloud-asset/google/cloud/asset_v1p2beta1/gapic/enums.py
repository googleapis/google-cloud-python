# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Wrappers for protocol buffer enum types."""

import enum


class ContentType(enum.IntEnum):
    """
    Asset content type.

    Attributes:
      CONTENT_TYPE_UNSPECIFIED (int): Unspecified content type.
      RESOURCE (int): Resource metadata.
      IAM_POLICY (int): The actual IAM policy set on a resource.
    """

    CONTENT_TYPE_UNSPECIFIED = 0
    RESOURCE = 1
    IAM_POLICY = 2
