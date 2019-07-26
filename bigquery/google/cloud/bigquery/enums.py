# Copyright 2019 Google LLC
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

import re
import warnings

import enum
import six

from google.cloud.bigquery_v2.gapic import enums as gapic_enums


def _make_sql_scalars_enum():
    """Create an enum based on a gapic enum containing only SQL scalar types."""
    sql_scalar_types = frozenset(
        (
            "INT64",
            "BOOL",
            "FLOAT64",
            "STRING",
            "BYTES",
            "TIMESTAMP",
            "DATE",
            "TIME",
            "DATETIME",
            "GEOGRAPHY",
            "NUMERIC",
        )
    )
    excluded_members = frozenset(("TYPE_KIND_UNSPECIFIED", "ARRAY", "STRUCT"))

    # Sanity check - we do not want the new enum to go out of sync with the original
    # enum from gapic.
    # ASSUMPTION: No existing types are ever renamed or deleted, we only try to
    # detect cases when new types are introduced.
    gapic_names = set(m.name for m in gapic_enums.StandardSqlDataType.TypeKind)
    anticipated_names = sql_scalar_types | excluded_members
    unhandled_names = gapic_names - anticipated_names

    if unhandled_names:
        msg = (
            "The StandardSqlDataTypes enum migh be out of sync with the "
            "original StandardSqlDataType.TypeKind enum from gapic. Check "
            "enum members: {}".format(", ".join(unhandled_names))
        )
        warnings.warn(msg, UserWarning)

    new_enum = enum.Enum(
        "StandardSqlDataTypes",
        (
            (member.name, member.value)
            for member in gapic_enums.StandardSqlDataType.TypeKind
            if member.name in sql_scalar_types
        ),
    )

    # make sure the docstring for the new enum is also correct
    orig_doc = gapic_enums.StandardSqlDataType.TypeKind.__doc__
    skip_pattern = re.compile(
        "|".join(excluded_members)
        + "|because a JSON object"  # the second description line of STRUCT member
    )

    new_doc = "\n".join(
        six.moves.filterfalse(skip_pattern.search, orig_doc.splitlines())
    )
    new_enum.__doc__ = new_doc

    return new_enum


StandardSqlDataTypes = _make_sql_scalars_enum()
