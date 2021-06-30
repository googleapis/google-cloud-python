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
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.talent_v4beta1.services.application_service import (
    ApplicationServiceAsyncClient,
)
from google.cloud.talent_v4beta1.services.application_service import (
    ApplicationServiceClient,
)
from google.cloud.talent_v4beta1.services.application_service import pagers
from google.cloud.talent_v4beta1.services.application_service import transports
from google.cloud.talent_v4beta1.services.application_service.transports.base import (
    _GOOGLE_AUTH_VERSION,
)
from google.cloud.talent_v4beta1.types import application
from google.cloud.talent_v4beta1.types import application as gct_application
from google.cloud.talent_v4beta1.types import application_service
from google.cloud.talent_v4beta1.types import common
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
from google.type import date_pb2  # type: ignore
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

    assert ApplicationServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        ApplicationServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        ApplicationServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        ApplicationServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        ApplicationServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        ApplicationServiceClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class", [ApplicationServiceClient, ApplicationServiceAsyncClient,]
)
def test_application_service_client_from_service_account_info(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "jobs.googleapis.com:443"


@pytest.mark.parametrize(
    "client_class", [ApplicationServiceClient, ApplicationServiceAsyncClient,]
)
def test_application_service_client_service_account_always_use_jwt(client_class):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        client = client_class(credentials=creds)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.ApplicationServiceGrpcTransport, "grpc"),
        (transports.ApplicationServiceGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_application_service_client_service_account_always_use_jwt_true(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)


@pytest.mark.parametrize(
    "client_class", [ApplicationServiceClient, ApplicationServiceAsyncClient,]
)
def test_application_service_client_from_service_account_file(client_class):
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

        assert client.transport._host == "jobs.googleapis.com:443"


def test_application_service_client_get_transport_class():
    transport = ApplicationServiceClient.get_transport_class()
    available_transports = [
        transports.ApplicationServiceGrpcTransport,
    ]
    assert transport in available_transports

    transport = ApplicationServiceClient.get_transport_class("grpc")
    assert transport == transports.ApplicationServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (ApplicationServiceClient, transports.ApplicationServiceGrpcTransport, "grpc"),
        (
            ApplicationServiceAsyncClient,
            transports.ApplicationServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    ApplicationServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ApplicationServiceClient),
)
@mock.patch.object(
    ApplicationServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ApplicationServiceAsyncClient),
)
def test_application_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(ApplicationServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(ApplicationServiceClient, "get_transport_class") as gtc:
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
            ApplicationServiceClient,
            transports.ApplicationServiceGrpcTransport,
            "grpc",
            "true",
        ),
        (
            ApplicationServiceAsyncClient,
            transports.ApplicationServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            ApplicationServiceClient,
            transports.ApplicationServiceGrpcTransport,
            "grpc",
            "false",
        ),
        (
            ApplicationServiceAsyncClient,
            transports.ApplicationServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    ApplicationServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ApplicationServiceClient),
)
@mock.patch.object(
    ApplicationServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ApplicationServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_application_service_client_mtls_env_auto(
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
        (ApplicationServiceClient, transports.ApplicationServiceGrpcTransport, "grpc"),
        (
            ApplicationServiceAsyncClient,
            transports.ApplicationServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_application_service_client_client_options_scopes(
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
        (ApplicationServiceClient, transports.ApplicationServiceGrpcTransport, "grpc"),
        (
            ApplicationServiceAsyncClient,
            transports.ApplicationServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_application_service_client_client_options_credentials_file(
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


def test_application_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.talent_v4beta1.services.application_service.transports.ApplicationServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = ApplicationServiceClient(
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


def test_create_application(
    transport: str = "grpc", request_type=application_service.CreateApplicationRequest
):
    client = ApplicationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_application), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gct_application.Application(
            name="name_value",
            external_id="external_id_value",
            profile="profile_value",
            job="job_value",
            company="company_value",
            stage=gct_application.Application.ApplicationStage.NEW,
            state=gct_application.Application.ApplicationState.IN_PROGRESS,
            outcome_notes="outcome_notes_value",
            outcome=common.Outcome.POSITIVE,
            job_title_snippet="job_title_snippet_value",
        )
        response = client.create_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == application_service.CreateApplicationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gct_application.Application)
    assert response.name == "name_value"
    assert response.external_id == "external_id_value"
    assert response.profile == "profile_value"
    assert response.job == "job_value"
    assert response.company == "company_value"
    assert response.stage == gct_application.Application.ApplicationStage.NEW
    assert response.state == gct_application.Application.ApplicationState.IN_PROGRESS
    assert response.outcome_notes == "outcome_notes_value"
    assert response.outcome == common.Outcome.POSITIVE
    assert response.job_title_snippet == "job_title_snippet_value"


def test_create_application_from_dict():
    test_create_application(request_type=dict)


def test_create_application_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ApplicationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_application), "__call__"
    ) as call:
        client.create_application()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == application_service.CreateApplicationRequest()


@pytest.mark.asyncio
async def test_create_application_async(
    transport: str = "grpc_asyncio",
    request_type=application_service.CreateApplicationRequest,
):
    client = ApplicationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_application), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gct_application.Application(
                name="name_value",
                external_id="external_id_value",
                profile="profile_value",
                job="job_value",
                company="company_value",
                stage=gct_application.Application.ApplicationStage.NEW,
                state=gct_application.Application.ApplicationState.IN_PROGRESS,
                outcome_notes="outcome_notes_value",
                outcome=common.Outcome.POSITIVE,
                job_title_snippet="job_title_snippet_value",
            )
        )
        response = await client.create_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == application_service.CreateApplicationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gct_application.Application)
    assert response.name == "name_value"
    assert response.external_id == "external_id_value"
    assert response.profile == "profile_value"
    assert response.job == "job_value"
    assert response.company == "company_value"
    assert response.stage == gct_application.Application.ApplicationStage.NEW
    assert response.state == gct_application.Application.ApplicationState.IN_PROGRESS
    assert response.outcome_notes == "outcome_notes_value"
    assert response.outcome == common.Outcome.POSITIVE
    assert response.job_title_snippet == "job_title_snippet_value"


@pytest.mark.asyncio
async def test_create_application_async_from_dict():
    await test_create_application_async(request_type=dict)


def test_create_application_field_headers():
    client = ApplicationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = application_service.CreateApplicationRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_application), "__call__"
    ) as call:
        call.return_value = gct_application.Application()
        client.create_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_application_field_headers_async():
    client = ApplicationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = application_service.CreateApplicationRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_application), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gct_application.Application()
        )
        await client.create_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_application_flattened():
    client = ApplicationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_application), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gct_application.Application()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_application(
            parent="parent_value",
            application=gct_application.Application(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].application == gct_application.Application(name="name_value")


def test_create_application_flattened_error():
    client = ApplicationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_application(
            application_service.CreateApplicationRequest(),
            parent="parent_value",
            application=gct_application.Application(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_application_flattened_async():
    client = ApplicationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_application), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gct_application.Application()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gct_application.Application()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_application(
            parent="parent_value",
            application=gct_application.Application(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].application == gct_application.Application(name="name_value")


@pytest.mark.asyncio
async def test_create_application_flattened_error_async():
    client = ApplicationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_application(
            application_service.CreateApplicationRequest(),
            parent="parent_value",
            application=gct_application.Application(name="name_value"),
        )


def test_get_application(
    transport: str = "grpc", request_type=application_service.GetApplicationRequest
):
    client = ApplicationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_application), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = application.Application(
            name="name_value",
            external_id="external_id_value",
            profile="profile_value",
            job="job_value",
            company="company_value",
            stage=application.Application.ApplicationStage.NEW,
            state=application.Application.ApplicationState.IN_PROGRESS,
            outcome_notes="outcome_notes_value",
            outcome=common.Outcome.POSITIVE,
            job_title_snippet="job_title_snippet_value",
        )
        response = client.get_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == application_service.GetApplicationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, application.Application)
    assert response.name == "name_value"
    assert response.external_id == "external_id_value"
    assert response.profile == "profile_value"
    assert response.job == "job_value"
    assert response.company == "company_value"
    assert response.stage == application.Application.ApplicationStage.NEW
    assert response.state == application.Application.ApplicationState.IN_PROGRESS
    assert response.outcome_notes == "outcome_notes_value"
    assert response.outcome == common.Outcome.POSITIVE
    assert response.job_title_snippet == "job_title_snippet_value"


def test_get_application_from_dict():
    test_get_application(request_type=dict)


def test_get_application_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ApplicationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_application), "__call__") as call:
        client.get_application()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == application_service.GetApplicationRequest()


@pytest.mark.asyncio
async def test_get_application_async(
    transport: str = "grpc_asyncio",
    request_type=application_service.GetApplicationRequest,
):
    client = ApplicationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_application), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            application.Application(
                name="name_value",
                external_id="external_id_value",
                profile="profile_value",
                job="job_value",
                company="company_value",
                stage=application.Application.ApplicationStage.NEW,
                state=application.Application.ApplicationState.IN_PROGRESS,
                outcome_notes="outcome_notes_value",
                outcome=common.Outcome.POSITIVE,
                job_title_snippet="job_title_snippet_value",
            )
        )
        response = await client.get_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == application_service.GetApplicationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, application.Application)
    assert response.name == "name_value"
    assert response.external_id == "external_id_value"
    assert response.profile == "profile_value"
    assert response.job == "job_value"
    assert response.company == "company_value"
    assert response.stage == application.Application.ApplicationStage.NEW
    assert response.state == application.Application.ApplicationState.IN_PROGRESS
    assert response.outcome_notes == "outcome_notes_value"
    assert response.outcome == common.Outcome.POSITIVE
    assert response.job_title_snippet == "job_title_snippet_value"


@pytest.mark.asyncio
async def test_get_application_async_from_dict():
    await test_get_application_async(request_type=dict)


def test_get_application_field_headers():
    client = ApplicationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = application_service.GetApplicationRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_application), "__call__") as call:
        call.return_value = application.Application()
        client.get_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_application_field_headers_async():
    client = ApplicationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = application_service.GetApplicationRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_application), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            application.Application()
        )
        await client.get_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_application_flattened():
    client = ApplicationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_application), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = application.Application()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_application(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_application_flattened_error():
    client = ApplicationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_application(
            application_service.GetApplicationRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_application_flattened_async():
    client = ApplicationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_application), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = application.Application()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            application.Application()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_application(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_application_flattened_error_async():
    client = ApplicationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_application(
            application_service.GetApplicationRequest(), name="name_value",
        )


def test_update_application(
    transport: str = "grpc", request_type=application_service.UpdateApplicationRequest
):
    client = ApplicationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_application), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gct_application.Application(
            name="name_value",
            external_id="external_id_value",
            profile="profile_value",
            job="job_value",
            company="company_value",
            stage=gct_application.Application.ApplicationStage.NEW,
            state=gct_application.Application.ApplicationState.IN_PROGRESS,
            outcome_notes="outcome_notes_value",
            outcome=common.Outcome.POSITIVE,
            job_title_snippet="job_title_snippet_value",
        )
        response = client.update_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == application_service.UpdateApplicationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gct_application.Application)
    assert response.name == "name_value"
    assert response.external_id == "external_id_value"
    assert response.profile == "profile_value"
    assert response.job == "job_value"
    assert response.company == "company_value"
    assert response.stage == gct_application.Application.ApplicationStage.NEW
    assert response.state == gct_application.Application.ApplicationState.IN_PROGRESS
    assert response.outcome_notes == "outcome_notes_value"
    assert response.outcome == common.Outcome.POSITIVE
    assert response.job_title_snippet == "job_title_snippet_value"


def test_update_application_from_dict():
    test_update_application(request_type=dict)


def test_update_application_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ApplicationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_application), "__call__"
    ) as call:
        client.update_application()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == application_service.UpdateApplicationRequest()


@pytest.mark.asyncio
async def test_update_application_async(
    transport: str = "grpc_asyncio",
    request_type=application_service.UpdateApplicationRequest,
):
    client = ApplicationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_application), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gct_application.Application(
                name="name_value",
                external_id="external_id_value",
                profile="profile_value",
                job="job_value",
                company="company_value",
                stage=gct_application.Application.ApplicationStage.NEW,
                state=gct_application.Application.ApplicationState.IN_PROGRESS,
                outcome_notes="outcome_notes_value",
                outcome=common.Outcome.POSITIVE,
                job_title_snippet="job_title_snippet_value",
            )
        )
        response = await client.update_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == application_service.UpdateApplicationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gct_application.Application)
    assert response.name == "name_value"
    assert response.external_id == "external_id_value"
    assert response.profile == "profile_value"
    assert response.job == "job_value"
    assert response.company == "company_value"
    assert response.stage == gct_application.Application.ApplicationStage.NEW
    assert response.state == gct_application.Application.ApplicationState.IN_PROGRESS
    assert response.outcome_notes == "outcome_notes_value"
    assert response.outcome == common.Outcome.POSITIVE
    assert response.job_title_snippet == "job_title_snippet_value"


@pytest.mark.asyncio
async def test_update_application_async_from_dict():
    await test_update_application_async(request_type=dict)


def test_update_application_field_headers():
    client = ApplicationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = application_service.UpdateApplicationRequest()

    request.application.name = "application.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_application), "__call__"
    ) as call:
        call.return_value = gct_application.Application()
        client.update_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "application.name=application.name/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_update_application_field_headers_async():
    client = ApplicationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = application_service.UpdateApplicationRequest()

    request.application.name = "application.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_application), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gct_application.Application()
        )
        await client.update_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "application.name=application.name/value",) in kw[
        "metadata"
    ]


def test_update_application_flattened():
    client = ApplicationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_application), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gct_application.Application()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_application(
            application=gct_application.Application(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].application == gct_application.Application(name="name_value")


def test_update_application_flattened_error():
    client = ApplicationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_application(
            application_service.UpdateApplicationRequest(),
            application=gct_application.Application(name="name_value"),
        )


@pytest.mark.asyncio
async def test_update_application_flattened_async():
    client = ApplicationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_application), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gct_application.Application()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gct_application.Application()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_application(
            application=gct_application.Application(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].application == gct_application.Application(name="name_value")


@pytest.mark.asyncio
async def test_update_application_flattened_error_async():
    client = ApplicationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_application(
            application_service.UpdateApplicationRequest(),
            application=gct_application.Application(name="name_value"),
        )


def test_delete_application(
    transport: str = "grpc", request_type=application_service.DeleteApplicationRequest
):
    client = ApplicationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_application), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == application_service.DeleteApplicationRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_application_from_dict():
    test_delete_application(request_type=dict)


def test_delete_application_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ApplicationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_application), "__call__"
    ) as call:
        client.delete_application()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == application_service.DeleteApplicationRequest()


@pytest.mark.asyncio
async def test_delete_application_async(
    transport: str = "grpc_asyncio",
    request_type=application_service.DeleteApplicationRequest,
):
    client = ApplicationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_application), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == application_service.DeleteApplicationRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_application_async_from_dict():
    await test_delete_application_async(request_type=dict)


def test_delete_application_field_headers():
    client = ApplicationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = application_service.DeleteApplicationRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_application), "__call__"
    ) as call:
        call.return_value = None
        client.delete_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_application_field_headers_async():
    client = ApplicationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = application_service.DeleteApplicationRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_application), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_application_flattened():
    client = ApplicationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_application), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_application(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_application_flattened_error():
    client = ApplicationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_application(
            application_service.DeleteApplicationRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_application_flattened_async():
    client = ApplicationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_application), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_application(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_application_flattened_error_async():
    client = ApplicationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_application(
            application_service.DeleteApplicationRequest(), name="name_value",
        )


def test_list_applications(
    transport: str = "grpc", request_type=application_service.ListApplicationsRequest
):
    client = ApplicationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_applications), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = application_service.ListApplicationsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_applications(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == application_service.ListApplicationsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListApplicationsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_applications_from_dict():
    test_list_applications(request_type=dict)


def test_list_applications_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ApplicationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_applications), "__call__"
    ) as call:
        client.list_applications()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == application_service.ListApplicationsRequest()


@pytest.mark.asyncio
async def test_list_applications_async(
    transport: str = "grpc_asyncio",
    request_type=application_service.ListApplicationsRequest,
):
    client = ApplicationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_applications), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            application_service.ListApplicationsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_applications(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == application_service.ListApplicationsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListApplicationsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_applications_async_from_dict():
    await test_list_applications_async(request_type=dict)


def test_list_applications_field_headers():
    client = ApplicationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = application_service.ListApplicationsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_applications), "__call__"
    ) as call:
        call.return_value = application_service.ListApplicationsResponse()
        client.list_applications(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_applications_field_headers_async():
    client = ApplicationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = application_service.ListApplicationsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_applications), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            application_service.ListApplicationsResponse()
        )
        await client.list_applications(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_applications_flattened():
    client = ApplicationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_applications), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = application_service.ListApplicationsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_applications(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_applications_flattened_error():
    client = ApplicationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_applications(
            application_service.ListApplicationsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_applications_flattened_async():
    client = ApplicationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_applications), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = application_service.ListApplicationsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            application_service.ListApplicationsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_applications(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_applications_flattened_error_async():
    client = ApplicationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_applications(
            application_service.ListApplicationsRequest(), parent="parent_value",
        )


def test_list_applications_pager():
    client = ApplicationServiceClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_applications), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            application_service.ListApplicationsResponse(
                applications=[
                    application.Application(),
                    application.Application(),
                    application.Application(),
                ],
                next_page_token="abc",
            ),
            application_service.ListApplicationsResponse(
                applications=[], next_page_token="def",
            ),
            application_service.ListApplicationsResponse(
                applications=[application.Application(),], next_page_token="ghi",
            ),
            application_service.ListApplicationsResponse(
                applications=[application.Application(), application.Application(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_applications(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, application.Application) for i in results)


def test_list_applications_pages():
    client = ApplicationServiceClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_applications), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            application_service.ListApplicationsResponse(
                applications=[
                    application.Application(),
                    application.Application(),
                    application.Application(),
                ],
                next_page_token="abc",
            ),
            application_service.ListApplicationsResponse(
                applications=[], next_page_token="def",
            ),
            application_service.ListApplicationsResponse(
                applications=[application.Application(),], next_page_token="ghi",
            ),
            application_service.ListApplicationsResponse(
                applications=[application.Application(), application.Application(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_applications(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_applications_async_pager():
    client = ApplicationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_applications),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            application_service.ListApplicationsResponse(
                applications=[
                    application.Application(),
                    application.Application(),
                    application.Application(),
                ],
                next_page_token="abc",
            ),
            application_service.ListApplicationsResponse(
                applications=[], next_page_token="def",
            ),
            application_service.ListApplicationsResponse(
                applications=[application.Application(),], next_page_token="ghi",
            ),
            application_service.ListApplicationsResponse(
                applications=[application.Application(), application.Application(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_applications(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, application.Application) for i in responses)


@pytest.mark.asyncio
async def test_list_applications_async_pages():
    client = ApplicationServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_applications),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            application_service.ListApplicationsResponse(
                applications=[
                    application.Application(),
                    application.Application(),
                    application.Application(),
                ],
                next_page_token="abc",
            ),
            application_service.ListApplicationsResponse(
                applications=[], next_page_token="def",
            ),
            application_service.ListApplicationsResponse(
                applications=[application.Application(),], next_page_token="ghi",
            ),
            application_service.ListApplicationsResponse(
                applications=[application.Application(), application.Application(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_applications(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.ApplicationServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ApplicationServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.ApplicationServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ApplicationServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.ApplicationServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ApplicationServiceClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ApplicationServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = ApplicationServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ApplicationServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.ApplicationServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ApplicationServiceGrpcTransport,
        transports.ApplicationServiceGrpcAsyncIOTransport,
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
    client = ApplicationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(client.transport, transports.ApplicationServiceGrpcTransport,)


def test_application_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.ApplicationServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_application_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.talent_v4beta1.services.application_service.transports.ApplicationServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.ApplicationServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_application",
        "get_application",
        "update_application",
        "delete_application",
        "list_applications",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


@requires_google_auth_gte_1_25_0
def test_application_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.talent_v4beta1.services.application_service.transports.ApplicationServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.ApplicationServiceTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/jobs",
            ),
            quota_project_id="octopus",
        )


@requires_google_auth_lt_1_25_0
def test_application_service_base_transport_with_credentials_file_old_google_auth():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.talent_v4beta1.services.application_service.transports.ApplicationServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.ApplicationServiceTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/jobs",
            ),
            quota_project_id="octopus",
        )


def test_application_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.talent_v4beta1.services.application_service.transports.ApplicationServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.ApplicationServiceTransport()
        adc.assert_called_once()


@requires_google_auth_gte_1_25_0
def test_application_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        ApplicationServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/jobs",
            ),
            quota_project_id=None,
        )


@requires_google_auth_lt_1_25_0
def test_application_service_auth_adc_old_google_auth():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        ApplicationServiceClient()
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/jobs",
            ),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ApplicationServiceGrpcTransport,
        transports.ApplicationServiceGrpcAsyncIOTransport,
    ],
)
@requires_google_auth_gte_1_25_0
def test_application_service_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/jobs",
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ApplicationServiceGrpcTransport,
        transports.ApplicationServiceGrpcAsyncIOTransport,
    ],
)
@requires_google_auth_lt_1_25_0
def test_application_service_transport_auth_adc_old_google_auth(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus")
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/jobs",
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.ApplicationServiceGrpcTransport, grpc_helpers),
        (transports.ApplicationServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_application_service_transport_create_channel(transport_class, grpc_helpers):
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
            "jobs.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/jobs",
            ),
            scopes=["1", "2"],
            default_host="jobs.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ApplicationServiceGrpcTransport,
        transports.ApplicationServiceGrpcAsyncIOTransport,
    ],
)
def test_application_service_grpc_transport_client_cert_source_for_mtls(
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


def test_application_service_host_no_port():
    client = ApplicationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(api_endpoint="jobs.googleapis.com"),
    )
    assert client.transport._host == "jobs.googleapis.com:443"


def test_application_service_host_with_port():
    client = ApplicationServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="jobs.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "jobs.googleapis.com:8000"


def test_application_service_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.ApplicationServiceGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_application_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.ApplicationServiceGrpcAsyncIOTransport(
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
        transports.ApplicationServiceGrpcTransport,
        transports.ApplicationServiceGrpcAsyncIOTransport,
    ],
)
def test_application_service_transport_channel_mtls_with_client_cert_source(
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
        transports.ApplicationServiceGrpcTransport,
        transports.ApplicationServiceGrpcAsyncIOTransport,
    ],
)
def test_application_service_transport_channel_mtls_with_adc(transport_class):
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


def test_application_path():
    project = "squid"
    tenant = "clam"
    profile = "whelk"
    application = "octopus"
    expected = "projects/{project}/tenants/{tenant}/profiles/{profile}/applications/{application}".format(
        project=project, tenant=tenant, profile=profile, application=application,
    )
    actual = ApplicationServiceClient.application_path(
        project, tenant, profile, application
    )
    assert expected == actual


def test_parse_application_path():
    expected = {
        "project": "oyster",
        "tenant": "nudibranch",
        "profile": "cuttlefish",
        "application": "mussel",
    }
    path = ApplicationServiceClient.application_path(**expected)

    # Check that the path construction is reversible.
    actual = ApplicationServiceClient.parse_application_path(path)
    assert expected == actual


def test_company_path():
    project = "winkle"
    tenant = "nautilus"
    company = "scallop"
    expected = "projects/{project}/tenants/{tenant}/companies/{company}".format(
        project=project, tenant=tenant, company=company,
    )
    actual = ApplicationServiceClient.company_path(project, tenant, company)
    assert expected == actual


def test_parse_company_path():
    expected = {
        "project": "abalone",
        "tenant": "squid",
        "company": "clam",
    }
    path = ApplicationServiceClient.company_path(**expected)

    # Check that the path construction is reversible.
    actual = ApplicationServiceClient.parse_company_path(path)
    assert expected == actual


def test_job_path():
    project = "whelk"
    tenant = "octopus"
    job = "oyster"
    expected = "projects/{project}/tenants/{tenant}/jobs/{job}".format(
        project=project, tenant=tenant, job=job,
    )
    actual = ApplicationServiceClient.job_path(project, tenant, job)
    assert expected == actual


def test_parse_job_path():
    expected = {
        "project": "nudibranch",
        "tenant": "cuttlefish",
        "job": "mussel",
    }
    path = ApplicationServiceClient.job_path(**expected)

    # Check that the path construction is reversible.
    actual = ApplicationServiceClient.parse_job_path(path)
    assert expected == actual


def test_profile_path():
    project = "winkle"
    tenant = "nautilus"
    profile = "scallop"
    expected = "projects/{project}/tenants/{tenant}/profiles/{profile}".format(
        project=project, tenant=tenant, profile=profile,
    )
    actual = ApplicationServiceClient.profile_path(project, tenant, profile)
    assert expected == actual


def test_parse_profile_path():
    expected = {
        "project": "abalone",
        "tenant": "squid",
        "profile": "clam",
    }
    path = ApplicationServiceClient.profile_path(**expected)

    # Check that the path construction is reversible.
    actual = ApplicationServiceClient.parse_profile_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "whelk"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = ApplicationServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "octopus",
    }
    path = ApplicationServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = ApplicationServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "oyster"
    expected = "folders/{folder}".format(folder=folder,)
    actual = ApplicationServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nudibranch",
    }
    path = ApplicationServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = ApplicationServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "cuttlefish"
    expected = "organizations/{organization}".format(organization=organization,)
    actual = ApplicationServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "mussel",
    }
    path = ApplicationServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = ApplicationServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "winkle"
    expected = "projects/{project}".format(project=project,)
    actual = ApplicationServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nautilus",
    }
    path = ApplicationServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = ApplicationServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "scallop"
    location = "abalone"
    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = ApplicationServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "squid",
        "location": "clam",
    }
    path = ApplicationServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = ApplicationServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.ApplicationServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = ApplicationServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.ApplicationServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = ApplicationServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
