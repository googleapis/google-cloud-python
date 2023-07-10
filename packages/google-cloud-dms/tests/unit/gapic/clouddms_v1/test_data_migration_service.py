# -*- coding: utf-8 -*-
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
#
import os

# try/except added for compatibility with python < 3.8
try:
    from unittest import mock
    from unittest.mock import AsyncMock  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    import mock

import math

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
from google.cloud.location import locations_pb2
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import options_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import any_pb2  # type: ignore
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest

from google.cloud.clouddms_v1.services.data_migration_service import (
    DataMigrationServiceAsyncClient,
    DataMigrationServiceClient,
    pagers,
    transports,
)
from google.cloud.clouddms_v1.types import (
    clouddms,
    clouddms_resources,
    conversionworkspace_resources,
)


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

    assert DataMigrationServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        DataMigrationServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        DataMigrationServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        DataMigrationServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        DataMigrationServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        DataMigrationServiceClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (DataMigrationServiceClient, "grpc"),
        (DataMigrationServiceAsyncClient, "grpc_asyncio"),
    ],
)
def test_data_migration_service_client_from_service_account_info(
    client_class, transport_name
):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == ("datamigration.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.DataMigrationServiceGrpcTransport, "grpc"),
        (transports.DataMigrationServiceGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_data_migration_service_client_service_account_always_use_jwt(
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
        (DataMigrationServiceClient, "grpc"),
        (DataMigrationServiceAsyncClient, "grpc_asyncio"),
    ],
)
def test_data_migration_service_client_from_service_account_file(
    client_class, transport_name
):
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

        assert client.transport._host == ("datamigration.googleapis.com:443")


def test_data_migration_service_client_get_transport_class():
    transport = DataMigrationServiceClient.get_transport_class()
    available_transports = [
        transports.DataMigrationServiceGrpcTransport,
    ]
    assert transport in available_transports

    transport = DataMigrationServiceClient.get_transport_class("grpc")
    assert transport == transports.DataMigrationServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            DataMigrationServiceClient,
            transports.DataMigrationServiceGrpcTransport,
            "grpc",
        ),
        (
            DataMigrationServiceAsyncClient,
            transports.DataMigrationServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    DataMigrationServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DataMigrationServiceClient),
)
@mock.patch.object(
    DataMigrationServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DataMigrationServiceAsyncClient),
)
def test_data_migration_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(DataMigrationServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(DataMigrationServiceClient, "get_transport_class") as gtc:
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
            api_audience=None,
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
                api_audience=None,
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
                api_audience=None,
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
            api_audience=None,
        )
    # Check the case api_endpoint is provided
    options = client_options.ClientOptions(
        api_audience="https://language.googleapis.com"
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience="https://language.googleapis.com",
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (
            DataMigrationServiceClient,
            transports.DataMigrationServiceGrpcTransport,
            "grpc",
            "true",
        ),
        (
            DataMigrationServiceAsyncClient,
            transports.DataMigrationServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            DataMigrationServiceClient,
            transports.DataMigrationServiceGrpcTransport,
            "grpc",
            "false",
        ),
        (
            DataMigrationServiceAsyncClient,
            transports.DataMigrationServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    DataMigrationServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DataMigrationServiceClient),
)
@mock.patch.object(
    DataMigrationServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DataMigrationServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_data_migration_service_client_mtls_env_auto(
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
                api_audience=None,
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
                        api_audience=None,
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
                    api_audience=None,
                )


@pytest.mark.parametrize(
    "client_class", [DataMigrationServiceClient, DataMigrationServiceAsyncClient]
)
@mock.patch.object(
    DataMigrationServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DataMigrationServiceClient),
)
@mock.patch.object(
    DataMigrationServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DataMigrationServiceAsyncClient),
)
def test_data_migration_service_client_get_mtls_endpoint_and_cert_source(client_class):
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
        (
            DataMigrationServiceClient,
            transports.DataMigrationServiceGrpcTransport,
            "grpc",
        ),
        (
            DataMigrationServiceAsyncClient,
            transports.DataMigrationServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_data_migration_service_client_client_options_scopes(
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
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (
            DataMigrationServiceClient,
            transports.DataMigrationServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            DataMigrationServiceAsyncClient,
            transports.DataMigrationServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_data_migration_service_client_client_options_credentials_file(
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
            api_audience=None,
        )


def test_data_migration_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.clouddms_v1.services.data_migration_service.transports.DataMigrationServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = DataMigrationServiceClient(
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
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (
            DataMigrationServiceClient,
            transports.DataMigrationServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            DataMigrationServiceAsyncClient,
            transports.DataMigrationServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_data_migration_service_client_create_channel_credentials_file(
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
            api_audience=None,
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
            "datamigration.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="datamigration.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        clouddms.ListMigrationJobsRequest,
        dict,
    ],
)
def test_list_migration_jobs(request_type, transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migration_jobs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = clouddms.ListMigrationJobsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_migration_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.ListMigrationJobsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMigrationJobsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_migration_jobs_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migration_jobs), "__call__"
    ) as call:
        client.list_migration_jobs()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.ListMigrationJobsRequest()


@pytest.mark.asyncio
async def test_list_migration_jobs_async(
    transport: str = "grpc_asyncio", request_type=clouddms.ListMigrationJobsRequest
):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migration_jobs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            clouddms.ListMigrationJobsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_migration_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.ListMigrationJobsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMigrationJobsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_migration_jobs_async_from_dict():
    await test_list_migration_jobs_async(request_type=dict)


def test_list_migration_jobs_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.ListMigrationJobsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migration_jobs), "__call__"
    ) as call:
        call.return_value = clouddms.ListMigrationJobsResponse()
        client.list_migration_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_migration_jobs_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.ListMigrationJobsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migration_jobs), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            clouddms.ListMigrationJobsResponse()
        )
        await client.list_migration_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_migration_jobs_flattened():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migration_jobs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = clouddms.ListMigrationJobsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_migration_jobs(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_migration_jobs_flattened_error():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_migration_jobs(
            clouddms.ListMigrationJobsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_migration_jobs_flattened_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migration_jobs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = clouddms.ListMigrationJobsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            clouddms.ListMigrationJobsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_migration_jobs(
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
async def test_list_migration_jobs_flattened_error_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_migration_jobs(
            clouddms.ListMigrationJobsRequest(),
            parent="parent_value",
        )


def test_list_migration_jobs_pager(transport_name: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migration_jobs), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            clouddms.ListMigrationJobsResponse(
                migration_jobs=[
                    clouddms_resources.MigrationJob(),
                    clouddms_resources.MigrationJob(),
                    clouddms_resources.MigrationJob(),
                ],
                next_page_token="abc",
            ),
            clouddms.ListMigrationJobsResponse(
                migration_jobs=[],
                next_page_token="def",
            ),
            clouddms.ListMigrationJobsResponse(
                migration_jobs=[
                    clouddms_resources.MigrationJob(),
                ],
                next_page_token="ghi",
            ),
            clouddms.ListMigrationJobsResponse(
                migration_jobs=[
                    clouddms_resources.MigrationJob(),
                    clouddms_resources.MigrationJob(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_migration_jobs(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, clouddms_resources.MigrationJob) for i in results)


def test_list_migration_jobs_pages(transport_name: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migration_jobs), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            clouddms.ListMigrationJobsResponse(
                migration_jobs=[
                    clouddms_resources.MigrationJob(),
                    clouddms_resources.MigrationJob(),
                    clouddms_resources.MigrationJob(),
                ],
                next_page_token="abc",
            ),
            clouddms.ListMigrationJobsResponse(
                migration_jobs=[],
                next_page_token="def",
            ),
            clouddms.ListMigrationJobsResponse(
                migration_jobs=[
                    clouddms_resources.MigrationJob(),
                ],
                next_page_token="ghi",
            ),
            clouddms.ListMigrationJobsResponse(
                migration_jobs=[
                    clouddms_resources.MigrationJob(),
                    clouddms_resources.MigrationJob(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_migration_jobs(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_migration_jobs_async_pager():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migration_jobs),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            clouddms.ListMigrationJobsResponse(
                migration_jobs=[
                    clouddms_resources.MigrationJob(),
                    clouddms_resources.MigrationJob(),
                    clouddms_resources.MigrationJob(),
                ],
                next_page_token="abc",
            ),
            clouddms.ListMigrationJobsResponse(
                migration_jobs=[],
                next_page_token="def",
            ),
            clouddms.ListMigrationJobsResponse(
                migration_jobs=[
                    clouddms_resources.MigrationJob(),
                ],
                next_page_token="ghi",
            ),
            clouddms.ListMigrationJobsResponse(
                migration_jobs=[
                    clouddms_resources.MigrationJob(),
                    clouddms_resources.MigrationJob(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_migration_jobs(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, clouddms_resources.MigrationJob) for i in responses)


@pytest.mark.asyncio
async def test_list_migration_jobs_async_pages():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_migration_jobs),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            clouddms.ListMigrationJobsResponse(
                migration_jobs=[
                    clouddms_resources.MigrationJob(),
                    clouddms_resources.MigrationJob(),
                    clouddms_resources.MigrationJob(),
                ],
                next_page_token="abc",
            ),
            clouddms.ListMigrationJobsResponse(
                migration_jobs=[],
                next_page_token="def",
            ),
            clouddms.ListMigrationJobsResponse(
                migration_jobs=[
                    clouddms_resources.MigrationJob(),
                ],
                next_page_token="ghi",
            ),
            clouddms.ListMigrationJobsResponse(
                migration_jobs=[
                    clouddms_resources.MigrationJob(),
                    clouddms_resources.MigrationJob(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_migration_jobs(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        clouddms.GetMigrationJobRequest,
        dict,
    ],
)
def test_get_migration_job(request_type, transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_migration_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = clouddms_resources.MigrationJob(
            name="name_value",
            display_name="display_name_value",
            state=clouddms_resources.MigrationJob.State.MAINTENANCE,
            phase=clouddms_resources.MigrationJob.Phase.FULL_DUMP,
            type_=clouddms_resources.MigrationJob.Type.ONE_TIME,
            dump_path="dump_path_value",
            source="source_value",
            destination="destination_value",
            filter="filter_value",
            cmek_key_name="cmek_key_name_value",
        )
        response = client.get_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.GetMigrationJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, clouddms_resources.MigrationJob)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.state == clouddms_resources.MigrationJob.State.MAINTENANCE
    assert response.phase == clouddms_resources.MigrationJob.Phase.FULL_DUMP
    assert response.type_ == clouddms_resources.MigrationJob.Type.ONE_TIME
    assert response.dump_path == "dump_path_value"
    assert response.source == "source_value"
    assert response.destination == "destination_value"
    assert response.filter == "filter_value"
    assert response.cmek_key_name == "cmek_key_name_value"


def test_get_migration_job_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_migration_job), "__call__"
    ) as call:
        client.get_migration_job()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.GetMigrationJobRequest()


@pytest.mark.asyncio
async def test_get_migration_job_async(
    transport: str = "grpc_asyncio", request_type=clouddms.GetMigrationJobRequest
):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_migration_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            clouddms_resources.MigrationJob(
                name="name_value",
                display_name="display_name_value",
                state=clouddms_resources.MigrationJob.State.MAINTENANCE,
                phase=clouddms_resources.MigrationJob.Phase.FULL_DUMP,
                type_=clouddms_resources.MigrationJob.Type.ONE_TIME,
                dump_path="dump_path_value",
                source="source_value",
                destination="destination_value",
                filter="filter_value",
                cmek_key_name="cmek_key_name_value",
            )
        )
        response = await client.get_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.GetMigrationJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, clouddms_resources.MigrationJob)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.state == clouddms_resources.MigrationJob.State.MAINTENANCE
    assert response.phase == clouddms_resources.MigrationJob.Phase.FULL_DUMP
    assert response.type_ == clouddms_resources.MigrationJob.Type.ONE_TIME
    assert response.dump_path == "dump_path_value"
    assert response.source == "source_value"
    assert response.destination == "destination_value"
    assert response.filter == "filter_value"
    assert response.cmek_key_name == "cmek_key_name_value"


@pytest.mark.asyncio
async def test_get_migration_job_async_from_dict():
    await test_get_migration_job_async(request_type=dict)


def test_get_migration_job_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.GetMigrationJobRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_migration_job), "__call__"
    ) as call:
        call.return_value = clouddms_resources.MigrationJob()
        client.get_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_migration_job_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.GetMigrationJobRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_migration_job), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            clouddms_resources.MigrationJob()
        )
        await client.get_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_migration_job_flattened():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_migration_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = clouddms_resources.MigrationJob()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_migration_job(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_migration_job_flattened_error():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_migration_job(
            clouddms.GetMigrationJobRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_migration_job_flattened_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_migration_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = clouddms_resources.MigrationJob()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            clouddms_resources.MigrationJob()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_migration_job(
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
async def test_get_migration_job_flattened_error_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_migration_job(
            clouddms.GetMigrationJobRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        clouddms.CreateMigrationJobRequest,
        dict,
    ],
)
def test_create_migration_job(request_type, transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_migration_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.CreateMigrationJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_migration_job_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_migration_job), "__call__"
    ) as call:
        client.create_migration_job()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.CreateMigrationJobRequest()


@pytest.mark.asyncio
async def test_create_migration_job_async(
    transport: str = "grpc_asyncio", request_type=clouddms.CreateMigrationJobRequest
):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_migration_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.CreateMigrationJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_migration_job_async_from_dict():
    await test_create_migration_job_async(request_type=dict)


def test_create_migration_job_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.CreateMigrationJobRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_migration_job), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_migration_job_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.CreateMigrationJobRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_migration_job), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_migration_job_flattened():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_migration_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_migration_job(
            parent="parent_value",
            migration_job=clouddms_resources.MigrationJob(name="name_value"),
            migration_job_id="migration_job_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].migration_job
        mock_val = clouddms_resources.MigrationJob(name="name_value")
        assert arg == mock_val
        arg = args[0].migration_job_id
        mock_val = "migration_job_id_value"
        assert arg == mock_val


def test_create_migration_job_flattened_error():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_migration_job(
            clouddms.CreateMigrationJobRequest(),
            parent="parent_value",
            migration_job=clouddms_resources.MigrationJob(name="name_value"),
            migration_job_id="migration_job_id_value",
        )


@pytest.mark.asyncio
async def test_create_migration_job_flattened_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_migration_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_migration_job(
            parent="parent_value",
            migration_job=clouddms_resources.MigrationJob(name="name_value"),
            migration_job_id="migration_job_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].migration_job
        mock_val = clouddms_resources.MigrationJob(name="name_value")
        assert arg == mock_val
        arg = args[0].migration_job_id
        mock_val = "migration_job_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_migration_job_flattened_error_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_migration_job(
            clouddms.CreateMigrationJobRequest(),
            parent="parent_value",
            migration_job=clouddms_resources.MigrationJob(name="name_value"),
            migration_job_id="migration_job_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        clouddms.UpdateMigrationJobRequest,
        dict,
    ],
)
def test_update_migration_job(request_type, transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_migration_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.UpdateMigrationJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_migration_job_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_migration_job), "__call__"
    ) as call:
        client.update_migration_job()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.UpdateMigrationJobRequest()


@pytest.mark.asyncio
async def test_update_migration_job_async(
    transport: str = "grpc_asyncio", request_type=clouddms.UpdateMigrationJobRequest
):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_migration_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.UpdateMigrationJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_migration_job_async_from_dict():
    await test_update_migration_job_async(request_type=dict)


def test_update_migration_job_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.UpdateMigrationJobRequest()

    request.migration_job.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_migration_job), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "migration_job.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_migration_job_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.UpdateMigrationJobRequest()

    request.migration_job.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_migration_job), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "migration_job.name=name_value",
    ) in kw["metadata"]


def test_update_migration_job_flattened():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_migration_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_migration_job(
            migration_job=clouddms_resources.MigrationJob(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].migration_job
        mock_val = clouddms_resources.MigrationJob(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_migration_job_flattened_error():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_migration_job(
            clouddms.UpdateMigrationJobRequest(),
            migration_job=clouddms_resources.MigrationJob(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_migration_job_flattened_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_migration_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_migration_job(
            migration_job=clouddms_resources.MigrationJob(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].migration_job
        mock_val = clouddms_resources.MigrationJob(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_migration_job_flattened_error_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_migration_job(
            clouddms.UpdateMigrationJobRequest(),
            migration_job=clouddms_resources.MigrationJob(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        clouddms.DeleteMigrationJobRequest,
        dict,
    ],
)
def test_delete_migration_job(request_type, transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_migration_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.DeleteMigrationJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_migration_job_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_migration_job), "__call__"
    ) as call:
        client.delete_migration_job()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.DeleteMigrationJobRequest()


@pytest.mark.asyncio
async def test_delete_migration_job_async(
    transport: str = "grpc_asyncio", request_type=clouddms.DeleteMigrationJobRequest
):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_migration_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.DeleteMigrationJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_migration_job_async_from_dict():
    await test_delete_migration_job_async(request_type=dict)


def test_delete_migration_job_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.DeleteMigrationJobRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_migration_job), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_migration_job_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.DeleteMigrationJobRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_migration_job), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_delete_migration_job_flattened():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_migration_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_migration_job(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_migration_job_flattened_error():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_migration_job(
            clouddms.DeleteMigrationJobRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_migration_job_flattened_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_migration_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_migration_job(
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
async def test_delete_migration_job_flattened_error_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_migration_job(
            clouddms.DeleteMigrationJobRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        clouddms.StartMigrationJobRequest,
        dict,
    ],
)
def test_start_migration_job(request_type, transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_migration_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.start_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.StartMigrationJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_start_migration_job_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_migration_job), "__call__"
    ) as call:
        client.start_migration_job()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.StartMigrationJobRequest()


@pytest.mark.asyncio
async def test_start_migration_job_async(
    transport: str = "grpc_asyncio", request_type=clouddms.StartMigrationJobRequest
):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_migration_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.start_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.StartMigrationJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_start_migration_job_async_from_dict():
    await test_start_migration_job_async(request_type=dict)


def test_start_migration_job_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.StartMigrationJobRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_migration_job), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.start_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_start_migration_job_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.StartMigrationJobRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.start_migration_job), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.start_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        clouddms.StopMigrationJobRequest,
        dict,
    ],
)
def test_stop_migration_job(request_type, transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.stop_migration_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.stop_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.StopMigrationJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_stop_migration_job_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.stop_migration_job), "__call__"
    ) as call:
        client.stop_migration_job()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.StopMigrationJobRequest()


@pytest.mark.asyncio
async def test_stop_migration_job_async(
    transport: str = "grpc_asyncio", request_type=clouddms.StopMigrationJobRequest
):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.stop_migration_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.stop_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.StopMigrationJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_stop_migration_job_async_from_dict():
    await test_stop_migration_job_async(request_type=dict)


def test_stop_migration_job_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.StopMigrationJobRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.stop_migration_job), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.stop_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_stop_migration_job_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.StopMigrationJobRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.stop_migration_job), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.stop_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        clouddms.ResumeMigrationJobRequest,
        dict,
    ],
)
def test_resume_migration_job(request_type, transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.resume_migration_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.resume_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.ResumeMigrationJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_resume_migration_job_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.resume_migration_job), "__call__"
    ) as call:
        client.resume_migration_job()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.ResumeMigrationJobRequest()


@pytest.mark.asyncio
async def test_resume_migration_job_async(
    transport: str = "grpc_asyncio", request_type=clouddms.ResumeMigrationJobRequest
):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.resume_migration_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.resume_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.ResumeMigrationJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_resume_migration_job_async_from_dict():
    await test_resume_migration_job_async(request_type=dict)


def test_resume_migration_job_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.ResumeMigrationJobRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.resume_migration_job), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.resume_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_resume_migration_job_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.ResumeMigrationJobRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.resume_migration_job), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.resume_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        clouddms.PromoteMigrationJobRequest,
        dict,
    ],
)
def test_promote_migration_job(request_type, transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.promote_migration_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.promote_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.PromoteMigrationJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_promote_migration_job_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.promote_migration_job), "__call__"
    ) as call:
        client.promote_migration_job()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.PromoteMigrationJobRequest()


@pytest.mark.asyncio
async def test_promote_migration_job_async(
    transport: str = "grpc_asyncio", request_type=clouddms.PromoteMigrationJobRequest
):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.promote_migration_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.promote_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.PromoteMigrationJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_promote_migration_job_async_from_dict():
    await test_promote_migration_job_async(request_type=dict)


def test_promote_migration_job_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.PromoteMigrationJobRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.promote_migration_job), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.promote_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_promote_migration_job_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.PromoteMigrationJobRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.promote_migration_job), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.promote_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        clouddms.VerifyMigrationJobRequest,
        dict,
    ],
)
def test_verify_migration_job(request_type, transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.verify_migration_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.verify_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.VerifyMigrationJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_verify_migration_job_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.verify_migration_job), "__call__"
    ) as call:
        client.verify_migration_job()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.VerifyMigrationJobRequest()


@pytest.mark.asyncio
async def test_verify_migration_job_async(
    transport: str = "grpc_asyncio", request_type=clouddms.VerifyMigrationJobRequest
):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.verify_migration_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.verify_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.VerifyMigrationJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_verify_migration_job_async_from_dict():
    await test_verify_migration_job_async(request_type=dict)


def test_verify_migration_job_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.VerifyMigrationJobRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.verify_migration_job), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.verify_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_verify_migration_job_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.VerifyMigrationJobRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.verify_migration_job), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.verify_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        clouddms.RestartMigrationJobRequest,
        dict,
    ],
)
def test_restart_migration_job(request_type, transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.restart_migration_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.restart_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.RestartMigrationJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_restart_migration_job_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.restart_migration_job), "__call__"
    ) as call:
        client.restart_migration_job()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.RestartMigrationJobRequest()


@pytest.mark.asyncio
async def test_restart_migration_job_async(
    transport: str = "grpc_asyncio", request_type=clouddms.RestartMigrationJobRequest
):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.restart_migration_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.restart_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.RestartMigrationJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_restart_migration_job_async_from_dict():
    await test_restart_migration_job_async(request_type=dict)


def test_restart_migration_job_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.RestartMigrationJobRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.restart_migration_job), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.restart_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_restart_migration_job_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.RestartMigrationJobRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.restart_migration_job), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.restart_migration_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        clouddms.GenerateSshScriptRequest,
        dict,
    ],
)
def test_generate_ssh_script(request_type, transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_ssh_script), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = clouddms.SshScript(
            script="script_value",
        )
        response = client.generate_ssh_script(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.GenerateSshScriptRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, clouddms.SshScript)
    assert response.script == "script_value"


def test_generate_ssh_script_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_ssh_script), "__call__"
    ) as call:
        client.generate_ssh_script()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.GenerateSshScriptRequest()


@pytest.mark.asyncio
async def test_generate_ssh_script_async(
    transport: str = "grpc_asyncio", request_type=clouddms.GenerateSshScriptRequest
):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_ssh_script), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            clouddms.SshScript(
                script="script_value",
            )
        )
        response = await client.generate_ssh_script(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.GenerateSshScriptRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, clouddms.SshScript)
    assert response.script == "script_value"


@pytest.mark.asyncio
async def test_generate_ssh_script_async_from_dict():
    await test_generate_ssh_script_async(request_type=dict)


def test_generate_ssh_script_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.GenerateSshScriptRequest()

    request.migration_job = "migration_job_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_ssh_script), "__call__"
    ) as call:
        call.return_value = clouddms.SshScript()
        client.generate_ssh_script(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "migration_job=migration_job_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_generate_ssh_script_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.GenerateSshScriptRequest()

    request.migration_job = "migration_job_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_ssh_script), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(clouddms.SshScript())
        await client.generate_ssh_script(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "migration_job=migration_job_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        clouddms.ListConnectionProfilesRequest,
        dict,
    ],
)
def test_list_connection_profiles(request_type, transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_connection_profiles), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = clouddms.ListConnectionProfilesResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_connection_profiles(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.ListConnectionProfilesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListConnectionProfilesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_connection_profiles_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_connection_profiles), "__call__"
    ) as call:
        client.list_connection_profiles()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.ListConnectionProfilesRequest()


@pytest.mark.asyncio
async def test_list_connection_profiles_async(
    transport: str = "grpc_asyncio", request_type=clouddms.ListConnectionProfilesRequest
):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_connection_profiles), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            clouddms.ListConnectionProfilesResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_connection_profiles(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.ListConnectionProfilesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListConnectionProfilesAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_connection_profiles_async_from_dict():
    await test_list_connection_profiles_async(request_type=dict)


def test_list_connection_profiles_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.ListConnectionProfilesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_connection_profiles), "__call__"
    ) as call:
        call.return_value = clouddms.ListConnectionProfilesResponse()
        client.list_connection_profiles(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_connection_profiles_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.ListConnectionProfilesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_connection_profiles), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            clouddms.ListConnectionProfilesResponse()
        )
        await client.list_connection_profiles(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_connection_profiles_flattened():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_connection_profiles), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = clouddms.ListConnectionProfilesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_connection_profiles(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_connection_profiles_flattened_error():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_connection_profiles(
            clouddms.ListConnectionProfilesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_connection_profiles_flattened_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_connection_profiles), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = clouddms.ListConnectionProfilesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            clouddms.ListConnectionProfilesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_connection_profiles(
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
async def test_list_connection_profiles_flattened_error_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_connection_profiles(
            clouddms.ListConnectionProfilesRequest(),
            parent="parent_value",
        )


def test_list_connection_profiles_pager(transport_name: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_connection_profiles), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            clouddms.ListConnectionProfilesResponse(
                connection_profiles=[
                    clouddms_resources.ConnectionProfile(),
                    clouddms_resources.ConnectionProfile(),
                    clouddms_resources.ConnectionProfile(),
                ],
                next_page_token="abc",
            ),
            clouddms.ListConnectionProfilesResponse(
                connection_profiles=[],
                next_page_token="def",
            ),
            clouddms.ListConnectionProfilesResponse(
                connection_profiles=[
                    clouddms_resources.ConnectionProfile(),
                ],
                next_page_token="ghi",
            ),
            clouddms.ListConnectionProfilesResponse(
                connection_profiles=[
                    clouddms_resources.ConnectionProfile(),
                    clouddms_resources.ConnectionProfile(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_connection_profiles(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, clouddms_resources.ConnectionProfile) for i in results)


def test_list_connection_profiles_pages(transport_name: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_connection_profiles), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            clouddms.ListConnectionProfilesResponse(
                connection_profiles=[
                    clouddms_resources.ConnectionProfile(),
                    clouddms_resources.ConnectionProfile(),
                    clouddms_resources.ConnectionProfile(),
                ],
                next_page_token="abc",
            ),
            clouddms.ListConnectionProfilesResponse(
                connection_profiles=[],
                next_page_token="def",
            ),
            clouddms.ListConnectionProfilesResponse(
                connection_profiles=[
                    clouddms_resources.ConnectionProfile(),
                ],
                next_page_token="ghi",
            ),
            clouddms.ListConnectionProfilesResponse(
                connection_profiles=[
                    clouddms_resources.ConnectionProfile(),
                    clouddms_resources.ConnectionProfile(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_connection_profiles(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_connection_profiles_async_pager():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_connection_profiles),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            clouddms.ListConnectionProfilesResponse(
                connection_profiles=[
                    clouddms_resources.ConnectionProfile(),
                    clouddms_resources.ConnectionProfile(),
                    clouddms_resources.ConnectionProfile(),
                ],
                next_page_token="abc",
            ),
            clouddms.ListConnectionProfilesResponse(
                connection_profiles=[],
                next_page_token="def",
            ),
            clouddms.ListConnectionProfilesResponse(
                connection_profiles=[
                    clouddms_resources.ConnectionProfile(),
                ],
                next_page_token="ghi",
            ),
            clouddms.ListConnectionProfilesResponse(
                connection_profiles=[
                    clouddms_resources.ConnectionProfile(),
                    clouddms_resources.ConnectionProfile(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_connection_profiles(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, clouddms_resources.ConnectionProfile) for i in responses
        )


@pytest.mark.asyncio
async def test_list_connection_profiles_async_pages():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_connection_profiles),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            clouddms.ListConnectionProfilesResponse(
                connection_profiles=[
                    clouddms_resources.ConnectionProfile(),
                    clouddms_resources.ConnectionProfile(),
                    clouddms_resources.ConnectionProfile(),
                ],
                next_page_token="abc",
            ),
            clouddms.ListConnectionProfilesResponse(
                connection_profiles=[],
                next_page_token="def",
            ),
            clouddms.ListConnectionProfilesResponse(
                connection_profiles=[
                    clouddms_resources.ConnectionProfile(),
                ],
                next_page_token="ghi",
            ),
            clouddms.ListConnectionProfilesResponse(
                connection_profiles=[
                    clouddms_resources.ConnectionProfile(),
                    clouddms_resources.ConnectionProfile(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_connection_profiles(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        clouddms.GetConnectionProfileRequest,
        dict,
    ],
)
def test_get_connection_profile(request_type, transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_connection_profile), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = clouddms_resources.ConnectionProfile(
            name="name_value",
            state=clouddms_resources.ConnectionProfile.State.DRAFT,
            display_name="display_name_value",
            provider=clouddms_resources.DatabaseProvider.CLOUDSQL,
        )
        response = client.get_connection_profile(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.GetConnectionProfileRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, clouddms_resources.ConnectionProfile)
    assert response.name == "name_value"
    assert response.state == clouddms_resources.ConnectionProfile.State.DRAFT
    assert response.display_name == "display_name_value"
    assert response.provider == clouddms_resources.DatabaseProvider.CLOUDSQL


def test_get_connection_profile_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_connection_profile), "__call__"
    ) as call:
        client.get_connection_profile()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.GetConnectionProfileRequest()


@pytest.mark.asyncio
async def test_get_connection_profile_async(
    transport: str = "grpc_asyncio", request_type=clouddms.GetConnectionProfileRequest
):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_connection_profile), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            clouddms_resources.ConnectionProfile(
                name="name_value",
                state=clouddms_resources.ConnectionProfile.State.DRAFT,
                display_name="display_name_value",
                provider=clouddms_resources.DatabaseProvider.CLOUDSQL,
            )
        )
        response = await client.get_connection_profile(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.GetConnectionProfileRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, clouddms_resources.ConnectionProfile)
    assert response.name == "name_value"
    assert response.state == clouddms_resources.ConnectionProfile.State.DRAFT
    assert response.display_name == "display_name_value"
    assert response.provider == clouddms_resources.DatabaseProvider.CLOUDSQL


@pytest.mark.asyncio
async def test_get_connection_profile_async_from_dict():
    await test_get_connection_profile_async(request_type=dict)


def test_get_connection_profile_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.GetConnectionProfileRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_connection_profile), "__call__"
    ) as call:
        call.return_value = clouddms_resources.ConnectionProfile()
        client.get_connection_profile(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_connection_profile_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.GetConnectionProfileRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_connection_profile), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            clouddms_resources.ConnectionProfile()
        )
        await client.get_connection_profile(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_connection_profile_flattened():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_connection_profile), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = clouddms_resources.ConnectionProfile()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_connection_profile(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_connection_profile_flattened_error():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_connection_profile(
            clouddms.GetConnectionProfileRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_connection_profile_flattened_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_connection_profile), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = clouddms_resources.ConnectionProfile()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            clouddms_resources.ConnectionProfile()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_connection_profile(
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
async def test_get_connection_profile_flattened_error_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_connection_profile(
            clouddms.GetConnectionProfileRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        clouddms.CreateConnectionProfileRequest,
        dict,
    ],
)
def test_create_connection_profile(request_type, transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_connection_profile), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_connection_profile(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.CreateConnectionProfileRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_connection_profile_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_connection_profile), "__call__"
    ) as call:
        client.create_connection_profile()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.CreateConnectionProfileRequest()


@pytest.mark.asyncio
async def test_create_connection_profile_async(
    transport: str = "grpc_asyncio",
    request_type=clouddms.CreateConnectionProfileRequest,
):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_connection_profile), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_connection_profile(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.CreateConnectionProfileRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_connection_profile_async_from_dict():
    await test_create_connection_profile_async(request_type=dict)


def test_create_connection_profile_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.CreateConnectionProfileRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_connection_profile), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_connection_profile(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_connection_profile_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.CreateConnectionProfileRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_connection_profile), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_connection_profile(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_connection_profile_flattened():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_connection_profile), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_connection_profile(
            parent="parent_value",
            connection_profile=clouddms_resources.ConnectionProfile(name="name_value"),
            connection_profile_id="connection_profile_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].connection_profile
        mock_val = clouddms_resources.ConnectionProfile(name="name_value")
        assert arg == mock_val
        arg = args[0].connection_profile_id
        mock_val = "connection_profile_id_value"
        assert arg == mock_val


def test_create_connection_profile_flattened_error():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_connection_profile(
            clouddms.CreateConnectionProfileRequest(),
            parent="parent_value",
            connection_profile=clouddms_resources.ConnectionProfile(name="name_value"),
            connection_profile_id="connection_profile_id_value",
        )


@pytest.mark.asyncio
async def test_create_connection_profile_flattened_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_connection_profile), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_connection_profile(
            parent="parent_value",
            connection_profile=clouddms_resources.ConnectionProfile(name="name_value"),
            connection_profile_id="connection_profile_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].connection_profile
        mock_val = clouddms_resources.ConnectionProfile(name="name_value")
        assert arg == mock_val
        arg = args[0].connection_profile_id
        mock_val = "connection_profile_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_connection_profile_flattened_error_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_connection_profile(
            clouddms.CreateConnectionProfileRequest(),
            parent="parent_value",
            connection_profile=clouddms_resources.ConnectionProfile(name="name_value"),
            connection_profile_id="connection_profile_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        clouddms.UpdateConnectionProfileRequest,
        dict,
    ],
)
def test_update_connection_profile(request_type, transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_connection_profile), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_connection_profile(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.UpdateConnectionProfileRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_connection_profile_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_connection_profile), "__call__"
    ) as call:
        client.update_connection_profile()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.UpdateConnectionProfileRequest()


@pytest.mark.asyncio
async def test_update_connection_profile_async(
    transport: str = "grpc_asyncio",
    request_type=clouddms.UpdateConnectionProfileRequest,
):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_connection_profile), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_connection_profile(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.UpdateConnectionProfileRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_connection_profile_async_from_dict():
    await test_update_connection_profile_async(request_type=dict)


def test_update_connection_profile_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.UpdateConnectionProfileRequest()

    request.connection_profile.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_connection_profile), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_connection_profile(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "connection_profile.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_connection_profile_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.UpdateConnectionProfileRequest()

    request.connection_profile.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_connection_profile), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_connection_profile(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "connection_profile.name=name_value",
    ) in kw["metadata"]


def test_update_connection_profile_flattened():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_connection_profile), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_connection_profile(
            connection_profile=clouddms_resources.ConnectionProfile(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].connection_profile
        mock_val = clouddms_resources.ConnectionProfile(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_connection_profile_flattened_error():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_connection_profile(
            clouddms.UpdateConnectionProfileRequest(),
            connection_profile=clouddms_resources.ConnectionProfile(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_connection_profile_flattened_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_connection_profile), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_connection_profile(
            connection_profile=clouddms_resources.ConnectionProfile(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].connection_profile
        mock_val = clouddms_resources.ConnectionProfile(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_connection_profile_flattened_error_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_connection_profile(
            clouddms.UpdateConnectionProfileRequest(),
            connection_profile=clouddms_resources.ConnectionProfile(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        clouddms.DeleteConnectionProfileRequest,
        dict,
    ],
)
def test_delete_connection_profile(request_type, transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_connection_profile), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_connection_profile(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.DeleteConnectionProfileRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_connection_profile_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_connection_profile), "__call__"
    ) as call:
        client.delete_connection_profile()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.DeleteConnectionProfileRequest()


@pytest.mark.asyncio
async def test_delete_connection_profile_async(
    transport: str = "grpc_asyncio",
    request_type=clouddms.DeleteConnectionProfileRequest,
):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_connection_profile), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_connection_profile(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.DeleteConnectionProfileRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_connection_profile_async_from_dict():
    await test_delete_connection_profile_async(request_type=dict)


def test_delete_connection_profile_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.DeleteConnectionProfileRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_connection_profile), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_connection_profile(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_connection_profile_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.DeleteConnectionProfileRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_connection_profile), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_connection_profile(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_delete_connection_profile_flattened():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_connection_profile), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_connection_profile(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_connection_profile_flattened_error():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_connection_profile(
            clouddms.DeleteConnectionProfileRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_connection_profile_flattened_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_connection_profile), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_connection_profile(
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
async def test_delete_connection_profile_flattened_error_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_connection_profile(
            clouddms.DeleteConnectionProfileRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        clouddms.CreatePrivateConnectionRequest,
        dict,
    ],
)
def test_create_private_connection(request_type, transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_private_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_private_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.CreatePrivateConnectionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_private_connection_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_private_connection), "__call__"
    ) as call:
        client.create_private_connection()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.CreatePrivateConnectionRequest()


@pytest.mark.asyncio
async def test_create_private_connection_async(
    transport: str = "grpc_asyncio",
    request_type=clouddms.CreatePrivateConnectionRequest,
):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_private_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_private_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.CreatePrivateConnectionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_private_connection_async_from_dict():
    await test_create_private_connection_async(request_type=dict)


def test_create_private_connection_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.CreatePrivateConnectionRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_private_connection), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_private_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_private_connection_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.CreatePrivateConnectionRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_private_connection), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_private_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_private_connection_flattened():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_private_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_private_connection(
            parent="parent_value",
            private_connection=clouddms_resources.PrivateConnection(name="name_value"),
            private_connection_id="private_connection_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].private_connection
        mock_val = clouddms_resources.PrivateConnection(name="name_value")
        assert arg == mock_val
        arg = args[0].private_connection_id
        mock_val = "private_connection_id_value"
        assert arg == mock_val


def test_create_private_connection_flattened_error():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_private_connection(
            clouddms.CreatePrivateConnectionRequest(),
            parent="parent_value",
            private_connection=clouddms_resources.PrivateConnection(name="name_value"),
            private_connection_id="private_connection_id_value",
        )


@pytest.mark.asyncio
async def test_create_private_connection_flattened_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_private_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_private_connection(
            parent="parent_value",
            private_connection=clouddms_resources.PrivateConnection(name="name_value"),
            private_connection_id="private_connection_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].private_connection
        mock_val = clouddms_resources.PrivateConnection(name="name_value")
        assert arg == mock_val
        arg = args[0].private_connection_id
        mock_val = "private_connection_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_private_connection_flattened_error_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_private_connection(
            clouddms.CreatePrivateConnectionRequest(),
            parent="parent_value",
            private_connection=clouddms_resources.PrivateConnection(name="name_value"),
            private_connection_id="private_connection_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        clouddms.GetPrivateConnectionRequest,
        dict,
    ],
)
def test_get_private_connection(request_type, transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_private_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = clouddms_resources.PrivateConnection(
            name="name_value",
            display_name="display_name_value",
            state=clouddms_resources.PrivateConnection.State.CREATING,
        )
        response = client.get_private_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.GetPrivateConnectionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, clouddms_resources.PrivateConnection)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.state == clouddms_resources.PrivateConnection.State.CREATING


def test_get_private_connection_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_private_connection), "__call__"
    ) as call:
        client.get_private_connection()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.GetPrivateConnectionRequest()


@pytest.mark.asyncio
async def test_get_private_connection_async(
    transport: str = "grpc_asyncio", request_type=clouddms.GetPrivateConnectionRequest
):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_private_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            clouddms_resources.PrivateConnection(
                name="name_value",
                display_name="display_name_value",
                state=clouddms_resources.PrivateConnection.State.CREATING,
            )
        )
        response = await client.get_private_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.GetPrivateConnectionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, clouddms_resources.PrivateConnection)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.state == clouddms_resources.PrivateConnection.State.CREATING


@pytest.mark.asyncio
async def test_get_private_connection_async_from_dict():
    await test_get_private_connection_async(request_type=dict)


def test_get_private_connection_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.GetPrivateConnectionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_private_connection), "__call__"
    ) as call:
        call.return_value = clouddms_resources.PrivateConnection()
        client.get_private_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_private_connection_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.GetPrivateConnectionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_private_connection), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            clouddms_resources.PrivateConnection()
        )
        await client.get_private_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_private_connection_flattened():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_private_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = clouddms_resources.PrivateConnection()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_private_connection(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_private_connection_flattened_error():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_private_connection(
            clouddms.GetPrivateConnectionRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_private_connection_flattened_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_private_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = clouddms_resources.PrivateConnection()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            clouddms_resources.PrivateConnection()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_private_connection(
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
async def test_get_private_connection_flattened_error_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_private_connection(
            clouddms.GetPrivateConnectionRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        clouddms.ListPrivateConnectionsRequest,
        dict,
    ],
)
def test_list_private_connections(request_type, transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_private_connections), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = clouddms.ListPrivateConnectionsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_private_connections(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.ListPrivateConnectionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPrivateConnectionsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_private_connections_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_private_connections), "__call__"
    ) as call:
        client.list_private_connections()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.ListPrivateConnectionsRequest()


@pytest.mark.asyncio
async def test_list_private_connections_async(
    transport: str = "grpc_asyncio", request_type=clouddms.ListPrivateConnectionsRequest
):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_private_connections), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            clouddms.ListPrivateConnectionsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_private_connections(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.ListPrivateConnectionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPrivateConnectionsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_private_connections_async_from_dict():
    await test_list_private_connections_async(request_type=dict)


def test_list_private_connections_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.ListPrivateConnectionsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_private_connections), "__call__"
    ) as call:
        call.return_value = clouddms.ListPrivateConnectionsResponse()
        client.list_private_connections(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_private_connections_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.ListPrivateConnectionsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_private_connections), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            clouddms.ListPrivateConnectionsResponse()
        )
        await client.list_private_connections(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_private_connections_flattened():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_private_connections), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = clouddms.ListPrivateConnectionsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_private_connections(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_private_connections_flattened_error():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_private_connections(
            clouddms.ListPrivateConnectionsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_private_connections_flattened_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_private_connections), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = clouddms.ListPrivateConnectionsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            clouddms.ListPrivateConnectionsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_private_connections(
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
async def test_list_private_connections_flattened_error_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_private_connections(
            clouddms.ListPrivateConnectionsRequest(),
            parent="parent_value",
        )


def test_list_private_connections_pager(transport_name: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_private_connections), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            clouddms.ListPrivateConnectionsResponse(
                private_connections=[
                    clouddms_resources.PrivateConnection(),
                    clouddms_resources.PrivateConnection(),
                    clouddms_resources.PrivateConnection(),
                ],
                next_page_token="abc",
            ),
            clouddms.ListPrivateConnectionsResponse(
                private_connections=[],
                next_page_token="def",
            ),
            clouddms.ListPrivateConnectionsResponse(
                private_connections=[
                    clouddms_resources.PrivateConnection(),
                ],
                next_page_token="ghi",
            ),
            clouddms.ListPrivateConnectionsResponse(
                private_connections=[
                    clouddms_resources.PrivateConnection(),
                    clouddms_resources.PrivateConnection(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_private_connections(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, clouddms_resources.PrivateConnection) for i in results)


def test_list_private_connections_pages(transport_name: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_private_connections), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            clouddms.ListPrivateConnectionsResponse(
                private_connections=[
                    clouddms_resources.PrivateConnection(),
                    clouddms_resources.PrivateConnection(),
                    clouddms_resources.PrivateConnection(),
                ],
                next_page_token="abc",
            ),
            clouddms.ListPrivateConnectionsResponse(
                private_connections=[],
                next_page_token="def",
            ),
            clouddms.ListPrivateConnectionsResponse(
                private_connections=[
                    clouddms_resources.PrivateConnection(),
                ],
                next_page_token="ghi",
            ),
            clouddms.ListPrivateConnectionsResponse(
                private_connections=[
                    clouddms_resources.PrivateConnection(),
                    clouddms_resources.PrivateConnection(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_private_connections(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_private_connections_async_pager():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_private_connections),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            clouddms.ListPrivateConnectionsResponse(
                private_connections=[
                    clouddms_resources.PrivateConnection(),
                    clouddms_resources.PrivateConnection(),
                    clouddms_resources.PrivateConnection(),
                ],
                next_page_token="abc",
            ),
            clouddms.ListPrivateConnectionsResponse(
                private_connections=[],
                next_page_token="def",
            ),
            clouddms.ListPrivateConnectionsResponse(
                private_connections=[
                    clouddms_resources.PrivateConnection(),
                ],
                next_page_token="ghi",
            ),
            clouddms.ListPrivateConnectionsResponse(
                private_connections=[
                    clouddms_resources.PrivateConnection(),
                    clouddms_resources.PrivateConnection(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_private_connections(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, clouddms_resources.PrivateConnection) for i in responses
        )


@pytest.mark.asyncio
async def test_list_private_connections_async_pages():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_private_connections),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            clouddms.ListPrivateConnectionsResponse(
                private_connections=[
                    clouddms_resources.PrivateConnection(),
                    clouddms_resources.PrivateConnection(),
                    clouddms_resources.PrivateConnection(),
                ],
                next_page_token="abc",
            ),
            clouddms.ListPrivateConnectionsResponse(
                private_connections=[],
                next_page_token="def",
            ),
            clouddms.ListPrivateConnectionsResponse(
                private_connections=[
                    clouddms_resources.PrivateConnection(),
                ],
                next_page_token="ghi",
            ),
            clouddms.ListPrivateConnectionsResponse(
                private_connections=[
                    clouddms_resources.PrivateConnection(),
                    clouddms_resources.PrivateConnection(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_private_connections(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        clouddms.DeletePrivateConnectionRequest,
        dict,
    ],
)
def test_delete_private_connection(request_type, transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_private_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_private_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.DeletePrivateConnectionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_private_connection_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_private_connection), "__call__"
    ) as call:
        client.delete_private_connection()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.DeletePrivateConnectionRequest()


@pytest.mark.asyncio
async def test_delete_private_connection_async(
    transport: str = "grpc_asyncio",
    request_type=clouddms.DeletePrivateConnectionRequest,
):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_private_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_private_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.DeletePrivateConnectionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_private_connection_async_from_dict():
    await test_delete_private_connection_async(request_type=dict)


def test_delete_private_connection_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.DeletePrivateConnectionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_private_connection), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_private_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_private_connection_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.DeletePrivateConnectionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_private_connection), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_private_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_delete_private_connection_flattened():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_private_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_private_connection(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_private_connection_flattened_error():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_private_connection(
            clouddms.DeletePrivateConnectionRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_private_connection_flattened_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_private_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_private_connection(
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
async def test_delete_private_connection_flattened_error_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_private_connection(
            clouddms.DeletePrivateConnectionRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        clouddms.GetConversionWorkspaceRequest,
        dict,
    ],
)
def test_get_conversion_workspace(request_type, transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_conversion_workspace), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = conversionworkspace_resources.ConversionWorkspace(
            name="name_value",
            has_uncommitted_changes=True,
            latest_commit_id="latest_commit_id_value",
            display_name="display_name_value",
        )
        response = client.get_conversion_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.GetConversionWorkspaceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, conversionworkspace_resources.ConversionWorkspace)
    assert response.name == "name_value"
    assert response.has_uncommitted_changes is True
    assert response.latest_commit_id == "latest_commit_id_value"
    assert response.display_name == "display_name_value"


def test_get_conversion_workspace_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_conversion_workspace), "__call__"
    ) as call:
        client.get_conversion_workspace()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.GetConversionWorkspaceRequest()


@pytest.mark.asyncio
async def test_get_conversion_workspace_async(
    transport: str = "grpc_asyncio", request_type=clouddms.GetConversionWorkspaceRequest
):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_conversion_workspace), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            conversionworkspace_resources.ConversionWorkspace(
                name="name_value",
                has_uncommitted_changes=True,
                latest_commit_id="latest_commit_id_value",
                display_name="display_name_value",
            )
        )
        response = await client.get_conversion_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.GetConversionWorkspaceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, conversionworkspace_resources.ConversionWorkspace)
    assert response.name == "name_value"
    assert response.has_uncommitted_changes is True
    assert response.latest_commit_id == "latest_commit_id_value"
    assert response.display_name == "display_name_value"


@pytest.mark.asyncio
async def test_get_conversion_workspace_async_from_dict():
    await test_get_conversion_workspace_async(request_type=dict)


def test_get_conversion_workspace_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.GetConversionWorkspaceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_conversion_workspace), "__call__"
    ) as call:
        call.return_value = conversionworkspace_resources.ConversionWorkspace()
        client.get_conversion_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_conversion_workspace_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.GetConversionWorkspaceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_conversion_workspace), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            conversionworkspace_resources.ConversionWorkspace()
        )
        await client.get_conversion_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_conversion_workspace_flattened():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_conversion_workspace), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = conversionworkspace_resources.ConversionWorkspace()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_conversion_workspace(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_conversion_workspace_flattened_error():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_conversion_workspace(
            clouddms.GetConversionWorkspaceRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_conversion_workspace_flattened_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_conversion_workspace), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = conversionworkspace_resources.ConversionWorkspace()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            conversionworkspace_resources.ConversionWorkspace()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_conversion_workspace(
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
async def test_get_conversion_workspace_flattened_error_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_conversion_workspace(
            clouddms.GetConversionWorkspaceRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        clouddms.ListConversionWorkspacesRequest,
        dict,
    ],
)
def test_list_conversion_workspaces(request_type, transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_workspaces), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = clouddms.ListConversionWorkspacesResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_conversion_workspaces(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.ListConversionWorkspacesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListConversionWorkspacesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_conversion_workspaces_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_workspaces), "__call__"
    ) as call:
        client.list_conversion_workspaces()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.ListConversionWorkspacesRequest()


@pytest.mark.asyncio
async def test_list_conversion_workspaces_async(
    transport: str = "grpc_asyncio",
    request_type=clouddms.ListConversionWorkspacesRequest,
):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_workspaces), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            clouddms.ListConversionWorkspacesResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_conversion_workspaces(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.ListConversionWorkspacesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListConversionWorkspacesAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_conversion_workspaces_async_from_dict():
    await test_list_conversion_workspaces_async(request_type=dict)


def test_list_conversion_workspaces_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.ListConversionWorkspacesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_workspaces), "__call__"
    ) as call:
        call.return_value = clouddms.ListConversionWorkspacesResponse()
        client.list_conversion_workspaces(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_conversion_workspaces_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.ListConversionWorkspacesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_workspaces), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            clouddms.ListConversionWorkspacesResponse()
        )
        await client.list_conversion_workspaces(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_conversion_workspaces_flattened():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_workspaces), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = clouddms.ListConversionWorkspacesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_conversion_workspaces(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_conversion_workspaces_flattened_error():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_conversion_workspaces(
            clouddms.ListConversionWorkspacesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_conversion_workspaces_flattened_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_workspaces), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = clouddms.ListConversionWorkspacesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            clouddms.ListConversionWorkspacesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_conversion_workspaces(
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
async def test_list_conversion_workspaces_flattened_error_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_conversion_workspaces(
            clouddms.ListConversionWorkspacesRequest(),
            parent="parent_value",
        )


def test_list_conversion_workspaces_pager(transport_name: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_workspaces), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            clouddms.ListConversionWorkspacesResponse(
                conversion_workspaces=[
                    conversionworkspace_resources.ConversionWorkspace(),
                    conversionworkspace_resources.ConversionWorkspace(),
                    conversionworkspace_resources.ConversionWorkspace(),
                ],
                next_page_token="abc",
            ),
            clouddms.ListConversionWorkspacesResponse(
                conversion_workspaces=[],
                next_page_token="def",
            ),
            clouddms.ListConversionWorkspacesResponse(
                conversion_workspaces=[
                    conversionworkspace_resources.ConversionWorkspace(),
                ],
                next_page_token="ghi",
            ),
            clouddms.ListConversionWorkspacesResponse(
                conversion_workspaces=[
                    conversionworkspace_resources.ConversionWorkspace(),
                    conversionworkspace_resources.ConversionWorkspace(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_conversion_workspaces(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, conversionworkspace_resources.ConversionWorkspace)
            for i in results
        )


def test_list_conversion_workspaces_pages(transport_name: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_workspaces), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            clouddms.ListConversionWorkspacesResponse(
                conversion_workspaces=[
                    conversionworkspace_resources.ConversionWorkspace(),
                    conversionworkspace_resources.ConversionWorkspace(),
                    conversionworkspace_resources.ConversionWorkspace(),
                ],
                next_page_token="abc",
            ),
            clouddms.ListConversionWorkspacesResponse(
                conversion_workspaces=[],
                next_page_token="def",
            ),
            clouddms.ListConversionWorkspacesResponse(
                conversion_workspaces=[
                    conversionworkspace_resources.ConversionWorkspace(),
                ],
                next_page_token="ghi",
            ),
            clouddms.ListConversionWorkspacesResponse(
                conversion_workspaces=[
                    conversionworkspace_resources.ConversionWorkspace(),
                    conversionworkspace_resources.ConversionWorkspace(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_conversion_workspaces(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_conversion_workspaces_async_pager():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_workspaces),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            clouddms.ListConversionWorkspacesResponse(
                conversion_workspaces=[
                    conversionworkspace_resources.ConversionWorkspace(),
                    conversionworkspace_resources.ConversionWorkspace(),
                    conversionworkspace_resources.ConversionWorkspace(),
                ],
                next_page_token="abc",
            ),
            clouddms.ListConversionWorkspacesResponse(
                conversion_workspaces=[],
                next_page_token="def",
            ),
            clouddms.ListConversionWorkspacesResponse(
                conversion_workspaces=[
                    conversionworkspace_resources.ConversionWorkspace(),
                ],
                next_page_token="ghi",
            ),
            clouddms.ListConversionWorkspacesResponse(
                conversion_workspaces=[
                    conversionworkspace_resources.ConversionWorkspace(),
                    conversionworkspace_resources.ConversionWorkspace(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_conversion_workspaces(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, conversionworkspace_resources.ConversionWorkspace)
            for i in responses
        )


@pytest.mark.asyncio
async def test_list_conversion_workspaces_async_pages():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_conversion_workspaces),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            clouddms.ListConversionWorkspacesResponse(
                conversion_workspaces=[
                    conversionworkspace_resources.ConversionWorkspace(),
                    conversionworkspace_resources.ConversionWorkspace(),
                    conversionworkspace_resources.ConversionWorkspace(),
                ],
                next_page_token="abc",
            ),
            clouddms.ListConversionWorkspacesResponse(
                conversion_workspaces=[],
                next_page_token="def",
            ),
            clouddms.ListConversionWorkspacesResponse(
                conversion_workspaces=[
                    conversionworkspace_resources.ConversionWorkspace(),
                ],
                next_page_token="ghi",
            ),
            clouddms.ListConversionWorkspacesResponse(
                conversion_workspaces=[
                    conversionworkspace_resources.ConversionWorkspace(),
                    conversionworkspace_resources.ConversionWorkspace(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_conversion_workspaces(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        clouddms.CreateConversionWorkspaceRequest,
        dict,
    ],
)
def test_create_conversion_workspace(request_type, transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversion_workspace), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_conversion_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.CreateConversionWorkspaceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_conversion_workspace_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversion_workspace), "__call__"
    ) as call:
        client.create_conversion_workspace()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.CreateConversionWorkspaceRequest()


@pytest.mark.asyncio
async def test_create_conversion_workspace_async(
    transport: str = "grpc_asyncio",
    request_type=clouddms.CreateConversionWorkspaceRequest,
):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversion_workspace), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_conversion_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.CreateConversionWorkspaceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_conversion_workspace_async_from_dict():
    await test_create_conversion_workspace_async(request_type=dict)


def test_create_conversion_workspace_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.CreateConversionWorkspaceRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversion_workspace), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_conversion_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_conversion_workspace_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.CreateConversionWorkspaceRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversion_workspace), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_conversion_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_conversion_workspace_flattened():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversion_workspace), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_conversion_workspace(
            parent="parent_value",
            conversion_workspace=conversionworkspace_resources.ConversionWorkspace(
                name="name_value"
            ),
            conversion_workspace_id="conversion_workspace_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].conversion_workspace
        mock_val = conversionworkspace_resources.ConversionWorkspace(name="name_value")
        assert arg == mock_val
        arg = args[0].conversion_workspace_id
        mock_val = "conversion_workspace_id_value"
        assert arg == mock_val


def test_create_conversion_workspace_flattened_error():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_conversion_workspace(
            clouddms.CreateConversionWorkspaceRequest(),
            parent="parent_value",
            conversion_workspace=conversionworkspace_resources.ConversionWorkspace(
                name="name_value"
            ),
            conversion_workspace_id="conversion_workspace_id_value",
        )


@pytest.mark.asyncio
async def test_create_conversion_workspace_flattened_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_conversion_workspace), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_conversion_workspace(
            parent="parent_value",
            conversion_workspace=conversionworkspace_resources.ConversionWorkspace(
                name="name_value"
            ),
            conversion_workspace_id="conversion_workspace_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].conversion_workspace
        mock_val = conversionworkspace_resources.ConversionWorkspace(name="name_value")
        assert arg == mock_val
        arg = args[0].conversion_workspace_id
        mock_val = "conversion_workspace_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_conversion_workspace_flattened_error_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_conversion_workspace(
            clouddms.CreateConversionWorkspaceRequest(),
            parent="parent_value",
            conversion_workspace=conversionworkspace_resources.ConversionWorkspace(
                name="name_value"
            ),
            conversion_workspace_id="conversion_workspace_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        clouddms.UpdateConversionWorkspaceRequest,
        dict,
    ],
)
def test_update_conversion_workspace(request_type, transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_conversion_workspace), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_conversion_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.UpdateConversionWorkspaceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_conversion_workspace_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_conversion_workspace), "__call__"
    ) as call:
        client.update_conversion_workspace()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.UpdateConversionWorkspaceRequest()


@pytest.mark.asyncio
async def test_update_conversion_workspace_async(
    transport: str = "grpc_asyncio",
    request_type=clouddms.UpdateConversionWorkspaceRequest,
):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_conversion_workspace), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_conversion_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.UpdateConversionWorkspaceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_conversion_workspace_async_from_dict():
    await test_update_conversion_workspace_async(request_type=dict)


def test_update_conversion_workspace_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.UpdateConversionWorkspaceRequest()

    request.conversion_workspace.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_conversion_workspace), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_conversion_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "conversion_workspace.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_conversion_workspace_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.UpdateConversionWorkspaceRequest()

    request.conversion_workspace.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_conversion_workspace), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_conversion_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "conversion_workspace.name=name_value",
    ) in kw["metadata"]


def test_update_conversion_workspace_flattened():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_conversion_workspace), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_conversion_workspace(
            conversion_workspace=conversionworkspace_resources.ConversionWorkspace(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].conversion_workspace
        mock_val = conversionworkspace_resources.ConversionWorkspace(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_conversion_workspace_flattened_error():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_conversion_workspace(
            clouddms.UpdateConversionWorkspaceRequest(),
            conversion_workspace=conversionworkspace_resources.ConversionWorkspace(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_conversion_workspace_flattened_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_conversion_workspace), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_conversion_workspace(
            conversion_workspace=conversionworkspace_resources.ConversionWorkspace(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].conversion_workspace
        mock_val = conversionworkspace_resources.ConversionWorkspace(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_conversion_workspace_flattened_error_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_conversion_workspace(
            clouddms.UpdateConversionWorkspaceRequest(),
            conversion_workspace=conversionworkspace_resources.ConversionWorkspace(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        clouddms.DeleteConversionWorkspaceRequest,
        dict,
    ],
)
def test_delete_conversion_workspace(request_type, transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_conversion_workspace), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_conversion_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.DeleteConversionWorkspaceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_conversion_workspace_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_conversion_workspace), "__call__"
    ) as call:
        client.delete_conversion_workspace()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.DeleteConversionWorkspaceRequest()


@pytest.mark.asyncio
async def test_delete_conversion_workspace_async(
    transport: str = "grpc_asyncio",
    request_type=clouddms.DeleteConversionWorkspaceRequest,
):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_conversion_workspace), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_conversion_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.DeleteConversionWorkspaceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_conversion_workspace_async_from_dict():
    await test_delete_conversion_workspace_async(request_type=dict)


def test_delete_conversion_workspace_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.DeleteConversionWorkspaceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_conversion_workspace), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_conversion_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_conversion_workspace_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.DeleteConversionWorkspaceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_conversion_workspace), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_conversion_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_delete_conversion_workspace_flattened():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_conversion_workspace), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_conversion_workspace(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_conversion_workspace_flattened_error():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_conversion_workspace(
            clouddms.DeleteConversionWorkspaceRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_conversion_workspace_flattened_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_conversion_workspace), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_conversion_workspace(
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
async def test_delete_conversion_workspace_flattened_error_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_conversion_workspace(
            clouddms.DeleteConversionWorkspaceRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        clouddms.SeedConversionWorkspaceRequest,
        dict,
    ],
)
def test_seed_conversion_workspace(request_type, transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.seed_conversion_workspace), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.seed_conversion_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.SeedConversionWorkspaceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_seed_conversion_workspace_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.seed_conversion_workspace), "__call__"
    ) as call:
        client.seed_conversion_workspace()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.SeedConversionWorkspaceRequest()


@pytest.mark.asyncio
async def test_seed_conversion_workspace_async(
    transport: str = "grpc_asyncio",
    request_type=clouddms.SeedConversionWorkspaceRequest,
):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.seed_conversion_workspace), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.seed_conversion_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.SeedConversionWorkspaceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_seed_conversion_workspace_async_from_dict():
    await test_seed_conversion_workspace_async(request_type=dict)


def test_seed_conversion_workspace_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.SeedConversionWorkspaceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.seed_conversion_workspace), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.seed_conversion_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_seed_conversion_workspace_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.SeedConversionWorkspaceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.seed_conversion_workspace), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.seed_conversion_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        clouddms.ImportMappingRulesRequest,
        dict,
    ],
)
def test_import_mapping_rules(request_type, transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_mapping_rules), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.import_mapping_rules(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.ImportMappingRulesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_import_mapping_rules_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_mapping_rules), "__call__"
    ) as call:
        client.import_mapping_rules()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.ImportMappingRulesRequest()


@pytest.mark.asyncio
async def test_import_mapping_rules_async(
    transport: str = "grpc_asyncio", request_type=clouddms.ImportMappingRulesRequest
):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_mapping_rules), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.import_mapping_rules(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.ImportMappingRulesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_import_mapping_rules_async_from_dict():
    await test_import_mapping_rules_async(request_type=dict)


def test_import_mapping_rules_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.ImportMappingRulesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_mapping_rules), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.import_mapping_rules(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_import_mapping_rules_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.ImportMappingRulesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_mapping_rules), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.import_mapping_rules(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        clouddms.ConvertConversionWorkspaceRequest,
        dict,
    ],
)
def test_convert_conversion_workspace(request_type, transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.convert_conversion_workspace), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.convert_conversion_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.ConvertConversionWorkspaceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_convert_conversion_workspace_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.convert_conversion_workspace), "__call__"
    ) as call:
        client.convert_conversion_workspace()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.ConvertConversionWorkspaceRequest()


@pytest.mark.asyncio
async def test_convert_conversion_workspace_async(
    transport: str = "grpc_asyncio",
    request_type=clouddms.ConvertConversionWorkspaceRequest,
):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.convert_conversion_workspace), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.convert_conversion_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.ConvertConversionWorkspaceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_convert_conversion_workspace_async_from_dict():
    await test_convert_conversion_workspace_async(request_type=dict)


def test_convert_conversion_workspace_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.ConvertConversionWorkspaceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.convert_conversion_workspace), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.convert_conversion_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_convert_conversion_workspace_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.ConvertConversionWorkspaceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.convert_conversion_workspace), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.convert_conversion_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        clouddms.CommitConversionWorkspaceRequest,
        dict,
    ],
)
def test_commit_conversion_workspace(request_type, transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.commit_conversion_workspace), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.commit_conversion_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.CommitConversionWorkspaceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_commit_conversion_workspace_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.commit_conversion_workspace), "__call__"
    ) as call:
        client.commit_conversion_workspace()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.CommitConversionWorkspaceRequest()


@pytest.mark.asyncio
async def test_commit_conversion_workspace_async(
    transport: str = "grpc_asyncio",
    request_type=clouddms.CommitConversionWorkspaceRequest,
):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.commit_conversion_workspace), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.commit_conversion_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.CommitConversionWorkspaceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_commit_conversion_workspace_async_from_dict():
    await test_commit_conversion_workspace_async(request_type=dict)


def test_commit_conversion_workspace_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.CommitConversionWorkspaceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.commit_conversion_workspace), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.commit_conversion_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_commit_conversion_workspace_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.CommitConversionWorkspaceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.commit_conversion_workspace), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.commit_conversion_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        clouddms.RollbackConversionWorkspaceRequest,
        dict,
    ],
)
def test_rollback_conversion_workspace(request_type, transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rollback_conversion_workspace), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.rollback_conversion_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.RollbackConversionWorkspaceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_rollback_conversion_workspace_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rollback_conversion_workspace), "__call__"
    ) as call:
        client.rollback_conversion_workspace()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.RollbackConversionWorkspaceRequest()


@pytest.mark.asyncio
async def test_rollback_conversion_workspace_async(
    transport: str = "grpc_asyncio",
    request_type=clouddms.RollbackConversionWorkspaceRequest,
):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rollback_conversion_workspace), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.rollback_conversion_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.RollbackConversionWorkspaceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_rollback_conversion_workspace_async_from_dict():
    await test_rollback_conversion_workspace_async(request_type=dict)


def test_rollback_conversion_workspace_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.RollbackConversionWorkspaceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rollback_conversion_workspace), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.rollback_conversion_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_rollback_conversion_workspace_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.RollbackConversionWorkspaceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rollback_conversion_workspace), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.rollback_conversion_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        clouddms.ApplyConversionWorkspaceRequest,
        dict,
    ],
)
def test_apply_conversion_workspace(request_type, transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.apply_conversion_workspace), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.apply_conversion_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.ApplyConversionWorkspaceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_apply_conversion_workspace_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.apply_conversion_workspace), "__call__"
    ) as call:
        client.apply_conversion_workspace()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.ApplyConversionWorkspaceRequest()


@pytest.mark.asyncio
async def test_apply_conversion_workspace_async(
    transport: str = "grpc_asyncio",
    request_type=clouddms.ApplyConversionWorkspaceRequest,
):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.apply_conversion_workspace), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.apply_conversion_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.ApplyConversionWorkspaceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_apply_conversion_workspace_async_from_dict():
    await test_apply_conversion_workspace_async(request_type=dict)


def test_apply_conversion_workspace_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.ApplyConversionWorkspaceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.apply_conversion_workspace), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.apply_conversion_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_apply_conversion_workspace_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.ApplyConversionWorkspaceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.apply_conversion_workspace), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.apply_conversion_workspace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        clouddms.DescribeDatabaseEntitiesRequest,
        dict,
    ],
)
def test_describe_database_entities(request_type, transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.describe_database_entities), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = clouddms.DescribeDatabaseEntitiesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.describe_database_entities(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.DescribeDatabaseEntitiesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.DescribeDatabaseEntitiesPager)
    assert response.next_page_token == "next_page_token_value"


def test_describe_database_entities_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.describe_database_entities), "__call__"
    ) as call:
        client.describe_database_entities()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.DescribeDatabaseEntitiesRequest()


@pytest.mark.asyncio
async def test_describe_database_entities_async(
    transport: str = "grpc_asyncio",
    request_type=clouddms.DescribeDatabaseEntitiesRequest,
):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.describe_database_entities), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            clouddms.DescribeDatabaseEntitiesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.describe_database_entities(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.DescribeDatabaseEntitiesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.DescribeDatabaseEntitiesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_describe_database_entities_async_from_dict():
    await test_describe_database_entities_async(request_type=dict)


def test_describe_database_entities_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.DescribeDatabaseEntitiesRequest()

    request.conversion_workspace = "conversion_workspace_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.describe_database_entities), "__call__"
    ) as call:
        call.return_value = clouddms.DescribeDatabaseEntitiesResponse()
        client.describe_database_entities(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "conversion_workspace=conversion_workspace_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_describe_database_entities_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.DescribeDatabaseEntitiesRequest()

    request.conversion_workspace = "conversion_workspace_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.describe_database_entities), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            clouddms.DescribeDatabaseEntitiesResponse()
        )
        await client.describe_database_entities(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "conversion_workspace=conversion_workspace_value",
    ) in kw["metadata"]


def test_describe_database_entities_pager(transport_name: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.describe_database_entities), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            clouddms.DescribeDatabaseEntitiesResponse(
                database_entities=[
                    conversionworkspace_resources.DatabaseEntity(),
                    conversionworkspace_resources.DatabaseEntity(),
                    conversionworkspace_resources.DatabaseEntity(),
                ],
                next_page_token="abc",
            ),
            clouddms.DescribeDatabaseEntitiesResponse(
                database_entities=[],
                next_page_token="def",
            ),
            clouddms.DescribeDatabaseEntitiesResponse(
                database_entities=[
                    conversionworkspace_resources.DatabaseEntity(),
                ],
                next_page_token="ghi",
            ),
            clouddms.DescribeDatabaseEntitiesResponse(
                database_entities=[
                    conversionworkspace_resources.DatabaseEntity(),
                    conversionworkspace_resources.DatabaseEntity(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("conversion_workspace", ""),)),
        )
        pager = client.describe_database_entities(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, conversionworkspace_resources.DatabaseEntity) for i in results
        )


def test_describe_database_entities_pages(transport_name: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.describe_database_entities), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            clouddms.DescribeDatabaseEntitiesResponse(
                database_entities=[
                    conversionworkspace_resources.DatabaseEntity(),
                    conversionworkspace_resources.DatabaseEntity(),
                    conversionworkspace_resources.DatabaseEntity(),
                ],
                next_page_token="abc",
            ),
            clouddms.DescribeDatabaseEntitiesResponse(
                database_entities=[],
                next_page_token="def",
            ),
            clouddms.DescribeDatabaseEntitiesResponse(
                database_entities=[
                    conversionworkspace_resources.DatabaseEntity(),
                ],
                next_page_token="ghi",
            ),
            clouddms.DescribeDatabaseEntitiesResponse(
                database_entities=[
                    conversionworkspace_resources.DatabaseEntity(),
                    conversionworkspace_resources.DatabaseEntity(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.describe_database_entities(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_describe_database_entities_async_pager():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.describe_database_entities),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            clouddms.DescribeDatabaseEntitiesResponse(
                database_entities=[
                    conversionworkspace_resources.DatabaseEntity(),
                    conversionworkspace_resources.DatabaseEntity(),
                    conversionworkspace_resources.DatabaseEntity(),
                ],
                next_page_token="abc",
            ),
            clouddms.DescribeDatabaseEntitiesResponse(
                database_entities=[],
                next_page_token="def",
            ),
            clouddms.DescribeDatabaseEntitiesResponse(
                database_entities=[
                    conversionworkspace_resources.DatabaseEntity(),
                ],
                next_page_token="ghi",
            ),
            clouddms.DescribeDatabaseEntitiesResponse(
                database_entities=[
                    conversionworkspace_resources.DatabaseEntity(),
                    conversionworkspace_resources.DatabaseEntity(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.describe_database_entities(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, conversionworkspace_resources.DatabaseEntity)
            for i in responses
        )


@pytest.mark.asyncio
async def test_describe_database_entities_async_pages():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.describe_database_entities),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            clouddms.DescribeDatabaseEntitiesResponse(
                database_entities=[
                    conversionworkspace_resources.DatabaseEntity(),
                    conversionworkspace_resources.DatabaseEntity(),
                    conversionworkspace_resources.DatabaseEntity(),
                ],
                next_page_token="abc",
            ),
            clouddms.DescribeDatabaseEntitiesResponse(
                database_entities=[],
                next_page_token="def",
            ),
            clouddms.DescribeDatabaseEntitiesResponse(
                database_entities=[
                    conversionworkspace_resources.DatabaseEntity(),
                ],
                next_page_token="ghi",
            ),
            clouddms.DescribeDatabaseEntitiesResponse(
                database_entities=[
                    conversionworkspace_resources.DatabaseEntity(),
                    conversionworkspace_resources.DatabaseEntity(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.describe_database_entities(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        clouddms.SearchBackgroundJobsRequest,
        dict,
    ],
)
def test_search_background_jobs(request_type, transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_background_jobs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = clouddms.SearchBackgroundJobsResponse()
        response = client.search_background_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.SearchBackgroundJobsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, clouddms.SearchBackgroundJobsResponse)


def test_search_background_jobs_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_background_jobs), "__call__"
    ) as call:
        client.search_background_jobs()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.SearchBackgroundJobsRequest()


@pytest.mark.asyncio
async def test_search_background_jobs_async(
    transport: str = "grpc_asyncio", request_type=clouddms.SearchBackgroundJobsRequest
):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_background_jobs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            clouddms.SearchBackgroundJobsResponse()
        )
        response = await client.search_background_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.SearchBackgroundJobsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, clouddms.SearchBackgroundJobsResponse)


@pytest.mark.asyncio
async def test_search_background_jobs_async_from_dict():
    await test_search_background_jobs_async(request_type=dict)


def test_search_background_jobs_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.SearchBackgroundJobsRequest()

    request.conversion_workspace = "conversion_workspace_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_background_jobs), "__call__"
    ) as call:
        call.return_value = clouddms.SearchBackgroundJobsResponse()
        client.search_background_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "conversion_workspace=conversion_workspace_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_search_background_jobs_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.SearchBackgroundJobsRequest()

    request.conversion_workspace = "conversion_workspace_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_background_jobs), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            clouddms.SearchBackgroundJobsResponse()
        )
        await client.search_background_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "conversion_workspace=conversion_workspace_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        clouddms.DescribeConversionWorkspaceRevisionsRequest,
        dict,
    ],
)
def test_describe_conversion_workspace_revisions(request_type, transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.describe_conversion_workspace_revisions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = clouddms.DescribeConversionWorkspaceRevisionsResponse()
        response = client.describe_conversion_workspace_revisions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.DescribeConversionWorkspaceRevisionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, clouddms.DescribeConversionWorkspaceRevisionsResponse)


def test_describe_conversion_workspace_revisions_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.describe_conversion_workspace_revisions), "__call__"
    ) as call:
        client.describe_conversion_workspace_revisions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.DescribeConversionWorkspaceRevisionsRequest()


@pytest.mark.asyncio
async def test_describe_conversion_workspace_revisions_async(
    transport: str = "grpc_asyncio",
    request_type=clouddms.DescribeConversionWorkspaceRevisionsRequest,
):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.describe_conversion_workspace_revisions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            clouddms.DescribeConversionWorkspaceRevisionsResponse()
        )
        response = await client.describe_conversion_workspace_revisions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.DescribeConversionWorkspaceRevisionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, clouddms.DescribeConversionWorkspaceRevisionsResponse)


@pytest.mark.asyncio
async def test_describe_conversion_workspace_revisions_async_from_dict():
    await test_describe_conversion_workspace_revisions_async(request_type=dict)


def test_describe_conversion_workspace_revisions_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.DescribeConversionWorkspaceRevisionsRequest()

    request.conversion_workspace = "conversion_workspace_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.describe_conversion_workspace_revisions), "__call__"
    ) as call:
        call.return_value = clouddms.DescribeConversionWorkspaceRevisionsResponse()
        client.describe_conversion_workspace_revisions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "conversion_workspace=conversion_workspace_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_describe_conversion_workspace_revisions_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.DescribeConversionWorkspaceRevisionsRequest()

    request.conversion_workspace = "conversion_workspace_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.describe_conversion_workspace_revisions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            clouddms.DescribeConversionWorkspaceRevisionsResponse()
        )
        await client.describe_conversion_workspace_revisions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "conversion_workspace=conversion_workspace_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        clouddms.FetchStaticIpsRequest,
        dict,
    ],
)
def test_fetch_static_ips(request_type, transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_static_ips), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = clouddms.FetchStaticIpsResponse(
            static_ips=["static_ips_value"],
            next_page_token="next_page_token_value",
        )
        response = client.fetch_static_ips(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.FetchStaticIpsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.FetchStaticIpsPager)
    assert response.static_ips == ["static_ips_value"]
    assert response.next_page_token == "next_page_token_value"


def test_fetch_static_ips_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_static_ips), "__call__") as call:
        client.fetch_static_ips()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.FetchStaticIpsRequest()


@pytest.mark.asyncio
async def test_fetch_static_ips_async(
    transport: str = "grpc_asyncio", request_type=clouddms.FetchStaticIpsRequest
):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_static_ips), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            clouddms.FetchStaticIpsResponse(
                static_ips=["static_ips_value"],
                next_page_token="next_page_token_value",
            )
        )
        response = await client.fetch_static_ips(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == clouddms.FetchStaticIpsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.FetchStaticIpsAsyncPager)
    assert response.static_ips == ["static_ips_value"]
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_fetch_static_ips_async_from_dict():
    await test_fetch_static_ips_async(request_type=dict)


def test_fetch_static_ips_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.FetchStaticIpsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_static_ips), "__call__") as call:
        call.return_value = clouddms.FetchStaticIpsResponse()
        client.fetch_static_ips(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_fetch_static_ips_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = clouddms.FetchStaticIpsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_static_ips), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            clouddms.FetchStaticIpsResponse()
        )
        await client.fetch_static_ips(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_fetch_static_ips_flattened():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_static_ips), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = clouddms.FetchStaticIpsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.fetch_static_ips(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_fetch_static_ips_flattened_error():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.fetch_static_ips(
            clouddms.FetchStaticIpsRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_fetch_static_ips_flattened_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_static_ips), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = clouddms.FetchStaticIpsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            clouddms.FetchStaticIpsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.fetch_static_ips(
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
async def test_fetch_static_ips_flattened_error_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.fetch_static_ips(
            clouddms.FetchStaticIpsRequest(),
            name="name_value",
        )


def test_fetch_static_ips_pager(transport_name: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_static_ips), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            clouddms.FetchStaticIpsResponse(
                static_ips=[
                    str(),
                    str(),
                    str(),
                ],
                next_page_token="abc",
            ),
            clouddms.FetchStaticIpsResponse(
                static_ips=[],
                next_page_token="def",
            ),
            clouddms.FetchStaticIpsResponse(
                static_ips=[
                    str(),
                ],
                next_page_token="ghi",
            ),
            clouddms.FetchStaticIpsResponse(
                static_ips=[
                    str(),
                    str(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", ""),)),
        )
        pager = client.fetch_static_ips(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, str) for i in results)


def test_fetch_static_ips_pages(transport_name: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_static_ips), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            clouddms.FetchStaticIpsResponse(
                static_ips=[
                    str(),
                    str(),
                    str(),
                ],
                next_page_token="abc",
            ),
            clouddms.FetchStaticIpsResponse(
                static_ips=[],
                next_page_token="def",
            ),
            clouddms.FetchStaticIpsResponse(
                static_ips=[
                    str(),
                ],
                next_page_token="ghi",
            ),
            clouddms.FetchStaticIpsResponse(
                static_ips=[
                    str(),
                    str(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.fetch_static_ips(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_fetch_static_ips_async_pager():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.fetch_static_ips), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            clouddms.FetchStaticIpsResponse(
                static_ips=[
                    str(),
                    str(),
                    str(),
                ],
                next_page_token="abc",
            ),
            clouddms.FetchStaticIpsResponse(
                static_ips=[],
                next_page_token="def",
            ),
            clouddms.FetchStaticIpsResponse(
                static_ips=[
                    str(),
                ],
                next_page_token="ghi",
            ),
            clouddms.FetchStaticIpsResponse(
                static_ips=[
                    str(),
                    str(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.fetch_static_ips(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, str) for i in responses)


@pytest.mark.asyncio
async def test_fetch_static_ips_async_pages():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.fetch_static_ips), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            clouddms.FetchStaticIpsResponse(
                static_ips=[
                    str(),
                    str(),
                    str(),
                ],
                next_page_token="abc",
            ),
            clouddms.FetchStaticIpsResponse(
                static_ips=[],
                next_page_token="def",
            ),
            clouddms.FetchStaticIpsResponse(
                static_ips=[
                    str(),
                ],
                next_page_token="ghi",
            ),
            clouddms.FetchStaticIpsResponse(
                static_ips=[
                    str(),
                    str(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.fetch_static_ips(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.DataMigrationServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DataMigrationServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.DataMigrationServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DataMigrationServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.DataMigrationServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = DataMigrationServiceClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = DataMigrationServiceClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.DataMigrationServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DataMigrationServiceClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.DataMigrationServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = DataMigrationServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.DataMigrationServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.DataMigrationServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.DataMigrationServiceGrpcTransport,
        transports.DataMigrationServiceGrpcAsyncIOTransport,
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
    transport = DataMigrationServiceClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.DataMigrationServiceGrpcTransport,
    )


def test_data_migration_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.DataMigrationServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_data_migration_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.clouddms_v1.services.data_migration_service.transports.DataMigrationServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.DataMigrationServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_migration_jobs",
        "get_migration_job",
        "create_migration_job",
        "update_migration_job",
        "delete_migration_job",
        "start_migration_job",
        "stop_migration_job",
        "resume_migration_job",
        "promote_migration_job",
        "verify_migration_job",
        "restart_migration_job",
        "generate_ssh_script",
        "list_connection_profiles",
        "get_connection_profile",
        "create_connection_profile",
        "update_connection_profile",
        "delete_connection_profile",
        "create_private_connection",
        "get_private_connection",
        "list_private_connections",
        "delete_private_connection",
        "get_conversion_workspace",
        "list_conversion_workspaces",
        "create_conversion_workspace",
        "update_conversion_workspace",
        "delete_conversion_workspace",
        "seed_conversion_workspace",
        "import_mapping_rules",
        "convert_conversion_workspace",
        "commit_conversion_workspace",
        "rollback_conversion_workspace",
        "apply_conversion_workspace",
        "describe_database_entities",
        "search_background_jobs",
        "describe_conversion_workspace_revisions",
        "fetch_static_ips",
        "set_iam_policy",
        "get_iam_policy",
        "test_iam_permissions",
        "get_location",
        "list_locations",
        "get_operation",
        "cancel_operation",
        "delete_operation",
        "list_operations",
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


def test_data_migration_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.clouddms_v1.services.data_migration_service.transports.DataMigrationServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.DataMigrationServiceTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_data_migration_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.clouddms_v1.services.data_migration_service.transports.DataMigrationServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.DataMigrationServiceTransport()
        adc.assert_called_once()


def test_data_migration_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        DataMigrationServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.DataMigrationServiceGrpcTransport,
        transports.DataMigrationServiceGrpcAsyncIOTransport,
    ],
)
def test_data_migration_service_transport_auth_adc(transport_class):
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
    "transport_class",
    [
        transports.DataMigrationServiceGrpcTransport,
        transports.DataMigrationServiceGrpcAsyncIOTransport,
    ],
)
def test_data_migration_service_transport_auth_gdch_credentials(transport_class):
    host = "https://language.com"
    api_audience_tests = [None, "https://language2.com"]
    api_audience_expect = [host, "https://language2.com"]
    for t, e in zip(api_audience_tests, api_audience_expect):
        with mock.patch.object(google.auth, "default", autospec=True) as adc:
            gdch_mock = mock.MagicMock()
            type(gdch_mock).with_gdch_audience = mock.PropertyMock(
                return_value=gdch_mock
            )
            adc.return_value = (gdch_mock, None)
            transport_class(host=host, api_audience=t)
            gdch_mock.with_gdch_audience.assert_called_once_with(e)


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.DataMigrationServiceGrpcTransport, grpc_helpers),
        (transports.DataMigrationServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_data_migration_service_transport_create_channel(transport_class, grpc_helpers):
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
            "datamigration.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="datamigration.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.DataMigrationServiceGrpcTransport,
        transports.DataMigrationServiceGrpcAsyncIOTransport,
    ],
)
def test_data_migration_service_grpc_transport_client_cert_source_for_mtls(
    transport_class,
):
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
def test_data_migration_service_host_no_port(transport_name):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="datamigration.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("datamigration.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
    ],
)
def test_data_migration_service_host_with_port(transport_name):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="datamigration.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("datamigration.googleapis.com:8000")


def test_data_migration_service_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.DataMigrationServiceGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_data_migration_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.DataMigrationServiceGrpcAsyncIOTransport(
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
    [
        transports.DataMigrationServiceGrpcTransport,
        transports.DataMigrationServiceGrpcAsyncIOTransport,
    ],
)
def test_data_migration_service_transport_channel_mtls_with_client_cert_source(
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
        transports.DataMigrationServiceGrpcTransport,
        transports.DataMigrationServiceGrpcAsyncIOTransport,
    ],
)
def test_data_migration_service_transport_channel_mtls_with_adc(transport_class):
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


def test_data_migration_service_grpc_lro_client():
    client = DataMigrationServiceClient(
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


def test_data_migration_service_grpc_lro_async_client():
    client = DataMigrationServiceAsyncClient(
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


def test_connection_profile_path():
    project = "squid"
    location = "clam"
    connection_profile = "whelk"
    expected = "projects/{project}/locations/{location}/connectionProfiles/{connection_profile}".format(
        project=project,
        location=location,
        connection_profile=connection_profile,
    )
    actual = DataMigrationServiceClient.connection_profile_path(
        project, location, connection_profile
    )
    assert expected == actual


def test_parse_connection_profile_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "connection_profile": "nudibranch",
    }
    path = DataMigrationServiceClient.connection_profile_path(**expected)

    # Check that the path construction is reversible.
    actual = DataMigrationServiceClient.parse_connection_profile_path(path)
    assert expected == actual


def test_conversion_workspace_path():
    project = "cuttlefish"
    location = "mussel"
    conversion_workspace = "winkle"
    expected = "projects/{project}/locations/{location}/conversionWorkspaces/{conversion_workspace}".format(
        project=project,
        location=location,
        conversion_workspace=conversion_workspace,
    )
    actual = DataMigrationServiceClient.conversion_workspace_path(
        project, location, conversion_workspace
    )
    assert expected == actual


def test_parse_conversion_workspace_path():
    expected = {
        "project": "nautilus",
        "location": "scallop",
        "conversion_workspace": "abalone",
    }
    path = DataMigrationServiceClient.conversion_workspace_path(**expected)

    # Check that the path construction is reversible.
    actual = DataMigrationServiceClient.parse_conversion_workspace_path(path)
    assert expected == actual


def test_migration_job_path():
    project = "squid"
    location = "clam"
    migration_job = "whelk"
    expected = (
        "projects/{project}/locations/{location}/migrationJobs/{migration_job}".format(
            project=project,
            location=location,
            migration_job=migration_job,
        )
    )
    actual = DataMigrationServiceClient.migration_job_path(
        project, location, migration_job
    )
    assert expected == actual


def test_parse_migration_job_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "migration_job": "nudibranch",
    }
    path = DataMigrationServiceClient.migration_job_path(**expected)

    # Check that the path construction is reversible.
    actual = DataMigrationServiceClient.parse_migration_job_path(path)
    assert expected == actual


def test_networks_path():
    project = "cuttlefish"
    network = "mussel"
    expected = "projects/{project}/global/networks/{network}".format(
        project=project,
        network=network,
    )
    actual = DataMigrationServiceClient.networks_path(project, network)
    assert expected == actual


def test_parse_networks_path():
    expected = {
        "project": "winkle",
        "network": "nautilus",
    }
    path = DataMigrationServiceClient.networks_path(**expected)

    # Check that the path construction is reversible.
    actual = DataMigrationServiceClient.parse_networks_path(path)
    assert expected == actual


def test_private_connection_path():
    project = "scallop"
    location = "abalone"
    private_connection = "squid"
    expected = "projects/{project}/locations/{location}/privateConnections/{private_connection}".format(
        project=project,
        location=location,
        private_connection=private_connection,
    )
    actual = DataMigrationServiceClient.private_connection_path(
        project, location, private_connection
    )
    assert expected == actual


def test_parse_private_connection_path():
    expected = {
        "project": "clam",
        "location": "whelk",
        "private_connection": "octopus",
    }
    path = DataMigrationServiceClient.private_connection_path(**expected)

    # Check that the path construction is reversible.
    actual = DataMigrationServiceClient.parse_private_connection_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "oyster"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = DataMigrationServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "nudibranch",
    }
    path = DataMigrationServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = DataMigrationServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "cuttlefish"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = DataMigrationServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "mussel",
    }
    path = DataMigrationServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = DataMigrationServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "winkle"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = DataMigrationServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nautilus",
    }
    path = DataMigrationServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = DataMigrationServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "scallop"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = DataMigrationServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "abalone",
    }
    path = DataMigrationServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = DataMigrationServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "squid"
    location = "clam"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = DataMigrationServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "whelk",
        "location": "octopus",
    }
    path = DataMigrationServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = DataMigrationServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.DataMigrationServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = DataMigrationServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.DataMigrationServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = DataMigrationServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(
        type(getattr(client.transport, "grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_delete_operation(transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.DeleteOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_operation_async(transport: str = "grpc"):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.DeleteOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_operation_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.DeleteOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        call.return_value = None

        client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_operation_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.DeleteOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_delete_operation_from_dict():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_delete_operation_from_dict_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_cancel_operation(transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.CancelOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_cancel_operation_async(transport: str = "grpc"):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.CancelOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_cancel_operation_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.CancelOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        call.return_value = None

        client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_cancel_operation_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.CancelOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_cancel_operation_from_dict():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.cancel_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_cancel_operation_from_dict_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.cancel_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_get_operation(transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.GetOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation()
        response = client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


@pytest.mark.asyncio
async def test_get_operation_async(transport: str = "grpc"):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.GetOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        response = await client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


def test_get_operation_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.GetOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        call.return_value = operations_pb2.Operation()

        client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_operation_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.GetOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        await client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_get_operation_from_dict():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation()

        response = client.get_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_get_operation_from_dict_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        response = await client.get_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_list_operations(transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.ListOperationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.ListOperationsResponse()
        response = client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


@pytest.mark.asyncio
async def test_list_operations_async(transport: str = "grpc"):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.ListOperationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        response = await client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


def test_list_operations_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.ListOperationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        call.return_value = operations_pb2.ListOperationsResponse()

        client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_operations_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.ListOperationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        await client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_list_operations_from_dict():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.ListOperationsResponse()

        response = client.list_operations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_list_operations_from_dict_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        response = await client.list_operations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_list_locations(transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = locations_pb2.ListLocationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = locations_pb2.ListLocationsResponse()
        response = client.list_locations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.ListLocationsResponse)


@pytest.mark.asyncio
async def test_list_locations_async(transport: str = "grpc"):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = locations_pb2.ListLocationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.ListLocationsResponse()
        )
        response = await client.list_locations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.ListLocationsResponse)


def test_list_locations_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = locations_pb2.ListLocationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        call.return_value = locations_pb2.ListLocationsResponse()

        client.list_locations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_locations_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = locations_pb2.ListLocationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.ListLocationsResponse()
        )
        await client.list_locations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_list_locations_from_dict():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = locations_pb2.ListLocationsResponse()

        response = client.list_locations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_list_locations_from_dict_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.ListLocationsResponse()
        )
        response = await client.list_locations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_get_location(transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = locations_pb2.GetLocationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_location), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = locations_pb2.Location()
        response = client.get_location(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.Location)


@pytest.mark.asyncio
async def test_get_location_async(transport: str = "grpc_asyncio"):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = locations_pb2.GetLocationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_location), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.Location()
        )
        response = await client.get_location(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.Location)


def test_get_location_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials()
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = locations_pb2.GetLocationRequest()
    request.name = "locations/abc"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_location), "__call__") as call:
        call.return_value = locations_pb2.Location()

        client.get_location(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations/abc",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_location_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials()
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = locations_pb2.GetLocationRequest()
    request.name = "locations/abc"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_location), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.Location()
        )
        await client.get_location(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations/abc",
    ) in kw["metadata"]


def test_get_location_from_dict():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = locations_pb2.Location()

        response = client.get_location(
            request={
                "name": "locations/abc",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_get_location_from_dict_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.Location()
        )
        response = await client.get_location(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_set_iam_policy(transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.SetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy(
            version=774,
            etag=b"etag_blob",
        )
        response = client.set_iam_policy(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


@pytest.mark.asyncio
async def test_set_iam_policy_async(transport: str = "grpc_asyncio"):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.SetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policy_pb2.Policy(
                version=774,
                etag=b"etag_blob",
            )
        )
        response = await client.set_iam_policy(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


def test_set_iam_policy_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.SetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        call.return_value = policy_pb2.Policy()

        client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_set_iam_policy_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.SetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy_pb2.Policy())

        await client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource/value",
    ) in kw["metadata"]


def test_set_iam_policy_from_dict():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy()

        response = client.set_iam_policy(
            request={
                "resource": "resource_value",
                "policy": policy_pb2.Policy(version=774),
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_set_iam_policy_from_dict_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy_pb2.Policy())

        response = await client.set_iam_policy(
            request={
                "resource": "resource_value",
                "policy": policy_pb2.Policy(version=774),
            }
        )
        call.assert_called()


def test_get_iam_policy(transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.GetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy(
            version=774,
            etag=b"etag_blob",
        )

        response = client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


@pytest.mark.asyncio
async def test_get_iam_policy_async(transport: str = "grpc_asyncio"):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.GetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policy_pb2.Policy(
                version=774,
                etag=b"etag_blob",
            )
        )

        response = await client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


def test_get_iam_policy_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.GetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        call.return_value = policy_pb2.Policy()

        client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_iam_policy_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.GetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy_pb2.Policy())

        await client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource/value",
    ) in kw["metadata"]


def test_get_iam_policy_from_dict():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy()

        response = client.get_iam_policy(
            request={
                "resource": "resource_value",
                "options": options_pb2.GetPolicyOptions(requested_policy_version=2598),
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_get_iam_policy_from_dict_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy_pb2.Policy())

        response = await client.get_iam_policy(
            request={
                "resource": "resource_value",
                "options": options_pb2.GetPolicyOptions(requested_policy_version=2598),
            }
        )
        call.assert_called()


def test_test_iam_permissions(transport: str = "grpc"):
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.TestIamPermissionsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy_pb2.TestIamPermissionsResponse(
            permissions=["permissions_value"],
        )

        response = client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy_pb2.TestIamPermissionsResponse)

    assert response.permissions == ["permissions_value"]


@pytest.mark.asyncio
async def test_test_iam_permissions_async(transport: str = "grpc_asyncio"):
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.TestIamPermissionsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            iam_policy_pb2.TestIamPermissionsResponse(
                permissions=["permissions_value"],
            )
        )

        response = await client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy_pb2.TestIamPermissionsResponse)

    assert response.permissions == ["permissions_value"]


def test_test_iam_permissions_field_headers():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.TestIamPermissionsRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        call.return_value = iam_policy_pb2.TestIamPermissionsResponse()

        client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_test_iam_permissions_field_headers_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.TestIamPermissionsRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            iam_policy_pb2.TestIamPermissionsResponse()
        )

        await client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource/value",
    ) in kw["metadata"]


def test_test_iam_permissions_from_dict():
    client = DataMigrationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy_pb2.TestIamPermissionsResponse()

        response = client.test_iam_permissions(
            request={
                "resource": "resource_value",
                "permissions": ["permissions_value"],
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_test_iam_permissions_from_dict_async():
    client = DataMigrationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            iam_policy_pb2.TestIamPermissionsResponse()
        )

        response = await client.test_iam_permissions(
            request={
                "resource": "resource_value",
                "permissions": ["permissions_value"],
            }
        )
        call.assert_called()


def test_transport_close():
    transports = {
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = DataMigrationServiceClient(
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
        client = DataMigrationServiceClient(
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
        (DataMigrationServiceClient, transports.DataMigrationServiceGrpcTransport),
        (
            DataMigrationServiceAsyncClient,
            transports.DataMigrationServiceGrpcAsyncIOTransport,
        ),
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
                api_audience=None,
            )
