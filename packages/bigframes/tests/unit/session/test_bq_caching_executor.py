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

from unittest import mock

import google.cloud.bigquery as bigquery
import google.cloud.exceptions
import pyarrow as pa
import pytest

import bigframes
import bigframes.core.nodes as nodes
import bigframes.core.schema as schemata
from bigframes.session.bq_caching_executor import BigQueryCachingExecutor


@pytest.fixture
def mock_executor():
    bqclient = mock.create_autospec(bigquery.Client)
    bqclient.project = "test-project"
    storage_manager = mock.Mock()
    bqstoragereadclient = mock.Mock()
    loader = mock.Mock()
    publisher = mock.Mock()
    return BigQueryCachingExecutor(
        bqclient, storage_manager, bqstoragereadclient, loader, publisher=publisher
    )


def test_compiler_with_fallback_legacy(mock_executor):
    run_fn = mock.Mock()
    with bigframes.option_context("experiments.sql_compiler", "legacy"):
        mock_executor._compile_with_fallback(run_fn)
    run_fn.assert_called_once_with("ibis")


def test_compiler_with_fallback_experimental(mock_executor):
    run_fn = mock.Mock()
    with bigframes.option_context("experiments.sql_compiler", "experimental"):
        mock_executor._compile_with_fallback(run_fn)
    run_fn.assert_called_once_with("sqlglot")


def test_compiler_with_fallback_stable_success(mock_executor):
    run_fn = mock.Mock()
    with bigframes.option_context("experiments.sql_compiler", "stable"):
        mock_executor._compile_with_fallback(run_fn)
    run_fn.assert_called_once_with("sqlglot", compiler_id=mock.ANY)


def test_compiler_execute_plan_gbq_fallback_labels(mock_executor):
    plan = mock.create_autospec(nodes.BigFrameNode)
    plan.schema = schemata.ArraySchema(tuple())
    plan.session = None

    # Mock prepare_plan
    mock_executor.prepare_plan = mock.Mock(return_value=plan)

    # Mock _compile
    from bigframes.core.compile.configs import CompileResult

    fake_compiled = CompileResult(
        sql="SELECT 1", sql_schema=[], row_order=None, encoded_type_refs="fake_refs"
    )
    mock_executor._compile = mock.Mock(return_value=fake_compiled)

    # Mock _run_execute_query to fail first time, then succeed
    mock_iterator = mock.Mock()
    mock_iterator.total_rows = 0
    mock_iterator.to_arrow.return_value = pa.Table.from_arrays([], names=[])
    mock_query_job = mock.Mock(spec=bigquery.QueryJob)
    mock_query_job.destination = None

    error = google.cloud.exceptions.BadRequest("failed")
    error.job = mock.Mock(spec=bigquery.QueryJob)  # type: ignore
    error.job.job_id = "failed_job_id"  # type: ignore

    mock_executor._run_execute_query = mock.Mock(
        side_effect=[error, (mock_iterator, mock_query_job)]
    )

    with (
        bigframes.option_context("experiments.sql_compiler", "stable"),
        pytest.warns(UserWarning, match="Falling back to ibis"),
    ):
        mock_executor._execute_plan_gbq(plan, ordered=False, must_create_table=False)

    # Verify labels for both calls
    assert mock_executor._run_execute_query.call_count == 2

    call_1_kwargs = mock_executor._run_execute_query.call_args_list[0][1]
    call_2_kwargs = mock_executor._run_execute_query.call_args_list[1][1]

    label_1 = call_1_kwargs["job_config"].labels["bigframes-compiler"]
    label_2 = call_2_kwargs["job_config"].labels["bigframes-compiler"]

    assert label_1.startswith("sqlglot-")
    assert label_2.startswith("ibis-")
    # Both should have the same compiler_id suffix
    assert label_1.split("-")[1] == label_2.split("-")[1]
