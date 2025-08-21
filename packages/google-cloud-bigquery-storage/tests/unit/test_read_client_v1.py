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

import importlib
from unittest import mock

import google.api_core.exceptions
from google.api_core.gapic_v1 import client_info
from google.auth import credentials
import pytest

from google.cloud.bigquery_storage_v1 import types

PROJECT = "my-project"
SERVICE_ACCOUNT_PROJECT = "project-from-credentials"


@pytest.fixture()
def mock_transport(monkeypatch):
    from google.cloud.bigquery_storage_v1.services.big_query_read import transports

    transport = mock.create_autospec(
        transports.grpc.BigQueryReadGrpcTransport, instance=True
    )

    transport.create_read_session = mock.Mock(name="fake_create_read_session")
    transport.read_rows = mock.Mock(name="fake_read_rows")
    transports.grpc.BigQueryReadGrpcTransport._prep_wrapped_messages(
        transport, client_info.ClientInfo()
    )

    # _credentials property for TPC support
    transport._credentials = ""

    return transport


@pytest.fixture()
def client_under_test(mock_transport):
    from google.cloud import bigquery_storage

    return bigquery_storage.BigQueryReadClient(transport=mock_transport)


def test_constructor_w_client_info():
    from google.cloud import bigquery_storage
    from google.cloud.bigquery_storage_v1.services import big_query_read

    class MyTransport:
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

    transport_class_patcher = mock.patch.object(
        big_query_read.BigQueryReadClient,
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
    # validate test assumptions
    assert client_under_test._transport is mock_transport

    rpc_callable = mock.Mock()
    mock_transport._wrapped_methods[mock_transport.create_read_session] = rpc_callable
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
    rpc_callable.assert_called_once_with(
        expected_session_arg, metadata=mock.ANY, retry=mock.ANY, timeout=mock.ANY
    )


def test_create_read_session_retries_serviceunavailable(
    mock_transport, client_under_test
):
    """Regression test for https://github.com/googleapis/python-bigquery-storage/issues/969."""
    # validate test assumptions
    assert client_under_test._transport is mock_transport

    mock_transport.create_read_session.side_effect = [
        google.api_core.exceptions.ServiceUnavailable("connection reset"),
        google.api_core.exceptions.ServiceUnavailable("connection reset"),
        types.ReadSession(),
    ]
    table = "projects/{}/datasets/{}/tables/{}".format(
        "data-project-id", "dataset_id", "table_id"
    )
    read_session = types.ReadSession()
    read_session.table = table

    # with pytest.raises(google.api_core.exceptions.ServiceUnavailable):
    client_under_test.create_read_session(
        parent="projects/other-project", read_session=read_session
    )

    expected_session_arg = types.CreateReadSessionRequest(
        parent="projects/other-project", read_session=read_session
    )
    expected_call = mock.call(expected_session_arg, metadata=mock.ANY, timeout=mock.ANY)
    mock_transport.create_read_session.assert_has_calls(
        [
            expected_call,
            expected_call,
            expected_call,
        ]
    )


def test_read_rows(mock_transport, client_under_test):
    stream_name = "teststream"
    offset = 0

    client_under_test.read_rows(stream_name)

    expected_request = types.ReadRowsRequest(read_stream=stream_name, offset=offset)
    mock_transport.create_read_session.read_rows(
        expected_request, metadata=mock.ANY, timeout=mock.ANY
    )


@pytest.mark.parametrize(
    "module_under_test",
    ["google.cloud.bigquery_storage_v1", "google.cloud.bigquery_storage_v1beta2"],
)
def test_init_default_client_info(module_under_test):
    from google.api_core.gapic_v1.client_info import METRICS_METADATA_KEY

    mut = importlib.import_module(module_under_test)

    creds = mock.Mock(spec=credentials.Credentials)
    client = mut.BigQueryWriteClient(credentials=creds)

    installed_version = mut.__version__
    expected_client_info = f"gccl/{installed_version}"

    for wrapped_method in client.transport._wrapped_methods.values():
        user_agent = next(
            (
                header_value
                for header, header_value in wrapped_method._metadata
                if header == METRICS_METADATA_KEY
            ),
            None,
        )
        assert user_agent is not None
        assert expected_client_info in user_agent
