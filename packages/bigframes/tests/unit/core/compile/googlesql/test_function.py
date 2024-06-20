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

import bigframes.core.compile.googlesql as sql


def test_cast():
    col = sql.ColumnExpression("col")
    assert sql.Cast(col, sql.DataType.STRING).sql() == "CAST (`col` AS STRING)"
    assert sql.Cast(col, sql.DataType.FLOAT64).sql() == "CAST (`col` AS FLOAT64)"
