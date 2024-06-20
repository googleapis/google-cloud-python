# Copyright 2024 Google LLC
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

import pytest

import bigframes.core.compile.googlesql as sql


@pytest.mark.parametrize(
    ("table_id", "dataset_id", "project_id", "expected"),
    [
        pytest.param("a", None, None, "`a`"),
        pytest.param("a", "b", None, "`b`.`a`"),
        pytest.param("a", "b", "c", "`c`.`b`.`a`"),
        pytest.param("a", None, "c", None, marks=pytest.mark.xfail(raises=ValueError)),
    ],
)
def test_table_expression(table_id, dataset_id, project_id, expected):
    expr = sql.TableExpression(
        table_id=table_id, dataset_id=dataset_id, project_id=project_id
    )
    assert expr.sql() == expected


def test_escape_chars():
    assert sql._escape_chars("\a\b\f\n\r\t\v\\?'\"`") == r"\a\b\f\n\r\t\v\\\?\'\"\`"
