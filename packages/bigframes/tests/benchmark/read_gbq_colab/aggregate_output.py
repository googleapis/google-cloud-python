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

import bigframes.session

PAGE_SIZE = utils.READ_GBQ_COLAB_PAGE_SIZE


def aggregate_output(
    *, project_id, dataset_id, table_id, session: bigframes.session.Session
):
    # TODO(tswast): Support alternative query if table_id is a local DataFrame,
    # e.g. "{local_inline}" or "{local_large}"
    df = session._read_gbq_colab(
        f"SELECT * FROM `{project_id}`.{dataset_id}.{table_id}"
    )

    # Simulate getting the first page, since we'll always do that first in the UI.
    df.shape
    next(iter(df.to_pandas_batches(page_size=PAGE_SIZE)))

    # To simulate very small rows that can only fit a boolean,
    # some tables don't have an integer column. If an integer column is available,
    # we prefer to group by that to get a more realistic number of groups.
    group_column = "col_int64_1"
    if group_column not in df.columns:
        group_column = "col_bool_0"

    # Simulate the user aggregating by a column and visualizing those results
    df_aggregated = (
        df.assign(rounded=df[group_column].astype("Int64").round(-9))
        .groupby("rounded")
        .sum(numeric_only=True)
    )

    df_aggregated.shape
    next(iter(df_aggregated.to_pandas_batches(page_size=PAGE_SIZE)))


if __name__ == "__main__":
    (
        project_id,
        dataset_id,
        table_id,
        session,
        suffix,
    ) = utils.get_configuration(include_table_id=True)
    current_path = pathlib.Path(__file__).absolute()

    utils.get_execution_time(
        aggregate_output,
        current_path,
        suffix,
        project_id=project_id,
        dataset_id=dataset_id,
        table_id=table_id,
        session=session,
    )
