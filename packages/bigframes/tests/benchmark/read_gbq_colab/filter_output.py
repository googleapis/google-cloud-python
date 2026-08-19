# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import pathlib

import benchmark.utils as utils

import bigframes.pandas as bpd

PAGE_SIZE = utils.READ_GBQ_COLAB_PAGE_SIZE


def filter_output(
    *,
    project_id,
    dataset_id,
    table_id,
):
    # TODO(tswast): Support alternative query if table_id is a local DataFrame,
    # e.g. "{local_inline}" or "{local_large}"
    df = bpd._read_gbq_colab(f"SELECT * FROM `{project_id}`.{dataset_id}.{table_id}")

    # Simulate getting the first page, since we'll always do that first in the UI.
    batches = df._to_pandas_batches(page_size=PAGE_SIZE)
    assert (tr := batches.total_rows) is not None and tr >= 0
    next(iter(batches))

    # Simulate the user filtering by a column and visualizing those results
    df_filtered = df[df["col_bool_0"]]
    batches = df_filtered._to_pandas_batches(page_size=PAGE_SIZE)
    assert (tr := batches.total_rows) is not None and tr >= 0
    first_page = next(iter(batches))

    # It's possible we don't have any pages at all, since we filtered out all
    # matching rows.
    assert len(first_page.index) <= tr


if __name__ == "__main__":
    config = utils.get_configuration(include_table_id=True)
    current_path = pathlib.Path(__file__).absolute()

    utils.get_execution_time(
        filter_output,
        current_path,
        config.benchmark_suffix,
        project_id=config.project_id,
        dataset_id=config.dataset_id,
        table_id=config.table_id,
    )
