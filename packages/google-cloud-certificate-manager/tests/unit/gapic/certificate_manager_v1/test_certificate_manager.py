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
import mock

import grpc
from grpc.experimental import aio
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule


from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import future
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.api_core import operation
from google.api_core import operation_async  # type: ignore
from google.api_core import operations_v1
from google.api_core import path_template
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.certificate_manager_v1.services.certificate_manager import (
    CertificateManagerAsyncClient,
)
from google.cloud.certificate_manager_v1.services.certificate_manager import (
    CertificateManagerClient,
)
from google.cloud.certificate_manager_v1.services.certificate_manager import pagers
from google.cloud.certificate_manager_v1.services.certificate_manager import transports
from google.cloud.certificate_manager_v1.types import certificate_manager
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
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

    assert CertificateManagerClient._get_default_mtls_endpoint(None) is None
    assert (
        CertificateManagerClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        CertificateManagerClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        CertificateManagerClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        CertificateManagerClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        CertificateManagerClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class",
    [
        CertificateManagerClient,
        CertificateManagerAsyncClient,
    ],
)
def test_certificate_manager_client_from_service_account_info(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "certificatemanager.googleapis.com:443"


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.CertificateManagerGrpcTransport, "grpc"),
        (transports.CertificateManagerGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_certificate_manager_client_service_account_always_use_jwt(
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
    "client_class",
    [
        CertificateManagerClient,
        CertificateManagerAsyncClient,
    ],
)
def test_certificate_manager_client_from_service_account_file(client_class):
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

        assert client.transport._host == "certificatemanager.googleapis.com:443"


def test_certificate_manager_client_get_transport_class():
    transport = CertificateManagerClient.get_transport_class()
    available_transports = [
        transports.CertificateManagerGrpcTransport,
    ]
    assert transport in available_transports

    transport = CertificateManagerClient.get_transport_class("grpc")
    assert transport == transports.CertificateManagerGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (CertificateManagerClient, transports.CertificateManagerGrpcTransport, "grpc"),
        (
            CertificateManagerAsyncClient,
            transports.CertificateManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    CertificateManagerClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CertificateManagerClient),
)
@mock.patch.object(
    CertificateManagerAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CertificateManagerAsyncClient),
)
def test_certificate_manager_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(CertificateManagerClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(CertificateManagerClient, "get_transport_class") as gtc:
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
            CertificateManagerClient,
            transports.CertificateManagerGrpcTransport,
            "grpc",
            "true",
        ),
        (
            CertificateManagerAsyncClient,
            transports.CertificateManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            CertificateManagerClient,
            transports.CertificateManagerGrpcTransport,
            "grpc",
            "false",
        ),
        (
            CertificateManagerAsyncClient,
            transports.CertificateManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    CertificateManagerClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CertificateManagerClient),
)
@mock.patch.object(
    CertificateManagerAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CertificateManagerAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_certificate_manager_client_mtls_env_auto(
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
    "client_class", [CertificateManagerClient, CertificateManagerAsyncClient]
)
@mock.patch.object(
    CertificateManagerClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CertificateManagerClient),
)
@mock.patch.object(
    CertificateManagerAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CertificateManagerAsyncClient),
)
def test_certificate_manager_client_get_mtls_endpoint_and_cert_source(client_class):
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
        (CertificateManagerClient, transports.CertificateManagerGrpcTransport, "grpc"),
        (
            CertificateManagerAsyncClient,
            transports.CertificateManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_certificate_manager_client_client_options_scopes(
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
        (
            CertificateManagerClient,
            transports.CertificateManagerGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            CertificateManagerAsyncClient,
            transports.CertificateManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_certificate_manager_client_client_options_credentials_file(
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


def test_certificate_manager_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.certificate_manager_v1.services.certificate_manager.transports.CertificateManagerGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = CertificateManagerClient(
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
            CertificateManagerClient,
            transports.CertificateManagerGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            CertificateManagerAsyncClient,
            transports.CertificateManagerGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_certificate_manager_client_create_channel_credentials_file(
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
            "certificatemanager.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="certificatemanager.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.ListCertificatesRequest,
        dict,
    ],
)
def test_list_certificates(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificates), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.ListCertificatesResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_certificates(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.ListCertificatesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCertificatesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_certificates_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificates), "__call__"
    ) as call:
        client.list_certificates()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.ListCertificatesRequest()


@pytest.mark.asyncio
async def test_list_certificates_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.ListCertificatesRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificates), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.ListCertificatesResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_certificates(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.ListCertificatesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCertificatesAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_certificates_async_from_dict():
    await test_list_certificates_async(request_type=dict)


def test_list_certificates_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.ListCertificatesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificates), "__call__"
    ) as call:
        call.return_value = certificate_manager.ListCertificatesResponse()
        client.list_certificates(request)

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
async def test_list_certificates_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.ListCertificatesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificates), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.ListCertificatesResponse()
        )
        await client.list_certificates(request)

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


def test_list_certificates_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificates), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.ListCertificatesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_certificates(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_certificates_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_certificates(
            certificate_manager.ListCertificatesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_certificates_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificates), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.ListCertificatesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.ListCertificatesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_certificates(
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
async def test_list_certificates_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_certificates(
            certificate_manager.ListCertificatesRequest(),
            parent="parent_value",
        )


def test_list_certificates_pager(transport_name: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificates), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            certificate_manager.ListCertificatesResponse(
                certificates=[
                    certificate_manager.Certificate(),
                    certificate_manager.Certificate(),
                    certificate_manager.Certificate(),
                ],
                next_page_token="abc",
            ),
            certificate_manager.ListCertificatesResponse(
                certificates=[],
                next_page_token="def",
            ),
            certificate_manager.ListCertificatesResponse(
                certificates=[
                    certificate_manager.Certificate(),
                ],
                next_page_token="ghi",
            ),
            certificate_manager.ListCertificatesResponse(
                certificates=[
                    certificate_manager.Certificate(),
                    certificate_manager.Certificate(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_certificates(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, certificate_manager.Certificate) for i in results)


def test_list_certificates_pages(transport_name: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificates), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            certificate_manager.ListCertificatesResponse(
                certificates=[
                    certificate_manager.Certificate(),
                    certificate_manager.Certificate(),
                    certificate_manager.Certificate(),
                ],
                next_page_token="abc",
            ),
            certificate_manager.ListCertificatesResponse(
                certificates=[],
                next_page_token="def",
            ),
            certificate_manager.ListCertificatesResponse(
                certificates=[
                    certificate_manager.Certificate(),
                ],
                next_page_token="ghi",
            ),
            certificate_manager.ListCertificatesResponse(
                certificates=[
                    certificate_manager.Certificate(),
                    certificate_manager.Certificate(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_certificates(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_certificates_async_pager():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificates),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            certificate_manager.ListCertificatesResponse(
                certificates=[
                    certificate_manager.Certificate(),
                    certificate_manager.Certificate(),
                    certificate_manager.Certificate(),
                ],
                next_page_token="abc",
            ),
            certificate_manager.ListCertificatesResponse(
                certificates=[],
                next_page_token="def",
            ),
            certificate_manager.ListCertificatesResponse(
                certificates=[
                    certificate_manager.Certificate(),
                ],
                next_page_token="ghi",
            ),
            certificate_manager.ListCertificatesResponse(
                certificates=[
                    certificate_manager.Certificate(),
                    certificate_manager.Certificate(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_certificates(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, certificate_manager.Certificate) for i in responses)


@pytest.mark.asyncio
async def test_list_certificates_async_pages():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificates),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            certificate_manager.ListCertificatesResponse(
                certificates=[
                    certificate_manager.Certificate(),
                    certificate_manager.Certificate(),
                    certificate_manager.Certificate(),
                ],
                next_page_token="abc",
            ),
            certificate_manager.ListCertificatesResponse(
                certificates=[],
                next_page_token="def",
            ),
            certificate_manager.ListCertificatesResponse(
                certificates=[
                    certificate_manager.Certificate(),
                ],
                next_page_token="ghi",
            ),
            certificate_manager.ListCertificatesResponse(
                certificates=[
                    certificate_manager.Certificate(),
                    certificate_manager.Certificate(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_certificates(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.GetCertificateRequest,
        dict,
    ],
)
def test_get_certificate(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_certificate), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.Certificate(
            name="name_value",
            description="description_value",
            san_dnsnames=["san_dnsnames_value"],
            pem_certificate="pem_certificate_value",
            scope=certificate_manager.Certificate.Scope.EDGE_CACHE,
            self_managed=certificate_manager.Certificate.SelfManagedCertificate(
                pem_certificate="pem_certificate_value"
            ),
        )
        response = client.get_certificate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.GetCertificateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, certificate_manager.Certificate)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.san_dnsnames == ["san_dnsnames_value"]
    assert response.pem_certificate == "pem_certificate_value"
    assert response.scope == certificate_manager.Certificate.Scope.EDGE_CACHE


def test_get_certificate_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_certificate), "__call__") as call:
        client.get_certificate()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.GetCertificateRequest()


@pytest.mark.asyncio
async def test_get_certificate_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.GetCertificateRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_certificate), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.Certificate(
                name="name_value",
                description="description_value",
                san_dnsnames=["san_dnsnames_value"],
                pem_certificate="pem_certificate_value",
                scope=certificate_manager.Certificate.Scope.EDGE_CACHE,
            )
        )
        response = await client.get_certificate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.GetCertificateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, certificate_manager.Certificate)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.san_dnsnames == ["san_dnsnames_value"]
    assert response.pem_certificate == "pem_certificate_value"
    assert response.scope == certificate_manager.Certificate.Scope.EDGE_CACHE


@pytest.mark.asyncio
async def test_get_certificate_async_from_dict():
    await test_get_certificate_async(request_type=dict)


def test_get_certificate_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.GetCertificateRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_certificate), "__call__") as call:
        call.return_value = certificate_manager.Certificate()
        client.get_certificate(request)

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
async def test_get_certificate_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.GetCertificateRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_certificate), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.Certificate()
        )
        await client.get_certificate(request)

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


def test_get_certificate_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_certificate), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.Certificate()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_certificate(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_certificate_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_certificate(
            certificate_manager.GetCertificateRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_certificate_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_certificate), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.Certificate()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.Certificate()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_certificate(
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
async def test_get_certificate_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_certificate(
            certificate_manager.GetCertificateRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.CreateCertificateRequest,
        dict,
    ],
)
def test_create_certificate(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_certificate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.CreateCertificateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_certificate_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate), "__call__"
    ) as call:
        client.create_certificate()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.CreateCertificateRequest()


@pytest.mark.asyncio
async def test_create_certificate_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.CreateCertificateRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_certificate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.CreateCertificateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_certificate_async_from_dict():
    await test_create_certificate_async(request_type=dict)


def test_create_certificate_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.CreateCertificateRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_certificate(request)

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
async def test_create_certificate_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.CreateCertificateRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_certificate(request)

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


def test_create_certificate_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_certificate(
            parent="parent_value",
            certificate=certificate_manager.Certificate(name="name_value"),
            certificate_id="certificate_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].certificate
        mock_val = certificate_manager.Certificate(name="name_value")
        assert arg == mock_val
        arg = args[0].certificate_id
        mock_val = "certificate_id_value"
        assert arg == mock_val


def test_create_certificate_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_certificate(
            certificate_manager.CreateCertificateRequest(),
            parent="parent_value",
            certificate=certificate_manager.Certificate(name="name_value"),
            certificate_id="certificate_id_value",
        )


@pytest.mark.asyncio
async def test_create_certificate_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_certificate(
            parent="parent_value",
            certificate=certificate_manager.Certificate(name="name_value"),
            certificate_id="certificate_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].certificate
        mock_val = certificate_manager.Certificate(name="name_value")
        assert arg == mock_val
        arg = args[0].certificate_id
        mock_val = "certificate_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_certificate_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_certificate(
            certificate_manager.CreateCertificateRequest(),
            parent="parent_value",
            certificate=certificate_manager.Certificate(name="name_value"),
            certificate_id="certificate_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.UpdateCertificateRequest,
        dict,
    ],
)
def test_update_certificate(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_certificate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.UpdateCertificateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_certificate_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate), "__call__"
    ) as call:
        client.update_certificate()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.UpdateCertificateRequest()


@pytest.mark.asyncio
async def test_update_certificate_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.UpdateCertificateRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_certificate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.UpdateCertificateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_certificate_async_from_dict():
    await test_update_certificate_async(request_type=dict)


def test_update_certificate_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.UpdateCertificateRequest()

    request.certificate.name = "certificate.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_certificate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "certificate.name=certificate.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_certificate_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.UpdateCertificateRequest()

    request.certificate.name = "certificate.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_certificate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "certificate.name=certificate.name/value",
    ) in kw["metadata"]


def test_update_certificate_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_certificate(
            certificate=certificate_manager.Certificate(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].certificate
        mock_val = certificate_manager.Certificate(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_certificate_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_certificate(
            certificate_manager.UpdateCertificateRequest(),
            certificate=certificate_manager.Certificate(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_certificate_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_certificate(
            certificate=certificate_manager.Certificate(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].certificate
        mock_val = certificate_manager.Certificate(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_certificate_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_certificate(
            certificate_manager.UpdateCertificateRequest(),
            certificate=certificate_manager.Certificate(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.DeleteCertificateRequest,
        dict,
    ],
)
def test_delete_certificate(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_certificate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.DeleteCertificateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_certificate_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate), "__call__"
    ) as call:
        client.delete_certificate()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.DeleteCertificateRequest()


@pytest.mark.asyncio
async def test_delete_certificate_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.DeleteCertificateRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_certificate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.DeleteCertificateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_certificate_async_from_dict():
    await test_delete_certificate_async(request_type=dict)


def test_delete_certificate_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.DeleteCertificateRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_certificate(request)

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
async def test_delete_certificate_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.DeleteCertificateRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_certificate(request)

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


def test_delete_certificate_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_certificate(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_certificate_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_certificate(
            certificate_manager.DeleteCertificateRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_certificate_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_certificate(
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
async def test_delete_certificate_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_certificate(
            certificate_manager.DeleteCertificateRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.ListCertificateMapsRequest,
        dict,
    ],
)
def test_list_certificate_maps(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_maps), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.ListCertificateMapsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_certificate_maps(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.ListCertificateMapsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCertificateMapsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_certificate_maps_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_maps), "__call__"
    ) as call:
        client.list_certificate_maps()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.ListCertificateMapsRequest()


@pytest.mark.asyncio
async def test_list_certificate_maps_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.ListCertificateMapsRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_maps), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.ListCertificateMapsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_certificate_maps(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.ListCertificateMapsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCertificateMapsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_certificate_maps_async_from_dict():
    await test_list_certificate_maps_async(request_type=dict)


def test_list_certificate_maps_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.ListCertificateMapsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_maps), "__call__"
    ) as call:
        call.return_value = certificate_manager.ListCertificateMapsResponse()
        client.list_certificate_maps(request)

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
async def test_list_certificate_maps_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.ListCertificateMapsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_maps), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.ListCertificateMapsResponse()
        )
        await client.list_certificate_maps(request)

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


def test_list_certificate_maps_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_maps), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.ListCertificateMapsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_certificate_maps(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_certificate_maps_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_certificate_maps(
            certificate_manager.ListCertificateMapsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_certificate_maps_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_maps), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.ListCertificateMapsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.ListCertificateMapsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_certificate_maps(
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
async def test_list_certificate_maps_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_certificate_maps(
            certificate_manager.ListCertificateMapsRequest(),
            parent="parent_value",
        )


def test_list_certificate_maps_pager(transport_name: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_maps), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            certificate_manager.ListCertificateMapsResponse(
                certificate_maps=[
                    certificate_manager.CertificateMap(),
                    certificate_manager.CertificateMap(),
                    certificate_manager.CertificateMap(),
                ],
                next_page_token="abc",
            ),
            certificate_manager.ListCertificateMapsResponse(
                certificate_maps=[],
                next_page_token="def",
            ),
            certificate_manager.ListCertificateMapsResponse(
                certificate_maps=[
                    certificate_manager.CertificateMap(),
                ],
                next_page_token="ghi",
            ),
            certificate_manager.ListCertificateMapsResponse(
                certificate_maps=[
                    certificate_manager.CertificateMap(),
                    certificate_manager.CertificateMap(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_certificate_maps(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, certificate_manager.CertificateMap) for i in results)


def test_list_certificate_maps_pages(transport_name: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_maps), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            certificate_manager.ListCertificateMapsResponse(
                certificate_maps=[
                    certificate_manager.CertificateMap(),
                    certificate_manager.CertificateMap(),
                    certificate_manager.CertificateMap(),
                ],
                next_page_token="abc",
            ),
            certificate_manager.ListCertificateMapsResponse(
                certificate_maps=[],
                next_page_token="def",
            ),
            certificate_manager.ListCertificateMapsResponse(
                certificate_maps=[
                    certificate_manager.CertificateMap(),
                ],
                next_page_token="ghi",
            ),
            certificate_manager.ListCertificateMapsResponse(
                certificate_maps=[
                    certificate_manager.CertificateMap(),
                    certificate_manager.CertificateMap(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_certificate_maps(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_certificate_maps_async_pager():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_maps),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            certificate_manager.ListCertificateMapsResponse(
                certificate_maps=[
                    certificate_manager.CertificateMap(),
                    certificate_manager.CertificateMap(),
                    certificate_manager.CertificateMap(),
                ],
                next_page_token="abc",
            ),
            certificate_manager.ListCertificateMapsResponse(
                certificate_maps=[],
                next_page_token="def",
            ),
            certificate_manager.ListCertificateMapsResponse(
                certificate_maps=[
                    certificate_manager.CertificateMap(),
                ],
                next_page_token="ghi",
            ),
            certificate_manager.ListCertificateMapsResponse(
                certificate_maps=[
                    certificate_manager.CertificateMap(),
                    certificate_manager.CertificateMap(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_certificate_maps(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, certificate_manager.CertificateMap) for i in responses)


@pytest.mark.asyncio
async def test_list_certificate_maps_async_pages():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_maps),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            certificate_manager.ListCertificateMapsResponse(
                certificate_maps=[
                    certificate_manager.CertificateMap(),
                    certificate_manager.CertificateMap(),
                    certificate_manager.CertificateMap(),
                ],
                next_page_token="abc",
            ),
            certificate_manager.ListCertificateMapsResponse(
                certificate_maps=[],
                next_page_token="def",
            ),
            certificate_manager.ListCertificateMapsResponse(
                certificate_maps=[
                    certificate_manager.CertificateMap(),
                ],
                next_page_token="ghi",
            ),
            certificate_manager.ListCertificateMapsResponse(
                certificate_maps=[
                    certificate_manager.CertificateMap(),
                    certificate_manager.CertificateMap(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_certificate_maps(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.GetCertificateMapRequest,
        dict,
    ],
)
def test_get_certificate_map(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_map), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.CertificateMap(
            name="name_value",
            description="description_value",
        )
        response = client.get_certificate_map(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.GetCertificateMapRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, certificate_manager.CertificateMap)
    assert response.name == "name_value"
    assert response.description == "description_value"


def test_get_certificate_map_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_map), "__call__"
    ) as call:
        client.get_certificate_map()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.GetCertificateMapRequest()


@pytest.mark.asyncio
async def test_get_certificate_map_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.GetCertificateMapRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_map), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.CertificateMap(
                name="name_value",
                description="description_value",
            )
        )
        response = await client.get_certificate_map(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.GetCertificateMapRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, certificate_manager.CertificateMap)
    assert response.name == "name_value"
    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_get_certificate_map_async_from_dict():
    await test_get_certificate_map_async(request_type=dict)


def test_get_certificate_map_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.GetCertificateMapRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_map), "__call__"
    ) as call:
        call.return_value = certificate_manager.CertificateMap()
        client.get_certificate_map(request)

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
async def test_get_certificate_map_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.GetCertificateMapRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_map), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.CertificateMap()
        )
        await client.get_certificate_map(request)

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


def test_get_certificate_map_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_map), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.CertificateMap()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_certificate_map(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_certificate_map_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_certificate_map(
            certificate_manager.GetCertificateMapRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_certificate_map_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_map), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.CertificateMap()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.CertificateMap()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_certificate_map(
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
async def test_get_certificate_map_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_certificate_map(
            certificate_manager.GetCertificateMapRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.CreateCertificateMapRequest,
        dict,
    ],
)
def test_create_certificate_map(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_map), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_certificate_map(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.CreateCertificateMapRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_certificate_map_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_map), "__call__"
    ) as call:
        client.create_certificate_map()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.CreateCertificateMapRequest()


@pytest.mark.asyncio
async def test_create_certificate_map_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.CreateCertificateMapRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_map), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_certificate_map(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.CreateCertificateMapRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_certificate_map_async_from_dict():
    await test_create_certificate_map_async(request_type=dict)


def test_create_certificate_map_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.CreateCertificateMapRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_map), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_certificate_map(request)

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
async def test_create_certificate_map_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.CreateCertificateMapRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_map), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_certificate_map(request)

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


def test_create_certificate_map_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_map), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_certificate_map(
            parent="parent_value",
            certificate_map=certificate_manager.CertificateMap(name="name_value"),
            certificate_map_id="certificate_map_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].certificate_map
        mock_val = certificate_manager.CertificateMap(name="name_value")
        assert arg == mock_val
        arg = args[0].certificate_map_id
        mock_val = "certificate_map_id_value"
        assert arg == mock_val


def test_create_certificate_map_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_certificate_map(
            certificate_manager.CreateCertificateMapRequest(),
            parent="parent_value",
            certificate_map=certificate_manager.CertificateMap(name="name_value"),
            certificate_map_id="certificate_map_id_value",
        )


@pytest.mark.asyncio
async def test_create_certificate_map_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_map), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_certificate_map(
            parent="parent_value",
            certificate_map=certificate_manager.CertificateMap(name="name_value"),
            certificate_map_id="certificate_map_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].certificate_map
        mock_val = certificate_manager.CertificateMap(name="name_value")
        assert arg == mock_val
        arg = args[0].certificate_map_id
        mock_val = "certificate_map_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_certificate_map_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_certificate_map(
            certificate_manager.CreateCertificateMapRequest(),
            parent="parent_value",
            certificate_map=certificate_manager.CertificateMap(name="name_value"),
            certificate_map_id="certificate_map_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.UpdateCertificateMapRequest,
        dict,
    ],
)
def test_update_certificate_map(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_map), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_certificate_map(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.UpdateCertificateMapRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_certificate_map_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_map), "__call__"
    ) as call:
        client.update_certificate_map()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.UpdateCertificateMapRequest()


@pytest.mark.asyncio
async def test_update_certificate_map_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.UpdateCertificateMapRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_map), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_certificate_map(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.UpdateCertificateMapRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_certificate_map_async_from_dict():
    await test_update_certificate_map_async(request_type=dict)


def test_update_certificate_map_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.UpdateCertificateMapRequest()

    request.certificate_map.name = "certificate_map.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_map), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_certificate_map(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "certificate_map.name=certificate_map.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_certificate_map_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.UpdateCertificateMapRequest()

    request.certificate_map.name = "certificate_map.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_map), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_certificate_map(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "certificate_map.name=certificate_map.name/value",
    ) in kw["metadata"]


def test_update_certificate_map_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_map), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_certificate_map(
            certificate_map=certificate_manager.CertificateMap(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].certificate_map
        mock_val = certificate_manager.CertificateMap(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_certificate_map_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_certificate_map(
            certificate_manager.UpdateCertificateMapRequest(),
            certificate_map=certificate_manager.CertificateMap(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_certificate_map_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_map), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_certificate_map(
            certificate_map=certificate_manager.CertificateMap(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].certificate_map
        mock_val = certificate_manager.CertificateMap(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_certificate_map_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_certificate_map(
            certificate_manager.UpdateCertificateMapRequest(),
            certificate_map=certificate_manager.CertificateMap(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.DeleteCertificateMapRequest,
        dict,
    ],
)
def test_delete_certificate_map(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_map), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_certificate_map(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.DeleteCertificateMapRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_certificate_map_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_map), "__call__"
    ) as call:
        client.delete_certificate_map()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.DeleteCertificateMapRequest()


@pytest.mark.asyncio
async def test_delete_certificate_map_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.DeleteCertificateMapRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_map), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_certificate_map(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.DeleteCertificateMapRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_certificate_map_async_from_dict():
    await test_delete_certificate_map_async(request_type=dict)


def test_delete_certificate_map_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.DeleteCertificateMapRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_map), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_certificate_map(request)

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
async def test_delete_certificate_map_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.DeleteCertificateMapRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_map), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_certificate_map(request)

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


def test_delete_certificate_map_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_map), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_certificate_map(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_certificate_map_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_certificate_map(
            certificate_manager.DeleteCertificateMapRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_certificate_map_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_map), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_certificate_map(
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
async def test_delete_certificate_map_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_certificate_map(
            certificate_manager.DeleteCertificateMapRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.ListCertificateMapEntriesRequest,
        dict,
    ],
)
def test_list_certificate_map_entries(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_map_entries), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.ListCertificateMapEntriesResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_certificate_map_entries(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.ListCertificateMapEntriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCertificateMapEntriesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_certificate_map_entries_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_map_entries), "__call__"
    ) as call:
        client.list_certificate_map_entries()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.ListCertificateMapEntriesRequest()


@pytest.mark.asyncio
async def test_list_certificate_map_entries_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.ListCertificateMapEntriesRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_map_entries), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.ListCertificateMapEntriesResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_certificate_map_entries(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.ListCertificateMapEntriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCertificateMapEntriesAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_certificate_map_entries_async_from_dict():
    await test_list_certificate_map_entries_async(request_type=dict)


def test_list_certificate_map_entries_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.ListCertificateMapEntriesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_map_entries), "__call__"
    ) as call:
        call.return_value = certificate_manager.ListCertificateMapEntriesResponse()
        client.list_certificate_map_entries(request)

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
async def test_list_certificate_map_entries_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.ListCertificateMapEntriesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_map_entries), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.ListCertificateMapEntriesResponse()
        )
        await client.list_certificate_map_entries(request)

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


def test_list_certificate_map_entries_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_map_entries), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.ListCertificateMapEntriesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_certificate_map_entries(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_certificate_map_entries_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_certificate_map_entries(
            certificate_manager.ListCertificateMapEntriesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_certificate_map_entries_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_map_entries), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.ListCertificateMapEntriesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.ListCertificateMapEntriesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_certificate_map_entries(
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
async def test_list_certificate_map_entries_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_certificate_map_entries(
            certificate_manager.ListCertificateMapEntriesRequest(),
            parent="parent_value",
        )


def test_list_certificate_map_entries_pager(transport_name: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_map_entries), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            certificate_manager.ListCertificateMapEntriesResponse(
                certificate_map_entries=[
                    certificate_manager.CertificateMapEntry(),
                    certificate_manager.CertificateMapEntry(),
                    certificate_manager.CertificateMapEntry(),
                ],
                next_page_token="abc",
            ),
            certificate_manager.ListCertificateMapEntriesResponse(
                certificate_map_entries=[],
                next_page_token="def",
            ),
            certificate_manager.ListCertificateMapEntriesResponse(
                certificate_map_entries=[
                    certificate_manager.CertificateMapEntry(),
                ],
                next_page_token="ghi",
            ),
            certificate_manager.ListCertificateMapEntriesResponse(
                certificate_map_entries=[
                    certificate_manager.CertificateMapEntry(),
                    certificate_manager.CertificateMapEntry(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_certificate_map_entries(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(
            isinstance(i, certificate_manager.CertificateMapEntry) for i in results
        )


def test_list_certificate_map_entries_pages(transport_name: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_map_entries), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            certificate_manager.ListCertificateMapEntriesResponse(
                certificate_map_entries=[
                    certificate_manager.CertificateMapEntry(),
                    certificate_manager.CertificateMapEntry(),
                    certificate_manager.CertificateMapEntry(),
                ],
                next_page_token="abc",
            ),
            certificate_manager.ListCertificateMapEntriesResponse(
                certificate_map_entries=[],
                next_page_token="def",
            ),
            certificate_manager.ListCertificateMapEntriesResponse(
                certificate_map_entries=[
                    certificate_manager.CertificateMapEntry(),
                ],
                next_page_token="ghi",
            ),
            certificate_manager.ListCertificateMapEntriesResponse(
                certificate_map_entries=[
                    certificate_manager.CertificateMapEntry(),
                    certificate_manager.CertificateMapEntry(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_certificate_map_entries(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_certificate_map_entries_async_pager():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_map_entries),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            certificate_manager.ListCertificateMapEntriesResponse(
                certificate_map_entries=[
                    certificate_manager.CertificateMapEntry(),
                    certificate_manager.CertificateMapEntry(),
                    certificate_manager.CertificateMapEntry(),
                ],
                next_page_token="abc",
            ),
            certificate_manager.ListCertificateMapEntriesResponse(
                certificate_map_entries=[],
                next_page_token="def",
            ),
            certificate_manager.ListCertificateMapEntriesResponse(
                certificate_map_entries=[
                    certificate_manager.CertificateMapEntry(),
                ],
                next_page_token="ghi",
            ),
            certificate_manager.ListCertificateMapEntriesResponse(
                certificate_map_entries=[
                    certificate_manager.CertificateMapEntry(),
                    certificate_manager.CertificateMapEntry(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_certificate_map_entries(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, certificate_manager.CertificateMapEntry) for i in responses
        )


@pytest.mark.asyncio
async def test_list_certificate_map_entries_async_pages():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_map_entries),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            certificate_manager.ListCertificateMapEntriesResponse(
                certificate_map_entries=[
                    certificate_manager.CertificateMapEntry(),
                    certificate_manager.CertificateMapEntry(),
                    certificate_manager.CertificateMapEntry(),
                ],
                next_page_token="abc",
            ),
            certificate_manager.ListCertificateMapEntriesResponse(
                certificate_map_entries=[],
                next_page_token="def",
            ),
            certificate_manager.ListCertificateMapEntriesResponse(
                certificate_map_entries=[
                    certificate_manager.CertificateMapEntry(),
                ],
                next_page_token="ghi",
            ),
            certificate_manager.ListCertificateMapEntriesResponse(
                certificate_map_entries=[
                    certificate_manager.CertificateMapEntry(),
                    certificate_manager.CertificateMapEntry(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_certificate_map_entries(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.GetCertificateMapEntryRequest,
        dict,
    ],
)
def test_get_certificate_map_entry(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_map_entry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.CertificateMapEntry(
            name="name_value",
            description="description_value",
            certificates=["certificates_value"],
            state=certificate_manager.ServingState.ACTIVE,
            hostname="hostname_value",
        )
        response = client.get_certificate_map_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.GetCertificateMapEntryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, certificate_manager.CertificateMapEntry)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.certificates == ["certificates_value"]
    assert response.state == certificate_manager.ServingState.ACTIVE


def test_get_certificate_map_entry_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_map_entry), "__call__"
    ) as call:
        client.get_certificate_map_entry()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.GetCertificateMapEntryRequest()


@pytest.mark.asyncio
async def test_get_certificate_map_entry_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.GetCertificateMapEntryRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_map_entry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.CertificateMapEntry(
                name="name_value",
                description="description_value",
                certificates=["certificates_value"],
                state=certificate_manager.ServingState.ACTIVE,
            )
        )
        response = await client.get_certificate_map_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.GetCertificateMapEntryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, certificate_manager.CertificateMapEntry)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.certificates == ["certificates_value"]
    assert response.state == certificate_manager.ServingState.ACTIVE


@pytest.mark.asyncio
async def test_get_certificate_map_entry_async_from_dict():
    await test_get_certificate_map_entry_async(request_type=dict)


def test_get_certificate_map_entry_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.GetCertificateMapEntryRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_map_entry), "__call__"
    ) as call:
        call.return_value = certificate_manager.CertificateMapEntry()
        client.get_certificate_map_entry(request)

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
async def test_get_certificate_map_entry_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.GetCertificateMapEntryRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_map_entry), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.CertificateMapEntry()
        )
        await client.get_certificate_map_entry(request)

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


def test_get_certificate_map_entry_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_map_entry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.CertificateMapEntry()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_certificate_map_entry(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_certificate_map_entry_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_certificate_map_entry(
            certificate_manager.GetCertificateMapEntryRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_certificate_map_entry_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_map_entry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.CertificateMapEntry()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.CertificateMapEntry()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_certificate_map_entry(
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
async def test_get_certificate_map_entry_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_certificate_map_entry(
            certificate_manager.GetCertificateMapEntryRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.CreateCertificateMapEntryRequest,
        dict,
    ],
)
def test_create_certificate_map_entry(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_map_entry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_certificate_map_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.CreateCertificateMapEntryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_certificate_map_entry_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_map_entry), "__call__"
    ) as call:
        client.create_certificate_map_entry()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.CreateCertificateMapEntryRequest()


@pytest.mark.asyncio
async def test_create_certificate_map_entry_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.CreateCertificateMapEntryRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_map_entry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_certificate_map_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.CreateCertificateMapEntryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_certificate_map_entry_async_from_dict():
    await test_create_certificate_map_entry_async(request_type=dict)


def test_create_certificate_map_entry_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.CreateCertificateMapEntryRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_map_entry), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_certificate_map_entry(request)

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
async def test_create_certificate_map_entry_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.CreateCertificateMapEntryRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_map_entry), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_certificate_map_entry(request)

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


def test_create_certificate_map_entry_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_map_entry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_certificate_map_entry(
            parent="parent_value",
            certificate_map_entry=certificate_manager.CertificateMapEntry(
                name="name_value"
            ),
            certificate_map_entry_id="certificate_map_entry_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].certificate_map_entry
        mock_val = certificate_manager.CertificateMapEntry(name="name_value")
        assert arg == mock_val
        arg = args[0].certificate_map_entry_id
        mock_val = "certificate_map_entry_id_value"
        assert arg == mock_val


def test_create_certificate_map_entry_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_certificate_map_entry(
            certificate_manager.CreateCertificateMapEntryRequest(),
            parent="parent_value",
            certificate_map_entry=certificate_manager.CertificateMapEntry(
                name="name_value"
            ),
            certificate_map_entry_id="certificate_map_entry_id_value",
        )


@pytest.mark.asyncio
async def test_create_certificate_map_entry_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_map_entry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_certificate_map_entry(
            parent="parent_value",
            certificate_map_entry=certificate_manager.CertificateMapEntry(
                name="name_value"
            ),
            certificate_map_entry_id="certificate_map_entry_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].certificate_map_entry
        mock_val = certificate_manager.CertificateMapEntry(name="name_value")
        assert arg == mock_val
        arg = args[0].certificate_map_entry_id
        mock_val = "certificate_map_entry_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_certificate_map_entry_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_certificate_map_entry(
            certificate_manager.CreateCertificateMapEntryRequest(),
            parent="parent_value",
            certificate_map_entry=certificate_manager.CertificateMapEntry(
                name="name_value"
            ),
            certificate_map_entry_id="certificate_map_entry_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.UpdateCertificateMapEntryRequest,
        dict,
    ],
)
def test_update_certificate_map_entry(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_map_entry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_certificate_map_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.UpdateCertificateMapEntryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_certificate_map_entry_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_map_entry), "__call__"
    ) as call:
        client.update_certificate_map_entry()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.UpdateCertificateMapEntryRequest()


@pytest.mark.asyncio
async def test_update_certificate_map_entry_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.UpdateCertificateMapEntryRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_map_entry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_certificate_map_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.UpdateCertificateMapEntryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_certificate_map_entry_async_from_dict():
    await test_update_certificate_map_entry_async(request_type=dict)


def test_update_certificate_map_entry_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.UpdateCertificateMapEntryRequest()

    request.certificate_map_entry.name = "certificate_map_entry.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_map_entry), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_certificate_map_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "certificate_map_entry.name=certificate_map_entry.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_certificate_map_entry_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.UpdateCertificateMapEntryRequest()

    request.certificate_map_entry.name = "certificate_map_entry.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_map_entry), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_certificate_map_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "certificate_map_entry.name=certificate_map_entry.name/value",
    ) in kw["metadata"]


def test_update_certificate_map_entry_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_map_entry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_certificate_map_entry(
            certificate_map_entry=certificate_manager.CertificateMapEntry(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].certificate_map_entry
        mock_val = certificate_manager.CertificateMapEntry(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_certificate_map_entry_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_certificate_map_entry(
            certificate_manager.UpdateCertificateMapEntryRequest(),
            certificate_map_entry=certificate_manager.CertificateMapEntry(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_certificate_map_entry_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_map_entry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_certificate_map_entry(
            certificate_map_entry=certificate_manager.CertificateMapEntry(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].certificate_map_entry
        mock_val = certificate_manager.CertificateMapEntry(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_certificate_map_entry_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_certificate_map_entry(
            certificate_manager.UpdateCertificateMapEntryRequest(),
            certificate_map_entry=certificate_manager.CertificateMapEntry(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.DeleteCertificateMapEntryRequest,
        dict,
    ],
)
def test_delete_certificate_map_entry(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_map_entry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_certificate_map_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.DeleteCertificateMapEntryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_certificate_map_entry_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_map_entry), "__call__"
    ) as call:
        client.delete_certificate_map_entry()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.DeleteCertificateMapEntryRequest()


@pytest.mark.asyncio
async def test_delete_certificate_map_entry_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.DeleteCertificateMapEntryRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_map_entry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_certificate_map_entry(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.DeleteCertificateMapEntryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_certificate_map_entry_async_from_dict():
    await test_delete_certificate_map_entry_async(request_type=dict)


def test_delete_certificate_map_entry_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.DeleteCertificateMapEntryRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_map_entry), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_certificate_map_entry(request)

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
async def test_delete_certificate_map_entry_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.DeleteCertificateMapEntryRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_map_entry), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_certificate_map_entry(request)

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


def test_delete_certificate_map_entry_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_map_entry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_certificate_map_entry(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_certificate_map_entry_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_certificate_map_entry(
            certificate_manager.DeleteCertificateMapEntryRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_certificate_map_entry_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_map_entry), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_certificate_map_entry(
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
async def test_delete_certificate_map_entry_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_certificate_map_entry(
            certificate_manager.DeleteCertificateMapEntryRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.ListDnsAuthorizationsRequest,
        dict,
    ],
)
def test_list_dns_authorizations(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_dns_authorizations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.ListDnsAuthorizationsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_dns_authorizations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.ListDnsAuthorizationsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDnsAuthorizationsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_dns_authorizations_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_dns_authorizations), "__call__"
    ) as call:
        client.list_dns_authorizations()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.ListDnsAuthorizationsRequest()


@pytest.mark.asyncio
async def test_list_dns_authorizations_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.ListDnsAuthorizationsRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_dns_authorizations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.ListDnsAuthorizationsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_dns_authorizations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.ListDnsAuthorizationsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDnsAuthorizationsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_dns_authorizations_async_from_dict():
    await test_list_dns_authorizations_async(request_type=dict)


def test_list_dns_authorizations_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.ListDnsAuthorizationsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_dns_authorizations), "__call__"
    ) as call:
        call.return_value = certificate_manager.ListDnsAuthorizationsResponse()
        client.list_dns_authorizations(request)

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
async def test_list_dns_authorizations_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.ListDnsAuthorizationsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_dns_authorizations), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.ListDnsAuthorizationsResponse()
        )
        await client.list_dns_authorizations(request)

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


def test_list_dns_authorizations_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_dns_authorizations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.ListDnsAuthorizationsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_dns_authorizations(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_dns_authorizations_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_dns_authorizations(
            certificate_manager.ListDnsAuthorizationsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_dns_authorizations_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_dns_authorizations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.ListDnsAuthorizationsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.ListDnsAuthorizationsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_dns_authorizations(
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
async def test_list_dns_authorizations_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_dns_authorizations(
            certificate_manager.ListDnsAuthorizationsRequest(),
            parent="parent_value",
        )


def test_list_dns_authorizations_pager(transport_name: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_dns_authorizations), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            certificate_manager.ListDnsAuthorizationsResponse(
                dns_authorizations=[
                    certificate_manager.DnsAuthorization(),
                    certificate_manager.DnsAuthorization(),
                    certificate_manager.DnsAuthorization(),
                ],
                next_page_token="abc",
            ),
            certificate_manager.ListDnsAuthorizationsResponse(
                dns_authorizations=[],
                next_page_token="def",
            ),
            certificate_manager.ListDnsAuthorizationsResponse(
                dns_authorizations=[
                    certificate_manager.DnsAuthorization(),
                ],
                next_page_token="ghi",
            ),
            certificate_manager.ListDnsAuthorizationsResponse(
                dns_authorizations=[
                    certificate_manager.DnsAuthorization(),
                    certificate_manager.DnsAuthorization(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_dns_authorizations(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, certificate_manager.DnsAuthorization) for i in results)


def test_list_dns_authorizations_pages(transport_name: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_dns_authorizations), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            certificate_manager.ListDnsAuthorizationsResponse(
                dns_authorizations=[
                    certificate_manager.DnsAuthorization(),
                    certificate_manager.DnsAuthorization(),
                    certificate_manager.DnsAuthorization(),
                ],
                next_page_token="abc",
            ),
            certificate_manager.ListDnsAuthorizationsResponse(
                dns_authorizations=[],
                next_page_token="def",
            ),
            certificate_manager.ListDnsAuthorizationsResponse(
                dns_authorizations=[
                    certificate_manager.DnsAuthorization(),
                ],
                next_page_token="ghi",
            ),
            certificate_manager.ListDnsAuthorizationsResponse(
                dns_authorizations=[
                    certificate_manager.DnsAuthorization(),
                    certificate_manager.DnsAuthorization(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_dns_authorizations(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_dns_authorizations_async_pager():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_dns_authorizations),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            certificate_manager.ListDnsAuthorizationsResponse(
                dns_authorizations=[
                    certificate_manager.DnsAuthorization(),
                    certificate_manager.DnsAuthorization(),
                    certificate_manager.DnsAuthorization(),
                ],
                next_page_token="abc",
            ),
            certificate_manager.ListDnsAuthorizationsResponse(
                dns_authorizations=[],
                next_page_token="def",
            ),
            certificate_manager.ListDnsAuthorizationsResponse(
                dns_authorizations=[
                    certificate_manager.DnsAuthorization(),
                ],
                next_page_token="ghi",
            ),
            certificate_manager.ListDnsAuthorizationsResponse(
                dns_authorizations=[
                    certificate_manager.DnsAuthorization(),
                    certificate_manager.DnsAuthorization(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_dns_authorizations(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, certificate_manager.DnsAuthorization) for i in responses
        )


@pytest.mark.asyncio
async def test_list_dns_authorizations_async_pages():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_dns_authorizations),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            certificate_manager.ListDnsAuthorizationsResponse(
                dns_authorizations=[
                    certificate_manager.DnsAuthorization(),
                    certificate_manager.DnsAuthorization(),
                    certificate_manager.DnsAuthorization(),
                ],
                next_page_token="abc",
            ),
            certificate_manager.ListDnsAuthorizationsResponse(
                dns_authorizations=[],
                next_page_token="def",
            ),
            certificate_manager.ListDnsAuthorizationsResponse(
                dns_authorizations=[
                    certificate_manager.DnsAuthorization(),
                ],
                next_page_token="ghi",
            ),
            certificate_manager.ListDnsAuthorizationsResponse(
                dns_authorizations=[
                    certificate_manager.DnsAuthorization(),
                    certificate_manager.DnsAuthorization(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_dns_authorizations(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.GetDnsAuthorizationRequest,
        dict,
    ],
)
def test_get_dns_authorization(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_dns_authorization), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.DnsAuthorization(
            name="name_value",
            description="description_value",
            domain="domain_value",
        )
        response = client.get_dns_authorization(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.GetDnsAuthorizationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, certificate_manager.DnsAuthorization)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.domain == "domain_value"


def test_get_dns_authorization_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_dns_authorization), "__call__"
    ) as call:
        client.get_dns_authorization()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.GetDnsAuthorizationRequest()


@pytest.mark.asyncio
async def test_get_dns_authorization_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.GetDnsAuthorizationRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_dns_authorization), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.DnsAuthorization(
                name="name_value",
                description="description_value",
                domain="domain_value",
            )
        )
        response = await client.get_dns_authorization(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.GetDnsAuthorizationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, certificate_manager.DnsAuthorization)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.domain == "domain_value"


@pytest.mark.asyncio
async def test_get_dns_authorization_async_from_dict():
    await test_get_dns_authorization_async(request_type=dict)


def test_get_dns_authorization_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.GetDnsAuthorizationRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_dns_authorization), "__call__"
    ) as call:
        call.return_value = certificate_manager.DnsAuthorization()
        client.get_dns_authorization(request)

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
async def test_get_dns_authorization_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.GetDnsAuthorizationRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_dns_authorization), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.DnsAuthorization()
        )
        await client.get_dns_authorization(request)

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


def test_get_dns_authorization_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_dns_authorization), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.DnsAuthorization()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_dns_authorization(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_dns_authorization_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_dns_authorization(
            certificate_manager.GetDnsAuthorizationRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_dns_authorization_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_dns_authorization), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = certificate_manager.DnsAuthorization()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            certificate_manager.DnsAuthorization()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_dns_authorization(
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
async def test_get_dns_authorization_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_dns_authorization(
            certificate_manager.GetDnsAuthorizationRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.CreateDnsAuthorizationRequest,
        dict,
    ],
)
def test_create_dns_authorization(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_dns_authorization), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_dns_authorization(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.CreateDnsAuthorizationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_dns_authorization_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_dns_authorization), "__call__"
    ) as call:
        client.create_dns_authorization()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.CreateDnsAuthorizationRequest()


@pytest.mark.asyncio
async def test_create_dns_authorization_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.CreateDnsAuthorizationRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_dns_authorization), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_dns_authorization(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.CreateDnsAuthorizationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_dns_authorization_async_from_dict():
    await test_create_dns_authorization_async(request_type=dict)


def test_create_dns_authorization_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.CreateDnsAuthorizationRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_dns_authorization), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_dns_authorization(request)

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
async def test_create_dns_authorization_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.CreateDnsAuthorizationRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_dns_authorization), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_dns_authorization(request)

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


def test_create_dns_authorization_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_dns_authorization), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_dns_authorization(
            parent="parent_value",
            dns_authorization=certificate_manager.DnsAuthorization(name="name_value"),
            dns_authorization_id="dns_authorization_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].dns_authorization
        mock_val = certificate_manager.DnsAuthorization(name="name_value")
        assert arg == mock_val
        arg = args[0].dns_authorization_id
        mock_val = "dns_authorization_id_value"
        assert arg == mock_val


def test_create_dns_authorization_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_dns_authorization(
            certificate_manager.CreateDnsAuthorizationRequest(),
            parent="parent_value",
            dns_authorization=certificate_manager.DnsAuthorization(name="name_value"),
            dns_authorization_id="dns_authorization_id_value",
        )


@pytest.mark.asyncio
async def test_create_dns_authorization_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_dns_authorization), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_dns_authorization(
            parent="parent_value",
            dns_authorization=certificate_manager.DnsAuthorization(name="name_value"),
            dns_authorization_id="dns_authorization_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].dns_authorization
        mock_val = certificate_manager.DnsAuthorization(name="name_value")
        assert arg == mock_val
        arg = args[0].dns_authorization_id
        mock_val = "dns_authorization_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_dns_authorization_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_dns_authorization(
            certificate_manager.CreateDnsAuthorizationRequest(),
            parent="parent_value",
            dns_authorization=certificate_manager.DnsAuthorization(name="name_value"),
            dns_authorization_id="dns_authorization_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.UpdateDnsAuthorizationRequest,
        dict,
    ],
)
def test_update_dns_authorization(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_dns_authorization), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_dns_authorization(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.UpdateDnsAuthorizationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_dns_authorization_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_dns_authorization), "__call__"
    ) as call:
        client.update_dns_authorization()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.UpdateDnsAuthorizationRequest()


@pytest.mark.asyncio
async def test_update_dns_authorization_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.UpdateDnsAuthorizationRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_dns_authorization), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_dns_authorization(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.UpdateDnsAuthorizationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_dns_authorization_async_from_dict():
    await test_update_dns_authorization_async(request_type=dict)


def test_update_dns_authorization_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.UpdateDnsAuthorizationRequest()

    request.dns_authorization.name = "dns_authorization.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_dns_authorization), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_dns_authorization(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "dns_authorization.name=dns_authorization.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_dns_authorization_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.UpdateDnsAuthorizationRequest()

    request.dns_authorization.name = "dns_authorization.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_dns_authorization), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_dns_authorization(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "dns_authorization.name=dns_authorization.name/value",
    ) in kw["metadata"]


def test_update_dns_authorization_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_dns_authorization), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_dns_authorization(
            dns_authorization=certificate_manager.DnsAuthorization(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].dns_authorization
        mock_val = certificate_manager.DnsAuthorization(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_dns_authorization_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_dns_authorization(
            certificate_manager.UpdateDnsAuthorizationRequest(),
            dns_authorization=certificate_manager.DnsAuthorization(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_dns_authorization_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_dns_authorization), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_dns_authorization(
            dns_authorization=certificate_manager.DnsAuthorization(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].dns_authorization
        mock_val = certificate_manager.DnsAuthorization(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_dns_authorization_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_dns_authorization(
            certificate_manager.UpdateDnsAuthorizationRequest(),
            dns_authorization=certificate_manager.DnsAuthorization(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        certificate_manager.DeleteDnsAuthorizationRequest,
        dict,
    ],
)
def test_delete_dns_authorization(request_type, transport: str = "grpc"):
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_dns_authorization), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_dns_authorization(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.DeleteDnsAuthorizationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_dns_authorization_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_dns_authorization), "__call__"
    ) as call:
        client.delete_dns_authorization()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.DeleteDnsAuthorizationRequest()


@pytest.mark.asyncio
async def test_delete_dns_authorization_async(
    transport: str = "grpc_asyncio",
    request_type=certificate_manager.DeleteDnsAuthorizationRequest,
):
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_dns_authorization), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_dns_authorization(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == certificate_manager.DeleteDnsAuthorizationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_dns_authorization_async_from_dict():
    await test_delete_dns_authorization_async(request_type=dict)


def test_delete_dns_authorization_field_headers():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.DeleteDnsAuthorizationRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_dns_authorization), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_dns_authorization(request)

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
async def test_delete_dns_authorization_field_headers_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = certificate_manager.DeleteDnsAuthorizationRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_dns_authorization), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_dns_authorization(request)

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


def test_delete_dns_authorization_flattened():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_dns_authorization), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_dns_authorization(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_dns_authorization_flattened_error():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_dns_authorization(
            certificate_manager.DeleteDnsAuthorizationRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_dns_authorization_flattened_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_dns_authorization), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_dns_authorization(
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
async def test_delete_dns_authorization_flattened_error_async():
    client = CertificateManagerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_dns_authorization(
            certificate_manager.DeleteDnsAuthorizationRequest(),
            name="name_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.CertificateManagerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CertificateManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.CertificateManagerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CertificateManagerClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.CertificateManagerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = CertificateManagerClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = CertificateManagerClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.CertificateManagerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CertificateManagerClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.CertificateManagerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = CertificateManagerClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.CertificateManagerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.CertificateManagerGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CertificateManagerGrpcTransport,
        transports.CertificateManagerGrpcAsyncIOTransport,
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
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.CertificateManagerGrpcTransport,
    )


def test_certificate_manager_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.CertificateManagerTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_certificate_manager_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.certificate_manager_v1.services.certificate_manager.transports.CertificateManagerTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.CertificateManagerTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_certificates",
        "get_certificate",
        "create_certificate",
        "update_certificate",
        "delete_certificate",
        "list_certificate_maps",
        "get_certificate_map",
        "create_certificate_map",
        "update_certificate_map",
        "delete_certificate_map",
        "list_certificate_map_entries",
        "get_certificate_map_entry",
        "create_certificate_map_entry",
        "update_certificate_map_entry",
        "delete_certificate_map_entry",
        "list_dns_authorizations",
        "get_dns_authorization",
        "create_dns_authorization",
        "update_dns_authorization",
        "delete_dns_authorization",
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


def test_certificate_manager_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.certificate_manager_v1.services.certificate_manager.transports.CertificateManagerTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.CertificateManagerTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_certificate_manager_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.certificate_manager_v1.services.certificate_manager.transports.CertificateManagerTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.CertificateManagerTransport()
        adc.assert_called_once()


def test_certificate_manager_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        CertificateManagerClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CertificateManagerGrpcTransport,
        transports.CertificateManagerGrpcAsyncIOTransport,
    ],
)
def test_certificate_manager_transport_auth_adc(transport_class):
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
        (transports.CertificateManagerGrpcTransport, grpc_helpers),
        (transports.CertificateManagerGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_certificate_manager_transport_create_channel(transport_class, grpc_helpers):
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
            "certificatemanager.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="certificatemanager.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CertificateManagerGrpcTransport,
        transports.CertificateManagerGrpcAsyncIOTransport,
    ],
)
def test_certificate_manager_grpc_transport_client_cert_source_for_mtls(
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


def test_certificate_manager_host_no_port():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="certificatemanager.googleapis.com"
        ),
    )
    assert client.transport._host == "certificatemanager.googleapis.com:443"


def test_certificate_manager_host_with_port():
    client = CertificateManagerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="certificatemanager.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "certificatemanager.googleapis.com:8000"


def test_certificate_manager_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.CertificateManagerGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_certificate_manager_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.CertificateManagerGrpcAsyncIOTransport(
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
        transports.CertificateManagerGrpcTransport,
        transports.CertificateManagerGrpcAsyncIOTransport,
    ],
)
def test_certificate_manager_transport_channel_mtls_with_client_cert_source(
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
        transports.CertificateManagerGrpcTransport,
        transports.CertificateManagerGrpcAsyncIOTransport,
    ],
)
def test_certificate_manager_transport_channel_mtls_with_adc(transport_class):
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


def test_certificate_manager_grpc_lro_client():
    client = CertificateManagerClient(
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


def test_certificate_manager_grpc_lro_async_client():
    client = CertificateManagerAsyncClient(
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


def test_certificate_path():
    project = "squid"
    location = "clam"
    certificate = "whelk"
    expected = (
        "projects/{project}/locations/{location}/certificates/{certificate}".format(
            project=project,
            location=location,
            certificate=certificate,
        )
    )
    actual = CertificateManagerClient.certificate_path(project, location, certificate)
    assert expected == actual


def test_parse_certificate_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "certificate": "nudibranch",
    }
    path = CertificateManagerClient.certificate_path(**expected)

    # Check that the path construction is reversible.
    actual = CertificateManagerClient.parse_certificate_path(path)
    assert expected == actual


def test_certificate_map_path():
    project = "cuttlefish"
    location = "mussel"
    certificate_map = "winkle"
    expected = "projects/{project}/locations/{location}/certificateMaps/{certificate_map}".format(
        project=project,
        location=location,
        certificate_map=certificate_map,
    )
    actual = CertificateManagerClient.certificate_map_path(
        project, location, certificate_map
    )
    assert expected == actual


def test_parse_certificate_map_path():
    expected = {
        "project": "nautilus",
        "location": "scallop",
        "certificate_map": "abalone",
    }
    path = CertificateManagerClient.certificate_map_path(**expected)

    # Check that the path construction is reversible.
    actual = CertificateManagerClient.parse_certificate_map_path(path)
    assert expected == actual


def test_certificate_map_entry_path():
    project = "squid"
    location = "clam"
    certificate_map = "whelk"
    certificate_map_entry = "octopus"
    expected = "projects/{project}/locations/{location}/certificateMaps/{certificate_map}/certificateMapEntries/{certificate_map_entry}".format(
        project=project,
        location=location,
        certificate_map=certificate_map,
        certificate_map_entry=certificate_map_entry,
    )
    actual = CertificateManagerClient.certificate_map_entry_path(
        project, location, certificate_map, certificate_map_entry
    )
    assert expected == actual


def test_parse_certificate_map_entry_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
        "certificate_map": "cuttlefish",
        "certificate_map_entry": "mussel",
    }
    path = CertificateManagerClient.certificate_map_entry_path(**expected)

    # Check that the path construction is reversible.
    actual = CertificateManagerClient.parse_certificate_map_entry_path(path)
    assert expected == actual


def test_dns_authorization_path():
    project = "winkle"
    location = "nautilus"
    dns_authorization = "scallop"
    expected = "projects/{project}/locations/{location}/dnsAuthorizations/{dns_authorization}".format(
        project=project,
        location=location,
        dns_authorization=dns_authorization,
    )
    actual = CertificateManagerClient.dns_authorization_path(
        project, location, dns_authorization
    )
    assert expected == actual


def test_parse_dns_authorization_path():
    expected = {
        "project": "abalone",
        "location": "squid",
        "dns_authorization": "clam",
    }
    path = CertificateManagerClient.dns_authorization_path(**expected)

    # Check that the path construction is reversible.
    actual = CertificateManagerClient.parse_dns_authorization_path(path)
    assert expected == actual


def test_target_https_proxies_path():
    project = "whelk"
    location = "octopus"
    target_https_proxy = "oyster"
    expected = "projects/{project}/locations/{location}/targetHttpsProxies/{target_https_proxy}".format(
        project=project,
        location=location,
        target_https_proxy=target_https_proxy,
    )
    actual = CertificateManagerClient.target_https_proxies_path(
        project, location, target_https_proxy
    )
    assert expected == actual


def test_parse_target_https_proxies_path():
    expected = {
        "project": "nudibranch",
        "location": "cuttlefish",
        "target_https_proxy": "mussel",
    }
    path = CertificateManagerClient.target_https_proxies_path(**expected)

    # Check that the path construction is reversible.
    actual = CertificateManagerClient.parse_target_https_proxies_path(path)
    assert expected == actual


def test_target_ssl_proxies_path():
    project = "winkle"
    location = "nautilus"
    target_ssl_proxy = "scallop"
    expected = "projects/{project}/locations/{location}/targetSslProxies/{target_ssl_proxy}".format(
        project=project,
        location=location,
        target_ssl_proxy=target_ssl_proxy,
    )
    actual = CertificateManagerClient.target_ssl_proxies_path(
        project, location, target_ssl_proxy
    )
    assert expected == actual


def test_parse_target_ssl_proxies_path():
    expected = {
        "project": "abalone",
        "location": "squid",
        "target_ssl_proxy": "clam",
    }
    path = CertificateManagerClient.target_ssl_proxies_path(**expected)

    # Check that the path construction is reversible.
    actual = CertificateManagerClient.parse_target_ssl_proxies_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "whelk"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = CertificateManagerClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "octopus",
    }
    path = CertificateManagerClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = CertificateManagerClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "oyster"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = CertificateManagerClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nudibranch",
    }
    path = CertificateManagerClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = CertificateManagerClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "cuttlefish"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = CertificateManagerClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "mussel",
    }
    path = CertificateManagerClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = CertificateManagerClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "winkle"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = CertificateManagerClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nautilus",
    }
    path = CertificateManagerClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = CertificateManagerClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "scallop"
    location = "abalone"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = CertificateManagerClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "squid",
        "location": "clam",
    }
    path = CertificateManagerClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = CertificateManagerClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.CertificateManagerTransport, "_prep_wrapped_messages"
    ) as prep:
        client = CertificateManagerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.CertificateManagerTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = CertificateManagerClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = CertificateManagerAsyncClient(
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
        client = CertificateManagerClient(
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
        client = CertificateManagerClient(
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
        (CertificateManagerClient, transports.CertificateManagerGrpcTransport),
        (
            CertificateManagerAsyncClient,
            transports.CertificateManagerGrpcAsyncIOTransport,
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
            )
