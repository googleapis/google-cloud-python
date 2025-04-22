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

import datetime

import google.cloud.bigquery as bigquery
import google.cloud.exceptions
import pytest

import bigframes
import bigframes.pandas as bpd
import bigframes.session._io.bigquery


def test_close(session: bigframes.Session):
    # we will create two tables and confirm that they are deleted
    # when the session is closed

    bqclient = session.bqclient

    expiration = (
        datetime.datetime.now(datetime.timezone.utc)
        + bigframes.constants.DEFAULT_EXPIRATION
    )
    full_id_1 = bigframes.session._io.bigquery.create_temp_table(
        session.bqclient,
        session._anon_dataset_manager.allocate_temp_table(),
        expiration,
    )
    full_id_2 = bigframes.session._io.bigquery.create_temp_table(
        session.bqclient,
        session._anon_dataset_manager.allocate_temp_table(),
        expiration,
    )

    # check that the tables were actually created
    assert bqclient.get_table(full_id_1).created is not None
    assert bqclient.get_table(full_id_2).created is not None

    session.close()

    # check that the tables are already deleted
    with pytest.raises(google.cloud.exceptions.NotFound):
        bqclient.delete_table(full_id_1)
    with pytest.raises(google.cloud.exceptions.NotFound):
        bqclient.delete_table(full_id_2)


def test_clean_up_by_session_id():
    # we do this test in a different region in order to avoid
    # overly large amounts of temp tables slowing the test down
    option_context = bigframes.BigQueryOptions()
    option_context.location = "europe-west10"
    session = bigframes.Session(context=option_context)
    session_id = session.session_id

    # we will create two tables and confirm that they are deleted
    # when the session is cleaned up by id
    bqclient = session.bqclient
    dataset = session._anonymous_dataset
    expiration = (
        datetime.datetime.now(datetime.timezone.utc)
        + bigframes.constants.DEFAULT_EXPIRATION
    )
    bigframes.session._io.bigquery.create_temp_table(
        session.bqclient,
        session._anon_dataset_manager.allocate_temp_table(),
        expiration,
    )
    bigframes.session._io.bigquery.create_temp_table(
        session.bqclient,
        session._anon_dataset_manager.allocate_temp_table(),
        expiration,
    )

    # check that some table exists with the expected session_id
    tables_before = bqclient.list_tables(
        dataset,
        max_results=bigframes.session._io.bigquery._LIST_TABLES_LIMIT,
        page_size=bigframes.session._io.bigquery._LIST_TABLES_LIMIT,
    )
    assert any([(session.session_id in table.full_table_id) for table in tables_before])

    bpd.clean_up_by_session_id(
        session_id, location=session._location, project=session._project
    )

    # check that no tables with the session_id are left after cleanup
    tables_after = bqclient.list_tables(
        dataset,
        max_results=bigframes.session._io.bigquery._LIST_TABLES_LIMIT,
        page_size=bigframes.session._io.bigquery._LIST_TABLES_LIMIT,
    )
    assert not any(
        [(session.session_id in table.full_table_id) for table in tables_after]
    )


@pytest.mark.parametrize(
    ("session_creator"),
    [
        pytest.param(bigframes.Session, id="session-constructor"),
        pytest.param(bigframes.connect, id="connect-method"),
    ],
)
@pytest.mark.flaky(retries=3)
def test_clean_up_via_context_manager(session_creator):
    # we will create two tables and confirm that they are deleted
    # when the session is closed
    with session_creator() as session:
        bqclient = session.bqclient

        full_id_1 = session._anon_dataset_manager.create_temp_table(
            [bigquery.SchemaField("a", "INT64")], cluster_cols=[]
        )
        assert session._session_resource_manager is not None
        full_id_2 = session._session_resource_manager.create_temp_table(
            [bigquery.SchemaField("b", "STRING")], cluster_cols=["b"]
        )

        # check that the tables were actually created
        assert bqclient.get_table(full_id_1).created is not None
        assert bqclient.get_table(full_id_2).created is not None

    # check that the tables are already deleted
    with pytest.raises(google.cloud.exceptions.NotFound):
        bqclient.delete_table(full_id_1)
    with pytest.raises(google.cloud.exceptions.NotFound):
        bqclient.delete_table(full_id_2)
