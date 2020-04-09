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


class EntryType(enum.IntEnum):
    """
    Protocol Buffers - Google's data interchange format Copyright 2008
    Google Inc. All rights reserved.
    https://developers.google.com/protocol-buffers/

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are
    met:

    ::

        * Redistributions of source code must retain the above copyright

    notice, this list of conditions and the following disclaimer. \*
    Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution. \*
    Neither the name of Google Inc. nor the names of its contributors may be
    used to endorse or promote products derived from this software without
    specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
    IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
    TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

    Attributes:
      ENTRY_TYPE_UNSPECIFIED (int): Default unknown type
      TABLE (int): Output only. The type of entry that has a GoogleSQL schema, including
      logical views.
      MODEL (int): Output only. The type of models.
      DATA_STREAM (int): Output only. An entry type which is used for streaming entries. Example:
      Cloud Pub/Sub topic.
      FILESET (int): An entry type which is a set of files or objects. Example:
      Cloud Storage fileset.
    """

    ENTRY_TYPE_UNSPECIFIED = 0
    TABLE = 2
    MODEL = 5
    DATA_STREAM = 3
    FILESET = 4


class IntegratedSystem(enum.IntEnum):
    """
    This enum describes all the possible systems that Data Catalog integrates
    with.

    Attributes:
      INTEGRATED_SYSTEM_UNSPECIFIED (int): Default unknown system.
      BIGQUERY (int): BigQuery.
      CLOUD_PUBSUB (int): Cloud Pub/Sub.
    """

    INTEGRATED_SYSTEM_UNSPECIFIED = 0
    BIGQUERY = 1
    CLOUD_PUBSUB = 2


class SearchResultType(enum.IntEnum):
    """
    The different types of resources that can be returned in search.

    Attributes:
      SEARCH_RESULT_TYPE_UNSPECIFIED (int): Default unknown type.
      ENTRY (int): A designation of a specific field behavior (required, output only,
      etc.) in protobuf messages.

      Examples:

      string name = 1 [(google.api.field_behavior) = REQUIRED]; State state =
      1 [(google.api.field_behavior) = OUTPUT_ONLY]; google.protobuf.Duration
      ttl = 1 [(google.api.field_behavior) = INPUT_ONLY];
      google.protobuf.Timestamp expire_time = 1 [(google.api.field_behavior) =
      OUTPUT_ONLY, (google.api.field_behavior) = IMMUTABLE];
      TAG_TEMPLATE (int): Request message for ``CreateEntry``.
      ENTRY_GROUP (int): Optional. A column's mode indicates whether the values in this
      column are required, nullable, etc. Only ``NULLABLE``, ``REQUIRED`` and
      ``REPEATED`` are supported. Default mode is ``NULLABLE``.
    """

    SEARCH_RESULT_TYPE_UNSPECIFIED = 0
    ENTRY = 1
    TAG_TEMPLATE = 2
    ENTRY_GROUP = 3


class TableSourceType(enum.IntEnum):
    """
    Table source type.

    Attributes:
      TABLE_SOURCE_TYPE_UNSPECIFIED (int): Default unknown type.
      BIGQUERY_VIEW (int): Table view.
      BIGQUERY_TABLE (int): BigQuery native table.
    """

    TABLE_SOURCE_TYPE_UNSPECIFIED = 0
    BIGQUERY_VIEW = 2
    BIGQUERY_TABLE = 5


class FieldType(object):
    class PrimitiveType(enum.IntEnum):
        """
        Attributes:
          PRIMITIVE_TYPE_UNSPECIFIED (int): This is the default invalid value for a type.
          DOUBLE (int): A double precision number.
          STRING (int): An UTF-8 string.
          BOOL (int): A boolean value.
          TIMESTAMP (int): A timestamp.
        """

        PRIMITIVE_TYPE_UNSPECIFIED = 0
        DOUBLE = 1
        STRING = 2
        BOOL = 3
        TIMESTAMP = 4


class Taxonomy(object):
    class PolicyType(enum.IntEnum):
        """
        Defines policy types where policy tag can be used for.

        Attributes:
          POLICY_TYPE_UNSPECIFIED (int): Unspecified policy type.
          FINE_GRAINED_ACCESS_CONTROL (int): Fine grained access control policy, which enables access control on
          tagged resources.
        """

        POLICY_TYPE_UNSPECIFIED = 0
        FINE_GRAINED_ACCESS_CONTROL = 1
