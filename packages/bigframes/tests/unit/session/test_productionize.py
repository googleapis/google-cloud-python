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


import google.cloud.bigquery
import pytest

import bigframes
import bigframes.core.global_session as global_session
import bigframes.pandas as bpd
from bigframes.session.productionize import (
    ProductionizeBlockedError,
)
from bigframes.testing import mocks


@pytest.fixture(autouse=True)
def setup_session_started():
    """Fixture to pretend a session has already started, skipping location auto-detection."""
    original = bigframes.options.bigquery._session_started
    bigframes.options.bigquery._session_started = True
    yield
    bigframes.options.bigquery._session_started = original


def _setup_mock_table(session, project, dataset, table_id):
    """Helper to register a mock table in the session's bigquery client."""
    table_ref = google.cloud.bigquery.TableReference(
        google.cloud.bigquery.DatasetReference(project, dataset),
        table_id,
    )
    table = google.cloud.bigquery.Table(
        table_ref, (google.cloud.bigquery.SchemaField("col", "INTEGER"),)
    )
    table._properties["location"] = session._location
    table._properties["numRows"] = "10"
    table._properties["type"] = "TABLE"

    # Mock get_table to return this table
    session.bqclient.get_table.return_value = table
    return table


def test_productionize_blocks_downloads_and_execution():
    session = mocks.create_bigquery_session()
    _setup_mock_table(session, "project", "dataset", "table")

    with global_session._GlobalSessionContext(session):
        with bpd.productionize() as pipeline:
            # Create a mock dataframe (backed by a mock table)
            df = bpd.read_gbq("project.dataset.table")

            # 1. to_pandas() should be blocked
            with pytest.raises(
                ProductionizeBlockedError,
                match="Immediate execution/data downloading is disabled",
            ):
                df.to_pandas()

            # 2. shape should be blocked (since it triggers execution to count rows)
            with pytest.raises(
                ProductionizeBlockedError,
                match="Immediate execution/data downloading is disabled",
            ):
                _ = df.shape

            # 3. Lazy operations should succeed
            df_lazy = df.sort_values("col").head()

            # 4. Downloading the lazy result should be blocked
            with pytest.raises(
                ProductionizeBlockedError,
                match="Immediate execution/data downloading is disabled",
            ):
                df_lazy.to_pandas()


def test_productionize_intercepts_to_gbq():
    session = mocks.create_bigquery_session()
    _setup_mock_table(session, "project", "dataset", "table")

    with global_session._GlobalSessionContext(session):
        with bpd.productionize() as pipeline:
            df = bpd.read_gbq("project.dataset.table")

            # to_gbq should NOT raise an error, but instead return successfully
            # and record the write!
            df.to_gbq("project.dataset.output_table", if_exists="replace")

            assert "project.dataset.output_table" in pipeline.recorded_writes

            # Check the recorded write
            array_value, dest_spec = pipeline.recorded_writes[
                "project.dataset.output_table"
            ]
            assert dest_spec.if_exists == "replace"

            # to_sql() should generate the SQL
            sql = pipeline.to_sql()
            assert "CREATE OR REPLACE TABLE `project.dataset.output_table` AS" in sql


def test_productionize_intercepts_udf():
    session = mocks.create_bigquery_session()

    with global_session._GlobalSessionContext(session):
        with bpd.productionize() as pipeline:
            # Define a UDF
            @bpd.udf(input_types=[int], output_type=int, name="my_udf")
            def add_one(x):
                return x + 1

            # The UDF should be recorded under the resolved routine name
            expected_routine_name = "test-project.test_dataset.my_udf"
            assert expected_routine_name in pipeline.recorded_udfs

            # to_sql should include the UDF DDL at the top
            sql = pipeline.to_sql()
            assert (
                "CREATE OR REPLACE FUNCTION `test-project.test_dataset.my_udf`" in sql
            )
            assert sql.strip().startswith("CREATE OR REPLACE FUNCTION")


def test_productionize_blocks_remote_function():
    session = mocks.create_bigquery_session()

    with global_session._GlobalSessionContext(session):
        with bpd.productionize() as pipeline:
            # remote_function should raise an error immediately
            with pytest.raises(
                ProductionizeBlockedError,
                match="Creating remote functions is not supported",
            ):

                @bpd.remote_function(
                    input_types=[int],
                    output_type=int,
                    cloud_function_service_account="test-sa@project.iam.gserviceaccount.com",
                )
                def remote_add_one(x):
                    return x + 1


def test_productionize_parameter():
    session = mocks.create_bigquery_session()
    _setup_mock_table(session, "project", "dataset", "table")

    with global_session._GlobalSessionContext(session):
        with bpd.productionize() as pipeline:
            # Define a parameter
            limit_val = bpd.parameter("limit_val", dtype=int)

            df = bpd.read_gbq("project.dataset.table")
            # Use the parameter in a filter
            df_filtered = df[df["col"] > limit_val]

            # Write the result
            df_filtered.to_gbq("project.dataset.output_table", if_exists="replace")

            # to_sql() should compile the SQL containing @limit_val
            sql = pipeline.to_sql()
            assert "@limit_val" in sql
            # Verify it compiles to a valid comparison
            assert "col` > @limit_val" in sql or "col > @limit_val" in sql


def test_productionize_parameter_dataform(tmp_path):
    import os

    session = mocks.create_bigquery_session()
    _setup_mock_table(session, "project", "dataset", "table")

    with global_session._GlobalSessionContext(session):
        with bpd.productionize() as pipeline:
            limit_val = bpd.parameter("limit_val", dtype=int)
            df = bpd.read_gbq("project.dataset.table")
            df_filtered = df[df["col"] > limit_val]
            df_filtered.to_gbq("project.dataset.output_table", if_exists="replace")

            # Export to Dataform
            target_dir = str(tmp_path)
            pipeline.export_dataform(target_dir)

            # Check the generated .sqlx file
            file_path = os.path.join(target_dir, "definitions", "output_table.sqlx")
            assert os.path.exists(file_path)

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # The parameter @limit_val should be rewritten to ${dataform.projectConfig.vars.limit_val}!
            assert "${dataform.projectConfig.vars.limit_val}" in content
            assert "@limit_val" not in content
