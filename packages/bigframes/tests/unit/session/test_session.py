# Copyright 2023 Google LLC
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

import os
from unittest import mock

import google.api_core.exceptions
import pytest

import bigframes

from .. import resources


@pytest.mark.parametrize("missing_parts_table_id", [(""), ("table")])
def test_read_gbq_missing_parts(missing_parts_table_id):
    session = resources.create_bigquery_session()

    with pytest.raises(ValueError):
        session.read_gbq(missing_parts_table_id)


@pytest.mark.parametrize(
    "not_found_table_id",
    [("unknown.dataset.table"), ("project.unknown.table"), ("project.dataset.unknown")],
)
def test_read_gdb_not_found_tables(not_found_table_id):
    bqclient = mock.create_autospec(google.cloud.bigquery.Client, instance=True)
    bqclient.project = "test-project"
    bqclient.get_table.side_effect = google.api_core.exceptions.NotFound(
        "table not found"
    )
    session = resources.create_bigquery_session(bqclient=bqclient)

    with pytest.raises(google.api_core.exceptions.NotFound):
        session.read_gbq(not_found_table_id)


@mock.patch.dict(os.environ, {}, clear=True)
def test_session_init_fails_with_no_project():
    with pytest.raises(
        ValueError, match="Project must be set to initialize BigQuery client."
    ):
        bigframes.Session(
            bigframes.BigQueryOptions(
                credentials=mock.Mock(spec=google.auth.credentials.Credentials)
            )
        )
