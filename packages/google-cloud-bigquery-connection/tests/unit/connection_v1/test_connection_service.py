# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
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
#

from unittest import mock

import grpc
import math
import pytest

from google import auth
from google.api_core import client_options
from google.api_core import grpc_helpers
from google.auth import credentials
from google.cloud.bigquery.connection_v1.services.connection_service import (
    ConnectionServiceClient,
)
from google.cloud.bigquery.connection_v1.services.connection_service import pagers
from google.cloud.bigquery.connection_v1.services.connection_service import transports
from google.cloud.bigquery.connection_v1.types import connection
from google.cloud.bigquery.connection_v1.types import connection as gcbc_connection
from google.iam.v1 import iam_policy_pb2 as iam_policy  # type: ignore
from google.iam.v1 import options_pb2 as options  # type: ignore
from google.iam.v1 import policy_pb2 as policy  # type: ignore
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.type import expr_pb2 as expr  # type: ignore


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert ConnectionServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        ConnectionServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        ConnectionServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        ConnectionServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        ConnectionServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        ConnectionServiceClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


def test_connection_service_client_from_service_account_file():
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = ConnectionServiceClient.from_service_account_file(
            "dummy/file/path.json"
        )
        assert client._transport._credentials == creds

        client = ConnectionServiceClient.from_service_account_json(
            "dummy/file/path.json"
        )
        assert client._transport._credentials == creds

        assert client._transport._host == "bigqueryconnection.googleapis.com:443"


def test_connection_service_client_client_options():
    # Check that if channel is provided we won't create a new one.
    with mock.patch(
        "google.cloud.bigquery.connection_v1.services.connection_service.ConnectionServiceClient.get_transport_class"
    ) as gtc:
        transport = transports.ConnectionServiceGrpcTransport(
            credentials=credentials.AnonymousCredentials()
        )
        client = ConnectionServiceClient(transport=transport)
        gtc.assert_not_called()

    # Check mTLS is not triggered with empty client options.
    options = client_options.ClientOptions()
    with mock.patch(
        "google.cloud.bigquery.connection_v1.services.connection_service.ConnectionServiceClient.get_transport_class"
    ) as gtc:
        transport = gtc.return_value = mock.MagicMock()
        client = ConnectionServiceClient(client_options=options)
        transport.assert_called_once_with(
            credentials=None, host=client.DEFAULT_ENDPOINT
        )

    # Check mTLS is not triggered if api_endpoint is provided but
    # client_cert_source is None.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch(
        "google.cloud.bigquery.connection_v1.services.connection_service.transports.ConnectionServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = ConnectionServiceClient(client_options=options)
        grpc_transport.assert_called_once_with(
            api_mtls_endpoint=None,
            client_cert_source=None,
            credentials=None,
            host="squid.clam.whelk",
        )

    # Check mTLS is triggered if client_cert_source is provided.
    options = client_options.ClientOptions(
        client_cert_source=client_cert_source_callback
    )
    with mock.patch(
        "google.cloud.bigquery.connection_v1.services.connection_service.transports.ConnectionServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = ConnectionServiceClient(client_options=options)
        grpc_transport.assert_called_once_with(
            api_mtls_endpoint=client.DEFAULT_MTLS_ENDPOINT,
            client_cert_source=client_cert_source_callback,
            credentials=None,
            host=client.DEFAULT_ENDPOINT,
        )

    # Check mTLS is triggered if api_endpoint and client_cert_source are provided.
    options = client_options.ClientOptions(
        api_endpoint="squid.clam.whelk", client_cert_source=client_cert_source_callback
    )
    with mock.patch(
        "google.cloud.bigquery.connection_v1.services.connection_service.transports.ConnectionServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = ConnectionServiceClient(client_options=options)
        grpc_transport.assert_called_once_with(
            api_mtls_endpoint="squid.clam.whelk",
            client_cert_source=client_cert_source_callback,
            credentials=None,
            host="squid.clam.whelk",
        )


def test_connection_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.bigquery.connection_v1.services.connection_service.transports.ConnectionServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = ConnectionServiceClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        grpc_transport.assert_called_once_with(
            api_mtls_endpoint=None,
            client_cert_source=None,
            credentials=None,
            host="squid.clam.whelk",
        )


def test_create_connection(transport: str = "grpc"):
    client = ConnectionServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = gcbc_connection.CreateConnectionRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcbc_connection.Connection(
            name="name_value",
            friendly_name="friendly_name_value",
            description="description_value",
            creation_time=1379,
            last_modified_time=1890,
            has_credential=True,
        )

        response = client.create_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcbc_connection.Connection)
    assert response.name == "name_value"
    assert response.friendly_name == "friendly_name_value"
    assert response.description == "description_value"
    assert response.creation_time == 1379
    assert response.last_modified_time == 1890

    assert response.has_credential is True


def test_create_connection_flattened():
    client = ConnectionServiceClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcbc_connection.Connection()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.create_connection(
            parent="parent_value",
            connection=gcbc_connection.Connection(name="name_value"),
            connection_id="connection_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].connection == gcbc_connection.Connection(name="name_value")
        assert args[0].connection_id == "connection_id_value"


def test_create_connection_flattened_error():
    client = ConnectionServiceClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_connection(
            gcbc_connection.CreateConnectionRequest(),
            parent="parent_value",
            connection=gcbc_connection.Connection(name="name_value"),
            connection_id="connection_id_value",
        )


def test_get_connection(transport: str = "grpc"):
    client = ConnectionServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = connection.GetConnectionRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_connection), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = connection.Connection(
            name="name_value",
            friendly_name="friendly_name_value",
            description="description_value",
            creation_time=1379,
            last_modified_time=1890,
            has_credential=True,
        )

        response = client.get_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, connection.Connection)
    assert response.name == "name_value"
    assert response.friendly_name == "friendly_name_value"
    assert response.description == "description_value"
    assert response.creation_time == 1379
    assert response.last_modified_time == 1890

    assert response.has_credential is True


def test_get_connection_field_headers():
    client = ConnectionServiceClient(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = connection.GetConnectionRequest(name="name/value")

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_connection), "__call__") as call:
        call.return_value = connection.Connection()
        client.get_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value") in kw["metadata"]


def test_get_connection_flattened():
    client = ConnectionServiceClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_connection), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = connection.Connection()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.get_connection(name="name_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_connection_flattened_error():
    client = ConnectionServiceClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_connection(connection.GetConnectionRequest(), name="name_value")


def test_list_connections(transport: str = "grpc"):
    client = ConnectionServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = connection.ListConnectionsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_connections), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = connection.ListConnectionsResponse(
            next_page_token="next_page_token_value"
        )

        response = client.list_connections(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListConnectionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_connections_field_headers():
    client = ConnectionServiceClient(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = connection.ListConnectionsRequest(parent="parent/value")

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_connections), "__call__"
    ) as call:
        call.return_value = connection.ListConnectionsResponse()
        client.list_connections(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value") in kw["metadata"]


def test_list_connections_pager():
    client = ConnectionServiceClient(credentials=credentials.AnonymousCredentials)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_connections), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            connection.ListConnectionsResponse(
                connections=[
                    connection.Connection(),
                    connection.Connection(),
                    connection.Connection(),
                ],
                next_page_token="abc",
            ),
            connection.ListConnectionsResponse(connections=[], next_page_token="def"),
            connection.ListConnectionsResponse(
                connections=[connection.Connection()], next_page_token="ghi"
            ),
            connection.ListConnectionsResponse(
                connections=[connection.Connection(), connection.Connection()]
            ),
            RuntimeError,
        )
        results = [i for i in client.list_connections(request={})]
        assert len(results) == 6
        assert all(isinstance(i, connection.Connection) for i in results)


def test_list_connections_pages():
    client = ConnectionServiceClient(credentials=credentials.AnonymousCredentials)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_connections), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            connection.ListConnectionsResponse(
                connections=[
                    connection.Connection(),
                    connection.Connection(),
                    connection.Connection(),
                ],
                next_page_token="abc",
            ),
            connection.ListConnectionsResponse(connections=[], next_page_token="def"),
            connection.ListConnectionsResponse(
                connections=[connection.Connection()], next_page_token="ghi"
            ),
            connection.ListConnectionsResponse(
                connections=[connection.Connection(), connection.Connection()]
            ),
            RuntimeError,
        )
        pages = list(client.list_connections(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_update_connection(transport: str = "grpc"):
    client = ConnectionServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = gcbc_connection.UpdateConnectionRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcbc_connection.Connection(
            name="name_value",
            friendly_name="friendly_name_value",
            description="description_value",
            creation_time=1379,
            last_modified_time=1890,
            has_credential=True,
        )

        response = client.update_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcbc_connection.Connection)
    assert response.name == "name_value"
    assert response.friendly_name == "friendly_name_value"
    assert response.description == "description_value"
    assert response.creation_time == 1379
    assert response.last_modified_time == 1890

    assert response.has_credential is True


def test_update_connection_flattened():
    client = ConnectionServiceClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcbc_connection.Connection()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.update_connection(
            name="name_value",
            connection=gcbc_connection.Connection(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].connection == gcbc_connection.Connection(name="name_value")
        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


def test_update_connection_flattened_error():
    client = ConnectionServiceClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_connection(
            gcbc_connection.UpdateConnectionRequest(),
            name="name_value",
            connection=gcbc_connection.Connection(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


def test_delete_connection(transport: str = "grpc"):
    client = ConnectionServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = connection.DeleteConnectionRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_connection_flattened():
    client = ConnectionServiceClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.delete_connection(name="name_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_connection_flattened_error():
    client = ConnectionServiceClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_connection(
            connection.DeleteConnectionRequest(), name="name_value"
        )


def test_get_iam_policy(transport: str = "grpc"):
    client = ConnectionServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy.GetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy(version=774, etag=b"etag_blob")

        response = client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy.Policy)
    assert response.version == 774
    assert response.etag == b"etag_blob"


def test_get_iam_policy_from_dict():
    client = ConnectionServiceClient(credentials=credentials.AnonymousCredentials())
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy()

        response = client.get_iam_policy(
            request={
                "resource": "resource_value",
                "options": options.GetPolicyOptions(requested_policy_version=2598),
            }
        )
        call.assert_called()


def test_get_iam_policy_flattened():
    client = ConnectionServiceClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.get_iam_policy(resource="resource_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].resource == "resource_value"


def test_get_iam_policy_flattened_error():
    client = ConnectionServiceClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_iam_policy(
            iam_policy.GetIamPolicyRequest(), resource="resource_value"
        )


def test_set_iam_policy(transport: str = "grpc"):
    client = ConnectionServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy.SetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy(version=774, etag=b"etag_blob")

        response = client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy.Policy)
    assert response.version == 774
    assert response.etag == b"etag_blob"


def test_set_iam_policy_from_dict():
    client = ConnectionServiceClient(credentials=credentials.AnonymousCredentials())
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy()

        response = client.set_iam_policy(
            request={"resource": "resource_value", "policy": policy.Policy(version=774)}
        )
        call.assert_called()


def test_set_iam_policy_flattened():
    client = ConnectionServiceClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.set_iam_policy(resource="resource_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].resource == "resource_value"


def test_set_iam_policy_flattened_error():
    client = ConnectionServiceClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_iam_policy(
            iam_policy.SetIamPolicyRequest(), resource="resource_value"
        )


def test_test_iam_permissions(transport: str = "grpc"):
    client = ConnectionServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy.TestIamPermissionsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy.TestIamPermissionsResponse(
            permissions=["permissions_value"]
        )

        response = client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy.TestIamPermissionsResponse)
    assert response.permissions == ["permissions_value"]


def test_test_iam_permissions_from_dict():
    client = ConnectionServiceClient(credentials=credentials.AnonymousCredentials())
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy.TestIamPermissionsResponse()

        response = client.test_iam_permissions(
            request={"resource": "resource_value", "permissions": ["permissions_value"]}
        )
        call.assert_called()


def test_test_iam_permissions_flattened():
    client = ConnectionServiceClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy.TestIamPermissionsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.test_iam_permissions(
            resource="resource_value", permissions=["permissions_value"]
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].resource == "resource_value"
        assert args[0].permissions == ["permissions_value"]


def test_test_iam_permissions_flattened_error():
    client = ConnectionServiceClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.test_iam_permissions(
            iam_policy.TestIamPermissionsRequest(),
            resource="resource_value",
            permissions=["permissions_value"],
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.ConnectionServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials()
    )
    with pytest.raises(ValueError):
        client = ConnectionServiceClient(
            credentials=credentials.AnonymousCredentials(), transport=transport
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ConnectionServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials()
    )
    client = ConnectionServiceClient(transport=transport)
    assert client._transport is transport


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = ConnectionServiceClient(credentials=credentials.AnonymousCredentials())
    assert isinstance(client._transport, transports.ConnectionServiceGrpcTransport)


def test_connection_service_base_transport():
    # Instantiate the base transport.
    transport = transports.ConnectionServiceTransport(
        credentials=credentials.AnonymousCredentials()
    )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_connection",
        "get_connection",
        "list_connections",
        "update_connection",
        "delete_connection",
        "get_iam_policy",
        "set_iam_policy",
        "test_iam_permissions",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_connection_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        ConnectionServiceClient()
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/bigquery",
                "https://www.googleapis.com/auth/cloud-platform",
            )
        )


def test_connection_service_host_no_port():
    client = ConnectionServiceClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="bigqueryconnection.googleapis.com"
        ),
        transport="grpc",
    )
    assert client._transport._host == "bigqueryconnection.googleapis.com:443"


def test_connection_service_host_with_port():
    client = ConnectionServiceClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="bigqueryconnection.googleapis.com:8000"
        ),
        transport="grpc",
    )
    assert client._transport._host == "bigqueryconnection.googleapis.com:8000"


def test_connection_service_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")

    # Check that if channel is provided, mtls endpoint and client_cert_source
    # won't be used.
    callback = mock.MagicMock()
    transport = transports.ConnectionServiceGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=callback,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert not callback.called


@mock.patch("grpc.ssl_channel_credentials", autospec=True)
@mock.patch("google.api_core.grpc_helpers.create_channel", autospec=True)
def test_connection_service_grpc_transport_channel_mtls_with_client_cert_source(
    grpc_create_channel, grpc_ssl_channel_cred
):
    # Check that if channel is None, but api_mtls_endpoint and client_cert_source
    # are provided, then a mTLS channel will be created.
    mock_cred = mock.Mock()

    mock_ssl_cred = mock.Mock()
    grpc_ssl_channel_cred.return_value = mock_ssl_cred

    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    transport = transports.ConnectionServiceGrpcTransport(
        host="squid.clam.whelk",
        credentials=mock_cred,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=client_cert_source_callback,
    )
    grpc_ssl_channel_cred.assert_called_once_with(
        certificate_chain=b"cert bytes", private_key=b"key bytes"
    )
    grpc_create_channel.assert_called_once_with(
        "mtls.squid.clam.whelk:443",
        credentials=mock_cred,
        ssl_credentials=mock_ssl_cred,
        scopes=(
            "https://www.googleapis.com/auth/bigquery",
            "https://www.googleapis.com/auth/cloud-platform",
        ),
    )
    assert transport.grpc_channel == mock_grpc_channel


@pytest.mark.parametrize(
    "api_mtls_endpoint", ["mtls.squid.clam.whelk", "mtls.squid.clam.whelk:443"]
)
@mock.patch("google.api_core.grpc_helpers.create_channel", autospec=True)
def test_connection_service_grpc_transport_channel_mtls_with_adc(
    grpc_create_channel, api_mtls_endpoint
):
    # Check that if channel and client_cert_source are None, but api_mtls_endpoint
    # is provided, then a mTLS channel will be created with SSL ADC.
    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    # Mock google.auth.transport.grpc.SslCredentials class.
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        mock_cred = mock.Mock()
        transport = transports.ConnectionServiceGrpcTransport(
            host="squid.clam.whelk",
            credentials=mock_cred,
            api_mtls_endpoint=api_mtls_endpoint,
            client_cert_source=None,
        )
        grpc_create_channel.assert_called_once_with(
            "mtls.squid.clam.whelk:443",
            credentials=mock_cred,
            ssl_credentials=mock_ssl_cred,
            scopes=(
                "https://www.googleapis.com/auth/bigquery",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
        )
        assert transport.grpc_channel == mock_grpc_channel


def test_connection_path():
    project = "squid"
    location = "clam"
    connection = "whelk"

    expected = "projects/{project}/locations/{location}/connections/{connection}".format(
        project=project, location=location, connection=connection
    )
    actual = ConnectionServiceClient.connection_path(project, location, connection)
    assert expected == actual


def test_parse_connection_path():
    expected = {"project": "octopus", "location": "oyster", "connection": "nudibranch"}
    path = ConnectionServiceClient.connection_path(**expected)

    # Check that the path construction is reversible.
    actual = ConnectionServiceClient.parse_connection_path(path)
    assert expected == actual
