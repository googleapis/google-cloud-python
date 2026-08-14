# Copyright 2026 Google LLC
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

import re

import pytest

freezegun = pytest.importorskip("freezegun")
pytest.importorskip("pytest_snapshot")


@pytest.mark.parametrize("query_num", range(1, 23))
def test_tpch_query(tpch_session, query_num, snapshot):
    project_id = "bigframes-dev-perf"
    dataset_id = "tpch_0001t"

    query_file_path = f"third_party/bigframes_vendored/tpch/queries/q{query_num}.py"

    with open(query_file_path, "r") as f:
        query_code = f.read()

    # We want to capture the result dataframe instead of running next(result.to_pandas_batches(...))
    modified_code = re.sub(
        r"next\((\w+)\.to_pandas_batches\((.*?)\)\)",
        r"return \1",
        query_code,
    )

    exec_globals = {}  # type: ignore[var-annotated]
    exec(modified_code, exec_globals)
    q_func = exec_globals["q"]

    result = q_func(project_id, dataset_id, tpch_session)

    # result should be a DataFrame
    snapshot.assert_match(result.sql, "out.sql")
