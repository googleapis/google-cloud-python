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


def test_to_pandas_override_global_option(scalars_df_index):
    bf_index = scalars_df_index.index
    # Direct call to_pandas uses global default setting (allow_large_results=True),
    # table has 'bqdf' prefix.
    bf_index.to_pandas()
    assert bf_index._query_job.destination.table_id.startswith("bqdf")

    # When allow_large_results=False, a destination table is implicitly created,
    # table has 'anon' prefix.
    bf_index.to_pandas(allow_large_results=False)
    assert bf_index._query_job.destination.table_id.startswith("anon")


def test_to_numpy_override_global_option(scalars_df_index):
    bf_index = scalars_df_index.index
    # Direct call to_pandas uses global default setting (allow_large_results=True),
    # table has 'bqdf' prefix.
    bf_index.to_numpy()
    assert bf_index._query_job.destination.table_id.startswith("bqdf")

    # When allow_large_results=False, a destination table is implicitly created,
    # table has 'anon' prefix.
    bf_index.to_numpy(allow_large_results=False)
    assert bf_index._query_job.destination.table_id.startswith("anon")
