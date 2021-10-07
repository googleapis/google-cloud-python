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
from google.api_core import path_template
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.osconfig_v1alpha.services.os_config_zonal_service import (
    OsConfigZonalServiceAsyncClient,
)
from google.cloud.osconfig_v1alpha.services.os_config_zonal_service import (
    OsConfigZonalServiceClient,
)
from google.cloud.osconfig_v1alpha.services.os_config_zonal_service import pagers
from google.cloud.osconfig_v1alpha.services.os_config_zonal_service import transports
from google.cloud.osconfig_v1alpha.services.os_config_zonal_service.transports.base import (
    _GOOGLE_AUTH_VERSION,
)
from google.cloud.osconfig_v1alpha.types import config_common
from google.cloud.osconfig_v1alpha.types import instance_os_policies_compliance
from google.cloud.osconfig_v1alpha.types import inventory
from google.cloud.osconfig_v1alpha.types import os_policy
from google.cloud.osconfig_v1alpha.types import os_policy_assignments
from google.cloud.osconfig_v1alpha.types import osconfig_common
from google.cloud.osconfig_v1alpha.types import vulnerability
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
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

    assert OsConfigZonalServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        OsConfigZonalServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        OsConfigZonalServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        OsConfigZonalServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        OsConfigZonalServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        OsConfigZonalServiceClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class", [OsConfigZonalServiceClient, OsConfigZonalServiceAsyncClient,]
)
def test_os_config_zonal_service_client_from_service_account_info(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "osconfig.googleapis.com:443"


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.OsConfigZonalServiceGrpcTransport, "grpc"),
        (transports.OsConfigZonalServiceGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_os_config_zonal_service_client_service_account_always_use_jwt(
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
    "client_class", [OsConfigZonalServiceClient, OsConfigZonalServiceAsyncClient,]
)
def test_os_config_zonal_service_client_from_service_account_file(client_class):
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

        assert client.transport._host == "osconfig.googleapis.com:443"


def test_os_config_zonal_service_client_get_transport_class():
    transport = OsConfigZonalServiceClient.get_transport_class()
    available_transports = [
        transports.OsConfigZonalServiceGrpcTransport,
    ]
    assert transport in available_transports

    transport = OsConfigZonalServiceClient.get_transport_class("grpc")
    assert transport == transports.OsConfigZonalServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            OsConfigZonalServiceClient,
            transports.OsConfigZonalServiceGrpcTransport,
            "grpc",
        ),
        (
            OsConfigZonalServiceAsyncClient,
            transports.OsConfigZonalServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    OsConfigZonalServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(OsConfigZonalServiceClient),
)
@mock.patch.object(
    OsConfigZonalServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(OsConfigZonalServiceAsyncClient),
)
def test_os_config_zonal_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(OsConfigZonalServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(OsConfigZonalServiceClient, "get_transport_class") as gtc:
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
            always_use_jwt_access=True,
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
                always_use_jwt_access=True,
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
                always_use_jwt_access=True,
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
            always_use_jwt_access=True,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (
            OsConfigZonalServiceClient,
            transports.OsConfigZonalServiceGrpcTransport,
            "grpc",
            "true",
        ),
        (
            OsConfigZonalServiceAsyncClient,
            transports.OsConfigZonalServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            OsConfigZonalServiceClient,
            transports.OsConfigZonalServiceGrpcTransport,
            "grpc",
            "false",
        ),
        (
            OsConfigZonalServiceAsyncClient,
            transports.OsConfigZonalServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    OsConfigZonalServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(OsConfigZonalServiceClient),
)
@mock.patch.object(
    OsConfigZonalServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(OsConfigZonalServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_os_config_zonal_service_client_mtls_env_auto(
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
                    client = client_class()
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
                client = client_class()
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
            OsConfigZonalServiceClient,
            transports.OsConfigZonalServiceGrpcTransport,
            "grpc",
        ),
        (
            OsConfigZonalServiceAsyncClient,
            transports.OsConfigZonalServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_os_config_zonal_service_client_client_options_scopes(
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
            always_use_jwt_access=True,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            OsConfigZonalServiceClient,
            transports.OsConfigZonalServiceGrpcTransport,
            "grpc",
        ),
        (
            OsConfigZonalServiceAsyncClient,
            transports.OsConfigZonalServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_os_config_zonal_service_client_client_options_credentials_file(
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
            always_use_jwt_access=True,
        )


def test_os_config_zonal_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.osconfig_v1alpha.services.os_config_zonal_service.transports.OsConfigZonalServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = OsConfigZonalServiceClient(
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


def test_create_os_policy_assignment(
    transport: str = "grpc",
    request_type=os_policy_assignments.CreateOSPolicyAssignmentRequest,
):
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_os_policy_assignment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_os_policy_assignment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == os_policy_assignments.CreateOSPolicyAssignmentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_os_policy_assignment_from_dict():
    test_create_os_policy_assignment(request_type=dict)


def test_create_os_policy_assignment_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_os_policy_assignment), "__call__"
    ) as call:
        client.create_os_policy_assignment()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == os_policy_assignments.CreateOSPolicyAssignmentRequest()


@pytest.mark.asyncio
async def test_create_os_policy_assignment_async(
    transport: str = "grpc_asyncio",
    request_type=os_policy_assignments.CreateOSPolicyAssignmentRequest,
):
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_os_policy_assignment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_os_policy_assignment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == os_policy_assignments.CreateOSPolicyAssignmentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_os_policy_assignment_async_from_dict():
    await test_create_os_policy_assignment_async(request_type=dict)


def test_create_os_policy_assignment_field_headers():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = os_policy_assignments.CreateOSPolicyAssignmentRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_os_policy_assignment), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_os_policy_assignment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_os_policy_assignment_field_headers_async():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = os_policy_assignments.CreateOSPolicyAssignmentRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_os_policy_assignment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_os_policy_assignment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_os_policy_assignment_flattened():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_os_policy_assignment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_os_policy_assignment(
            parent="parent_value",
            os_policy_assignment=os_policy_assignments.OSPolicyAssignment(
                name="name_value"
            ),
            os_policy_assignment_id="os_policy_assignment_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].os_policy_assignment == os_policy_assignments.OSPolicyAssignment(
            name="name_value"
        )
        assert args[0].os_policy_assignment_id == "os_policy_assignment_id_value"


def test_create_os_policy_assignment_flattened_error():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_os_policy_assignment(
            os_policy_assignments.CreateOSPolicyAssignmentRequest(),
            parent="parent_value",
            os_policy_assignment=os_policy_assignments.OSPolicyAssignment(
                name="name_value"
            ),
            os_policy_assignment_id="os_policy_assignment_id_value",
        )


@pytest.mark.asyncio
async def test_create_os_policy_assignment_flattened_async():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_os_policy_assignment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_os_policy_assignment(
            parent="parent_value",
            os_policy_assignment=os_policy_assignments.OSPolicyAssignment(
                name="name_value"
            ),
            os_policy_assignment_id="os_policy_assignment_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].os_policy_assignment == os_policy_assignments.OSPolicyAssignment(
            name="name_value"
        )
        assert args[0].os_policy_assignment_id == "os_policy_assignment_id_value"


@pytest.mark.asyncio
async def test_create_os_policy_assignment_flattened_error_async():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_os_policy_assignment(
            os_policy_assignments.CreateOSPolicyAssignmentRequest(),
            parent="parent_value",
            os_policy_assignment=os_policy_assignments.OSPolicyAssignment(
                name="name_value"
            ),
            os_policy_assignment_id="os_policy_assignment_id_value",
        )


def test_update_os_policy_assignment(
    transport: str = "grpc",
    request_type=os_policy_assignments.UpdateOSPolicyAssignmentRequest,
):
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_os_policy_assignment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_os_policy_assignment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == os_policy_assignments.UpdateOSPolicyAssignmentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_os_policy_assignment_from_dict():
    test_update_os_policy_assignment(request_type=dict)


def test_update_os_policy_assignment_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_os_policy_assignment), "__call__"
    ) as call:
        client.update_os_policy_assignment()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == os_policy_assignments.UpdateOSPolicyAssignmentRequest()


@pytest.mark.asyncio
async def test_update_os_policy_assignment_async(
    transport: str = "grpc_asyncio",
    request_type=os_policy_assignments.UpdateOSPolicyAssignmentRequest,
):
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_os_policy_assignment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_os_policy_assignment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == os_policy_assignments.UpdateOSPolicyAssignmentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_os_policy_assignment_async_from_dict():
    await test_update_os_policy_assignment_async(request_type=dict)


def test_update_os_policy_assignment_field_headers():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = os_policy_assignments.UpdateOSPolicyAssignmentRequest()

    request.os_policy_assignment.name = "os_policy_assignment.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_os_policy_assignment), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_os_policy_assignment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "os_policy_assignment.name=os_policy_assignment.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_os_policy_assignment_field_headers_async():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = os_policy_assignments.UpdateOSPolicyAssignmentRequest()

    request.os_policy_assignment.name = "os_policy_assignment.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_os_policy_assignment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_os_policy_assignment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "os_policy_assignment.name=os_policy_assignment.name/value",
    ) in kw["metadata"]


def test_update_os_policy_assignment_flattened():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_os_policy_assignment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_os_policy_assignment(
            os_policy_assignment=os_policy_assignments.OSPolicyAssignment(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].os_policy_assignment == os_policy_assignments.OSPolicyAssignment(
            name="name_value"
        )
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


def test_update_os_policy_assignment_flattened_error():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_os_policy_assignment(
            os_policy_assignments.UpdateOSPolicyAssignmentRequest(),
            os_policy_assignment=os_policy_assignments.OSPolicyAssignment(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_os_policy_assignment_flattened_async():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_os_policy_assignment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_os_policy_assignment(
            os_policy_assignment=os_policy_assignments.OSPolicyAssignment(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].os_policy_assignment == os_policy_assignments.OSPolicyAssignment(
            name="name_value"
        )
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_os_policy_assignment_flattened_error_async():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_os_policy_assignment(
            os_policy_assignments.UpdateOSPolicyAssignmentRequest(),
            os_policy_assignment=os_policy_assignments.OSPolicyAssignment(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_get_os_policy_assignment(
    transport: str = "grpc",
    request_type=os_policy_assignments.GetOSPolicyAssignmentRequest,
):
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_os_policy_assignment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = os_policy_assignments.OSPolicyAssignment(
            name="name_value",
            description="description_value",
            revision_id="revision_id_value",
            rollout_state=os_policy_assignments.OSPolicyAssignment.RolloutState.IN_PROGRESS,
            baseline=True,
            deleted=True,
            reconciling=True,
            uid="uid_value",
        )
        response = client.get_os_policy_assignment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == os_policy_assignments.GetOSPolicyAssignmentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, os_policy_assignments.OSPolicyAssignment)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.revision_id == "revision_id_value"
    assert (
        response.rollout_state
        == os_policy_assignments.OSPolicyAssignment.RolloutState.IN_PROGRESS
    )
    assert response.baseline is True
    assert response.deleted is True
    assert response.reconciling is True
    assert response.uid == "uid_value"


def test_get_os_policy_assignment_from_dict():
    test_get_os_policy_assignment(request_type=dict)


def test_get_os_policy_assignment_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_os_policy_assignment), "__call__"
    ) as call:
        client.get_os_policy_assignment()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == os_policy_assignments.GetOSPolicyAssignmentRequest()


@pytest.mark.asyncio
async def test_get_os_policy_assignment_async(
    transport: str = "grpc_asyncio",
    request_type=os_policy_assignments.GetOSPolicyAssignmentRequest,
):
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_os_policy_assignment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            os_policy_assignments.OSPolicyAssignment(
                name="name_value",
                description="description_value",
                revision_id="revision_id_value",
                rollout_state=os_policy_assignments.OSPolicyAssignment.RolloutState.IN_PROGRESS,
                baseline=True,
                deleted=True,
                reconciling=True,
                uid="uid_value",
            )
        )
        response = await client.get_os_policy_assignment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == os_policy_assignments.GetOSPolicyAssignmentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, os_policy_assignments.OSPolicyAssignment)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.revision_id == "revision_id_value"
    assert (
        response.rollout_state
        == os_policy_assignments.OSPolicyAssignment.RolloutState.IN_PROGRESS
    )
    assert response.baseline is True
    assert response.deleted is True
    assert response.reconciling is True
    assert response.uid == "uid_value"


@pytest.mark.asyncio
async def test_get_os_policy_assignment_async_from_dict():
    await test_get_os_policy_assignment_async(request_type=dict)


def test_get_os_policy_assignment_field_headers():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = os_policy_assignments.GetOSPolicyAssignmentRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_os_policy_assignment), "__call__"
    ) as call:
        call.return_value = os_policy_assignments.OSPolicyAssignment()
        client.get_os_policy_assignment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_os_policy_assignment_field_headers_async():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = os_policy_assignments.GetOSPolicyAssignmentRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_os_policy_assignment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            os_policy_assignments.OSPolicyAssignment()
        )
        await client.get_os_policy_assignment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_os_policy_assignment_flattened():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_os_policy_assignment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = os_policy_assignments.OSPolicyAssignment()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_os_policy_assignment(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_os_policy_assignment_flattened_error():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_os_policy_assignment(
            os_policy_assignments.GetOSPolicyAssignmentRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_os_policy_assignment_flattened_async():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_os_policy_assignment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = os_policy_assignments.OSPolicyAssignment()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            os_policy_assignments.OSPolicyAssignment()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_os_policy_assignment(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_os_policy_assignment_flattened_error_async():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_os_policy_assignment(
            os_policy_assignments.GetOSPolicyAssignmentRequest(), name="name_value",
        )


def test_list_os_policy_assignments(
    transport: str = "grpc",
    request_type=os_policy_assignments.ListOSPolicyAssignmentsRequest,
):
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_os_policy_assignments), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = os_policy_assignments.ListOSPolicyAssignmentsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_os_policy_assignments(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == os_policy_assignments.ListOSPolicyAssignmentsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListOSPolicyAssignmentsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_os_policy_assignments_from_dict():
    test_list_os_policy_assignments(request_type=dict)


def test_list_os_policy_assignments_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_os_policy_assignments), "__call__"
    ) as call:
        client.list_os_policy_assignments()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == os_policy_assignments.ListOSPolicyAssignmentsRequest()


@pytest.mark.asyncio
async def test_list_os_policy_assignments_async(
    transport: str = "grpc_asyncio",
    request_type=os_policy_assignments.ListOSPolicyAssignmentsRequest,
):
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_os_policy_assignments), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            os_policy_assignments.ListOSPolicyAssignmentsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_os_policy_assignments(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == os_policy_assignments.ListOSPolicyAssignmentsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListOSPolicyAssignmentsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_os_policy_assignments_async_from_dict():
    await test_list_os_policy_assignments_async(request_type=dict)


def test_list_os_policy_assignments_field_headers():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = os_policy_assignments.ListOSPolicyAssignmentsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_os_policy_assignments), "__call__"
    ) as call:
        call.return_value = os_policy_assignments.ListOSPolicyAssignmentsResponse()
        client.list_os_policy_assignments(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_os_policy_assignments_field_headers_async():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = os_policy_assignments.ListOSPolicyAssignmentsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_os_policy_assignments), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            os_policy_assignments.ListOSPolicyAssignmentsResponse()
        )
        await client.list_os_policy_assignments(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_os_policy_assignments_flattened():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_os_policy_assignments), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = os_policy_assignments.ListOSPolicyAssignmentsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_os_policy_assignments(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_os_policy_assignments_flattened_error():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_os_policy_assignments(
            os_policy_assignments.ListOSPolicyAssignmentsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_os_policy_assignments_flattened_async():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_os_policy_assignments), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = os_policy_assignments.ListOSPolicyAssignmentsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            os_policy_assignments.ListOSPolicyAssignmentsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_os_policy_assignments(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_os_policy_assignments_flattened_error_async():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_os_policy_assignments(
            os_policy_assignments.ListOSPolicyAssignmentsRequest(),
            parent="parent_value",
        )


def test_list_os_policy_assignments_pager():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_os_policy_assignments), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            os_policy_assignments.ListOSPolicyAssignmentsResponse(
                os_policy_assignments=[
                    os_policy_assignments.OSPolicyAssignment(),
                    os_policy_assignments.OSPolicyAssignment(),
                    os_policy_assignments.OSPolicyAssignment(),
                ],
                next_page_token="abc",
            ),
            os_policy_assignments.ListOSPolicyAssignmentsResponse(
                os_policy_assignments=[], next_page_token="def",
            ),
            os_policy_assignments.ListOSPolicyAssignmentsResponse(
                os_policy_assignments=[os_policy_assignments.OSPolicyAssignment(),],
                next_page_token="ghi",
            ),
            os_policy_assignments.ListOSPolicyAssignmentsResponse(
                os_policy_assignments=[
                    os_policy_assignments.OSPolicyAssignment(),
                    os_policy_assignments.OSPolicyAssignment(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_os_policy_assignments(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(
            isinstance(i, os_policy_assignments.OSPolicyAssignment) for i in results
        )


def test_list_os_policy_assignments_pages():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_os_policy_assignments), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            os_policy_assignments.ListOSPolicyAssignmentsResponse(
                os_policy_assignments=[
                    os_policy_assignments.OSPolicyAssignment(),
                    os_policy_assignments.OSPolicyAssignment(),
                    os_policy_assignments.OSPolicyAssignment(),
                ],
                next_page_token="abc",
            ),
            os_policy_assignments.ListOSPolicyAssignmentsResponse(
                os_policy_assignments=[], next_page_token="def",
            ),
            os_policy_assignments.ListOSPolicyAssignmentsResponse(
                os_policy_assignments=[os_policy_assignments.OSPolicyAssignment(),],
                next_page_token="ghi",
            ),
            os_policy_assignments.ListOSPolicyAssignmentsResponse(
                os_policy_assignments=[
                    os_policy_assignments.OSPolicyAssignment(),
                    os_policy_assignments.OSPolicyAssignment(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_os_policy_assignments(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_os_policy_assignments_async_pager():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_os_policy_assignments),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            os_policy_assignments.ListOSPolicyAssignmentsResponse(
                os_policy_assignments=[
                    os_policy_assignments.OSPolicyAssignment(),
                    os_policy_assignments.OSPolicyAssignment(),
                    os_policy_assignments.OSPolicyAssignment(),
                ],
                next_page_token="abc",
            ),
            os_policy_assignments.ListOSPolicyAssignmentsResponse(
                os_policy_assignments=[], next_page_token="def",
            ),
            os_policy_assignments.ListOSPolicyAssignmentsResponse(
                os_policy_assignments=[os_policy_assignments.OSPolicyAssignment(),],
                next_page_token="ghi",
            ),
            os_policy_assignments.ListOSPolicyAssignmentsResponse(
                os_policy_assignments=[
                    os_policy_assignments.OSPolicyAssignment(),
                    os_policy_assignments.OSPolicyAssignment(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_os_policy_assignments(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, os_policy_assignments.OSPolicyAssignment) for i in responses
        )


@pytest.mark.asyncio
async def test_list_os_policy_assignments_async_pages():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_os_policy_assignments),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            os_policy_assignments.ListOSPolicyAssignmentsResponse(
                os_policy_assignments=[
                    os_policy_assignments.OSPolicyAssignment(),
                    os_policy_assignments.OSPolicyAssignment(),
                    os_policy_assignments.OSPolicyAssignment(),
                ],
                next_page_token="abc",
            ),
            os_policy_assignments.ListOSPolicyAssignmentsResponse(
                os_policy_assignments=[], next_page_token="def",
            ),
            os_policy_assignments.ListOSPolicyAssignmentsResponse(
                os_policy_assignments=[os_policy_assignments.OSPolicyAssignment(),],
                next_page_token="ghi",
            ),
            os_policy_assignments.ListOSPolicyAssignmentsResponse(
                os_policy_assignments=[
                    os_policy_assignments.OSPolicyAssignment(),
                    os_policy_assignments.OSPolicyAssignment(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_os_policy_assignments(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_list_os_policy_assignment_revisions(
    transport: str = "grpc",
    request_type=os_policy_assignments.ListOSPolicyAssignmentRevisionsRequest,
):
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_os_policy_assignment_revisions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = os_policy_assignments.ListOSPolicyAssignmentRevisionsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_os_policy_assignment_revisions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == os_policy_assignments.ListOSPolicyAssignmentRevisionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListOSPolicyAssignmentRevisionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_os_policy_assignment_revisions_from_dict():
    test_list_os_policy_assignment_revisions(request_type=dict)


def test_list_os_policy_assignment_revisions_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_os_policy_assignment_revisions), "__call__"
    ) as call:
        client.list_os_policy_assignment_revisions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == os_policy_assignments.ListOSPolicyAssignmentRevisionsRequest()


@pytest.mark.asyncio
async def test_list_os_policy_assignment_revisions_async(
    transport: str = "grpc_asyncio",
    request_type=os_policy_assignments.ListOSPolicyAssignmentRevisionsRequest,
):
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_os_policy_assignment_revisions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            os_policy_assignments.ListOSPolicyAssignmentRevisionsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_os_policy_assignment_revisions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == os_policy_assignments.ListOSPolicyAssignmentRevisionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListOSPolicyAssignmentRevisionsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_os_policy_assignment_revisions_async_from_dict():
    await test_list_os_policy_assignment_revisions_async(request_type=dict)


def test_list_os_policy_assignment_revisions_field_headers():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = os_policy_assignments.ListOSPolicyAssignmentRevisionsRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_os_policy_assignment_revisions), "__call__"
    ) as call:
        call.return_value = (
            os_policy_assignments.ListOSPolicyAssignmentRevisionsResponse()
        )
        client.list_os_policy_assignment_revisions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_os_policy_assignment_revisions_field_headers_async():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = os_policy_assignments.ListOSPolicyAssignmentRevisionsRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_os_policy_assignment_revisions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            os_policy_assignments.ListOSPolicyAssignmentRevisionsResponse()
        )
        await client.list_os_policy_assignment_revisions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_list_os_policy_assignment_revisions_flattened():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_os_policy_assignment_revisions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            os_policy_assignments.ListOSPolicyAssignmentRevisionsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_os_policy_assignment_revisions(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_list_os_policy_assignment_revisions_flattened_error():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_os_policy_assignment_revisions(
            os_policy_assignments.ListOSPolicyAssignmentRevisionsRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_list_os_policy_assignment_revisions_flattened_async():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_os_policy_assignment_revisions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            os_policy_assignments.ListOSPolicyAssignmentRevisionsResponse()
        )

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            os_policy_assignments.ListOSPolicyAssignmentRevisionsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_os_policy_assignment_revisions(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_list_os_policy_assignment_revisions_flattened_error_async():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_os_policy_assignment_revisions(
            os_policy_assignments.ListOSPolicyAssignmentRevisionsRequest(),
            name="name_value",
        )


def test_list_os_policy_assignment_revisions_pager():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_os_policy_assignment_revisions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            os_policy_assignments.ListOSPolicyAssignmentRevisionsResponse(
                os_policy_assignments=[
                    os_policy_assignments.OSPolicyAssignment(),
                    os_policy_assignments.OSPolicyAssignment(),
                    os_policy_assignments.OSPolicyAssignment(),
                ],
                next_page_token="abc",
            ),
            os_policy_assignments.ListOSPolicyAssignmentRevisionsResponse(
                os_policy_assignments=[], next_page_token="def",
            ),
            os_policy_assignments.ListOSPolicyAssignmentRevisionsResponse(
                os_policy_assignments=[os_policy_assignments.OSPolicyAssignment(),],
                next_page_token="ghi",
            ),
            os_policy_assignments.ListOSPolicyAssignmentRevisionsResponse(
                os_policy_assignments=[
                    os_policy_assignments.OSPolicyAssignment(),
                    os_policy_assignments.OSPolicyAssignment(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", ""),)),
        )
        pager = client.list_os_policy_assignment_revisions(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(
            isinstance(i, os_policy_assignments.OSPolicyAssignment) for i in results
        )


def test_list_os_policy_assignment_revisions_pages():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_os_policy_assignment_revisions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            os_policy_assignments.ListOSPolicyAssignmentRevisionsResponse(
                os_policy_assignments=[
                    os_policy_assignments.OSPolicyAssignment(),
                    os_policy_assignments.OSPolicyAssignment(),
                    os_policy_assignments.OSPolicyAssignment(),
                ],
                next_page_token="abc",
            ),
            os_policy_assignments.ListOSPolicyAssignmentRevisionsResponse(
                os_policy_assignments=[], next_page_token="def",
            ),
            os_policy_assignments.ListOSPolicyAssignmentRevisionsResponse(
                os_policy_assignments=[os_policy_assignments.OSPolicyAssignment(),],
                next_page_token="ghi",
            ),
            os_policy_assignments.ListOSPolicyAssignmentRevisionsResponse(
                os_policy_assignments=[
                    os_policy_assignments.OSPolicyAssignment(),
                    os_policy_assignments.OSPolicyAssignment(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_os_policy_assignment_revisions(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_os_policy_assignment_revisions_async_pager():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_os_policy_assignment_revisions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            os_policy_assignments.ListOSPolicyAssignmentRevisionsResponse(
                os_policy_assignments=[
                    os_policy_assignments.OSPolicyAssignment(),
                    os_policy_assignments.OSPolicyAssignment(),
                    os_policy_assignments.OSPolicyAssignment(),
                ],
                next_page_token="abc",
            ),
            os_policy_assignments.ListOSPolicyAssignmentRevisionsResponse(
                os_policy_assignments=[], next_page_token="def",
            ),
            os_policy_assignments.ListOSPolicyAssignmentRevisionsResponse(
                os_policy_assignments=[os_policy_assignments.OSPolicyAssignment(),],
                next_page_token="ghi",
            ),
            os_policy_assignments.ListOSPolicyAssignmentRevisionsResponse(
                os_policy_assignments=[
                    os_policy_assignments.OSPolicyAssignment(),
                    os_policy_assignments.OSPolicyAssignment(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_os_policy_assignment_revisions(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, os_policy_assignments.OSPolicyAssignment) for i in responses
        )


@pytest.mark.asyncio
async def test_list_os_policy_assignment_revisions_async_pages():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_os_policy_assignment_revisions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            os_policy_assignments.ListOSPolicyAssignmentRevisionsResponse(
                os_policy_assignments=[
                    os_policy_assignments.OSPolicyAssignment(),
                    os_policy_assignments.OSPolicyAssignment(),
                    os_policy_assignments.OSPolicyAssignment(),
                ],
                next_page_token="abc",
            ),
            os_policy_assignments.ListOSPolicyAssignmentRevisionsResponse(
                os_policy_assignments=[], next_page_token="def",
            ),
            os_policy_assignments.ListOSPolicyAssignmentRevisionsResponse(
                os_policy_assignments=[os_policy_assignments.OSPolicyAssignment(),],
                next_page_token="ghi",
            ),
            os_policy_assignments.ListOSPolicyAssignmentRevisionsResponse(
                os_policy_assignments=[
                    os_policy_assignments.OSPolicyAssignment(),
                    os_policy_assignments.OSPolicyAssignment(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_os_policy_assignment_revisions(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_delete_os_policy_assignment(
    transport: str = "grpc",
    request_type=os_policy_assignments.DeleteOSPolicyAssignmentRequest,
):
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_os_policy_assignment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_os_policy_assignment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == os_policy_assignments.DeleteOSPolicyAssignmentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_os_policy_assignment_from_dict():
    test_delete_os_policy_assignment(request_type=dict)


def test_delete_os_policy_assignment_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_os_policy_assignment), "__call__"
    ) as call:
        client.delete_os_policy_assignment()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == os_policy_assignments.DeleteOSPolicyAssignmentRequest()


@pytest.mark.asyncio
async def test_delete_os_policy_assignment_async(
    transport: str = "grpc_asyncio",
    request_type=os_policy_assignments.DeleteOSPolicyAssignmentRequest,
):
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_os_policy_assignment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_os_policy_assignment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == os_policy_assignments.DeleteOSPolicyAssignmentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_os_policy_assignment_async_from_dict():
    await test_delete_os_policy_assignment_async(request_type=dict)


def test_delete_os_policy_assignment_field_headers():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = os_policy_assignments.DeleteOSPolicyAssignmentRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_os_policy_assignment), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_os_policy_assignment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_os_policy_assignment_field_headers_async():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = os_policy_assignments.DeleteOSPolicyAssignmentRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_os_policy_assignment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_os_policy_assignment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_os_policy_assignment_flattened():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_os_policy_assignment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_os_policy_assignment(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_os_policy_assignment_flattened_error():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_os_policy_assignment(
            os_policy_assignments.DeleteOSPolicyAssignmentRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_os_policy_assignment_flattened_async():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_os_policy_assignment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_os_policy_assignment(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_os_policy_assignment_flattened_error_async():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_os_policy_assignment(
            os_policy_assignments.DeleteOSPolicyAssignmentRequest(), name="name_value",
        )


def test_get_instance_os_policies_compliance(
    transport: str = "grpc",
    request_type=instance_os_policies_compliance.GetInstanceOSPoliciesComplianceRequest,
):
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_instance_os_policies_compliance), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = instance_os_policies_compliance.InstanceOSPoliciesCompliance(
            name="name_value",
            instance="instance_value",
            state=config_common.OSPolicyComplianceState.COMPLIANT,
            detailed_state="detailed_state_value",
            detailed_state_reason="detailed_state_reason_value",
            last_compliance_run_id="last_compliance_run_id_value",
        )
        response = client.get_instance_os_policies_compliance(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == instance_os_policies_compliance.GetInstanceOSPoliciesComplianceRequest()
        )

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, instance_os_policies_compliance.InstanceOSPoliciesCompliance
    )
    assert response.name == "name_value"
    assert response.instance == "instance_value"
    assert response.state == config_common.OSPolicyComplianceState.COMPLIANT
    assert response.detailed_state == "detailed_state_value"
    assert response.detailed_state_reason == "detailed_state_reason_value"
    assert response.last_compliance_run_id == "last_compliance_run_id_value"


def test_get_instance_os_policies_compliance_from_dict():
    test_get_instance_os_policies_compliance(request_type=dict)


def test_get_instance_os_policies_compliance_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_instance_os_policies_compliance), "__call__"
    ) as call:
        client.get_instance_os_policies_compliance()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == instance_os_policies_compliance.GetInstanceOSPoliciesComplianceRequest()
        )


@pytest.mark.asyncio
async def test_get_instance_os_policies_compliance_async(
    transport: str = "grpc_asyncio",
    request_type=instance_os_policies_compliance.GetInstanceOSPoliciesComplianceRequest,
):
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_instance_os_policies_compliance), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            instance_os_policies_compliance.InstanceOSPoliciesCompliance(
                name="name_value",
                instance="instance_value",
                state=config_common.OSPolicyComplianceState.COMPLIANT,
                detailed_state="detailed_state_value",
                detailed_state_reason="detailed_state_reason_value",
                last_compliance_run_id="last_compliance_run_id_value",
            )
        )
        response = await client.get_instance_os_policies_compliance(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == instance_os_policies_compliance.GetInstanceOSPoliciesComplianceRequest()
        )

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, instance_os_policies_compliance.InstanceOSPoliciesCompliance
    )
    assert response.name == "name_value"
    assert response.instance == "instance_value"
    assert response.state == config_common.OSPolicyComplianceState.COMPLIANT
    assert response.detailed_state == "detailed_state_value"
    assert response.detailed_state_reason == "detailed_state_reason_value"
    assert response.last_compliance_run_id == "last_compliance_run_id_value"


@pytest.mark.asyncio
async def test_get_instance_os_policies_compliance_async_from_dict():
    await test_get_instance_os_policies_compliance_async(request_type=dict)


def test_get_instance_os_policies_compliance_field_headers():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = instance_os_policies_compliance.GetInstanceOSPoliciesComplianceRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_instance_os_policies_compliance), "__call__"
    ) as call:
        call.return_value = (
            instance_os_policies_compliance.InstanceOSPoliciesCompliance()
        )
        client.get_instance_os_policies_compliance(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_instance_os_policies_compliance_field_headers_async():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = instance_os_policies_compliance.GetInstanceOSPoliciesComplianceRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_instance_os_policies_compliance), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            instance_os_policies_compliance.InstanceOSPoliciesCompliance()
        )
        await client.get_instance_os_policies_compliance(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_instance_os_policies_compliance_flattened():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_instance_os_policies_compliance), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            instance_os_policies_compliance.InstanceOSPoliciesCompliance()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_instance_os_policies_compliance(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_instance_os_policies_compliance_flattened_error():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_instance_os_policies_compliance(
            instance_os_policies_compliance.GetInstanceOSPoliciesComplianceRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_instance_os_policies_compliance_flattened_async():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_instance_os_policies_compliance), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            instance_os_policies_compliance.InstanceOSPoliciesCompliance()
        )

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            instance_os_policies_compliance.InstanceOSPoliciesCompliance()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_instance_os_policies_compliance(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_instance_os_policies_compliance_flattened_error_async():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_instance_os_policies_compliance(
            instance_os_policies_compliance.GetInstanceOSPoliciesComplianceRequest(),
            name="name_value",
        )


def test_list_instance_os_policies_compliances(
    transport: str = "grpc",
    request_type=instance_os_policies_compliance.ListInstanceOSPoliciesCompliancesRequest,
):
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_instance_os_policies_compliances), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = instance_os_policies_compliance.ListInstanceOSPoliciesCompliancesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_instance_os_policies_compliances(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == instance_os_policies_compliance.ListInstanceOSPoliciesCompliancesRequest()
        )

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListInstanceOSPoliciesCompliancesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_instance_os_policies_compliances_from_dict():
    test_list_instance_os_policies_compliances(request_type=dict)


def test_list_instance_os_policies_compliances_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_instance_os_policies_compliances), "__call__"
    ) as call:
        client.list_instance_os_policies_compliances()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == instance_os_policies_compliance.ListInstanceOSPoliciesCompliancesRequest()
        )


@pytest.mark.asyncio
async def test_list_instance_os_policies_compliances_async(
    transport: str = "grpc_asyncio",
    request_type=instance_os_policies_compliance.ListInstanceOSPoliciesCompliancesRequest,
):
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_instance_os_policies_compliances), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            instance_os_policies_compliance.ListInstanceOSPoliciesCompliancesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_instance_os_policies_compliances(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == instance_os_policies_compliance.ListInstanceOSPoliciesCompliancesRequest()
        )

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListInstanceOSPoliciesCompliancesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_instance_os_policies_compliances_async_from_dict():
    await test_list_instance_os_policies_compliances_async(request_type=dict)


def test_list_instance_os_policies_compliances_field_headers():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = instance_os_policies_compliance.ListInstanceOSPoliciesCompliancesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_instance_os_policies_compliances), "__call__"
    ) as call:
        call.return_value = (
            instance_os_policies_compliance.ListInstanceOSPoliciesCompliancesResponse()
        )
        client.list_instance_os_policies_compliances(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_instance_os_policies_compliances_field_headers_async():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = instance_os_policies_compliance.ListInstanceOSPoliciesCompliancesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_instance_os_policies_compliances), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            instance_os_policies_compliance.ListInstanceOSPoliciesCompliancesResponse()
        )
        await client.list_instance_os_policies_compliances(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_instance_os_policies_compliances_flattened():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_instance_os_policies_compliances), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            instance_os_policies_compliance.ListInstanceOSPoliciesCompliancesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_instance_os_policies_compliances(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_instance_os_policies_compliances_flattened_error():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_instance_os_policies_compliances(
            instance_os_policies_compliance.ListInstanceOSPoliciesCompliancesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_instance_os_policies_compliances_flattened_async():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_instance_os_policies_compliances), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            instance_os_policies_compliance.ListInstanceOSPoliciesCompliancesResponse()
        )

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            instance_os_policies_compliance.ListInstanceOSPoliciesCompliancesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_instance_os_policies_compliances(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_instance_os_policies_compliances_flattened_error_async():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_instance_os_policies_compliances(
            instance_os_policies_compliance.ListInstanceOSPoliciesCompliancesRequest(),
            parent="parent_value",
        )


def test_list_instance_os_policies_compliances_pager():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_instance_os_policies_compliances), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            instance_os_policies_compliance.ListInstanceOSPoliciesCompliancesResponse(
                instance_os_policies_compliances=[
                    instance_os_policies_compliance.InstanceOSPoliciesCompliance(),
                    instance_os_policies_compliance.InstanceOSPoliciesCompliance(),
                    instance_os_policies_compliance.InstanceOSPoliciesCompliance(),
                ],
                next_page_token="abc",
            ),
            instance_os_policies_compliance.ListInstanceOSPoliciesCompliancesResponse(
                instance_os_policies_compliances=[], next_page_token="def",
            ),
            instance_os_policies_compliance.ListInstanceOSPoliciesCompliancesResponse(
                instance_os_policies_compliances=[
                    instance_os_policies_compliance.InstanceOSPoliciesCompliance(),
                ],
                next_page_token="ghi",
            ),
            instance_os_policies_compliance.ListInstanceOSPoliciesCompliancesResponse(
                instance_os_policies_compliances=[
                    instance_os_policies_compliance.InstanceOSPoliciesCompliance(),
                    instance_os_policies_compliance.InstanceOSPoliciesCompliance(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_instance_os_policies_compliances(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(
            isinstance(i, instance_os_policies_compliance.InstanceOSPoliciesCompliance)
            for i in results
        )


def test_list_instance_os_policies_compliances_pages():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_instance_os_policies_compliances), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            instance_os_policies_compliance.ListInstanceOSPoliciesCompliancesResponse(
                instance_os_policies_compliances=[
                    instance_os_policies_compliance.InstanceOSPoliciesCompliance(),
                    instance_os_policies_compliance.InstanceOSPoliciesCompliance(),
                    instance_os_policies_compliance.InstanceOSPoliciesCompliance(),
                ],
                next_page_token="abc",
            ),
            instance_os_policies_compliance.ListInstanceOSPoliciesCompliancesResponse(
                instance_os_policies_compliances=[], next_page_token="def",
            ),
            instance_os_policies_compliance.ListInstanceOSPoliciesCompliancesResponse(
                instance_os_policies_compliances=[
                    instance_os_policies_compliance.InstanceOSPoliciesCompliance(),
                ],
                next_page_token="ghi",
            ),
            instance_os_policies_compliance.ListInstanceOSPoliciesCompliancesResponse(
                instance_os_policies_compliances=[
                    instance_os_policies_compliance.InstanceOSPoliciesCompliance(),
                    instance_os_policies_compliance.InstanceOSPoliciesCompliance(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_instance_os_policies_compliances(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_instance_os_policies_compliances_async_pager():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_instance_os_policies_compliances),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            instance_os_policies_compliance.ListInstanceOSPoliciesCompliancesResponse(
                instance_os_policies_compliances=[
                    instance_os_policies_compliance.InstanceOSPoliciesCompliance(),
                    instance_os_policies_compliance.InstanceOSPoliciesCompliance(),
                    instance_os_policies_compliance.InstanceOSPoliciesCompliance(),
                ],
                next_page_token="abc",
            ),
            instance_os_policies_compliance.ListInstanceOSPoliciesCompliancesResponse(
                instance_os_policies_compliances=[], next_page_token="def",
            ),
            instance_os_policies_compliance.ListInstanceOSPoliciesCompliancesResponse(
                instance_os_policies_compliances=[
                    instance_os_policies_compliance.InstanceOSPoliciesCompliance(),
                ],
                next_page_token="ghi",
            ),
            instance_os_policies_compliance.ListInstanceOSPoliciesCompliancesResponse(
                instance_os_policies_compliances=[
                    instance_os_policies_compliance.InstanceOSPoliciesCompliance(),
                    instance_os_policies_compliance.InstanceOSPoliciesCompliance(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_instance_os_policies_compliances(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, instance_os_policies_compliance.InstanceOSPoliciesCompliance)
            for i in responses
        )


@pytest.mark.asyncio
async def test_list_instance_os_policies_compliances_async_pages():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_instance_os_policies_compliances),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            instance_os_policies_compliance.ListInstanceOSPoliciesCompliancesResponse(
                instance_os_policies_compliances=[
                    instance_os_policies_compliance.InstanceOSPoliciesCompliance(),
                    instance_os_policies_compliance.InstanceOSPoliciesCompliance(),
                    instance_os_policies_compliance.InstanceOSPoliciesCompliance(),
                ],
                next_page_token="abc",
            ),
            instance_os_policies_compliance.ListInstanceOSPoliciesCompliancesResponse(
                instance_os_policies_compliances=[], next_page_token="def",
            ),
            instance_os_policies_compliance.ListInstanceOSPoliciesCompliancesResponse(
                instance_os_policies_compliances=[
                    instance_os_policies_compliance.InstanceOSPoliciesCompliance(),
                ],
                next_page_token="ghi",
            ),
            instance_os_policies_compliance.ListInstanceOSPoliciesCompliancesResponse(
                instance_os_policies_compliances=[
                    instance_os_policies_compliance.InstanceOSPoliciesCompliance(),
                    instance_os_policies_compliance.InstanceOSPoliciesCompliance(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_instance_os_policies_compliances(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_inventory(
    transport: str = "grpc", request_type=inventory.GetInventoryRequest
):
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_inventory), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = inventory.Inventory(name="name_value",)
        response = client.get_inventory(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == inventory.GetInventoryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, inventory.Inventory)
    assert response.name == "name_value"


def test_get_inventory_from_dict():
    test_get_inventory(request_type=dict)


def test_get_inventory_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_inventory), "__call__") as call:
        client.get_inventory()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == inventory.GetInventoryRequest()


@pytest.mark.asyncio
async def test_get_inventory_async(
    transport: str = "grpc_asyncio", request_type=inventory.GetInventoryRequest
):
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_inventory), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            inventory.Inventory(name="name_value",)
        )
        response = await client.get_inventory(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == inventory.GetInventoryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, inventory.Inventory)
    assert response.name == "name_value"


@pytest.mark.asyncio
async def test_get_inventory_async_from_dict():
    await test_get_inventory_async(request_type=dict)


def test_get_inventory_field_headers():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = inventory.GetInventoryRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_inventory), "__call__") as call:
        call.return_value = inventory.Inventory()
        client.get_inventory(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_inventory_field_headers_async():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = inventory.GetInventoryRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_inventory), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(inventory.Inventory())
        await client.get_inventory(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_inventory_flattened():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_inventory), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = inventory.Inventory()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_inventory(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_inventory_flattened_error():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_inventory(
            inventory.GetInventoryRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_inventory_flattened_async():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_inventory), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = inventory.Inventory()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(inventory.Inventory())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_inventory(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_inventory_flattened_error_async():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_inventory(
            inventory.GetInventoryRequest(), name="name_value",
        )


def test_list_inventories(
    transport: str = "grpc", request_type=inventory.ListInventoriesRequest
):
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_inventories), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = inventory.ListInventoriesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_inventories(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == inventory.ListInventoriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListInventoriesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_inventories_from_dict():
    test_list_inventories(request_type=dict)


def test_list_inventories_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_inventories), "__call__") as call:
        client.list_inventories()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == inventory.ListInventoriesRequest()


@pytest.mark.asyncio
async def test_list_inventories_async(
    transport: str = "grpc_asyncio", request_type=inventory.ListInventoriesRequest
):
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_inventories), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            inventory.ListInventoriesResponse(next_page_token="next_page_token_value",)
        )
        response = await client.list_inventories(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == inventory.ListInventoriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListInventoriesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_inventories_async_from_dict():
    await test_list_inventories_async(request_type=dict)


def test_list_inventories_field_headers():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = inventory.ListInventoriesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_inventories), "__call__") as call:
        call.return_value = inventory.ListInventoriesResponse()
        client.list_inventories(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_inventories_field_headers_async():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = inventory.ListInventoriesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_inventories), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            inventory.ListInventoriesResponse()
        )
        await client.list_inventories(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_inventories_flattened():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_inventories), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = inventory.ListInventoriesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_inventories(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_inventories_flattened_error():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_inventories(
            inventory.ListInventoriesRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_inventories_flattened_async():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_inventories), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = inventory.ListInventoriesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            inventory.ListInventoriesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_inventories(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_inventories_flattened_error_async():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_inventories(
            inventory.ListInventoriesRequest(), parent="parent_value",
        )


def test_list_inventories_pager():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_inventories), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            inventory.ListInventoriesResponse(
                inventories=[
                    inventory.Inventory(),
                    inventory.Inventory(),
                    inventory.Inventory(),
                ],
                next_page_token="abc",
            ),
            inventory.ListInventoriesResponse(inventories=[], next_page_token="def",),
            inventory.ListInventoriesResponse(
                inventories=[inventory.Inventory(),], next_page_token="ghi",
            ),
            inventory.ListInventoriesResponse(
                inventories=[inventory.Inventory(), inventory.Inventory(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_inventories(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, inventory.Inventory) for i in results)


def test_list_inventories_pages():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_inventories), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            inventory.ListInventoriesResponse(
                inventories=[
                    inventory.Inventory(),
                    inventory.Inventory(),
                    inventory.Inventory(),
                ],
                next_page_token="abc",
            ),
            inventory.ListInventoriesResponse(inventories=[], next_page_token="def",),
            inventory.ListInventoriesResponse(
                inventories=[inventory.Inventory(),], next_page_token="ghi",
            ),
            inventory.ListInventoriesResponse(
                inventories=[inventory.Inventory(), inventory.Inventory(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_inventories(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_inventories_async_pager():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_inventories), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            inventory.ListInventoriesResponse(
                inventories=[
                    inventory.Inventory(),
                    inventory.Inventory(),
                    inventory.Inventory(),
                ],
                next_page_token="abc",
            ),
            inventory.ListInventoriesResponse(inventories=[], next_page_token="def",),
            inventory.ListInventoriesResponse(
                inventories=[inventory.Inventory(),], next_page_token="ghi",
            ),
            inventory.ListInventoriesResponse(
                inventories=[inventory.Inventory(), inventory.Inventory(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_inventories(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, inventory.Inventory) for i in responses)


@pytest.mark.asyncio
async def test_list_inventories_async_pages():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_inventories), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            inventory.ListInventoriesResponse(
                inventories=[
                    inventory.Inventory(),
                    inventory.Inventory(),
                    inventory.Inventory(),
                ],
                next_page_token="abc",
            ),
            inventory.ListInventoriesResponse(inventories=[], next_page_token="def",),
            inventory.ListInventoriesResponse(
                inventories=[inventory.Inventory(),], next_page_token="ghi",
            ),
            inventory.ListInventoriesResponse(
                inventories=[inventory.Inventory(), inventory.Inventory(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_inventories(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_vulnerability_report(
    transport: str = "grpc", request_type=vulnerability.GetVulnerabilityReportRequest
):
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_vulnerability_report), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = vulnerability.VulnerabilityReport(name="name_value",)
        response = client.get_vulnerability_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vulnerability.GetVulnerabilityReportRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, vulnerability.VulnerabilityReport)
    assert response.name == "name_value"


def test_get_vulnerability_report_from_dict():
    test_get_vulnerability_report(request_type=dict)


def test_get_vulnerability_report_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_vulnerability_report), "__call__"
    ) as call:
        client.get_vulnerability_report()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vulnerability.GetVulnerabilityReportRequest()


@pytest.mark.asyncio
async def test_get_vulnerability_report_async(
    transport: str = "grpc_asyncio",
    request_type=vulnerability.GetVulnerabilityReportRequest,
):
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_vulnerability_report), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vulnerability.VulnerabilityReport(name="name_value",)
        )
        response = await client.get_vulnerability_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vulnerability.GetVulnerabilityReportRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, vulnerability.VulnerabilityReport)
    assert response.name == "name_value"


@pytest.mark.asyncio
async def test_get_vulnerability_report_async_from_dict():
    await test_get_vulnerability_report_async(request_type=dict)


def test_get_vulnerability_report_field_headers():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vulnerability.GetVulnerabilityReportRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_vulnerability_report), "__call__"
    ) as call:
        call.return_value = vulnerability.VulnerabilityReport()
        client.get_vulnerability_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_vulnerability_report_field_headers_async():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vulnerability.GetVulnerabilityReportRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_vulnerability_report), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vulnerability.VulnerabilityReport()
        )
        await client.get_vulnerability_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_vulnerability_report_flattened():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_vulnerability_report), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = vulnerability.VulnerabilityReport()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_vulnerability_report(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_vulnerability_report_flattened_error():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_vulnerability_report(
            vulnerability.GetVulnerabilityReportRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_vulnerability_report_flattened_async():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_vulnerability_report), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = vulnerability.VulnerabilityReport()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vulnerability.VulnerabilityReport()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_vulnerability_report(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_vulnerability_report_flattened_error_async():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_vulnerability_report(
            vulnerability.GetVulnerabilityReportRequest(), name="name_value",
        )


def test_list_vulnerability_reports(
    transport: str = "grpc", request_type=vulnerability.ListVulnerabilityReportsRequest
):
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vulnerability_reports), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = vulnerability.ListVulnerabilityReportsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_vulnerability_reports(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == vulnerability.ListVulnerabilityReportsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListVulnerabilityReportsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_vulnerability_reports_from_dict():
    test_list_vulnerability_reports(request_type=dict)


def test_list_vulnerability_reports_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vulnerability_reports), "__call__"
    ) as call:
        client.list_vulnerability_reports()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == vulnerability.ListVulnerabilityReportsRequest()


@pytest.mark.asyncio
async def test_list_vulnerability_reports_async(
    transport: str = "grpc_asyncio",
    request_type=vulnerability.ListVulnerabilityReportsRequest,
):
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vulnerability_reports), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vulnerability.ListVulnerabilityReportsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_vulnerability_reports(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == vulnerability.ListVulnerabilityReportsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListVulnerabilityReportsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_vulnerability_reports_async_from_dict():
    await test_list_vulnerability_reports_async(request_type=dict)


def test_list_vulnerability_reports_field_headers():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vulnerability.ListVulnerabilityReportsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vulnerability_reports), "__call__"
    ) as call:
        call.return_value = vulnerability.ListVulnerabilityReportsResponse()
        client.list_vulnerability_reports(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_vulnerability_reports_field_headers_async():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = vulnerability.ListVulnerabilityReportsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vulnerability_reports), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vulnerability.ListVulnerabilityReportsResponse()
        )
        await client.list_vulnerability_reports(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_vulnerability_reports_flattened():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vulnerability_reports), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = vulnerability.ListVulnerabilityReportsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_vulnerability_reports(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_vulnerability_reports_flattened_error():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_vulnerability_reports(
            vulnerability.ListVulnerabilityReportsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_vulnerability_reports_flattened_async():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vulnerability_reports), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = vulnerability.ListVulnerabilityReportsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            vulnerability.ListVulnerabilityReportsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_vulnerability_reports(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_vulnerability_reports_flattened_error_async():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_vulnerability_reports(
            vulnerability.ListVulnerabilityReportsRequest(), parent="parent_value",
        )


def test_list_vulnerability_reports_pager():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vulnerability_reports), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            vulnerability.ListVulnerabilityReportsResponse(
                vulnerability_reports=[
                    vulnerability.VulnerabilityReport(),
                    vulnerability.VulnerabilityReport(),
                    vulnerability.VulnerabilityReport(),
                ],
                next_page_token="abc",
            ),
            vulnerability.ListVulnerabilityReportsResponse(
                vulnerability_reports=[], next_page_token="def",
            ),
            vulnerability.ListVulnerabilityReportsResponse(
                vulnerability_reports=[vulnerability.VulnerabilityReport(),],
                next_page_token="ghi",
            ),
            vulnerability.ListVulnerabilityReportsResponse(
                vulnerability_reports=[
                    vulnerability.VulnerabilityReport(),
                    vulnerability.VulnerabilityReport(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_vulnerability_reports(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, vulnerability.VulnerabilityReport) for i in results)


def test_list_vulnerability_reports_pages():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vulnerability_reports), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            vulnerability.ListVulnerabilityReportsResponse(
                vulnerability_reports=[
                    vulnerability.VulnerabilityReport(),
                    vulnerability.VulnerabilityReport(),
                    vulnerability.VulnerabilityReport(),
                ],
                next_page_token="abc",
            ),
            vulnerability.ListVulnerabilityReportsResponse(
                vulnerability_reports=[], next_page_token="def",
            ),
            vulnerability.ListVulnerabilityReportsResponse(
                vulnerability_reports=[vulnerability.VulnerabilityReport(),],
                next_page_token="ghi",
            ),
            vulnerability.ListVulnerabilityReportsResponse(
                vulnerability_reports=[
                    vulnerability.VulnerabilityReport(),
                    vulnerability.VulnerabilityReport(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_vulnerability_reports(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_vulnerability_reports_async_pager():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vulnerability_reports),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            vulnerability.ListVulnerabilityReportsResponse(
                vulnerability_reports=[
                    vulnerability.VulnerabilityReport(),
                    vulnerability.VulnerabilityReport(),
                    vulnerability.VulnerabilityReport(),
                ],
                next_page_token="abc",
            ),
            vulnerability.ListVulnerabilityReportsResponse(
                vulnerability_reports=[], next_page_token="def",
            ),
            vulnerability.ListVulnerabilityReportsResponse(
                vulnerability_reports=[vulnerability.VulnerabilityReport(),],
                next_page_token="ghi",
            ),
            vulnerability.ListVulnerabilityReportsResponse(
                vulnerability_reports=[
                    vulnerability.VulnerabilityReport(),
                    vulnerability.VulnerabilityReport(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_vulnerability_reports(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, vulnerability.VulnerabilityReport) for i in responses)


@pytest.mark.asyncio
async def test_list_vulnerability_reports_async_pages():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vulnerability_reports),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            vulnerability.ListVulnerabilityReportsResponse(
                vulnerability_reports=[
                    vulnerability.VulnerabilityReport(),
                    vulnerability.VulnerabilityReport(),
                    vulnerability.VulnerabilityReport(),
                ],
                next_page_token="abc",
            ),
            vulnerability.ListVulnerabilityReportsResponse(
                vulnerability_reports=[], next_page_token="def",
            ),
            vulnerability.ListVulnerabilityReportsResponse(
                vulnerability_reports=[vulnerability.VulnerabilityReport(),],
                next_page_token="ghi",
            ),
            vulnerability.ListVulnerabilityReportsResponse(
                vulnerability_reports=[
                    vulnerability.VulnerabilityReport(),
                    vulnerability.VulnerabilityReport(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_vulnerability_reports(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.OsConfigZonalServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = OsConfigZonalServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.OsConfigZonalServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = OsConfigZonalServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.OsConfigZonalServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = OsConfigZonalServiceClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.OsConfigZonalServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = OsConfigZonalServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.OsConfigZonalServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.OsConfigZonalServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.OsConfigZonalServiceGrpcTransport,
        transports.OsConfigZonalServiceGrpcAsyncIOTransport,
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
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(client.transport, transports.OsConfigZonalServiceGrpcTransport,)


def test_os_config_zonal_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.OsConfigZonalServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_os_config_zonal_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.osconfig_v1alpha.services.os_config_zonal_service.transports.OsConfigZonalServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.OsConfigZonalServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_os_policy_assignment",
        "update_os_policy_assignment",
        "get_os_policy_assignment",
        "list_os_policy_assignments",
        "list_os_policy_assignment_revisions",
        "delete_os_policy_assignment",
        "get_instance_os_policies_compliance",
        "list_instance_os_policies_compliances",
        "get_inventory",
        "list_inventories",
        "get_vulnerability_report",
        "list_vulnerability_reports",
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


@requires_google_auth_gte_1_25_0
def test_os_config_zonal_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.osconfig_v1alpha.services.os_config_zonal_service.transports.OsConfigZonalServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.OsConfigZonalServiceTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


@requires_google_auth_lt_1_25_0
def test_os_config_zonal_service_base_transport_with_credentials_file_old_google_auth():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.osconfig_v1alpha.services.os_config_zonal_service.transports.OsConfigZonalServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.OsConfigZonalServiceTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_os_config_zonal_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.osconfig_v1alpha.services.os_config_zonal_service.transports.OsConfigZonalServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.OsConfigZonalServiceTransport()
        adc.assert_called_once()


@requires_google_auth_gte_1_25_0
def test_os_config_zonal_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        OsConfigZonalServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@requires_google_auth_lt_1_25_0
def test_os_config_zonal_service_auth_adc_old_google_auth():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        OsConfigZonalServiceClient()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.OsConfigZonalServiceGrpcTransport,
        transports.OsConfigZonalServiceGrpcAsyncIOTransport,
    ],
)
@requires_google_auth_gte_1_25_0
def test_os_config_zonal_service_transport_auth_adc(transport_class):
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
        transports.OsConfigZonalServiceGrpcTransport,
        transports.OsConfigZonalServiceGrpcAsyncIOTransport,
    ],
)
@requires_google_auth_lt_1_25_0
def test_os_config_zonal_service_transport_auth_adc_old_google_auth(transport_class):
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
        (transports.OsConfigZonalServiceGrpcTransport, grpc_helpers),
        (transports.OsConfigZonalServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_os_config_zonal_service_transport_create_channel(
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
            "osconfig.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="osconfig.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.OsConfigZonalServiceGrpcTransport,
        transports.OsConfigZonalServiceGrpcAsyncIOTransport,
    ],
)
def test_os_config_zonal_service_grpc_transport_client_cert_source_for_mtls(
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


def test_os_config_zonal_service_host_no_port():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="osconfig.googleapis.com"
        ),
    )
    assert client.transport._host == "osconfig.googleapis.com:443"


def test_os_config_zonal_service_host_with_port():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="osconfig.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "osconfig.googleapis.com:8000"


def test_os_config_zonal_service_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.OsConfigZonalServiceGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_os_config_zonal_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.OsConfigZonalServiceGrpcAsyncIOTransport(
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
        transports.OsConfigZonalServiceGrpcTransport,
        transports.OsConfigZonalServiceGrpcAsyncIOTransport,
    ],
)
def test_os_config_zonal_service_transport_channel_mtls_with_client_cert_source(
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
        transports.OsConfigZonalServiceGrpcTransport,
        transports.OsConfigZonalServiceGrpcAsyncIOTransport,
    ],
)
def test_os_config_zonal_service_transport_channel_mtls_with_adc(transport_class):
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


def test_os_config_zonal_service_grpc_lro_client():
    client = OsConfigZonalServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_os_config_zonal_service_grpc_lro_async_client():
    client = OsConfigZonalServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc_asyncio",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsAsyncClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_instance_path():
    project = "squid"
    location = "clam"
    instance = "whelk"
    expected = "projects/{project}/locations/{location}/instances/{instance}".format(
        project=project, location=location, instance=instance,
    )
    actual = OsConfigZonalServiceClient.instance_path(project, location, instance)
    assert expected == actual


def test_parse_instance_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "instance": "nudibranch",
    }
    path = OsConfigZonalServiceClient.instance_path(**expected)

    # Check that the path construction is reversible.
    actual = OsConfigZonalServiceClient.parse_instance_path(path)
    assert expected == actual


def test_instance_os_policies_compliance_path():
    project = "cuttlefish"
    location = "mussel"
    instance = "winkle"
    expected = "projects/{project}/locations/{location}/instanceOSPoliciesCompliances/{instance}".format(
        project=project, location=location, instance=instance,
    )
    actual = OsConfigZonalServiceClient.instance_os_policies_compliance_path(
        project, location, instance
    )
    assert expected == actual


def test_parse_instance_os_policies_compliance_path():
    expected = {
        "project": "nautilus",
        "location": "scallop",
        "instance": "abalone",
    }
    path = OsConfigZonalServiceClient.instance_os_policies_compliance_path(**expected)

    # Check that the path construction is reversible.
    actual = OsConfigZonalServiceClient.parse_instance_os_policies_compliance_path(path)
    assert expected == actual


def test_inventory_path():
    project = "squid"
    location = "clam"
    instance = "whelk"
    expected = "projects/{project}/locations/{location}/instances/{instance}/inventory".format(
        project=project, location=location, instance=instance,
    )
    actual = OsConfigZonalServiceClient.inventory_path(project, location, instance)
    assert expected == actual


def test_parse_inventory_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "instance": "nudibranch",
    }
    path = OsConfigZonalServiceClient.inventory_path(**expected)

    # Check that the path construction is reversible.
    actual = OsConfigZonalServiceClient.parse_inventory_path(path)
    assert expected == actual


def test_os_policy_assignment_path():
    project = "cuttlefish"
    location = "mussel"
    os_policy_assignment = "winkle"
    expected = "projects/{project}/locations/{location}/osPolicyAssignments/{os_policy_assignment}".format(
        project=project, location=location, os_policy_assignment=os_policy_assignment,
    )
    actual = OsConfigZonalServiceClient.os_policy_assignment_path(
        project, location, os_policy_assignment
    )
    assert expected == actual


def test_parse_os_policy_assignment_path():
    expected = {
        "project": "nautilus",
        "location": "scallop",
        "os_policy_assignment": "abalone",
    }
    path = OsConfigZonalServiceClient.os_policy_assignment_path(**expected)

    # Check that the path construction is reversible.
    actual = OsConfigZonalServiceClient.parse_os_policy_assignment_path(path)
    assert expected == actual


def test_vulnerability_report_path():
    project = "squid"
    location = "clam"
    instance = "whelk"
    expected = "projects/{project}/locations/{location}/instances/{instance}/vulnerabilityReport".format(
        project=project, location=location, instance=instance,
    )
    actual = OsConfigZonalServiceClient.vulnerability_report_path(
        project, location, instance
    )
    assert expected == actual


def test_parse_vulnerability_report_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "instance": "nudibranch",
    }
    path = OsConfigZonalServiceClient.vulnerability_report_path(**expected)

    # Check that the path construction is reversible.
    actual = OsConfigZonalServiceClient.parse_vulnerability_report_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "cuttlefish"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = OsConfigZonalServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "mussel",
    }
    path = OsConfigZonalServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = OsConfigZonalServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "winkle"
    expected = "folders/{folder}".format(folder=folder,)
    actual = OsConfigZonalServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nautilus",
    }
    path = OsConfigZonalServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = OsConfigZonalServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "scallop"
    expected = "organizations/{organization}".format(organization=organization,)
    actual = OsConfigZonalServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "abalone",
    }
    path = OsConfigZonalServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = OsConfigZonalServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "squid"
    expected = "projects/{project}".format(project=project,)
    actual = OsConfigZonalServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "clam",
    }
    path = OsConfigZonalServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = OsConfigZonalServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "whelk"
    location = "octopus"
    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = OsConfigZonalServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
    }
    path = OsConfigZonalServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = OsConfigZonalServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.OsConfigZonalServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = OsConfigZonalServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.OsConfigZonalServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = OsConfigZonalServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = OsConfigZonalServiceAsyncClient(
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
        client = OsConfigZonalServiceClient(
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
        client = OsConfigZonalServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()
