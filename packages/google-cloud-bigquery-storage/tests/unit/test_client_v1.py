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

from unittest import mock

from google.api_core.gapic_v1 import client_info
import pytest

from google.cloud.bigquery_storage import types


PROJECT = "my-project"
SERVICE_ACCOUNT_PROJECT = "project-from-credentials"


@pytest.fixture()
def mock_transport(monkeypatch):
    from google.cloud.bigquery_storage_v1.services.big_query_read import transports

    fake_create_session_rpc = mock.Mock(name="create_read_session_rpc")
    fake_read_rows_rpc = mock.Mock(name="read_rows_rpc")

    transport = mock.create_autospec(
        transports.grpc.BigQueryReadGrpcTransport, instance=True
    )

    transport.create_read_session = mock.Mock(name="fake_create_read_session")
    transport.read_rows = mock.Mock(name="fake_read_rows")

    transport._wrapped_methods = {
        transport.create_read_session: fake_create_session_rpc,
        transport.read_rows: fake_read_rows_rpc,
    }

    return transport


@pytest.fixture()
def client_under_test(mock_transport):
    from google.cloud import bigquery_storage

    return bigquery_storage.BigQueryReadClient(transport=mock_transport)


def test_constructor_w_client_info():
    from google.cloud import bigquery_storage

    class MyTransport:
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

    transport_class_patcher = mock.patch.object(
        bigquery_storage.BigQueryReadClient,
        "get_transport_class",
        return_value=MyTransport,
    )

    with transport_class_patcher:
        client_under_test = bigquery_storage.BigQueryReadClient(
            client_info=client_info.ClientInfo(
                client_library_version="test-client-version"
            ),
        )

    transport_client_info = client_under_test._transport.kwargs["client_info"]
    user_agent = transport_client_info.to_user_agent()
    assert "test-client-version" in user_agent


def test_create_read_session(mock_transport, client_under_test):
    assert client_under_test._transport is mock_transport  # sanity check

    table = "projects/{}/datasets/{}/tables/{}".format(
        "data-project-id", "dataset_id", "table_id"
    )

    read_session = types.ReadSession()
    read_session.table = table

    client_under_test.create_read_session(
        parent="projects/other-project", read_session=read_session
    )

    expected_session_arg = types.CreateReadSessionRequest(
        parent="projects/other-project", read_session=read_session
    )
    rpc_callable = mock_transport._wrapped_methods[mock_transport.create_read_session]
    rpc_callable.assert_called_once_with(
        expected_session_arg, metadata=mock.ANY, retry=mock.ANY, timeout=mock.ANY
    )


def test_read_rows(mock_transport, client_under_test):
    stream_name = "teststream"
    offset = 0

    client_under_test.read_rows(stream_name)

    expected_request = types.ReadRowsRequest(read_stream=stream_name, offset=offset)
    mock_transport.create_read_session.read_rows(
        expected_request, metadata=mock.ANY, timeout=mock.ANY
    )
