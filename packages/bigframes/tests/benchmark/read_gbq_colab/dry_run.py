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


def dry_run(*, project_id, dataset_id, table_id, session: bigframes.session.Session):
    # TODO(tswast): Support alternative query if table_id is a local DataFrame,
    # e.g. "{local_inline}" or "{local_large}"
    session._read_gbq_colab(
        f"SELECT * FROM `{project_id}`.{dataset_id}.{table_id}",
        dry_run=True,
    )


if __name__ == "__main__":
    config = utils.get_configuration(include_table_id=True)
    current_path = pathlib.Path(__file__).absolute()

    utils.get_execution_time(
        dry_run,
        current_path,
        config.benchmark_suffix,
        project_id=config.project_id,
        dataset_id=config.dataset_id,
        table_id=config.table_id,
        session=config.session,
    )
