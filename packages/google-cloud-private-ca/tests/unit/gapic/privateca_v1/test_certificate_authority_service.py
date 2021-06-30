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
import packaging.version

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
from google.api_core import operation_async  # type: ignore
from google.api_core import operations_v1
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.security.privateca_v1.services.certificate_authority_service import (
    CertificateAuthorityServiceAsyncClient,
)
from google.cloud.security.privateca_v1.services.certificate_authority_service import (
    CertificateAuthorityServiceClient,
)
from google.cloud.security.privateca_v1.services.certificate_authority_service import (
    pagers,
)
from google.cloud.security.privateca_v1.services.certificate_authority_service import (
    transports,
)
from google.cloud.security.privateca_v1.services.certificate_authority_service.transports.base import (
    _GOOGLE_AUTH_VERSION,
)
from google.cloud.security.privateca_v1.types import resources
from google.cloud.security.privateca_v1.types import service
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.type import expr_pb2  # type: ignore
import google.auth


# TODO(busunkim): Once google-auth >= 1.25.0 is required transitively
# through google-api-core:
# - Delete the auth "less than" test cases
# - Delete these pytest markers (Make the "greater than or equal to" tests the default).
requires_google_auth_lt_1_25_0 = pytest.mark.skipif(
    packaging.version.parse(_GOOGLE_AUTH_VERSION) >= packaging.version.parse("1.25.0"),
    reason="This test requires google-auth < 1.25.0",
)
requires_google_auth_gte_1_25_0 = pytest.mark.skipif(
    packaging.version.parse(_GOOGLE_AUTH_VERSION) < packaging.version.parse("1.25.0"),
    reason="This test requires google-auth >= 1.25.0",
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

    assert CertificateAuthorityServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        CertificateAuthorityServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        CertificateAuthorityServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        CertificateAuthorityServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        CertificateAuthorityServiceClient._get_default_mtls_endpoint(
            sandbox_mtls_endpoint
        )
        == sandbox_mtls_endpoint
    )
    assert (
        CertificateAuthorityServiceClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class",
    [CertificateAuthorityServiceClient, CertificateAuthorityServiceAsyncClient,],
)
def test_certificate_authority_service_client_from_service_account_info(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "privateca.googleapis.com:443"


@pytest.mark.parametrize(
    "client_class",
    [CertificateAuthorityServiceClient, CertificateAuthorityServiceAsyncClient,],
)
def test_certificate_authority_service_client_service_account_always_use_jwt(
    client_class,
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        client = client_class(credentials=creds)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.CertificateAuthorityServiceGrpcTransport, "grpc"),
        (transports.CertificateAuthorityServiceGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_certificate_authority_service_client_service_account_always_use_jwt_true(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)


@pytest.mark.parametrize(
    "client_class",
    [CertificateAuthorityServiceClient, CertificateAuthorityServiceAsyncClient,],
)
def test_certificate_authority_service_client_from_service_account_file(client_class):
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

        assert client.transport._host == "privateca.googleapis.com:443"


def test_certificate_authority_service_client_get_transport_class():
    transport = CertificateAuthorityServiceClient.get_transport_class()
    available_transports = [
        transports.CertificateAuthorityServiceGrpcTransport,
    ]
    assert transport in available_transports

    transport = CertificateAuthorityServiceClient.get_transport_class("grpc")
    assert transport == transports.CertificateAuthorityServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            CertificateAuthorityServiceClient,
            transports.CertificateAuthorityServiceGrpcTransport,
            "grpc",
        ),
        (
            CertificateAuthorityServiceAsyncClient,
            transports.CertificateAuthorityServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    CertificateAuthorityServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CertificateAuthorityServiceClient),
)
@mock.patch.object(
    CertificateAuthorityServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CertificateAuthorityServiceAsyncClient),
)
def test_certificate_authority_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(
        CertificateAuthorityServiceClient, "get_transport_class"
    ) as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(
        CertificateAuthorityServiceClient, "get_transport_class"
    ) as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class()

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError):
            client = client_class()

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (
            CertificateAuthorityServiceClient,
            transports.CertificateAuthorityServiceGrpcTransport,
            "grpc",
            "true",
        ),
        (
            CertificateAuthorityServiceAsyncClient,
            transports.CertificateAuthorityServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            CertificateAuthorityServiceClient,
            transports.CertificateAuthorityServiceGrpcTransport,
            "grpc",
            "false",
        ),
        (
            CertificateAuthorityServiceAsyncClient,
            transports.CertificateAuthorityServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    CertificateAuthorityServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CertificateAuthorityServiceClient),
)
@mock.patch.object(
    CertificateAuthorityServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CertificateAuthorityServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_certificate_authority_service_client_mtls_env_auto(
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
            client = client_class(client_options=options)

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
                    client = client_class()
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
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
                client = client_class()
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_ENDPOINT,
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            CertificateAuthorityServiceClient,
            transports.CertificateAuthorityServiceGrpcTransport,
            "grpc",
        ),
        (
            CertificateAuthorityServiceAsyncClient,
            transports.CertificateAuthorityServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_certificate_authority_service_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(scopes=["1", "2"],)
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            CertificateAuthorityServiceClient,
            transports.CertificateAuthorityServiceGrpcTransport,
            "grpc",
        ),
        (
            CertificateAuthorityServiceAsyncClient,
            transports.CertificateAuthorityServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_certificate_authority_service_client_client_options_credentials_file(
    client_class, transport_class, transport_name
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_certificate_authority_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.security.privateca_v1.services.certificate_authority_service.transports.CertificateAuthorityServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = CertificateAuthorityServiceClient(
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
        )


def test_create_certificate(
    transport: str = "grpc", request_type=service.CreateCertificateRequest
):
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Certificate(
            name="name_value",
            issuer_certificate_authority="issuer_certificate_authority_value",
            certificate_template="certificate_template_value",
            subject_mode=resources.SubjectRequestMode.DEFAULT,
            pem_certificate="pem_certificate_value",
            pem_certificate_chain=["pem_certificate_chain_value"],
            pem_csr="pem_csr_value",
        )
        response = client.create_certificate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateCertificateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Certificate)
    assert response.name == "name_value"
    assert response.issuer_certificate_authority == "issuer_certificate_authority_value"
    assert response.certificate_template == "certificate_template_value"
    assert response.subject_mode == resources.SubjectRequestMode.DEFAULT
    assert response.pem_certificate == "pem_certificate_value"
    assert response.pem_certificate_chain == ["pem_certificate_chain_value"]


def test_create_certificate_from_dict():
    test_create_certificate(request_type=dict)


def test_create_certificate_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate), "__call__"
    ) as call:
        client.create_certificate()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateCertificateRequest()


@pytest.mark.asyncio
async def test_create_certificate_async(
    transport: str = "grpc_asyncio", request_type=service.CreateCertificateRequest
):
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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
            resources.Certificate(
                name="name_value",
                issuer_certificate_authority="issuer_certificate_authority_value",
                certificate_template="certificate_template_value",
                subject_mode=resources.SubjectRequestMode.DEFAULT,
                pem_certificate="pem_certificate_value",
                pem_certificate_chain=["pem_certificate_chain_value"],
            )
        )
        response = await client.create_certificate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateCertificateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Certificate)
    assert response.name == "name_value"
    assert response.issuer_certificate_authority == "issuer_certificate_authority_value"
    assert response.certificate_template == "certificate_template_value"
    assert response.subject_mode == resources.SubjectRequestMode.DEFAULT
    assert response.pem_certificate == "pem_certificate_value"
    assert response.pem_certificate_chain == ["pem_certificate_chain_value"]


@pytest.mark.asyncio
async def test_create_certificate_async_from_dict():
    await test_create_certificate_async(request_type=dict)


def test_create_certificate_field_headers():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateCertificateRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate), "__call__"
    ) as call:
        call.return_value = resources.Certificate()
        client.create_certificate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_certificate_field_headers_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateCertificateRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Certificate()
        )
        await client.create_certificate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_certificate_flattened():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Certificate()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_certificate(
            parent="parent_value",
            certificate=resources.Certificate(name="name_value"),
            certificate_id="certificate_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].certificate == resources.Certificate(name="name_value")
        assert args[0].certificate_id == "certificate_id_value"


def test_create_certificate_flattened_error():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_certificate(
            service.CreateCertificateRequest(),
            parent="parent_value",
            certificate=resources.Certificate(name="name_value"),
            certificate_id="certificate_id_value",
        )


@pytest.mark.asyncio
async def test_create_certificate_flattened_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Certificate()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Certificate()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_certificate(
            parent="parent_value",
            certificate=resources.Certificate(name="name_value"),
            certificate_id="certificate_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].certificate == resources.Certificate(name="name_value")
        assert args[0].certificate_id == "certificate_id_value"


@pytest.mark.asyncio
async def test_create_certificate_flattened_error_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_certificate(
            service.CreateCertificateRequest(),
            parent="parent_value",
            certificate=resources.Certificate(name="name_value"),
            certificate_id="certificate_id_value",
        )


def test_get_certificate(
    transport: str = "grpc", request_type=service.GetCertificateRequest
):
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_certificate), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Certificate(
            name="name_value",
            issuer_certificate_authority="issuer_certificate_authority_value",
            certificate_template="certificate_template_value",
            subject_mode=resources.SubjectRequestMode.DEFAULT,
            pem_certificate="pem_certificate_value",
            pem_certificate_chain=["pem_certificate_chain_value"],
            pem_csr="pem_csr_value",
        )
        response = client.get_certificate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetCertificateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Certificate)
    assert response.name == "name_value"
    assert response.issuer_certificate_authority == "issuer_certificate_authority_value"
    assert response.certificate_template == "certificate_template_value"
    assert response.subject_mode == resources.SubjectRequestMode.DEFAULT
    assert response.pem_certificate == "pem_certificate_value"
    assert response.pem_certificate_chain == ["pem_certificate_chain_value"]


def test_get_certificate_from_dict():
    test_get_certificate(request_type=dict)


def test_get_certificate_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_certificate), "__call__") as call:
        client.get_certificate()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetCertificateRequest()


@pytest.mark.asyncio
async def test_get_certificate_async(
    transport: str = "grpc_asyncio", request_type=service.GetCertificateRequest
):
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_certificate), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Certificate(
                name="name_value",
                issuer_certificate_authority="issuer_certificate_authority_value",
                certificate_template="certificate_template_value",
                subject_mode=resources.SubjectRequestMode.DEFAULT,
                pem_certificate="pem_certificate_value",
                pem_certificate_chain=["pem_certificate_chain_value"],
            )
        )
        response = await client.get_certificate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetCertificateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Certificate)
    assert response.name == "name_value"
    assert response.issuer_certificate_authority == "issuer_certificate_authority_value"
    assert response.certificate_template == "certificate_template_value"
    assert response.subject_mode == resources.SubjectRequestMode.DEFAULT
    assert response.pem_certificate == "pem_certificate_value"
    assert response.pem_certificate_chain == ["pem_certificate_chain_value"]


@pytest.mark.asyncio
async def test_get_certificate_async_from_dict():
    await test_get_certificate_async(request_type=dict)


def test_get_certificate_field_headers():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetCertificateRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_certificate), "__call__") as call:
        call.return_value = resources.Certificate()
        client.get_certificate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_certificate_field_headers_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetCertificateRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_certificate), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Certificate()
        )
        await client.get_certificate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_certificate_flattened():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_certificate), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Certificate()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_certificate(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_certificate_flattened_error():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_certificate(
            service.GetCertificateRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_certificate_flattened_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_certificate), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Certificate()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Certificate()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_certificate(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_certificate_flattened_error_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_certificate(
            service.GetCertificateRequest(), name="name_value",
        )


def test_list_certificates(
    transport: str = "grpc", request_type=service.ListCertificatesRequest
):
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificates), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListCertificatesResponse(
            next_page_token="next_page_token_value", unreachable=["unreachable_value"],
        )
        response = client.list_certificates(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListCertificatesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCertificatesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_certificates_from_dict():
    test_list_certificates(request_type=dict)


def test_list_certificates_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificates), "__call__"
    ) as call:
        client.list_certificates()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListCertificatesRequest()


@pytest.mark.asyncio
async def test_list_certificates_async(
    transport: str = "grpc_asyncio", request_type=service.ListCertificatesRequest
):
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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
            service.ListCertificatesResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_certificates(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListCertificatesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCertificatesAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_certificates_async_from_dict():
    await test_list_certificates_async(request_type=dict)


def test_list_certificates_field_headers():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListCertificatesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificates), "__call__"
    ) as call:
        call.return_value = service.ListCertificatesResponse()
        client.list_certificates(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_certificates_field_headers_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListCertificatesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificates), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListCertificatesResponse()
        )
        await client.list_certificates(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_certificates_flattened():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificates), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListCertificatesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_certificates(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_certificates_flattened_error():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_certificates(
            service.ListCertificatesRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_certificates_flattened_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificates), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListCertificatesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListCertificatesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_certificates(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_certificates_flattened_error_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_certificates(
            service.ListCertificatesRequest(), parent="parent_value",
        )


def test_list_certificates_pager():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificates), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListCertificatesResponse(
                certificates=[
                    resources.Certificate(),
                    resources.Certificate(),
                    resources.Certificate(),
                ],
                next_page_token="abc",
            ),
            service.ListCertificatesResponse(certificates=[], next_page_token="def",),
            service.ListCertificatesResponse(
                certificates=[resources.Certificate(),], next_page_token="ghi",
            ),
            service.ListCertificatesResponse(
                certificates=[resources.Certificate(), resources.Certificate(),],
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
        assert all(isinstance(i, resources.Certificate) for i in results)


def test_list_certificates_pages():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificates), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListCertificatesResponse(
                certificates=[
                    resources.Certificate(),
                    resources.Certificate(),
                    resources.Certificate(),
                ],
                next_page_token="abc",
            ),
            service.ListCertificatesResponse(certificates=[], next_page_token="def",),
            service.ListCertificatesResponse(
                certificates=[resources.Certificate(),], next_page_token="ghi",
            ),
            service.ListCertificatesResponse(
                certificates=[resources.Certificate(), resources.Certificate(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_certificates(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_certificates_async_pager():
    client = CertificateAuthorityServiceAsyncClient(
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
            service.ListCertificatesResponse(
                certificates=[
                    resources.Certificate(),
                    resources.Certificate(),
                    resources.Certificate(),
                ],
                next_page_token="abc",
            ),
            service.ListCertificatesResponse(certificates=[], next_page_token="def",),
            service.ListCertificatesResponse(
                certificates=[resources.Certificate(),], next_page_token="ghi",
            ),
            service.ListCertificatesResponse(
                certificates=[resources.Certificate(), resources.Certificate(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_certificates(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.Certificate) for i in responses)


@pytest.mark.asyncio
async def test_list_certificates_async_pages():
    client = CertificateAuthorityServiceAsyncClient(
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
            service.ListCertificatesResponse(
                certificates=[
                    resources.Certificate(),
                    resources.Certificate(),
                    resources.Certificate(),
                ],
                next_page_token="abc",
            ),
            service.ListCertificatesResponse(certificates=[], next_page_token="def",),
            service.ListCertificatesResponse(
                certificates=[resources.Certificate(),], next_page_token="ghi",
            ),
            service.ListCertificatesResponse(
                certificates=[resources.Certificate(), resources.Certificate(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_certificates(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_revoke_certificate(
    transport: str = "grpc", request_type=service.RevokeCertificateRequest
):
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.revoke_certificate), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Certificate(
            name="name_value",
            issuer_certificate_authority="issuer_certificate_authority_value",
            certificate_template="certificate_template_value",
            subject_mode=resources.SubjectRequestMode.DEFAULT,
            pem_certificate="pem_certificate_value",
            pem_certificate_chain=["pem_certificate_chain_value"],
            pem_csr="pem_csr_value",
        )
        response = client.revoke_certificate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.RevokeCertificateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Certificate)
    assert response.name == "name_value"
    assert response.issuer_certificate_authority == "issuer_certificate_authority_value"
    assert response.certificate_template == "certificate_template_value"
    assert response.subject_mode == resources.SubjectRequestMode.DEFAULT
    assert response.pem_certificate == "pem_certificate_value"
    assert response.pem_certificate_chain == ["pem_certificate_chain_value"]


def test_revoke_certificate_from_dict():
    test_revoke_certificate(request_type=dict)


def test_revoke_certificate_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.revoke_certificate), "__call__"
    ) as call:
        client.revoke_certificate()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.RevokeCertificateRequest()


@pytest.mark.asyncio
async def test_revoke_certificate_async(
    transport: str = "grpc_asyncio", request_type=service.RevokeCertificateRequest
):
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.revoke_certificate), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Certificate(
                name="name_value",
                issuer_certificate_authority="issuer_certificate_authority_value",
                certificate_template="certificate_template_value",
                subject_mode=resources.SubjectRequestMode.DEFAULT,
                pem_certificate="pem_certificate_value",
                pem_certificate_chain=["pem_certificate_chain_value"],
            )
        )
        response = await client.revoke_certificate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.RevokeCertificateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Certificate)
    assert response.name == "name_value"
    assert response.issuer_certificate_authority == "issuer_certificate_authority_value"
    assert response.certificate_template == "certificate_template_value"
    assert response.subject_mode == resources.SubjectRequestMode.DEFAULT
    assert response.pem_certificate == "pem_certificate_value"
    assert response.pem_certificate_chain == ["pem_certificate_chain_value"]


@pytest.mark.asyncio
async def test_revoke_certificate_async_from_dict():
    await test_revoke_certificate_async(request_type=dict)


def test_revoke_certificate_field_headers():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.RevokeCertificateRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.revoke_certificate), "__call__"
    ) as call:
        call.return_value = resources.Certificate()
        client.revoke_certificate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_revoke_certificate_field_headers_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.RevokeCertificateRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.revoke_certificate), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Certificate()
        )
        await client.revoke_certificate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_revoke_certificate_flattened():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.revoke_certificate), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Certificate()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.revoke_certificate(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_revoke_certificate_flattened_error():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.revoke_certificate(
            service.RevokeCertificateRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_revoke_certificate_flattened_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.revoke_certificate), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Certificate()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Certificate()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.revoke_certificate(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_revoke_certificate_flattened_error_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.revoke_certificate(
            service.RevokeCertificateRequest(), name="name_value",
        )


def test_update_certificate(
    transport: str = "grpc", request_type=service.UpdateCertificateRequest
):
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Certificate(
            name="name_value",
            issuer_certificate_authority="issuer_certificate_authority_value",
            certificate_template="certificate_template_value",
            subject_mode=resources.SubjectRequestMode.DEFAULT,
            pem_certificate="pem_certificate_value",
            pem_certificate_chain=["pem_certificate_chain_value"],
            pem_csr="pem_csr_value",
        )
        response = client.update_certificate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateCertificateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Certificate)
    assert response.name == "name_value"
    assert response.issuer_certificate_authority == "issuer_certificate_authority_value"
    assert response.certificate_template == "certificate_template_value"
    assert response.subject_mode == resources.SubjectRequestMode.DEFAULT
    assert response.pem_certificate == "pem_certificate_value"
    assert response.pem_certificate_chain == ["pem_certificate_chain_value"]


def test_update_certificate_from_dict():
    test_update_certificate(request_type=dict)


def test_update_certificate_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate), "__call__"
    ) as call:
        client.update_certificate()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateCertificateRequest()


@pytest.mark.asyncio
async def test_update_certificate_async(
    transport: str = "grpc_asyncio", request_type=service.UpdateCertificateRequest
):
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
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
            resources.Certificate(
                name="name_value",
                issuer_certificate_authority="issuer_certificate_authority_value",
                certificate_template="certificate_template_value",
                subject_mode=resources.SubjectRequestMode.DEFAULT,
                pem_certificate="pem_certificate_value",
                pem_certificate_chain=["pem_certificate_chain_value"],
            )
        )
        response = await client.update_certificate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateCertificateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Certificate)
    assert response.name == "name_value"
    assert response.issuer_certificate_authority == "issuer_certificate_authority_value"
    assert response.certificate_template == "certificate_template_value"
    assert response.subject_mode == resources.SubjectRequestMode.DEFAULT
    assert response.pem_certificate == "pem_certificate_value"
    assert response.pem_certificate_chain == ["pem_certificate_chain_value"]


@pytest.mark.asyncio
async def test_update_certificate_async_from_dict():
    await test_update_certificate_async(request_type=dict)


def test_update_certificate_field_headers():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateCertificateRequest()

    request.certificate.name = "certificate.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate), "__call__"
    ) as call:
        call.return_value = resources.Certificate()
        client.update_certificate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "certificate.name=certificate.name/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_update_certificate_field_headers_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateCertificateRequest()

    request.certificate.name = "certificate.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Certificate()
        )
        await client.update_certificate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "certificate.name=certificate.name/value",) in kw[
        "metadata"
    ]


def test_update_certificate_flattened():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Certificate()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_certificate(
            certificate=resources.Certificate(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].certificate == resources.Certificate(name="name_value")
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


def test_update_certificate_flattened_error():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_certificate(
            service.UpdateCertificateRequest(),
            certificate=resources.Certificate(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_certificate_flattened_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Certificate()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Certificate()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_certificate(
            certificate=resources.Certificate(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].certificate == resources.Certificate(name="name_value")
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_certificate_flattened_error_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_certificate(
            service.UpdateCertificateRequest(),
            certificate=resources.Certificate(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_activate_certificate_authority(
    transport: str = "grpc", request_type=service.ActivateCertificateAuthorityRequest
):
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.activate_certificate_authority), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.activate_certificate_authority(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ActivateCertificateAuthorityRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_activate_certificate_authority_from_dict():
    test_activate_certificate_authority(request_type=dict)


def test_activate_certificate_authority_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.activate_certificate_authority), "__call__"
    ) as call:
        client.activate_certificate_authority()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ActivateCertificateAuthorityRequest()


@pytest.mark.asyncio
async def test_activate_certificate_authority_async(
    transport: str = "grpc_asyncio",
    request_type=service.ActivateCertificateAuthorityRequest,
):
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.activate_certificate_authority), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.activate_certificate_authority(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ActivateCertificateAuthorityRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_activate_certificate_authority_async_from_dict():
    await test_activate_certificate_authority_async(request_type=dict)


def test_activate_certificate_authority_field_headers():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ActivateCertificateAuthorityRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.activate_certificate_authority), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.activate_certificate_authority(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_activate_certificate_authority_field_headers_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ActivateCertificateAuthorityRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.activate_certificate_authority), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.activate_certificate_authority(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_activate_certificate_authority_flattened():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.activate_certificate_authority), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.activate_certificate_authority(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_activate_certificate_authority_flattened_error():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.activate_certificate_authority(
            service.ActivateCertificateAuthorityRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_activate_certificate_authority_flattened_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.activate_certificate_authority), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.activate_certificate_authority(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_activate_certificate_authority_flattened_error_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.activate_certificate_authority(
            service.ActivateCertificateAuthorityRequest(), name="name_value",
        )


def test_create_certificate_authority(
    transport: str = "grpc", request_type=service.CreateCertificateAuthorityRequest
):
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_authority), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_certificate_authority(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateCertificateAuthorityRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_certificate_authority_from_dict():
    test_create_certificate_authority(request_type=dict)


def test_create_certificate_authority_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_authority), "__call__"
    ) as call:
        client.create_certificate_authority()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateCertificateAuthorityRequest()


@pytest.mark.asyncio
async def test_create_certificate_authority_async(
    transport: str = "grpc_asyncio",
    request_type=service.CreateCertificateAuthorityRequest,
):
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_authority), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_certificate_authority(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateCertificateAuthorityRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_certificate_authority_async_from_dict():
    await test_create_certificate_authority_async(request_type=dict)


def test_create_certificate_authority_field_headers():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateCertificateAuthorityRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_authority), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_certificate_authority(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_certificate_authority_field_headers_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateCertificateAuthorityRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_authority), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_certificate_authority(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_certificate_authority_flattened():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_authority), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_certificate_authority(
            parent="parent_value",
            certificate_authority=resources.CertificateAuthority(name="name_value"),
            certificate_authority_id="certificate_authority_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].certificate_authority == resources.CertificateAuthority(
            name="name_value"
        )
        assert args[0].certificate_authority_id == "certificate_authority_id_value"


def test_create_certificate_authority_flattened_error():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_certificate_authority(
            service.CreateCertificateAuthorityRequest(),
            parent="parent_value",
            certificate_authority=resources.CertificateAuthority(name="name_value"),
            certificate_authority_id="certificate_authority_id_value",
        )


@pytest.mark.asyncio
async def test_create_certificate_authority_flattened_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_authority), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_certificate_authority(
            parent="parent_value",
            certificate_authority=resources.CertificateAuthority(name="name_value"),
            certificate_authority_id="certificate_authority_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].certificate_authority == resources.CertificateAuthority(
            name="name_value"
        )
        assert args[0].certificate_authority_id == "certificate_authority_id_value"


@pytest.mark.asyncio
async def test_create_certificate_authority_flattened_error_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_certificate_authority(
            service.CreateCertificateAuthorityRequest(),
            parent="parent_value",
            certificate_authority=resources.CertificateAuthority(name="name_value"),
            certificate_authority_id="certificate_authority_id_value",
        )


def test_disable_certificate_authority(
    transport: str = "grpc", request_type=service.DisableCertificateAuthorityRequest
):
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.disable_certificate_authority), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.disable_certificate_authority(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DisableCertificateAuthorityRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_disable_certificate_authority_from_dict():
    test_disable_certificate_authority(request_type=dict)


def test_disable_certificate_authority_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.disable_certificate_authority), "__call__"
    ) as call:
        client.disable_certificate_authority()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DisableCertificateAuthorityRequest()


@pytest.mark.asyncio
async def test_disable_certificate_authority_async(
    transport: str = "grpc_asyncio",
    request_type=service.DisableCertificateAuthorityRequest,
):
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.disable_certificate_authority), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.disable_certificate_authority(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DisableCertificateAuthorityRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_disable_certificate_authority_async_from_dict():
    await test_disable_certificate_authority_async(request_type=dict)


def test_disable_certificate_authority_field_headers():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.DisableCertificateAuthorityRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.disable_certificate_authority), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.disable_certificate_authority(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_disable_certificate_authority_field_headers_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.DisableCertificateAuthorityRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.disable_certificate_authority), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.disable_certificate_authority(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_disable_certificate_authority_flattened():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.disable_certificate_authority), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.disable_certificate_authority(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_disable_certificate_authority_flattened_error():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.disable_certificate_authority(
            service.DisableCertificateAuthorityRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_disable_certificate_authority_flattened_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.disable_certificate_authority), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.disable_certificate_authority(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_disable_certificate_authority_flattened_error_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.disable_certificate_authority(
            service.DisableCertificateAuthorityRequest(), name="name_value",
        )


def test_enable_certificate_authority(
    transport: str = "grpc", request_type=service.EnableCertificateAuthorityRequest
):
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.enable_certificate_authority), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.enable_certificate_authority(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.EnableCertificateAuthorityRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_enable_certificate_authority_from_dict():
    test_enable_certificate_authority(request_type=dict)


def test_enable_certificate_authority_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.enable_certificate_authority), "__call__"
    ) as call:
        client.enable_certificate_authority()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.EnableCertificateAuthorityRequest()


@pytest.mark.asyncio
async def test_enable_certificate_authority_async(
    transport: str = "grpc_asyncio",
    request_type=service.EnableCertificateAuthorityRequest,
):
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.enable_certificate_authority), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.enable_certificate_authority(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.EnableCertificateAuthorityRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_enable_certificate_authority_async_from_dict():
    await test_enable_certificate_authority_async(request_type=dict)


def test_enable_certificate_authority_field_headers():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.EnableCertificateAuthorityRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.enable_certificate_authority), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.enable_certificate_authority(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_enable_certificate_authority_field_headers_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.EnableCertificateAuthorityRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.enable_certificate_authority), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.enable_certificate_authority(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_enable_certificate_authority_flattened():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.enable_certificate_authority), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.enable_certificate_authority(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_enable_certificate_authority_flattened_error():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.enable_certificate_authority(
            service.EnableCertificateAuthorityRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_enable_certificate_authority_flattened_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.enable_certificate_authority), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.enable_certificate_authority(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_enable_certificate_authority_flattened_error_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.enable_certificate_authority(
            service.EnableCertificateAuthorityRequest(), name="name_value",
        )


def test_fetch_certificate_authority_csr(
    transport: str = "grpc", request_type=service.FetchCertificateAuthorityCsrRequest
):
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.fetch_certificate_authority_csr), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.FetchCertificateAuthorityCsrResponse(
            pem_csr="pem_csr_value",
        )
        response = client.fetch_certificate_authority_csr(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.FetchCertificateAuthorityCsrRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.FetchCertificateAuthorityCsrResponse)
    assert response.pem_csr == "pem_csr_value"


def test_fetch_certificate_authority_csr_from_dict():
    test_fetch_certificate_authority_csr(request_type=dict)


def test_fetch_certificate_authority_csr_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.fetch_certificate_authority_csr), "__call__"
    ) as call:
        client.fetch_certificate_authority_csr()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.FetchCertificateAuthorityCsrRequest()


@pytest.mark.asyncio
async def test_fetch_certificate_authority_csr_async(
    transport: str = "grpc_asyncio",
    request_type=service.FetchCertificateAuthorityCsrRequest,
):
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.fetch_certificate_authority_csr), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.FetchCertificateAuthorityCsrResponse(pem_csr="pem_csr_value",)
        )
        response = await client.fetch_certificate_authority_csr(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.FetchCertificateAuthorityCsrRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.FetchCertificateAuthorityCsrResponse)
    assert response.pem_csr == "pem_csr_value"


@pytest.mark.asyncio
async def test_fetch_certificate_authority_csr_async_from_dict():
    await test_fetch_certificate_authority_csr_async(request_type=dict)


def test_fetch_certificate_authority_csr_field_headers():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.FetchCertificateAuthorityCsrRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.fetch_certificate_authority_csr), "__call__"
    ) as call:
        call.return_value = service.FetchCertificateAuthorityCsrResponse()
        client.fetch_certificate_authority_csr(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_fetch_certificate_authority_csr_field_headers_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.FetchCertificateAuthorityCsrRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.fetch_certificate_authority_csr), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.FetchCertificateAuthorityCsrResponse()
        )
        await client.fetch_certificate_authority_csr(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_fetch_certificate_authority_csr_flattened():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.fetch_certificate_authority_csr), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.FetchCertificateAuthorityCsrResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.fetch_certificate_authority_csr(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_fetch_certificate_authority_csr_flattened_error():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.fetch_certificate_authority_csr(
            service.FetchCertificateAuthorityCsrRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_fetch_certificate_authority_csr_flattened_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.fetch_certificate_authority_csr), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.FetchCertificateAuthorityCsrResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.FetchCertificateAuthorityCsrResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.fetch_certificate_authority_csr(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_fetch_certificate_authority_csr_flattened_error_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.fetch_certificate_authority_csr(
            service.FetchCertificateAuthorityCsrRequest(), name="name_value",
        )


def test_get_certificate_authority(
    transport: str = "grpc", request_type=service.GetCertificateAuthorityRequest
):
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_authority), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CertificateAuthority(
            name="name_value",
            type_=resources.CertificateAuthority.Type.SELF_SIGNED,
            tier=resources.CaPool.Tier.ENTERPRISE,
            state=resources.CertificateAuthority.State.ENABLED,
            pem_ca_certificates=["pem_ca_certificates_value"],
            gcs_bucket="gcs_bucket_value",
        )
        response = client.get_certificate_authority(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetCertificateAuthorityRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CertificateAuthority)
    assert response.name == "name_value"
    assert response.type_ == resources.CertificateAuthority.Type.SELF_SIGNED
    assert response.tier == resources.CaPool.Tier.ENTERPRISE
    assert response.state == resources.CertificateAuthority.State.ENABLED
    assert response.pem_ca_certificates == ["pem_ca_certificates_value"]
    assert response.gcs_bucket == "gcs_bucket_value"


def test_get_certificate_authority_from_dict():
    test_get_certificate_authority(request_type=dict)


def test_get_certificate_authority_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_authority), "__call__"
    ) as call:
        client.get_certificate_authority()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetCertificateAuthorityRequest()


@pytest.mark.asyncio
async def test_get_certificate_authority_async(
    transport: str = "grpc_asyncio", request_type=service.GetCertificateAuthorityRequest
):
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_authority), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CertificateAuthority(
                name="name_value",
                type_=resources.CertificateAuthority.Type.SELF_SIGNED,
                tier=resources.CaPool.Tier.ENTERPRISE,
                state=resources.CertificateAuthority.State.ENABLED,
                pem_ca_certificates=["pem_ca_certificates_value"],
                gcs_bucket="gcs_bucket_value",
            )
        )
        response = await client.get_certificate_authority(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetCertificateAuthorityRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CertificateAuthority)
    assert response.name == "name_value"
    assert response.type_ == resources.CertificateAuthority.Type.SELF_SIGNED
    assert response.tier == resources.CaPool.Tier.ENTERPRISE
    assert response.state == resources.CertificateAuthority.State.ENABLED
    assert response.pem_ca_certificates == ["pem_ca_certificates_value"]
    assert response.gcs_bucket == "gcs_bucket_value"


@pytest.mark.asyncio
async def test_get_certificate_authority_async_from_dict():
    await test_get_certificate_authority_async(request_type=dict)


def test_get_certificate_authority_field_headers():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetCertificateAuthorityRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_authority), "__call__"
    ) as call:
        call.return_value = resources.CertificateAuthority()
        client.get_certificate_authority(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_certificate_authority_field_headers_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetCertificateAuthorityRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_authority), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CertificateAuthority()
        )
        await client.get_certificate_authority(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_certificate_authority_flattened():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_authority), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CertificateAuthority()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_certificate_authority(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_certificate_authority_flattened_error():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_certificate_authority(
            service.GetCertificateAuthorityRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_certificate_authority_flattened_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_authority), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CertificateAuthority()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CertificateAuthority()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_certificate_authority(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_certificate_authority_flattened_error_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_certificate_authority(
            service.GetCertificateAuthorityRequest(), name="name_value",
        )


def test_list_certificate_authorities(
    transport: str = "grpc", request_type=service.ListCertificateAuthoritiesRequest
):
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_authorities), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListCertificateAuthoritiesResponse(
            next_page_token="next_page_token_value", unreachable=["unreachable_value"],
        )
        response = client.list_certificate_authorities(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListCertificateAuthoritiesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCertificateAuthoritiesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_certificate_authorities_from_dict():
    test_list_certificate_authorities(request_type=dict)


def test_list_certificate_authorities_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_authorities), "__call__"
    ) as call:
        client.list_certificate_authorities()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListCertificateAuthoritiesRequest()


@pytest.mark.asyncio
async def test_list_certificate_authorities_async(
    transport: str = "grpc_asyncio",
    request_type=service.ListCertificateAuthoritiesRequest,
):
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_authorities), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListCertificateAuthoritiesResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_certificate_authorities(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListCertificateAuthoritiesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCertificateAuthoritiesAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_certificate_authorities_async_from_dict():
    await test_list_certificate_authorities_async(request_type=dict)


def test_list_certificate_authorities_field_headers():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListCertificateAuthoritiesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_authorities), "__call__"
    ) as call:
        call.return_value = service.ListCertificateAuthoritiesResponse()
        client.list_certificate_authorities(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_certificate_authorities_field_headers_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListCertificateAuthoritiesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_authorities), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListCertificateAuthoritiesResponse()
        )
        await client.list_certificate_authorities(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_certificate_authorities_flattened():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_authorities), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListCertificateAuthoritiesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_certificate_authorities(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_certificate_authorities_flattened_error():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_certificate_authorities(
            service.ListCertificateAuthoritiesRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_certificate_authorities_flattened_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_authorities), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListCertificateAuthoritiesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListCertificateAuthoritiesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_certificate_authorities(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_certificate_authorities_flattened_error_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_certificate_authorities(
            service.ListCertificateAuthoritiesRequest(), parent="parent_value",
        )


def test_list_certificate_authorities_pager():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_authorities), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListCertificateAuthoritiesResponse(
                certificate_authorities=[
                    resources.CertificateAuthority(),
                    resources.CertificateAuthority(),
                    resources.CertificateAuthority(),
                ],
                next_page_token="abc",
            ),
            service.ListCertificateAuthoritiesResponse(
                certificate_authorities=[], next_page_token="def",
            ),
            service.ListCertificateAuthoritiesResponse(
                certificate_authorities=[resources.CertificateAuthority(),],
                next_page_token="ghi",
            ),
            service.ListCertificateAuthoritiesResponse(
                certificate_authorities=[
                    resources.CertificateAuthority(),
                    resources.CertificateAuthority(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_certificate_authorities(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, resources.CertificateAuthority) for i in results)


def test_list_certificate_authorities_pages():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_authorities), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListCertificateAuthoritiesResponse(
                certificate_authorities=[
                    resources.CertificateAuthority(),
                    resources.CertificateAuthority(),
                    resources.CertificateAuthority(),
                ],
                next_page_token="abc",
            ),
            service.ListCertificateAuthoritiesResponse(
                certificate_authorities=[], next_page_token="def",
            ),
            service.ListCertificateAuthoritiesResponse(
                certificate_authorities=[resources.CertificateAuthority(),],
                next_page_token="ghi",
            ),
            service.ListCertificateAuthoritiesResponse(
                certificate_authorities=[
                    resources.CertificateAuthority(),
                    resources.CertificateAuthority(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_certificate_authorities(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_certificate_authorities_async_pager():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_authorities),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListCertificateAuthoritiesResponse(
                certificate_authorities=[
                    resources.CertificateAuthority(),
                    resources.CertificateAuthority(),
                    resources.CertificateAuthority(),
                ],
                next_page_token="abc",
            ),
            service.ListCertificateAuthoritiesResponse(
                certificate_authorities=[], next_page_token="def",
            ),
            service.ListCertificateAuthoritiesResponse(
                certificate_authorities=[resources.CertificateAuthority(),],
                next_page_token="ghi",
            ),
            service.ListCertificateAuthoritiesResponse(
                certificate_authorities=[
                    resources.CertificateAuthority(),
                    resources.CertificateAuthority(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_certificate_authorities(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.CertificateAuthority) for i in responses)


@pytest.mark.asyncio
async def test_list_certificate_authorities_async_pages():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_authorities),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListCertificateAuthoritiesResponse(
                certificate_authorities=[
                    resources.CertificateAuthority(),
                    resources.CertificateAuthority(),
                    resources.CertificateAuthority(),
                ],
                next_page_token="abc",
            ),
            service.ListCertificateAuthoritiesResponse(
                certificate_authorities=[], next_page_token="def",
            ),
            service.ListCertificateAuthoritiesResponse(
                certificate_authorities=[resources.CertificateAuthority(),],
                next_page_token="ghi",
            ),
            service.ListCertificateAuthoritiesResponse(
                certificate_authorities=[
                    resources.CertificateAuthority(),
                    resources.CertificateAuthority(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_certificate_authorities(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_undelete_certificate_authority(
    transport: str = "grpc", request_type=service.UndeleteCertificateAuthorityRequest
):
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undelete_certificate_authority), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.undelete_certificate_authority(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UndeleteCertificateAuthorityRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_undelete_certificate_authority_from_dict():
    test_undelete_certificate_authority(request_type=dict)


def test_undelete_certificate_authority_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undelete_certificate_authority), "__call__"
    ) as call:
        client.undelete_certificate_authority()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UndeleteCertificateAuthorityRequest()


@pytest.mark.asyncio
async def test_undelete_certificate_authority_async(
    transport: str = "grpc_asyncio",
    request_type=service.UndeleteCertificateAuthorityRequest,
):
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undelete_certificate_authority), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.undelete_certificate_authority(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UndeleteCertificateAuthorityRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_undelete_certificate_authority_async_from_dict():
    await test_undelete_certificate_authority_async(request_type=dict)


def test_undelete_certificate_authority_field_headers():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UndeleteCertificateAuthorityRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undelete_certificate_authority), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.undelete_certificate_authority(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_undelete_certificate_authority_field_headers_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UndeleteCertificateAuthorityRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undelete_certificate_authority), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.undelete_certificate_authority(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_undelete_certificate_authority_flattened():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undelete_certificate_authority), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.undelete_certificate_authority(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_undelete_certificate_authority_flattened_error():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.undelete_certificate_authority(
            service.UndeleteCertificateAuthorityRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_undelete_certificate_authority_flattened_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.undelete_certificate_authority), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.undelete_certificate_authority(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_undelete_certificate_authority_flattened_error_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.undelete_certificate_authority(
            service.UndeleteCertificateAuthorityRequest(), name="name_value",
        )


def test_delete_certificate_authority(
    transport: str = "grpc", request_type=service.DeleteCertificateAuthorityRequest
):
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_authority), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_certificate_authority(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteCertificateAuthorityRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_certificate_authority_from_dict():
    test_delete_certificate_authority(request_type=dict)


def test_delete_certificate_authority_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_authority), "__call__"
    ) as call:
        client.delete_certificate_authority()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteCertificateAuthorityRequest()


@pytest.mark.asyncio
async def test_delete_certificate_authority_async(
    transport: str = "grpc_asyncio",
    request_type=service.DeleteCertificateAuthorityRequest,
):
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_authority), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_certificate_authority(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteCertificateAuthorityRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_certificate_authority_async_from_dict():
    await test_delete_certificate_authority_async(request_type=dict)


def test_delete_certificate_authority_field_headers():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.DeleteCertificateAuthorityRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_authority), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_certificate_authority(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_certificate_authority_field_headers_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.DeleteCertificateAuthorityRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_authority), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_certificate_authority(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_certificate_authority_flattened():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_authority), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_certificate_authority(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_certificate_authority_flattened_error():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_certificate_authority(
            service.DeleteCertificateAuthorityRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_certificate_authority_flattened_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_authority), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_certificate_authority(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_certificate_authority_flattened_error_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_certificate_authority(
            service.DeleteCertificateAuthorityRequest(), name="name_value",
        )


def test_update_certificate_authority(
    transport: str = "grpc", request_type=service.UpdateCertificateAuthorityRequest
):
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_authority), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_certificate_authority(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateCertificateAuthorityRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_certificate_authority_from_dict():
    test_update_certificate_authority(request_type=dict)


def test_update_certificate_authority_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_authority), "__call__"
    ) as call:
        client.update_certificate_authority()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateCertificateAuthorityRequest()


@pytest.mark.asyncio
async def test_update_certificate_authority_async(
    transport: str = "grpc_asyncio",
    request_type=service.UpdateCertificateAuthorityRequest,
):
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_authority), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_certificate_authority(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateCertificateAuthorityRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_certificate_authority_async_from_dict():
    await test_update_certificate_authority_async(request_type=dict)


def test_update_certificate_authority_field_headers():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateCertificateAuthorityRequest()

    request.certificate_authority.name = "certificate_authority.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_authority), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_certificate_authority(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "certificate_authority.name=certificate_authority.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_certificate_authority_field_headers_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateCertificateAuthorityRequest()

    request.certificate_authority.name = "certificate_authority.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_authority), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_certificate_authority(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "certificate_authority.name=certificate_authority.name/value",
    ) in kw["metadata"]


def test_update_certificate_authority_flattened():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_authority), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_certificate_authority(
            certificate_authority=resources.CertificateAuthority(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].certificate_authority == resources.CertificateAuthority(
            name="name_value"
        )
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


def test_update_certificate_authority_flattened_error():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_certificate_authority(
            service.UpdateCertificateAuthorityRequest(),
            certificate_authority=resources.CertificateAuthority(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_certificate_authority_flattened_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_authority), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_certificate_authority(
            certificate_authority=resources.CertificateAuthority(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].certificate_authority == resources.CertificateAuthority(
            name="name_value"
        )
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_certificate_authority_flattened_error_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_certificate_authority(
            service.UpdateCertificateAuthorityRequest(),
            certificate_authority=resources.CertificateAuthority(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_create_ca_pool(
    transport: str = "grpc", request_type=service.CreateCaPoolRequest
):
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_ca_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_ca_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateCaPoolRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_ca_pool_from_dict():
    test_create_ca_pool(request_type=dict)


def test_create_ca_pool_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_ca_pool), "__call__") as call:
        client.create_ca_pool()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateCaPoolRequest()


@pytest.mark.asyncio
async def test_create_ca_pool_async(
    transport: str = "grpc_asyncio", request_type=service.CreateCaPoolRequest
):
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_ca_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_ca_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateCaPoolRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_ca_pool_async_from_dict():
    await test_create_ca_pool_async(request_type=dict)


def test_create_ca_pool_field_headers():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateCaPoolRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_ca_pool), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_ca_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_ca_pool_field_headers_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateCaPoolRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_ca_pool), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_ca_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_ca_pool_flattened():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_ca_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_ca_pool(
            parent="parent_value",
            ca_pool=resources.CaPool(name="name_value"),
            ca_pool_id="ca_pool_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].ca_pool == resources.CaPool(name="name_value")
        assert args[0].ca_pool_id == "ca_pool_id_value"


def test_create_ca_pool_flattened_error():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_ca_pool(
            service.CreateCaPoolRequest(),
            parent="parent_value",
            ca_pool=resources.CaPool(name="name_value"),
            ca_pool_id="ca_pool_id_value",
        )


@pytest.mark.asyncio
async def test_create_ca_pool_flattened_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_ca_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_ca_pool(
            parent="parent_value",
            ca_pool=resources.CaPool(name="name_value"),
            ca_pool_id="ca_pool_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].ca_pool == resources.CaPool(name="name_value")
        assert args[0].ca_pool_id == "ca_pool_id_value"


@pytest.mark.asyncio
async def test_create_ca_pool_flattened_error_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_ca_pool(
            service.CreateCaPoolRequest(),
            parent="parent_value",
            ca_pool=resources.CaPool(name="name_value"),
            ca_pool_id="ca_pool_id_value",
        )


def test_update_ca_pool(
    transport: str = "grpc", request_type=service.UpdateCaPoolRequest
):
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_ca_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_ca_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateCaPoolRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_ca_pool_from_dict():
    test_update_ca_pool(request_type=dict)


def test_update_ca_pool_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_ca_pool), "__call__") as call:
        client.update_ca_pool()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateCaPoolRequest()


@pytest.mark.asyncio
async def test_update_ca_pool_async(
    transport: str = "grpc_asyncio", request_type=service.UpdateCaPoolRequest
):
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_ca_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_ca_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateCaPoolRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_ca_pool_async_from_dict():
    await test_update_ca_pool_async(request_type=dict)


def test_update_ca_pool_field_headers():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateCaPoolRequest()

    request.ca_pool.name = "ca_pool.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_ca_pool), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_ca_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "ca_pool.name=ca_pool.name/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_update_ca_pool_field_headers_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateCaPoolRequest()

    request.ca_pool.name = "ca_pool.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_ca_pool), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_ca_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "ca_pool.name=ca_pool.name/value",) in kw[
        "metadata"
    ]


def test_update_ca_pool_flattened():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_ca_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_ca_pool(
            ca_pool=resources.CaPool(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].ca_pool == resources.CaPool(name="name_value")
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


def test_update_ca_pool_flattened_error():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_ca_pool(
            service.UpdateCaPoolRequest(),
            ca_pool=resources.CaPool(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_ca_pool_flattened_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_ca_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_ca_pool(
            ca_pool=resources.CaPool(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].ca_pool == resources.CaPool(name="name_value")
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_ca_pool_flattened_error_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_ca_pool(
            service.UpdateCaPoolRequest(),
            ca_pool=resources.CaPool(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_get_ca_pool(transport: str = "grpc", request_type=service.GetCaPoolRequest):
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_ca_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CaPool(
            name="name_value", tier=resources.CaPool.Tier.ENTERPRISE,
        )
        response = client.get_ca_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetCaPoolRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CaPool)
    assert response.name == "name_value"
    assert response.tier == resources.CaPool.Tier.ENTERPRISE


def test_get_ca_pool_from_dict():
    test_get_ca_pool(request_type=dict)


def test_get_ca_pool_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_ca_pool), "__call__") as call:
        client.get_ca_pool()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetCaPoolRequest()


@pytest.mark.asyncio
async def test_get_ca_pool_async(
    transport: str = "grpc_asyncio", request_type=service.GetCaPoolRequest
):
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_ca_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CaPool(name="name_value", tier=resources.CaPool.Tier.ENTERPRISE,)
        )
        response = await client.get_ca_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetCaPoolRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CaPool)
    assert response.name == "name_value"
    assert response.tier == resources.CaPool.Tier.ENTERPRISE


@pytest.mark.asyncio
async def test_get_ca_pool_async_from_dict():
    await test_get_ca_pool_async(request_type=dict)


def test_get_ca_pool_field_headers():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetCaPoolRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_ca_pool), "__call__") as call:
        call.return_value = resources.CaPool()
        client.get_ca_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_ca_pool_field_headers_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetCaPoolRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_ca_pool), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.CaPool())
        await client.get_ca_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_ca_pool_flattened():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_ca_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CaPool()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_ca_pool(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_ca_pool_flattened_error():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_ca_pool(
            service.GetCaPoolRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_ca_pool_flattened_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_ca_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CaPool()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.CaPool())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_ca_pool(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_ca_pool_flattened_error_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_ca_pool(
            service.GetCaPoolRequest(), name="name_value",
        )


def test_list_ca_pools(
    transport: str = "grpc", request_type=service.ListCaPoolsRequest
):
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_ca_pools), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListCaPoolsResponse(
            next_page_token="next_page_token_value", unreachable=["unreachable_value"],
        )
        response = client.list_ca_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListCaPoolsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCaPoolsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_ca_pools_from_dict():
    test_list_ca_pools(request_type=dict)


def test_list_ca_pools_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_ca_pools), "__call__") as call:
        client.list_ca_pools()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListCaPoolsRequest()


@pytest.mark.asyncio
async def test_list_ca_pools_async(
    transport: str = "grpc_asyncio", request_type=service.ListCaPoolsRequest
):
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_ca_pools), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListCaPoolsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_ca_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListCaPoolsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCaPoolsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_ca_pools_async_from_dict():
    await test_list_ca_pools_async(request_type=dict)


def test_list_ca_pools_field_headers():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListCaPoolsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_ca_pools), "__call__") as call:
        call.return_value = service.ListCaPoolsResponse()
        client.list_ca_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_ca_pools_field_headers_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListCaPoolsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_ca_pools), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListCaPoolsResponse()
        )
        await client.list_ca_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_ca_pools_flattened():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_ca_pools), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListCaPoolsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_ca_pools(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_ca_pools_flattened_error():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_ca_pools(
            service.ListCaPoolsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_ca_pools_flattened_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_ca_pools), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListCaPoolsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListCaPoolsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_ca_pools(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_ca_pools_flattened_error_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_ca_pools(
            service.ListCaPoolsRequest(), parent="parent_value",
        )


def test_list_ca_pools_pager():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_ca_pools), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListCaPoolsResponse(
                ca_pools=[resources.CaPool(), resources.CaPool(), resources.CaPool(),],
                next_page_token="abc",
            ),
            service.ListCaPoolsResponse(ca_pools=[], next_page_token="def",),
            service.ListCaPoolsResponse(
                ca_pools=[resources.CaPool(),], next_page_token="ghi",
            ),
            service.ListCaPoolsResponse(
                ca_pools=[resources.CaPool(), resources.CaPool(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_ca_pools(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, resources.CaPool) for i in results)


def test_list_ca_pools_pages():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_ca_pools), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListCaPoolsResponse(
                ca_pools=[resources.CaPool(), resources.CaPool(), resources.CaPool(),],
                next_page_token="abc",
            ),
            service.ListCaPoolsResponse(ca_pools=[], next_page_token="def",),
            service.ListCaPoolsResponse(
                ca_pools=[resources.CaPool(),], next_page_token="ghi",
            ),
            service.ListCaPoolsResponse(
                ca_pools=[resources.CaPool(), resources.CaPool(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_ca_pools(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_ca_pools_async_pager():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_ca_pools), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListCaPoolsResponse(
                ca_pools=[resources.CaPool(), resources.CaPool(), resources.CaPool(),],
                next_page_token="abc",
            ),
            service.ListCaPoolsResponse(ca_pools=[], next_page_token="def",),
            service.ListCaPoolsResponse(
                ca_pools=[resources.CaPool(),], next_page_token="ghi",
            ),
            service.ListCaPoolsResponse(
                ca_pools=[resources.CaPool(), resources.CaPool(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_ca_pools(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.CaPool) for i in responses)


@pytest.mark.asyncio
async def test_list_ca_pools_async_pages():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_ca_pools), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListCaPoolsResponse(
                ca_pools=[resources.CaPool(), resources.CaPool(), resources.CaPool(),],
                next_page_token="abc",
            ),
            service.ListCaPoolsResponse(ca_pools=[], next_page_token="def",),
            service.ListCaPoolsResponse(
                ca_pools=[resources.CaPool(),], next_page_token="ghi",
            ),
            service.ListCaPoolsResponse(
                ca_pools=[resources.CaPool(), resources.CaPool(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_ca_pools(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_delete_ca_pool(
    transport: str = "grpc", request_type=service.DeleteCaPoolRequest
):
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_ca_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_ca_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteCaPoolRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_ca_pool_from_dict():
    test_delete_ca_pool(request_type=dict)


def test_delete_ca_pool_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_ca_pool), "__call__") as call:
        client.delete_ca_pool()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteCaPoolRequest()


@pytest.mark.asyncio
async def test_delete_ca_pool_async(
    transport: str = "grpc_asyncio", request_type=service.DeleteCaPoolRequest
):
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_ca_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_ca_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteCaPoolRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_ca_pool_async_from_dict():
    await test_delete_ca_pool_async(request_type=dict)


def test_delete_ca_pool_field_headers():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.DeleteCaPoolRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_ca_pool), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_ca_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_ca_pool_field_headers_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.DeleteCaPoolRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_ca_pool), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_ca_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_ca_pool_flattened():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_ca_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_ca_pool(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_ca_pool_flattened_error():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_ca_pool(
            service.DeleteCaPoolRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_ca_pool_flattened_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_ca_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_ca_pool(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_ca_pool_flattened_error_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_ca_pool(
            service.DeleteCaPoolRequest(), name="name_value",
        )


def test_fetch_ca_certs(
    transport: str = "grpc", request_type=service.FetchCaCertsRequest
):
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_ca_certs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.FetchCaCertsResponse()
        response = client.fetch_ca_certs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.FetchCaCertsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.FetchCaCertsResponse)


def test_fetch_ca_certs_from_dict():
    test_fetch_ca_certs(request_type=dict)


def test_fetch_ca_certs_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_ca_certs), "__call__") as call:
        client.fetch_ca_certs()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.FetchCaCertsRequest()


@pytest.mark.asyncio
async def test_fetch_ca_certs_async(
    transport: str = "grpc_asyncio", request_type=service.FetchCaCertsRequest
):
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_ca_certs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.FetchCaCertsResponse()
        )
        response = await client.fetch_ca_certs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.FetchCaCertsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.FetchCaCertsResponse)


@pytest.mark.asyncio
async def test_fetch_ca_certs_async_from_dict():
    await test_fetch_ca_certs_async(request_type=dict)


def test_fetch_ca_certs_field_headers():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.FetchCaCertsRequest()

    request.ca_pool = "ca_pool/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_ca_certs), "__call__") as call:
        call.return_value = service.FetchCaCertsResponse()
        client.fetch_ca_certs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "ca_pool=ca_pool/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_fetch_ca_certs_field_headers_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.FetchCaCertsRequest()

    request.ca_pool = "ca_pool/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_ca_certs), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.FetchCaCertsResponse()
        )
        await client.fetch_ca_certs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "ca_pool=ca_pool/value",) in kw["metadata"]


def test_fetch_ca_certs_flattened():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_ca_certs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.FetchCaCertsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.fetch_ca_certs(ca_pool="ca_pool_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].ca_pool == "ca_pool_value"


def test_fetch_ca_certs_flattened_error():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.fetch_ca_certs(
            service.FetchCaCertsRequest(), ca_pool="ca_pool_value",
        )


@pytest.mark.asyncio
async def test_fetch_ca_certs_flattened_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.fetch_ca_certs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.FetchCaCertsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.FetchCaCertsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.fetch_ca_certs(ca_pool="ca_pool_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].ca_pool == "ca_pool_value"


@pytest.mark.asyncio
async def test_fetch_ca_certs_flattened_error_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.fetch_ca_certs(
            service.FetchCaCertsRequest(), ca_pool="ca_pool_value",
        )


def test_get_certificate_revocation_list(
    transport: str = "grpc", request_type=service.GetCertificateRevocationListRequest
):
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_revocation_list), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CertificateRevocationList(
            name="name_value",
            sequence_number=1601,
            pem_crl="pem_crl_value",
            access_url="access_url_value",
            state=resources.CertificateRevocationList.State.ACTIVE,
            revision_id="revision_id_value",
        )
        response = client.get_certificate_revocation_list(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetCertificateRevocationListRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CertificateRevocationList)
    assert response.name == "name_value"
    assert response.sequence_number == 1601
    assert response.pem_crl == "pem_crl_value"
    assert response.access_url == "access_url_value"
    assert response.state == resources.CertificateRevocationList.State.ACTIVE
    assert response.revision_id == "revision_id_value"


def test_get_certificate_revocation_list_from_dict():
    test_get_certificate_revocation_list(request_type=dict)


def test_get_certificate_revocation_list_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_revocation_list), "__call__"
    ) as call:
        client.get_certificate_revocation_list()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetCertificateRevocationListRequest()


@pytest.mark.asyncio
async def test_get_certificate_revocation_list_async(
    transport: str = "grpc_asyncio",
    request_type=service.GetCertificateRevocationListRequest,
):
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_revocation_list), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CertificateRevocationList(
                name="name_value",
                sequence_number=1601,
                pem_crl="pem_crl_value",
                access_url="access_url_value",
                state=resources.CertificateRevocationList.State.ACTIVE,
                revision_id="revision_id_value",
            )
        )
        response = await client.get_certificate_revocation_list(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetCertificateRevocationListRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CertificateRevocationList)
    assert response.name == "name_value"
    assert response.sequence_number == 1601
    assert response.pem_crl == "pem_crl_value"
    assert response.access_url == "access_url_value"
    assert response.state == resources.CertificateRevocationList.State.ACTIVE
    assert response.revision_id == "revision_id_value"


@pytest.mark.asyncio
async def test_get_certificate_revocation_list_async_from_dict():
    await test_get_certificate_revocation_list_async(request_type=dict)


def test_get_certificate_revocation_list_field_headers():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetCertificateRevocationListRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_revocation_list), "__call__"
    ) as call:
        call.return_value = resources.CertificateRevocationList()
        client.get_certificate_revocation_list(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_certificate_revocation_list_field_headers_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetCertificateRevocationListRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_revocation_list), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CertificateRevocationList()
        )
        await client.get_certificate_revocation_list(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_certificate_revocation_list_flattened():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_revocation_list), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CertificateRevocationList()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_certificate_revocation_list(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_certificate_revocation_list_flattened_error():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_certificate_revocation_list(
            service.GetCertificateRevocationListRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_certificate_revocation_list_flattened_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_revocation_list), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CertificateRevocationList()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CertificateRevocationList()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_certificate_revocation_list(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_certificate_revocation_list_flattened_error_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_certificate_revocation_list(
            service.GetCertificateRevocationListRequest(), name="name_value",
        )


def test_list_certificate_revocation_lists(
    transport: str = "grpc", request_type=service.ListCertificateRevocationListsRequest
):
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_revocation_lists), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListCertificateRevocationListsResponse(
            next_page_token="next_page_token_value", unreachable=["unreachable_value"],
        )
        response = client.list_certificate_revocation_lists(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListCertificateRevocationListsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCertificateRevocationListsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_certificate_revocation_lists_from_dict():
    test_list_certificate_revocation_lists(request_type=dict)


def test_list_certificate_revocation_lists_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_revocation_lists), "__call__"
    ) as call:
        client.list_certificate_revocation_lists()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListCertificateRevocationListsRequest()


@pytest.mark.asyncio
async def test_list_certificate_revocation_lists_async(
    transport: str = "grpc_asyncio",
    request_type=service.ListCertificateRevocationListsRequest,
):
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_revocation_lists), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListCertificateRevocationListsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_certificate_revocation_lists(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListCertificateRevocationListsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCertificateRevocationListsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_certificate_revocation_lists_async_from_dict():
    await test_list_certificate_revocation_lists_async(request_type=dict)


def test_list_certificate_revocation_lists_field_headers():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListCertificateRevocationListsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_revocation_lists), "__call__"
    ) as call:
        call.return_value = service.ListCertificateRevocationListsResponse()
        client.list_certificate_revocation_lists(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_certificate_revocation_lists_field_headers_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListCertificateRevocationListsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_revocation_lists), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListCertificateRevocationListsResponse()
        )
        await client.list_certificate_revocation_lists(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_certificate_revocation_lists_flattened():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_revocation_lists), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListCertificateRevocationListsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_certificate_revocation_lists(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_certificate_revocation_lists_flattened_error():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_certificate_revocation_lists(
            service.ListCertificateRevocationListsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_certificate_revocation_lists_flattened_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_revocation_lists), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListCertificateRevocationListsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListCertificateRevocationListsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_certificate_revocation_lists(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_certificate_revocation_lists_flattened_error_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_certificate_revocation_lists(
            service.ListCertificateRevocationListsRequest(), parent="parent_value",
        )


def test_list_certificate_revocation_lists_pager():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_revocation_lists), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListCertificateRevocationListsResponse(
                certificate_revocation_lists=[
                    resources.CertificateRevocationList(),
                    resources.CertificateRevocationList(),
                    resources.CertificateRevocationList(),
                ],
                next_page_token="abc",
            ),
            service.ListCertificateRevocationListsResponse(
                certificate_revocation_lists=[], next_page_token="def",
            ),
            service.ListCertificateRevocationListsResponse(
                certificate_revocation_lists=[resources.CertificateRevocationList(),],
                next_page_token="ghi",
            ),
            service.ListCertificateRevocationListsResponse(
                certificate_revocation_lists=[
                    resources.CertificateRevocationList(),
                    resources.CertificateRevocationList(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_certificate_revocation_lists(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, resources.CertificateRevocationList) for i in results)


def test_list_certificate_revocation_lists_pages():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_revocation_lists), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListCertificateRevocationListsResponse(
                certificate_revocation_lists=[
                    resources.CertificateRevocationList(),
                    resources.CertificateRevocationList(),
                    resources.CertificateRevocationList(),
                ],
                next_page_token="abc",
            ),
            service.ListCertificateRevocationListsResponse(
                certificate_revocation_lists=[], next_page_token="def",
            ),
            service.ListCertificateRevocationListsResponse(
                certificate_revocation_lists=[resources.CertificateRevocationList(),],
                next_page_token="ghi",
            ),
            service.ListCertificateRevocationListsResponse(
                certificate_revocation_lists=[
                    resources.CertificateRevocationList(),
                    resources.CertificateRevocationList(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_certificate_revocation_lists(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_certificate_revocation_lists_async_pager():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_revocation_lists),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListCertificateRevocationListsResponse(
                certificate_revocation_lists=[
                    resources.CertificateRevocationList(),
                    resources.CertificateRevocationList(),
                    resources.CertificateRevocationList(),
                ],
                next_page_token="abc",
            ),
            service.ListCertificateRevocationListsResponse(
                certificate_revocation_lists=[], next_page_token="def",
            ),
            service.ListCertificateRevocationListsResponse(
                certificate_revocation_lists=[resources.CertificateRevocationList(),],
                next_page_token="ghi",
            ),
            service.ListCertificateRevocationListsResponse(
                certificate_revocation_lists=[
                    resources.CertificateRevocationList(),
                    resources.CertificateRevocationList(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_certificate_revocation_lists(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, resources.CertificateRevocationList) for i in responses
        )


@pytest.mark.asyncio
async def test_list_certificate_revocation_lists_async_pages():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_revocation_lists),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListCertificateRevocationListsResponse(
                certificate_revocation_lists=[
                    resources.CertificateRevocationList(),
                    resources.CertificateRevocationList(),
                    resources.CertificateRevocationList(),
                ],
                next_page_token="abc",
            ),
            service.ListCertificateRevocationListsResponse(
                certificate_revocation_lists=[], next_page_token="def",
            ),
            service.ListCertificateRevocationListsResponse(
                certificate_revocation_lists=[resources.CertificateRevocationList(),],
                next_page_token="ghi",
            ),
            service.ListCertificateRevocationListsResponse(
                certificate_revocation_lists=[
                    resources.CertificateRevocationList(),
                    resources.CertificateRevocationList(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_certificate_revocation_lists(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_update_certificate_revocation_list(
    transport: str = "grpc", request_type=service.UpdateCertificateRevocationListRequest
):
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_revocation_list), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_certificate_revocation_list(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateCertificateRevocationListRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_certificate_revocation_list_from_dict():
    test_update_certificate_revocation_list(request_type=dict)


def test_update_certificate_revocation_list_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_revocation_list), "__call__"
    ) as call:
        client.update_certificate_revocation_list()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateCertificateRevocationListRequest()


@pytest.mark.asyncio
async def test_update_certificate_revocation_list_async(
    transport: str = "grpc_asyncio",
    request_type=service.UpdateCertificateRevocationListRequest,
):
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_revocation_list), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_certificate_revocation_list(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateCertificateRevocationListRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_certificate_revocation_list_async_from_dict():
    await test_update_certificate_revocation_list_async(request_type=dict)


def test_update_certificate_revocation_list_field_headers():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateCertificateRevocationListRequest()

    request.certificate_revocation_list.name = "certificate_revocation_list.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_revocation_list), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_certificate_revocation_list(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "certificate_revocation_list.name=certificate_revocation_list.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_certificate_revocation_list_field_headers_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateCertificateRevocationListRequest()

    request.certificate_revocation_list.name = "certificate_revocation_list.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_revocation_list), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_certificate_revocation_list(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "certificate_revocation_list.name=certificate_revocation_list.name/value",
    ) in kw["metadata"]


def test_update_certificate_revocation_list_flattened():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_revocation_list), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_certificate_revocation_list(
            certificate_revocation_list=resources.CertificateRevocationList(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[
            0
        ].certificate_revocation_list == resources.CertificateRevocationList(
            name="name_value"
        )
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


def test_update_certificate_revocation_list_flattened_error():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_certificate_revocation_list(
            service.UpdateCertificateRevocationListRequest(),
            certificate_revocation_list=resources.CertificateRevocationList(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_certificate_revocation_list_flattened_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_revocation_list), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_certificate_revocation_list(
            certificate_revocation_list=resources.CertificateRevocationList(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[
            0
        ].certificate_revocation_list == resources.CertificateRevocationList(
            name="name_value"
        )
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_certificate_revocation_list_flattened_error_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_certificate_revocation_list(
            service.UpdateCertificateRevocationListRequest(),
            certificate_revocation_list=resources.CertificateRevocationList(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_create_certificate_template(
    transport: str = "grpc", request_type=service.CreateCertificateTemplateRequest
):
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_certificate_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateCertificateTemplateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_certificate_template_from_dict():
    test_create_certificate_template(request_type=dict)


def test_create_certificate_template_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_template), "__call__"
    ) as call:
        client.create_certificate_template()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateCertificateTemplateRequest()


@pytest.mark.asyncio
async def test_create_certificate_template_async(
    transport: str = "grpc_asyncio",
    request_type=service.CreateCertificateTemplateRequest,
):
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_certificate_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateCertificateTemplateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_certificate_template_async_from_dict():
    await test_create_certificate_template_async(request_type=dict)


def test_create_certificate_template_field_headers():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateCertificateTemplateRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_template), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_certificate_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_certificate_template_field_headers_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateCertificateTemplateRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_template), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_certificate_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_certificate_template_flattened():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_certificate_template(
            parent="parent_value",
            certificate_template=resources.CertificateTemplate(name="name_value"),
            certificate_template_id="certificate_template_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].certificate_template == resources.CertificateTemplate(
            name="name_value"
        )
        assert args[0].certificate_template_id == "certificate_template_id_value"


def test_create_certificate_template_flattened_error():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_certificate_template(
            service.CreateCertificateTemplateRequest(),
            parent="parent_value",
            certificate_template=resources.CertificateTemplate(name="name_value"),
            certificate_template_id="certificate_template_id_value",
        )


@pytest.mark.asyncio
async def test_create_certificate_template_flattened_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_certificate_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_certificate_template(
            parent="parent_value",
            certificate_template=resources.CertificateTemplate(name="name_value"),
            certificate_template_id="certificate_template_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].certificate_template == resources.CertificateTemplate(
            name="name_value"
        )
        assert args[0].certificate_template_id == "certificate_template_id_value"


@pytest.mark.asyncio
async def test_create_certificate_template_flattened_error_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_certificate_template(
            service.CreateCertificateTemplateRequest(),
            parent="parent_value",
            certificate_template=resources.CertificateTemplate(name="name_value"),
            certificate_template_id="certificate_template_id_value",
        )


def test_delete_certificate_template(
    transport: str = "grpc", request_type=service.DeleteCertificateTemplateRequest
):
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_certificate_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteCertificateTemplateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_certificate_template_from_dict():
    test_delete_certificate_template(request_type=dict)


def test_delete_certificate_template_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_template), "__call__"
    ) as call:
        client.delete_certificate_template()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteCertificateTemplateRequest()


@pytest.mark.asyncio
async def test_delete_certificate_template_async(
    transport: str = "grpc_asyncio",
    request_type=service.DeleteCertificateTemplateRequest,
):
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_certificate_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteCertificateTemplateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_certificate_template_async_from_dict():
    await test_delete_certificate_template_async(request_type=dict)


def test_delete_certificate_template_field_headers():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.DeleteCertificateTemplateRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_template), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_certificate_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_certificate_template_field_headers_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.DeleteCertificateTemplateRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_template), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_certificate_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_certificate_template_flattened():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_certificate_template(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_certificate_template_flattened_error():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_certificate_template(
            service.DeleteCertificateTemplateRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_certificate_template_flattened_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_certificate_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_certificate_template(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_certificate_template_flattened_error_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_certificate_template(
            service.DeleteCertificateTemplateRequest(), name="name_value",
        )


def test_get_certificate_template(
    transport: str = "grpc", request_type=service.GetCertificateTemplateRequest
):
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CertificateTemplate(
            name="name_value", description="description_value",
        )
        response = client.get_certificate_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetCertificateTemplateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CertificateTemplate)
    assert response.name == "name_value"
    assert response.description == "description_value"


def test_get_certificate_template_from_dict():
    test_get_certificate_template(request_type=dict)


def test_get_certificate_template_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_template), "__call__"
    ) as call:
        client.get_certificate_template()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetCertificateTemplateRequest()


@pytest.mark.asyncio
async def test_get_certificate_template_async(
    transport: str = "grpc_asyncio", request_type=service.GetCertificateTemplateRequest
):
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CertificateTemplate(
                name="name_value", description="description_value",
            )
        )
        response = await client.get_certificate_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetCertificateTemplateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CertificateTemplate)
    assert response.name == "name_value"
    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_get_certificate_template_async_from_dict():
    await test_get_certificate_template_async(request_type=dict)


def test_get_certificate_template_field_headers():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetCertificateTemplateRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_template), "__call__"
    ) as call:
        call.return_value = resources.CertificateTemplate()
        client.get_certificate_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_certificate_template_field_headers_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetCertificateTemplateRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_template), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CertificateTemplate()
        )
        await client.get_certificate_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_certificate_template_flattened():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CertificateTemplate()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_certificate_template(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_certificate_template_flattened_error():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_certificate_template(
            service.GetCertificateTemplateRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_certificate_template_flattened_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_certificate_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CertificateTemplate()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.CertificateTemplate()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_certificate_template(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_certificate_template_flattened_error_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_certificate_template(
            service.GetCertificateTemplateRequest(), name="name_value",
        )


def test_list_certificate_templates(
    transport: str = "grpc", request_type=service.ListCertificateTemplatesRequest
):
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_templates), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListCertificateTemplatesResponse(
            next_page_token="next_page_token_value", unreachable=["unreachable_value"],
        )
        response = client.list_certificate_templates(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListCertificateTemplatesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCertificateTemplatesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_certificate_templates_from_dict():
    test_list_certificate_templates(request_type=dict)


def test_list_certificate_templates_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_templates), "__call__"
    ) as call:
        client.list_certificate_templates()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListCertificateTemplatesRequest()


@pytest.mark.asyncio
async def test_list_certificate_templates_async(
    transport: str = "grpc_asyncio",
    request_type=service.ListCertificateTemplatesRequest,
):
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_templates), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListCertificateTemplatesResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_certificate_templates(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListCertificateTemplatesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCertificateTemplatesAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_certificate_templates_async_from_dict():
    await test_list_certificate_templates_async(request_type=dict)


def test_list_certificate_templates_field_headers():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListCertificateTemplatesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_templates), "__call__"
    ) as call:
        call.return_value = service.ListCertificateTemplatesResponse()
        client.list_certificate_templates(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_certificate_templates_field_headers_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListCertificateTemplatesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_templates), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListCertificateTemplatesResponse()
        )
        await client.list_certificate_templates(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_certificate_templates_flattened():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_templates), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListCertificateTemplatesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_certificate_templates(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_certificate_templates_flattened_error():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_certificate_templates(
            service.ListCertificateTemplatesRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_certificate_templates_flattened_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_templates), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListCertificateTemplatesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListCertificateTemplatesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_certificate_templates(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_certificate_templates_flattened_error_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_certificate_templates(
            service.ListCertificateTemplatesRequest(), parent="parent_value",
        )


def test_list_certificate_templates_pager():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_templates), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListCertificateTemplatesResponse(
                certificate_templates=[
                    resources.CertificateTemplate(),
                    resources.CertificateTemplate(),
                    resources.CertificateTemplate(),
                ],
                next_page_token="abc",
            ),
            service.ListCertificateTemplatesResponse(
                certificate_templates=[], next_page_token="def",
            ),
            service.ListCertificateTemplatesResponse(
                certificate_templates=[resources.CertificateTemplate(),],
                next_page_token="ghi",
            ),
            service.ListCertificateTemplatesResponse(
                certificate_templates=[
                    resources.CertificateTemplate(),
                    resources.CertificateTemplate(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_certificate_templates(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, resources.CertificateTemplate) for i in results)


def test_list_certificate_templates_pages():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_templates), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListCertificateTemplatesResponse(
                certificate_templates=[
                    resources.CertificateTemplate(),
                    resources.CertificateTemplate(),
                    resources.CertificateTemplate(),
                ],
                next_page_token="abc",
            ),
            service.ListCertificateTemplatesResponse(
                certificate_templates=[], next_page_token="def",
            ),
            service.ListCertificateTemplatesResponse(
                certificate_templates=[resources.CertificateTemplate(),],
                next_page_token="ghi",
            ),
            service.ListCertificateTemplatesResponse(
                certificate_templates=[
                    resources.CertificateTemplate(),
                    resources.CertificateTemplate(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_certificate_templates(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_certificate_templates_async_pager():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_templates),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListCertificateTemplatesResponse(
                certificate_templates=[
                    resources.CertificateTemplate(),
                    resources.CertificateTemplate(),
                    resources.CertificateTemplate(),
                ],
                next_page_token="abc",
            ),
            service.ListCertificateTemplatesResponse(
                certificate_templates=[], next_page_token="def",
            ),
            service.ListCertificateTemplatesResponse(
                certificate_templates=[resources.CertificateTemplate(),],
                next_page_token="ghi",
            ),
            service.ListCertificateTemplatesResponse(
                certificate_templates=[
                    resources.CertificateTemplate(),
                    resources.CertificateTemplate(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_certificate_templates(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.CertificateTemplate) for i in responses)


@pytest.mark.asyncio
async def test_list_certificate_templates_async_pages():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_certificate_templates),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListCertificateTemplatesResponse(
                certificate_templates=[
                    resources.CertificateTemplate(),
                    resources.CertificateTemplate(),
                    resources.CertificateTemplate(),
                ],
                next_page_token="abc",
            ),
            service.ListCertificateTemplatesResponse(
                certificate_templates=[], next_page_token="def",
            ),
            service.ListCertificateTemplatesResponse(
                certificate_templates=[resources.CertificateTemplate(),],
                next_page_token="ghi",
            ),
            service.ListCertificateTemplatesResponse(
                certificate_templates=[
                    resources.CertificateTemplate(),
                    resources.CertificateTemplate(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_certificate_templates(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_update_certificate_template(
    transport: str = "grpc", request_type=service.UpdateCertificateTemplateRequest
):
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_certificate_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateCertificateTemplateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_certificate_template_from_dict():
    test_update_certificate_template(request_type=dict)


def test_update_certificate_template_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_template), "__call__"
    ) as call:
        client.update_certificate_template()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateCertificateTemplateRequest()


@pytest.mark.asyncio
async def test_update_certificate_template_async(
    transport: str = "grpc_asyncio",
    request_type=service.UpdateCertificateTemplateRequest,
):
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_certificate_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateCertificateTemplateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_certificate_template_async_from_dict():
    await test_update_certificate_template_async(request_type=dict)


def test_update_certificate_template_field_headers():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateCertificateTemplateRequest()

    request.certificate_template.name = "certificate_template.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_template), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_certificate_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "certificate_template.name=certificate_template.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_certificate_template_field_headers_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateCertificateTemplateRequest()

    request.certificate_template.name = "certificate_template.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_template), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_certificate_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "certificate_template.name=certificate_template.name/value",
    ) in kw["metadata"]


def test_update_certificate_template_flattened():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_certificate_template(
            certificate_template=resources.CertificateTemplate(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].certificate_template == resources.CertificateTemplate(
            name="name_value"
        )
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


def test_update_certificate_template_flattened_error():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_certificate_template(
            service.UpdateCertificateTemplateRequest(),
            certificate_template=resources.CertificateTemplate(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_certificate_template_flattened_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_certificate_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_certificate_template(
            certificate_template=resources.CertificateTemplate(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].certificate_template == resources.CertificateTemplate(
            name="name_value"
        )
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_certificate_template_flattened_error_async():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_certificate_template(
            service.UpdateCertificateTemplateRequest(),
            certificate_template=resources.CertificateTemplate(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.CertificateAuthorityServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CertificateAuthorityServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.CertificateAuthorityServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CertificateAuthorityServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.CertificateAuthorityServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CertificateAuthorityServiceClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.CertificateAuthorityServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = CertificateAuthorityServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.CertificateAuthorityServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.CertificateAuthorityServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CertificateAuthorityServiceGrpcTransport,
        transports.CertificateAuthorityServiceGrpcAsyncIOTransport,
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
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport, transports.CertificateAuthorityServiceGrpcTransport,
    )


def test_certificate_authority_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.CertificateAuthorityServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_certificate_authority_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.security.privateca_v1.services.certificate_authority_service.transports.CertificateAuthorityServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.CertificateAuthorityServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_certificate",
        "get_certificate",
        "list_certificates",
        "revoke_certificate",
        "update_certificate",
        "activate_certificate_authority",
        "create_certificate_authority",
        "disable_certificate_authority",
        "enable_certificate_authority",
        "fetch_certificate_authority_csr",
        "get_certificate_authority",
        "list_certificate_authorities",
        "undelete_certificate_authority",
        "delete_certificate_authority",
        "update_certificate_authority",
        "create_ca_pool",
        "update_ca_pool",
        "get_ca_pool",
        "list_ca_pools",
        "delete_ca_pool",
        "fetch_ca_certs",
        "get_certificate_revocation_list",
        "list_certificate_revocation_lists",
        "update_certificate_revocation_list",
        "create_certificate_template",
        "delete_certificate_template",
        "get_certificate_template",
        "list_certificate_templates",
        "update_certificate_template",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client


@requires_google_auth_gte_1_25_0
def test_certificate_authority_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.security.privateca_v1.services.certificate_authority_service.transports.CertificateAuthorityServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.CertificateAuthorityServiceTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


@requires_google_auth_lt_1_25_0
def test_certificate_authority_service_base_transport_with_credentials_file_old_google_auth():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.security.privateca_v1.services.certificate_authority_service.transports.CertificateAuthorityServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.CertificateAuthorityServiceTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_certificate_authority_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.security.privateca_v1.services.certificate_authority_service.transports.CertificateAuthorityServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.CertificateAuthorityServiceTransport()
        adc.assert_called_once()


@requires_google_auth_gte_1_25_0
def test_certificate_authority_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        CertificateAuthorityServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@requires_google_auth_lt_1_25_0
def test_certificate_authority_service_auth_adc_old_google_auth():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        CertificateAuthorityServiceClient()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CertificateAuthorityServiceGrpcTransport,
        transports.CertificateAuthorityServiceGrpcAsyncIOTransport,
    ],
)
@requires_google_auth_gte_1_25_0
def test_certificate_authority_service_transport_auth_adc(transport_class):
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
        transports.CertificateAuthorityServiceGrpcTransport,
        transports.CertificateAuthorityServiceGrpcAsyncIOTransport,
    ],
)
@requires_google_auth_lt_1_25_0
def test_certificate_authority_service_transport_auth_adc_old_google_auth(
    transport_class,
):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus")
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.CertificateAuthorityServiceGrpcTransport, grpc_helpers),
        (
            transports.CertificateAuthorityServiceGrpcAsyncIOTransport,
            grpc_helpers_async,
        ),
    ],
)
def test_certificate_authority_service_transport_create_channel(
    transport_class, grpc_helpers
):
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
            "privateca.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="privateca.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CertificateAuthorityServiceGrpcTransport,
        transports.CertificateAuthorityServiceGrpcAsyncIOTransport,
    ],
)
def test_certificate_authority_service_grpc_transport_client_cert_source_for_mtls(
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


def test_certificate_authority_service_host_no_port():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="privateca.googleapis.com"
        ),
    )
    assert client.transport._host == "privateca.googleapis.com:443"


def test_certificate_authority_service_host_with_port():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="privateca.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "privateca.googleapis.com:8000"


def test_certificate_authority_service_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.CertificateAuthorityServiceGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_certificate_authority_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.CertificateAuthorityServiceGrpcAsyncIOTransport(
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
        transports.CertificateAuthorityServiceGrpcTransport,
        transports.CertificateAuthorityServiceGrpcAsyncIOTransport,
    ],
)
def test_certificate_authority_service_transport_channel_mtls_with_client_cert_source(
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
        transports.CertificateAuthorityServiceGrpcTransport,
        transports.CertificateAuthorityServiceGrpcAsyncIOTransport,
    ],
)
def test_certificate_authority_service_transport_channel_mtls_with_adc(transport_class):
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


def test_certificate_authority_service_grpc_lro_client():
    client = CertificateAuthorityServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_certificate_authority_service_grpc_lro_async_client():
    client = CertificateAuthorityServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc_asyncio",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsAsyncClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_ca_pool_path():
    project = "squid"
    location = "clam"
    ca_pool = "whelk"
    expected = "projects/{project}/locations/{location}/caPools/{ca_pool}".format(
        project=project, location=location, ca_pool=ca_pool,
    )
    actual = CertificateAuthorityServiceClient.ca_pool_path(project, location, ca_pool)
    assert expected == actual


def test_parse_ca_pool_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "ca_pool": "nudibranch",
    }
    path = CertificateAuthorityServiceClient.ca_pool_path(**expected)

    # Check that the path construction is reversible.
    actual = CertificateAuthorityServiceClient.parse_ca_pool_path(path)
    assert expected == actual


def test_certificate_path():
    project = "cuttlefish"
    location = "mussel"
    ca_pool = "winkle"
    certificate = "nautilus"
    expected = "projects/{project}/locations/{location}/caPools/{ca_pool}/certificates/{certificate}".format(
        project=project, location=location, ca_pool=ca_pool, certificate=certificate,
    )
    actual = CertificateAuthorityServiceClient.certificate_path(
        project, location, ca_pool, certificate
    )
    assert expected == actual


def test_parse_certificate_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
        "ca_pool": "squid",
        "certificate": "clam",
    }
    path = CertificateAuthorityServiceClient.certificate_path(**expected)

    # Check that the path construction is reversible.
    actual = CertificateAuthorityServiceClient.parse_certificate_path(path)
    assert expected == actual


def test_certificate_authority_path():
    project = "whelk"
    location = "octopus"
    ca_pool = "oyster"
    certificate_authority = "nudibranch"
    expected = "projects/{project}/locations/{location}/caPools/{ca_pool}/certificateAuthorities/{certificate_authority}".format(
        project=project,
        location=location,
        ca_pool=ca_pool,
        certificate_authority=certificate_authority,
    )
    actual = CertificateAuthorityServiceClient.certificate_authority_path(
        project, location, ca_pool, certificate_authority
    )
    assert expected == actual


def test_parse_certificate_authority_path():
    expected = {
        "project": "cuttlefish",
        "location": "mussel",
        "ca_pool": "winkle",
        "certificate_authority": "nautilus",
    }
    path = CertificateAuthorityServiceClient.certificate_authority_path(**expected)

    # Check that the path construction is reversible.
    actual = CertificateAuthorityServiceClient.parse_certificate_authority_path(path)
    assert expected == actual


def test_certificate_revocation_list_path():
    project = "scallop"
    location = "abalone"
    ca_pool = "squid"
    certificate_authority = "clam"
    certificate_revocation_list = "whelk"
    expected = "projects/{project}/locations/{location}/caPools/{ca_pool}/certificateAuthorities/{certificate_authority}/certificateRevocationLists/{certificate_revocation_list}".format(
        project=project,
        location=location,
        ca_pool=ca_pool,
        certificate_authority=certificate_authority,
        certificate_revocation_list=certificate_revocation_list,
    )
    actual = CertificateAuthorityServiceClient.certificate_revocation_list_path(
        project, location, ca_pool, certificate_authority, certificate_revocation_list
    )
    assert expected == actual


def test_parse_certificate_revocation_list_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "ca_pool": "nudibranch",
        "certificate_authority": "cuttlefish",
        "certificate_revocation_list": "mussel",
    }
    path = CertificateAuthorityServiceClient.certificate_revocation_list_path(
        **expected
    )

    # Check that the path construction is reversible.
    actual = CertificateAuthorityServiceClient.parse_certificate_revocation_list_path(
        path
    )
    assert expected == actual


def test_certificate_template_path():
    project = "winkle"
    location = "nautilus"
    certificate_template = "scallop"
    expected = "projects/{project}/locations/{location}/certificateTemplates/{certificate_template}".format(
        project=project, location=location, certificate_template=certificate_template,
    )
    actual = CertificateAuthorityServiceClient.certificate_template_path(
        project, location, certificate_template
    )
    assert expected == actual


def test_parse_certificate_template_path():
    expected = {
        "project": "abalone",
        "location": "squid",
        "certificate_template": "clam",
    }
    path = CertificateAuthorityServiceClient.certificate_template_path(**expected)

    # Check that the path construction is reversible.
    actual = CertificateAuthorityServiceClient.parse_certificate_template_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "whelk"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = CertificateAuthorityServiceClient.common_billing_account_path(
        billing_account
    )
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "octopus",
    }
    path = CertificateAuthorityServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = CertificateAuthorityServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "oyster"
    expected = "folders/{folder}".format(folder=folder,)
    actual = CertificateAuthorityServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nudibranch",
    }
    path = CertificateAuthorityServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = CertificateAuthorityServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "cuttlefish"
    expected = "organizations/{organization}".format(organization=organization,)
    actual = CertificateAuthorityServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "mussel",
    }
    path = CertificateAuthorityServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = CertificateAuthorityServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "winkle"
    expected = "projects/{project}".format(project=project,)
    actual = CertificateAuthorityServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nautilus",
    }
    path = CertificateAuthorityServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = CertificateAuthorityServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "scallop"
    location = "abalone"
    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = CertificateAuthorityServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "squid",
        "location": "clam",
    }
    path = CertificateAuthorityServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = CertificateAuthorityServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.CertificateAuthorityServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = CertificateAuthorityServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.CertificateAuthorityServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = CertificateAuthorityServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
