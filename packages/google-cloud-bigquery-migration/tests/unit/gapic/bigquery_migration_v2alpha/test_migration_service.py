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
import os
import mock

import grpc
from grpc.experimental import aio
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule


from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.api_core import path_template
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.bigquery_migration_v2alpha.services.migration_service import (
    MigrationServiceAsyncClient,
)
from google.cloud.bigquery_migration_v2alpha.services.migration_service import (
    MigrationServiceClient,
)
from google.cloud.bigquery_migration_v2alpha.services.migration_service import pagers
from google.cloud.bigquery_migration_v2alpha.services.migration_service import (
    transports,
)
from google.cloud.bigquery_migration_v2alpha.types import assessment_task
from google.cloud.bigquery_migration_v2alpha.types import migration_entities
from google.cloud.bigquery_migration_v2alpha.types import migration_error_details
from google.cloud.bigquery_migration_v2alpha.types import migration_metrics
from google.cloud.bigquery_migration_v2alpha.types import migration_service
from google.cloud.bigquery_migration_v2alpha.types import translation_task
from google.oauth2 import service_account
from google.protobuf import any_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import error_details_pb2  # type: ignore
import google.auth


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

    assert MigrationServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        MigrationServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        MigrationServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        MigrationServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        MigrationServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        MigrationServiceClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class", [MigrationServiceClient, MigrationServiceAsyncClient,]
)
def test_migration_service_client_from_service_account_info(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "bigquerymigration.googleapis.com:443"


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.MigrationServiceGrpcTransport, "grpc"),
        (transports.MigrationServiceGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_migration_service_client_service_account_always_use_jwt(
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
    "client_class", [MigrationServiceClient, MigrationServiceAsyncClient,]
)
def test_migration_service_client_from_service_account_file(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "bigquerymigration.googleapis.com:443"


def test_migration_service_client_get_transport_class():
    transport = MigrationServiceClient.get_transport_class()
    available_transports = [
        transports.MigrationServiceGrpcTransport,
    ]
    assert transport in available_transports

    transport = MigrationServiceClient.get_transport_class("grpc")
    assert transport == transports.MigrationServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (MigrationServiceClient, transports.MigrationServiceGrpcTransport, "grpc"),
        (
            MigrationServiceAsyncClient,
            transports.MigrationServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    MigrationServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(MigrationServiceClient),
)
@mock.patch.object(
    MigrationServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(MigrationServiceAsyncClient),
)
def test_migration_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(MigrationServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(MigrationServiceClient, "get_transport_class") as gtc:
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
        (
            MigrationServiceClient,
            transports.MigrationServiceGrpcTransport,
            "grpc",
            "true",
        ),
        (
            MigrationServiceAsyncClient,
            transports.MigrationServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            MigrationServiceClient,
            transports.MigrationServiceGrpcTransport,
            "grpc",
            "false",
        ),
        (
            MigrationServiceAsyncClient,
            transports.MigrationServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    MigrationServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(MigrationServiceClient),
)
@mock.patch.object(
    MigrationServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(MigrationServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_migration_service_client_mtls_env_auto(
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


@pytest.mark.parametrize(
    "client_class", [MigrationServiceClient, MigrationServiceAsyncClient]
)
@mock.patch.object(
    MigrationServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(MigrationServiceClient),
)
@mock.patch.object(
    MigrationServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(MigrationServiceAsyncClient),
)
def test_migration_service_client_get_mtls_endpoint_and_cert_source(client_class):
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
        (MigrationServiceClient, transports.MigrationServiceGrpcTransport, "grpc"),
        (
            MigrationServiceAsyncClient,
            transports.MigrationServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_migration_service_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(scopes=["1", "2"],)
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
        (
            MigrationServiceClient,
            transports.MigrationServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            MigrationServiceAsyncClient,
            transports.MigrationServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_migration_service_client_client_options_credentials_file(
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


def test_migration_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.bigquery_migration_v2alpha.services.migration_service.transports.MigrationServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = MigrationServiceClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
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
        (
            MigrationServiceClient,
            transports.MigrationServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            MigrationServiceAsyncClient,
            transports.MigrationServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_migration_service_client_create_channel_credentials_file(
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
            "bigquerymigration.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="bigquerymigration.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type", [migration_service.CreateMigrationWorkflowRequest, dict,]
)
def test_create_migration_workflow(request_type, transport: str = "grpc"):
    client = MigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_migration_workflow), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = migration_entities.MigrationWorkflow(
            name="name_value",
            display_name="display_name_value",
            state=migration_entities.MigrationWorkflow.State.DRAFT,
        )
        response = client.create_migration_workflow(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == migration_service.CreateMigrationWorkflowRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, migration_entities.MigrationWorkflow)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.state == migration_entities.MigrationWorkflow.State.DRAFT


def test_create_migration_workflow_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_migration_workflow), "__call__"
    ) as call:
        client.create_migration_workflow()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == migration_service.CreateMigrationWorkflowRequest()


@pytest.mark.asyncio
async def test_create_migration_workflow_async(
    transport: str = "grpc_asyncio",
    request_type=migration_service.CreateMigrationWorkflowRequest,
):
    client = MigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_migration_workflow), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            migration_entities.MigrationWorkflow(
                name="name_value",
                display_name="display_name_value",
                state=migration_entities.MigrationWorkflow.State.DRAFT,
            )
        )
        response = await client.create_migration_workflow(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == migration_service.CreateMigrationWorkflowRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, migration_entities.MigrationWorkflow)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.state == migration_entities.MigrationWorkflow.State.DRAFT


@pytest.mark.asyncio
async def test_create_migration_workflow_async_from_dict():
    await test_create_migration_workflow_async(request_type=dict)


def test_create_migration_workflow_field_headers():
    client = MigrationServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = migration_service.CreateMigrationWorkflowRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_migration_workflow), "__call__"
    ) as call:
        call.return_value = migration_entities.MigrationWorkflow()
        client.create_migration_workflow(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_migration_workflow_field_headers_async():
    client = MigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = migration_service.CreateMigrationWorkflowRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_migration_workflow), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            migration_entities.MigrationWorkflow()
        )
        await client.create_migration_workflow(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_migration_workflow_flattened():
    client = MigrationServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_migration_workflow), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = migration_entities.MigrationWorkflow()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_migration_workflow(
            parent="parent_value",
            migration_workflow=migration_entities.MigrationWorkflow(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].migration_workflow
        mock_val = migration_entities.MigrationWorkflow(name="name_value")
        assert arg == mock_val


def test_create_migration_workflow_flattened_error():
    client = MigrationServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_migration_workflow(
            migration_service.CreateMigrationWorkflowRequest(),
            parent="parent_value",
            migration_workflow=migration_entities.MigrationWorkflow(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_migration_workflow_flattened_async():
    client = MigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_migration_workflow), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = migration_entities.MigrationWorkflow()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            migration_entities.MigrationWorkflow()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_migration_workflow(
            parent="parent_value",
            migration_workflow=migration_entities.MigrationWorkflow(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].migration_workflow
        mock_val = migration_entities.MigrationWorkflow(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_migration_workflow_flattened_error_async():
    client = MigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_migration_workflow(
            migration_service.CreateMigrationWorkflowRequest(),
            parent="parent_value",
            migration_workflow=migration_entities.MigrationWorkflow(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type", [migration_service.GetMigrationWorkflowRequest, dict,]
)
def test_get_migration_workflow(request_type, transport: str = "grpc"):
    client = MigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_migration_workflow), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = migration_entities.MigrationWorkflow(
            name="name_value",
            display_name="display_name_value",
            state=migration_entities.MigrationWorkflow.State.DRAFT,
        )
        response = client.get_migration_workflow(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == migration_service.GetMigrationWorkflowRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, migration_entities.MigrationWorkflow)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.state == migration_entities.MigrationWorkflow.State.DRAFT


def test_get_migration_workflow_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_migration_workflow), "__call__"
    ) as call:
        client.get_migration_workflow()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == migration_service.GetMigrationWorkflowRequest()


@pytest.mark.asyncio
async def test_get_migration_workflow_async(
    transport: str = "grpc_asyncio",
    request_type=migration_service.GetMigrationWorkflowRequest,
):
    client = MigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_migration_workflow), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            migration_entities.MigrationWorkflow(
                name="name_value",
                display_name="display_name_value",
                state=migration_entities.MigrationWorkflow.State.DRAFT,
            )
        )
        response = await client.get_migration_workflow(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == migration_service.GetMigrationWorkflowRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, migration_entities.MigrationWorkflow)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.state == migration_entities.MigrationWorkflow.State.DRAFT


@pytest.mark.asyncio
async def test_get_migration_workflow_async_from_dict():
    await test_get_migration_workflow_async(request_type=dict)


def test_get_migration_workflow_field_headers():
    client = MigrationServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = migration_service.GetMigrationWorkflowRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_migration_workflow), "__call__"
    ) as call:
        call.return_value = migration_entities.MigrationWorkflow()
        client.get_migration_workflow(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_migration_workflow_field_headers_async():
    client = MigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = migration_service.GetMigrationWorkflowRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_migration_workflow), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            migration_entities.MigrationWorkflow()
        )
        await client.get_migration_workflow(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_migration_workflow_flattened():
    client = MigrationServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_migration_workflow), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = migration_entities.MigrationWorkflow()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_migration_workflow(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_migration_workflow_flattened_error():
    client = MigrationServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_migration_workflow(
            migration_service.GetMigrationWorkflowRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_migration_workflow_flattened_async():
    client = MigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_migration_workflow), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = migration_entities.MigrationWorkflow()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            migration_entities.MigrationWorkflow()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_migration_workflow(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_migration_workflow_flattened_error_async():
    client = MigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_migration_workflow(
            migration_service.GetMigrationWorkflowRequest(), name="name_value",
        )


@pytest.mark.parametrize(
    "request_type", [migration_service.ListMigrationWorkflowsRequest, dict,]
)
def test_list_migration_workflows(request_type, transport: str = "grpc"):
    client = MigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migration_workflows), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = migration_service.ListMigrationWorkflowsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_migration_workflows(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == migration_service.ListMigrationWorkflowsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMigrationWorkflowsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_migration_workflows_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migration_workflows), "__call__"
    ) as call:
        client.list_migration_workflows()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == migration_service.ListMigrationWorkflowsRequest()


@pytest.mark.asyncio
async def test_list_migration_workflows_async(
    transport: str = "grpc_asyncio",
    request_type=migration_service.ListMigrationWorkflowsRequest,
):
    client = MigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migration_workflows), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            migration_service.ListMigrationWorkflowsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_migration_workflows(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == migration_service.ListMigrationWorkflowsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMigrationWorkflowsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_migration_workflows_async_from_dict():
    await test_list_migration_workflows_async(request_type=dict)


def test_list_migration_workflows_field_headers():
    client = MigrationServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = migration_service.ListMigrationWorkflowsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migration_workflows), "__call__"
    ) as call:
        call.return_value = migration_service.ListMigrationWorkflowsResponse()
        client.list_migration_workflows(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_migration_workflows_field_headers_async():
    client = MigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = migration_service.ListMigrationWorkflowsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migration_workflows), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            migration_service.ListMigrationWorkflowsResponse()
        )
        await client.list_migration_workflows(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_migration_workflows_flattened():
    client = MigrationServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migration_workflows), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = migration_service.ListMigrationWorkflowsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_migration_workflows(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_migration_workflows_flattened_error():
    client = MigrationServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_migration_workflows(
            migration_service.ListMigrationWorkflowsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_migration_workflows_flattened_async():
    client = MigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migration_workflows), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = migration_service.ListMigrationWorkflowsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            migration_service.ListMigrationWorkflowsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_migration_workflows(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_migration_workflows_flattened_error_async():
    client = MigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_migration_workflows(
            migration_service.ListMigrationWorkflowsRequest(), parent="parent_value",
        )


def test_list_migration_workflows_pager(transport_name: str = "grpc"):
    client = MigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials, transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migration_workflows), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            migration_service.ListMigrationWorkflowsResponse(
                migration_workflows=[
                    migration_entities.MigrationWorkflow(),
                    migration_entities.MigrationWorkflow(),
                    migration_entities.MigrationWorkflow(),
                ],
                next_page_token="abc",
            ),
            migration_service.ListMigrationWorkflowsResponse(
                migration_workflows=[], next_page_token="def",
            ),
            migration_service.ListMigrationWorkflowsResponse(
                migration_workflows=[migration_entities.MigrationWorkflow(),],
                next_page_token="ghi",
            ),
            migration_service.ListMigrationWorkflowsResponse(
                migration_workflows=[
                    migration_entities.MigrationWorkflow(),
                    migration_entities.MigrationWorkflow(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_migration_workflows(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, migration_entities.MigrationWorkflow) for i in results)


def test_list_migration_workflows_pages(transport_name: str = "grpc"):
    client = MigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials, transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migration_workflows), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            migration_service.ListMigrationWorkflowsResponse(
                migration_workflows=[
                    migration_entities.MigrationWorkflow(),
                    migration_entities.MigrationWorkflow(),
                    migration_entities.MigrationWorkflow(),
                ],
                next_page_token="abc",
            ),
            migration_service.ListMigrationWorkflowsResponse(
                migration_workflows=[], next_page_token="def",
            ),
            migration_service.ListMigrationWorkflowsResponse(
                migration_workflows=[migration_entities.MigrationWorkflow(),],
                next_page_token="ghi",
            ),
            migration_service.ListMigrationWorkflowsResponse(
                migration_workflows=[
                    migration_entities.MigrationWorkflow(),
                    migration_entities.MigrationWorkflow(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_migration_workflows(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_migration_workflows_async_pager():
    client = MigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migration_workflows),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            migration_service.ListMigrationWorkflowsResponse(
                migration_workflows=[
                    migration_entities.MigrationWorkflow(),
                    migration_entities.MigrationWorkflow(),
                    migration_entities.MigrationWorkflow(),
                ],
                next_page_token="abc",
            ),
            migration_service.ListMigrationWorkflowsResponse(
                migration_workflows=[], next_page_token="def",
            ),
            migration_service.ListMigrationWorkflowsResponse(
                migration_workflows=[migration_entities.MigrationWorkflow(),],
                next_page_token="ghi",
            ),
            migration_service.ListMigrationWorkflowsResponse(
                migration_workflows=[
                    migration_entities.MigrationWorkflow(),
                    migration_entities.MigrationWorkflow(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_migration_workflows(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, migration_entities.MigrationWorkflow) for i in responses
        )


@pytest.mark.asyncio
async def test_list_migration_workflows_async_pages():
    client = MigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migration_workflows),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            migration_service.ListMigrationWorkflowsResponse(
                migration_workflows=[
                    migration_entities.MigrationWorkflow(),
                    migration_entities.MigrationWorkflow(),
                    migration_entities.MigrationWorkflow(),
                ],
                next_page_token="abc",
            ),
            migration_service.ListMigrationWorkflowsResponse(
                migration_workflows=[], next_page_token="def",
            ),
            migration_service.ListMigrationWorkflowsResponse(
                migration_workflows=[migration_entities.MigrationWorkflow(),],
                next_page_token="ghi",
            ),
            migration_service.ListMigrationWorkflowsResponse(
                migration_workflows=[
                    migration_entities.MigrationWorkflow(),
                    migration_entities.MigrationWorkflow(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_migration_workflows(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type", [migration_service.DeleteMigrationWorkflowRequest, dict,]
)
def test_delete_migration_workflow(request_type, transport: str = "grpc"):
    client = MigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_migration_workflow), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_migration_workflow(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == migration_service.DeleteMigrationWorkflowRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_migration_workflow_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_migration_workflow), "__call__"
    ) as call:
        client.delete_migration_workflow()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == migration_service.DeleteMigrationWorkflowRequest()


@pytest.mark.asyncio
async def test_delete_migration_workflow_async(
    transport: str = "grpc_asyncio",
    request_type=migration_service.DeleteMigrationWorkflowRequest,
):
    client = MigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_migration_workflow), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_migration_workflow(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == migration_service.DeleteMigrationWorkflowRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_migration_workflow_async_from_dict():
    await test_delete_migration_workflow_async(request_type=dict)


def test_delete_migration_workflow_field_headers():
    client = MigrationServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = migration_service.DeleteMigrationWorkflowRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_migration_workflow), "__call__"
    ) as call:
        call.return_value = None
        client.delete_migration_workflow(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_migration_workflow_field_headers_async():
    client = MigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = migration_service.DeleteMigrationWorkflowRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_migration_workflow), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_migration_workflow(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_migration_workflow_flattened():
    client = MigrationServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_migration_workflow), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_migration_workflow(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_migration_workflow_flattened_error():
    client = MigrationServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_migration_workflow(
            migration_service.DeleteMigrationWorkflowRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_migration_workflow_flattened_async():
    client = MigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_migration_workflow), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_migration_workflow(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_migration_workflow_flattened_error_async():
    client = MigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_migration_workflow(
            migration_service.DeleteMigrationWorkflowRequest(), name="name_value",
        )


@pytest.mark.parametrize(
    "request_type", [migration_service.StartMigrationWorkflowRequest, dict,]
)
def test_start_migration_workflow(request_type, transport: str = "grpc"):
    client = MigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_migration_workflow), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.start_migration_workflow(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == migration_service.StartMigrationWorkflowRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_start_migration_workflow_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_migration_workflow), "__call__"
    ) as call:
        client.start_migration_workflow()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == migration_service.StartMigrationWorkflowRequest()


@pytest.mark.asyncio
async def test_start_migration_workflow_async(
    transport: str = "grpc_asyncio",
    request_type=migration_service.StartMigrationWorkflowRequest,
):
    client = MigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_migration_workflow), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.start_migration_workflow(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == migration_service.StartMigrationWorkflowRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_start_migration_workflow_async_from_dict():
    await test_start_migration_workflow_async(request_type=dict)


def test_start_migration_workflow_field_headers():
    client = MigrationServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = migration_service.StartMigrationWorkflowRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_migration_workflow), "__call__"
    ) as call:
        call.return_value = None
        client.start_migration_workflow(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_start_migration_workflow_field_headers_async():
    client = MigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = migration_service.StartMigrationWorkflowRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_migration_workflow), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.start_migration_workflow(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_start_migration_workflow_flattened():
    client = MigrationServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_migration_workflow), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.start_migration_workflow(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_start_migration_workflow_flattened_error():
    client = MigrationServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.start_migration_workflow(
            migration_service.StartMigrationWorkflowRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_start_migration_workflow_flattened_async():
    client = MigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_migration_workflow), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.start_migration_workflow(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_start_migration_workflow_flattened_error_async():
    client = MigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.start_migration_workflow(
            migration_service.StartMigrationWorkflowRequest(), name="name_value",
        )


@pytest.mark.parametrize(
    "request_type", [migration_service.GetMigrationSubtaskRequest, dict,]
)
def test_get_migration_subtask(request_type, transport: str = "grpc"):
    client = MigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_migration_subtask), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = migration_entities.MigrationSubtask(
            name="name_value",
            task_id="task_id_value",
            type_="type__value",
            state=migration_entities.MigrationSubtask.State.ACTIVE,
            resource_error_count=2169,
        )
        response = client.get_migration_subtask(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == migration_service.GetMigrationSubtaskRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, migration_entities.MigrationSubtask)
    assert response.name == "name_value"
    assert response.task_id == "task_id_value"
    assert response.type_ == "type__value"
    assert response.state == migration_entities.MigrationSubtask.State.ACTIVE
    assert response.resource_error_count == 2169


def test_get_migration_subtask_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_migration_subtask), "__call__"
    ) as call:
        client.get_migration_subtask()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == migration_service.GetMigrationSubtaskRequest()


@pytest.mark.asyncio
async def test_get_migration_subtask_async(
    transport: str = "grpc_asyncio",
    request_type=migration_service.GetMigrationSubtaskRequest,
):
    client = MigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_migration_subtask), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            migration_entities.MigrationSubtask(
                name="name_value",
                task_id="task_id_value",
                type_="type__value",
                state=migration_entities.MigrationSubtask.State.ACTIVE,
                resource_error_count=2169,
            )
        )
        response = await client.get_migration_subtask(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == migration_service.GetMigrationSubtaskRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, migration_entities.MigrationSubtask)
    assert response.name == "name_value"
    assert response.task_id == "task_id_value"
    assert response.type_ == "type__value"
    assert response.state == migration_entities.MigrationSubtask.State.ACTIVE
    assert response.resource_error_count == 2169


@pytest.mark.asyncio
async def test_get_migration_subtask_async_from_dict():
    await test_get_migration_subtask_async(request_type=dict)


def test_get_migration_subtask_field_headers():
    client = MigrationServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = migration_service.GetMigrationSubtaskRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_migration_subtask), "__call__"
    ) as call:
        call.return_value = migration_entities.MigrationSubtask()
        client.get_migration_subtask(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_migration_subtask_field_headers_async():
    client = MigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = migration_service.GetMigrationSubtaskRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_migration_subtask), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            migration_entities.MigrationSubtask()
        )
        await client.get_migration_subtask(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_migration_subtask_flattened():
    client = MigrationServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_migration_subtask), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = migration_entities.MigrationSubtask()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_migration_subtask(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_migration_subtask_flattened_error():
    client = MigrationServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_migration_subtask(
            migration_service.GetMigrationSubtaskRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_migration_subtask_flattened_async():
    client = MigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_migration_subtask), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = migration_entities.MigrationSubtask()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            migration_entities.MigrationSubtask()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_migration_subtask(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_migration_subtask_flattened_error_async():
    client = MigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_migration_subtask(
            migration_service.GetMigrationSubtaskRequest(), name="name_value",
        )


@pytest.mark.parametrize(
    "request_type", [migration_service.ListMigrationSubtasksRequest, dict,]
)
def test_list_migration_subtasks(request_type, transport: str = "grpc"):
    client = MigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migration_subtasks), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = migration_service.ListMigrationSubtasksResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_migration_subtasks(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == migration_service.ListMigrationSubtasksRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMigrationSubtasksPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_migration_subtasks_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migration_subtasks), "__call__"
    ) as call:
        client.list_migration_subtasks()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == migration_service.ListMigrationSubtasksRequest()


@pytest.mark.asyncio
async def test_list_migration_subtasks_async(
    transport: str = "grpc_asyncio",
    request_type=migration_service.ListMigrationSubtasksRequest,
):
    client = MigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migration_subtasks), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            migration_service.ListMigrationSubtasksResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_migration_subtasks(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == migration_service.ListMigrationSubtasksRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMigrationSubtasksAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_migration_subtasks_async_from_dict():
    await test_list_migration_subtasks_async(request_type=dict)


def test_list_migration_subtasks_field_headers():
    client = MigrationServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = migration_service.ListMigrationSubtasksRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migration_subtasks), "__call__"
    ) as call:
        call.return_value = migration_service.ListMigrationSubtasksResponse()
        client.list_migration_subtasks(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_migration_subtasks_field_headers_async():
    client = MigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = migration_service.ListMigrationSubtasksRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migration_subtasks), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            migration_service.ListMigrationSubtasksResponse()
        )
        await client.list_migration_subtasks(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_migration_subtasks_flattened():
    client = MigrationServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migration_subtasks), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = migration_service.ListMigrationSubtasksResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_migration_subtasks(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_migration_subtasks_flattened_error():
    client = MigrationServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_migration_subtasks(
            migration_service.ListMigrationSubtasksRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_migration_subtasks_flattened_async():
    client = MigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migration_subtasks), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = migration_service.ListMigrationSubtasksResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            migration_service.ListMigrationSubtasksResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_migration_subtasks(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_migration_subtasks_flattened_error_async():
    client = MigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_migration_subtasks(
            migration_service.ListMigrationSubtasksRequest(), parent="parent_value",
        )


def test_list_migration_subtasks_pager(transport_name: str = "grpc"):
    client = MigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials, transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migration_subtasks), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            migration_service.ListMigrationSubtasksResponse(
                migration_subtasks=[
                    migration_entities.MigrationSubtask(),
                    migration_entities.MigrationSubtask(),
                    migration_entities.MigrationSubtask(),
                ],
                next_page_token="abc",
            ),
            migration_service.ListMigrationSubtasksResponse(
                migration_subtasks=[], next_page_token="def",
            ),
            migration_service.ListMigrationSubtasksResponse(
                migration_subtasks=[migration_entities.MigrationSubtask(),],
                next_page_token="ghi",
            ),
            migration_service.ListMigrationSubtasksResponse(
                migration_subtasks=[
                    migration_entities.MigrationSubtask(),
                    migration_entities.MigrationSubtask(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_migration_subtasks(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, migration_entities.MigrationSubtask) for i in results)


def test_list_migration_subtasks_pages(transport_name: str = "grpc"):
    client = MigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials, transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migration_subtasks), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            migration_service.ListMigrationSubtasksResponse(
                migration_subtasks=[
                    migration_entities.MigrationSubtask(),
                    migration_entities.MigrationSubtask(),
                    migration_entities.MigrationSubtask(),
                ],
                next_page_token="abc",
            ),
            migration_service.ListMigrationSubtasksResponse(
                migration_subtasks=[], next_page_token="def",
            ),
            migration_service.ListMigrationSubtasksResponse(
                migration_subtasks=[migration_entities.MigrationSubtask(),],
                next_page_token="ghi",
            ),
            migration_service.ListMigrationSubtasksResponse(
                migration_subtasks=[
                    migration_entities.MigrationSubtask(),
                    migration_entities.MigrationSubtask(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_migration_subtasks(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_migration_subtasks_async_pager():
    client = MigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migration_subtasks),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            migration_service.ListMigrationSubtasksResponse(
                migration_subtasks=[
                    migration_entities.MigrationSubtask(),
                    migration_entities.MigrationSubtask(),
                    migration_entities.MigrationSubtask(),
                ],
                next_page_token="abc",
            ),
            migration_service.ListMigrationSubtasksResponse(
                migration_subtasks=[], next_page_token="def",
            ),
            migration_service.ListMigrationSubtasksResponse(
                migration_subtasks=[migration_entities.MigrationSubtask(),],
                next_page_token="ghi",
            ),
            migration_service.ListMigrationSubtasksResponse(
                migration_subtasks=[
                    migration_entities.MigrationSubtask(),
                    migration_entities.MigrationSubtask(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_migration_subtasks(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, migration_entities.MigrationSubtask) for i in responses
        )


@pytest.mark.asyncio
async def test_list_migration_subtasks_async_pages():
    client = MigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migration_subtasks),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            migration_service.ListMigrationSubtasksResponse(
                migration_subtasks=[
                    migration_entities.MigrationSubtask(),
                    migration_entities.MigrationSubtask(),
                    migration_entities.MigrationSubtask(),
                ],
                next_page_token="abc",
            ),
            migration_service.ListMigrationSubtasksResponse(
                migration_subtasks=[], next_page_token="def",
            ),
            migration_service.ListMigrationSubtasksResponse(
                migration_subtasks=[migration_entities.MigrationSubtask(),],
                next_page_token="ghi",
            ),
            migration_service.ListMigrationSubtasksResponse(
                migration_subtasks=[
                    migration_entities.MigrationSubtask(),
                    migration_entities.MigrationSubtask(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_migration_subtasks(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.MigrationServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = MigrationServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.MigrationServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = MigrationServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.MigrationServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = MigrationServiceClient(client_options=options, transport=transport,)

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = MigrationServiceClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.MigrationServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = MigrationServiceClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.MigrationServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = MigrationServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.MigrationServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.MigrationServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.MigrationServiceGrpcTransport,
        transports.MigrationServiceGrpcAsyncIOTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = MigrationServiceClient(credentials=ga_credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.MigrationServiceGrpcTransport,)


def test_migration_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.MigrationServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_migration_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.bigquery_migration_v2alpha.services.migration_service.transports.MigrationServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.MigrationServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_migration_workflow",
        "get_migration_workflow",
        "list_migration_workflows",
        "delete_migration_workflow",
        "start_migration_workflow",
        "get_migration_subtask",
        "list_migration_subtasks",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()


def test_migration_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.bigquery_migration_v2alpha.services.migration_service.transports.MigrationServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.MigrationServiceTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_migration_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.bigquery_migration_v2alpha.services.migration_service.transports.MigrationServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.MigrationServiceTransport()
        adc.assert_called_once()


def test_migration_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        MigrationServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.MigrationServiceGrpcTransport,
        transports.MigrationServiceGrpcAsyncIOTransport,
    ],
)
def test_migration_service_transport_auth_adc(transport_class):
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
        (transports.MigrationServiceGrpcTransport, grpc_helpers),
        (transports.MigrationServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_migration_service_transport_create_channel(transport_class, grpc_helpers):
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
            "bigquerymigration.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="bigquerymigration.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.MigrationServiceGrpcTransport,
        transports.MigrationServiceGrpcAsyncIOTransport,
    ],
)
def test_migration_service_grpc_transport_client_cert_source_for_mtls(transport_class):
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


def test_migration_service_host_no_port():
    client = MigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="bigquerymigration.googleapis.com"
        ),
    )
    assert client.transport._host == "bigquerymigration.googleapis.com:443"


def test_migration_service_host_with_port():
    client = MigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="bigquerymigration.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "bigquerymigration.googleapis.com:8000"


def test_migration_service_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.MigrationServiceGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_migration_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.MigrationServiceGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [
        transports.MigrationServiceGrpcTransport,
        transports.MigrationServiceGrpcAsyncIOTransport,
    ],
)
def test_migration_service_transport_channel_mtls_with_client_cert_source(
    transport_class,
):
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
    [
        transports.MigrationServiceGrpcTransport,
        transports.MigrationServiceGrpcAsyncIOTransport,
    ],
)
def test_migration_service_transport_channel_mtls_with_adc(transport_class):
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


def test_migration_subtask_path():
    project = "squid"
    location = "clam"
    workflow = "whelk"
    subtask = "octopus"
    expected = "projects/{project}/locations/{location}/workflows/{workflow}/subtasks/{subtask}".format(
        project=project, location=location, workflow=workflow, subtask=subtask,
    )
    actual = MigrationServiceClient.migration_subtask_path(
        project, location, workflow, subtask
    )
    assert expected == actual


def test_parse_migration_subtask_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
        "workflow": "cuttlefish",
        "subtask": "mussel",
    }
    path = MigrationServiceClient.migration_subtask_path(**expected)

    # Check that the path construction is reversible.
    actual = MigrationServiceClient.parse_migration_subtask_path(path)
    assert expected == actual


def test_migration_workflow_path():
    project = "winkle"
    location = "nautilus"
    workflow = "scallop"
    expected = "projects/{project}/locations/{location}/workflows/{workflow}".format(
        project=project, location=location, workflow=workflow,
    )
    actual = MigrationServiceClient.migration_workflow_path(project, location, workflow)
    assert expected == actual


def test_parse_migration_workflow_path():
    expected = {
        "project": "abalone",
        "location": "squid",
        "workflow": "clam",
    }
    path = MigrationServiceClient.migration_workflow_path(**expected)

    # Check that the path construction is reversible.
    actual = MigrationServiceClient.parse_migration_workflow_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "whelk"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = MigrationServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "octopus",
    }
    path = MigrationServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = MigrationServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "oyster"
    expected = "folders/{folder}".format(folder=folder,)
    actual = MigrationServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nudibranch",
    }
    path = MigrationServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = MigrationServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "cuttlefish"
    expected = "organizations/{organization}".format(organization=organization,)
    actual = MigrationServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "mussel",
    }
    path = MigrationServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = MigrationServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "winkle"
    expected = "projects/{project}".format(project=project,)
    actual = MigrationServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nautilus",
    }
    path = MigrationServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = MigrationServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "scallop"
    location = "abalone"
    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = MigrationServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "squid",
        "location": "clam",
    }
    path = MigrationServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = MigrationServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.MigrationServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = MigrationServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.MigrationServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = MigrationServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = MigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc_asyncio",
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
        client = MigrationServiceClient(
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
        client = MigrationServiceClient(
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
        (MigrationServiceClient, transports.MigrationServiceGrpcTransport),
        (MigrationServiceAsyncClient, transports.MigrationServiceGrpcAsyncIOTransport),
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
