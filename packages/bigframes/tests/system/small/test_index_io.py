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
import pandas as pd

import bigframes


def test_to_pandas_override_global_option(scalars_df_index):
    with bigframes.option_context("compute.allow_large_results", True):

        bf_index = scalars_df_index.index

        # Direct call to_pandas uses global default setting (allow_large_results=True),
        bf_index.to_pandas()
        table_id = bf_index._query_job.destination.table_id
        assert table_id is not None

        # When allow_large_results=False, a query_job object should not be created.
        # Therefore, the table_id should remain unchanged.
        bf_index.to_pandas(allow_large_results=False)
        assert bf_index._query_job.destination.table_id == table_id


def test_to_pandas_dry_run(scalars_df_index):
    index = scalars_df_index.index

    result = index.to_pandas(dry_run=True)

    assert isinstance(result, pd.Series)
    assert len(result) > 0


def test_to_numpy_override_global_option(scalars_df_index):
    with bigframes.option_context("compute.allow_large_results", True):

        bf_index = scalars_df_index.index

        # Direct call to_numpy uses global default setting (allow_large_results=True),
        # table has 'bqdf' prefix.
        bf_index.to_numpy()
        table_id = bf_index._query_job.destination.table_id
        assert table_id is not None

        # When allow_large_results=False, a query_job object should not be created.
        # Therefore, the table_id should remain unchanged.
        bf_index.to_numpy(allow_large_results=False)
        assert bf_index._query_job.destination.table_id == table_id
