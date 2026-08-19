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

import bigframes.pandas

PAGE_SIZE = utils.READ_GBQ_COLAB_PAGE_SIZE


def first_page(*, project_id, dataset_id, table_id):
    # TODO(tswast): Support alternative query if table_id is a local DataFrame,
    # e.g. "{local_inline}" or "{local_large}"
    df = bigframes.pandas._read_gbq_colab(
        f"SELECT * FROM `{project_id}`.{dataset_id}.{table_id}"
    )

    # Get number of rows (to calculate number of pages) and the first page.
    batches = df._to_pandas_batches(page_size=PAGE_SIZE)
    assert (tr := batches.total_rows) is not None and tr >= 0
    next(iter(batches))


if __name__ == "__main__":
    config = utils.get_configuration(include_table_id=True, start_session=False)
    current_path = pathlib.Path(__file__).absolute()

    utils.get_execution_time(
        first_page,
        current_path,
        config.benchmark_suffix,
        project_id=config.project_id,
        dataset_id=config.dataset_id,
        table_id=config.table_id,
    )
