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

from __future__ import annotations

import typing

import bigframes_vendored.sqlglot.expressions as sge
from google.cloud import bigquery

from bigframes import dtypes
from bigframes.core.compile.sqlglot.sql import base


def insert(
    query_or_table: typing.Union[sge.Select, sge.Table],
    destination: bigquery.TableReference,
) -> sge.Insert:
    """Generates an INSERT INTO SQL statement from the given SELECT statement or
    table reference."""
    return sge.insert(_as_from_item(query_or_table), base.table(destination))


def replace(
    query_or_table: typing.Union[sge.Select, sge.Table],
    destination: bigquery.TableReference,
) -> sge.Merge:
    """Generates a MERGE statement to replace the contents of the destination table."""
    return sge.Merge(
        this=base.table(destination),
        using=_as_from_item(query_or_table),
        on=base.literal(False, dtypes.BOOL_DTYPE),
        whens=sge.Whens(
            expressions=[
                sge.When(matched=False, source=True, then=sge.Delete()),
                sge.When(matched=False, then=sge.Insert(this=sge.Var(this="ROW"))),
            ]
        ),
    )


def _as_from_item(
    query_or_table: typing.Union[sge.Select, sge.Table]
) -> typing.Union[sge.Subquery, sge.Table]:
    if isinstance(query_or_table, sge.Select):
        return query_or_table.subquery()
    else:  # table
        return query_or_table
