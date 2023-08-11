# Copyright 2023 Google LLC
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

"""Tests for monkeypatched ibis code."""

import ibis.expr.types as ibis_types

import bigframes
import third_party.bigframes_vendored.ibis.expr.operations as vendored_ibis_ops


def test_approximate_quantiles(session: bigframes.Session, scalars_table_id: str):
    num_bins = 3
    ibis_client = session.ibis_client
    _, dataset, table_id = scalars_table_id.split(".")
    ibis_table: ibis_types.Table = ibis_client.table(table_id, database=dataset)
    ibis_column: ibis_types.NumericColumn = ibis_table["int64_col"]
    quantiles: ibis_types.ArrayScalar = vendored_ibis_ops.ApproximateMultiQuantile(  # type: ignore
        ibis_column, num_bins=num_bins
    ).to_expr()
    value = quantiles[1]
    num_edges = quantiles.length()

    sql = ibis_client.compile(value)
    num_edges_result = num_edges.to_pandas()

    assert "APPROX_QUANTILES" in sql
    assert num_edges_result == num_bins + 1
