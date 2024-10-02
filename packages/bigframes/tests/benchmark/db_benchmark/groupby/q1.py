# Copyright 2024 Google LLC
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
import bigframes_vendored.db_benchmark.groupby_queries as vendored_dbbenchmark_groupby_queries

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
        vendored_dbbenchmark_groupby_queries.q1,
        current_path,
        suffix,
        project_id,
        dataset_id,
        table_id,
        session,
    )
