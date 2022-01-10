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
from google.cloud.recaptchaenterprise_v1.services.recaptcha_enterprise_service import (
    RecaptchaEnterpriseServiceAsyncClient,
)
from google.cloud.recaptchaenterprise_v1.services.recaptcha_enterprise_service import (
    RecaptchaEnterpriseServiceClient,
)
from google.cloud.recaptchaenterprise_v1.services.recaptcha_enterprise_service import (
    pagers,
)
from google.cloud.recaptchaenterprise_v1.services.recaptcha_enterprise_service import (
    transports,
)
from google.cloud.recaptchaenterprise_v1.types import recaptchaenterprise
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

    assert RecaptchaEnterpriseServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        RecaptchaEnterpriseServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        RecaptchaEnterpriseServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        RecaptchaEnterpriseServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        RecaptchaEnterpriseServiceClient._get_default_mtls_endpoint(
            sandbox_mtls_endpoint
        )
        == sandbox_mtls_endpoint
    )
    assert (
        RecaptchaEnterpriseServiceClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class",
    [RecaptchaEnterpriseServiceClient, RecaptchaEnterpriseServiceAsyncClient,],
)
def test_recaptcha_enterprise_service_client_from_service_account_info(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "recaptchaenterprise.googleapis.com:443"


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.RecaptchaEnterpriseServiceGrpcTransport, "grpc"),
        (transports.RecaptchaEnterpriseServiceGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_recaptcha_enterprise_service_client_service_account_always_use_jwt(
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
    [RecaptchaEnterpriseServiceClient, RecaptchaEnterpriseServiceAsyncClient,],
)
def test_recaptcha_enterprise_service_client_from_service_account_file(client_class):
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

        assert client.transport._host == "recaptchaenterprise.googleapis.com:443"


def test_recaptcha_enterprise_service_client_get_transport_class():
    transport = RecaptchaEnterpriseServiceClient.get_transport_class()
    available_transports = [
        transports.RecaptchaEnterpriseServiceGrpcTransport,
    ]
    assert transport in available_transports

    transport = RecaptchaEnterpriseServiceClient.get_transport_class("grpc")
    assert transport == transports.RecaptchaEnterpriseServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            RecaptchaEnterpriseServiceClient,
            transports.RecaptchaEnterpriseServiceGrpcTransport,
            "grpc",
        ),
        (
            RecaptchaEnterpriseServiceAsyncClient,
            transports.RecaptchaEnterpriseServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    RecaptchaEnterpriseServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(RecaptchaEnterpriseServiceClient),
)
@mock.patch.object(
    RecaptchaEnterpriseServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(RecaptchaEnterpriseServiceAsyncClient),
)
def test_recaptcha_enterprise_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(
        RecaptchaEnterpriseServiceClient, "get_transport_class"
    ) as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(
        RecaptchaEnterpriseServiceClient, "get_transport_class"
    ) as gtc:
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
            RecaptchaEnterpriseServiceClient,
            transports.RecaptchaEnterpriseServiceGrpcTransport,
            "grpc",
            "true",
        ),
        (
            RecaptchaEnterpriseServiceAsyncClient,
            transports.RecaptchaEnterpriseServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            RecaptchaEnterpriseServiceClient,
            transports.RecaptchaEnterpriseServiceGrpcTransport,
            "grpc",
            "false",
        ),
        (
            RecaptchaEnterpriseServiceAsyncClient,
            transports.RecaptchaEnterpriseServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    RecaptchaEnterpriseServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(RecaptchaEnterpriseServiceClient),
)
@mock.patch.object(
    RecaptchaEnterpriseServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(RecaptchaEnterpriseServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_recaptcha_enterprise_service_client_mtls_env_auto(
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
    "client_class,transport_class,transport_name",
    [
        (
            RecaptchaEnterpriseServiceClient,
            transports.RecaptchaEnterpriseServiceGrpcTransport,
            "grpc",
        ),
        (
            RecaptchaEnterpriseServiceAsyncClient,
            transports.RecaptchaEnterpriseServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_recaptcha_enterprise_service_client_client_options_scopes(
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
    "client_class,transport_class,transport_name",
    [
        (
            RecaptchaEnterpriseServiceClient,
            transports.RecaptchaEnterpriseServiceGrpcTransport,
            "grpc",
        ),
        (
            RecaptchaEnterpriseServiceAsyncClient,
            transports.RecaptchaEnterpriseServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_recaptcha_enterprise_service_client_client_options_credentials_file(
    client_class, transport_class, transport_name
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


def test_recaptcha_enterprise_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.recaptchaenterprise_v1.services.recaptcha_enterprise_service.transports.RecaptchaEnterpriseServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = RecaptchaEnterpriseServiceClient(
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
    "request_type", [recaptchaenterprise.CreateAssessmentRequest, dict,]
)
def test_create_assessment(request_type, transport: str = "grpc"):
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_assessment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = recaptchaenterprise.Assessment(name="name_value",)
        response = client.create_assessment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == recaptchaenterprise.CreateAssessmentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, recaptchaenterprise.Assessment)
    assert response.name == "name_value"


def test_create_assessment_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_assessment), "__call__"
    ) as call:
        client.create_assessment()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == recaptchaenterprise.CreateAssessmentRequest()


@pytest.mark.asyncio
async def test_create_assessment_async(
    transport: str = "grpc_asyncio",
    request_type=recaptchaenterprise.CreateAssessmentRequest,
):
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_assessment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recaptchaenterprise.Assessment(name="name_value",)
        )
        response = await client.create_assessment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == recaptchaenterprise.CreateAssessmentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, recaptchaenterprise.Assessment)
    assert response.name == "name_value"


@pytest.mark.asyncio
async def test_create_assessment_async_from_dict():
    await test_create_assessment_async(request_type=dict)


def test_create_assessment_field_headers():
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recaptchaenterprise.CreateAssessmentRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_assessment), "__call__"
    ) as call:
        call.return_value = recaptchaenterprise.Assessment()
        client.create_assessment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_assessment_field_headers_async():
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recaptchaenterprise.CreateAssessmentRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_assessment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recaptchaenterprise.Assessment()
        )
        await client.create_assessment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_assessment_flattened():
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_assessment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = recaptchaenterprise.Assessment()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_assessment(
            parent="parent_value",
            assessment=recaptchaenterprise.Assessment(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].assessment
        mock_val = recaptchaenterprise.Assessment(name="name_value")
        assert arg == mock_val


def test_create_assessment_flattened_error():
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_assessment(
            recaptchaenterprise.CreateAssessmentRequest(),
            parent="parent_value",
            assessment=recaptchaenterprise.Assessment(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_assessment_flattened_async():
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_assessment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = recaptchaenterprise.Assessment()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recaptchaenterprise.Assessment()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_assessment(
            parent="parent_value",
            assessment=recaptchaenterprise.Assessment(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].assessment
        mock_val = recaptchaenterprise.Assessment(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_assessment_flattened_error_async():
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_assessment(
            recaptchaenterprise.CreateAssessmentRequest(),
            parent="parent_value",
            assessment=recaptchaenterprise.Assessment(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type", [recaptchaenterprise.AnnotateAssessmentRequest, dict,]
)
def test_annotate_assessment(request_type, transport: str = "grpc"):
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.annotate_assessment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = recaptchaenterprise.AnnotateAssessmentResponse()
        response = client.annotate_assessment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == recaptchaenterprise.AnnotateAssessmentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, recaptchaenterprise.AnnotateAssessmentResponse)


def test_annotate_assessment_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.annotate_assessment), "__call__"
    ) as call:
        client.annotate_assessment()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == recaptchaenterprise.AnnotateAssessmentRequest()


@pytest.mark.asyncio
async def test_annotate_assessment_async(
    transport: str = "grpc_asyncio",
    request_type=recaptchaenterprise.AnnotateAssessmentRequest,
):
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.annotate_assessment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recaptchaenterprise.AnnotateAssessmentResponse()
        )
        response = await client.annotate_assessment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == recaptchaenterprise.AnnotateAssessmentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, recaptchaenterprise.AnnotateAssessmentResponse)


@pytest.mark.asyncio
async def test_annotate_assessment_async_from_dict():
    await test_annotate_assessment_async(request_type=dict)


def test_annotate_assessment_field_headers():
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recaptchaenterprise.AnnotateAssessmentRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.annotate_assessment), "__call__"
    ) as call:
        call.return_value = recaptchaenterprise.AnnotateAssessmentResponse()
        client.annotate_assessment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_annotate_assessment_field_headers_async():
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recaptchaenterprise.AnnotateAssessmentRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.annotate_assessment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recaptchaenterprise.AnnotateAssessmentResponse()
        )
        await client.annotate_assessment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_annotate_assessment_flattened():
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.annotate_assessment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = recaptchaenterprise.AnnotateAssessmentResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.annotate_assessment(
            name="name_value",
            annotation=recaptchaenterprise.AnnotateAssessmentRequest.Annotation.LEGITIMATE,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].annotation
        mock_val = recaptchaenterprise.AnnotateAssessmentRequest.Annotation.LEGITIMATE
        assert arg == mock_val


def test_annotate_assessment_flattened_error():
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.annotate_assessment(
            recaptchaenterprise.AnnotateAssessmentRequest(),
            name="name_value",
            annotation=recaptchaenterprise.AnnotateAssessmentRequest.Annotation.LEGITIMATE,
        )


@pytest.mark.asyncio
async def test_annotate_assessment_flattened_async():
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.annotate_assessment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = recaptchaenterprise.AnnotateAssessmentResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recaptchaenterprise.AnnotateAssessmentResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.annotate_assessment(
            name="name_value",
            annotation=recaptchaenterprise.AnnotateAssessmentRequest.Annotation.LEGITIMATE,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].annotation
        mock_val = recaptchaenterprise.AnnotateAssessmentRequest.Annotation.LEGITIMATE
        assert arg == mock_val


@pytest.mark.asyncio
async def test_annotate_assessment_flattened_error_async():
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.annotate_assessment(
            recaptchaenterprise.AnnotateAssessmentRequest(),
            name="name_value",
            annotation=recaptchaenterprise.AnnotateAssessmentRequest.Annotation.LEGITIMATE,
        )


@pytest.mark.parametrize("request_type", [recaptchaenterprise.CreateKeyRequest, dict,])
def test_create_key(request_type, transport: str = "grpc"):
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = recaptchaenterprise.Key(
            name="name_value",
            display_name="display_name_value",
            web_settings=recaptchaenterprise.WebKeySettings(allow_all_domains=True),
        )
        response = client.create_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == recaptchaenterprise.CreateKeyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, recaptchaenterprise.Key)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"


def test_create_key_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_key), "__call__") as call:
        client.create_key()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == recaptchaenterprise.CreateKeyRequest()


@pytest.mark.asyncio
async def test_create_key_async(
    transport: str = "grpc_asyncio", request_type=recaptchaenterprise.CreateKeyRequest
):
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recaptchaenterprise.Key(
                name="name_value", display_name="display_name_value",
            )
        )
        response = await client.create_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == recaptchaenterprise.CreateKeyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, recaptchaenterprise.Key)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"


@pytest.mark.asyncio
async def test_create_key_async_from_dict():
    await test_create_key_async(request_type=dict)


def test_create_key_field_headers():
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recaptchaenterprise.CreateKeyRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_key), "__call__") as call:
        call.return_value = recaptchaenterprise.Key()
        client.create_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_key_field_headers_async():
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recaptchaenterprise.CreateKeyRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_key), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recaptchaenterprise.Key()
        )
        await client.create_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.parametrize("request_type", [recaptchaenterprise.ListKeysRequest, dict,])
def test_list_keys(request_type, transport: str = "grpc"):
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_keys), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = recaptchaenterprise.ListKeysResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_keys(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == recaptchaenterprise.ListKeysRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListKeysPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_keys_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_keys), "__call__") as call:
        client.list_keys()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == recaptchaenterprise.ListKeysRequest()


@pytest.mark.asyncio
async def test_list_keys_async(
    transport: str = "grpc_asyncio", request_type=recaptchaenterprise.ListKeysRequest
):
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_keys), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recaptchaenterprise.ListKeysResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_keys(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == recaptchaenterprise.ListKeysRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListKeysAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_keys_async_from_dict():
    await test_list_keys_async(request_type=dict)


def test_list_keys_field_headers():
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recaptchaenterprise.ListKeysRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_keys), "__call__") as call:
        call.return_value = recaptchaenterprise.ListKeysResponse()
        client.list_keys(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_keys_field_headers_async():
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recaptchaenterprise.ListKeysRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_keys), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recaptchaenterprise.ListKeysResponse()
        )
        await client.list_keys(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_keys_pager(transport_name: str = "grpc"):
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials, transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_keys), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            recaptchaenterprise.ListKeysResponse(
                keys=[
                    recaptchaenterprise.Key(),
                    recaptchaenterprise.Key(),
                    recaptchaenterprise.Key(),
                ],
                next_page_token="abc",
            ),
            recaptchaenterprise.ListKeysResponse(keys=[], next_page_token="def",),
            recaptchaenterprise.ListKeysResponse(
                keys=[recaptchaenterprise.Key(),], next_page_token="ghi",
            ),
            recaptchaenterprise.ListKeysResponse(
                keys=[recaptchaenterprise.Key(), recaptchaenterprise.Key(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_keys(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, recaptchaenterprise.Key) for i in results)


def test_list_keys_pages(transport_name: str = "grpc"):
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials, transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_keys), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            recaptchaenterprise.ListKeysResponse(
                keys=[
                    recaptchaenterprise.Key(),
                    recaptchaenterprise.Key(),
                    recaptchaenterprise.Key(),
                ],
                next_page_token="abc",
            ),
            recaptchaenterprise.ListKeysResponse(keys=[], next_page_token="def",),
            recaptchaenterprise.ListKeysResponse(
                keys=[recaptchaenterprise.Key(),], next_page_token="ghi",
            ),
            recaptchaenterprise.ListKeysResponse(
                keys=[recaptchaenterprise.Key(), recaptchaenterprise.Key(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_keys(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_keys_async_pager():
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_keys), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            recaptchaenterprise.ListKeysResponse(
                keys=[
                    recaptchaenterprise.Key(),
                    recaptchaenterprise.Key(),
                    recaptchaenterprise.Key(),
                ],
                next_page_token="abc",
            ),
            recaptchaenterprise.ListKeysResponse(keys=[], next_page_token="def",),
            recaptchaenterprise.ListKeysResponse(
                keys=[recaptchaenterprise.Key(),], next_page_token="ghi",
            ),
            recaptchaenterprise.ListKeysResponse(
                keys=[recaptchaenterprise.Key(), recaptchaenterprise.Key(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_keys(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, recaptchaenterprise.Key) for i in responses)


@pytest.mark.asyncio
async def test_list_keys_async_pages():
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_keys), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            recaptchaenterprise.ListKeysResponse(
                keys=[
                    recaptchaenterprise.Key(),
                    recaptchaenterprise.Key(),
                    recaptchaenterprise.Key(),
                ],
                next_page_token="abc",
            ),
            recaptchaenterprise.ListKeysResponse(keys=[], next_page_token="def",),
            recaptchaenterprise.ListKeysResponse(
                keys=[recaptchaenterprise.Key(),], next_page_token="ghi",
            ),
            recaptchaenterprise.ListKeysResponse(
                keys=[recaptchaenterprise.Key(), recaptchaenterprise.Key(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_keys(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize("request_type", [recaptchaenterprise.GetKeyRequest, dict,])
def test_get_key(request_type, transport: str = "grpc"):
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = recaptchaenterprise.Key(
            name="name_value",
            display_name="display_name_value",
            web_settings=recaptchaenterprise.WebKeySettings(allow_all_domains=True),
        )
        response = client.get_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == recaptchaenterprise.GetKeyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, recaptchaenterprise.Key)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"


def test_get_key_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_key), "__call__") as call:
        client.get_key()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == recaptchaenterprise.GetKeyRequest()


@pytest.mark.asyncio
async def test_get_key_async(
    transport: str = "grpc_asyncio", request_type=recaptchaenterprise.GetKeyRequest
):
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recaptchaenterprise.Key(
                name="name_value", display_name="display_name_value",
            )
        )
        response = await client.get_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == recaptchaenterprise.GetKeyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, recaptchaenterprise.Key)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"


@pytest.mark.asyncio
async def test_get_key_async_from_dict():
    await test_get_key_async(request_type=dict)


def test_get_key_field_headers():
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recaptchaenterprise.GetKeyRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_key), "__call__") as call:
        call.return_value = recaptchaenterprise.Key()
        client.get_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_key_field_headers_async():
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recaptchaenterprise.GetKeyRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_key), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recaptchaenterprise.Key()
        )
        await client.get_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.parametrize("request_type", [recaptchaenterprise.UpdateKeyRequest, dict,])
def test_update_key(request_type, transport: str = "grpc"):
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = recaptchaenterprise.Key(
            name="name_value",
            display_name="display_name_value",
            web_settings=recaptchaenterprise.WebKeySettings(allow_all_domains=True),
        )
        response = client.update_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == recaptchaenterprise.UpdateKeyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, recaptchaenterprise.Key)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"


def test_update_key_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_key), "__call__") as call:
        client.update_key()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == recaptchaenterprise.UpdateKeyRequest()


@pytest.mark.asyncio
async def test_update_key_async(
    transport: str = "grpc_asyncio", request_type=recaptchaenterprise.UpdateKeyRequest
):
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recaptchaenterprise.Key(
                name="name_value", display_name="display_name_value",
            )
        )
        response = await client.update_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == recaptchaenterprise.UpdateKeyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, recaptchaenterprise.Key)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"


@pytest.mark.asyncio
async def test_update_key_async_from_dict():
    await test_update_key_async(request_type=dict)


def test_update_key_field_headers():
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recaptchaenterprise.UpdateKeyRequest()

    request.key.name = "key.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_key), "__call__") as call:
        call.return_value = recaptchaenterprise.Key()
        client.update_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "key.name=key.name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_key_field_headers_async():
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recaptchaenterprise.UpdateKeyRequest()

    request.key.name = "key.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_key), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recaptchaenterprise.Key()
        )
        await client.update_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "key.name=key.name/value",) in kw["metadata"]


@pytest.mark.parametrize("request_type", [recaptchaenterprise.DeleteKeyRequest, dict,])
def test_delete_key(request_type, transport: str = "grpc"):
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == recaptchaenterprise.DeleteKeyRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_key_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_key), "__call__") as call:
        client.delete_key()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == recaptchaenterprise.DeleteKeyRequest()


@pytest.mark.asyncio
async def test_delete_key_async(
    transport: str = "grpc_asyncio", request_type=recaptchaenterprise.DeleteKeyRequest
):
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == recaptchaenterprise.DeleteKeyRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_key_async_from_dict():
    await test_delete_key_async(request_type=dict)


def test_delete_key_field_headers():
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recaptchaenterprise.DeleteKeyRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_key), "__call__") as call:
        call.return_value = None
        client.delete_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_key_field_headers_async():
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recaptchaenterprise.DeleteKeyRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_key), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.parametrize("request_type", [recaptchaenterprise.MigrateKeyRequest, dict,])
def test_migrate_key(request_type, transport: str = "grpc"):
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.migrate_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = recaptchaenterprise.Key(
            name="name_value",
            display_name="display_name_value",
            web_settings=recaptchaenterprise.WebKeySettings(allow_all_domains=True),
        )
        response = client.migrate_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == recaptchaenterprise.MigrateKeyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, recaptchaenterprise.Key)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"


def test_migrate_key_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.migrate_key), "__call__") as call:
        client.migrate_key()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == recaptchaenterprise.MigrateKeyRequest()


@pytest.mark.asyncio
async def test_migrate_key_async(
    transport: str = "grpc_asyncio", request_type=recaptchaenterprise.MigrateKeyRequest
):
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.migrate_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recaptchaenterprise.Key(
                name="name_value", display_name="display_name_value",
            )
        )
        response = await client.migrate_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == recaptchaenterprise.MigrateKeyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, recaptchaenterprise.Key)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"


@pytest.mark.asyncio
async def test_migrate_key_async_from_dict():
    await test_migrate_key_async(request_type=dict)


def test_migrate_key_field_headers():
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recaptchaenterprise.MigrateKeyRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.migrate_key), "__call__") as call:
        call.return_value = recaptchaenterprise.Key()
        client.migrate_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_migrate_key_field_headers_async():
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recaptchaenterprise.MigrateKeyRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.migrate_key), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recaptchaenterprise.Key()
        )
        await client.migrate_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.parametrize("request_type", [recaptchaenterprise.GetMetricsRequest, dict,])
def test_get_metrics(request_type, transport: str = "grpc"):
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_metrics), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = recaptchaenterprise.Metrics(name="name_value",)
        response = client.get_metrics(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == recaptchaenterprise.GetMetricsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, recaptchaenterprise.Metrics)
    assert response.name == "name_value"


def test_get_metrics_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_metrics), "__call__") as call:
        client.get_metrics()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == recaptchaenterprise.GetMetricsRequest()


@pytest.mark.asyncio
async def test_get_metrics_async(
    transport: str = "grpc_asyncio", request_type=recaptchaenterprise.GetMetricsRequest
):
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_metrics), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recaptchaenterprise.Metrics(name="name_value",)
        )
        response = await client.get_metrics(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == recaptchaenterprise.GetMetricsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, recaptchaenterprise.Metrics)
    assert response.name == "name_value"


@pytest.mark.asyncio
async def test_get_metrics_async_from_dict():
    await test_get_metrics_async(request_type=dict)


def test_get_metrics_field_headers():
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recaptchaenterprise.GetMetricsRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_metrics), "__call__") as call:
        call.return_value = recaptchaenterprise.Metrics()
        client.get_metrics(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_metrics_field_headers_async():
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recaptchaenterprise.GetMetricsRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_metrics), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recaptchaenterprise.Metrics()
        )
        await client.get_metrics(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_metrics_flattened():
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_metrics), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = recaptchaenterprise.Metrics()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_metrics(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_metrics_flattened_error():
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_metrics(
            recaptchaenterprise.GetMetricsRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_metrics_flattened_async():
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_metrics), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = recaptchaenterprise.Metrics()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recaptchaenterprise.Metrics()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_metrics(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_metrics_flattened_error_async():
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_metrics(
            recaptchaenterprise.GetMetricsRequest(), name="name_value",
        )


@pytest.mark.parametrize(
    "request_type", [recaptchaenterprise.ListRelatedAccountGroupsRequest, dict,]
)
def test_list_related_account_groups(request_type, transport: str = "grpc"):
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_related_account_groups), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = recaptchaenterprise.ListRelatedAccountGroupsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_related_account_groups(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == recaptchaenterprise.ListRelatedAccountGroupsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRelatedAccountGroupsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_related_account_groups_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_related_account_groups), "__call__"
    ) as call:
        client.list_related_account_groups()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == recaptchaenterprise.ListRelatedAccountGroupsRequest()


@pytest.mark.asyncio
async def test_list_related_account_groups_async(
    transport: str = "grpc_asyncio",
    request_type=recaptchaenterprise.ListRelatedAccountGroupsRequest,
):
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_related_account_groups), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recaptchaenterprise.ListRelatedAccountGroupsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_related_account_groups(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == recaptchaenterprise.ListRelatedAccountGroupsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRelatedAccountGroupsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_related_account_groups_async_from_dict():
    await test_list_related_account_groups_async(request_type=dict)


def test_list_related_account_groups_field_headers():
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recaptchaenterprise.ListRelatedAccountGroupsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_related_account_groups), "__call__"
    ) as call:
        call.return_value = recaptchaenterprise.ListRelatedAccountGroupsResponse()
        client.list_related_account_groups(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_related_account_groups_field_headers_async():
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recaptchaenterprise.ListRelatedAccountGroupsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_related_account_groups), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recaptchaenterprise.ListRelatedAccountGroupsResponse()
        )
        await client.list_related_account_groups(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_related_account_groups_flattened():
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_related_account_groups), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = recaptchaenterprise.ListRelatedAccountGroupsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_related_account_groups(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_related_account_groups_flattened_error():
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_related_account_groups(
            recaptchaenterprise.ListRelatedAccountGroupsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_related_account_groups_flattened_async():
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_related_account_groups), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = recaptchaenterprise.ListRelatedAccountGroupsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recaptchaenterprise.ListRelatedAccountGroupsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_related_account_groups(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_related_account_groups_flattened_error_async():
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_related_account_groups(
            recaptchaenterprise.ListRelatedAccountGroupsRequest(),
            parent="parent_value",
        )


def test_list_related_account_groups_pager(transport_name: str = "grpc"):
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials, transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_related_account_groups), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            recaptchaenterprise.ListRelatedAccountGroupsResponse(
                related_account_groups=[
                    recaptchaenterprise.RelatedAccountGroup(),
                    recaptchaenterprise.RelatedAccountGroup(),
                    recaptchaenterprise.RelatedAccountGroup(),
                ],
                next_page_token="abc",
            ),
            recaptchaenterprise.ListRelatedAccountGroupsResponse(
                related_account_groups=[], next_page_token="def",
            ),
            recaptchaenterprise.ListRelatedAccountGroupsResponse(
                related_account_groups=[recaptchaenterprise.RelatedAccountGroup(),],
                next_page_token="ghi",
            ),
            recaptchaenterprise.ListRelatedAccountGroupsResponse(
                related_account_groups=[
                    recaptchaenterprise.RelatedAccountGroup(),
                    recaptchaenterprise.RelatedAccountGroup(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_related_account_groups(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(
            isinstance(i, recaptchaenterprise.RelatedAccountGroup) for i in results
        )


def test_list_related_account_groups_pages(transport_name: str = "grpc"):
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials, transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_related_account_groups), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            recaptchaenterprise.ListRelatedAccountGroupsResponse(
                related_account_groups=[
                    recaptchaenterprise.RelatedAccountGroup(),
                    recaptchaenterprise.RelatedAccountGroup(),
                    recaptchaenterprise.RelatedAccountGroup(),
                ],
                next_page_token="abc",
            ),
            recaptchaenterprise.ListRelatedAccountGroupsResponse(
                related_account_groups=[], next_page_token="def",
            ),
            recaptchaenterprise.ListRelatedAccountGroupsResponse(
                related_account_groups=[recaptchaenterprise.RelatedAccountGroup(),],
                next_page_token="ghi",
            ),
            recaptchaenterprise.ListRelatedAccountGroupsResponse(
                related_account_groups=[
                    recaptchaenterprise.RelatedAccountGroup(),
                    recaptchaenterprise.RelatedAccountGroup(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_related_account_groups(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_related_account_groups_async_pager():
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_related_account_groups),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            recaptchaenterprise.ListRelatedAccountGroupsResponse(
                related_account_groups=[
                    recaptchaenterprise.RelatedAccountGroup(),
                    recaptchaenterprise.RelatedAccountGroup(),
                    recaptchaenterprise.RelatedAccountGroup(),
                ],
                next_page_token="abc",
            ),
            recaptchaenterprise.ListRelatedAccountGroupsResponse(
                related_account_groups=[], next_page_token="def",
            ),
            recaptchaenterprise.ListRelatedAccountGroupsResponse(
                related_account_groups=[recaptchaenterprise.RelatedAccountGroup(),],
                next_page_token="ghi",
            ),
            recaptchaenterprise.ListRelatedAccountGroupsResponse(
                related_account_groups=[
                    recaptchaenterprise.RelatedAccountGroup(),
                    recaptchaenterprise.RelatedAccountGroup(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_related_account_groups(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, recaptchaenterprise.RelatedAccountGroup) for i in responses
        )


@pytest.mark.asyncio
async def test_list_related_account_groups_async_pages():
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_related_account_groups),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            recaptchaenterprise.ListRelatedAccountGroupsResponse(
                related_account_groups=[
                    recaptchaenterprise.RelatedAccountGroup(),
                    recaptchaenterprise.RelatedAccountGroup(),
                    recaptchaenterprise.RelatedAccountGroup(),
                ],
                next_page_token="abc",
            ),
            recaptchaenterprise.ListRelatedAccountGroupsResponse(
                related_account_groups=[], next_page_token="def",
            ),
            recaptchaenterprise.ListRelatedAccountGroupsResponse(
                related_account_groups=[recaptchaenterprise.RelatedAccountGroup(),],
                next_page_token="ghi",
            ),
            recaptchaenterprise.ListRelatedAccountGroupsResponse(
                related_account_groups=[
                    recaptchaenterprise.RelatedAccountGroup(),
                    recaptchaenterprise.RelatedAccountGroup(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_related_account_groups(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [recaptchaenterprise.ListRelatedAccountGroupMembershipsRequest, dict,],
)
def test_list_related_account_group_memberships(request_type, transport: str = "grpc"):
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_related_account_group_memberships), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = recaptchaenterprise.ListRelatedAccountGroupMembershipsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_related_account_group_memberships(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert (
            args[0] == recaptchaenterprise.ListRelatedAccountGroupMembershipsRequest()
        )

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRelatedAccountGroupMembershipsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_related_account_group_memberships_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_related_account_group_memberships), "__call__"
    ) as call:
        client.list_related_account_group_memberships()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0] == recaptchaenterprise.ListRelatedAccountGroupMembershipsRequest()
        )


@pytest.mark.asyncio
async def test_list_related_account_group_memberships_async(
    transport: str = "grpc_asyncio",
    request_type=recaptchaenterprise.ListRelatedAccountGroupMembershipsRequest,
):
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_related_account_group_memberships), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recaptchaenterprise.ListRelatedAccountGroupMembershipsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_related_account_group_memberships(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert (
            args[0] == recaptchaenterprise.ListRelatedAccountGroupMembershipsRequest()
        )

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRelatedAccountGroupMembershipsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_related_account_group_memberships_async_from_dict():
    await test_list_related_account_group_memberships_async(request_type=dict)


def test_list_related_account_group_memberships_field_headers():
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recaptchaenterprise.ListRelatedAccountGroupMembershipsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_related_account_group_memberships), "__call__"
    ) as call:
        call.return_value = (
            recaptchaenterprise.ListRelatedAccountGroupMembershipsResponse()
        )
        client.list_related_account_group_memberships(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_related_account_group_memberships_field_headers_async():
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recaptchaenterprise.ListRelatedAccountGroupMembershipsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_related_account_group_memberships), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recaptchaenterprise.ListRelatedAccountGroupMembershipsResponse()
        )
        await client.list_related_account_group_memberships(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_related_account_group_memberships_flattened():
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_related_account_group_memberships), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            recaptchaenterprise.ListRelatedAccountGroupMembershipsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_related_account_group_memberships(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_related_account_group_memberships_flattened_error():
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_related_account_group_memberships(
            recaptchaenterprise.ListRelatedAccountGroupMembershipsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_related_account_group_memberships_flattened_async():
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_related_account_group_memberships), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            recaptchaenterprise.ListRelatedAccountGroupMembershipsResponse()
        )

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recaptchaenterprise.ListRelatedAccountGroupMembershipsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_related_account_group_memberships(
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
async def test_list_related_account_group_memberships_flattened_error_async():
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_related_account_group_memberships(
            recaptchaenterprise.ListRelatedAccountGroupMembershipsRequest(),
            parent="parent_value",
        )


def test_list_related_account_group_memberships_pager(transport_name: str = "grpc"):
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials, transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_related_account_group_memberships), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            recaptchaenterprise.ListRelatedAccountGroupMembershipsResponse(
                related_account_group_memberships=[
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                ],
                next_page_token="abc",
            ),
            recaptchaenterprise.ListRelatedAccountGroupMembershipsResponse(
                related_account_group_memberships=[], next_page_token="def",
            ),
            recaptchaenterprise.ListRelatedAccountGroupMembershipsResponse(
                related_account_group_memberships=[
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                ],
                next_page_token="ghi",
            ),
            recaptchaenterprise.ListRelatedAccountGroupMembershipsResponse(
                related_account_group_memberships=[
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_related_account_group_memberships(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(
            isinstance(i, recaptchaenterprise.RelatedAccountGroupMembership)
            for i in results
        )


def test_list_related_account_group_memberships_pages(transport_name: str = "grpc"):
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials, transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_related_account_group_memberships), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            recaptchaenterprise.ListRelatedAccountGroupMembershipsResponse(
                related_account_group_memberships=[
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                ],
                next_page_token="abc",
            ),
            recaptchaenterprise.ListRelatedAccountGroupMembershipsResponse(
                related_account_group_memberships=[], next_page_token="def",
            ),
            recaptchaenterprise.ListRelatedAccountGroupMembershipsResponse(
                related_account_group_memberships=[
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                ],
                next_page_token="ghi",
            ),
            recaptchaenterprise.ListRelatedAccountGroupMembershipsResponse(
                related_account_group_memberships=[
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_related_account_group_memberships(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_related_account_group_memberships_async_pager():
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_related_account_group_memberships),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            recaptchaenterprise.ListRelatedAccountGroupMembershipsResponse(
                related_account_group_memberships=[
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                ],
                next_page_token="abc",
            ),
            recaptchaenterprise.ListRelatedAccountGroupMembershipsResponse(
                related_account_group_memberships=[], next_page_token="def",
            ),
            recaptchaenterprise.ListRelatedAccountGroupMembershipsResponse(
                related_account_group_memberships=[
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                ],
                next_page_token="ghi",
            ),
            recaptchaenterprise.ListRelatedAccountGroupMembershipsResponse(
                related_account_group_memberships=[
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_related_account_group_memberships(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, recaptchaenterprise.RelatedAccountGroupMembership)
            for i in responses
        )


@pytest.mark.asyncio
async def test_list_related_account_group_memberships_async_pages():
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_related_account_group_memberships),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            recaptchaenterprise.ListRelatedAccountGroupMembershipsResponse(
                related_account_group_memberships=[
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                ],
                next_page_token="abc",
            ),
            recaptchaenterprise.ListRelatedAccountGroupMembershipsResponse(
                related_account_group_memberships=[], next_page_token="def",
            ),
            recaptchaenterprise.ListRelatedAccountGroupMembershipsResponse(
                related_account_group_memberships=[
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                ],
                next_page_token="ghi",
            ),
            recaptchaenterprise.ListRelatedAccountGroupMembershipsResponse(
                related_account_group_memberships=[
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_related_account_group_memberships(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [recaptchaenterprise.SearchRelatedAccountGroupMembershipsRequest, dict,],
)
def test_search_related_account_group_memberships(
    request_type, transport: str = "grpc"
):
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_related_account_group_memberships), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = recaptchaenterprise.SearchRelatedAccountGroupMembershipsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.search_related_account_group_memberships(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert (
            args[0] == recaptchaenterprise.SearchRelatedAccountGroupMembershipsRequest()
        )

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchRelatedAccountGroupMembershipsPager)
    assert response.next_page_token == "next_page_token_value"


def test_search_related_account_group_memberships_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_related_account_group_memberships), "__call__"
    ) as call:
        client.search_related_account_group_memberships()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0] == recaptchaenterprise.SearchRelatedAccountGroupMembershipsRequest()
        )


@pytest.mark.asyncio
async def test_search_related_account_group_memberships_async(
    transport: str = "grpc_asyncio",
    request_type=recaptchaenterprise.SearchRelatedAccountGroupMembershipsRequest,
):
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_related_account_group_memberships), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recaptchaenterprise.SearchRelatedAccountGroupMembershipsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.search_related_account_group_memberships(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert (
            args[0] == recaptchaenterprise.SearchRelatedAccountGroupMembershipsRequest()
        )

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchRelatedAccountGroupMembershipsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_search_related_account_group_memberships_async_from_dict():
    await test_search_related_account_group_memberships_async(request_type=dict)


def test_search_related_account_group_memberships_field_headers():
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recaptchaenterprise.SearchRelatedAccountGroupMembershipsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_related_account_group_memberships), "__call__"
    ) as call:
        call.return_value = (
            recaptchaenterprise.SearchRelatedAccountGroupMembershipsResponse()
        )
        client.search_related_account_group_memberships(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_search_related_account_group_memberships_field_headers_async():
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recaptchaenterprise.SearchRelatedAccountGroupMembershipsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_related_account_group_memberships), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recaptchaenterprise.SearchRelatedAccountGroupMembershipsResponse()
        )
        await client.search_related_account_group_memberships(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_search_related_account_group_memberships_flattened():
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_related_account_group_memberships), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            recaptchaenterprise.SearchRelatedAccountGroupMembershipsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.search_related_account_group_memberships(
            parent="parent_value", hashed_account_id=b"hashed_account_id_blob",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].hashed_account_id
        mock_val = b"hashed_account_id_blob"
        assert arg == mock_val


def test_search_related_account_group_memberships_flattened_error():
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.search_related_account_group_memberships(
            recaptchaenterprise.SearchRelatedAccountGroupMembershipsRequest(),
            parent="parent_value",
            hashed_account_id=b"hashed_account_id_blob",
        )


@pytest.mark.asyncio
async def test_search_related_account_group_memberships_flattened_async():
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_related_account_group_memberships), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            recaptchaenterprise.SearchRelatedAccountGroupMembershipsResponse()
        )

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            recaptchaenterprise.SearchRelatedAccountGroupMembershipsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.search_related_account_group_memberships(
            parent="parent_value", hashed_account_id=b"hashed_account_id_blob",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].hashed_account_id
        mock_val = b"hashed_account_id_blob"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_search_related_account_group_memberships_flattened_error_async():
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.search_related_account_group_memberships(
            recaptchaenterprise.SearchRelatedAccountGroupMembershipsRequest(),
            parent="parent_value",
            hashed_account_id=b"hashed_account_id_blob",
        )


def test_search_related_account_group_memberships_pager(transport_name: str = "grpc"):
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials, transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_related_account_group_memberships), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            recaptchaenterprise.SearchRelatedAccountGroupMembershipsResponse(
                related_account_group_memberships=[
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                ],
                next_page_token="abc",
            ),
            recaptchaenterprise.SearchRelatedAccountGroupMembershipsResponse(
                related_account_group_memberships=[], next_page_token="def",
            ),
            recaptchaenterprise.SearchRelatedAccountGroupMembershipsResponse(
                related_account_group_memberships=[
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                ],
                next_page_token="ghi",
            ),
            recaptchaenterprise.SearchRelatedAccountGroupMembershipsResponse(
                related_account_group_memberships=[
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.search_related_account_group_memberships(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(
            isinstance(i, recaptchaenterprise.RelatedAccountGroupMembership)
            for i in results
        )


def test_search_related_account_group_memberships_pages(transport_name: str = "grpc"):
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials, transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_related_account_group_memberships), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            recaptchaenterprise.SearchRelatedAccountGroupMembershipsResponse(
                related_account_group_memberships=[
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                ],
                next_page_token="abc",
            ),
            recaptchaenterprise.SearchRelatedAccountGroupMembershipsResponse(
                related_account_group_memberships=[], next_page_token="def",
            ),
            recaptchaenterprise.SearchRelatedAccountGroupMembershipsResponse(
                related_account_group_memberships=[
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                ],
                next_page_token="ghi",
            ),
            recaptchaenterprise.SearchRelatedAccountGroupMembershipsResponse(
                related_account_group_memberships=[
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.search_related_account_group_memberships(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_search_related_account_group_memberships_async_pager():
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_related_account_group_memberships),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            recaptchaenterprise.SearchRelatedAccountGroupMembershipsResponse(
                related_account_group_memberships=[
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                ],
                next_page_token="abc",
            ),
            recaptchaenterprise.SearchRelatedAccountGroupMembershipsResponse(
                related_account_group_memberships=[], next_page_token="def",
            ),
            recaptchaenterprise.SearchRelatedAccountGroupMembershipsResponse(
                related_account_group_memberships=[
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                ],
                next_page_token="ghi",
            ),
            recaptchaenterprise.SearchRelatedAccountGroupMembershipsResponse(
                related_account_group_memberships=[
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.search_related_account_group_memberships(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, recaptchaenterprise.RelatedAccountGroupMembership)
            for i in responses
        )


@pytest.mark.asyncio
async def test_search_related_account_group_memberships_async_pages():
    client = RecaptchaEnterpriseServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_related_account_group_memberships),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            recaptchaenterprise.SearchRelatedAccountGroupMembershipsResponse(
                related_account_group_memberships=[
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                ],
                next_page_token="abc",
            ),
            recaptchaenterprise.SearchRelatedAccountGroupMembershipsResponse(
                related_account_group_memberships=[], next_page_token="def",
            ),
            recaptchaenterprise.SearchRelatedAccountGroupMembershipsResponse(
                related_account_group_memberships=[
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                ],
                next_page_token="ghi",
            ),
            recaptchaenterprise.SearchRelatedAccountGroupMembershipsResponse(
                related_account_group_memberships=[
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                    recaptchaenterprise.RelatedAccountGroupMembership(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.search_related_account_group_memberships(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.RecaptchaEnterpriseServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = RecaptchaEnterpriseServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.RecaptchaEnterpriseServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = RecaptchaEnterpriseServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.RecaptchaEnterpriseServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = RecaptchaEnterpriseServiceClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.RecaptchaEnterpriseServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = RecaptchaEnterpriseServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.RecaptchaEnterpriseServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.RecaptchaEnterpriseServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.RecaptchaEnterpriseServiceGrpcTransport,
        transports.RecaptchaEnterpriseServiceGrpcAsyncIOTransport,
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
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport, transports.RecaptchaEnterpriseServiceGrpcTransport,
    )


def test_recaptcha_enterprise_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.RecaptchaEnterpriseServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_recaptcha_enterprise_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.recaptchaenterprise_v1.services.recaptcha_enterprise_service.transports.RecaptchaEnterpriseServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.RecaptchaEnterpriseServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_assessment",
        "annotate_assessment",
        "create_key",
        "list_keys",
        "get_key",
        "update_key",
        "delete_key",
        "migrate_key",
        "get_metrics",
        "list_related_account_groups",
        "list_related_account_group_memberships",
        "search_related_account_group_memberships",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()


def test_recaptcha_enterprise_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.recaptchaenterprise_v1.services.recaptcha_enterprise_service.transports.RecaptchaEnterpriseServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.RecaptchaEnterpriseServiceTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_recaptcha_enterprise_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.recaptchaenterprise_v1.services.recaptcha_enterprise_service.transports.RecaptchaEnterpriseServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.RecaptchaEnterpriseServiceTransport()
        adc.assert_called_once()


def test_recaptcha_enterprise_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        RecaptchaEnterpriseServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.RecaptchaEnterpriseServiceGrpcTransport,
        transports.RecaptchaEnterpriseServiceGrpcAsyncIOTransport,
    ],
)
def test_recaptcha_enterprise_service_transport_auth_adc(transport_class):
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
        (transports.RecaptchaEnterpriseServiceGrpcTransport, grpc_helpers),
        (transports.RecaptchaEnterpriseServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_recaptcha_enterprise_service_transport_create_channel(
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
            "recaptchaenterprise.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="recaptchaenterprise.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.RecaptchaEnterpriseServiceGrpcTransport,
        transports.RecaptchaEnterpriseServiceGrpcAsyncIOTransport,
    ],
)
def test_recaptcha_enterprise_service_grpc_transport_client_cert_source_for_mtls(
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


def test_recaptcha_enterprise_service_host_no_port():
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="recaptchaenterprise.googleapis.com"
        ),
    )
    assert client.transport._host == "recaptchaenterprise.googleapis.com:443"


def test_recaptcha_enterprise_service_host_with_port():
    client = RecaptchaEnterpriseServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="recaptchaenterprise.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "recaptchaenterprise.googleapis.com:8000"


def test_recaptcha_enterprise_service_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.RecaptchaEnterpriseServiceGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_recaptcha_enterprise_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.RecaptchaEnterpriseServiceGrpcAsyncIOTransport(
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
        transports.RecaptchaEnterpriseServiceGrpcTransport,
        transports.RecaptchaEnterpriseServiceGrpcAsyncIOTransport,
    ],
)
def test_recaptcha_enterprise_service_transport_channel_mtls_with_client_cert_source(
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
        transports.RecaptchaEnterpriseServiceGrpcTransport,
        transports.RecaptchaEnterpriseServiceGrpcAsyncIOTransport,
    ],
)
def test_recaptcha_enterprise_service_transport_channel_mtls_with_adc(transport_class):
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


def test_assessment_path():
    project = "squid"
    assessment = "clam"
    expected = "projects/{project}/assessments/{assessment}".format(
        project=project, assessment=assessment,
    )
    actual = RecaptchaEnterpriseServiceClient.assessment_path(project, assessment)
    assert expected == actual


def test_parse_assessment_path():
    expected = {
        "project": "whelk",
        "assessment": "octopus",
    }
    path = RecaptchaEnterpriseServiceClient.assessment_path(**expected)

    # Check that the path construction is reversible.
    actual = RecaptchaEnterpriseServiceClient.parse_assessment_path(path)
    assert expected == actual


def test_key_path():
    project = "oyster"
    key = "nudibranch"
    expected = "projects/{project}/keys/{key}".format(project=project, key=key,)
    actual = RecaptchaEnterpriseServiceClient.key_path(project, key)
    assert expected == actual


def test_parse_key_path():
    expected = {
        "project": "cuttlefish",
        "key": "mussel",
    }
    path = RecaptchaEnterpriseServiceClient.key_path(**expected)

    # Check that the path construction is reversible.
    actual = RecaptchaEnterpriseServiceClient.parse_key_path(path)
    assert expected == actual


def test_metrics_path():
    project = "winkle"
    key = "nautilus"
    expected = "projects/{project}/keys/{key}/metrics".format(project=project, key=key,)
    actual = RecaptchaEnterpriseServiceClient.metrics_path(project, key)
    assert expected == actual


def test_parse_metrics_path():
    expected = {
        "project": "scallop",
        "key": "abalone",
    }
    path = RecaptchaEnterpriseServiceClient.metrics_path(**expected)

    # Check that the path construction is reversible.
    actual = RecaptchaEnterpriseServiceClient.parse_metrics_path(path)
    assert expected == actual


def test_related_account_group_path():
    project = "squid"
    relatedaccountgroup = "clam"
    expected = "projects/{project}/relatedaccountgroups/{relatedaccountgroup}".format(
        project=project, relatedaccountgroup=relatedaccountgroup,
    )
    actual = RecaptchaEnterpriseServiceClient.related_account_group_path(
        project, relatedaccountgroup
    )
    assert expected == actual


def test_parse_related_account_group_path():
    expected = {
        "project": "whelk",
        "relatedaccountgroup": "octopus",
    }
    path = RecaptchaEnterpriseServiceClient.related_account_group_path(**expected)

    # Check that the path construction is reversible.
    actual = RecaptchaEnterpriseServiceClient.parse_related_account_group_path(path)
    assert expected == actual


def test_related_account_group_membership_path():
    project = "oyster"
    relatedaccountgroup = "nudibranch"
    membership = "cuttlefish"
    expected = "projects/{project}/relatedaccountgroups/{relatedaccountgroup}/memberships/{membership}".format(
        project=project, relatedaccountgroup=relatedaccountgroup, membership=membership,
    )
    actual = RecaptchaEnterpriseServiceClient.related_account_group_membership_path(
        project, relatedaccountgroup, membership
    )
    assert expected == actual


def test_parse_related_account_group_membership_path():
    expected = {
        "project": "mussel",
        "relatedaccountgroup": "winkle",
        "membership": "nautilus",
    }
    path = RecaptchaEnterpriseServiceClient.related_account_group_membership_path(
        **expected
    )

    # Check that the path construction is reversible.
    actual = RecaptchaEnterpriseServiceClient.parse_related_account_group_membership_path(
        path
    )
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "scallop"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = RecaptchaEnterpriseServiceClient.common_billing_account_path(
        billing_account
    )
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "abalone",
    }
    path = RecaptchaEnterpriseServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = RecaptchaEnterpriseServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "squid"
    expected = "folders/{folder}".format(folder=folder,)
    actual = RecaptchaEnterpriseServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "clam",
    }
    path = RecaptchaEnterpriseServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = RecaptchaEnterpriseServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "whelk"
    expected = "organizations/{organization}".format(organization=organization,)
    actual = RecaptchaEnterpriseServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "octopus",
    }
    path = RecaptchaEnterpriseServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = RecaptchaEnterpriseServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "oyster"
    expected = "projects/{project}".format(project=project,)
    actual = RecaptchaEnterpriseServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nudibranch",
    }
    path = RecaptchaEnterpriseServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = RecaptchaEnterpriseServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "cuttlefish"
    location = "mussel"
    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = RecaptchaEnterpriseServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "winkle",
        "location": "nautilus",
    }
    path = RecaptchaEnterpriseServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = RecaptchaEnterpriseServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.RecaptchaEnterpriseServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = RecaptchaEnterpriseServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.RecaptchaEnterpriseServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = RecaptchaEnterpriseServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = RecaptchaEnterpriseServiceAsyncClient(
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
        client = RecaptchaEnterpriseServiceClient(
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
        client = RecaptchaEnterpriseServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()
