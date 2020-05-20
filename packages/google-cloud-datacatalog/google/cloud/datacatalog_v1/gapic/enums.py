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
    Entry resources in Data Catalog can be of different types e.g. a
    BigQuery Table entry is of type ``TABLE``. This enum describes all the
    possible types Data Catalog contains.

    Attributes:
      ENTRY_TYPE_UNSPECIFIED (int): Default unknown type.
      TABLE (int): Output only. The type of entry that has a GoogleSQL schema, including
      logical views.
      MODEL (int): Output only. The type of models, examples include
      https://cloud.google.com/bigquery-ml/docs/bigqueryml-intro
      DATA_STREAM (int): Output only. An entry type which is used for streaming entries. Example:
      Pub/Sub topic.
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
      ENTRY (int): An ``Entry``.
      TAG_TEMPLATE (int): A ``TagTemplate``.
      ENTRY_GROUP (int): An ``EntryGroup``.
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
