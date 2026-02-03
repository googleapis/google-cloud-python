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

import pytest

import bigframes.bigquery._operations.io
import bigframes.core.sql.io
import bigframes.session


@pytest.fixture
def mock_session():
    return mock.create_autospec(spec=bigframes.session.Session)


@mock.patch("bigframes.bigquery._operations.io._get_table_metadata")
def test_load_data(get_table_metadata_mock, mock_session):
    bigframes.bigquery._operations.io.load_data(
        "my-project.my_dataset.my_table",
        columns={"col1": "INT64", "col2": "STRING"},
        from_files_options={"format": "CSV", "uris": ["gs://bucket/path*"]},
        session=mock_session,
    )
    mock_session.read_gbq_query.assert_called_once()
    generated_sql = mock_session.read_gbq_query.call_args[0][0]
    expected = "LOAD DATA INTO my-project.my_dataset.my_table (col1 INT64, col2 STRING) FROM FILES (format = 'CSV', uris = ['gs://bucket/path*'])"
    assert generated_sql == expected
    get_table_metadata_mock.assert_called_once()
