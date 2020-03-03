# Copyright 2018 Google LLC
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

from google.api_core.gapic_v1 import client_info
import mock
import pytest

from google.cloud.bigquery_storage_v1 import types


PROJECT = "my-project"
SERVICE_ACCOUNT_PROJECT = "project-from-credentials"


@pytest.fixture()
def mock_transport(monkeypatch):
    from google.cloud.bigquery_storage_v1.gapic.transports import (
        big_query_read_grpc_transport,
    )

    transport = mock.create_autospec(
        big_query_read_grpc_transport.BigQueryReadGrpcTransport
    )
    return transport


@pytest.fixture()
def client_under_test(mock_transport):
    from google.cloud.bigquery_storage_v1 import client

    # The mock is detected as a callable. By creating a real callable here, the
    # mock can still be used to verify RPCs.
    def transport_callable(credentials=None, default_class=None, address=None):
        return mock_transport

    return client.BigQueryReadClient(transport=transport_callable)


def test_constructor_w_client_info(mock_transport):
    from google.cloud.bigquery_storage_v1 import client

    def transport_callable(credentials=None, default_class=None, address=None):
        return mock_transport

    client_under_test = client.BigQueryReadClient(
        transport=transport_callable,
        client_info=client_info.ClientInfo(
            client_library_version="test-client-version"
        ),
    )

    user_agent = client_under_test._client_info.to_user_agent()
    assert "test-client-version" in user_agent


def test_create_read_session(mock_transport, client_under_test):
    table = "projects/{}/datasets/{}/tables/{}".format(
        "data-project-id", "dataset_id", "table_id"
    )

    read_session = types.ReadSession()
    read_session.table = table

    client_under_test.create_read_session("projects/other-project", read_session)

    expected_request = types.CreateReadSessionRequest(
        parent="projects/other-project", read_session=read_session
    )
    mock_transport.create_read_session.assert_called_once_with(
        expected_request, metadata=mock.ANY, timeout=mock.ANY
    )


def test_read_rows(mock_transport, client_under_test):
    stream_name = "teststream"
    offset = 0

    client_under_test.read_rows(stream_name)

    expected_request = types.ReadRowsRequest(read_stream=stream_name, offset=offset)
    mock_transport.create_read_session.read_rows(
        expected_request, metadata=mock.ANY, timeout=mock.ANY
    )
