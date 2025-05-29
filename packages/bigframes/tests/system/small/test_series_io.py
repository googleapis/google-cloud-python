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
import numpy
import numpy.testing
import pandas as pd
import pytest

import bigframes
import bigframes.series


def test_to_pandas_override_global_option(scalars_df_index):
    with bigframes.option_context("compute.allow_large_results", True):

        bf_series = scalars_df_index["int64_col"]

        # Direct call to_pandas uses global default setting (allow_large_results=True)
        bf_series.to_pandas()
        table_id = bf_series._query_job.destination.table_id
        assert table_id is not None

        session = bf_series._block.session
        execution_count = session._metrics.execution_count

        # When allow_large_results=False, a query_job object should not be created.
        # Therefore, the table_id should remain unchanged.
        bf_series.to_pandas(allow_large_results=False)
        assert bf_series._query_job.destination.table_id == table_id
        assert session._metrics.execution_count - execution_count == 1


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        pytest.param(
            {"sampling_method": "head"},
            r"DEPRECATED[\S\s]*sampling_method[\S\s]*Series.sample",
            id="sampling_method",
        ),
        pytest.param(
            {"random_state": 10},
            r"DEPRECATED[\S\s]*random_state[\S\s]*Series.sample",
            id="random_state",
        ),
        pytest.param(
            {"max_download_size": 10},
            r"DEPRECATED[\S\s]*max_download_size[\S\s]*Series.to_pandas_batches",
            id="max_download_size",
        ),
    ],
)
def test_to_pandas_warns_deprecated_parameters(scalars_df_index, kwargs, message):
    s: bigframes.series.Series = scalars_df_index["int64_col"]
    with pytest.warns(FutureWarning, match=message):
        s.to_pandas(
            # limits only apply for allow_large_result=True
            allow_large_results=True,
            **kwargs,
        )


@pytest.mark.parametrize(
    ("page_size", "max_results", "allow_large_results"),
    [
        pytest.param(None, None, True),
        pytest.param(2, None, False),
        pytest.param(None, 1, True),
        pytest.param(2, 5, False),
        pytest.param(3, 6, True),
        pytest.param(3, 100, False),
        pytest.param(100, 100, True),
    ],
)
def test_to_pandas_batches(scalars_dfs, page_size, max_results, allow_large_results):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_series = scalars_df["int64_col"]
    pd_series = scalars_pandas_df["int64_col"]

    total_rows = 0
    expected_total_rows = (
        min(max_results, len(pd_series)) if max_results else len(pd_series)
    )

    hit_last_page = False
    for s in bf_series.to_pandas_batches(
        page_size=page_size,
        max_results=max_results,
        allow_large_results=allow_large_results,
    ):
        assert not hit_last_page

        actual_rows = s.shape[0]
        expected_rows = (
            min(page_size, expected_total_rows) if page_size else expected_total_rows
        )

        assert actual_rows <= expected_rows
        if actual_rows < expected_rows:
            assert page_size
            hit_last_page = True

        pd.testing.assert_series_equal(
            s, pd_series[total_rows : total_rows + actual_rows]
        )
        total_rows += actual_rows

    assert total_rows == expected_total_rows


def test_to_numpy(scalars_dfs):
    bf_df, pd_df = scalars_dfs

    bf_result = numpy.array(bf_df["int64_too"], dtype="int64")
    pd_result = numpy.array(pd_df["int64_too"], dtype="int64")

    numpy.testing.assert_array_equal(bf_result, pd_result)
