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
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest

from google.cloud.dataplex_v1.services.dataplex_service import (
    DataplexServiceAsyncClient,
    DataplexServiceClient,
    pagers,
    transports,
)
from google.cloud.dataplex_v1.types import analyze, resources, service, tasks


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

    assert DataplexServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        DataplexServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        DataplexServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        DataplexServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        DataplexServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        DataplexServiceClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (DataplexServiceClient, "grpc"),
        (DataplexServiceAsyncClient, "grpc_asyncio"),
    ],
)
def test_dataplex_service_client_from_service_account_info(
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

        assert client.transport._host == ("dataplex.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.DataplexServiceGrpcTransport, "grpc"),
        (transports.DataplexServiceGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_dataplex_service_client_service_account_always_use_jwt(
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
        (DataplexServiceClient, "grpc"),
        (DataplexServiceAsyncClient, "grpc_asyncio"),
    ],
)
def test_dataplex_service_client_from_service_account_file(
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

        assert client.transport._host == ("dataplex.googleapis.com:443")


def test_dataplex_service_client_get_transport_class():
    transport = DataplexServiceClient.get_transport_class()
    available_transports = [
        transports.DataplexServiceGrpcTransport,
    ]
    assert transport in available_transports

    transport = DataplexServiceClient.get_transport_class("grpc")
    assert transport == transports.DataplexServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (DataplexServiceClient, transports.DataplexServiceGrpcTransport, "grpc"),
        (
            DataplexServiceAsyncClient,
            transports.DataplexServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    DataplexServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DataplexServiceClient),
)
@mock.patch.object(
    DataplexServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DataplexServiceAsyncClient),
)
def test_dataplex_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(DataplexServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(DataplexServiceClient, "get_transport_class") as gtc:
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
            DataplexServiceClient,
            transports.DataplexServiceGrpcTransport,
            "grpc",
            "true",
        ),
        (
            DataplexServiceAsyncClient,
            transports.DataplexServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            DataplexServiceClient,
            transports.DataplexServiceGrpcTransport,
            "grpc",
            "false",
        ),
        (
            DataplexServiceAsyncClient,
            transports.DataplexServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    DataplexServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DataplexServiceClient),
)
@mock.patch.object(
    DataplexServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DataplexServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_dataplex_service_client_mtls_env_auto(
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
    "client_class", [DataplexServiceClient, DataplexServiceAsyncClient]
)
@mock.patch.object(
    DataplexServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DataplexServiceClient),
)
@mock.patch.object(
    DataplexServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(DataplexServiceAsyncClient),
)
def test_dataplex_service_client_get_mtls_endpoint_and_cert_source(client_class):
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
        (DataplexServiceClient, transports.DataplexServiceGrpcTransport, "grpc"),
        (
            DataplexServiceAsyncClient,
            transports.DataplexServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_dataplex_service_client_client_options_scopes(
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
            DataplexServiceClient,
            transports.DataplexServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            DataplexServiceAsyncClient,
            transports.DataplexServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_dataplex_service_client_client_options_credentials_file(
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


def test_dataplex_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.dataplex_v1.services.dataplex_service.transports.DataplexServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = DataplexServiceClient(
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
            DataplexServiceClient,
            transports.DataplexServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            DataplexServiceAsyncClient,
            transports.DataplexServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_dataplex_service_client_create_channel_credentials_file(
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
            "dataplex.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="dataplex.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.CreateLakeRequest,
        dict,
    ],
)
def test_create_lake(request_type, transport: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_lake), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_lake(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateLakeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_lake_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_lake), "__call__") as call:
        client.create_lake()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateLakeRequest()


@pytest.mark.asyncio
async def test_create_lake_async(
    transport: str = "grpc_asyncio", request_type=service.CreateLakeRequest
):
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_lake), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_lake(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateLakeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_lake_async_from_dict():
    await test_create_lake_async(request_type=dict)


def test_create_lake_field_headers():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateLakeRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_lake), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_lake(request)

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
async def test_create_lake_field_headers_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateLakeRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_lake), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_lake(request)

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


def test_create_lake_flattened():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_lake), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_lake(
            parent="parent_value",
            lake=resources.Lake(name="name_value"),
            lake_id="lake_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].lake
        mock_val = resources.Lake(name="name_value")
        assert arg == mock_val
        arg = args[0].lake_id
        mock_val = "lake_id_value"
        assert arg == mock_val


def test_create_lake_flattened_error():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_lake(
            service.CreateLakeRequest(),
            parent="parent_value",
            lake=resources.Lake(name="name_value"),
            lake_id="lake_id_value",
        )


@pytest.mark.asyncio
async def test_create_lake_flattened_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_lake), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_lake(
            parent="parent_value",
            lake=resources.Lake(name="name_value"),
            lake_id="lake_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].lake
        mock_val = resources.Lake(name="name_value")
        assert arg == mock_val
        arg = args[0].lake_id
        mock_val = "lake_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_lake_flattened_error_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_lake(
            service.CreateLakeRequest(),
            parent="parent_value",
            lake=resources.Lake(name="name_value"),
            lake_id="lake_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.UpdateLakeRequest,
        dict,
    ],
)
def test_update_lake(request_type, transport: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_lake), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_lake(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateLakeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_lake_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_lake), "__call__") as call:
        client.update_lake()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateLakeRequest()


@pytest.mark.asyncio
async def test_update_lake_async(
    transport: str = "grpc_asyncio", request_type=service.UpdateLakeRequest
):
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_lake), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_lake(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateLakeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_lake_async_from_dict():
    await test_update_lake_async(request_type=dict)


def test_update_lake_field_headers():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateLakeRequest()

    request.lake.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_lake), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_lake(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "lake.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_lake_field_headers_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateLakeRequest()

    request.lake.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_lake), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_lake(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "lake.name=name_value",
    ) in kw["metadata"]


def test_update_lake_flattened():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_lake), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_lake(
            lake=resources.Lake(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].lake
        mock_val = resources.Lake(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_lake_flattened_error():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_lake(
            service.UpdateLakeRequest(),
            lake=resources.Lake(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_lake_flattened_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_lake), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_lake(
            lake=resources.Lake(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].lake
        mock_val = resources.Lake(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_lake_flattened_error_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_lake(
            service.UpdateLakeRequest(),
            lake=resources.Lake(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.DeleteLakeRequest,
        dict,
    ],
)
def test_delete_lake(request_type, transport: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_lake), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_lake(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteLakeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_lake_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_lake), "__call__") as call:
        client.delete_lake()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteLakeRequest()


@pytest.mark.asyncio
async def test_delete_lake_async(
    transport: str = "grpc_asyncio", request_type=service.DeleteLakeRequest
):
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_lake), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_lake(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteLakeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_lake_async_from_dict():
    await test_delete_lake_async(request_type=dict)


def test_delete_lake_field_headers():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.DeleteLakeRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_lake), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_lake(request)

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
async def test_delete_lake_field_headers_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.DeleteLakeRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_lake), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_lake(request)

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


def test_delete_lake_flattened():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_lake), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_lake(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_lake_flattened_error():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_lake(
            service.DeleteLakeRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_lake_flattened_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_lake), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_lake(
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
async def test_delete_lake_flattened_error_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_lake(
            service.DeleteLakeRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.ListLakesRequest,
        dict,
    ],
)
def test_list_lakes(request_type, transport: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_lakes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListLakesResponse(
            next_page_token="next_page_token_value",
            unreachable_locations=["unreachable_locations_value"],
        )
        response = client.list_lakes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListLakesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListLakesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable_locations == ["unreachable_locations_value"]


def test_list_lakes_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_lakes), "__call__") as call:
        client.list_lakes()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListLakesRequest()


@pytest.mark.asyncio
async def test_list_lakes_async(
    transport: str = "grpc_asyncio", request_type=service.ListLakesRequest
):
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_lakes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListLakesResponse(
                next_page_token="next_page_token_value",
                unreachable_locations=["unreachable_locations_value"],
            )
        )
        response = await client.list_lakes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListLakesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListLakesAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable_locations == ["unreachable_locations_value"]


@pytest.mark.asyncio
async def test_list_lakes_async_from_dict():
    await test_list_lakes_async(request_type=dict)


def test_list_lakes_field_headers():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListLakesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_lakes), "__call__") as call:
        call.return_value = service.ListLakesResponse()
        client.list_lakes(request)

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
async def test_list_lakes_field_headers_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListLakesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_lakes), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListLakesResponse()
        )
        await client.list_lakes(request)

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


def test_list_lakes_flattened():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_lakes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListLakesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_lakes(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_lakes_flattened_error():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_lakes(
            service.ListLakesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_lakes_flattened_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_lakes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListLakesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListLakesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_lakes(
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
async def test_list_lakes_flattened_error_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_lakes(
            service.ListLakesRequest(),
            parent="parent_value",
        )


def test_list_lakes_pager(transport_name: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_lakes), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListLakesResponse(
                lakes=[
                    resources.Lake(),
                    resources.Lake(),
                    resources.Lake(),
                ],
                next_page_token="abc",
            ),
            service.ListLakesResponse(
                lakes=[],
                next_page_token="def",
            ),
            service.ListLakesResponse(
                lakes=[
                    resources.Lake(),
                ],
                next_page_token="ghi",
            ),
            service.ListLakesResponse(
                lakes=[
                    resources.Lake(),
                    resources.Lake(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_lakes(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.Lake) for i in results)


def test_list_lakes_pages(transport_name: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_lakes), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListLakesResponse(
                lakes=[
                    resources.Lake(),
                    resources.Lake(),
                    resources.Lake(),
                ],
                next_page_token="abc",
            ),
            service.ListLakesResponse(
                lakes=[],
                next_page_token="def",
            ),
            service.ListLakesResponse(
                lakes=[
                    resources.Lake(),
                ],
                next_page_token="ghi",
            ),
            service.ListLakesResponse(
                lakes=[
                    resources.Lake(),
                    resources.Lake(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_lakes(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_lakes_async_pager():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_lakes), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListLakesResponse(
                lakes=[
                    resources.Lake(),
                    resources.Lake(),
                    resources.Lake(),
                ],
                next_page_token="abc",
            ),
            service.ListLakesResponse(
                lakes=[],
                next_page_token="def",
            ),
            service.ListLakesResponse(
                lakes=[
                    resources.Lake(),
                ],
                next_page_token="ghi",
            ),
            service.ListLakesResponse(
                lakes=[
                    resources.Lake(),
                    resources.Lake(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_lakes(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.Lake) for i in responses)


@pytest.mark.asyncio
async def test_list_lakes_async_pages():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_lakes), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListLakesResponse(
                lakes=[
                    resources.Lake(),
                    resources.Lake(),
                    resources.Lake(),
                ],
                next_page_token="abc",
            ),
            service.ListLakesResponse(
                lakes=[],
                next_page_token="def",
            ),
            service.ListLakesResponse(
                lakes=[
                    resources.Lake(),
                ],
                next_page_token="ghi",
            ),
            service.ListLakesResponse(
                lakes=[
                    resources.Lake(),
                    resources.Lake(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_lakes(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        service.GetLakeRequest,
        dict,
    ],
)
def test_get_lake(request_type, transport: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_lake), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Lake(
            name="name_value",
            display_name="display_name_value",
            uid="uid_value",
            description="description_value",
            state=resources.State.ACTIVE,
            service_account="service_account_value",
        )
        response = client.get_lake(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetLakeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Lake)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.uid == "uid_value"
    assert response.description == "description_value"
    assert response.state == resources.State.ACTIVE
    assert response.service_account == "service_account_value"


def test_get_lake_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_lake), "__call__") as call:
        client.get_lake()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetLakeRequest()


@pytest.mark.asyncio
async def test_get_lake_async(
    transport: str = "grpc_asyncio", request_type=service.GetLakeRequest
):
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_lake), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Lake(
                name="name_value",
                display_name="display_name_value",
                uid="uid_value",
                description="description_value",
                state=resources.State.ACTIVE,
                service_account="service_account_value",
            )
        )
        response = await client.get_lake(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetLakeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Lake)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.uid == "uid_value"
    assert response.description == "description_value"
    assert response.state == resources.State.ACTIVE
    assert response.service_account == "service_account_value"


@pytest.mark.asyncio
async def test_get_lake_async_from_dict():
    await test_get_lake_async(request_type=dict)


def test_get_lake_field_headers():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetLakeRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_lake), "__call__") as call:
        call.return_value = resources.Lake()
        client.get_lake(request)

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
async def test_get_lake_field_headers_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetLakeRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_lake), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Lake())
        await client.get_lake(request)

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


def test_get_lake_flattened():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_lake), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Lake()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_lake(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_lake_flattened_error():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_lake(
            service.GetLakeRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_lake_flattened_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_lake), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Lake()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Lake())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_lake(
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
async def test_get_lake_flattened_error_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_lake(
            service.GetLakeRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.ListLakeActionsRequest,
        dict,
    ],
)
def test_list_lake_actions(request_type, transport: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_lake_actions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListActionsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_lake_actions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListLakeActionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListLakeActionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_lake_actions_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_lake_actions), "__call__"
    ) as call:
        client.list_lake_actions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListLakeActionsRequest()


@pytest.mark.asyncio
async def test_list_lake_actions_async(
    transport: str = "grpc_asyncio", request_type=service.ListLakeActionsRequest
):
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_lake_actions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListActionsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_lake_actions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListLakeActionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListLakeActionsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_lake_actions_async_from_dict():
    await test_list_lake_actions_async(request_type=dict)


def test_list_lake_actions_field_headers():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListLakeActionsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_lake_actions), "__call__"
    ) as call:
        call.return_value = service.ListActionsResponse()
        client.list_lake_actions(request)

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
async def test_list_lake_actions_field_headers_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListLakeActionsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_lake_actions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListActionsResponse()
        )
        await client.list_lake_actions(request)

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


def test_list_lake_actions_flattened():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_lake_actions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListActionsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_lake_actions(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_lake_actions_flattened_error():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_lake_actions(
            service.ListLakeActionsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_lake_actions_flattened_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_lake_actions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListActionsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListActionsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_lake_actions(
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
async def test_list_lake_actions_flattened_error_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_lake_actions(
            service.ListLakeActionsRequest(),
            parent="parent_value",
        )


def test_list_lake_actions_pager(transport_name: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_lake_actions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListActionsResponse(
                actions=[
                    resources.Action(),
                    resources.Action(),
                    resources.Action(),
                ],
                next_page_token="abc",
            ),
            service.ListActionsResponse(
                actions=[],
                next_page_token="def",
            ),
            service.ListActionsResponse(
                actions=[
                    resources.Action(),
                ],
                next_page_token="ghi",
            ),
            service.ListActionsResponse(
                actions=[
                    resources.Action(),
                    resources.Action(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_lake_actions(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.Action) for i in results)


def test_list_lake_actions_pages(transport_name: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_lake_actions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListActionsResponse(
                actions=[
                    resources.Action(),
                    resources.Action(),
                    resources.Action(),
                ],
                next_page_token="abc",
            ),
            service.ListActionsResponse(
                actions=[],
                next_page_token="def",
            ),
            service.ListActionsResponse(
                actions=[
                    resources.Action(),
                ],
                next_page_token="ghi",
            ),
            service.ListActionsResponse(
                actions=[
                    resources.Action(),
                    resources.Action(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_lake_actions(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_lake_actions_async_pager():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_lake_actions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListActionsResponse(
                actions=[
                    resources.Action(),
                    resources.Action(),
                    resources.Action(),
                ],
                next_page_token="abc",
            ),
            service.ListActionsResponse(
                actions=[],
                next_page_token="def",
            ),
            service.ListActionsResponse(
                actions=[
                    resources.Action(),
                ],
                next_page_token="ghi",
            ),
            service.ListActionsResponse(
                actions=[
                    resources.Action(),
                    resources.Action(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_lake_actions(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.Action) for i in responses)


@pytest.mark.asyncio
async def test_list_lake_actions_async_pages():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_lake_actions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListActionsResponse(
                actions=[
                    resources.Action(),
                    resources.Action(),
                    resources.Action(),
                ],
                next_page_token="abc",
            ),
            service.ListActionsResponse(
                actions=[],
                next_page_token="def",
            ),
            service.ListActionsResponse(
                actions=[
                    resources.Action(),
                ],
                next_page_token="ghi",
            ),
            service.ListActionsResponse(
                actions=[
                    resources.Action(),
                    resources.Action(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_lake_actions(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        service.CreateZoneRequest,
        dict,
    ],
)
def test_create_zone(request_type, transport: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_zone), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_zone(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateZoneRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_zone_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_zone), "__call__") as call:
        client.create_zone()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateZoneRequest()


@pytest.mark.asyncio
async def test_create_zone_async(
    transport: str = "grpc_asyncio", request_type=service.CreateZoneRequest
):
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_zone), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_zone(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateZoneRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_zone_async_from_dict():
    await test_create_zone_async(request_type=dict)


def test_create_zone_field_headers():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateZoneRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_zone), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_zone(request)

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
async def test_create_zone_field_headers_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateZoneRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_zone), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_zone(request)

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


def test_create_zone_flattened():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_zone), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_zone(
            parent="parent_value",
            zone=resources.Zone(name="name_value"),
            zone_id="zone_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = resources.Zone(name="name_value")
        assert arg == mock_val
        arg = args[0].zone_id
        mock_val = "zone_id_value"
        assert arg == mock_val


def test_create_zone_flattened_error():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_zone(
            service.CreateZoneRequest(),
            parent="parent_value",
            zone=resources.Zone(name="name_value"),
            zone_id="zone_id_value",
        )


@pytest.mark.asyncio
async def test_create_zone_flattened_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_zone), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_zone(
            parent="parent_value",
            zone=resources.Zone(name="name_value"),
            zone_id="zone_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].zone
        mock_val = resources.Zone(name="name_value")
        assert arg == mock_val
        arg = args[0].zone_id
        mock_val = "zone_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_zone_flattened_error_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_zone(
            service.CreateZoneRequest(),
            parent="parent_value",
            zone=resources.Zone(name="name_value"),
            zone_id="zone_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.UpdateZoneRequest,
        dict,
    ],
)
def test_update_zone(request_type, transport: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_zone), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_zone(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateZoneRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_zone_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_zone), "__call__") as call:
        client.update_zone()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateZoneRequest()


@pytest.mark.asyncio
async def test_update_zone_async(
    transport: str = "grpc_asyncio", request_type=service.UpdateZoneRequest
):
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_zone), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_zone(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateZoneRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_zone_async_from_dict():
    await test_update_zone_async(request_type=dict)


def test_update_zone_field_headers():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateZoneRequest()

    request.zone.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_zone), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_zone(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "zone.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_zone_field_headers_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateZoneRequest()

    request.zone.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_zone), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_zone(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "zone.name=name_value",
    ) in kw["metadata"]


def test_update_zone_flattened():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_zone), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_zone(
            zone=resources.Zone(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].zone
        mock_val = resources.Zone(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_zone_flattened_error():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_zone(
            service.UpdateZoneRequest(),
            zone=resources.Zone(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_zone_flattened_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_zone), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_zone(
            zone=resources.Zone(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].zone
        mock_val = resources.Zone(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_zone_flattened_error_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_zone(
            service.UpdateZoneRequest(),
            zone=resources.Zone(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.DeleteZoneRequest,
        dict,
    ],
)
def test_delete_zone(request_type, transport: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_zone), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_zone(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteZoneRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_zone_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_zone), "__call__") as call:
        client.delete_zone()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteZoneRequest()


@pytest.mark.asyncio
async def test_delete_zone_async(
    transport: str = "grpc_asyncio", request_type=service.DeleteZoneRequest
):
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_zone), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_zone(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteZoneRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_zone_async_from_dict():
    await test_delete_zone_async(request_type=dict)


def test_delete_zone_field_headers():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.DeleteZoneRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_zone), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_zone(request)

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
async def test_delete_zone_field_headers_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.DeleteZoneRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_zone), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_zone(request)

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


def test_delete_zone_flattened():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_zone), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_zone(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_zone_flattened_error():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_zone(
            service.DeleteZoneRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_zone_flattened_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_zone), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_zone(
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
async def test_delete_zone_flattened_error_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_zone(
            service.DeleteZoneRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.ListZonesRequest,
        dict,
    ],
)
def test_list_zones(request_type, transport: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_zones), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListZonesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_zones(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListZonesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListZonesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_zones_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_zones), "__call__") as call:
        client.list_zones()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListZonesRequest()


@pytest.mark.asyncio
async def test_list_zones_async(
    transport: str = "grpc_asyncio", request_type=service.ListZonesRequest
):
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_zones), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListZonesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_zones(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListZonesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListZonesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_zones_async_from_dict():
    await test_list_zones_async(request_type=dict)


def test_list_zones_field_headers():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListZonesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_zones), "__call__") as call:
        call.return_value = service.ListZonesResponse()
        client.list_zones(request)

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
async def test_list_zones_field_headers_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListZonesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_zones), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListZonesResponse()
        )
        await client.list_zones(request)

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


def test_list_zones_flattened():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_zones), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListZonesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_zones(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_zones_flattened_error():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_zones(
            service.ListZonesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_zones_flattened_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_zones), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListZonesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListZonesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_zones(
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
async def test_list_zones_flattened_error_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_zones(
            service.ListZonesRequest(),
            parent="parent_value",
        )


def test_list_zones_pager(transport_name: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_zones), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListZonesResponse(
                zones=[
                    resources.Zone(),
                    resources.Zone(),
                    resources.Zone(),
                ],
                next_page_token="abc",
            ),
            service.ListZonesResponse(
                zones=[],
                next_page_token="def",
            ),
            service.ListZonesResponse(
                zones=[
                    resources.Zone(),
                ],
                next_page_token="ghi",
            ),
            service.ListZonesResponse(
                zones=[
                    resources.Zone(),
                    resources.Zone(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_zones(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.Zone) for i in results)


def test_list_zones_pages(transport_name: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_zones), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListZonesResponse(
                zones=[
                    resources.Zone(),
                    resources.Zone(),
                    resources.Zone(),
                ],
                next_page_token="abc",
            ),
            service.ListZonesResponse(
                zones=[],
                next_page_token="def",
            ),
            service.ListZonesResponse(
                zones=[
                    resources.Zone(),
                ],
                next_page_token="ghi",
            ),
            service.ListZonesResponse(
                zones=[
                    resources.Zone(),
                    resources.Zone(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_zones(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_zones_async_pager():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_zones), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListZonesResponse(
                zones=[
                    resources.Zone(),
                    resources.Zone(),
                    resources.Zone(),
                ],
                next_page_token="abc",
            ),
            service.ListZonesResponse(
                zones=[],
                next_page_token="def",
            ),
            service.ListZonesResponse(
                zones=[
                    resources.Zone(),
                ],
                next_page_token="ghi",
            ),
            service.ListZonesResponse(
                zones=[
                    resources.Zone(),
                    resources.Zone(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_zones(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.Zone) for i in responses)


@pytest.mark.asyncio
async def test_list_zones_async_pages():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_zones), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListZonesResponse(
                zones=[
                    resources.Zone(),
                    resources.Zone(),
                    resources.Zone(),
                ],
                next_page_token="abc",
            ),
            service.ListZonesResponse(
                zones=[],
                next_page_token="def",
            ),
            service.ListZonesResponse(
                zones=[
                    resources.Zone(),
                ],
                next_page_token="ghi",
            ),
            service.ListZonesResponse(
                zones=[
                    resources.Zone(),
                    resources.Zone(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_zones(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        service.GetZoneRequest,
        dict,
    ],
)
def test_get_zone(request_type, transport: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_zone), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Zone(
            name="name_value",
            display_name="display_name_value",
            uid="uid_value",
            description="description_value",
            state=resources.State.ACTIVE,
            type_=resources.Zone.Type.RAW,
        )
        response = client.get_zone(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetZoneRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Zone)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.uid == "uid_value"
    assert response.description == "description_value"
    assert response.state == resources.State.ACTIVE
    assert response.type_ == resources.Zone.Type.RAW


def test_get_zone_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_zone), "__call__") as call:
        client.get_zone()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetZoneRequest()


@pytest.mark.asyncio
async def test_get_zone_async(
    transport: str = "grpc_asyncio", request_type=service.GetZoneRequest
):
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_zone), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Zone(
                name="name_value",
                display_name="display_name_value",
                uid="uid_value",
                description="description_value",
                state=resources.State.ACTIVE,
                type_=resources.Zone.Type.RAW,
            )
        )
        response = await client.get_zone(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetZoneRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Zone)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.uid == "uid_value"
    assert response.description == "description_value"
    assert response.state == resources.State.ACTIVE
    assert response.type_ == resources.Zone.Type.RAW


@pytest.mark.asyncio
async def test_get_zone_async_from_dict():
    await test_get_zone_async(request_type=dict)


def test_get_zone_field_headers():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetZoneRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_zone), "__call__") as call:
        call.return_value = resources.Zone()
        client.get_zone(request)

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
async def test_get_zone_field_headers_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetZoneRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_zone), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Zone())
        await client.get_zone(request)

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


def test_get_zone_flattened():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_zone), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Zone()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_zone(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_zone_flattened_error():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_zone(
            service.GetZoneRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_zone_flattened_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_zone), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Zone()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Zone())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_zone(
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
async def test_get_zone_flattened_error_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_zone(
            service.GetZoneRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.ListZoneActionsRequest,
        dict,
    ],
)
def test_list_zone_actions(request_type, transport: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_zone_actions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListActionsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_zone_actions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListZoneActionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListZoneActionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_zone_actions_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_zone_actions), "__call__"
    ) as call:
        client.list_zone_actions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListZoneActionsRequest()


@pytest.mark.asyncio
async def test_list_zone_actions_async(
    transport: str = "grpc_asyncio", request_type=service.ListZoneActionsRequest
):
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_zone_actions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListActionsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_zone_actions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListZoneActionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListZoneActionsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_zone_actions_async_from_dict():
    await test_list_zone_actions_async(request_type=dict)


def test_list_zone_actions_field_headers():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListZoneActionsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_zone_actions), "__call__"
    ) as call:
        call.return_value = service.ListActionsResponse()
        client.list_zone_actions(request)

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
async def test_list_zone_actions_field_headers_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListZoneActionsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_zone_actions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListActionsResponse()
        )
        await client.list_zone_actions(request)

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


def test_list_zone_actions_flattened():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_zone_actions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListActionsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_zone_actions(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_zone_actions_flattened_error():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_zone_actions(
            service.ListZoneActionsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_zone_actions_flattened_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_zone_actions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListActionsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListActionsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_zone_actions(
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
async def test_list_zone_actions_flattened_error_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_zone_actions(
            service.ListZoneActionsRequest(),
            parent="parent_value",
        )


def test_list_zone_actions_pager(transport_name: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_zone_actions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListActionsResponse(
                actions=[
                    resources.Action(),
                    resources.Action(),
                    resources.Action(),
                ],
                next_page_token="abc",
            ),
            service.ListActionsResponse(
                actions=[],
                next_page_token="def",
            ),
            service.ListActionsResponse(
                actions=[
                    resources.Action(),
                ],
                next_page_token="ghi",
            ),
            service.ListActionsResponse(
                actions=[
                    resources.Action(),
                    resources.Action(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_zone_actions(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.Action) for i in results)


def test_list_zone_actions_pages(transport_name: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_zone_actions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListActionsResponse(
                actions=[
                    resources.Action(),
                    resources.Action(),
                    resources.Action(),
                ],
                next_page_token="abc",
            ),
            service.ListActionsResponse(
                actions=[],
                next_page_token="def",
            ),
            service.ListActionsResponse(
                actions=[
                    resources.Action(),
                ],
                next_page_token="ghi",
            ),
            service.ListActionsResponse(
                actions=[
                    resources.Action(),
                    resources.Action(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_zone_actions(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_zone_actions_async_pager():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_zone_actions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListActionsResponse(
                actions=[
                    resources.Action(),
                    resources.Action(),
                    resources.Action(),
                ],
                next_page_token="abc",
            ),
            service.ListActionsResponse(
                actions=[],
                next_page_token="def",
            ),
            service.ListActionsResponse(
                actions=[
                    resources.Action(),
                ],
                next_page_token="ghi",
            ),
            service.ListActionsResponse(
                actions=[
                    resources.Action(),
                    resources.Action(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_zone_actions(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.Action) for i in responses)


@pytest.mark.asyncio
async def test_list_zone_actions_async_pages():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_zone_actions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListActionsResponse(
                actions=[
                    resources.Action(),
                    resources.Action(),
                    resources.Action(),
                ],
                next_page_token="abc",
            ),
            service.ListActionsResponse(
                actions=[],
                next_page_token="def",
            ),
            service.ListActionsResponse(
                actions=[
                    resources.Action(),
                ],
                next_page_token="ghi",
            ),
            service.ListActionsResponse(
                actions=[
                    resources.Action(),
                    resources.Action(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_zone_actions(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        service.CreateAssetRequest,
        dict,
    ],
)
def test_create_asset(request_type, transport: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_asset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_asset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateAssetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_asset_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_asset), "__call__") as call:
        client.create_asset()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateAssetRequest()


@pytest.mark.asyncio
async def test_create_asset_async(
    transport: str = "grpc_asyncio", request_type=service.CreateAssetRequest
):
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_asset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_asset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateAssetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_asset_async_from_dict():
    await test_create_asset_async(request_type=dict)


def test_create_asset_field_headers():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateAssetRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_asset), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_asset(request)

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
async def test_create_asset_field_headers_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateAssetRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_asset), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_asset(request)

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


def test_create_asset_flattened():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_asset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_asset(
            parent="parent_value",
            asset=resources.Asset(name="name_value"),
            asset_id="asset_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].asset
        mock_val = resources.Asset(name="name_value")
        assert arg == mock_val
        arg = args[0].asset_id
        mock_val = "asset_id_value"
        assert arg == mock_val


def test_create_asset_flattened_error():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_asset(
            service.CreateAssetRequest(),
            parent="parent_value",
            asset=resources.Asset(name="name_value"),
            asset_id="asset_id_value",
        )


@pytest.mark.asyncio
async def test_create_asset_flattened_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_asset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_asset(
            parent="parent_value",
            asset=resources.Asset(name="name_value"),
            asset_id="asset_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].asset
        mock_val = resources.Asset(name="name_value")
        assert arg == mock_val
        arg = args[0].asset_id
        mock_val = "asset_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_asset_flattened_error_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_asset(
            service.CreateAssetRequest(),
            parent="parent_value",
            asset=resources.Asset(name="name_value"),
            asset_id="asset_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.UpdateAssetRequest,
        dict,
    ],
)
def test_update_asset(request_type, transport: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_asset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_asset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateAssetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_asset_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_asset), "__call__") as call:
        client.update_asset()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateAssetRequest()


@pytest.mark.asyncio
async def test_update_asset_async(
    transport: str = "grpc_asyncio", request_type=service.UpdateAssetRequest
):
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_asset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_asset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateAssetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_asset_async_from_dict():
    await test_update_asset_async(request_type=dict)


def test_update_asset_field_headers():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateAssetRequest()

    request.asset.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_asset), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_asset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "asset.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_asset_field_headers_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateAssetRequest()

    request.asset.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_asset), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_asset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "asset.name=name_value",
    ) in kw["metadata"]


def test_update_asset_flattened():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_asset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_asset(
            asset=resources.Asset(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].asset
        mock_val = resources.Asset(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_asset_flattened_error():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_asset(
            service.UpdateAssetRequest(),
            asset=resources.Asset(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_asset_flattened_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_asset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_asset(
            asset=resources.Asset(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].asset
        mock_val = resources.Asset(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_asset_flattened_error_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_asset(
            service.UpdateAssetRequest(),
            asset=resources.Asset(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.DeleteAssetRequest,
        dict,
    ],
)
def test_delete_asset(request_type, transport: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_asset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_asset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteAssetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_asset_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_asset), "__call__") as call:
        client.delete_asset()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteAssetRequest()


@pytest.mark.asyncio
async def test_delete_asset_async(
    transport: str = "grpc_asyncio", request_type=service.DeleteAssetRequest
):
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_asset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_asset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteAssetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_asset_async_from_dict():
    await test_delete_asset_async(request_type=dict)


def test_delete_asset_field_headers():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.DeleteAssetRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_asset), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_asset(request)

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
async def test_delete_asset_field_headers_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.DeleteAssetRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_asset), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_asset(request)

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


def test_delete_asset_flattened():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_asset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_asset(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_asset_flattened_error():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_asset(
            service.DeleteAssetRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_asset_flattened_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_asset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_asset(
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
async def test_delete_asset_flattened_error_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_asset(
            service.DeleteAssetRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.ListAssetsRequest,
        dict,
    ],
)
def test_list_assets(request_type, transport: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_assets), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListAssetsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_assets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListAssetsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAssetsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_assets_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_assets), "__call__") as call:
        client.list_assets()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListAssetsRequest()


@pytest.mark.asyncio
async def test_list_assets_async(
    transport: str = "grpc_asyncio", request_type=service.ListAssetsRequest
):
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_assets), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListAssetsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_assets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListAssetsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAssetsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_assets_async_from_dict():
    await test_list_assets_async(request_type=dict)


def test_list_assets_field_headers():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListAssetsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_assets), "__call__") as call:
        call.return_value = service.ListAssetsResponse()
        client.list_assets(request)

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
async def test_list_assets_field_headers_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListAssetsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_assets), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListAssetsResponse()
        )
        await client.list_assets(request)

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


def test_list_assets_flattened():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_assets), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListAssetsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_assets(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_assets_flattened_error():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_assets(
            service.ListAssetsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_assets_flattened_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_assets), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListAssetsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListAssetsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_assets(
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
async def test_list_assets_flattened_error_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_assets(
            service.ListAssetsRequest(),
            parent="parent_value",
        )


def test_list_assets_pager(transport_name: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_assets), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListAssetsResponse(
                assets=[
                    resources.Asset(),
                    resources.Asset(),
                    resources.Asset(),
                ],
                next_page_token="abc",
            ),
            service.ListAssetsResponse(
                assets=[],
                next_page_token="def",
            ),
            service.ListAssetsResponse(
                assets=[
                    resources.Asset(),
                ],
                next_page_token="ghi",
            ),
            service.ListAssetsResponse(
                assets=[
                    resources.Asset(),
                    resources.Asset(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_assets(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.Asset) for i in results)


def test_list_assets_pages(transport_name: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_assets), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListAssetsResponse(
                assets=[
                    resources.Asset(),
                    resources.Asset(),
                    resources.Asset(),
                ],
                next_page_token="abc",
            ),
            service.ListAssetsResponse(
                assets=[],
                next_page_token="def",
            ),
            service.ListAssetsResponse(
                assets=[
                    resources.Asset(),
                ],
                next_page_token="ghi",
            ),
            service.ListAssetsResponse(
                assets=[
                    resources.Asset(),
                    resources.Asset(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_assets(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_assets_async_pager():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_assets), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListAssetsResponse(
                assets=[
                    resources.Asset(),
                    resources.Asset(),
                    resources.Asset(),
                ],
                next_page_token="abc",
            ),
            service.ListAssetsResponse(
                assets=[],
                next_page_token="def",
            ),
            service.ListAssetsResponse(
                assets=[
                    resources.Asset(),
                ],
                next_page_token="ghi",
            ),
            service.ListAssetsResponse(
                assets=[
                    resources.Asset(),
                    resources.Asset(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_assets(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.Asset) for i in responses)


@pytest.mark.asyncio
async def test_list_assets_async_pages():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_assets), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListAssetsResponse(
                assets=[
                    resources.Asset(),
                    resources.Asset(),
                    resources.Asset(),
                ],
                next_page_token="abc",
            ),
            service.ListAssetsResponse(
                assets=[],
                next_page_token="def",
            ),
            service.ListAssetsResponse(
                assets=[
                    resources.Asset(),
                ],
                next_page_token="ghi",
            ),
            service.ListAssetsResponse(
                assets=[
                    resources.Asset(),
                    resources.Asset(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_assets(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        service.GetAssetRequest,
        dict,
    ],
)
def test_get_asset(request_type, transport: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_asset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Asset(
            name="name_value",
            display_name="display_name_value",
            uid="uid_value",
            description="description_value",
            state=resources.State.ACTIVE,
        )
        response = client.get_asset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetAssetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Asset)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.uid == "uid_value"
    assert response.description == "description_value"
    assert response.state == resources.State.ACTIVE


def test_get_asset_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_asset), "__call__") as call:
        client.get_asset()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetAssetRequest()


@pytest.mark.asyncio
async def test_get_asset_async(
    transport: str = "grpc_asyncio", request_type=service.GetAssetRequest
):
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_asset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Asset(
                name="name_value",
                display_name="display_name_value",
                uid="uid_value",
                description="description_value",
                state=resources.State.ACTIVE,
            )
        )
        response = await client.get_asset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetAssetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Asset)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.uid == "uid_value"
    assert response.description == "description_value"
    assert response.state == resources.State.ACTIVE


@pytest.mark.asyncio
async def test_get_asset_async_from_dict():
    await test_get_asset_async(request_type=dict)


def test_get_asset_field_headers():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetAssetRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_asset), "__call__") as call:
        call.return_value = resources.Asset()
        client.get_asset(request)

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
async def test_get_asset_field_headers_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetAssetRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_asset), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Asset())
        await client.get_asset(request)

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


def test_get_asset_flattened():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_asset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Asset()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_asset(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_asset_flattened_error():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_asset(
            service.GetAssetRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_asset_flattened_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_asset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Asset()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Asset())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_asset(
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
async def test_get_asset_flattened_error_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_asset(
            service.GetAssetRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.ListAssetActionsRequest,
        dict,
    ],
)
def test_list_asset_actions(request_type, transport: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_asset_actions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListActionsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_asset_actions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListAssetActionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAssetActionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_asset_actions_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_asset_actions), "__call__"
    ) as call:
        client.list_asset_actions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListAssetActionsRequest()


@pytest.mark.asyncio
async def test_list_asset_actions_async(
    transport: str = "grpc_asyncio", request_type=service.ListAssetActionsRequest
):
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_asset_actions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListActionsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_asset_actions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListAssetActionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAssetActionsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_asset_actions_async_from_dict():
    await test_list_asset_actions_async(request_type=dict)


def test_list_asset_actions_field_headers():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListAssetActionsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_asset_actions), "__call__"
    ) as call:
        call.return_value = service.ListActionsResponse()
        client.list_asset_actions(request)

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
async def test_list_asset_actions_field_headers_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListAssetActionsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_asset_actions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListActionsResponse()
        )
        await client.list_asset_actions(request)

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


def test_list_asset_actions_flattened():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_asset_actions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListActionsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_asset_actions(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_asset_actions_flattened_error():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_asset_actions(
            service.ListAssetActionsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_asset_actions_flattened_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_asset_actions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListActionsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListActionsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_asset_actions(
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
async def test_list_asset_actions_flattened_error_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_asset_actions(
            service.ListAssetActionsRequest(),
            parent="parent_value",
        )


def test_list_asset_actions_pager(transport_name: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_asset_actions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListActionsResponse(
                actions=[
                    resources.Action(),
                    resources.Action(),
                    resources.Action(),
                ],
                next_page_token="abc",
            ),
            service.ListActionsResponse(
                actions=[],
                next_page_token="def",
            ),
            service.ListActionsResponse(
                actions=[
                    resources.Action(),
                ],
                next_page_token="ghi",
            ),
            service.ListActionsResponse(
                actions=[
                    resources.Action(),
                    resources.Action(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_asset_actions(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.Action) for i in results)


def test_list_asset_actions_pages(transport_name: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_asset_actions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListActionsResponse(
                actions=[
                    resources.Action(),
                    resources.Action(),
                    resources.Action(),
                ],
                next_page_token="abc",
            ),
            service.ListActionsResponse(
                actions=[],
                next_page_token="def",
            ),
            service.ListActionsResponse(
                actions=[
                    resources.Action(),
                ],
                next_page_token="ghi",
            ),
            service.ListActionsResponse(
                actions=[
                    resources.Action(),
                    resources.Action(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_asset_actions(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_asset_actions_async_pager():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_asset_actions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListActionsResponse(
                actions=[
                    resources.Action(),
                    resources.Action(),
                    resources.Action(),
                ],
                next_page_token="abc",
            ),
            service.ListActionsResponse(
                actions=[],
                next_page_token="def",
            ),
            service.ListActionsResponse(
                actions=[
                    resources.Action(),
                ],
                next_page_token="ghi",
            ),
            service.ListActionsResponse(
                actions=[
                    resources.Action(),
                    resources.Action(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_asset_actions(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.Action) for i in responses)


@pytest.mark.asyncio
async def test_list_asset_actions_async_pages():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_asset_actions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListActionsResponse(
                actions=[
                    resources.Action(),
                    resources.Action(),
                    resources.Action(),
                ],
                next_page_token="abc",
            ),
            service.ListActionsResponse(
                actions=[],
                next_page_token="def",
            ),
            service.ListActionsResponse(
                actions=[
                    resources.Action(),
                ],
                next_page_token="ghi",
            ),
            service.ListActionsResponse(
                actions=[
                    resources.Action(),
                    resources.Action(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_asset_actions(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        service.CreateTaskRequest,
        dict,
    ],
)
def test_create_task(request_type, transport: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_task), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_task(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateTaskRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_task_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_task), "__call__") as call:
        client.create_task()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateTaskRequest()


@pytest.mark.asyncio
async def test_create_task_async(
    transport: str = "grpc_asyncio", request_type=service.CreateTaskRequest
):
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_task), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_task(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateTaskRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_task_async_from_dict():
    await test_create_task_async(request_type=dict)


def test_create_task_field_headers():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateTaskRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_task), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_task(request)

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
async def test_create_task_field_headers_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateTaskRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_task), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_task(request)

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


def test_create_task_flattened():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_task), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_task(
            parent="parent_value",
            task=tasks.Task(name="name_value"),
            task_id="task_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].task
        mock_val = tasks.Task(name="name_value")
        assert arg == mock_val
        arg = args[0].task_id
        mock_val = "task_id_value"
        assert arg == mock_val


def test_create_task_flattened_error():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_task(
            service.CreateTaskRequest(),
            parent="parent_value",
            task=tasks.Task(name="name_value"),
            task_id="task_id_value",
        )


@pytest.mark.asyncio
async def test_create_task_flattened_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_task), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_task(
            parent="parent_value",
            task=tasks.Task(name="name_value"),
            task_id="task_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].task
        mock_val = tasks.Task(name="name_value")
        assert arg == mock_val
        arg = args[0].task_id
        mock_val = "task_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_task_flattened_error_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_task(
            service.CreateTaskRequest(),
            parent="parent_value",
            task=tasks.Task(name="name_value"),
            task_id="task_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.UpdateTaskRequest,
        dict,
    ],
)
def test_update_task(request_type, transport: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_task), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_task(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateTaskRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_task_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_task), "__call__") as call:
        client.update_task()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateTaskRequest()


@pytest.mark.asyncio
async def test_update_task_async(
    transport: str = "grpc_asyncio", request_type=service.UpdateTaskRequest
):
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_task), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_task(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateTaskRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_task_async_from_dict():
    await test_update_task_async(request_type=dict)


def test_update_task_field_headers():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateTaskRequest()

    request.task.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_task), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_task(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "task.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_task_field_headers_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateTaskRequest()

    request.task.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_task), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_task(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "task.name=name_value",
    ) in kw["metadata"]


def test_update_task_flattened():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_task), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_task(
            task=tasks.Task(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].task
        mock_val = tasks.Task(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_task_flattened_error():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_task(
            service.UpdateTaskRequest(),
            task=tasks.Task(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_task_flattened_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_task), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_task(
            task=tasks.Task(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].task
        mock_val = tasks.Task(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_task_flattened_error_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_task(
            service.UpdateTaskRequest(),
            task=tasks.Task(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.DeleteTaskRequest,
        dict,
    ],
)
def test_delete_task(request_type, transport: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_task), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_task(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteTaskRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_task_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_task), "__call__") as call:
        client.delete_task()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteTaskRequest()


@pytest.mark.asyncio
async def test_delete_task_async(
    transport: str = "grpc_asyncio", request_type=service.DeleteTaskRequest
):
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_task), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_task(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteTaskRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_task_async_from_dict():
    await test_delete_task_async(request_type=dict)


def test_delete_task_field_headers():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.DeleteTaskRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_task), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_task(request)

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
async def test_delete_task_field_headers_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.DeleteTaskRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_task), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_task(request)

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


def test_delete_task_flattened():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_task), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_task(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_task_flattened_error():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_task(
            service.DeleteTaskRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_task_flattened_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_task), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_task(
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
async def test_delete_task_flattened_error_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_task(
            service.DeleteTaskRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.ListTasksRequest,
        dict,
    ],
)
def test_list_tasks(request_type, transport: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tasks), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListTasksResponse(
            next_page_token="next_page_token_value",
            unreachable_locations=["unreachable_locations_value"],
        )
        response = client.list_tasks(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListTasksRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTasksPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable_locations == ["unreachable_locations_value"]


def test_list_tasks_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tasks), "__call__") as call:
        client.list_tasks()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListTasksRequest()


@pytest.mark.asyncio
async def test_list_tasks_async(
    transport: str = "grpc_asyncio", request_type=service.ListTasksRequest
):
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tasks), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListTasksResponse(
                next_page_token="next_page_token_value",
                unreachable_locations=["unreachable_locations_value"],
            )
        )
        response = await client.list_tasks(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListTasksRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTasksAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable_locations == ["unreachable_locations_value"]


@pytest.mark.asyncio
async def test_list_tasks_async_from_dict():
    await test_list_tasks_async(request_type=dict)


def test_list_tasks_field_headers():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListTasksRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tasks), "__call__") as call:
        call.return_value = service.ListTasksResponse()
        client.list_tasks(request)

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
async def test_list_tasks_field_headers_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListTasksRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tasks), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListTasksResponse()
        )
        await client.list_tasks(request)

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


def test_list_tasks_flattened():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tasks), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListTasksResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_tasks(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_tasks_flattened_error():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_tasks(
            service.ListTasksRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_tasks_flattened_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tasks), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListTasksResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListTasksResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_tasks(
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
async def test_list_tasks_flattened_error_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_tasks(
            service.ListTasksRequest(),
            parent="parent_value",
        )


def test_list_tasks_pager(transport_name: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tasks), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListTasksResponse(
                tasks=[
                    tasks.Task(),
                    tasks.Task(),
                    tasks.Task(),
                ],
                next_page_token="abc",
            ),
            service.ListTasksResponse(
                tasks=[],
                next_page_token="def",
            ),
            service.ListTasksResponse(
                tasks=[
                    tasks.Task(),
                ],
                next_page_token="ghi",
            ),
            service.ListTasksResponse(
                tasks=[
                    tasks.Task(),
                    tasks.Task(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_tasks(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, tasks.Task) for i in results)


def test_list_tasks_pages(transport_name: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tasks), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListTasksResponse(
                tasks=[
                    tasks.Task(),
                    tasks.Task(),
                    tasks.Task(),
                ],
                next_page_token="abc",
            ),
            service.ListTasksResponse(
                tasks=[],
                next_page_token="def",
            ),
            service.ListTasksResponse(
                tasks=[
                    tasks.Task(),
                ],
                next_page_token="ghi",
            ),
            service.ListTasksResponse(
                tasks=[
                    tasks.Task(),
                    tasks.Task(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_tasks(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_tasks_async_pager():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tasks), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListTasksResponse(
                tasks=[
                    tasks.Task(),
                    tasks.Task(),
                    tasks.Task(),
                ],
                next_page_token="abc",
            ),
            service.ListTasksResponse(
                tasks=[],
                next_page_token="def",
            ),
            service.ListTasksResponse(
                tasks=[
                    tasks.Task(),
                ],
                next_page_token="ghi",
            ),
            service.ListTasksResponse(
                tasks=[
                    tasks.Task(),
                    tasks.Task(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_tasks(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, tasks.Task) for i in responses)


@pytest.mark.asyncio
async def test_list_tasks_async_pages():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tasks), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListTasksResponse(
                tasks=[
                    tasks.Task(),
                    tasks.Task(),
                    tasks.Task(),
                ],
                next_page_token="abc",
            ),
            service.ListTasksResponse(
                tasks=[],
                next_page_token="def",
            ),
            service.ListTasksResponse(
                tasks=[
                    tasks.Task(),
                ],
                next_page_token="ghi",
            ),
            service.ListTasksResponse(
                tasks=[
                    tasks.Task(),
                    tasks.Task(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_tasks(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        service.GetTaskRequest,
        dict,
    ],
)
def test_get_task(request_type, transport: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_task), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tasks.Task(
            name="name_value",
            uid="uid_value",
            description="description_value",
            display_name="display_name_value",
            state=resources.State.ACTIVE,
        )
        response = client.get_task(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetTaskRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tasks.Task)
    assert response.name == "name_value"
    assert response.uid == "uid_value"
    assert response.description == "description_value"
    assert response.display_name == "display_name_value"
    assert response.state == resources.State.ACTIVE


def test_get_task_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_task), "__call__") as call:
        client.get_task()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetTaskRequest()


@pytest.mark.asyncio
async def test_get_task_async(
    transport: str = "grpc_asyncio", request_type=service.GetTaskRequest
):
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_task), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tasks.Task(
                name="name_value",
                uid="uid_value",
                description="description_value",
                display_name="display_name_value",
                state=resources.State.ACTIVE,
            )
        )
        response = await client.get_task(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetTaskRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tasks.Task)
    assert response.name == "name_value"
    assert response.uid == "uid_value"
    assert response.description == "description_value"
    assert response.display_name == "display_name_value"
    assert response.state == resources.State.ACTIVE


@pytest.mark.asyncio
async def test_get_task_async_from_dict():
    await test_get_task_async(request_type=dict)


def test_get_task_field_headers():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetTaskRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_task), "__call__") as call:
        call.return_value = tasks.Task()
        client.get_task(request)

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
async def test_get_task_field_headers_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetTaskRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_task), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(tasks.Task())
        await client.get_task(request)

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


def test_get_task_flattened():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_task), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tasks.Task()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_task(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_task_flattened_error():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_task(
            service.GetTaskRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_task_flattened_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_task), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tasks.Task()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(tasks.Task())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_task(
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
async def test_get_task_flattened_error_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_task(
            service.GetTaskRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.ListJobsRequest,
        dict,
    ],
)
def test_list_jobs(request_type, transport: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_jobs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListJobsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListJobsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListJobsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_jobs_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_jobs), "__call__") as call:
        client.list_jobs()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListJobsRequest()


@pytest.mark.asyncio
async def test_list_jobs_async(
    transport: str = "grpc_asyncio", request_type=service.ListJobsRequest
):
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_jobs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListJobsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListJobsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListJobsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_jobs_async_from_dict():
    await test_list_jobs_async(request_type=dict)


def test_list_jobs_field_headers():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListJobsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_jobs), "__call__") as call:
        call.return_value = service.ListJobsResponse()
        client.list_jobs(request)

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
async def test_list_jobs_field_headers_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListJobsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_jobs), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListJobsResponse()
        )
        await client.list_jobs(request)

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


def test_list_jobs_flattened():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_jobs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListJobsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_jobs(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_jobs_flattened_error():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_jobs(
            service.ListJobsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_jobs_flattened_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_jobs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListJobsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListJobsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_jobs(
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
async def test_list_jobs_flattened_error_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_jobs(
            service.ListJobsRequest(),
            parent="parent_value",
        )


def test_list_jobs_pager(transport_name: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_jobs), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListJobsResponse(
                jobs=[
                    tasks.Job(),
                    tasks.Job(),
                    tasks.Job(),
                ],
                next_page_token="abc",
            ),
            service.ListJobsResponse(
                jobs=[],
                next_page_token="def",
            ),
            service.ListJobsResponse(
                jobs=[
                    tasks.Job(),
                ],
                next_page_token="ghi",
            ),
            service.ListJobsResponse(
                jobs=[
                    tasks.Job(),
                    tasks.Job(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_jobs(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, tasks.Job) for i in results)


def test_list_jobs_pages(transport_name: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_jobs), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListJobsResponse(
                jobs=[
                    tasks.Job(),
                    tasks.Job(),
                    tasks.Job(),
                ],
                next_page_token="abc",
            ),
            service.ListJobsResponse(
                jobs=[],
                next_page_token="def",
            ),
            service.ListJobsResponse(
                jobs=[
                    tasks.Job(),
                ],
                next_page_token="ghi",
            ),
            service.ListJobsResponse(
                jobs=[
                    tasks.Job(),
                    tasks.Job(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_jobs(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_jobs_async_pager():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_jobs), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListJobsResponse(
                jobs=[
                    tasks.Job(),
                    tasks.Job(),
                    tasks.Job(),
                ],
                next_page_token="abc",
            ),
            service.ListJobsResponse(
                jobs=[],
                next_page_token="def",
            ),
            service.ListJobsResponse(
                jobs=[
                    tasks.Job(),
                ],
                next_page_token="ghi",
            ),
            service.ListJobsResponse(
                jobs=[
                    tasks.Job(),
                    tasks.Job(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_jobs(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, tasks.Job) for i in responses)


@pytest.mark.asyncio
async def test_list_jobs_async_pages():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_jobs), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListJobsResponse(
                jobs=[
                    tasks.Job(),
                    tasks.Job(),
                    tasks.Job(),
                ],
                next_page_token="abc",
            ),
            service.ListJobsResponse(
                jobs=[],
                next_page_token="def",
            ),
            service.ListJobsResponse(
                jobs=[
                    tasks.Job(),
                ],
                next_page_token="ghi",
            ),
            service.ListJobsResponse(
                jobs=[
                    tasks.Job(),
                    tasks.Job(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_jobs(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        service.RunTaskRequest,
        dict,
    ],
)
def test_run_task(request_type, transport: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_task), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.RunTaskResponse()
        response = client.run_task(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.RunTaskRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.RunTaskResponse)


def test_run_task_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_task), "__call__") as call:
        client.run_task()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.RunTaskRequest()


@pytest.mark.asyncio
async def test_run_task_async(
    transport: str = "grpc_asyncio", request_type=service.RunTaskRequest
):
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_task), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.RunTaskResponse()
        )
        response = await client.run_task(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.RunTaskRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.RunTaskResponse)


@pytest.mark.asyncio
async def test_run_task_async_from_dict():
    await test_run_task_async(request_type=dict)


def test_run_task_field_headers():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.RunTaskRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_task), "__call__") as call:
        call.return_value = service.RunTaskResponse()
        client.run_task(request)

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
async def test_run_task_field_headers_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.RunTaskRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_task), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.RunTaskResponse()
        )
        await client.run_task(request)

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


def test_run_task_flattened():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_task), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.RunTaskResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.run_task(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_run_task_flattened_error():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.run_task(
            service.RunTaskRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_run_task_flattened_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_task), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.RunTaskResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.RunTaskResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.run_task(
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
async def test_run_task_flattened_error_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.run_task(
            service.RunTaskRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.GetJobRequest,
        dict,
    ],
)
def test_get_job(request_type, transport: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tasks.Job(
            name="name_value",
            uid="uid_value",
            state=tasks.Job.State.RUNNING,
            retry_count=1214,
            service=tasks.Job.Service.DATAPROC,
            service_job="service_job_value",
            message="message_value",
        )
        response = client.get_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tasks.Job)
    assert response.name == "name_value"
    assert response.uid == "uid_value"
    assert response.state == tasks.Job.State.RUNNING
    assert response.retry_count == 1214
    assert response.service == tasks.Job.Service.DATAPROC
    assert response.service_job == "service_job_value"
    assert response.message == "message_value"


def test_get_job_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_job), "__call__") as call:
        client.get_job()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetJobRequest()


@pytest.mark.asyncio
async def test_get_job_async(
    transport: str = "grpc_asyncio", request_type=service.GetJobRequest
):
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            tasks.Job(
                name="name_value",
                uid="uid_value",
                state=tasks.Job.State.RUNNING,
                retry_count=1214,
                service=tasks.Job.Service.DATAPROC,
                service_job="service_job_value",
                message="message_value",
            )
        )
        response = await client.get_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, tasks.Job)
    assert response.name == "name_value"
    assert response.uid == "uid_value"
    assert response.state == tasks.Job.State.RUNNING
    assert response.retry_count == 1214
    assert response.service == tasks.Job.Service.DATAPROC
    assert response.service_job == "service_job_value"
    assert response.message == "message_value"


@pytest.mark.asyncio
async def test_get_job_async_from_dict():
    await test_get_job_async(request_type=dict)


def test_get_job_field_headers():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetJobRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_job), "__call__") as call:
        call.return_value = tasks.Job()
        client.get_job(request)

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
async def test_get_job_field_headers_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetJobRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_job), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(tasks.Job())
        await client.get_job(request)

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


def test_get_job_flattened():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tasks.Job()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_job(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_job_flattened_error():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_job(
            service.GetJobRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_job_flattened_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = tasks.Job()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(tasks.Job())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_job(
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
async def test_get_job_flattened_error_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_job(
            service.GetJobRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.CancelJobRequest,
        dict,
    ],
)
def test_cancel_job(request_type, transport: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.cancel_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CancelJobRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_cancel_job_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_job), "__call__") as call:
        client.cancel_job()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CancelJobRequest()


@pytest.mark.asyncio
async def test_cancel_job_async(
    transport: str = "grpc_asyncio", request_type=service.CancelJobRequest
):
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.cancel_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CancelJobRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_cancel_job_async_from_dict():
    await test_cancel_job_async(request_type=dict)


def test_cancel_job_field_headers():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CancelJobRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_job), "__call__") as call:
        call.return_value = None
        client.cancel_job(request)

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
async def test_cancel_job_field_headers_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CancelJobRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_job), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.cancel_job(request)

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


def test_cancel_job_flattened():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.cancel_job(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_cancel_job_flattened_error():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.cancel_job(
            service.CancelJobRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_cancel_job_flattened_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.cancel_job(
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
async def test_cancel_job_flattened_error_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.cancel_job(
            service.CancelJobRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.CreateEnvironmentRequest,
        dict,
    ],
)
def test_create_environment(request_type, transport: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateEnvironmentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_environment_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_environment), "__call__"
    ) as call:
        client.create_environment()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateEnvironmentRequest()


@pytest.mark.asyncio
async def test_create_environment_async(
    transport: str = "grpc_asyncio", request_type=service.CreateEnvironmentRequest
):
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateEnvironmentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_environment_async_from_dict():
    await test_create_environment_async(request_type=dict)


def test_create_environment_field_headers():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateEnvironmentRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_environment), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_environment(request)

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
async def test_create_environment_field_headers_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateEnvironmentRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_environment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_environment(request)

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


def test_create_environment_flattened():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_environment(
            parent="parent_value",
            environment=analyze.Environment(name="name_value"),
            environment_id="environment_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].environment
        mock_val = analyze.Environment(name="name_value")
        assert arg == mock_val
        arg = args[0].environment_id
        mock_val = "environment_id_value"
        assert arg == mock_val


def test_create_environment_flattened_error():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_environment(
            service.CreateEnvironmentRequest(),
            parent="parent_value",
            environment=analyze.Environment(name="name_value"),
            environment_id="environment_id_value",
        )


@pytest.mark.asyncio
async def test_create_environment_flattened_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_environment(
            parent="parent_value",
            environment=analyze.Environment(name="name_value"),
            environment_id="environment_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].environment
        mock_val = analyze.Environment(name="name_value")
        assert arg == mock_val
        arg = args[0].environment_id
        mock_val = "environment_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_environment_flattened_error_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_environment(
            service.CreateEnvironmentRequest(),
            parent="parent_value",
            environment=analyze.Environment(name="name_value"),
            environment_id="environment_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.UpdateEnvironmentRequest,
        dict,
    ],
)
def test_update_environment(request_type, transport: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateEnvironmentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_environment_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_environment), "__call__"
    ) as call:
        client.update_environment()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateEnvironmentRequest()


@pytest.mark.asyncio
async def test_update_environment_async(
    transport: str = "grpc_asyncio", request_type=service.UpdateEnvironmentRequest
):
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateEnvironmentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_environment_async_from_dict():
    await test_update_environment_async(request_type=dict)


def test_update_environment_field_headers():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateEnvironmentRequest()

    request.environment.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_environment), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "environment.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_environment_field_headers_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateEnvironmentRequest()

    request.environment.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_environment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "environment.name=name_value",
    ) in kw["metadata"]


def test_update_environment_flattened():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_environment(
            environment=analyze.Environment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].environment
        mock_val = analyze.Environment(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_environment_flattened_error():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_environment(
            service.UpdateEnvironmentRequest(),
            environment=analyze.Environment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_environment_flattened_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_environment(
            environment=analyze.Environment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].environment
        mock_val = analyze.Environment(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_environment_flattened_error_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_environment(
            service.UpdateEnvironmentRequest(),
            environment=analyze.Environment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.DeleteEnvironmentRequest,
        dict,
    ],
)
def test_delete_environment(request_type, transport: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteEnvironmentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_environment_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_environment), "__call__"
    ) as call:
        client.delete_environment()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteEnvironmentRequest()


@pytest.mark.asyncio
async def test_delete_environment_async(
    transport: str = "grpc_asyncio", request_type=service.DeleteEnvironmentRequest
):
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteEnvironmentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_environment_async_from_dict():
    await test_delete_environment_async(request_type=dict)


def test_delete_environment_field_headers():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.DeleteEnvironmentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_environment), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_environment(request)

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
async def test_delete_environment_field_headers_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.DeleteEnvironmentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_environment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_environment(request)

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


def test_delete_environment_flattened():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_environment(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_environment_flattened_error():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_environment(
            service.DeleteEnvironmentRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_environment_flattened_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_environment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_environment(
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
async def test_delete_environment_flattened_error_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_environment(
            service.DeleteEnvironmentRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.ListEnvironmentsRequest,
        dict,
    ],
)
def test_list_environments(request_type, transport: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_environments), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListEnvironmentsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_environments(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListEnvironmentsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListEnvironmentsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_environments_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_environments), "__call__"
    ) as call:
        client.list_environments()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListEnvironmentsRequest()


@pytest.mark.asyncio
async def test_list_environments_async(
    transport: str = "grpc_asyncio", request_type=service.ListEnvironmentsRequest
):
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_environments), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListEnvironmentsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_environments(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListEnvironmentsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListEnvironmentsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_environments_async_from_dict():
    await test_list_environments_async(request_type=dict)


def test_list_environments_field_headers():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListEnvironmentsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_environments), "__call__"
    ) as call:
        call.return_value = service.ListEnvironmentsResponse()
        client.list_environments(request)

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
async def test_list_environments_field_headers_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListEnvironmentsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_environments), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListEnvironmentsResponse()
        )
        await client.list_environments(request)

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


def test_list_environments_flattened():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_environments), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListEnvironmentsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_environments(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_environments_flattened_error():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_environments(
            service.ListEnvironmentsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_environments_flattened_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_environments), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListEnvironmentsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListEnvironmentsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_environments(
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
async def test_list_environments_flattened_error_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_environments(
            service.ListEnvironmentsRequest(),
            parent="parent_value",
        )


def test_list_environments_pager(transport_name: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_environments), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListEnvironmentsResponse(
                environments=[
                    analyze.Environment(),
                    analyze.Environment(),
                    analyze.Environment(),
                ],
                next_page_token="abc",
            ),
            service.ListEnvironmentsResponse(
                environments=[],
                next_page_token="def",
            ),
            service.ListEnvironmentsResponse(
                environments=[
                    analyze.Environment(),
                ],
                next_page_token="ghi",
            ),
            service.ListEnvironmentsResponse(
                environments=[
                    analyze.Environment(),
                    analyze.Environment(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_environments(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, analyze.Environment) for i in results)


def test_list_environments_pages(transport_name: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_environments), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListEnvironmentsResponse(
                environments=[
                    analyze.Environment(),
                    analyze.Environment(),
                    analyze.Environment(),
                ],
                next_page_token="abc",
            ),
            service.ListEnvironmentsResponse(
                environments=[],
                next_page_token="def",
            ),
            service.ListEnvironmentsResponse(
                environments=[
                    analyze.Environment(),
                ],
                next_page_token="ghi",
            ),
            service.ListEnvironmentsResponse(
                environments=[
                    analyze.Environment(),
                    analyze.Environment(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_environments(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_environments_async_pager():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_environments),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListEnvironmentsResponse(
                environments=[
                    analyze.Environment(),
                    analyze.Environment(),
                    analyze.Environment(),
                ],
                next_page_token="abc",
            ),
            service.ListEnvironmentsResponse(
                environments=[],
                next_page_token="def",
            ),
            service.ListEnvironmentsResponse(
                environments=[
                    analyze.Environment(),
                ],
                next_page_token="ghi",
            ),
            service.ListEnvironmentsResponse(
                environments=[
                    analyze.Environment(),
                    analyze.Environment(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_environments(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, analyze.Environment) for i in responses)


@pytest.mark.asyncio
async def test_list_environments_async_pages():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_environments),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListEnvironmentsResponse(
                environments=[
                    analyze.Environment(),
                    analyze.Environment(),
                    analyze.Environment(),
                ],
                next_page_token="abc",
            ),
            service.ListEnvironmentsResponse(
                environments=[],
                next_page_token="def",
            ),
            service.ListEnvironmentsResponse(
                environments=[
                    analyze.Environment(),
                ],
                next_page_token="ghi",
            ),
            service.ListEnvironmentsResponse(
                environments=[
                    analyze.Environment(),
                    analyze.Environment(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_environments(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        service.GetEnvironmentRequest,
        dict,
    ],
)
def test_get_environment(request_type, transport: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_environment), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = analyze.Environment(
            name="name_value",
            display_name="display_name_value",
            uid="uid_value",
            description="description_value",
            state=resources.State.ACTIVE,
        )
        response = client.get_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetEnvironmentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, analyze.Environment)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.uid == "uid_value"
    assert response.description == "description_value"
    assert response.state == resources.State.ACTIVE


def test_get_environment_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_environment), "__call__") as call:
        client.get_environment()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetEnvironmentRequest()


@pytest.mark.asyncio
async def test_get_environment_async(
    transport: str = "grpc_asyncio", request_type=service.GetEnvironmentRequest
):
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_environment), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analyze.Environment(
                name="name_value",
                display_name="display_name_value",
                uid="uid_value",
                description="description_value",
                state=resources.State.ACTIVE,
            )
        )
        response = await client.get_environment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetEnvironmentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, analyze.Environment)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.uid == "uid_value"
    assert response.description == "description_value"
    assert response.state == resources.State.ACTIVE


@pytest.mark.asyncio
async def test_get_environment_async_from_dict():
    await test_get_environment_async(request_type=dict)


def test_get_environment_field_headers():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetEnvironmentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_environment), "__call__") as call:
        call.return_value = analyze.Environment()
        client.get_environment(request)

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
async def test_get_environment_field_headers_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetEnvironmentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_environment), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(analyze.Environment())
        await client.get_environment(request)

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


def test_get_environment_flattened():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_environment), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = analyze.Environment()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_environment(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_environment_flattened_error():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_environment(
            service.GetEnvironmentRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_environment_flattened_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_environment), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = analyze.Environment()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(analyze.Environment())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_environment(
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
async def test_get_environment_flattened_error_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_environment(
            service.GetEnvironmentRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.ListSessionsRequest,
        dict,
    ],
)
def test_list_sessions(request_type, transport: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_sessions), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListSessionsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_sessions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListSessionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSessionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_sessions_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_sessions), "__call__") as call:
        client.list_sessions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListSessionsRequest()


@pytest.mark.asyncio
async def test_list_sessions_async(
    transport: str = "grpc_asyncio", request_type=service.ListSessionsRequest
):
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_sessions), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListSessionsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_sessions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListSessionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSessionsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_sessions_async_from_dict():
    await test_list_sessions_async(request_type=dict)


def test_list_sessions_field_headers():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListSessionsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_sessions), "__call__") as call:
        call.return_value = service.ListSessionsResponse()
        client.list_sessions(request)

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
async def test_list_sessions_field_headers_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListSessionsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_sessions), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListSessionsResponse()
        )
        await client.list_sessions(request)

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


def test_list_sessions_flattened():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_sessions), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListSessionsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_sessions(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_sessions_flattened_error():
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_sessions(
            service.ListSessionsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_sessions_flattened_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_sessions), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListSessionsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListSessionsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_sessions(
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
async def test_list_sessions_flattened_error_async():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_sessions(
            service.ListSessionsRequest(),
            parent="parent_value",
        )


def test_list_sessions_pager(transport_name: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_sessions), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListSessionsResponse(
                sessions=[
                    analyze.Session(),
                    analyze.Session(),
                    analyze.Session(),
                ],
                next_page_token="abc",
            ),
            service.ListSessionsResponse(
                sessions=[],
                next_page_token="def",
            ),
            service.ListSessionsResponse(
                sessions=[
                    analyze.Session(),
                ],
                next_page_token="ghi",
            ),
            service.ListSessionsResponse(
                sessions=[
                    analyze.Session(),
                    analyze.Session(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_sessions(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, analyze.Session) for i in results)


def test_list_sessions_pages(transport_name: str = "grpc"):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_sessions), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListSessionsResponse(
                sessions=[
                    analyze.Session(),
                    analyze.Session(),
                    analyze.Session(),
                ],
                next_page_token="abc",
            ),
            service.ListSessionsResponse(
                sessions=[],
                next_page_token="def",
            ),
            service.ListSessionsResponse(
                sessions=[
                    analyze.Session(),
                ],
                next_page_token="ghi",
            ),
            service.ListSessionsResponse(
                sessions=[
                    analyze.Session(),
                    analyze.Session(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_sessions(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_sessions_async_pager():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_sessions), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListSessionsResponse(
                sessions=[
                    analyze.Session(),
                    analyze.Session(),
                    analyze.Session(),
                ],
                next_page_token="abc",
            ),
            service.ListSessionsResponse(
                sessions=[],
                next_page_token="def",
            ),
            service.ListSessionsResponse(
                sessions=[
                    analyze.Session(),
                ],
                next_page_token="ghi",
            ),
            service.ListSessionsResponse(
                sessions=[
                    analyze.Session(),
                    analyze.Session(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_sessions(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, analyze.Session) for i in responses)


@pytest.mark.asyncio
async def test_list_sessions_async_pages():
    client = DataplexServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_sessions), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListSessionsResponse(
                sessions=[
                    analyze.Session(),
                    analyze.Session(),
                    analyze.Session(),
                ],
                next_page_token="abc",
            ),
            service.ListSessionsResponse(
                sessions=[],
                next_page_token="def",
            ),
            service.ListSessionsResponse(
                sessions=[
                    analyze.Session(),
                ],
                next_page_token="ghi",
            ),
            service.ListSessionsResponse(
                sessions=[
                    analyze.Session(),
                    analyze.Session(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_sessions(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.DataplexServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DataplexServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.DataplexServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DataplexServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.DataplexServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = DataplexServiceClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = DataplexServiceClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.DataplexServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = DataplexServiceClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.DataplexServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = DataplexServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.DataplexServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.DataplexServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.DataplexServiceGrpcTransport,
        transports.DataplexServiceGrpcAsyncIOTransport,
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
    transport = DataplexServiceClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.DataplexServiceGrpcTransport,
    )


def test_dataplex_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.DataplexServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_dataplex_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.dataplex_v1.services.dataplex_service.transports.DataplexServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.DataplexServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_lake",
        "update_lake",
        "delete_lake",
        "list_lakes",
        "get_lake",
        "list_lake_actions",
        "create_zone",
        "update_zone",
        "delete_zone",
        "list_zones",
        "get_zone",
        "list_zone_actions",
        "create_asset",
        "update_asset",
        "delete_asset",
        "list_assets",
        "get_asset",
        "list_asset_actions",
        "create_task",
        "update_task",
        "delete_task",
        "list_tasks",
        "get_task",
        "list_jobs",
        "run_task",
        "get_job",
        "cancel_job",
        "create_environment",
        "update_environment",
        "delete_environment",
        "list_environments",
        "get_environment",
        "list_sessions",
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


def test_dataplex_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.dataplex_v1.services.dataplex_service.transports.DataplexServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.DataplexServiceTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_dataplex_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.dataplex_v1.services.dataplex_service.transports.DataplexServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.DataplexServiceTransport()
        adc.assert_called_once()


def test_dataplex_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        DataplexServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.DataplexServiceGrpcTransport,
        transports.DataplexServiceGrpcAsyncIOTransport,
    ],
)
def test_dataplex_service_transport_auth_adc(transport_class):
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
        transports.DataplexServiceGrpcTransport,
        transports.DataplexServiceGrpcAsyncIOTransport,
    ],
)
def test_dataplex_service_transport_auth_gdch_credentials(transport_class):
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
        (transports.DataplexServiceGrpcTransport, grpc_helpers),
        (transports.DataplexServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_dataplex_service_transport_create_channel(transport_class, grpc_helpers):
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
            "dataplex.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="dataplex.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.DataplexServiceGrpcTransport,
        transports.DataplexServiceGrpcAsyncIOTransport,
    ],
)
def test_dataplex_service_grpc_transport_client_cert_source_for_mtls(transport_class):
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
def test_dataplex_service_host_no_port(transport_name):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dataplex.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("dataplex.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
    ],
)
def test_dataplex_service_host_with_port(transport_name):
    client = DataplexServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dataplex.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("dataplex.googleapis.com:8000")


def test_dataplex_service_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.DataplexServiceGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_dataplex_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.DataplexServiceGrpcAsyncIOTransport(
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
        transports.DataplexServiceGrpcTransport,
        transports.DataplexServiceGrpcAsyncIOTransport,
    ],
)
def test_dataplex_service_transport_channel_mtls_with_client_cert_source(
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
        transports.DataplexServiceGrpcTransport,
        transports.DataplexServiceGrpcAsyncIOTransport,
    ],
)
def test_dataplex_service_transport_channel_mtls_with_adc(transport_class):
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


def test_dataplex_service_grpc_lro_client():
    client = DataplexServiceClient(
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


def test_dataplex_service_grpc_lro_async_client():
    client = DataplexServiceAsyncClient(
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


def test_action_path():
    project = "squid"
    location = "clam"
    lake = "whelk"
    action = "octopus"
    expected = (
        "projects/{project}/locations/{location}/lakes/{lake}/actions/{action}".format(
            project=project,
            location=location,
            lake=lake,
            action=action,
        )
    )
    actual = DataplexServiceClient.action_path(project, location, lake, action)
    assert expected == actual


def test_parse_action_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
        "lake": "cuttlefish",
        "action": "mussel",
    }
    path = DataplexServiceClient.action_path(**expected)

    # Check that the path construction is reversible.
    actual = DataplexServiceClient.parse_action_path(path)
    assert expected == actual


def test_asset_path():
    project = "winkle"
    location = "nautilus"
    lake = "scallop"
    zone = "abalone"
    asset = "squid"
    expected = "projects/{project}/locations/{location}/lakes/{lake}/zones/{zone}/assets/{asset}".format(
        project=project,
        location=location,
        lake=lake,
        zone=zone,
        asset=asset,
    )
    actual = DataplexServiceClient.asset_path(project, location, lake, zone, asset)
    assert expected == actual


def test_parse_asset_path():
    expected = {
        "project": "clam",
        "location": "whelk",
        "lake": "octopus",
        "zone": "oyster",
        "asset": "nudibranch",
    }
    path = DataplexServiceClient.asset_path(**expected)

    # Check that the path construction is reversible.
    actual = DataplexServiceClient.parse_asset_path(path)
    assert expected == actual


def test_environment_path():
    project = "cuttlefish"
    location = "mussel"
    lake = "winkle"
    environment = "nautilus"
    expected = "projects/{project}/locations/{location}/lakes/{lake}/environments/{environment}".format(
        project=project,
        location=location,
        lake=lake,
        environment=environment,
    )
    actual = DataplexServiceClient.environment_path(
        project, location, lake, environment
    )
    assert expected == actual


def test_parse_environment_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
        "lake": "squid",
        "environment": "clam",
    }
    path = DataplexServiceClient.environment_path(**expected)

    # Check that the path construction is reversible.
    actual = DataplexServiceClient.parse_environment_path(path)
    assert expected == actual


def test_job_path():
    project = "whelk"
    location = "octopus"
    lake = "oyster"
    task = "nudibranch"
    job = "cuttlefish"
    expected = "projects/{project}/locations/{location}/lakes/{lake}/tasks/{task}/jobs/{job}".format(
        project=project,
        location=location,
        lake=lake,
        task=task,
        job=job,
    )
    actual = DataplexServiceClient.job_path(project, location, lake, task, job)
    assert expected == actual


def test_parse_job_path():
    expected = {
        "project": "mussel",
        "location": "winkle",
        "lake": "nautilus",
        "task": "scallop",
        "job": "abalone",
    }
    path = DataplexServiceClient.job_path(**expected)

    # Check that the path construction is reversible.
    actual = DataplexServiceClient.parse_job_path(path)
    assert expected == actual


def test_lake_path():
    project = "squid"
    location = "clam"
    lake = "whelk"
    expected = "projects/{project}/locations/{location}/lakes/{lake}".format(
        project=project,
        location=location,
        lake=lake,
    )
    actual = DataplexServiceClient.lake_path(project, location, lake)
    assert expected == actual


def test_parse_lake_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "lake": "nudibranch",
    }
    path = DataplexServiceClient.lake_path(**expected)

    # Check that the path construction is reversible.
    actual = DataplexServiceClient.parse_lake_path(path)
    assert expected == actual


def test_session_path():
    project = "cuttlefish"
    location = "mussel"
    lake = "winkle"
    environment = "nautilus"
    session = "scallop"
    expected = "projects/{project}/locations/{location}/lakes/{lake}/environments/{environment}/sessions/{session}".format(
        project=project,
        location=location,
        lake=lake,
        environment=environment,
        session=session,
    )
    actual = DataplexServiceClient.session_path(
        project, location, lake, environment, session
    )
    assert expected == actual


def test_parse_session_path():
    expected = {
        "project": "abalone",
        "location": "squid",
        "lake": "clam",
        "environment": "whelk",
        "session": "octopus",
    }
    path = DataplexServiceClient.session_path(**expected)

    # Check that the path construction is reversible.
    actual = DataplexServiceClient.parse_session_path(path)
    assert expected == actual


def test_task_path():
    project = "oyster"
    location = "nudibranch"
    lake = "cuttlefish"
    task = "mussel"
    expected = (
        "projects/{project}/locations/{location}/lakes/{lake}/tasks/{task}".format(
            project=project,
            location=location,
            lake=lake,
            task=task,
        )
    )
    actual = DataplexServiceClient.task_path(project, location, lake, task)
    assert expected == actual


def test_parse_task_path():
    expected = {
        "project": "winkle",
        "location": "nautilus",
        "lake": "scallop",
        "task": "abalone",
    }
    path = DataplexServiceClient.task_path(**expected)

    # Check that the path construction is reversible.
    actual = DataplexServiceClient.parse_task_path(path)
    assert expected == actual


def test_zone_path():
    project = "squid"
    location = "clam"
    lake = "whelk"
    zone = "octopus"
    expected = (
        "projects/{project}/locations/{location}/lakes/{lake}/zones/{zone}".format(
            project=project,
            location=location,
            lake=lake,
            zone=zone,
        )
    )
    actual = DataplexServiceClient.zone_path(project, location, lake, zone)
    assert expected == actual


def test_parse_zone_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
        "lake": "cuttlefish",
        "zone": "mussel",
    }
    path = DataplexServiceClient.zone_path(**expected)

    # Check that the path construction is reversible.
    actual = DataplexServiceClient.parse_zone_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "winkle"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = DataplexServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "nautilus",
    }
    path = DataplexServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = DataplexServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "scallop"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = DataplexServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "abalone",
    }
    path = DataplexServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = DataplexServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "squid"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = DataplexServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "clam",
    }
    path = DataplexServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = DataplexServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "whelk"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = DataplexServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "octopus",
    }
    path = DataplexServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = DataplexServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "oyster"
    location = "nudibranch"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = DataplexServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "cuttlefish",
        "location": "mussel",
    }
    path = DataplexServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = DataplexServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.DataplexServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = DataplexServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.DataplexServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = DataplexServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = DataplexServiceAsyncClient(
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
    client = DataplexServiceClient(
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
    client = DataplexServiceAsyncClient(
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
    client = DataplexServiceClient(
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
    client = DataplexServiceAsyncClient(
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
    client = DataplexServiceClient(
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
    client = DataplexServiceAsyncClient(
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
    client = DataplexServiceClient(
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
    client = DataplexServiceAsyncClient(
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
    client = DataplexServiceClient(
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
    client = DataplexServiceAsyncClient(
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
    client = DataplexServiceClient(
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
    client = DataplexServiceAsyncClient(
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
    client = DataplexServiceClient(
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
    client = DataplexServiceAsyncClient(
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
    client = DataplexServiceClient(
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
    client = DataplexServiceAsyncClient(
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
    client = DataplexServiceClient(
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
    client = DataplexServiceAsyncClient(
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
    client = DataplexServiceClient(
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
    client = DataplexServiceAsyncClient(
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
    client = DataplexServiceClient(
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
    client = DataplexServiceAsyncClient(
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
    client = DataplexServiceClient(
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
    client = DataplexServiceAsyncClient(
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
    client = DataplexServiceClient(
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
    client = DataplexServiceAsyncClient(
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
    client = DataplexServiceClient(
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
    client = DataplexServiceAsyncClient(
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
    client = DataplexServiceClient(
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
    client = DataplexServiceAsyncClient(
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
    client = DataplexServiceClient(
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
    client = DataplexServiceAsyncClient(
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
    client = DataplexServiceClient(credentials=ga_credentials.AnonymousCredentials())

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
    client = DataplexServiceAsyncClient(
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
    client = DataplexServiceClient(
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
    client = DataplexServiceAsyncClient(
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


def test_transport_close():
    transports = {
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = DataplexServiceClient(
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
        client = DataplexServiceClient(
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
        (DataplexServiceClient, transports.DataplexServiceGrpcTransport),
        (DataplexServiceAsyncClient, transports.DataplexServiceGrpcAsyncIOTransport),
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
