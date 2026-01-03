# Copyright 2025 Google LLC
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

import unittest

import bigframes_vendored.sqlglot.expressions as sge
import pandas as pd
import pytest

from bigframes import dtypes
from bigframes.core import window_spec
from bigframes.core.compile.sqlglot.aggregations.windows import (
    apply_window_if_present,
    get_window_order_by,
)
import bigframes.core.expression as ex
import bigframes.core.identifiers as ids
import bigframes.core.ordering as ordering


class WindowsTest(unittest.TestCase):
    def test_get_window_order_by_empty(self):
        self.assertIsNone(get_window_order_by(tuple()))

    def test_get_window_order_by(self):
        result = get_window_order_by((ordering.OrderingExpression(ex.deref("col1")),))
        self.assertEqual(
            sge.Order(expressions=result).sql(dialect="bigquery"),
            "ORDER BY `col1` ASC NULLS LAST",
        )

    def test_get_window_order_by_override_nulls(self):
        result = get_window_order_by(
            (ordering.OrderingExpression(ex.deref("col1")),),
            override_null_order=True,
        )
        self.assertEqual(
            sge.Order(expressions=result).sql(dialect="bigquery"),
            "ORDER BY `col1` IS NULL ASC NULLS LAST, `col1` ASC NULLS LAST",
        )

    def test_get_window_order_by_override_nulls_desc(self):
        result = get_window_order_by(
            (
                ordering.OrderingExpression(
                    ex.deref("col1"),
                    direction=ordering.OrderingDirection.DESC,
                    na_last=False,
                ),
            ),
            override_null_order=True,
        )
        self.assertEqual(
            sge.Order(expressions=result).sql(dialect="bigquery"),
            "ORDER BY `col1` IS NULL DESC NULLS FIRST, `col1` DESC NULLS FIRST",
        )

    def test_apply_window_if_present_no_window(self):
        value = sge.func(
            "SUM", sge.Column(this=sge.to_identifier("col_0", quoted=True))
        )
        result = apply_window_if_present(value)
        self.assertEqual(result, value)

    def test_apply_window_if_present_row_bounded_no_ordering_raises(self):
        with pytest.raises(
            ValueError, match="No ordering provided for ordered analytic function"
        ):
            apply_window_if_present(
                sge.Var(this="value"),
                window_spec.WindowSpec(
                    bounds=window_spec.RowsWindowBounds(start=-1, end=1)
                ),
            )

    def test_apply_window_if_present_grouping_no_ordering(self):
        result = apply_window_if_present(
            sge.Var(this="value"),
            window_spec.WindowSpec(
                grouping_keys=(
                    ex.ResolvedDerefOp(
                        ids.ColumnId("col1"),
                        dtype=dtypes.STRING_DTYPE,
                        is_nullable=True,
                    ),
                    ex.ResolvedDerefOp(
                        ids.ColumnId("col2"),
                        dtype=dtypes.FLOAT_DTYPE,
                        is_nullable=True,
                    ),
                    ex.ResolvedDerefOp(
                        ids.ColumnId("col3"),
                        dtype=dtypes.JSON_DTYPE,
                        is_nullable=True,
                    ),
                    ex.ResolvedDerefOp(
                        ids.ColumnId("col4"),
                        dtype=dtypes.GEO_DTYPE,
                        is_nullable=True,
                    ),
                ),
            ),
        )
        self.assertEqual(
            result.sql(dialect="bigquery"),
            "value OVER (PARTITION BY `col1`, CAST(`col2` AS STRING), TO_JSON_STRING(`col3`), ST_ASBINARY(`col4`))",
        )

    def test_apply_window_if_present_range_bounded(self):
        result = apply_window_if_present(
            sge.Var(this="value"),
            window_spec.WindowSpec(
                ordering=(ordering.OrderingExpression(ex.deref("col1")),),
                bounds=window_spec.RangeWindowBounds(start=None, end=pd.Timedelta(0)),
            ),
        )
        self.assertEqual(
            result.sql(dialect="bigquery"),
            "value OVER (ORDER BY `col1` ASC NULLS LAST RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)",
        )

    def test_apply_window_if_present_range_bounded_timedelta(self):
        result = apply_window_if_present(
            sge.Var(this="value"),
            window_spec.WindowSpec(
                ordering=(ordering.OrderingExpression(ex.deref("col1")),),
                bounds=window_spec.RangeWindowBounds(
                    start=pd.Timedelta(days=-1), end=pd.Timedelta(hours=12)
                ),
            ),
        )
        self.assertEqual(
            result.sql(dialect="bigquery"),
            "value OVER (ORDER BY `col1` ASC NULLS LAST RANGE BETWEEN 86400000000 PRECEDING AND 43200000000 FOLLOWING)",
        )

    def test_apply_window_if_present_all_params(self):
        result = apply_window_if_present(
            sge.Var(this="value"),
            window_spec.WindowSpec(
                grouping_keys=(
                    ex.ResolvedDerefOp(
                        ids.ColumnId("col1"),
                        dtype=dtypes.STRING_DTYPE,
                        is_nullable=True,
                    ),
                ),
                ordering=(
                    ordering.OrderingExpression(
                        ex.ResolvedDerefOp(
                            ids.ColumnId("col2"),
                            dtype=dtypes.STRING_DTYPE,
                            is_nullable=True,
                        )
                    ),
                ),
                bounds=window_spec.RowsWindowBounds(start=-1, end=0),
            ),
        )
        self.assertEqual(
            result.sql(dialect="bigquery"),
            "value OVER (PARTITION BY `col1` ORDER BY `col2` ASC NULLS LAST ROWS BETWEEN 1 PRECEDING AND CURRENT ROW)",
        )


if __name__ == "__main__":
    unittest.main()
