# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
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
    Entry resources in Cloud Data Catalog can be of different types e.g. BigQuery
    Table entry is of type 'TABLE'. This enum describes all the possible types
    Cloud Data Catalog contains.

    Attributes:
      ENTRY_TYPE_UNSPECIFIED (int): Default unknown type
      TABLE (int): The type of entry that has a GoogleSQL schema, including logical views.
      DATA_STREAM (int): An entry type which is used for streaming entries. Example - Pub/Sub.
    """

    ENTRY_TYPE_UNSPECIFIED = 0
    TABLE = 2
    DATA_STREAM = 3


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
