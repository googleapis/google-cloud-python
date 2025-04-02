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
import bigframes


def test_to_pandas_override_global_option(scalars_df_index):
    with bigframes.option_context("bigquery.allow_large_results", True):

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
