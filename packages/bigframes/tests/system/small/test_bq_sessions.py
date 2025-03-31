# Copyright 2025 Google LLC
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

from concurrent.futures import ThreadPoolExecutor
import time

import google
import google.api_core.exceptions
import google.cloud
from google.cloud import bigquery
import pytest

from bigframes.session import bigquery_session

TEST_SCHEMA = [
    bigquery.SchemaField("bool field", "BOOLEAN"),
    bigquery.SchemaField("string field", "STRING"),
    bigquery.SchemaField("float array_field", "FLOAT", mode="REPEATED"),
    bigquery.SchemaField(
        "struct field",
        "RECORD",
        fields=(bigquery.SchemaField("int subfield", "INTEGER"),),
    ),
]


@pytest.fixture
def session_resource_manager(
    bigquery_client,
) -> bigquery_session.SessionResourceManager:
    return bigquery_session.SessionResourceManager(bigquery_client, "US")


def test_bq_session_create_temp_table_clustered(bigquery_client: bigquery.Client):
    session_resource_manager = bigquery_session.SessionResourceManager(
        bigquery_client, "US"
    )
    cluster_cols = ["string field", "bool field"]

    session_table_ref = session_resource_manager.create_temp_table(
        TEST_SCHEMA, cluster_cols=cluster_cols
    )
    session_resource_manager._keep_session_alive()

    result_table = bigquery_client.get_table(session_table_ref)
    assert result_table.schema == TEST_SCHEMA
    assert result_table.clustering_fields == cluster_cols

    session_resource_manager.close()
    with pytest.raises(google.api_core.exceptions.NotFound):
        # It may take time for the underlying tables to get cleaned up after
        # closing the session, so wait at least 1 minute to check.
        for _ in range(6):
            bigquery_client.get_table(session_table_ref)
            time.sleep(10)


def test_bq_session_create_multi_temp_tables(bigquery_client: bigquery.Client):
    session_resource_manager = bigquery_session.SessionResourceManager(
        bigquery_client, "US"
    )

    def create_table():
        return session_resource_manager.create_temp_table(TEST_SCHEMA)

    with ThreadPoolExecutor() as executor:
        results = [executor.submit(create_table) for i in range(10)]

    for future in results:
        table = future.result()
        result_table = bigquery_client.get_table(table)
        assert result_table.schema == TEST_SCHEMA

    session_resource_manager.close()
