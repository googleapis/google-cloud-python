# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
import math
import os

from google.api_core import (
    future,
    gapic_v1,
    grpc_helpers,
    grpc_helpers_async,
    operation,
    operations_v1,
    path_template,
)
from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import operation_async  # type: ignore
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import any_pb2  # type: ignore
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
import grpc
from grpc.experimental import aio
import mock
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest

from google.cloud.vmmigration_v1.services.vm_migration import (
    VmMigrationAsyncClient,
    VmMigrationClient,
    pagers,
    transports,
)
from google.cloud.vmmigration_v1.types import vmmigration


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert VmMigrationClient._get_default_mtls_endpoint(None) is None
    assert (
        VmMigrationClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    )
    assert (
        VmMigrationClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        VmMigrationClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        VmMigrationClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert VmMigrationClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (VmMigrationClient, "grpc"),
        (VmMigrationAsyncClient, "grpc_asyncio"),
    ],
)
def test_vm_migration_client_from_service_account_info(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == ("vmmigration.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.VmMigrationGrpcTransport, "grpc"),
        (transports.VmMigrationGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_vm_migration_client_service_account_always_use_jwt(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (VmMigrationClient, "grpc"),
        (VmMigrationAsyncClient, "grpc_asyncio"),
    ],
)
def test_vm_migration_client_from_service_account_file(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == ("vmmigration.googleapis.com:443")


def test_vm_migration_client_get_transport_class():
    transport = VmMigrationClient.get_transport_class()
    available_transports = [
        transports.VmMigrationGrpcTransport,
    ]
    assert transport in available_transports

    transport = VmMigrationClient.get_transport_class("grpc")
    assert transport == transports.VmMigrationGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (VmMigrationClient, transports.VmMigrationGrpcTransport, "grpc"),
        (
            VmMigrationAsyncClient,
            transports.VmMigrationGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    VmMigrationClient, "DEFAULT_ENDPOINT", modify_default_endpoint(VmMigrationClient)
)
@mock.patch.object(
    VmMigrationAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(VmMigrationAsyncClient),
)
def test_vm_migration_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(VmMigrationClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(VmMigrationClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(transport=transport_name, client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class(transport=transport_name)

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError):
            client = client_class(transport=transport_name)

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (VmMigrationClient, transports.VmMigrationGrpcTransport, "grpc", "true"),
        (
            VmMigrationAsyncClient,
            transports.VmMigrationGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (VmMigrationClient, transports.VmMigrationGrpcTransport, "grpc", "false"),
        (
            VmMigrationAsyncClient,
            transports.VmMigrationGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    VmMigrationClient, "DEFAULT_ENDPOINT", modify_default_endpoint(VmMigrationClient)
)
@mock.patch.object(
    VmMigrationAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(VmMigrationAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_vm_migration_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options, transport=transport_name)

            if use_client_cert_env == "false":
                expected_client_cert_source = None
                expected_host = client.DEFAULT_ENDPOINT
            else:
                expected_client_cert_source = client_cert_source_callback
                expected_host = client.DEFAULT_MTLS_ENDPOINT

            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=expected_host,
                scopes=None,
                client_cert_source_for_mtls=expected_client_cert_source,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
            )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                with mock.patch(
                    "google.auth.transport.mtls.default_client_cert_source",
                    return_value=client_cert_source_callback,
                ):
                    if use_client_cert_env == "false":
                        expected_host = client.DEFAULT_ENDPOINT
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class(transport=transport_name)
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                        always_use_jwt_access=True,
                    )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=False,
            ):
                patched.return_value = None
                client = client_class(transport=transport_name)
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_ENDPOINT,
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                )


@pytest.mark.parametrize("client_class", [VmMigrationClient, VmMigrationAsyncClient])
@mock.patch.object(
    VmMigrationClient, "DEFAULT_ENDPOINT", modify_default_endpoint(VmMigrationClient)
)
@mock.patch.object(
    VmMigrationAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(VmMigrationAsyncClient),
)
def test_vm_migration_client_get_mtls_endpoint_and_cert_source(client_class):
    mock_client_cert_source = mock.Mock()

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "true".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source == mock_client_cert_source

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "false".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        mock_client_cert_source = mock.Mock()
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert doesn't exist.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=False,
        ):
            api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
            assert api_endpoint == client_class.DEFAULT_ENDPOINT
            assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert exists.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=True,
        ):
            with mock.patch(
                "google.auth.transport.mtls.default_client_cert_source",
                return_value=mock_client_cert_source,
            ):
                (
                    api_endpoint,
                    cert_source,
                ) = client_class.get_mtls_endpoint_and_cert_source()
                assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
                assert cert_source == mock_client_cert_source


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (VmMigrationClient, transports.VmMigrationGrpcTransport, "grpc"),
        (
            VmMigrationAsyncClient,
            transports.VmMigrationGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_vm_migration_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(
        scopes=["1", "2"],
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (VmMigrationClient, transports.VmMigrationGrpcTransport, "grpc", grpc_helpers),
        (
            VmMigrationAsyncClient,
            transports.VmMigrationGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_vm_migration_client_client_options_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )


def test_vm_migration_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.vmmigration_v1.services.vm_migration.transports.VmMigrationGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = VmMigrationClient(client_options={"api_endpoint": "squid.clam.whelk"})
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (VmMigrationClient, transports.VmMigrationGrpcTransport, "grpc", grpc_helpers),
        (
            VmMigrationAsyncClient,
            transports.VmMigrationGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_vm_migration_client_create_channel_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )

    # test that the credentials from file are saved and used as the credentials.
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel"
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        file_creds = ga_credentials.AnonymousCredentials()
        load_creds.return_value = (file_creds, None)
        adc.return_value = (creds, None)
        client = client_class(client_options=options, transport=transport_name)
        create_channel.assert_called_with(
            "vmmigration.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="vmmigration.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.ListSourcesRequest,
        dict,
    ],
)
def test_list_sources(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_sources), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.ListSourcesResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_sources(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.ListSourcesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSourcesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_sources_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_sources), "__call__") as call:
        client.list_sources()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.ListSourcesRequest()


@pytest.mark.asyncio
async def test_list_sources_async(
    transport: str = "grpc_asyncio", request_type=vmmigration.ListSourcesRequest
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_sources), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.ListSourcesResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_sources(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.ListSourcesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSourcesAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_sources_async_from_dict():
    await test_list_sources_async(request_type=dict)


def test_list_sources_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.ListSourcesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_sources), "__call__") as call:
        call.return_value = vmmigration.ListSourcesResponse()
        client.list_sources(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_sources_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.ListSourcesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_sources), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.ListSourcesResponse()
        )
        await client.list_sources(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


def test_list_sources_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_sources), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.ListSourcesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_sources(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_sources_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_sources(
            vmmigration.ListSourcesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_sources_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_sources), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.ListSourcesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.ListSourcesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_sources(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_sources_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_sources(
            vmmigration.ListSourcesRequest(),
            parent="parent_value",
        )


def test_list_sources_pager(transport_name: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_sources), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            vmmigration.ListSourcesResponse(
                sources=[
                    vmmigration.Source(),
                    vmmigration.Source(),
                    vmmigration.Source(),
                ],
                next_page_token="abc",
            ),
            vmmigration.ListSourcesResponse(
                sources=[],
                next_page_token="def",
            ),
            vmmigration.ListSourcesResponse(
                sources=[
                    vmmigration.Source(),
                ],
                next_page_token="ghi",
            ),
            vmmigration.ListSourcesResponse(
                sources=[
                    vmmigration.Source(),
                    vmmigration.Source(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_sources(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, vmmigration.Source) for i in results)


def test_list_sources_pages(transport_name: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_sources), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            vmmigration.ListSourcesResponse(
                sources=[
                    vmmigration.Source(),
                    vmmigration.Source(),
                    vmmigration.Source(),
                ],
                next_page_token="abc",
            ),
            vmmigration.ListSourcesResponse(
                sources=[],
                next_page_token="def",
            ),
            vmmigration.ListSourcesResponse(
                sources=[
                    vmmigration.Source(),
                ],
                next_page_token="ghi",
            ),
            vmmigration.ListSourcesResponse(
                sources=[
                    vmmigration.Source(),
                    vmmigration.Source(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_sources(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_sources_async_pager():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_sources), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            vmmigration.ListSourcesResponse(
                sources=[
                    vmmigration.Source(),
                    vmmigration.Source(),
                    vmmigration.Source(),
                ],
                next_page_token="abc",
            ),
            vmmigration.ListSourcesResponse(
                sources=[],
                next_page_token="def",
            ),
            vmmigration.ListSourcesResponse(
                sources=[
                    vmmigration.Source(),
                ],
                next_page_token="ghi",
            ),
            vmmigration.ListSourcesResponse(
                sources=[
                    vmmigration.Source(),
                    vmmigration.Source(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_sources(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, vmmigration.Source) for i in responses)


@pytest.mark.asyncio
async def test_list_sources_async_pages():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_sources), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            vmmigration.ListSourcesResponse(
                sources=[
                    vmmigration.Source(),
                    vmmigration.Source(),
                    vmmigration.Source(),
                ],
                next_page_token="abc",
            ),
            vmmigration.ListSourcesResponse(
                sources=[],
                next_page_token="def",
            ),
            vmmigration.ListSourcesResponse(
                sources=[
                    vmmigration.Source(),
                ],
                next_page_token="ghi",
            ),
            vmmigration.ListSourcesResponse(
                sources=[
                    vmmigration.Source(),
                    vmmigration.Source(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_sources(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.GetSourceRequest,
        dict,
    ],
)
def test_get_source(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_source), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.Source(
            name="name_value",
            description="description_value",
            vmware=vmmigration.VmwareSourceDetails(username="username_value"),
        )
        response = client.get_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.GetSourceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, vmmigration.Source)
    assert response.name == "name_value"
    assert response.description == "description_value"


def test_get_source_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_source), "__call__") as call:
        client.get_source()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.GetSourceRequest()


@pytest.mark.asyncio
async def test_get_source_async(
    transport: str = "grpc_asyncio", request_type=vmmigration.GetSourceRequest
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_source), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.Source(
                name="name_value",
                description="description_value",
            )
        )
        response = await client.get_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.GetSourceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, vmmigration.Source)
    assert response.name == "name_value"
    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_get_source_async_from_dict():
    await test_get_source_async(request_type=dict)


def test_get_source_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.GetSourceRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_source), "__call__") as call:
        call.return_value = vmmigration.Source()
        client.get_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_source_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.GetSourceRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_source), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(vmmigration.Source())
        await client.get_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


def test_get_source_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_source), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.Source()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_source(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_source_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_source(
            vmmigration.GetSourceRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_source_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_source), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.Source()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(vmmigration.Source())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_source(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_source_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_source(
            vmmigration.GetSourceRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.CreateSourceRequest,
        dict,
    ],
)
def test_create_source(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_source), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.CreateSourceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_source_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_source), "__call__") as call:
        client.create_source()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.CreateSourceRequest()


@pytest.mark.asyncio
async def test_create_source_async(
    transport: str = "grpc_asyncio", request_type=vmmigration.CreateSourceRequest
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_source), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.CreateSourceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_source_async_from_dict():
    await test_create_source_async(request_type=dict)


def test_create_source_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.CreateSourceRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_source), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_source_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.CreateSourceRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_source), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


def test_create_source_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_source), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_source(
            parent="parent_value",
            source=vmmigration.Source(
                vmware=vmmigration.VmwareSourceDetails(username="username_value")
            ),
            source_id="source_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].source
        mock_val = vmmigration.Source(
            vmware=vmmigration.VmwareSourceDetails(username="username_value")
        )
        assert arg == mock_val
        arg = args[0].source_id
        mock_val = "source_id_value"
        assert arg == mock_val


def test_create_source_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_source(
            vmmigration.CreateSourceRequest(),
            parent="parent_value",
            source=vmmigration.Source(
                vmware=vmmigration.VmwareSourceDetails(username="username_value")
            ),
            source_id="source_id_value",
        )


@pytest.mark.asyncio
async def test_create_source_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_source), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_source(
            parent="parent_value",
            source=vmmigration.Source(
                vmware=vmmigration.VmwareSourceDetails(username="username_value")
            ),
            source_id="source_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].source
        mock_val = vmmigration.Source(
            vmware=vmmigration.VmwareSourceDetails(username="username_value")
        )
        assert arg == mock_val
        arg = args[0].source_id
        mock_val = "source_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_source_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_source(
            vmmigration.CreateSourceRequest(),
            parent="parent_value",
            source=vmmigration.Source(
                vmware=vmmigration.VmwareSourceDetails(username="username_value")
            ),
            source_id="source_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.UpdateSourceRequest,
        dict,
    ],
)
def test_update_source(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_source), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.UpdateSourceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_source_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_source), "__call__") as call:
        client.update_source()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.UpdateSourceRequest()


@pytest.mark.asyncio
async def test_update_source_async(
    transport: str = "grpc_asyncio", request_type=vmmigration.UpdateSourceRequest
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_source), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.UpdateSourceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_source_async_from_dict():
    await test_update_source_async(request_type=dict)


def test_update_source_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.UpdateSourceRequest()

    request.source.name = "source.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_source), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "source.name=source.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_source_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.UpdateSourceRequest()

    request.source.name = "source.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_source), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "source.name=source.name/value",
    ) in kw["metadata"]


def test_update_source_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_source), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_source(
            source=vmmigration.Source(
                vmware=vmmigration.VmwareSourceDetails(username="username_value")
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].source
        mock_val = vmmigration.Source(
            vmware=vmmigration.VmwareSourceDetails(username="username_value")
        )
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_source_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_source(
            vmmigration.UpdateSourceRequest(),
            source=vmmigration.Source(
                vmware=vmmigration.VmwareSourceDetails(username="username_value")
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_source_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_source), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_source(
            source=vmmigration.Source(
                vmware=vmmigration.VmwareSourceDetails(username="username_value")
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].source
        mock_val = vmmigration.Source(
            vmware=vmmigration.VmwareSourceDetails(username="username_value")
        )
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_source_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_source(
            vmmigration.UpdateSourceRequest(),
            source=vmmigration.Source(
                vmware=vmmigration.VmwareSourceDetails(username="username_value")
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.DeleteSourceRequest,
        dict,
    ],
)
def test_delete_source(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_source), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.DeleteSourceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_source_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_source), "__call__") as call:
        client.delete_source()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.DeleteSourceRequest()


@pytest.mark.asyncio
async def test_delete_source_async(
    transport: str = "grpc_asyncio", request_type=vmmigration.DeleteSourceRequest
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_source), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.DeleteSourceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_source_async_from_dict():
    await test_delete_source_async(request_type=dict)


def test_delete_source_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.DeleteSourceRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_source), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_source_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.DeleteSourceRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_source), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_source(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


def test_delete_source_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_source), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_source(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_source_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_source(
            vmmigration.DeleteSourceRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_source_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_source), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_source(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_source_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_source(
            vmmigration.DeleteSourceRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.FetchInventoryRequest,
        dict,
    ],
)
def test_fetch_inventory(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_inventory), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.FetchInventoryResponse(
            vmware_vms=vmmigration.VmwareVmsDetails(
                details=[vmmigration.VmwareVmDetails(vm_id="vm_id_value")]
            ),
        )
        response = client.fetch_inventory(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.FetchInventoryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, vmmigration.FetchInventoryResponse)


def test_fetch_inventory_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_inventory), "__call__") as call:
        client.fetch_inventory()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.FetchInventoryRequest()


@pytest.mark.asyncio
async def test_fetch_inventory_async(
    transport: str = "grpc_asyncio", request_type=vmmigration.FetchInventoryRequest
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_inventory), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.FetchInventoryResponse()
        )
        response = await client.fetch_inventory(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.FetchInventoryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, vmmigration.FetchInventoryResponse)


@pytest.mark.asyncio
async def test_fetch_inventory_async_from_dict():
    await test_fetch_inventory_async(request_type=dict)


def test_fetch_inventory_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.FetchInventoryRequest()

    request.source = "source/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_inventory), "__call__") as call:
        call.return_value = vmmigration.FetchInventoryResponse()
        client.fetch_inventory(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "source=source/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_fetch_inventory_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.FetchInventoryRequest()

    request.source = "source/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_inventory), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.FetchInventoryResponse()
        )
        await client.fetch_inventory(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "source=source/value",
    ) in kw["metadata"]


def test_fetch_inventory_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_inventory), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.FetchInventoryResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.fetch_inventory(
            source="source_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].source
        mock_val = "source_value"
        assert arg == mock_val


def test_fetch_inventory_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.fetch_inventory(
            vmmigration.FetchInventoryRequest(),
            source="source_value",
        )


@pytest.mark.asyncio
async def test_fetch_inventory_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_inventory), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.FetchInventoryResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.FetchInventoryResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.fetch_inventory(
            source="source_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].source
        mock_val = "source_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_fetch_inventory_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.fetch_inventory(
            vmmigration.FetchInventoryRequest(),
            source="source_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.ListUtilizationReportsRequest,
        dict,
    ],
)
def test_list_utilization_reports(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_utilization_reports), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.ListUtilizationReportsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_utilization_reports(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.ListUtilizationReportsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListUtilizationReportsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_utilization_reports_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_utilization_reports), "__call__"
    ) as call:
        client.list_utilization_reports()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.ListUtilizationReportsRequest()


@pytest.mark.asyncio
async def test_list_utilization_reports_async(
    transport: str = "grpc_asyncio",
    request_type=vmmigration.ListUtilizationReportsRequest,
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_utilization_reports), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.ListUtilizationReportsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_utilization_reports(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.ListUtilizationReportsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListUtilizationReportsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_utilization_reports_async_from_dict():
    await test_list_utilization_reports_async(request_type=dict)


def test_list_utilization_reports_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.ListUtilizationReportsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_utilization_reports), "__call__"
    ) as call:
        call.return_value = vmmigration.ListUtilizationReportsResponse()
        client.list_utilization_reports(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_utilization_reports_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.ListUtilizationReportsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_utilization_reports), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.ListUtilizationReportsResponse()
        )
        await client.list_utilization_reports(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


def test_list_utilization_reports_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_utilization_reports), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.ListUtilizationReportsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_utilization_reports(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_utilization_reports_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_utilization_reports(
            vmmigration.ListUtilizationReportsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_utilization_reports_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_utilization_reports), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.ListUtilizationReportsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.ListUtilizationReportsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_utilization_reports(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_utilization_reports_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_utilization_reports(
            vmmigration.ListUtilizationReportsRequest(),
            parent="parent_value",
        )


def test_list_utilization_reports_pager(transport_name: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_utilization_reports), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            vmmigration.ListUtilizationReportsResponse(
                utilization_reports=[
                    vmmigration.UtilizationReport(),
                    vmmigration.UtilizationReport(),
                    vmmigration.UtilizationReport(),
                ],
                next_page_token="abc",
            ),
            vmmigration.ListUtilizationReportsResponse(
                utilization_reports=[],
                next_page_token="def",
            ),
            vmmigration.ListUtilizationReportsResponse(
                utilization_reports=[
                    vmmigration.UtilizationReport(),
                ],
                next_page_token="ghi",
            ),
            vmmigration.ListUtilizationReportsResponse(
                utilization_reports=[
                    vmmigration.UtilizationReport(),
                    vmmigration.UtilizationReport(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_utilization_reports(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, vmmigration.UtilizationReport) for i in results)


def test_list_utilization_reports_pages(transport_name: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_utilization_reports), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            vmmigration.ListUtilizationReportsResponse(
                utilization_reports=[
                    vmmigration.UtilizationReport(),
                    vmmigration.UtilizationReport(),
                    vmmigration.UtilizationReport(),
                ],
                next_page_token="abc",
            ),
            vmmigration.ListUtilizationReportsResponse(
                utilization_reports=[],
                next_page_token="def",
            ),
            vmmigration.ListUtilizationReportsResponse(
                utilization_reports=[
                    vmmigration.UtilizationReport(),
                ],
                next_page_token="ghi",
            ),
            vmmigration.ListUtilizationReportsResponse(
                utilization_reports=[
                    vmmigration.UtilizationReport(),
                    vmmigration.UtilizationReport(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_utilization_reports(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_utilization_reports_async_pager():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_utilization_reports),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            vmmigration.ListUtilizationReportsResponse(
                utilization_reports=[
                    vmmigration.UtilizationReport(),
                    vmmigration.UtilizationReport(),
                    vmmigration.UtilizationReport(),
                ],
                next_page_token="abc",
            ),
            vmmigration.ListUtilizationReportsResponse(
                utilization_reports=[],
                next_page_token="def",
            ),
            vmmigration.ListUtilizationReportsResponse(
                utilization_reports=[
                    vmmigration.UtilizationReport(),
                ],
                next_page_token="ghi",
            ),
            vmmigration.ListUtilizationReportsResponse(
                utilization_reports=[
                    vmmigration.UtilizationReport(),
                    vmmigration.UtilizationReport(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_utilization_reports(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, vmmigration.UtilizationReport) for i in responses)


@pytest.mark.asyncio
async def test_list_utilization_reports_async_pages():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_utilization_reports),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            vmmigration.ListUtilizationReportsResponse(
                utilization_reports=[
                    vmmigration.UtilizationReport(),
                    vmmigration.UtilizationReport(),
                    vmmigration.UtilizationReport(),
                ],
                next_page_token="abc",
            ),
            vmmigration.ListUtilizationReportsResponse(
                utilization_reports=[],
                next_page_token="def",
            ),
            vmmigration.ListUtilizationReportsResponse(
                utilization_reports=[
                    vmmigration.UtilizationReport(),
                ],
                next_page_token="ghi",
            ),
            vmmigration.ListUtilizationReportsResponse(
                utilization_reports=[
                    vmmigration.UtilizationReport(),
                    vmmigration.UtilizationReport(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_utilization_reports(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.GetUtilizationReportRequest,
        dict,
    ],
)
def test_get_utilization_report(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_utilization_report), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.UtilizationReport(
            name="name_value",
            display_name="display_name_value",
            state=vmmigration.UtilizationReport.State.CREATING,
            time_frame=vmmigration.UtilizationReport.TimeFrame.WEEK,
            vm_count=875,
        )
        response = client.get_utilization_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.GetUtilizationReportRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, vmmigration.UtilizationReport)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.state == vmmigration.UtilizationReport.State.CREATING
    assert response.time_frame == vmmigration.UtilizationReport.TimeFrame.WEEK
    assert response.vm_count == 875


def test_get_utilization_report_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_utilization_report), "__call__"
    ) as call:
        client.get_utilization_report()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.GetUtilizationReportRequest()


@pytest.mark.asyncio
async def test_get_utilization_report_async(
    transport: str = "grpc_asyncio",
    request_type=vmmigration.GetUtilizationReportRequest,
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_utilization_report), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.UtilizationReport(
                name="name_value",
                display_name="display_name_value",
                state=vmmigration.UtilizationReport.State.CREATING,
                time_frame=vmmigration.UtilizationReport.TimeFrame.WEEK,
                vm_count=875,
            )
        )
        response = await client.get_utilization_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.GetUtilizationReportRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, vmmigration.UtilizationReport)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.state == vmmigration.UtilizationReport.State.CREATING
    assert response.time_frame == vmmigration.UtilizationReport.TimeFrame.WEEK
    assert response.vm_count == 875


@pytest.mark.asyncio
async def test_get_utilization_report_async_from_dict():
    await test_get_utilization_report_async(request_type=dict)


def test_get_utilization_report_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.GetUtilizationReportRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_utilization_report), "__call__"
    ) as call:
        call.return_value = vmmigration.UtilizationReport()
        client.get_utilization_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_utilization_report_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.GetUtilizationReportRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_utilization_report), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.UtilizationReport()
        )
        await client.get_utilization_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


def test_get_utilization_report_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_utilization_report), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.UtilizationReport()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_utilization_report(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_utilization_report_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_utilization_report(
            vmmigration.GetUtilizationReportRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_utilization_report_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_utilization_report), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.UtilizationReport()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.UtilizationReport()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_utilization_report(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_utilization_report_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_utilization_report(
            vmmigration.GetUtilizationReportRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.CreateUtilizationReportRequest,
        dict,
    ],
)
def test_create_utilization_report(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_utilization_report), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_utilization_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.CreateUtilizationReportRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_utilization_report_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_utilization_report), "__call__"
    ) as call:
        client.create_utilization_report()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.CreateUtilizationReportRequest()


@pytest.mark.asyncio
async def test_create_utilization_report_async(
    transport: str = "grpc_asyncio",
    request_type=vmmigration.CreateUtilizationReportRequest,
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_utilization_report), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_utilization_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.CreateUtilizationReportRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_utilization_report_async_from_dict():
    await test_create_utilization_report_async(request_type=dict)


def test_create_utilization_report_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.CreateUtilizationReportRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_utilization_report), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_utilization_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_utilization_report_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.CreateUtilizationReportRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_utilization_report), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_utilization_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


def test_create_utilization_report_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_utilization_report), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_utilization_report(
            parent="parent_value",
            utilization_report=vmmigration.UtilizationReport(name="name_value"),
            utilization_report_id="utilization_report_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].utilization_report
        mock_val = vmmigration.UtilizationReport(name="name_value")
        assert arg == mock_val
        arg = args[0].utilization_report_id
        mock_val = "utilization_report_id_value"
        assert arg == mock_val


def test_create_utilization_report_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_utilization_report(
            vmmigration.CreateUtilizationReportRequest(),
            parent="parent_value",
            utilization_report=vmmigration.UtilizationReport(name="name_value"),
            utilization_report_id="utilization_report_id_value",
        )


@pytest.mark.asyncio
async def test_create_utilization_report_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_utilization_report), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_utilization_report(
            parent="parent_value",
            utilization_report=vmmigration.UtilizationReport(name="name_value"),
            utilization_report_id="utilization_report_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].utilization_report
        mock_val = vmmigration.UtilizationReport(name="name_value")
        assert arg == mock_val
        arg = args[0].utilization_report_id
        mock_val = "utilization_report_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_utilization_report_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_utilization_report(
            vmmigration.CreateUtilizationReportRequest(),
            parent="parent_value",
            utilization_report=vmmigration.UtilizationReport(name="name_value"),
            utilization_report_id="utilization_report_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.DeleteUtilizationReportRequest,
        dict,
    ],
)
def test_delete_utilization_report(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_utilization_report), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_utilization_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.DeleteUtilizationReportRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_utilization_report_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_utilization_report), "__call__"
    ) as call:
        client.delete_utilization_report()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.DeleteUtilizationReportRequest()


@pytest.mark.asyncio
async def test_delete_utilization_report_async(
    transport: str = "grpc_asyncio",
    request_type=vmmigration.DeleteUtilizationReportRequest,
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_utilization_report), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_utilization_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.DeleteUtilizationReportRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_utilization_report_async_from_dict():
    await test_delete_utilization_report_async(request_type=dict)


def test_delete_utilization_report_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.DeleteUtilizationReportRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_utilization_report), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_utilization_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_utilization_report_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.DeleteUtilizationReportRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_utilization_report), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_utilization_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


def test_delete_utilization_report_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_utilization_report), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_utilization_report(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_utilization_report_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_utilization_report(
            vmmigration.DeleteUtilizationReportRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_utilization_report_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_utilization_report), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_utilization_report(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_utilization_report_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_utilization_report(
            vmmigration.DeleteUtilizationReportRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.ListDatacenterConnectorsRequest,
        dict,
    ],
)
def test_list_datacenter_connectors(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_datacenter_connectors), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.ListDatacenterConnectorsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_datacenter_connectors(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.ListDatacenterConnectorsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDatacenterConnectorsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_datacenter_connectors_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_datacenter_connectors), "__call__"
    ) as call:
        client.list_datacenter_connectors()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.ListDatacenterConnectorsRequest()


@pytest.mark.asyncio
async def test_list_datacenter_connectors_async(
    transport: str = "grpc_asyncio",
    request_type=vmmigration.ListDatacenterConnectorsRequest,
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_datacenter_connectors), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.ListDatacenterConnectorsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_datacenter_connectors(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.ListDatacenterConnectorsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDatacenterConnectorsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_datacenter_connectors_async_from_dict():
    await test_list_datacenter_connectors_async(request_type=dict)


def test_list_datacenter_connectors_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.ListDatacenterConnectorsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_datacenter_connectors), "__call__"
    ) as call:
        call.return_value = vmmigration.ListDatacenterConnectorsResponse()
        client.list_datacenter_connectors(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_datacenter_connectors_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.ListDatacenterConnectorsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_datacenter_connectors), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.ListDatacenterConnectorsResponse()
        )
        await client.list_datacenter_connectors(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


def test_list_datacenter_connectors_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_datacenter_connectors), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.ListDatacenterConnectorsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_datacenter_connectors(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_datacenter_connectors_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_datacenter_connectors(
            vmmigration.ListDatacenterConnectorsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_datacenter_connectors_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_datacenter_connectors), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.ListDatacenterConnectorsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.ListDatacenterConnectorsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_datacenter_connectors(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_datacenter_connectors_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_datacenter_connectors(
            vmmigration.ListDatacenterConnectorsRequest(),
            parent="parent_value",
        )


def test_list_datacenter_connectors_pager(transport_name: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_datacenter_connectors), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            vmmigration.ListDatacenterConnectorsResponse(
                datacenter_connectors=[
                    vmmigration.DatacenterConnector(),
                    vmmigration.DatacenterConnector(),
                    vmmigration.DatacenterConnector(),
                ],
                next_page_token="abc",
            ),
            vmmigration.ListDatacenterConnectorsResponse(
                datacenter_connectors=[],
                next_page_token="def",
            ),
            vmmigration.ListDatacenterConnectorsResponse(
                datacenter_connectors=[
                    vmmigration.DatacenterConnector(),
                ],
                next_page_token="ghi",
            ),
            vmmigration.ListDatacenterConnectorsResponse(
                datacenter_connectors=[
                    vmmigration.DatacenterConnector(),
                    vmmigration.DatacenterConnector(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_datacenter_connectors(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, vmmigration.DatacenterConnector) for i in results)


def test_list_datacenter_connectors_pages(transport_name: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_datacenter_connectors), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            vmmigration.ListDatacenterConnectorsResponse(
                datacenter_connectors=[
                    vmmigration.DatacenterConnector(),
                    vmmigration.DatacenterConnector(),
                    vmmigration.DatacenterConnector(),
                ],
                next_page_token="abc",
            ),
            vmmigration.ListDatacenterConnectorsResponse(
                datacenter_connectors=[],
                next_page_token="def",
            ),
            vmmigration.ListDatacenterConnectorsResponse(
                datacenter_connectors=[
                    vmmigration.DatacenterConnector(),
                ],
                next_page_token="ghi",
            ),
            vmmigration.ListDatacenterConnectorsResponse(
                datacenter_connectors=[
                    vmmigration.DatacenterConnector(),
                    vmmigration.DatacenterConnector(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_datacenter_connectors(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_datacenter_connectors_async_pager():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_datacenter_connectors),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            vmmigration.ListDatacenterConnectorsResponse(
                datacenter_connectors=[
                    vmmigration.DatacenterConnector(),
                    vmmigration.DatacenterConnector(),
                    vmmigration.DatacenterConnector(),
                ],
                next_page_token="abc",
            ),
            vmmigration.ListDatacenterConnectorsResponse(
                datacenter_connectors=[],
                next_page_token="def",
            ),
            vmmigration.ListDatacenterConnectorsResponse(
                datacenter_connectors=[
                    vmmigration.DatacenterConnector(),
                ],
                next_page_token="ghi",
            ),
            vmmigration.ListDatacenterConnectorsResponse(
                datacenter_connectors=[
                    vmmigration.DatacenterConnector(),
                    vmmigration.DatacenterConnector(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_datacenter_connectors(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, vmmigration.DatacenterConnector) for i in responses)


@pytest.mark.asyncio
async def test_list_datacenter_connectors_async_pages():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_datacenter_connectors),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            vmmigration.ListDatacenterConnectorsResponse(
                datacenter_connectors=[
                    vmmigration.DatacenterConnector(),
                    vmmigration.DatacenterConnector(),
                    vmmigration.DatacenterConnector(),
                ],
                next_page_token="abc",
            ),
            vmmigration.ListDatacenterConnectorsResponse(
                datacenter_connectors=[],
                next_page_token="def",
            ),
            vmmigration.ListDatacenterConnectorsResponse(
                datacenter_connectors=[
                    vmmigration.DatacenterConnector(),
                ],
                next_page_token="ghi",
            ),
            vmmigration.ListDatacenterConnectorsResponse(
                datacenter_connectors=[
                    vmmigration.DatacenterConnector(),
                    vmmigration.DatacenterConnector(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_datacenter_connectors(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.GetDatacenterConnectorRequest,
        dict,
    ],
)
def test_get_datacenter_connector(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_datacenter_connector), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.DatacenterConnector(
            name="name_value",
            registration_id="registration_id_value",
            service_account="service_account_value",
            version="version_value",
            bucket="bucket_value",
            state=vmmigration.DatacenterConnector.State.PENDING,
        )
        response = client.get_datacenter_connector(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.GetDatacenterConnectorRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, vmmigration.DatacenterConnector)
    assert response.name == "name_value"
    assert response.registration_id == "registration_id_value"
    assert response.service_account == "service_account_value"
    assert response.version == "version_value"
    assert response.bucket == "bucket_value"
    assert response.state == vmmigration.DatacenterConnector.State.PENDING


def test_get_datacenter_connector_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_datacenter_connector), "__call__"
    ) as call:
        client.get_datacenter_connector()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.GetDatacenterConnectorRequest()


@pytest.mark.asyncio
async def test_get_datacenter_connector_async(
    transport: str = "grpc_asyncio",
    request_type=vmmigration.GetDatacenterConnectorRequest,
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_datacenter_connector), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.DatacenterConnector(
                name="name_value",
                registration_id="registration_id_value",
                service_account="service_account_value",
                version="version_value",
                bucket="bucket_value",
                state=vmmigration.DatacenterConnector.State.PENDING,
            )
        )
        response = await client.get_datacenter_connector(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.GetDatacenterConnectorRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, vmmigration.DatacenterConnector)
    assert response.name == "name_value"
    assert response.registration_id == "registration_id_value"
    assert response.service_account == "service_account_value"
    assert response.version == "version_value"
    assert response.bucket == "bucket_value"
    assert response.state == vmmigration.DatacenterConnector.State.PENDING


@pytest.mark.asyncio
async def test_get_datacenter_connector_async_from_dict():
    await test_get_datacenter_connector_async(request_type=dict)


def test_get_datacenter_connector_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.GetDatacenterConnectorRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_datacenter_connector), "__call__"
    ) as call:
        call.return_value = vmmigration.DatacenterConnector()
        client.get_datacenter_connector(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_datacenter_connector_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.GetDatacenterConnectorRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_datacenter_connector), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.DatacenterConnector()
        )
        await client.get_datacenter_connector(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


def test_get_datacenter_connector_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_datacenter_connector), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.DatacenterConnector()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_datacenter_connector(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_datacenter_connector_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_datacenter_connector(
            vmmigration.GetDatacenterConnectorRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_datacenter_connector_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_datacenter_connector), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.DatacenterConnector()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.DatacenterConnector()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_datacenter_connector(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_datacenter_connector_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_datacenter_connector(
            vmmigration.GetDatacenterConnectorRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.CreateDatacenterConnectorRequest,
        dict,
    ],
)
def test_create_datacenter_connector(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_datacenter_connector), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_datacenter_connector(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.CreateDatacenterConnectorRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_datacenter_connector_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_datacenter_connector), "__call__"
    ) as call:
        client.create_datacenter_connector()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.CreateDatacenterConnectorRequest()


@pytest.mark.asyncio
async def test_create_datacenter_connector_async(
    transport: str = "grpc_asyncio",
    request_type=vmmigration.CreateDatacenterConnectorRequest,
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_datacenter_connector), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_datacenter_connector(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.CreateDatacenterConnectorRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_datacenter_connector_async_from_dict():
    await test_create_datacenter_connector_async(request_type=dict)


def test_create_datacenter_connector_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.CreateDatacenterConnectorRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_datacenter_connector), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_datacenter_connector(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_datacenter_connector_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.CreateDatacenterConnectorRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_datacenter_connector), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_datacenter_connector(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


def test_create_datacenter_connector_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_datacenter_connector), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_datacenter_connector(
            parent="parent_value",
            datacenter_connector=vmmigration.DatacenterConnector(
                create_time=timestamp_pb2.Timestamp(seconds=751)
            ),
            datacenter_connector_id="datacenter_connector_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].datacenter_connector
        mock_val = vmmigration.DatacenterConnector(
            create_time=timestamp_pb2.Timestamp(seconds=751)
        )
        assert arg == mock_val
        arg = args[0].datacenter_connector_id
        mock_val = "datacenter_connector_id_value"
        assert arg == mock_val


def test_create_datacenter_connector_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_datacenter_connector(
            vmmigration.CreateDatacenterConnectorRequest(),
            parent="parent_value",
            datacenter_connector=vmmigration.DatacenterConnector(
                create_time=timestamp_pb2.Timestamp(seconds=751)
            ),
            datacenter_connector_id="datacenter_connector_id_value",
        )


@pytest.mark.asyncio
async def test_create_datacenter_connector_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_datacenter_connector), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_datacenter_connector(
            parent="parent_value",
            datacenter_connector=vmmigration.DatacenterConnector(
                create_time=timestamp_pb2.Timestamp(seconds=751)
            ),
            datacenter_connector_id="datacenter_connector_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].datacenter_connector
        mock_val = vmmigration.DatacenterConnector(
            create_time=timestamp_pb2.Timestamp(seconds=751)
        )
        assert arg == mock_val
        arg = args[0].datacenter_connector_id
        mock_val = "datacenter_connector_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_datacenter_connector_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_datacenter_connector(
            vmmigration.CreateDatacenterConnectorRequest(),
            parent="parent_value",
            datacenter_connector=vmmigration.DatacenterConnector(
                create_time=timestamp_pb2.Timestamp(seconds=751)
            ),
            datacenter_connector_id="datacenter_connector_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.DeleteDatacenterConnectorRequest,
        dict,
    ],
)
def test_delete_datacenter_connector(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_datacenter_connector), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_datacenter_connector(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.DeleteDatacenterConnectorRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_datacenter_connector_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_datacenter_connector), "__call__"
    ) as call:
        client.delete_datacenter_connector()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.DeleteDatacenterConnectorRequest()


@pytest.mark.asyncio
async def test_delete_datacenter_connector_async(
    transport: str = "grpc_asyncio",
    request_type=vmmigration.DeleteDatacenterConnectorRequest,
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_datacenter_connector), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_datacenter_connector(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.DeleteDatacenterConnectorRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_datacenter_connector_async_from_dict():
    await test_delete_datacenter_connector_async(request_type=dict)


def test_delete_datacenter_connector_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.DeleteDatacenterConnectorRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_datacenter_connector), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_datacenter_connector(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_datacenter_connector_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.DeleteDatacenterConnectorRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_datacenter_connector), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_datacenter_connector(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


def test_delete_datacenter_connector_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_datacenter_connector), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_datacenter_connector(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_datacenter_connector_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_datacenter_connector(
            vmmigration.DeleteDatacenterConnectorRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_datacenter_connector_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_datacenter_connector), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_datacenter_connector(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_datacenter_connector_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_datacenter_connector(
            vmmigration.DeleteDatacenterConnectorRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.CreateMigratingVmRequest,
        dict,
    ],
)
def test_create_migrating_vm(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_migrating_vm), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_migrating_vm(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.CreateMigratingVmRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_migrating_vm_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_migrating_vm), "__call__"
    ) as call:
        client.create_migrating_vm()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.CreateMigratingVmRequest()


@pytest.mark.asyncio
async def test_create_migrating_vm_async(
    transport: str = "grpc_asyncio", request_type=vmmigration.CreateMigratingVmRequest
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_migrating_vm), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_migrating_vm(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.CreateMigratingVmRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_migrating_vm_async_from_dict():
    await test_create_migrating_vm_async(request_type=dict)


def test_create_migrating_vm_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.CreateMigratingVmRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_migrating_vm), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_migrating_vm(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_migrating_vm_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.CreateMigratingVmRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_migrating_vm), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_migrating_vm(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


def test_create_migrating_vm_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_migrating_vm), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_migrating_vm(
            parent="parent_value",
            migrating_vm=vmmigration.MigratingVm(
                compute_engine_target_defaults=vmmigration.ComputeEngineTargetDefaults(
                    vm_name="vm_name_value"
                )
            ),
            migrating_vm_id="migrating_vm_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].migrating_vm
        mock_val = vmmigration.MigratingVm(
            compute_engine_target_defaults=vmmigration.ComputeEngineTargetDefaults(
                vm_name="vm_name_value"
            )
        )
        assert arg == mock_val
        arg = args[0].migrating_vm_id
        mock_val = "migrating_vm_id_value"
        assert arg == mock_val


def test_create_migrating_vm_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_migrating_vm(
            vmmigration.CreateMigratingVmRequest(),
            parent="parent_value",
            migrating_vm=vmmigration.MigratingVm(
                compute_engine_target_defaults=vmmigration.ComputeEngineTargetDefaults(
                    vm_name="vm_name_value"
                )
            ),
            migrating_vm_id="migrating_vm_id_value",
        )


@pytest.mark.asyncio
async def test_create_migrating_vm_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_migrating_vm), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_migrating_vm(
            parent="parent_value",
            migrating_vm=vmmigration.MigratingVm(
                compute_engine_target_defaults=vmmigration.ComputeEngineTargetDefaults(
                    vm_name="vm_name_value"
                )
            ),
            migrating_vm_id="migrating_vm_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].migrating_vm
        mock_val = vmmigration.MigratingVm(
            compute_engine_target_defaults=vmmigration.ComputeEngineTargetDefaults(
                vm_name="vm_name_value"
            )
        )
        assert arg == mock_val
        arg = args[0].migrating_vm_id
        mock_val = "migrating_vm_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_migrating_vm_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_migrating_vm(
            vmmigration.CreateMigratingVmRequest(),
            parent="parent_value",
            migrating_vm=vmmigration.MigratingVm(
                compute_engine_target_defaults=vmmigration.ComputeEngineTargetDefaults(
                    vm_name="vm_name_value"
                )
            ),
            migrating_vm_id="migrating_vm_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.ListMigratingVmsRequest,
        dict,
    ],
)
def test_list_migrating_vms(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migrating_vms), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.ListMigratingVmsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_migrating_vms(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.ListMigratingVmsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMigratingVmsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_migrating_vms_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migrating_vms), "__call__"
    ) as call:
        client.list_migrating_vms()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.ListMigratingVmsRequest()


@pytest.mark.asyncio
async def test_list_migrating_vms_async(
    transport: str = "grpc_asyncio", request_type=vmmigration.ListMigratingVmsRequest
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migrating_vms), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.ListMigratingVmsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_migrating_vms(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.ListMigratingVmsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMigratingVmsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_migrating_vms_async_from_dict():
    await test_list_migrating_vms_async(request_type=dict)


def test_list_migrating_vms_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.ListMigratingVmsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migrating_vms), "__call__"
    ) as call:
        call.return_value = vmmigration.ListMigratingVmsResponse()
        client.list_migrating_vms(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_migrating_vms_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.ListMigratingVmsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migrating_vms), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.ListMigratingVmsResponse()
        )
        await client.list_migrating_vms(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


def test_list_migrating_vms_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migrating_vms), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.ListMigratingVmsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_migrating_vms(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_migrating_vms_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_migrating_vms(
            vmmigration.ListMigratingVmsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_migrating_vms_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migrating_vms), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.ListMigratingVmsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.ListMigratingVmsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_migrating_vms(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_migrating_vms_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_migrating_vms(
            vmmigration.ListMigratingVmsRequest(),
            parent="parent_value",
        )


def test_list_migrating_vms_pager(transport_name: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migrating_vms), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            vmmigration.ListMigratingVmsResponse(
                migrating_vms=[
                    vmmigration.MigratingVm(),
                    vmmigration.MigratingVm(),
                    vmmigration.MigratingVm(),
                ],
                next_page_token="abc",
            ),
            vmmigration.ListMigratingVmsResponse(
                migrating_vms=[],
                next_page_token="def",
            ),
            vmmigration.ListMigratingVmsResponse(
                migrating_vms=[
                    vmmigration.MigratingVm(),
                ],
                next_page_token="ghi",
            ),
            vmmigration.ListMigratingVmsResponse(
                migrating_vms=[
                    vmmigration.MigratingVm(),
                    vmmigration.MigratingVm(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_migrating_vms(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, vmmigration.MigratingVm) for i in results)


def test_list_migrating_vms_pages(transport_name: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migrating_vms), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            vmmigration.ListMigratingVmsResponse(
                migrating_vms=[
                    vmmigration.MigratingVm(),
                    vmmigration.MigratingVm(),
                    vmmigration.MigratingVm(),
                ],
                next_page_token="abc",
            ),
            vmmigration.ListMigratingVmsResponse(
                migrating_vms=[],
                next_page_token="def",
            ),
            vmmigration.ListMigratingVmsResponse(
                migrating_vms=[
                    vmmigration.MigratingVm(),
                ],
                next_page_token="ghi",
            ),
            vmmigration.ListMigratingVmsResponse(
                migrating_vms=[
                    vmmigration.MigratingVm(),
                    vmmigration.MigratingVm(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_migrating_vms(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_migrating_vms_async_pager():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migrating_vms),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            vmmigration.ListMigratingVmsResponse(
                migrating_vms=[
                    vmmigration.MigratingVm(),
                    vmmigration.MigratingVm(),
                    vmmigration.MigratingVm(),
                ],
                next_page_token="abc",
            ),
            vmmigration.ListMigratingVmsResponse(
                migrating_vms=[],
                next_page_token="def",
            ),
            vmmigration.ListMigratingVmsResponse(
                migrating_vms=[
                    vmmigration.MigratingVm(),
                ],
                next_page_token="ghi",
            ),
            vmmigration.ListMigratingVmsResponse(
                migrating_vms=[
                    vmmigration.MigratingVm(),
                    vmmigration.MigratingVm(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_migrating_vms(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, vmmigration.MigratingVm) for i in responses)


@pytest.mark.asyncio
async def test_list_migrating_vms_async_pages():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migrating_vms),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            vmmigration.ListMigratingVmsResponse(
                migrating_vms=[
                    vmmigration.MigratingVm(),
                    vmmigration.MigratingVm(),
                    vmmigration.MigratingVm(),
                ],
                next_page_token="abc",
            ),
            vmmigration.ListMigratingVmsResponse(
                migrating_vms=[],
                next_page_token="def",
            ),
            vmmigration.ListMigratingVmsResponse(
                migrating_vms=[
                    vmmigration.MigratingVm(),
                ],
                next_page_token="ghi",
            ),
            vmmigration.ListMigratingVmsResponse(
                migrating_vms=[
                    vmmigration.MigratingVm(),
                    vmmigration.MigratingVm(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_migrating_vms(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.GetMigratingVmRequest,
        dict,
    ],
)
def test_get_migrating_vm(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_migrating_vm), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.MigratingVm(
            name="name_value",
            source_vm_id="source_vm_id_value",
            display_name="display_name_value",
            description="description_value",
            state=vmmigration.MigratingVm.State.PENDING,
            group="group_value",
            compute_engine_target_defaults=vmmigration.ComputeEngineTargetDefaults(
                vm_name="vm_name_value"
            ),
        )
        response = client.get_migrating_vm(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.GetMigratingVmRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, vmmigration.MigratingVm)
    assert response.name == "name_value"
    assert response.source_vm_id == "source_vm_id_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.state == vmmigration.MigratingVm.State.PENDING
    assert response.group == "group_value"


def test_get_migrating_vm_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_migrating_vm), "__call__") as call:
        client.get_migrating_vm()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.GetMigratingVmRequest()


@pytest.mark.asyncio
async def test_get_migrating_vm_async(
    transport: str = "grpc_asyncio", request_type=vmmigration.GetMigratingVmRequest
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_migrating_vm), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.MigratingVm(
                name="name_value",
                source_vm_id="source_vm_id_value",
                display_name="display_name_value",
                description="description_value",
                state=vmmigration.MigratingVm.State.PENDING,
                group="group_value",
            )
        )
        response = await client.get_migrating_vm(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.GetMigratingVmRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, vmmigration.MigratingVm)
    assert response.name == "name_value"
    assert response.source_vm_id == "source_vm_id_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.state == vmmigration.MigratingVm.State.PENDING
    assert response.group == "group_value"


@pytest.mark.asyncio
async def test_get_migrating_vm_async_from_dict():
    await test_get_migrating_vm_async(request_type=dict)


def test_get_migrating_vm_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.GetMigratingVmRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_migrating_vm), "__call__") as call:
        call.return_value = vmmigration.MigratingVm()
        client.get_migrating_vm(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_migrating_vm_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.GetMigratingVmRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_migrating_vm), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.MigratingVm()
        )
        await client.get_migrating_vm(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


def test_get_migrating_vm_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_migrating_vm), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.MigratingVm()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_migrating_vm(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_migrating_vm_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_migrating_vm(
            vmmigration.GetMigratingVmRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_migrating_vm_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_migrating_vm), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.MigratingVm()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.MigratingVm()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_migrating_vm(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_migrating_vm_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_migrating_vm(
            vmmigration.GetMigratingVmRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.UpdateMigratingVmRequest,
        dict,
    ],
)
def test_update_migrating_vm(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_migrating_vm), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_migrating_vm(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.UpdateMigratingVmRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_migrating_vm_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_migrating_vm), "__call__"
    ) as call:
        client.update_migrating_vm()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.UpdateMigratingVmRequest()


@pytest.mark.asyncio
async def test_update_migrating_vm_async(
    transport: str = "grpc_asyncio", request_type=vmmigration.UpdateMigratingVmRequest
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_migrating_vm), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_migrating_vm(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.UpdateMigratingVmRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_migrating_vm_async_from_dict():
    await test_update_migrating_vm_async(request_type=dict)


def test_update_migrating_vm_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.UpdateMigratingVmRequest()

    request.migrating_vm.name = "migrating_vm.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_migrating_vm), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_migrating_vm(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "migrating_vm.name=migrating_vm.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_migrating_vm_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.UpdateMigratingVmRequest()

    request.migrating_vm.name = "migrating_vm.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_migrating_vm), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_migrating_vm(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "migrating_vm.name=migrating_vm.name/value",
    ) in kw["metadata"]


def test_update_migrating_vm_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_migrating_vm), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_migrating_vm(
            migrating_vm=vmmigration.MigratingVm(
                compute_engine_target_defaults=vmmigration.ComputeEngineTargetDefaults(
                    vm_name="vm_name_value"
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].migrating_vm
        mock_val = vmmigration.MigratingVm(
            compute_engine_target_defaults=vmmigration.ComputeEngineTargetDefaults(
                vm_name="vm_name_value"
            )
        )
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_migrating_vm_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_migrating_vm(
            vmmigration.UpdateMigratingVmRequest(),
            migrating_vm=vmmigration.MigratingVm(
                compute_engine_target_defaults=vmmigration.ComputeEngineTargetDefaults(
                    vm_name="vm_name_value"
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_migrating_vm_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_migrating_vm), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_migrating_vm(
            migrating_vm=vmmigration.MigratingVm(
                compute_engine_target_defaults=vmmigration.ComputeEngineTargetDefaults(
                    vm_name="vm_name_value"
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].migrating_vm
        mock_val = vmmigration.MigratingVm(
            compute_engine_target_defaults=vmmigration.ComputeEngineTargetDefaults(
                vm_name="vm_name_value"
            )
        )
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_migrating_vm_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_migrating_vm(
            vmmigration.UpdateMigratingVmRequest(),
            migrating_vm=vmmigration.MigratingVm(
                compute_engine_target_defaults=vmmigration.ComputeEngineTargetDefaults(
                    vm_name="vm_name_value"
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.DeleteMigratingVmRequest,
        dict,
    ],
)
def test_delete_migrating_vm(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_migrating_vm), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_migrating_vm(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.DeleteMigratingVmRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_migrating_vm_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_migrating_vm), "__call__"
    ) as call:
        client.delete_migrating_vm()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.DeleteMigratingVmRequest()


@pytest.mark.asyncio
async def test_delete_migrating_vm_async(
    transport: str = "grpc_asyncio", request_type=vmmigration.DeleteMigratingVmRequest
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_migrating_vm), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_migrating_vm(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.DeleteMigratingVmRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_migrating_vm_async_from_dict():
    await test_delete_migrating_vm_async(request_type=dict)


def test_delete_migrating_vm_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.DeleteMigratingVmRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_migrating_vm), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_migrating_vm(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_migrating_vm_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.DeleteMigratingVmRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_migrating_vm), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_migrating_vm(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


def test_delete_migrating_vm_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_migrating_vm), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_migrating_vm(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_migrating_vm_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_migrating_vm(
            vmmigration.DeleteMigratingVmRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_migrating_vm_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_migrating_vm), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_migrating_vm(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_migrating_vm_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_migrating_vm(
            vmmigration.DeleteMigratingVmRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.StartMigrationRequest,
        dict,
    ],
)
def test_start_migration(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.start_migration), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.start_migration(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.StartMigrationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_start_migration_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.start_migration), "__call__") as call:
        client.start_migration()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.StartMigrationRequest()


@pytest.mark.asyncio
async def test_start_migration_async(
    transport: str = "grpc_asyncio", request_type=vmmigration.StartMigrationRequest
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.start_migration), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.start_migration(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.StartMigrationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_start_migration_async_from_dict():
    await test_start_migration_async(request_type=dict)


def test_start_migration_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.StartMigrationRequest()

    request.migrating_vm = "migrating_vm/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.start_migration), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.start_migration(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "migrating_vm=migrating_vm/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_start_migration_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.StartMigrationRequest()

    request.migrating_vm = "migrating_vm/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.start_migration), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.start_migration(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "migrating_vm=migrating_vm/value",
    ) in kw["metadata"]


def test_start_migration_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.start_migration), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.start_migration(
            migrating_vm="migrating_vm_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].migrating_vm
        mock_val = "migrating_vm_value"
        assert arg == mock_val


def test_start_migration_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.start_migration(
            vmmigration.StartMigrationRequest(),
            migrating_vm="migrating_vm_value",
        )


@pytest.mark.asyncio
async def test_start_migration_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.start_migration), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.start_migration(
            migrating_vm="migrating_vm_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].migrating_vm
        mock_val = "migrating_vm_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_start_migration_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.start_migration(
            vmmigration.StartMigrationRequest(),
            migrating_vm="migrating_vm_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.ResumeMigrationRequest,
        dict,
    ],
)
def test_resume_migration(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.resume_migration), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.resume_migration(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.ResumeMigrationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_resume_migration_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.resume_migration), "__call__") as call:
        client.resume_migration()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.ResumeMigrationRequest()


@pytest.mark.asyncio
async def test_resume_migration_async(
    transport: str = "grpc_asyncio", request_type=vmmigration.ResumeMigrationRequest
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.resume_migration), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.resume_migration(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.ResumeMigrationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_resume_migration_async_from_dict():
    await test_resume_migration_async(request_type=dict)


def test_resume_migration_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.ResumeMigrationRequest()

    request.migrating_vm = "migrating_vm/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.resume_migration), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.resume_migration(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "migrating_vm=migrating_vm/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_resume_migration_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.ResumeMigrationRequest()

    request.migrating_vm = "migrating_vm/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.resume_migration), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.resume_migration(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "migrating_vm=migrating_vm/value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.PauseMigrationRequest,
        dict,
    ],
)
def test_pause_migration(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.pause_migration), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.pause_migration(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.PauseMigrationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_pause_migration_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.pause_migration), "__call__") as call:
        client.pause_migration()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.PauseMigrationRequest()


@pytest.mark.asyncio
async def test_pause_migration_async(
    transport: str = "grpc_asyncio", request_type=vmmigration.PauseMigrationRequest
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.pause_migration), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.pause_migration(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.PauseMigrationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_pause_migration_async_from_dict():
    await test_pause_migration_async(request_type=dict)


def test_pause_migration_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.PauseMigrationRequest()

    request.migrating_vm = "migrating_vm/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.pause_migration), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.pause_migration(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "migrating_vm=migrating_vm/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_pause_migration_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.PauseMigrationRequest()

    request.migrating_vm = "migrating_vm/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.pause_migration), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.pause_migration(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "migrating_vm=migrating_vm/value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.FinalizeMigrationRequest,
        dict,
    ],
)
def test_finalize_migration(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.finalize_migration), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.finalize_migration(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.FinalizeMigrationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_finalize_migration_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.finalize_migration), "__call__"
    ) as call:
        client.finalize_migration()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.FinalizeMigrationRequest()


@pytest.mark.asyncio
async def test_finalize_migration_async(
    transport: str = "grpc_asyncio", request_type=vmmigration.FinalizeMigrationRequest
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.finalize_migration), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.finalize_migration(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.FinalizeMigrationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_finalize_migration_async_from_dict():
    await test_finalize_migration_async(request_type=dict)


def test_finalize_migration_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.FinalizeMigrationRequest()

    request.migrating_vm = "migrating_vm/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.finalize_migration), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.finalize_migration(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "migrating_vm=migrating_vm/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_finalize_migration_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.FinalizeMigrationRequest()

    request.migrating_vm = "migrating_vm/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.finalize_migration), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.finalize_migration(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "migrating_vm=migrating_vm/value",
    ) in kw["metadata"]


def test_finalize_migration_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.finalize_migration), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.finalize_migration(
            migrating_vm="migrating_vm_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].migrating_vm
        mock_val = "migrating_vm_value"
        assert arg == mock_val


def test_finalize_migration_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.finalize_migration(
            vmmigration.FinalizeMigrationRequest(),
            migrating_vm="migrating_vm_value",
        )


@pytest.mark.asyncio
async def test_finalize_migration_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.finalize_migration), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.finalize_migration(
            migrating_vm="migrating_vm_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].migrating_vm
        mock_val = "migrating_vm_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_finalize_migration_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.finalize_migration(
            vmmigration.FinalizeMigrationRequest(),
            migrating_vm="migrating_vm_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.CreateCloneJobRequest,
        dict,
    ],
)
def test_create_clone_job(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_clone_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_clone_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.CreateCloneJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_clone_job_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_clone_job), "__call__") as call:
        client.create_clone_job()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.CreateCloneJobRequest()


@pytest.mark.asyncio
async def test_create_clone_job_async(
    transport: str = "grpc_asyncio", request_type=vmmigration.CreateCloneJobRequest
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_clone_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_clone_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.CreateCloneJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_clone_job_async_from_dict():
    await test_create_clone_job_async(request_type=dict)


def test_create_clone_job_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.CreateCloneJobRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_clone_job), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_clone_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_clone_job_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.CreateCloneJobRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_clone_job), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_clone_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


def test_create_clone_job_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_clone_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_clone_job(
            parent="parent_value",
            clone_job=vmmigration.CloneJob(
                compute_engine_target_details=vmmigration.ComputeEngineTargetDetails(
                    vm_name="vm_name_value"
                )
            ),
            clone_job_id="clone_job_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].clone_job
        mock_val = vmmigration.CloneJob(
            compute_engine_target_details=vmmigration.ComputeEngineTargetDetails(
                vm_name="vm_name_value"
            )
        )
        assert arg == mock_val
        arg = args[0].clone_job_id
        mock_val = "clone_job_id_value"
        assert arg == mock_val


def test_create_clone_job_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_clone_job(
            vmmigration.CreateCloneJobRequest(),
            parent="parent_value",
            clone_job=vmmigration.CloneJob(
                compute_engine_target_details=vmmigration.ComputeEngineTargetDetails(
                    vm_name="vm_name_value"
                )
            ),
            clone_job_id="clone_job_id_value",
        )


@pytest.mark.asyncio
async def test_create_clone_job_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_clone_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_clone_job(
            parent="parent_value",
            clone_job=vmmigration.CloneJob(
                compute_engine_target_details=vmmigration.ComputeEngineTargetDetails(
                    vm_name="vm_name_value"
                )
            ),
            clone_job_id="clone_job_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].clone_job
        mock_val = vmmigration.CloneJob(
            compute_engine_target_details=vmmigration.ComputeEngineTargetDetails(
                vm_name="vm_name_value"
            )
        )
        assert arg == mock_val
        arg = args[0].clone_job_id
        mock_val = "clone_job_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_clone_job_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_clone_job(
            vmmigration.CreateCloneJobRequest(),
            parent="parent_value",
            clone_job=vmmigration.CloneJob(
                compute_engine_target_details=vmmigration.ComputeEngineTargetDetails(
                    vm_name="vm_name_value"
                )
            ),
            clone_job_id="clone_job_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.CancelCloneJobRequest,
        dict,
    ],
)
def test_cancel_clone_job(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_clone_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.cancel_clone_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.CancelCloneJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_cancel_clone_job_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_clone_job), "__call__") as call:
        client.cancel_clone_job()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.CancelCloneJobRequest()


@pytest.mark.asyncio
async def test_cancel_clone_job_async(
    transport: str = "grpc_asyncio", request_type=vmmigration.CancelCloneJobRequest
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_clone_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.cancel_clone_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.CancelCloneJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_cancel_clone_job_async_from_dict():
    await test_cancel_clone_job_async(request_type=dict)


def test_cancel_clone_job_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.CancelCloneJobRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_clone_job), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.cancel_clone_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_cancel_clone_job_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.CancelCloneJobRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_clone_job), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.cancel_clone_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


def test_cancel_clone_job_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_clone_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.cancel_clone_job(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_cancel_clone_job_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.cancel_clone_job(
            vmmigration.CancelCloneJobRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_cancel_clone_job_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_clone_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.cancel_clone_job(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_cancel_clone_job_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.cancel_clone_job(
            vmmigration.CancelCloneJobRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.ListCloneJobsRequest,
        dict,
    ],
)
def test_list_clone_jobs(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_clone_jobs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.ListCloneJobsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_clone_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.ListCloneJobsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCloneJobsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_clone_jobs_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_clone_jobs), "__call__") as call:
        client.list_clone_jobs()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.ListCloneJobsRequest()


@pytest.mark.asyncio
async def test_list_clone_jobs_async(
    transport: str = "grpc_asyncio", request_type=vmmigration.ListCloneJobsRequest
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_clone_jobs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.ListCloneJobsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_clone_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.ListCloneJobsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCloneJobsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_clone_jobs_async_from_dict():
    await test_list_clone_jobs_async(request_type=dict)


def test_list_clone_jobs_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.ListCloneJobsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_clone_jobs), "__call__") as call:
        call.return_value = vmmigration.ListCloneJobsResponse()
        client.list_clone_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_clone_jobs_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.ListCloneJobsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_clone_jobs), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.ListCloneJobsResponse()
        )
        await client.list_clone_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


def test_list_clone_jobs_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_clone_jobs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.ListCloneJobsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_clone_jobs(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_clone_jobs_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_clone_jobs(
            vmmigration.ListCloneJobsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_clone_jobs_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_clone_jobs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.ListCloneJobsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.ListCloneJobsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_clone_jobs(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_clone_jobs_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_clone_jobs(
            vmmigration.ListCloneJobsRequest(),
            parent="parent_value",
        )


def test_list_clone_jobs_pager(transport_name: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_clone_jobs), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            vmmigration.ListCloneJobsResponse(
                clone_jobs=[
                    vmmigration.CloneJob(),
                    vmmigration.CloneJob(),
                    vmmigration.CloneJob(),
                ],
                next_page_token="abc",
            ),
            vmmigration.ListCloneJobsResponse(
                clone_jobs=[],
                next_page_token="def",
            ),
            vmmigration.ListCloneJobsResponse(
                clone_jobs=[
                    vmmigration.CloneJob(),
                ],
                next_page_token="ghi",
            ),
            vmmigration.ListCloneJobsResponse(
                clone_jobs=[
                    vmmigration.CloneJob(),
                    vmmigration.CloneJob(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_clone_jobs(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, vmmigration.CloneJob) for i in results)


def test_list_clone_jobs_pages(transport_name: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_clone_jobs), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            vmmigration.ListCloneJobsResponse(
                clone_jobs=[
                    vmmigration.CloneJob(),
                    vmmigration.CloneJob(),
                    vmmigration.CloneJob(),
                ],
                next_page_token="abc",
            ),
            vmmigration.ListCloneJobsResponse(
                clone_jobs=[],
                next_page_token="def",
            ),
            vmmigration.ListCloneJobsResponse(
                clone_jobs=[
                    vmmigration.CloneJob(),
                ],
                next_page_token="ghi",
            ),
            vmmigration.ListCloneJobsResponse(
                clone_jobs=[
                    vmmigration.CloneJob(),
                    vmmigration.CloneJob(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_clone_jobs(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_clone_jobs_async_pager():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_clone_jobs), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            vmmigration.ListCloneJobsResponse(
                clone_jobs=[
                    vmmigration.CloneJob(),
                    vmmigration.CloneJob(),
                    vmmigration.CloneJob(),
                ],
                next_page_token="abc",
            ),
            vmmigration.ListCloneJobsResponse(
                clone_jobs=[],
                next_page_token="def",
            ),
            vmmigration.ListCloneJobsResponse(
                clone_jobs=[
                    vmmigration.CloneJob(),
                ],
                next_page_token="ghi",
            ),
            vmmigration.ListCloneJobsResponse(
                clone_jobs=[
                    vmmigration.CloneJob(),
                    vmmigration.CloneJob(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_clone_jobs(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, vmmigration.CloneJob) for i in responses)


@pytest.mark.asyncio
async def test_list_clone_jobs_async_pages():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_clone_jobs), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            vmmigration.ListCloneJobsResponse(
                clone_jobs=[
                    vmmigration.CloneJob(),
                    vmmigration.CloneJob(),
                    vmmigration.CloneJob(),
                ],
                next_page_token="abc",
            ),
            vmmigration.ListCloneJobsResponse(
                clone_jobs=[],
                next_page_token="def",
            ),
            vmmigration.ListCloneJobsResponse(
                clone_jobs=[
                    vmmigration.CloneJob(),
                ],
                next_page_token="ghi",
            ),
            vmmigration.ListCloneJobsResponse(
                clone_jobs=[
                    vmmigration.CloneJob(),
                    vmmigration.CloneJob(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_clone_jobs(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.GetCloneJobRequest,
        dict,
    ],
)
def test_get_clone_job(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_clone_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.CloneJob(
            name="name_value",
            state=vmmigration.CloneJob.State.PENDING,
            compute_engine_target_details=vmmigration.ComputeEngineTargetDetails(
                vm_name="vm_name_value"
            ),
        )
        response = client.get_clone_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.GetCloneJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, vmmigration.CloneJob)
    assert response.name == "name_value"
    assert response.state == vmmigration.CloneJob.State.PENDING


def test_get_clone_job_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_clone_job), "__call__") as call:
        client.get_clone_job()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.GetCloneJobRequest()


@pytest.mark.asyncio
async def test_get_clone_job_async(
    transport: str = "grpc_asyncio", request_type=vmmigration.GetCloneJobRequest
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_clone_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.CloneJob(
                name="name_value",
                state=vmmigration.CloneJob.State.PENDING,
            )
        )
        response = await client.get_clone_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.GetCloneJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, vmmigration.CloneJob)
    assert response.name == "name_value"
    assert response.state == vmmigration.CloneJob.State.PENDING


@pytest.mark.asyncio
async def test_get_clone_job_async_from_dict():
    await test_get_clone_job_async(request_type=dict)


def test_get_clone_job_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.GetCloneJobRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_clone_job), "__call__") as call:
        call.return_value = vmmigration.CloneJob()
        client.get_clone_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_clone_job_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.GetCloneJobRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_clone_job), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.CloneJob()
        )
        await client.get_clone_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


def test_get_clone_job_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_clone_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.CloneJob()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_clone_job(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_clone_job_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_clone_job(
            vmmigration.GetCloneJobRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_clone_job_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_clone_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.CloneJob()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.CloneJob()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_clone_job(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_clone_job_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_clone_job(
            vmmigration.GetCloneJobRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.CreateCutoverJobRequest,
        dict,
    ],
)
def test_create_cutover_job(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_cutover_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_cutover_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.CreateCutoverJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_cutover_job_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_cutover_job), "__call__"
    ) as call:
        client.create_cutover_job()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.CreateCutoverJobRequest()


@pytest.mark.asyncio
async def test_create_cutover_job_async(
    transport: str = "grpc_asyncio", request_type=vmmigration.CreateCutoverJobRequest
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_cutover_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_cutover_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.CreateCutoverJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_cutover_job_async_from_dict():
    await test_create_cutover_job_async(request_type=dict)


def test_create_cutover_job_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.CreateCutoverJobRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_cutover_job), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_cutover_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_cutover_job_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.CreateCutoverJobRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_cutover_job), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_cutover_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


def test_create_cutover_job_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_cutover_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_cutover_job(
            parent="parent_value",
            cutover_job=vmmigration.CutoverJob(
                compute_engine_target_details=vmmigration.ComputeEngineTargetDetails(
                    vm_name="vm_name_value"
                )
            ),
            cutover_job_id="cutover_job_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].cutover_job
        mock_val = vmmigration.CutoverJob(
            compute_engine_target_details=vmmigration.ComputeEngineTargetDetails(
                vm_name="vm_name_value"
            )
        )
        assert arg == mock_val
        arg = args[0].cutover_job_id
        mock_val = "cutover_job_id_value"
        assert arg == mock_val


def test_create_cutover_job_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_cutover_job(
            vmmigration.CreateCutoverJobRequest(),
            parent="parent_value",
            cutover_job=vmmigration.CutoverJob(
                compute_engine_target_details=vmmigration.ComputeEngineTargetDetails(
                    vm_name="vm_name_value"
                )
            ),
            cutover_job_id="cutover_job_id_value",
        )


@pytest.mark.asyncio
async def test_create_cutover_job_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_cutover_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_cutover_job(
            parent="parent_value",
            cutover_job=vmmigration.CutoverJob(
                compute_engine_target_details=vmmigration.ComputeEngineTargetDetails(
                    vm_name="vm_name_value"
                )
            ),
            cutover_job_id="cutover_job_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].cutover_job
        mock_val = vmmigration.CutoverJob(
            compute_engine_target_details=vmmigration.ComputeEngineTargetDetails(
                vm_name="vm_name_value"
            )
        )
        assert arg == mock_val
        arg = args[0].cutover_job_id
        mock_val = "cutover_job_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_cutover_job_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_cutover_job(
            vmmigration.CreateCutoverJobRequest(),
            parent="parent_value",
            cutover_job=vmmigration.CutoverJob(
                compute_engine_target_details=vmmigration.ComputeEngineTargetDetails(
                    vm_name="vm_name_value"
                )
            ),
            cutover_job_id="cutover_job_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.CancelCutoverJobRequest,
        dict,
    ],
)
def test_cancel_cutover_job(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.cancel_cutover_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.cancel_cutover_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.CancelCutoverJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_cancel_cutover_job_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.cancel_cutover_job), "__call__"
    ) as call:
        client.cancel_cutover_job()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.CancelCutoverJobRequest()


@pytest.mark.asyncio
async def test_cancel_cutover_job_async(
    transport: str = "grpc_asyncio", request_type=vmmigration.CancelCutoverJobRequest
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.cancel_cutover_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.cancel_cutover_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.CancelCutoverJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_cancel_cutover_job_async_from_dict():
    await test_cancel_cutover_job_async(request_type=dict)


def test_cancel_cutover_job_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.CancelCutoverJobRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.cancel_cutover_job), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.cancel_cutover_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_cancel_cutover_job_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.CancelCutoverJobRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.cancel_cutover_job), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.cancel_cutover_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


def test_cancel_cutover_job_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.cancel_cutover_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.cancel_cutover_job(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_cancel_cutover_job_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.cancel_cutover_job(
            vmmigration.CancelCutoverJobRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_cancel_cutover_job_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.cancel_cutover_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.cancel_cutover_job(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_cancel_cutover_job_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.cancel_cutover_job(
            vmmigration.CancelCutoverJobRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.ListCutoverJobsRequest,
        dict,
    ],
)
def test_list_cutover_jobs(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cutover_jobs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.ListCutoverJobsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_cutover_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.ListCutoverJobsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCutoverJobsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_cutover_jobs_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cutover_jobs), "__call__"
    ) as call:
        client.list_cutover_jobs()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.ListCutoverJobsRequest()


@pytest.mark.asyncio
async def test_list_cutover_jobs_async(
    transport: str = "grpc_asyncio", request_type=vmmigration.ListCutoverJobsRequest
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cutover_jobs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.ListCutoverJobsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_cutover_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.ListCutoverJobsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCutoverJobsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_cutover_jobs_async_from_dict():
    await test_list_cutover_jobs_async(request_type=dict)


def test_list_cutover_jobs_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.ListCutoverJobsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cutover_jobs), "__call__"
    ) as call:
        call.return_value = vmmigration.ListCutoverJobsResponse()
        client.list_cutover_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_cutover_jobs_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.ListCutoverJobsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cutover_jobs), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.ListCutoverJobsResponse()
        )
        await client.list_cutover_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


def test_list_cutover_jobs_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cutover_jobs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.ListCutoverJobsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_cutover_jobs(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_cutover_jobs_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_cutover_jobs(
            vmmigration.ListCutoverJobsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_cutover_jobs_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cutover_jobs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.ListCutoverJobsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.ListCutoverJobsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_cutover_jobs(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_cutover_jobs_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_cutover_jobs(
            vmmigration.ListCutoverJobsRequest(),
            parent="parent_value",
        )


def test_list_cutover_jobs_pager(transport_name: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cutover_jobs), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            vmmigration.ListCutoverJobsResponse(
                cutover_jobs=[
                    vmmigration.CutoverJob(),
                    vmmigration.CutoverJob(),
                    vmmigration.CutoverJob(),
                ],
                next_page_token="abc",
            ),
            vmmigration.ListCutoverJobsResponse(
                cutover_jobs=[],
                next_page_token="def",
            ),
            vmmigration.ListCutoverJobsResponse(
                cutover_jobs=[
                    vmmigration.CutoverJob(),
                ],
                next_page_token="ghi",
            ),
            vmmigration.ListCutoverJobsResponse(
                cutover_jobs=[
                    vmmigration.CutoverJob(),
                    vmmigration.CutoverJob(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_cutover_jobs(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, vmmigration.CutoverJob) for i in results)


def test_list_cutover_jobs_pages(transport_name: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cutover_jobs), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            vmmigration.ListCutoverJobsResponse(
                cutover_jobs=[
                    vmmigration.CutoverJob(),
                    vmmigration.CutoverJob(),
                    vmmigration.CutoverJob(),
                ],
                next_page_token="abc",
            ),
            vmmigration.ListCutoverJobsResponse(
                cutover_jobs=[],
                next_page_token="def",
            ),
            vmmigration.ListCutoverJobsResponse(
                cutover_jobs=[
                    vmmigration.CutoverJob(),
                ],
                next_page_token="ghi",
            ),
            vmmigration.ListCutoverJobsResponse(
                cutover_jobs=[
                    vmmigration.CutoverJob(),
                    vmmigration.CutoverJob(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_cutover_jobs(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_cutover_jobs_async_pager():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cutover_jobs),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            vmmigration.ListCutoverJobsResponse(
                cutover_jobs=[
                    vmmigration.CutoverJob(),
                    vmmigration.CutoverJob(),
                    vmmigration.CutoverJob(),
                ],
                next_page_token="abc",
            ),
            vmmigration.ListCutoverJobsResponse(
                cutover_jobs=[],
                next_page_token="def",
            ),
            vmmigration.ListCutoverJobsResponse(
                cutover_jobs=[
                    vmmigration.CutoverJob(),
                ],
                next_page_token="ghi",
            ),
            vmmigration.ListCutoverJobsResponse(
                cutover_jobs=[
                    vmmigration.CutoverJob(),
                    vmmigration.CutoverJob(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_cutover_jobs(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, vmmigration.CutoverJob) for i in responses)


@pytest.mark.asyncio
async def test_list_cutover_jobs_async_pages():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cutover_jobs),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            vmmigration.ListCutoverJobsResponse(
                cutover_jobs=[
                    vmmigration.CutoverJob(),
                    vmmigration.CutoverJob(),
                    vmmigration.CutoverJob(),
                ],
                next_page_token="abc",
            ),
            vmmigration.ListCutoverJobsResponse(
                cutover_jobs=[],
                next_page_token="def",
            ),
            vmmigration.ListCutoverJobsResponse(
                cutover_jobs=[
                    vmmigration.CutoverJob(),
                ],
                next_page_token="ghi",
            ),
            vmmigration.ListCutoverJobsResponse(
                cutover_jobs=[
                    vmmigration.CutoverJob(),
                    vmmigration.CutoverJob(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_cutover_jobs(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.GetCutoverJobRequest,
        dict,
    ],
)
def test_get_cutover_job(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_cutover_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.CutoverJob(
            name="name_value",
            state=vmmigration.CutoverJob.State.PENDING,
            progress_percent=1733,
            state_message="state_message_value",
            compute_engine_target_details=vmmigration.ComputeEngineTargetDetails(
                vm_name="vm_name_value"
            ),
        )
        response = client.get_cutover_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.GetCutoverJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, vmmigration.CutoverJob)
    assert response.name == "name_value"
    assert response.state == vmmigration.CutoverJob.State.PENDING
    assert response.progress_percent == 1733
    assert response.state_message == "state_message_value"


def test_get_cutover_job_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_cutover_job), "__call__") as call:
        client.get_cutover_job()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.GetCutoverJobRequest()


@pytest.mark.asyncio
async def test_get_cutover_job_async(
    transport: str = "grpc_asyncio", request_type=vmmigration.GetCutoverJobRequest
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_cutover_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.CutoverJob(
                name="name_value",
                state=vmmigration.CutoverJob.State.PENDING,
                progress_percent=1733,
                state_message="state_message_value",
            )
        )
        response = await client.get_cutover_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.GetCutoverJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, vmmigration.CutoverJob)
    assert response.name == "name_value"
    assert response.state == vmmigration.CutoverJob.State.PENDING
    assert response.progress_percent == 1733
    assert response.state_message == "state_message_value"


@pytest.mark.asyncio
async def test_get_cutover_job_async_from_dict():
    await test_get_cutover_job_async(request_type=dict)


def test_get_cutover_job_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.GetCutoverJobRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_cutover_job), "__call__") as call:
        call.return_value = vmmigration.CutoverJob()
        client.get_cutover_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_cutover_job_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.GetCutoverJobRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_cutover_job), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.CutoverJob()
        )
        await client.get_cutover_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


def test_get_cutover_job_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_cutover_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.CutoverJob()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_cutover_job(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_cutover_job_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_cutover_job(
            vmmigration.GetCutoverJobRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_cutover_job_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_cutover_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.CutoverJob()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.CutoverJob()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_cutover_job(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_cutover_job_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_cutover_job(
            vmmigration.GetCutoverJobRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.ListGroupsRequest,
        dict,
    ],
)
def test_list_groups(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_groups), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.ListGroupsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_groups(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.ListGroupsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListGroupsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_groups_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_groups), "__call__") as call:
        client.list_groups()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.ListGroupsRequest()


@pytest.mark.asyncio
async def test_list_groups_async(
    transport: str = "grpc_asyncio", request_type=vmmigration.ListGroupsRequest
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_groups), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.ListGroupsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_groups(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.ListGroupsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListGroupsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_groups_async_from_dict():
    await test_list_groups_async(request_type=dict)


def test_list_groups_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.ListGroupsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_groups), "__call__") as call:
        call.return_value = vmmigration.ListGroupsResponse()
        client.list_groups(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_groups_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.ListGroupsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_groups), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.ListGroupsResponse()
        )
        await client.list_groups(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


def test_list_groups_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_groups), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.ListGroupsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_groups(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_groups_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_groups(
            vmmigration.ListGroupsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_groups_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_groups), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.ListGroupsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.ListGroupsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_groups(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_groups_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_groups(
            vmmigration.ListGroupsRequest(),
            parent="parent_value",
        )


def test_list_groups_pager(transport_name: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_groups), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            vmmigration.ListGroupsResponse(
                groups=[
                    vmmigration.Group(),
                    vmmigration.Group(),
                    vmmigration.Group(),
                ],
                next_page_token="abc",
            ),
            vmmigration.ListGroupsResponse(
                groups=[],
                next_page_token="def",
            ),
            vmmigration.ListGroupsResponse(
                groups=[
                    vmmigration.Group(),
                ],
                next_page_token="ghi",
            ),
            vmmigration.ListGroupsResponse(
                groups=[
                    vmmigration.Group(),
                    vmmigration.Group(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_groups(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, vmmigration.Group) for i in results)


def test_list_groups_pages(transport_name: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_groups), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            vmmigration.ListGroupsResponse(
                groups=[
                    vmmigration.Group(),
                    vmmigration.Group(),
                    vmmigration.Group(),
                ],
                next_page_token="abc",
            ),
            vmmigration.ListGroupsResponse(
                groups=[],
                next_page_token="def",
            ),
            vmmigration.ListGroupsResponse(
                groups=[
                    vmmigration.Group(),
                ],
                next_page_token="ghi",
            ),
            vmmigration.ListGroupsResponse(
                groups=[
                    vmmigration.Group(),
                    vmmigration.Group(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_groups(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_groups_async_pager():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_groups), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            vmmigration.ListGroupsResponse(
                groups=[
                    vmmigration.Group(),
                    vmmigration.Group(),
                    vmmigration.Group(),
                ],
                next_page_token="abc",
            ),
            vmmigration.ListGroupsResponse(
                groups=[],
                next_page_token="def",
            ),
            vmmigration.ListGroupsResponse(
                groups=[
                    vmmigration.Group(),
                ],
                next_page_token="ghi",
            ),
            vmmigration.ListGroupsResponse(
                groups=[
                    vmmigration.Group(),
                    vmmigration.Group(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_groups(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, vmmigration.Group) for i in responses)


@pytest.mark.asyncio
async def test_list_groups_async_pages():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_groups), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            vmmigration.ListGroupsResponse(
                groups=[
                    vmmigration.Group(),
                    vmmigration.Group(),
                    vmmigration.Group(),
                ],
                next_page_token="abc",
            ),
            vmmigration.ListGroupsResponse(
                groups=[],
                next_page_token="def",
            ),
            vmmigration.ListGroupsResponse(
                groups=[
                    vmmigration.Group(),
                ],
                next_page_token="ghi",
            ),
            vmmigration.ListGroupsResponse(
                groups=[
                    vmmigration.Group(),
                    vmmigration.Group(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_groups(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.GetGroupRequest,
        dict,
    ],
)
def test_get_group(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_group), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.Group(
            name="name_value",
            description="description_value",
            display_name="display_name_value",
        )
        response = client.get_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.GetGroupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, vmmigration.Group)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.display_name == "display_name_value"


def test_get_group_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_group), "__call__") as call:
        client.get_group()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.GetGroupRequest()


@pytest.mark.asyncio
async def test_get_group_async(
    transport: str = "grpc_asyncio", request_type=vmmigration.GetGroupRequest
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_group), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.Group(
                name="name_value",
                description="description_value",
                display_name="display_name_value",
            )
        )
        response = await client.get_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.GetGroupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, vmmigration.Group)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.display_name == "display_name_value"


@pytest.mark.asyncio
async def test_get_group_async_from_dict():
    await test_get_group_async(request_type=dict)


def test_get_group_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.GetGroupRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_group), "__call__") as call:
        call.return_value = vmmigration.Group()
        client.get_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_group_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.GetGroupRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_group), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(vmmigration.Group())
        await client.get_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


def test_get_group_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_group), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.Group()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_group(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_group_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_group(
            vmmigration.GetGroupRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_group_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_group), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.Group()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(vmmigration.Group())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_group(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_group_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_group(
            vmmigration.GetGroupRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.CreateGroupRequest,
        dict,
    ],
)
def test_create_group(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_group), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.CreateGroupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_group_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_group), "__call__") as call:
        client.create_group()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.CreateGroupRequest()


@pytest.mark.asyncio
async def test_create_group_async(
    transport: str = "grpc_asyncio", request_type=vmmigration.CreateGroupRequest
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_group), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.CreateGroupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_group_async_from_dict():
    await test_create_group_async(request_type=dict)


def test_create_group_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.CreateGroupRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_group), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_group_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.CreateGroupRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_group), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


def test_create_group_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_group), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_group(
            parent="parent_value",
            group=vmmigration.Group(name="name_value"),
            group_id="group_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].group
        mock_val = vmmigration.Group(name="name_value")
        assert arg == mock_val
        arg = args[0].group_id
        mock_val = "group_id_value"
        assert arg == mock_val


def test_create_group_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_group(
            vmmigration.CreateGroupRequest(),
            parent="parent_value",
            group=vmmigration.Group(name="name_value"),
            group_id="group_id_value",
        )


@pytest.mark.asyncio
async def test_create_group_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_group), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_group(
            parent="parent_value",
            group=vmmigration.Group(name="name_value"),
            group_id="group_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].group
        mock_val = vmmigration.Group(name="name_value")
        assert arg == mock_val
        arg = args[0].group_id
        mock_val = "group_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_group_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_group(
            vmmigration.CreateGroupRequest(),
            parent="parent_value",
            group=vmmigration.Group(name="name_value"),
            group_id="group_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.UpdateGroupRequest,
        dict,
    ],
)
def test_update_group(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_group), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.UpdateGroupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_group_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_group), "__call__") as call:
        client.update_group()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.UpdateGroupRequest()


@pytest.mark.asyncio
async def test_update_group_async(
    transport: str = "grpc_asyncio", request_type=vmmigration.UpdateGroupRequest
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_group), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.UpdateGroupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_group_async_from_dict():
    await test_update_group_async(request_type=dict)


def test_update_group_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.UpdateGroupRequest()

    request.group.name = "group.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_group), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "group.name=group.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_group_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.UpdateGroupRequest()

    request.group.name = "group.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_group), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "group.name=group.name/value",
    ) in kw["metadata"]


def test_update_group_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_group), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_group(
            group=vmmigration.Group(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].group
        mock_val = vmmigration.Group(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_group_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_group(
            vmmigration.UpdateGroupRequest(),
            group=vmmigration.Group(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_group_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_group), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_group(
            group=vmmigration.Group(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].group
        mock_val = vmmigration.Group(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_group_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_group(
            vmmigration.UpdateGroupRequest(),
            group=vmmigration.Group(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.DeleteGroupRequest,
        dict,
    ],
)
def test_delete_group(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_group), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.DeleteGroupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_group_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_group), "__call__") as call:
        client.delete_group()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.DeleteGroupRequest()


@pytest.mark.asyncio
async def test_delete_group_async(
    transport: str = "grpc_asyncio", request_type=vmmigration.DeleteGroupRequest
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_group), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.DeleteGroupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_group_async_from_dict():
    await test_delete_group_async(request_type=dict)


def test_delete_group_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.DeleteGroupRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_group), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_group_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.DeleteGroupRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_group), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_group(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


def test_delete_group_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_group), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_group(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_group_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_group(
            vmmigration.DeleteGroupRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_group_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_group), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_group(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_group_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_group(
            vmmigration.DeleteGroupRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.AddGroupMigrationRequest,
        dict,
    ],
)
def test_add_group_migration(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.add_group_migration), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.add_group_migration(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.AddGroupMigrationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_add_group_migration_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.add_group_migration), "__call__"
    ) as call:
        client.add_group_migration()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.AddGroupMigrationRequest()


@pytest.mark.asyncio
async def test_add_group_migration_async(
    transport: str = "grpc_asyncio", request_type=vmmigration.AddGroupMigrationRequest
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.add_group_migration), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.add_group_migration(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.AddGroupMigrationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_add_group_migration_async_from_dict():
    await test_add_group_migration_async(request_type=dict)


def test_add_group_migration_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.AddGroupMigrationRequest()

    request.group = "group/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.add_group_migration), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.add_group_migration(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "group=group/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_add_group_migration_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.AddGroupMigrationRequest()

    request.group = "group/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.add_group_migration), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.add_group_migration(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "group=group/value",
    ) in kw["metadata"]


def test_add_group_migration_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.add_group_migration), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.add_group_migration(
            group="group_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].group
        mock_val = "group_value"
        assert arg == mock_val


def test_add_group_migration_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.add_group_migration(
            vmmigration.AddGroupMigrationRequest(),
            group="group_value",
        )


@pytest.mark.asyncio
async def test_add_group_migration_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.add_group_migration), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.add_group_migration(
            group="group_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].group
        mock_val = "group_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_add_group_migration_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.add_group_migration(
            vmmigration.AddGroupMigrationRequest(),
            group="group_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.RemoveGroupMigrationRequest,
        dict,
    ],
)
def test_remove_group_migration(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.remove_group_migration), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.remove_group_migration(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.RemoveGroupMigrationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_remove_group_migration_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.remove_group_migration), "__call__"
    ) as call:
        client.remove_group_migration()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.RemoveGroupMigrationRequest()


@pytest.mark.asyncio
async def test_remove_group_migration_async(
    transport: str = "grpc_asyncio",
    request_type=vmmigration.RemoveGroupMigrationRequest,
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.remove_group_migration), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.remove_group_migration(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.RemoveGroupMigrationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_remove_group_migration_async_from_dict():
    await test_remove_group_migration_async(request_type=dict)


def test_remove_group_migration_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.RemoveGroupMigrationRequest()

    request.group = "group/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.remove_group_migration), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.remove_group_migration(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "group=group/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_remove_group_migration_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.RemoveGroupMigrationRequest()

    request.group = "group/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.remove_group_migration), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.remove_group_migration(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "group=group/value",
    ) in kw["metadata"]


def test_remove_group_migration_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.remove_group_migration), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.remove_group_migration(
            group="group_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].group
        mock_val = "group_value"
        assert arg == mock_val


def test_remove_group_migration_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.remove_group_migration(
            vmmigration.RemoveGroupMigrationRequest(),
            group="group_value",
        )


@pytest.mark.asyncio
async def test_remove_group_migration_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.remove_group_migration), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.remove_group_migration(
            group="group_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].group
        mock_val = "group_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_remove_group_migration_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.remove_group_migration(
            vmmigration.RemoveGroupMigrationRequest(),
            group="group_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.ListTargetProjectsRequest,
        dict,
    ],
)
def test_list_target_projects(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_target_projects), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.ListTargetProjectsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_target_projects(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.ListTargetProjectsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTargetProjectsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_target_projects_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_target_projects), "__call__"
    ) as call:
        client.list_target_projects()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.ListTargetProjectsRequest()


@pytest.mark.asyncio
async def test_list_target_projects_async(
    transport: str = "grpc_asyncio", request_type=vmmigration.ListTargetProjectsRequest
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_target_projects), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.ListTargetProjectsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_target_projects(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.ListTargetProjectsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTargetProjectsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_target_projects_async_from_dict():
    await test_list_target_projects_async(request_type=dict)


def test_list_target_projects_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.ListTargetProjectsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_target_projects), "__call__"
    ) as call:
        call.return_value = vmmigration.ListTargetProjectsResponse()
        client.list_target_projects(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_target_projects_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.ListTargetProjectsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_target_projects), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.ListTargetProjectsResponse()
        )
        await client.list_target_projects(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


def test_list_target_projects_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_target_projects), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.ListTargetProjectsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_target_projects(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_target_projects_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_target_projects(
            vmmigration.ListTargetProjectsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_target_projects_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_target_projects), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.ListTargetProjectsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.ListTargetProjectsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_target_projects(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_target_projects_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_target_projects(
            vmmigration.ListTargetProjectsRequest(),
            parent="parent_value",
        )


def test_list_target_projects_pager(transport_name: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_target_projects), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            vmmigration.ListTargetProjectsResponse(
                target_projects=[
                    vmmigration.TargetProject(),
                    vmmigration.TargetProject(),
                    vmmigration.TargetProject(),
                ],
                next_page_token="abc",
            ),
            vmmigration.ListTargetProjectsResponse(
                target_projects=[],
                next_page_token="def",
            ),
            vmmigration.ListTargetProjectsResponse(
                target_projects=[
                    vmmigration.TargetProject(),
                ],
                next_page_token="ghi",
            ),
            vmmigration.ListTargetProjectsResponse(
                target_projects=[
                    vmmigration.TargetProject(),
                    vmmigration.TargetProject(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_target_projects(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, vmmigration.TargetProject) for i in results)


def test_list_target_projects_pages(transport_name: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_target_projects), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            vmmigration.ListTargetProjectsResponse(
                target_projects=[
                    vmmigration.TargetProject(),
                    vmmigration.TargetProject(),
                    vmmigration.TargetProject(),
                ],
                next_page_token="abc",
            ),
            vmmigration.ListTargetProjectsResponse(
                target_projects=[],
                next_page_token="def",
            ),
            vmmigration.ListTargetProjectsResponse(
                target_projects=[
                    vmmigration.TargetProject(),
                ],
                next_page_token="ghi",
            ),
            vmmigration.ListTargetProjectsResponse(
                target_projects=[
                    vmmigration.TargetProject(),
                    vmmigration.TargetProject(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_target_projects(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_target_projects_async_pager():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_target_projects),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            vmmigration.ListTargetProjectsResponse(
                target_projects=[
                    vmmigration.TargetProject(),
                    vmmigration.TargetProject(),
                    vmmigration.TargetProject(),
                ],
                next_page_token="abc",
            ),
            vmmigration.ListTargetProjectsResponse(
                target_projects=[],
                next_page_token="def",
            ),
            vmmigration.ListTargetProjectsResponse(
                target_projects=[
                    vmmigration.TargetProject(),
                ],
                next_page_token="ghi",
            ),
            vmmigration.ListTargetProjectsResponse(
                target_projects=[
                    vmmigration.TargetProject(),
                    vmmigration.TargetProject(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_target_projects(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, vmmigration.TargetProject) for i in responses)


@pytest.mark.asyncio
async def test_list_target_projects_async_pages():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_target_projects),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            vmmigration.ListTargetProjectsResponse(
                target_projects=[
                    vmmigration.TargetProject(),
                    vmmigration.TargetProject(),
                    vmmigration.TargetProject(),
                ],
                next_page_token="abc",
            ),
            vmmigration.ListTargetProjectsResponse(
                target_projects=[],
                next_page_token="def",
            ),
            vmmigration.ListTargetProjectsResponse(
                target_projects=[
                    vmmigration.TargetProject(),
                ],
                next_page_token="ghi",
            ),
            vmmigration.ListTargetProjectsResponse(
                target_projects=[
                    vmmigration.TargetProject(),
                    vmmigration.TargetProject(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_target_projects(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.GetTargetProjectRequest,
        dict,
    ],
)
def test_get_target_project(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_target_project), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.TargetProject(
            name="name_value",
            project="project_value",
            description="description_value",
        )
        response = client.get_target_project(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.GetTargetProjectRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, vmmigration.TargetProject)
    assert response.name == "name_value"
    assert response.project == "project_value"
    assert response.description == "description_value"


def test_get_target_project_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_target_project), "__call__"
    ) as call:
        client.get_target_project()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.GetTargetProjectRequest()


@pytest.mark.asyncio
async def test_get_target_project_async(
    transport: str = "grpc_asyncio", request_type=vmmigration.GetTargetProjectRequest
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_target_project), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.TargetProject(
                name="name_value",
                project="project_value",
                description="description_value",
            )
        )
        response = await client.get_target_project(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.GetTargetProjectRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, vmmigration.TargetProject)
    assert response.name == "name_value"
    assert response.project == "project_value"
    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_get_target_project_async_from_dict():
    await test_get_target_project_async(request_type=dict)


def test_get_target_project_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.GetTargetProjectRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_target_project), "__call__"
    ) as call:
        call.return_value = vmmigration.TargetProject()
        client.get_target_project(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_target_project_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.GetTargetProjectRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_target_project), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.TargetProject()
        )
        await client.get_target_project(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


def test_get_target_project_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_target_project), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.TargetProject()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_target_project(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_target_project_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_target_project(
            vmmigration.GetTargetProjectRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_target_project_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_target_project), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = vmmigration.TargetProject()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vmmigration.TargetProject()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_target_project(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_target_project_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_target_project(
            vmmigration.GetTargetProjectRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.CreateTargetProjectRequest,
        dict,
    ],
)
def test_create_target_project(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_target_project), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_target_project(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.CreateTargetProjectRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_target_project_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_target_project), "__call__"
    ) as call:
        client.create_target_project()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.CreateTargetProjectRequest()


@pytest.mark.asyncio
async def test_create_target_project_async(
    transport: str = "grpc_asyncio", request_type=vmmigration.CreateTargetProjectRequest
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_target_project), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_target_project(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.CreateTargetProjectRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_target_project_async_from_dict():
    await test_create_target_project_async(request_type=dict)


def test_create_target_project_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.CreateTargetProjectRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_target_project), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_target_project(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_target_project_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.CreateTargetProjectRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_target_project), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_target_project(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent/value",
    ) in kw["metadata"]


def test_create_target_project_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_target_project), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_target_project(
            parent="parent_value",
            target_project=vmmigration.TargetProject(name="name_value"),
            target_project_id="target_project_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].target_project
        mock_val = vmmigration.TargetProject(name="name_value")
        assert arg == mock_val
        arg = args[0].target_project_id
        mock_val = "target_project_id_value"
        assert arg == mock_val


def test_create_target_project_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_target_project(
            vmmigration.CreateTargetProjectRequest(),
            parent="parent_value",
            target_project=vmmigration.TargetProject(name="name_value"),
            target_project_id="target_project_id_value",
        )


@pytest.mark.asyncio
async def test_create_target_project_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_target_project), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_target_project(
            parent="parent_value",
            target_project=vmmigration.TargetProject(name="name_value"),
            target_project_id="target_project_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].target_project
        mock_val = vmmigration.TargetProject(name="name_value")
        assert arg == mock_val
        arg = args[0].target_project_id
        mock_val = "target_project_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_target_project_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_target_project(
            vmmigration.CreateTargetProjectRequest(),
            parent="parent_value",
            target_project=vmmigration.TargetProject(name="name_value"),
            target_project_id="target_project_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.UpdateTargetProjectRequest,
        dict,
    ],
)
def test_update_target_project(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_target_project), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_target_project(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.UpdateTargetProjectRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_target_project_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_target_project), "__call__"
    ) as call:
        client.update_target_project()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.UpdateTargetProjectRequest()


@pytest.mark.asyncio
async def test_update_target_project_async(
    transport: str = "grpc_asyncio", request_type=vmmigration.UpdateTargetProjectRequest
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_target_project), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_target_project(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.UpdateTargetProjectRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_target_project_async_from_dict():
    await test_update_target_project_async(request_type=dict)


def test_update_target_project_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.UpdateTargetProjectRequest()

    request.target_project.name = "target_project.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_target_project), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_target_project(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "target_project.name=target_project.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_target_project_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.UpdateTargetProjectRequest()

    request.target_project.name = "target_project.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_target_project), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_target_project(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "target_project.name=target_project.name/value",
    ) in kw["metadata"]


def test_update_target_project_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_target_project), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_target_project(
            target_project=vmmigration.TargetProject(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].target_project
        mock_val = vmmigration.TargetProject(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_target_project_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_target_project(
            vmmigration.UpdateTargetProjectRequest(),
            target_project=vmmigration.TargetProject(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_target_project_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_target_project), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_target_project(
            target_project=vmmigration.TargetProject(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].target_project
        mock_val = vmmigration.TargetProject(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_target_project_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_target_project(
            vmmigration.UpdateTargetProjectRequest(),
            target_project=vmmigration.TargetProject(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        vmmigration.DeleteTargetProjectRequest,
        dict,
    ],
)
def test_delete_target_project(request_type, transport: str = "grpc"):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_target_project), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_target_project(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.DeleteTargetProjectRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_target_project_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_target_project), "__call__"
    ) as call:
        client.delete_target_project()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.DeleteTargetProjectRequest()


@pytest.mark.asyncio
async def test_delete_target_project_async(
    transport: str = "grpc_asyncio", request_type=vmmigration.DeleteTargetProjectRequest
):
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_target_project), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_target_project(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vmmigration.DeleteTargetProjectRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_target_project_async_from_dict():
    await test_delete_target_project_async(request_type=dict)


def test_delete_target_project_field_headers():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.DeleteTargetProjectRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_target_project), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_target_project(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_target_project_field_headers_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vmmigration.DeleteTargetProjectRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_target_project), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_target_project(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name/value",
    ) in kw["metadata"]


def test_delete_target_project_flattened():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_target_project), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_target_project(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_target_project_flattened_error():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_target_project(
            vmmigration.DeleteTargetProjectRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_target_project_flattened_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_target_project), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_target_project(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_target_project_flattened_error_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_target_project(
            vmmigration.DeleteTargetProjectRequest(),
            name="name_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.VmMigrationGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = VmMigrationClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.VmMigrationGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = VmMigrationClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.VmMigrationGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = VmMigrationClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = VmMigrationClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.VmMigrationGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = VmMigrationClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.VmMigrationGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = VmMigrationClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.VmMigrationGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.VmMigrationGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.VmMigrationGrpcTransport,
        transports.VmMigrationGrpcAsyncIOTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
    ],
)
def test_transport_kind(transport_name):
    transport = VmMigrationClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.VmMigrationGrpcTransport,
    )


def test_vm_migration_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.VmMigrationTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_vm_migration_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.vmmigration_v1.services.vm_migration.transports.VmMigrationTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.VmMigrationTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_sources",
        "get_source",
        "create_source",
        "update_source",
        "delete_source",
        "fetch_inventory",
        "list_utilization_reports",
        "get_utilization_report",
        "create_utilization_report",
        "delete_utilization_report",
        "list_datacenter_connectors",
        "get_datacenter_connector",
        "create_datacenter_connector",
        "delete_datacenter_connector",
        "create_migrating_vm",
        "list_migrating_vms",
        "get_migrating_vm",
        "update_migrating_vm",
        "delete_migrating_vm",
        "start_migration",
        "resume_migration",
        "pause_migration",
        "finalize_migration",
        "create_clone_job",
        "cancel_clone_job",
        "list_clone_jobs",
        "get_clone_job",
        "create_cutover_job",
        "cancel_cutover_job",
        "list_cutover_jobs",
        "get_cutover_job",
        "list_groups",
        "get_group",
        "create_group",
        "update_group",
        "delete_group",
        "add_group_migration",
        "remove_group_migration",
        "list_target_projects",
        "get_target_project",
        "create_target_project",
        "update_target_project",
        "delete_target_project",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client

    # Catch all for all remaining methods and properties
    remainder = [
        "kind",
    ]
    for r in remainder:
        with pytest.raises(NotImplementedError):
            getattr(transport, r)()


def test_vm_migration_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.vmmigration_v1.services.vm_migration.transports.VmMigrationTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.VmMigrationTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_vm_migration_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.vmmigration_v1.services.vm_migration.transports.VmMigrationTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.VmMigrationTransport()
        adc.assert_called_once()


def test_vm_migration_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        VmMigrationClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.VmMigrationGrpcTransport,
        transports.VmMigrationGrpcAsyncIOTransport,
    ],
)
def test_vm_migration_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.VmMigrationGrpcTransport, grpc_helpers),
        (transports.VmMigrationGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_vm_migration_transport_create_channel(transport_class, grpc_helpers):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel", autospec=True
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        adc.return_value = (creds, None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])

        create_channel.assert_called_with(
            "vmmigration.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="vmmigration.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.VmMigrationGrpcTransport, transports.VmMigrationGrpcAsyncIOTransport],
)
def test_vm_migration_grpc_transport_client_cert_source_for_mtls(transport_class):
    cred = ga_credentials.AnonymousCredentials()

    # Check ssl_channel_credentials is used if provided.
    with mock.patch.object(transport_class, "create_channel") as mock_create_channel:
        mock_ssl_channel_creds = mock.Mock()
        transport_class(
            host="squid.clam.whelk",
            credentials=cred,
            ssl_channel_credentials=mock_ssl_channel_creds,
        )
        mock_create_channel.assert_called_once_with(
            "squid.clam.whelk:443",
            credentials=cred,
            credentials_file=None,
            scopes=None,
            ssl_credentials=mock_ssl_channel_creds,
            quota_project_id=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )

    # Check if ssl_channel_credentials is not provided, then client_cert_source_for_mtls
    # is used.
    with mock.patch.object(transport_class, "create_channel", return_value=mock.Mock()):
        with mock.patch("grpc.ssl_channel_credentials") as mock_ssl_cred:
            transport_class(
                credentials=cred,
                client_cert_source_for_mtls=client_cert_source_callback,
            )
            expected_cert, expected_key = client_cert_source_callback()
            mock_ssl_cred.assert_called_once_with(
                certificate_chain=expected_cert, private_key=expected_key
            )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
    ],
)
def test_vm_migration_host_no_port(transport_name):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="vmmigration.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("vmmigration.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
    ],
)
def test_vm_migration_host_with_port(transport_name):
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="vmmigration.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("vmmigration.googleapis.com:8000")


def test_vm_migration_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.VmMigrationGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_vm_migration_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.VmMigrationGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [transports.VmMigrationGrpcTransport, transports.VmMigrationGrpcAsyncIOTransport],
)
def test_vm_migration_transport_channel_mtls_with_client_cert_source(transport_class):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = ga_credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(google.auth, "default") as adc:
                    adc.return_value = (cred, None)
                    transport = transport_class(
                        host="squid.clam.whelk",
                        api_mtls_endpoint="mtls.squid.clam.whelk",
                        client_cert_source=client_cert_source_callback,
                    )
                    adc.assert_called_once()

            grpc_ssl_channel_cred.assert_called_once_with(
                certificate_chain=b"cert bytes", private_key=b"key bytes"
            )
            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [transports.VmMigrationGrpcTransport, transports.VmMigrationGrpcAsyncIOTransport],
)
def test_vm_migration_transport_channel_mtls_with_adc(transport_class):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel
            mock_cred = mock.Mock()

            with pytest.warns(DeprecationWarning):
                transport = transport_class(
                    host="squid.clam.whelk",
                    credentials=mock_cred,
                    api_mtls_endpoint="mtls.squid.clam.whelk",
                    client_cert_source=None,
                )

            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=mock_cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_vm_migration_grpc_lro_client():
    client = VmMigrationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.OperationsClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_vm_migration_grpc_lro_async_client():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.OperationsAsyncClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_clone_job_path():
    project = "squid"
    location = "clam"
    source = "whelk"
    migrating_vm = "octopus"
    clone_job = "oyster"
    expected = "projects/{project}/locations/{location}/sources/{source}/migratingVms/{migrating_vm}/cloneJobs/{clone_job}".format(
        project=project,
        location=location,
        source=source,
        migrating_vm=migrating_vm,
        clone_job=clone_job,
    )
    actual = VmMigrationClient.clone_job_path(
        project, location, source, migrating_vm, clone_job
    )
    assert expected == actual


def test_parse_clone_job_path():
    expected = {
        "project": "nudibranch",
        "location": "cuttlefish",
        "source": "mussel",
        "migrating_vm": "winkle",
        "clone_job": "nautilus",
    }
    path = VmMigrationClient.clone_job_path(**expected)

    # Check that the path construction is reversible.
    actual = VmMigrationClient.parse_clone_job_path(path)
    assert expected == actual


def test_cutover_job_path():
    project = "scallop"
    location = "abalone"
    source = "squid"
    migrating_vm = "clam"
    cutover_job = "whelk"
    expected = "projects/{project}/locations/{location}/sources/{source}/migratingVms/{migrating_vm}/cutoverJobs/{cutover_job}".format(
        project=project,
        location=location,
        source=source,
        migrating_vm=migrating_vm,
        cutover_job=cutover_job,
    )
    actual = VmMigrationClient.cutover_job_path(
        project, location, source, migrating_vm, cutover_job
    )
    assert expected == actual


def test_parse_cutover_job_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "source": "nudibranch",
        "migrating_vm": "cuttlefish",
        "cutover_job": "mussel",
    }
    path = VmMigrationClient.cutover_job_path(**expected)

    # Check that the path construction is reversible.
    actual = VmMigrationClient.parse_cutover_job_path(path)
    assert expected == actual


def test_datacenter_connector_path():
    project = "winkle"
    location = "nautilus"
    source = "scallop"
    datacenter_connector = "abalone"
    expected = "projects/{project}/locations/{location}/sources/{source}/datacenterConnectors/{datacenter_connector}".format(
        project=project,
        location=location,
        source=source,
        datacenter_connector=datacenter_connector,
    )
    actual = VmMigrationClient.datacenter_connector_path(
        project, location, source, datacenter_connector
    )
    assert expected == actual


def test_parse_datacenter_connector_path():
    expected = {
        "project": "squid",
        "location": "clam",
        "source": "whelk",
        "datacenter_connector": "octopus",
    }
    path = VmMigrationClient.datacenter_connector_path(**expected)

    # Check that the path construction is reversible.
    actual = VmMigrationClient.parse_datacenter_connector_path(path)
    assert expected == actual


def test_group_path():
    project = "oyster"
    location = "nudibranch"
    group = "cuttlefish"
    expected = "projects/{project}/locations/{location}/groups/{group}".format(
        project=project,
        location=location,
        group=group,
    )
    actual = VmMigrationClient.group_path(project, location, group)
    assert expected == actual


def test_parse_group_path():
    expected = {
        "project": "mussel",
        "location": "winkle",
        "group": "nautilus",
    }
    path = VmMigrationClient.group_path(**expected)

    # Check that the path construction is reversible.
    actual = VmMigrationClient.parse_group_path(path)
    assert expected == actual


def test_migrating_vm_path():
    project = "scallop"
    location = "abalone"
    source = "squid"
    migrating_vm = "clam"
    expected = "projects/{project}/locations/{location}/sources/{source}/migratingVms/{migrating_vm}".format(
        project=project,
        location=location,
        source=source,
        migrating_vm=migrating_vm,
    )
    actual = VmMigrationClient.migrating_vm_path(
        project, location, source, migrating_vm
    )
    assert expected == actual


def test_parse_migrating_vm_path():
    expected = {
        "project": "whelk",
        "location": "octopus",
        "source": "oyster",
        "migrating_vm": "nudibranch",
    }
    path = VmMigrationClient.migrating_vm_path(**expected)

    # Check that the path construction is reversible.
    actual = VmMigrationClient.parse_migrating_vm_path(path)
    assert expected == actual


def test_source_path():
    project = "cuttlefish"
    location = "mussel"
    source = "winkle"
    expected = "projects/{project}/locations/{location}/sources/{source}".format(
        project=project,
        location=location,
        source=source,
    )
    actual = VmMigrationClient.source_path(project, location, source)
    assert expected == actual


def test_parse_source_path():
    expected = {
        "project": "nautilus",
        "location": "scallop",
        "source": "abalone",
    }
    path = VmMigrationClient.source_path(**expected)

    # Check that the path construction is reversible.
    actual = VmMigrationClient.parse_source_path(path)
    assert expected == actual


def test_target_project_path():
    project = "squid"
    location = "clam"
    target_project = "whelk"
    expected = "projects/{project}/locations/{location}/targetProjects/{target_project}".format(
        project=project,
        location=location,
        target_project=target_project,
    )
    actual = VmMigrationClient.target_project_path(project, location, target_project)
    assert expected == actual


def test_parse_target_project_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "target_project": "nudibranch",
    }
    path = VmMigrationClient.target_project_path(**expected)

    # Check that the path construction is reversible.
    actual = VmMigrationClient.parse_target_project_path(path)
    assert expected == actual


def test_utilization_report_path():
    project = "cuttlefish"
    location = "mussel"
    source = "winkle"
    utilization_report = "nautilus"
    expected = "projects/{project}/locations/{location}/sources/{source}/utilizationReports/{utilization_report}".format(
        project=project,
        location=location,
        source=source,
        utilization_report=utilization_report,
    )
    actual = VmMigrationClient.utilization_report_path(
        project, location, source, utilization_report
    )
    assert expected == actual


def test_parse_utilization_report_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
        "source": "squid",
        "utilization_report": "clam",
    }
    path = VmMigrationClient.utilization_report_path(**expected)

    # Check that the path construction is reversible.
    actual = VmMigrationClient.parse_utilization_report_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "whelk"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = VmMigrationClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "octopus",
    }
    path = VmMigrationClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = VmMigrationClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "oyster"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = VmMigrationClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nudibranch",
    }
    path = VmMigrationClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = VmMigrationClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "cuttlefish"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = VmMigrationClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "mussel",
    }
    path = VmMigrationClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = VmMigrationClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "winkle"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = VmMigrationClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nautilus",
    }
    path = VmMigrationClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = VmMigrationClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "scallop"
    location = "abalone"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = VmMigrationClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "squid",
        "location": "clam",
    }
    path = VmMigrationClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = VmMigrationClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.VmMigrationTransport, "_prep_wrapped_messages"
    ) as prep:
        client = VmMigrationClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.VmMigrationTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = VmMigrationClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = VmMigrationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(
        type(getattr(client.transport, "grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_transport_close():
    transports = {
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = VmMigrationClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        with mock.patch.object(
            type(getattr(client.transport, close_name)), "close"
        ) as close:
            with client:
                close.assert_not_called()
            close.assert_called_once()


def test_client_ctx():
    transports = [
        "grpc",
    ]
    for transport in transports:
        client = VmMigrationClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()


@pytest.mark.parametrize(
    "client_class,transport_class",
    [
        (VmMigrationClient, transports.VmMigrationGrpcTransport),
        (VmMigrationAsyncClient, transports.VmMigrationGrpcAsyncIOTransport),
    ],
)
def test_api_key_credentials(client_class, transport_class):
    with mock.patch.object(
        google.auth._default, "get_api_key_credentials", create=True
    ) as get_api_key_credentials:
        mock_cred = mock.Mock()
        get_api_key_credentials.return_value = mock_cred
        options = client_options.ClientOptions()
        options.api_key = "api_key"
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=mock_cred,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
            )
