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
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest

from google.cloud.retail_v2alpha.services.model_service import (
    ModelServiceAsyncClient,
    ModelServiceClient,
    pagers,
    transports,
)
from google.cloud.retail_v2alpha.types import common
from google.cloud.retail_v2alpha.types import model
from google.cloud.retail_v2alpha.types import model as gcr_model
from google.cloud.retail_v2alpha.types import model_service


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

    assert ModelServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        ModelServiceClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    )
    assert (
        ModelServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        ModelServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        ModelServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert ModelServiceClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (ModelServiceClient, "grpc"),
        (ModelServiceAsyncClient, "grpc_asyncio"),
    ],
)
def test_model_service_client_from_service_account_info(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == ("retail.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.ModelServiceGrpcTransport, "grpc"),
        (transports.ModelServiceGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_model_service_client_service_account_always_use_jwt(
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
        (ModelServiceClient, "grpc"),
        (ModelServiceAsyncClient, "grpc_asyncio"),
    ],
)
def test_model_service_client_from_service_account_file(client_class, transport_name):
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

        assert client.transport._host == ("retail.googleapis.com:443")


def test_model_service_client_get_transport_class():
    transport = ModelServiceClient.get_transport_class()
    available_transports = [
        transports.ModelServiceGrpcTransport,
    ]
    assert transport in available_transports

    transport = ModelServiceClient.get_transport_class("grpc")
    assert transport == transports.ModelServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (ModelServiceClient, transports.ModelServiceGrpcTransport, "grpc"),
        (
            ModelServiceAsyncClient,
            transports.ModelServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    ModelServiceClient, "DEFAULT_ENDPOINT", modify_default_endpoint(ModelServiceClient)
)
@mock.patch.object(
    ModelServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ModelServiceAsyncClient),
)
def test_model_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(ModelServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(ModelServiceClient, "get_transport_class") as gtc:
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
        (ModelServiceClient, transports.ModelServiceGrpcTransport, "grpc", "true"),
        (
            ModelServiceAsyncClient,
            transports.ModelServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (ModelServiceClient, transports.ModelServiceGrpcTransport, "grpc", "false"),
        (
            ModelServiceAsyncClient,
            transports.ModelServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    ModelServiceClient, "DEFAULT_ENDPOINT", modify_default_endpoint(ModelServiceClient)
)
@mock.patch.object(
    ModelServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ModelServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_model_service_client_mtls_env_auto(
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


@pytest.mark.parametrize("client_class", [ModelServiceClient, ModelServiceAsyncClient])
@mock.patch.object(
    ModelServiceClient, "DEFAULT_ENDPOINT", modify_default_endpoint(ModelServiceClient)
)
@mock.patch.object(
    ModelServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ModelServiceAsyncClient),
)
def test_model_service_client_get_mtls_endpoint_and_cert_source(client_class):
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
        (ModelServiceClient, transports.ModelServiceGrpcTransport, "grpc"),
        (
            ModelServiceAsyncClient,
            transports.ModelServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_model_service_client_client_options_scopes(
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
            ModelServiceClient,
            transports.ModelServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            ModelServiceAsyncClient,
            transports.ModelServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_model_service_client_client_options_credentials_file(
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


def test_model_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.retail_v2alpha.services.model_service.transports.ModelServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = ModelServiceClient(client_options={"api_endpoint": "squid.clam.whelk"})
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
            ModelServiceClient,
            transports.ModelServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            ModelServiceAsyncClient,
            transports.ModelServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_model_service_client_create_channel_credentials_file(
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
            "retail.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="retail.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        model_service.CreateModelRequest,
        dict,
    ],
)
def test_create_model(request_type, transport: str = "grpc"):
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == model_service.CreateModelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_model_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_model), "__call__") as call:
        client.create_model()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == model_service.CreateModelRequest()


@pytest.mark.asyncio
async def test_create_model_async(
    transport: str = "grpc_asyncio", request_type=model_service.CreateModelRequest
):
    client = ModelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == model_service.CreateModelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_model_async_from_dict():
    await test_create_model_async(request_type=dict)


def test_create_model_field_headers():
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = model_service.CreateModelRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_model), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_model(request)

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
async def test_create_model_field_headers_async():
    client = ModelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = model_service.CreateModelRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_model), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_model(request)

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


def test_create_model_flattened():
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_model(
            parent="parent_value",
            model=gcr_model.Model(
                page_optimization_config=gcr_model.Model.PageOptimizationConfig(
                    page_optimization_event_type="page_optimization_event_type_value"
                )
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].model
        mock_val = gcr_model.Model(
            page_optimization_config=gcr_model.Model.PageOptimizationConfig(
                page_optimization_event_type="page_optimization_event_type_value"
            )
        )
        assert arg == mock_val


def test_create_model_flattened_error():
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_model(
            model_service.CreateModelRequest(),
            parent="parent_value",
            model=gcr_model.Model(
                page_optimization_config=gcr_model.Model.PageOptimizationConfig(
                    page_optimization_event_type="page_optimization_event_type_value"
                )
            ),
        )


@pytest.mark.asyncio
async def test_create_model_flattened_async():
    client = ModelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_model(
            parent="parent_value",
            model=gcr_model.Model(
                page_optimization_config=gcr_model.Model.PageOptimizationConfig(
                    page_optimization_event_type="page_optimization_event_type_value"
                )
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].model
        mock_val = gcr_model.Model(
            page_optimization_config=gcr_model.Model.PageOptimizationConfig(
                page_optimization_event_type="page_optimization_event_type_value"
            )
        )
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_model_flattened_error_async():
    client = ModelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_model(
            model_service.CreateModelRequest(),
            parent="parent_value",
            model=gcr_model.Model(
                page_optimization_config=gcr_model.Model.PageOptimizationConfig(
                    page_optimization_event_type="page_optimization_event_type_value"
                )
            ),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        model_service.PauseModelRequest,
        dict,
    ],
)
def test_pause_model(request_type, transport: str = "grpc"):
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.pause_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = model.Model(
            name="name_value",
            display_name="display_name_value",
            training_state=model.Model.TrainingState.PAUSED,
            serving_state=model.Model.ServingState.INACTIVE,
            type_="type__value",
            optimization_objective="optimization_objective_value",
            periodic_tuning_state=model.Model.PeriodicTuningState.PERIODIC_TUNING_DISABLED,
            tuning_operation="tuning_operation_value",
            data_state=model.Model.DataState.DATA_OK,
            filtering_option=common.RecommendationsFilteringOption.RECOMMENDATIONS_FILTERING_DISABLED,
            page_optimization_config=model.Model.PageOptimizationConfig(
                page_optimization_event_type="page_optimization_event_type_value"
            ),
        )
        response = client.pause_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == model_service.PauseModelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, model.Model)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.training_state == model.Model.TrainingState.PAUSED
    assert response.serving_state == model.Model.ServingState.INACTIVE
    assert response.type_ == "type__value"
    assert response.optimization_objective == "optimization_objective_value"
    assert (
        response.periodic_tuning_state
        == model.Model.PeriodicTuningState.PERIODIC_TUNING_DISABLED
    )
    assert response.tuning_operation == "tuning_operation_value"
    assert response.data_state == model.Model.DataState.DATA_OK
    assert (
        response.filtering_option
        == common.RecommendationsFilteringOption.RECOMMENDATIONS_FILTERING_DISABLED
    )


def test_pause_model_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.pause_model), "__call__") as call:
        client.pause_model()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == model_service.PauseModelRequest()


@pytest.mark.asyncio
async def test_pause_model_async(
    transport: str = "grpc_asyncio", request_type=model_service.PauseModelRequest
):
    client = ModelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.pause_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            model.Model(
                name="name_value",
                display_name="display_name_value",
                training_state=model.Model.TrainingState.PAUSED,
                serving_state=model.Model.ServingState.INACTIVE,
                type_="type__value",
                optimization_objective="optimization_objective_value",
                periodic_tuning_state=model.Model.PeriodicTuningState.PERIODIC_TUNING_DISABLED,
                tuning_operation="tuning_operation_value",
                data_state=model.Model.DataState.DATA_OK,
                filtering_option=common.RecommendationsFilteringOption.RECOMMENDATIONS_FILTERING_DISABLED,
            )
        )
        response = await client.pause_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == model_service.PauseModelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, model.Model)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.training_state == model.Model.TrainingState.PAUSED
    assert response.serving_state == model.Model.ServingState.INACTIVE
    assert response.type_ == "type__value"
    assert response.optimization_objective == "optimization_objective_value"
    assert (
        response.periodic_tuning_state
        == model.Model.PeriodicTuningState.PERIODIC_TUNING_DISABLED
    )
    assert response.tuning_operation == "tuning_operation_value"
    assert response.data_state == model.Model.DataState.DATA_OK
    assert (
        response.filtering_option
        == common.RecommendationsFilteringOption.RECOMMENDATIONS_FILTERING_DISABLED
    )


@pytest.mark.asyncio
async def test_pause_model_async_from_dict():
    await test_pause_model_async(request_type=dict)


def test_pause_model_field_headers():
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = model_service.PauseModelRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.pause_model), "__call__") as call:
        call.return_value = model.Model()
        client.pause_model(request)

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
async def test_pause_model_field_headers_async():
    client = ModelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = model_service.PauseModelRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.pause_model), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(model.Model())
        await client.pause_model(request)

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


def test_pause_model_flattened():
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.pause_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = model.Model()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.pause_model(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_pause_model_flattened_error():
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.pause_model(
            model_service.PauseModelRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_pause_model_flattened_async():
    client = ModelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.pause_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = model.Model()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(model.Model())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.pause_model(
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
async def test_pause_model_flattened_error_async():
    client = ModelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.pause_model(
            model_service.PauseModelRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        model_service.ResumeModelRequest,
        dict,
    ],
)
def test_resume_model(request_type, transport: str = "grpc"):
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.resume_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = model.Model(
            name="name_value",
            display_name="display_name_value",
            training_state=model.Model.TrainingState.PAUSED,
            serving_state=model.Model.ServingState.INACTIVE,
            type_="type__value",
            optimization_objective="optimization_objective_value",
            periodic_tuning_state=model.Model.PeriodicTuningState.PERIODIC_TUNING_DISABLED,
            tuning_operation="tuning_operation_value",
            data_state=model.Model.DataState.DATA_OK,
            filtering_option=common.RecommendationsFilteringOption.RECOMMENDATIONS_FILTERING_DISABLED,
            page_optimization_config=model.Model.PageOptimizationConfig(
                page_optimization_event_type="page_optimization_event_type_value"
            ),
        )
        response = client.resume_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == model_service.ResumeModelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, model.Model)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.training_state == model.Model.TrainingState.PAUSED
    assert response.serving_state == model.Model.ServingState.INACTIVE
    assert response.type_ == "type__value"
    assert response.optimization_objective == "optimization_objective_value"
    assert (
        response.periodic_tuning_state
        == model.Model.PeriodicTuningState.PERIODIC_TUNING_DISABLED
    )
    assert response.tuning_operation == "tuning_operation_value"
    assert response.data_state == model.Model.DataState.DATA_OK
    assert (
        response.filtering_option
        == common.RecommendationsFilteringOption.RECOMMENDATIONS_FILTERING_DISABLED
    )


def test_resume_model_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.resume_model), "__call__") as call:
        client.resume_model()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == model_service.ResumeModelRequest()


@pytest.mark.asyncio
async def test_resume_model_async(
    transport: str = "grpc_asyncio", request_type=model_service.ResumeModelRequest
):
    client = ModelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.resume_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            model.Model(
                name="name_value",
                display_name="display_name_value",
                training_state=model.Model.TrainingState.PAUSED,
                serving_state=model.Model.ServingState.INACTIVE,
                type_="type__value",
                optimization_objective="optimization_objective_value",
                periodic_tuning_state=model.Model.PeriodicTuningState.PERIODIC_TUNING_DISABLED,
                tuning_operation="tuning_operation_value",
                data_state=model.Model.DataState.DATA_OK,
                filtering_option=common.RecommendationsFilteringOption.RECOMMENDATIONS_FILTERING_DISABLED,
            )
        )
        response = await client.resume_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == model_service.ResumeModelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, model.Model)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.training_state == model.Model.TrainingState.PAUSED
    assert response.serving_state == model.Model.ServingState.INACTIVE
    assert response.type_ == "type__value"
    assert response.optimization_objective == "optimization_objective_value"
    assert (
        response.periodic_tuning_state
        == model.Model.PeriodicTuningState.PERIODIC_TUNING_DISABLED
    )
    assert response.tuning_operation == "tuning_operation_value"
    assert response.data_state == model.Model.DataState.DATA_OK
    assert (
        response.filtering_option
        == common.RecommendationsFilteringOption.RECOMMENDATIONS_FILTERING_DISABLED
    )


@pytest.mark.asyncio
async def test_resume_model_async_from_dict():
    await test_resume_model_async(request_type=dict)


def test_resume_model_field_headers():
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = model_service.ResumeModelRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.resume_model), "__call__") as call:
        call.return_value = model.Model()
        client.resume_model(request)

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
async def test_resume_model_field_headers_async():
    client = ModelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = model_service.ResumeModelRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.resume_model), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(model.Model())
        await client.resume_model(request)

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


def test_resume_model_flattened():
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.resume_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = model.Model()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.resume_model(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_resume_model_flattened_error():
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.resume_model(
            model_service.ResumeModelRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_resume_model_flattened_async():
    client = ModelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.resume_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = model.Model()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(model.Model())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.resume_model(
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
async def test_resume_model_flattened_error_async():
    client = ModelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.resume_model(
            model_service.ResumeModelRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        model_service.DeleteModelRequest,
        dict,
    ],
)
def test_delete_model(request_type, transport: str = "grpc"):
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == model_service.DeleteModelRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_model_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_model), "__call__") as call:
        client.delete_model()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == model_service.DeleteModelRequest()


@pytest.mark.asyncio
async def test_delete_model_async(
    transport: str = "grpc_asyncio", request_type=model_service.DeleteModelRequest
):
    client = ModelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == model_service.DeleteModelRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_model_async_from_dict():
    await test_delete_model_async(request_type=dict)


def test_delete_model_field_headers():
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = model_service.DeleteModelRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_model), "__call__") as call:
        call.return_value = None
        client.delete_model(request)

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
async def test_delete_model_field_headers_async():
    client = ModelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = model_service.DeleteModelRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_model), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_model(request)

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


def test_delete_model_flattened():
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_model(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_model_flattened_error():
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_model(
            model_service.DeleteModelRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_model_flattened_async():
    client = ModelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_model(
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
async def test_delete_model_flattened_error_async():
    client = ModelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_model(
            model_service.DeleteModelRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        model_service.ListModelsRequest,
        dict,
    ],
)
def test_list_models(request_type, transport: str = "grpc"):
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_models), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = model_service.ListModelsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_models(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == model_service.ListModelsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListModelsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_models_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_models), "__call__") as call:
        client.list_models()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == model_service.ListModelsRequest()


@pytest.mark.asyncio
async def test_list_models_async(
    transport: str = "grpc_asyncio", request_type=model_service.ListModelsRequest
):
    client = ModelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_models), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            model_service.ListModelsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_models(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == model_service.ListModelsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListModelsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_models_async_from_dict():
    await test_list_models_async(request_type=dict)


def test_list_models_field_headers():
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = model_service.ListModelsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_models), "__call__") as call:
        call.return_value = model_service.ListModelsResponse()
        client.list_models(request)

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
async def test_list_models_field_headers_async():
    client = ModelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = model_service.ListModelsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_models), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            model_service.ListModelsResponse()
        )
        await client.list_models(request)

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


def test_list_models_flattened():
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_models), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = model_service.ListModelsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_models(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_models_flattened_error():
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_models(
            model_service.ListModelsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_models_flattened_async():
    client = ModelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_models), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = model_service.ListModelsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            model_service.ListModelsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_models(
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
async def test_list_models_flattened_error_async():
    client = ModelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_models(
            model_service.ListModelsRequest(),
            parent="parent_value",
        )


def test_list_models_pager(transport_name: str = "grpc"):
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_models), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            model_service.ListModelsResponse(
                models=[
                    model.Model(),
                    model.Model(),
                    model.Model(),
                ],
                next_page_token="abc",
            ),
            model_service.ListModelsResponse(
                models=[],
                next_page_token="def",
            ),
            model_service.ListModelsResponse(
                models=[
                    model.Model(),
                ],
                next_page_token="ghi",
            ),
            model_service.ListModelsResponse(
                models=[
                    model.Model(),
                    model.Model(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_models(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, model.Model) for i in results)


def test_list_models_pages(transport_name: str = "grpc"):
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_models), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            model_service.ListModelsResponse(
                models=[
                    model.Model(),
                    model.Model(),
                    model.Model(),
                ],
                next_page_token="abc",
            ),
            model_service.ListModelsResponse(
                models=[],
                next_page_token="def",
            ),
            model_service.ListModelsResponse(
                models=[
                    model.Model(),
                ],
                next_page_token="ghi",
            ),
            model_service.ListModelsResponse(
                models=[
                    model.Model(),
                    model.Model(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_models(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_models_async_pager():
    client = ModelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_models), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            model_service.ListModelsResponse(
                models=[
                    model.Model(),
                    model.Model(),
                    model.Model(),
                ],
                next_page_token="abc",
            ),
            model_service.ListModelsResponse(
                models=[],
                next_page_token="def",
            ),
            model_service.ListModelsResponse(
                models=[
                    model.Model(),
                ],
                next_page_token="ghi",
            ),
            model_service.ListModelsResponse(
                models=[
                    model.Model(),
                    model.Model(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_models(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, model.Model) for i in responses)


@pytest.mark.asyncio
async def test_list_models_async_pages():
    client = ModelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_models), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            model_service.ListModelsResponse(
                models=[
                    model.Model(),
                    model.Model(),
                    model.Model(),
                ],
                next_page_token="abc",
            ),
            model_service.ListModelsResponse(
                models=[],
                next_page_token="def",
            ),
            model_service.ListModelsResponse(
                models=[
                    model.Model(),
                ],
                next_page_token="ghi",
            ),
            model_service.ListModelsResponse(
                models=[
                    model.Model(),
                    model.Model(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_models(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        model_service.UpdateModelRequest,
        dict,
    ],
)
def test_update_model(request_type, transport: str = "grpc"):
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcr_model.Model(
            name="name_value",
            display_name="display_name_value",
            training_state=gcr_model.Model.TrainingState.PAUSED,
            serving_state=gcr_model.Model.ServingState.INACTIVE,
            type_="type__value",
            optimization_objective="optimization_objective_value",
            periodic_tuning_state=gcr_model.Model.PeriodicTuningState.PERIODIC_TUNING_DISABLED,
            tuning_operation="tuning_operation_value",
            data_state=gcr_model.Model.DataState.DATA_OK,
            filtering_option=common.RecommendationsFilteringOption.RECOMMENDATIONS_FILTERING_DISABLED,
            page_optimization_config=gcr_model.Model.PageOptimizationConfig(
                page_optimization_event_type="page_optimization_event_type_value"
            ),
        )
        response = client.update_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == model_service.UpdateModelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcr_model.Model)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.training_state == gcr_model.Model.TrainingState.PAUSED
    assert response.serving_state == gcr_model.Model.ServingState.INACTIVE
    assert response.type_ == "type__value"
    assert response.optimization_objective == "optimization_objective_value"
    assert (
        response.periodic_tuning_state
        == gcr_model.Model.PeriodicTuningState.PERIODIC_TUNING_DISABLED
    )
    assert response.tuning_operation == "tuning_operation_value"
    assert response.data_state == gcr_model.Model.DataState.DATA_OK
    assert (
        response.filtering_option
        == common.RecommendationsFilteringOption.RECOMMENDATIONS_FILTERING_DISABLED
    )


def test_update_model_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_model), "__call__") as call:
        client.update_model()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == model_service.UpdateModelRequest()


@pytest.mark.asyncio
async def test_update_model_async(
    transport: str = "grpc_asyncio", request_type=model_service.UpdateModelRequest
):
    client = ModelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcr_model.Model(
                name="name_value",
                display_name="display_name_value",
                training_state=gcr_model.Model.TrainingState.PAUSED,
                serving_state=gcr_model.Model.ServingState.INACTIVE,
                type_="type__value",
                optimization_objective="optimization_objective_value",
                periodic_tuning_state=gcr_model.Model.PeriodicTuningState.PERIODIC_TUNING_DISABLED,
                tuning_operation="tuning_operation_value",
                data_state=gcr_model.Model.DataState.DATA_OK,
                filtering_option=common.RecommendationsFilteringOption.RECOMMENDATIONS_FILTERING_DISABLED,
            )
        )
        response = await client.update_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == model_service.UpdateModelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcr_model.Model)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.training_state == gcr_model.Model.TrainingState.PAUSED
    assert response.serving_state == gcr_model.Model.ServingState.INACTIVE
    assert response.type_ == "type__value"
    assert response.optimization_objective == "optimization_objective_value"
    assert (
        response.periodic_tuning_state
        == gcr_model.Model.PeriodicTuningState.PERIODIC_TUNING_DISABLED
    )
    assert response.tuning_operation == "tuning_operation_value"
    assert response.data_state == gcr_model.Model.DataState.DATA_OK
    assert (
        response.filtering_option
        == common.RecommendationsFilteringOption.RECOMMENDATIONS_FILTERING_DISABLED
    )


@pytest.mark.asyncio
async def test_update_model_async_from_dict():
    await test_update_model_async(request_type=dict)


def test_update_model_field_headers():
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = model_service.UpdateModelRequest()

    request.model.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_model), "__call__") as call:
        call.return_value = gcr_model.Model()
        client.update_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "model.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_model_field_headers_async():
    client = ModelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = model_service.UpdateModelRequest()

    request.model.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_model), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gcr_model.Model())
        await client.update_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "model.name=name_value",
    ) in kw["metadata"]


def test_update_model_flattened():
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcr_model.Model()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_model(
            model=gcr_model.Model(
                page_optimization_config=gcr_model.Model.PageOptimizationConfig(
                    page_optimization_event_type="page_optimization_event_type_value"
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].model
        mock_val = gcr_model.Model(
            page_optimization_config=gcr_model.Model.PageOptimizationConfig(
                page_optimization_event_type="page_optimization_event_type_value"
            )
        )
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_model_flattened_error():
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_model(
            model_service.UpdateModelRequest(),
            model=gcr_model.Model(
                page_optimization_config=gcr_model.Model.PageOptimizationConfig(
                    page_optimization_event_type="page_optimization_event_type_value"
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_model_flattened_async():
    client = ModelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcr_model.Model()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gcr_model.Model())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_model(
            model=gcr_model.Model(
                page_optimization_config=gcr_model.Model.PageOptimizationConfig(
                    page_optimization_event_type="page_optimization_event_type_value"
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].model
        mock_val = gcr_model.Model(
            page_optimization_config=gcr_model.Model.PageOptimizationConfig(
                page_optimization_event_type="page_optimization_event_type_value"
            )
        )
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_model_flattened_error_async():
    client = ModelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_model(
            model_service.UpdateModelRequest(),
            model=gcr_model.Model(
                page_optimization_config=gcr_model.Model.PageOptimizationConfig(
                    page_optimization_event_type="page_optimization_event_type_value"
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        model_service.TuneModelRequest,
        dict,
    ],
)
def test_tune_model(request_type, transport: str = "grpc"):
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.tune_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.tune_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == model_service.TuneModelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_tune_model_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.tune_model), "__call__") as call:
        client.tune_model()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == model_service.TuneModelRequest()


@pytest.mark.asyncio
async def test_tune_model_async(
    transport: str = "grpc_asyncio", request_type=model_service.TuneModelRequest
):
    client = ModelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.tune_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.tune_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == model_service.TuneModelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_tune_model_async_from_dict():
    await test_tune_model_async(request_type=dict)


def test_tune_model_field_headers():
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = model_service.TuneModelRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.tune_model), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.tune_model(request)

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
async def test_tune_model_field_headers_async():
    client = ModelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = model_service.TuneModelRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.tune_model), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.tune_model(request)

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


def test_tune_model_flattened():
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.tune_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.tune_model(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_tune_model_flattened_error():
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.tune_model(
            model_service.TuneModelRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_tune_model_flattened_async():
    client = ModelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.tune_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.tune_model(
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
async def test_tune_model_flattened_error_async():
    client = ModelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.tune_model(
            model_service.TuneModelRequest(),
            name="name_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.ModelServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ModelServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.ModelServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ModelServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.ModelServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = ModelServiceClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = ModelServiceClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.ModelServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ModelServiceClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ModelServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = ModelServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ModelServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.ModelServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ModelServiceGrpcTransport,
        transports.ModelServiceGrpcAsyncIOTransport,
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
    transport = ModelServiceClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.ModelServiceGrpcTransport,
    )


def test_model_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.ModelServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_model_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.retail_v2alpha.services.model_service.transports.ModelServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.ModelServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_model",
        "pause_model",
        "resume_model",
        "delete_model",
        "list_models",
        "update_model",
        "tune_model",
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


def test_model_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.retail_v2alpha.services.model_service.transports.ModelServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.ModelServiceTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_model_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.retail_v2alpha.services.model_service.transports.ModelServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.ModelServiceTransport()
        adc.assert_called_once()


def test_model_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        ModelServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ModelServiceGrpcTransport,
        transports.ModelServiceGrpcAsyncIOTransport,
    ],
)
def test_model_service_transport_auth_adc(transport_class):
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
        transports.ModelServiceGrpcTransport,
        transports.ModelServiceGrpcAsyncIOTransport,
    ],
)
def test_model_service_transport_auth_gdch_credentials(transport_class):
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
        (transports.ModelServiceGrpcTransport, grpc_helpers),
        (transports.ModelServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_model_service_transport_create_channel(transport_class, grpc_helpers):
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
            "retail.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="retail.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.ModelServiceGrpcTransport, transports.ModelServiceGrpcAsyncIOTransport],
)
def test_model_service_grpc_transport_client_cert_source_for_mtls(transport_class):
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
def test_model_service_host_no_port(transport_name):
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="retail.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("retail.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
    ],
)
def test_model_service_host_with_port(transport_name):
    client = ModelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="retail.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("retail.googleapis.com:8000")


def test_model_service_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.ModelServiceGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_model_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.ModelServiceGrpcAsyncIOTransport(
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
    [transports.ModelServiceGrpcTransport, transports.ModelServiceGrpcAsyncIOTransport],
)
def test_model_service_transport_channel_mtls_with_client_cert_source(transport_class):
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
    [transports.ModelServiceGrpcTransport, transports.ModelServiceGrpcAsyncIOTransport],
)
def test_model_service_transport_channel_mtls_with_adc(transport_class):
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


def test_model_service_grpc_lro_client():
    client = ModelServiceClient(
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


def test_model_service_grpc_lro_async_client():
    client = ModelServiceAsyncClient(
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


def test_catalog_path():
    project = "squid"
    location = "clam"
    catalog = "whelk"
    expected = "projects/{project}/locations/{location}/catalogs/{catalog}".format(
        project=project,
        location=location,
        catalog=catalog,
    )
    actual = ModelServiceClient.catalog_path(project, location, catalog)
    assert expected == actual


def test_parse_catalog_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "catalog": "nudibranch",
    }
    path = ModelServiceClient.catalog_path(**expected)

    # Check that the path construction is reversible.
    actual = ModelServiceClient.parse_catalog_path(path)
    assert expected == actual


def test_model_path():
    project = "cuttlefish"
    location = "mussel"
    catalog = "winkle"
    model = "nautilus"
    expected = "projects/{project}/locations/{location}/catalogs/{catalog}/models/{model}".format(
        project=project,
        location=location,
        catalog=catalog,
        model=model,
    )
    actual = ModelServiceClient.model_path(project, location, catalog, model)
    assert expected == actual


def test_parse_model_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
        "catalog": "squid",
        "model": "clam",
    }
    path = ModelServiceClient.model_path(**expected)

    # Check that the path construction is reversible.
    actual = ModelServiceClient.parse_model_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "whelk"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = ModelServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "octopus",
    }
    path = ModelServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = ModelServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "oyster"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = ModelServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nudibranch",
    }
    path = ModelServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = ModelServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "cuttlefish"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = ModelServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "mussel",
    }
    path = ModelServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = ModelServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "winkle"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = ModelServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nautilus",
    }
    path = ModelServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = ModelServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "scallop"
    location = "abalone"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = ModelServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "squid",
        "location": "clam",
    }
    path = ModelServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = ModelServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.ModelServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = ModelServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.ModelServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = ModelServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = ModelServiceAsyncClient(
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
        client = ModelServiceClient(
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
        client = ModelServiceClient(
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
        (ModelServiceClient, transports.ModelServiceGrpcTransport),
        (ModelServiceAsyncClient, transports.ModelServiceGrpcAsyncIOTransport),
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
