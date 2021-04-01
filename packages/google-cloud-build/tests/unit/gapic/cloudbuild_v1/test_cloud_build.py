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

from google import auth
from google.api import httpbody_pb2 as httpbody  # type: ignore
from google.api_core import client_options
from google.api_core import exceptions
from google.api_core import future
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.api_core import operation_async  # type: ignore
from google.api_core import operations_v1
from google.auth import credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.devtools.cloudbuild_v1.services.cloud_build import (
    CloudBuildAsyncClient,
)
from google.cloud.devtools.cloudbuild_v1.services.cloud_build import CloudBuildClient
from google.cloud.devtools.cloudbuild_v1.services.cloud_build import pagers
from google.cloud.devtools.cloudbuild_v1.services.cloud_build import transports
from google.cloud.devtools.cloudbuild_v1.types import cloudbuild
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import any_pb2 as gp_any  # type: ignore
from google.protobuf import duration_pb2 as duration  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore


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

    assert CloudBuildClient._get_default_mtls_endpoint(None) is None
    assert (
        CloudBuildClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    )
    assert (
        CloudBuildClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        CloudBuildClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        CloudBuildClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert CloudBuildClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize("client_class", [CloudBuildClient, CloudBuildAsyncClient,])
def test_cloud_build_client_from_service_account_info(client_class):
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "cloudbuild.googleapis.com:443"


@pytest.mark.parametrize("client_class", [CloudBuildClient, CloudBuildAsyncClient,])
def test_cloud_build_client_from_service_account_file(client_class):
    creds = credentials.AnonymousCredentials()
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

        assert client.transport._host == "cloudbuild.googleapis.com:443"


def test_cloud_build_client_get_transport_class():
    transport = CloudBuildClient.get_transport_class()
    available_transports = [
        transports.CloudBuildGrpcTransport,
    ]
    assert transport in available_transports

    transport = CloudBuildClient.get_transport_class("grpc")
    assert transport == transports.CloudBuildGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (CloudBuildClient, transports.CloudBuildGrpcTransport, "grpc"),
        (
            CloudBuildAsyncClient,
            transports.CloudBuildGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    CloudBuildClient, "DEFAULT_ENDPOINT", modify_default_endpoint(CloudBuildClient)
)
@mock.patch.object(
    CloudBuildAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CloudBuildAsyncClient),
)
def test_cloud_build_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(CloudBuildClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(CloudBuildClient, "get_transport_class") as gtc:
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
        (CloudBuildClient, transports.CloudBuildGrpcTransport, "grpc", "true"),
        (
            CloudBuildAsyncClient,
            transports.CloudBuildGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (CloudBuildClient, transports.CloudBuildGrpcTransport, "grpc", "false"),
        (
            CloudBuildAsyncClient,
            transports.CloudBuildGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    CloudBuildClient, "DEFAULT_ENDPOINT", modify_default_endpoint(CloudBuildClient)
)
@mock.patch.object(
    CloudBuildAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CloudBuildAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_cloud_build_client_mtls_env_auto(
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
        (CloudBuildClient, transports.CloudBuildGrpcTransport, "grpc"),
        (
            CloudBuildAsyncClient,
            transports.CloudBuildGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_cloud_build_client_client_options_scopes(
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
        (CloudBuildClient, transports.CloudBuildGrpcTransport, "grpc"),
        (
            CloudBuildAsyncClient,
            transports.CloudBuildGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_cloud_build_client_client_options_credentials_file(
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


def test_cloud_build_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.devtools.cloudbuild_v1.services.cloud_build.transports.CloudBuildGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = CloudBuildClient(client_options={"api_endpoint": "squid.clam.whelk"})
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_create_build(
    transport: str = "grpc", request_type=cloudbuild.CreateBuildRequest
):
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")

        response = client.create_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.CreateBuildRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_build_from_dict():
    test_create_build(request_type=dict)


def test_create_build_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_build), "__call__") as call:
        client.create_build()
        call.assert_called()
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.CreateBuildRequest()


@pytest.mark.asyncio
async def test_create_build_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.CreateBuildRequest
):
    client = CloudBuildAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )

        response = await client.create_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.CreateBuildRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_build_async_from_dict():
    await test_create_build_async(request_type=dict)


def test_create_build_flattened():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_build(
            project_id="project_id_value", build=cloudbuild.Build(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].build == cloudbuild.Build(name="name_value")


def test_create_build_flattened_error():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_build(
            cloudbuild.CreateBuildRequest(),
            project_id="project_id_value",
            build=cloudbuild.Build(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_build_flattened_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_build(
            project_id="project_id_value", build=cloudbuild.Build(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].build == cloudbuild.Build(name="name_value")


@pytest.mark.asyncio
async def test_create_build_flattened_error_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_build(
            cloudbuild.CreateBuildRequest(),
            project_id="project_id_value",
            build=cloudbuild.Build(name="name_value"),
        )


def test_get_build(transport: str = "grpc", request_type=cloudbuild.GetBuildRequest):
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.Build(
            name="name_value",
            id="id_value",
            project_id="project_id_value",
            status=cloudbuild.Build.Status.QUEUED,
            status_detail="status_detail_value",
            images=["images_value"],
            logs_bucket="logs_bucket_value",
            build_trigger_id="build_trigger_id_value",
            log_url="log_url_value",
            tags=["tags_value"],
            service_account="service_account_value",
        )

        response = client.get_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.GetBuildRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cloudbuild.Build)

    assert response.name == "name_value"

    assert response.id == "id_value"

    assert response.project_id == "project_id_value"

    assert response.status == cloudbuild.Build.Status.QUEUED

    assert response.status_detail == "status_detail_value"

    assert response.images == ["images_value"]

    assert response.logs_bucket == "logs_bucket_value"

    assert response.build_trigger_id == "build_trigger_id_value"

    assert response.log_url == "log_url_value"

    assert response.tags == ["tags_value"]

    assert response.service_account == "service_account_value"


def test_get_build_from_dict():
    test_get_build(request_type=dict)


def test_get_build_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_build), "__call__") as call:
        client.get_build()
        call.assert_called()
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.GetBuildRequest()


@pytest.mark.asyncio
async def test_get_build_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.GetBuildRequest
):
    client = CloudBuildAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.Build(
                name="name_value",
                id="id_value",
                project_id="project_id_value",
                status=cloudbuild.Build.Status.QUEUED,
                status_detail="status_detail_value",
                images=["images_value"],
                logs_bucket="logs_bucket_value",
                build_trigger_id="build_trigger_id_value",
                log_url="log_url_value",
                tags=["tags_value"],
                service_account="service_account_value",
            )
        )

        response = await client.get_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.GetBuildRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.Build)

    assert response.name == "name_value"

    assert response.id == "id_value"

    assert response.project_id == "project_id_value"

    assert response.status == cloudbuild.Build.Status.QUEUED

    assert response.status_detail == "status_detail_value"

    assert response.images == ["images_value"]

    assert response.logs_bucket == "logs_bucket_value"

    assert response.build_trigger_id == "build_trigger_id_value"

    assert response.log_url == "log_url_value"

    assert response.tags == ["tags_value"]

    assert response.service_account == "service_account_value"


@pytest.mark.asyncio
async def test_get_build_async_from_dict():
    await test_get_build_async(request_type=dict)


def test_get_build_flattened():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.Build()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_build(
            project_id="project_id_value", id="id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].id == "id_value"


def test_get_build_flattened_error():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_build(
            cloudbuild.GetBuildRequest(), project_id="project_id_value", id="id_value",
        )


@pytest.mark.asyncio
async def test_get_build_flattened_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.Build()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(cloudbuild.Build())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_build(project_id="project_id_value", id="id_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].id == "id_value"


@pytest.mark.asyncio
async def test_get_build_flattened_error_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_build(
            cloudbuild.GetBuildRequest(), project_id="project_id_value", id="id_value",
        )


def test_list_builds(
    transport: str = "grpc", request_type=cloudbuild.ListBuildsRequest
):
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_builds), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.ListBuildsResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_builds(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.ListBuildsRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, pagers.ListBuildsPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_builds_from_dict():
    test_list_builds(request_type=dict)


def test_list_builds_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_builds), "__call__") as call:
        client.list_builds()
        call.assert_called()
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.ListBuildsRequest()


@pytest.mark.asyncio
async def test_list_builds_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.ListBuildsRequest
):
    client = CloudBuildAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_builds), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.ListBuildsResponse(next_page_token="next_page_token_value",)
        )

        response = await client.list_builds(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.ListBuildsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBuildsAsyncPager)

    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_builds_async_from_dict():
    await test_list_builds_async(request_type=dict)


def test_list_builds_flattened():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_builds), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.ListBuildsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_builds(
            project_id="project_id_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].filter == "filter_value"


def test_list_builds_flattened_error():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_builds(
            cloudbuild.ListBuildsRequest(),
            project_id="project_id_value",
            filter="filter_value",
        )


@pytest.mark.asyncio
async def test_list_builds_flattened_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_builds), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.ListBuildsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.ListBuildsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_builds(
            project_id="project_id_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].filter == "filter_value"


@pytest.mark.asyncio
async def test_list_builds_flattened_error_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_builds(
            cloudbuild.ListBuildsRequest(),
            project_id="project_id_value",
            filter="filter_value",
        )


def test_list_builds_pager():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_builds), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListBuildsResponse(
                builds=[cloudbuild.Build(), cloudbuild.Build(), cloudbuild.Build(),],
                next_page_token="abc",
            ),
            cloudbuild.ListBuildsResponse(builds=[], next_page_token="def",),
            cloudbuild.ListBuildsResponse(
                builds=[cloudbuild.Build(),], next_page_token="ghi",
            ),
            cloudbuild.ListBuildsResponse(
                builds=[cloudbuild.Build(), cloudbuild.Build(),],
            ),
            RuntimeError,
        )

        metadata = ()
        pager = client.list_builds(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, cloudbuild.Build) for i in results)


def test_list_builds_pages():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_builds), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListBuildsResponse(
                builds=[cloudbuild.Build(), cloudbuild.Build(), cloudbuild.Build(),],
                next_page_token="abc",
            ),
            cloudbuild.ListBuildsResponse(builds=[], next_page_token="def",),
            cloudbuild.ListBuildsResponse(
                builds=[cloudbuild.Build(),], next_page_token="ghi",
            ),
            cloudbuild.ListBuildsResponse(
                builds=[cloudbuild.Build(), cloudbuild.Build(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_builds(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_builds_async_pager():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_builds), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListBuildsResponse(
                builds=[cloudbuild.Build(), cloudbuild.Build(), cloudbuild.Build(),],
                next_page_token="abc",
            ),
            cloudbuild.ListBuildsResponse(builds=[], next_page_token="def",),
            cloudbuild.ListBuildsResponse(
                builds=[cloudbuild.Build(),], next_page_token="ghi",
            ),
            cloudbuild.ListBuildsResponse(
                builds=[cloudbuild.Build(), cloudbuild.Build(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_builds(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, cloudbuild.Build) for i in responses)


@pytest.mark.asyncio
async def test_list_builds_async_pages():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_builds), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListBuildsResponse(
                builds=[cloudbuild.Build(), cloudbuild.Build(), cloudbuild.Build(),],
                next_page_token="abc",
            ),
            cloudbuild.ListBuildsResponse(builds=[], next_page_token="def",),
            cloudbuild.ListBuildsResponse(
                builds=[cloudbuild.Build(),], next_page_token="ghi",
            ),
            cloudbuild.ListBuildsResponse(
                builds=[cloudbuild.Build(), cloudbuild.Build(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_builds(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_cancel_build(
    transport: str = "grpc", request_type=cloudbuild.CancelBuildRequest
):
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.Build(
            name="name_value",
            id="id_value",
            project_id="project_id_value",
            status=cloudbuild.Build.Status.QUEUED,
            status_detail="status_detail_value",
            images=["images_value"],
            logs_bucket="logs_bucket_value",
            build_trigger_id="build_trigger_id_value",
            log_url="log_url_value",
            tags=["tags_value"],
            service_account="service_account_value",
        )

        response = client.cancel_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.CancelBuildRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cloudbuild.Build)

    assert response.name == "name_value"

    assert response.id == "id_value"

    assert response.project_id == "project_id_value"

    assert response.status == cloudbuild.Build.Status.QUEUED

    assert response.status_detail == "status_detail_value"

    assert response.images == ["images_value"]

    assert response.logs_bucket == "logs_bucket_value"

    assert response.build_trigger_id == "build_trigger_id_value"

    assert response.log_url == "log_url_value"

    assert response.tags == ["tags_value"]

    assert response.service_account == "service_account_value"


def test_cancel_build_from_dict():
    test_cancel_build(request_type=dict)


def test_cancel_build_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_build), "__call__") as call:
        client.cancel_build()
        call.assert_called()
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.CancelBuildRequest()


@pytest.mark.asyncio
async def test_cancel_build_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.CancelBuildRequest
):
    client = CloudBuildAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.Build(
                name="name_value",
                id="id_value",
                project_id="project_id_value",
                status=cloudbuild.Build.Status.QUEUED,
                status_detail="status_detail_value",
                images=["images_value"],
                logs_bucket="logs_bucket_value",
                build_trigger_id="build_trigger_id_value",
                log_url="log_url_value",
                tags=["tags_value"],
                service_account="service_account_value",
            )
        )

        response = await client.cancel_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.CancelBuildRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.Build)

    assert response.name == "name_value"

    assert response.id == "id_value"

    assert response.project_id == "project_id_value"

    assert response.status == cloudbuild.Build.Status.QUEUED

    assert response.status_detail == "status_detail_value"

    assert response.images == ["images_value"]

    assert response.logs_bucket == "logs_bucket_value"

    assert response.build_trigger_id == "build_trigger_id_value"

    assert response.log_url == "log_url_value"

    assert response.tags == ["tags_value"]

    assert response.service_account == "service_account_value"


@pytest.mark.asyncio
async def test_cancel_build_async_from_dict():
    await test_cancel_build_async(request_type=dict)


def test_cancel_build_flattened():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.Build()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.cancel_build(
            project_id="project_id_value", id="id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].id == "id_value"


def test_cancel_build_flattened_error():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.cancel_build(
            cloudbuild.CancelBuildRequest(),
            project_id="project_id_value",
            id="id_value",
        )


@pytest.mark.asyncio
async def test_cancel_build_flattened_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.Build()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(cloudbuild.Build())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.cancel_build(
            project_id="project_id_value", id="id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].id == "id_value"


@pytest.mark.asyncio
async def test_cancel_build_flattened_error_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.cancel_build(
            cloudbuild.CancelBuildRequest(),
            project_id="project_id_value",
            id="id_value",
        )


def test_retry_build(
    transport: str = "grpc", request_type=cloudbuild.RetryBuildRequest
):
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.retry_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")

        response = client.retry_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.RetryBuildRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_retry_build_from_dict():
    test_retry_build(request_type=dict)


def test_retry_build_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.retry_build), "__call__") as call:
        client.retry_build()
        call.assert_called()
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.RetryBuildRequest()


@pytest.mark.asyncio
async def test_retry_build_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.RetryBuildRequest
):
    client = CloudBuildAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.retry_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )

        response = await client.retry_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.RetryBuildRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_retry_build_async_from_dict():
    await test_retry_build_async(request_type=dict)


def test_retry_build_flattened():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.retry_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.retry_build(
            project_id="project_id_value", id="id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].id == "id_value"


def test_retry_build_flattened_error():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.retry_build(
            cloudbuild.RetryBuildRequest(),
            project_id="project_id_value",
            id="id_value",
        )


@pytest.mark.asyncio
async def test_retry_build_flattened_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.retry_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.retry_build(
            project_id="project_id_value", id="id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].id == "id_value"


@pytest.mark.asyncio
async def test_retry_build_flattened_error_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.retry_build(
            cloudbuild.RetryBuildRequest(),
            project_id="project_id_value",
            id="id_value",
        )


def test_create_build_trigger(
    transport: str = "grpc", request_type=cloudbuild.CreateBuildTriggerRequest
):
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.BuildTrigger(
            id="id_value",
            description="description_value",
            name="name_value",
            tags=["tags_value"],
            disabled=True,
            ignored_files=["ignored_files_value"],
            included_files=["included_files_value"],
            build=cloudbuild.Build(name="name_value"),
        )

        response = client.create_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.CreateBuildTriggerRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cloudbuild.BuildTrigger)

    assert response.id == "id_value"

    assert response.description == "description_value"

    assert response.name == "name_value"

    assert response.tags == ["tags_value"]

    assert response.disabled is True

    assert response.ignored_files == ["ignored_files_value"]

    assert response.included_files == ["included_files_value"]


def test_create_build_trigger_from_dict():
    test_create_build_trigger(request_type=dict)


def test_create_build_trigger_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_build_trigger), "__call__"
    ) as call:
        client.create_build_trigger()
        call.assert_called()
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.CreateBuildTriggerRequest()


@pytest.mark.asyncio
async def test_create_build_trigger_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.CreateBuildTriggerRequest
):
    client = CloudBuildAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.BuildTrigger(
                id="id_value",
                description="description_value",
                name="name_value",
                tags=["tags_value"],
                disabled=True,
                ignored_files=["ignored_files_value"],
                included_files=["included_files_value"],
            )
        )

        response = await client.create_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.CreateBuildTriggerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.BuildTrigger)

    assert response.id == "id_value"

    assert response.description == "description_value"

    assert response.name == "name_value"

    assert response.tags == ["tags_value"]

    assert response.disabled is True

    assert response.ignored_files == ["ignored_files_value"]

    assert response.included_files == ["included_files_value"]


@pytest.mark.asyncio
async def test_create_build_trigger_async_from_dict():
    await test_create_build_trigger_async(request_type=dict)


def test_create_build_trigger_flattened():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.BuildTrigger()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_build_trigger(
            project_id="project_id_value",
            trigger=cloudbuild.BuildTrigger(id="id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].trigger == cloudbuild.BuildTrigger(id="id_value")


def test_create_build_trigger_flattened_error():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_build_trigger(
            cloudbuild.CreateBuildTriggerRequest(),
            project_id="project_id_value",
            trigger=cloudbuild.BuildTrigger(id="id_value"),
        )


@pytest.mark.asyncio
async def test_create_build_trigger_flattened_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.BuildTrigger()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.BuildTrigger()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_build_trigger(
            project_id="project_id_value",
            trigger=cloudbuild.BuildTrigger(id="id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].trigger == cloudbuild.BuildTrigger(id="id_value")


@pytest.mark.asyncio
async def test_create_build_trigger_flattened_error_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_build_trigger(
            cloudbuild.CreateBuildTriggerRequest(),
            project_id="project_id_value",
            trigger=cloudbuild.BuildTrigger(id="id_value"),
        )


def test_get_build_trigger(
    transport: str = "grpc", request_type=cloudbuild.GetBuildTriggerRequest
):
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.BuildTrigger(
            id="id_value",
            description="description_value",
            name="name_value",
            tags=["tags_value"],
            disabled=True,
            ignored_files=["ignored_files_value"],
            included_files=["included_files_value"],
            build=cloudbuild.Build(name="name_value"),
        )

        response = client.get_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.GetBuildTriggerRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cloudbuild.BuildTrigger)

    assert response.id == "id_value"

    assert response.description == "description_value"

    assert response.name == "name_value"

    assert response.tags == ["tags_value"]

    assert response.disabled is True

    assert response.ignored_files == ["ignored_files_value"]

    assert response.included_files == ["included_files_value"]


def test_get_build_trigger_from_dict():
    test_get_build_trigger(request_type=dict)


def test_get_build_trigger_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_build_trigger), "__call__"
    ) as call:
        client.get_build_trigger()
        call.assert_called()
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.GetBuildTriggerRequest()


@pytest.mark.asyncio
async def test_get_build_trigger_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.GetBuildTriggerRequest
):
    client = CloudBuildAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.BuildTrigger(
                id="id_value",
                description="description_value",
                name="name_value",
                tags=["tags_value"],
                disabled=True,
                ignored_files=["ignored_files_value"],
                included_files=["included_files_value"],
            )
        )

        response = await client.get_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.GetBuildTriggerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.BuildTrigger)

    assert response.id == "id_value"

    assert response.description == "description_value"

    assert response.name == "name_value"

    assert response.tags == ["tags_value"]

    assert response.disabled is True

    assert response.ignored_files == ["ignored_files_value"]

    assert response.included_files == ["included_files_value"]


@pytest.mark.asyncio
async def test_get_build_trigger_async_from_dict():
    await test_get_build_trigger_async(request_type=dict)


def test_get_build_trigger_flattened():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.BuildTrigger()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_build_trigger(
            project_id="project_id_value", trigger_id="trigger_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].trigger_id == "trigger_id_value"


def test_get_build_trigger_flattened_error():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_build_trigger(
            cloudbuild.GetBuildTriggerRequest(),
            project_id="project_id_value",
            trigger_id="trigger_id_value",
        )


@pytest.mark.asyncio
async def test_get_build_trigger_flattened_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.BuildTrigger()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.BuildTrigger()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_build_trigger(
            project_id="project_id_value", trigger_id="trigger_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].trigger_id == "trigger_id_value"


@pytest.mark.asyncio
async def test_get_build_trigger_flattened_error_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_build_trigger(
            cloudbuild.GetBuildTriggerRequest(),
            project_id="project_id_value",
            trigger_id="trigger_id_value",
        )


def test_list_build_triggers(
    transport: str = "grpc", request_type=cloudbuild.ListBuildTriggersRequest
):
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_build_triggers), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.ListBuildTriggersResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_build_triggers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.ListBuildTriggersRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, pagers.ListBuildTriggersPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_build_triggers_from_dict():
    test_list_build_triggers(request_type=dict)


def test_list_build_triggers_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_build_triggers), "__call__"
    ) as call:
        client.list_build_triggers()
        call.assert_called()
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.ListBuildTriggersRequest()


@pytest.mark.asyncio
async def test_list_build_triggers_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.ListBuildTriggersRequest
):
    client = CloudBuildAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_build_triggers), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.ListBuildTriggersResponse(
                next_page_token="next_page_token_value",
            )
        )

        response = await client.list_build_triggers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.ListBuildTriggersRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBuildTriggersAsyncPager)

    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_build_triggers_async_from_dict():
    await test_list_build_triggers_async(request_type=dict)


def test_list_build_triggers_flattened():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_build_triggers), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.ListBuildTriggersResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_build_triggers(project_id="project_id_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"


def test_list_build_triggers_flattened_error():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_build_triggers(
            cloudbuild.ListBuildTriggersRequest(), project_id="project_id_value",
        )


@pytest.mark.asyncio
async def test_list_build_triggers_flattened_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_build_triggers), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.ListBuildTriggersResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.ListBuildTriggersResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_build_triggers(project_id="project_id_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"


@pytest.mark.asyncio
async def test_list_build_triggers_flattened_error_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_build_triggers(
            cloudbuild.ListBuildTriggersRequest(), project_id="project_id_value",
        )


def test_list_build_triggers_pager():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_build_triggers), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListBuildTriggersResponse(
                triggers=[
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                ],
                next_page_token="abc",
            ),
            cloudbuild.ListBuildTriggersResponse(triggers=[], next_page_token="def",),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[cloudbuild.BuildTrigger(),], next_page_token="ghi",
            ),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[cloudbuild.BuildTrigger(), cloudbuild.BuildTrigger(),],
            ),
            RuntimeError,
        )

        metadata = ()
        pager = client.list_build_triggers(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, cloudbuild.BuildTrigger) for i in results)


def test_list_build_triggers_pages():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_build_triggers), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListBuildTriggersResponse(
                triggers=[
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                ],
                next_page_token="abc",
            ),
            cloudbuild.ListBuildTriggersResponse(triggers=[], next_page_token="def",),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[cloudbuild.BuildTrigger(),], next_page_token="ghi",
            ),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[cloudbuild.BuildTrigger(), cloudbuild.BuildTrigger(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_build_triggers(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_build_triggers_async_pager():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_build_triggers),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListBuildTriggersResponse(
                triggers=[
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                ],
                next_page_token="abc",
            ),
            cloudbuild.ListBuildTriggersResponse(triggers=[], next_page_token="def",),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[cloudbuild.BuildTrigger(),], next_page_token="ghi",
            ),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[cloudbuild.BuildTrigger(), cloudbuild.BuildTrigger(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_build_triggers(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, cloudbuild.BuildTrigger) for i in responses)


@pytest.mark.asyncio
async def test_list_build_triggers_async_pages():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_build_triggers),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListBuildTriggersResponse(
                triggers=[
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                ],
                next_page_token="abc",
            ),
            cloudbuild.ListBuildTriggersResponse(triggers=[], next_page_token="def",),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[cloudbuild.BuildTrigger(),], next_page_token="ghi",
            ),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[cloudbuild.BuildTrigger(), cloudbuild.BuildTrigger(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_build_triggers(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_delete_build_trigger(
    transport: str = "grpc", request_type=cloudbuild.DeleteBuildTriggerRequest
):
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.DeleteBuildTriggerRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_build_trigger_from_dict():
    test_delete_build_trigger(request_type=dict)


def test_delete_build_trigger_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_build_trigger), "__call__"
    ) as call:
        client.delete_build_trigger()
        call.assert_called()
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.DeleteBuildTriggerRequest()


@pytest.mark.asyncio
async def test_delete_build_trigger_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.DeleteBuildTriggerRequest
):
    client = CloudBuildAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.DeleteBuildTriggerRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_build_trigger_async_from_dict():
    await test_delete_build_trigger_async(request_type=dict)


def test_delete_build_trigger_flattened():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_build_trigger(
            project_id="project_id_value", trigger_id="trigger_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].trigger_id == "trigger_id_value"


def test_delete_build_trigger_flattened_error():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_build_trigger(
            cloudbuild.DeleteBuildTriggerRequest(),
            project_id="project_id_value",
            trigger_id="trigger_id_value",
        )


@pytest.mark.asyncio
async def test_delete_build_trigger_flattened_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_build_trigger(
            project_id="project_id_value", trigger_id="trigger_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].trigger_id == "trigger_id_value"


@pytest.mark.asyncio
async def test_delete_build_trigger_flattened_error_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_build_trigger(
            cloudbuild.DeleteBuildTriggerRequest(),
            project_id="project_id_value",
            trigger_id="trigger_id_value",
        )


def test_update_build_trigger(
    transport: str = "grpc", request_type=cloudbuild.UpdateBuildTriggerRequest
):
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.BuildTrigger(
            id="id_value",
            description="description_value",
            name="name_value",
            tags=["tags_value"],
            disabled=True,
            ignored_files=["ignored_files_value"],
            included_files=["included_files_value"],
            build=cloudbuild.Build(name="name_value"),
        )

        response = client.update_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.UpdateBuildTriggerRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cloudbuild.BuildTrigger)

    assert response.id == "id_value"

    assert response.description == "description_value"

    assert response.name == "name_value"

    assert response.tags == ["tags_value"]

    assert response.disabled is True

    assert response.ignored_files == ["ignored_files_value"]

    assert response.included_files == ["included_files_value"]


def test_update_build_trigger_from_dict():
    test_update_build_trigger(request_type=dict)


def test_update_build_trigger_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_build_trigger), "__call__"
    ) as call:
        client.update_build_trigger()
        call.assert_called()
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.UpdateBuildTriggerRequest()


@pytest.mark.asyncio
async def test_update_build_trigger_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.UpdateBuildTriggerRequest
):
    client = CloudBuildAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.BuildTrigger(
                id="id_value",
                description="description_value",
                name="name_value",
                tags=["tags_value"],
                disabled=True,
                ignored_files=["ignored_files_value"],
                included_files=["included_files_value"],
            )
        )

        response = await client.update_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.UpdateBuildTriggerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.BuildTrigger)

    assert response.id == "id_value"

    assert response.description == "description_value"

    assert response.name == "name_value"

    assert response.tags == ["tags_value"]

    assert response.disabled is True

    assert response.ignored_files == ["ignored_files_value"]

    assert response.included_files == ["included_files_value"]


@pytest.mark.asyncio
async def test_update_build_trigger_async_from_dict():
    await test_update_build_trigger_async(request_type=dict)


def test_update_build_trigger_flattened():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.BuildTrigger()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_build_trigger(
            project_id="project_id_value",
            trigger_id="trigger_id_value",
            trigger=cloudbuild.BuildTrigger(id="id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].trigger_id == "trigger_id_value"

        assert args[0].trigger == cloudbuild.BuildTrigger(id="id_value")


def test_update_build_trigger_flattened_error():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_build_trigger(
            cloudbuild.UpdateBuildTriggerRequest(),
            project_id="project_id_value",
            trigger_id="trigger_id_value",
            trigger=cloudbuild.BuildTrigger(id="id_value"),
        )


@pytest.mark.asyncio
async def test_update_build_trigger_flattened_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.BuildTrigger()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.BuildTrigger()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_build_trigger(
            project_id="project_id_value",
            trigger_id="trigger_id_value",
            trigger=cloudbuild.BuildTrigger(id="id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].trigger_id == "trigger_id_value"

        assert args[0].trigger == cloudbuild.BuildTrigger(id="id_value")


@pytest.mark.asyncio
async def test_update_build_trigger_flattened_error_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_build_trigger(
            cloudbuild.UpdateBuildTriggerRequest(),
            project_id="project_id_value",
            trigger_id="trigger_id_value",
            trigger=cloudbuild.BuildTrigger(id="id_value"),
        )


def test_run_build_trigger(
    transport: str = "grpc", request_type=cloudbuild.RunBuildTriggerRequest
):
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")

        response = client.run_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.RunBuildTriggerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_run_build_trigger_from_dict():
    test_run_build_trigger(request_type=dict)


def test_run_build_trigger_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_build_trigger), "__call__"
    ) as call:
        client.run_build_trigger()
        call.assert_called()
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.RunBuildTriggerRequest()


@pytest.mark.asyncio
async def test_run_build_trigger_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.RunBuildTriggerRequest
):
    client = CloudBuildAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )

        response = await client.run_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.RunBuildTriggerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_run_build_trigger_async_from_dict():
    await test_run_build_trigger_async(request_type=dict)


def test_run_build_trigger_flattened():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.run_build_trigger(
            project_id="project_id_value",
            trigger_id="trigger_id_value",
            source=cloudbuild.RepoSource(project_id="project_id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].trigger_id == "trigger_id_value"

        assert args[0].source == cloudbuild.RepoSource(project_id="project_id_value")


def test_run_build_trigger_flattened_error():
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.run_build_trigger(
            cloudbuild.RunBuildTriggerRequest(),
            project_id="project_id_value",
            trigger_id="trigger_id_value",
            source=cloudbuild.RepoSource(project_id="project_id_value"),
        )


@pytest.mark.asyncio
async def test_run_build_trigger_flattened_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.run_build_trigger(
            project_id="project_id_value",
            trigger_id="trigger_id_value",
            source=cloudbuild.RepoSource(project_id="project_id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].trigger_id == "trigger_id_value"

        assert args[0].source == cloudbuild.RepoSource(project_id="project_id_value")


@pytest.mark.asyncio
async def test_run_build_trigger_flattened_error_async():
    client = CloudBuildAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.run_build_trigger(
            cloudbuild.RunBuildTriggerRequest(),
            project_id="project_id_value",
            trigger_id="trigger_id_value",
            source=cloudbuild.RepoSource(project_id="project_id_value"),
        )


def test_receive_trigger_webhook(
    transport: str = "grpc", request_type=cloudbuild.ReceiveTriggerWebhookRequest
):
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.receive_trigger_webhook), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.ReceiveTriggerWebhookResponse()

        response = client.receive_trigger_webhook(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.ReceiveTriggerWebhookRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cloudbuild.ReceiveTriggerWebhookResponse)


def test_receive_trigger_webhook_from_dict():
    test_receive_trigger_webhook(request_type=dict)


def test_receive_trigger_webhook_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.receive_trigger_webhook), "__call__"
    ) as call:
        client.receive_trigger_webhook()
        call.assert_called()
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.ReceiveTriggerWebhookRequest()


@pytest.mark.asyncio
async def test_receive_trigger_webhook_async(
    transport: str = "grpc_asyncio",
    request_type=cloudbuild.ReceiveTriggerWebhookRequest,
):
    client = CloudBuildAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.receive_trigger_webhook), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.ReceiveTriggerWebhookResponse()
        )

        response = await client.receive_trigger_webhook(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.ReceiveTriggerWebhookRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.ReceiveTriggerWebhookResponse)


@pytest.mark.asyncio
async def test_receive_trigger_webhook_async_from_dict():
    await test_receive_trigger_webhook_async(request_type=dict)


def test_create_worker_pool(
    transport: str = "grpc", request_type=cloudbuild.CreateWorkerPoolRequest
):
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.WorkerPool(
            name="name_value",
            project_id="project_id_value",
            service_account_email="service_account_email_value",
            worker_count=1314,
            regions=[cloudbuild.WorkerPool.Region.US_CENTRAL1],
            status=cloudbuild.WorkerPool.Status.CREATING,
        )

        response = client.create_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.CreateWorkerPoolRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cloudbuild.WorkerPool)

    assert response.name == "name_value"

    assert response.project_id == "project_id_value"

    assert response.service_account_email == "service_account_email_value"

    assert response.worker_count == 1314

    assert response.regions == [cloudbuild.WorkerPool.Region.US_CENTRAL1]

    assert response.status == cloudbuild.WorkerPool.Status.CREATING


def test_create_worker_pool_from_dict():
    test_create_worker_pool(request_type=dict)


def test_create_worker_pool_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_worker_pool), "__call__"
    ) as call:
        client.create_worker_pool()
        call.assert_called()
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.CreateWorkerPoolRequest()


@pytest.mark.asyncio
async def test_create_worker_pool_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.CreateWorkerPoolRequest
):
    client = CloudBuildAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.WorkerPool(
                name="name_value",
                project_id="project_id_value",
                service_account_email="service_account_email_value",
                worker_count=1314,
                regions=[cloudbuild.WorkerPool.Region.US_CENTRAL1],
                status=cloudbuild.WorkerPool.Status.CREATING,
            )
        )

        response = await client.create_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.CreateWorkerPoolRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.WorkerPool)

    assert response.name == "name_value"

    assert response.project_id == "project_id_value"

    assert response.service_account_email == "service_account_email_value"

    assert response.worker_count == 1314

    assert response.regions == [cloudbuild.WorkerPool.Region.US_CENTRAL1]

    assert response.status == cloudbuild.WorkerPool.Status.CREATING


@pytest.mark.asyncio
async def test_create_worker_pool_async_from_dict():
    await test_create_worker_pool_async(request_type=dict)


def test_get_worker_pool(
    transport: str = "grpc", request_type=cloudbuild.GetWorkerPoolRequest
):
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_worker_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.WorkerPool(
            name="name_value",
            project_id="project_id_value",
            service_account_email="service_account_email_value",
            worker_count=1314,
            regions=[cloudbuild.WorkerPool.Region.US_CENTRAL1],
            status=cloudbuild.WorkerPool.Status.CREATING,
        )

        response = client.get_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.GetWorkerPoolRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cloudbuild.WorkerPool)

    assert response.name == "name_value"

    assert response.project_id == "project_id_value"

    assert response.service_account_email == "service_account_email_value"

    assert response.worker_count == 1314

    assert response.regions == [cloudbuild.WorkerPool.Region.US_CENTRAL1]

    assert response.status == cloudbuild.WorkerPool.Status.CREATING


def test_get_worker_pool_from_dict():
    test_get_worker_pool(request_type=dict)


def test_get_worker_pool_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_worker_pool), "__call__") as call:
        client.get_worker_pool()
        call.assert_called()
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.GetWorkerPoolRequest()


@pytest.mark.asyncio
async def test_get_worker_pool_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.GetWorkerPoolRequest
):
    client = CloudBuildAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_worker_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.WorkerPool(
                name="name_value",
                project_id="project_id_value",
                service_account_email="service_account_email_value",
                worker_count=1314,
                regions=[cloudbuild.WorkerPool.Region.US_CENTRAL1],
                status=cloudbuild.WorkerPool.Status.CREATING,
            )
        )

        response = await client.get_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.GetWorkerPoolRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.WorkerPool)

    assert response.name == "name_value"

    assert response.project_id == "project_id_value"

    assert response.service_account_email == "service_account_email_value"

    assert response.worker_count == 1314

    assert response.regions == [cloudbuild.WorkerPool.Region.US_CENTRAL1]

    assert response.status == cloudbuild.WorkerPool.Status.CREATING


@pytest.mark.asyncio
async def test_get_worker_pool_async_from_dict():
    await test_get_worker_pool_async(request_type=dict)


def test_delete_worker_pool(
    transport: str = "grpc", request_type=cloudbuild.DeleteWorkerPoolRequest
):
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.DeleteWorkerPoolRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_worker_pool_from_dict():
    test_delete_worker_pool(request_type=dict)


def test_delete_worker_pool_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_worker_pool), "__call__"
    ) as call:
        client.delete_worker_pool()
        call.assert_called()
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.DeleteWorkerPoolRequest()


@pytest.mark.asyncio
async def test_delete_worker_pool_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.DeleteWorkerPoolRequest
):
    client = CloudBuildAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.DeleteWorkerPoolRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_worker_pool_async_from_dict():
    await test_delete_worker_pool_async(request_type=dict)


def test_update_worker_pool(
    transport: str = "grpc", request_type=cloudbuild.UpdateWorkerPoolRequest
):
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.WorkerPool(
            name="name_value",
            project_id="project_id_value",
            service_account_email="service_account_email_value",
            worker_count=1314,
            regions=[cloudbuild.WorkerPool.Region.US_CENTRAL1],
            status=cloudbuild.WorkerPool.Status.CREATING,
        )

        response = client.update_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.UpdateWorkerPoolRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cloudbuild.WorkerPool)

    assert response.name == "name_value"

    assert response.project_id == "project_id_value"

    assert response.service_account_email == "service_account_email_value"

    assert response.worker_count == 1314

    assert response.regions == [cloudbuild.WorkerPool.Region.US_CENTRAL1]

    assert response.status == cloudbuild.WorkerPool.Status.CREATING


def test_update_worker_pool_from_dict():
    test_update_worker_pool(request_type=dict)


def test_update_worker_pool_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_worker_pool), "__call__"
    ) as call:
        client.update_worker_pool()
        call.assert_called()
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.UpdateWorkerPoolRequest()


@pytest.mark.asyncio
async def test_update_worker_pool_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.UpdateWorkerPoolRequest
):
    client = CloudBuildAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.WorkerPool(
                name="name_value",
                project_id="project_id_value",
                service_account_email="service_account_email_value",
                worker_count=1314,
                regions=[cloudbuild.WorkerPool.Region.US_CENTRAL1],
                status=cloudbuild.WorkerPool.Status.CREATING,
            )
        )

        response = await client.update_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.UpdateWorkerPoolRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.WorkerPool)

    assert response.name == "name_value"

    assert response.project_id == "project_id_value"

    assert response.service_account_email == "service_account_email_value"

    assert response.worker_count == 1314

    assert response.regions == [cloudbuild.WorkerPool.Region.US_CENTRAL1]

    assert response.status == cloudbuild.WorkerPool.Status.CREATING


@pytest.mark.asyncio
async def test_update_worker_pool_async_from_dict():
    await test_update_worker_pool_async(request_type=dict)


def test_list_worker_pools(
    transport: str = "grpc", request_type=cloudbuild.ListWorkerPoolsRequest
):
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_worker_pools), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.ListWorkerPoolsResponse()

        response = client.list_worker_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.ListWorkerPoolsRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, cloudbuild.ListWorkerPoolsResponse)


def test_list_worker_pools_from_dict():
    test_list_worker_pools(request_type=dict)


def test_list_worker_pools_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_worker_pools), "__call__"
    ) as call:
        client.list_worker_pools()
        call.assert_called()
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.ListWorkerPoolsRequest()


@pytest.mark.asyncio
async def test_list_worker_pools_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.ListWorkerPoolsRequest
):
    client = CloudBuildAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_worker_pools), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.ListWorkerPoolsResponse()
        )

        response = await client.list_worker_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudbuild.ListWorkerPoolsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.ListWorkerPoolsResponse)


@pytest.mark.asyncio
async def test_list_worker_pools_async_from_dict():
    await test_list_worker_pools_async(request_type=dict)


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.CloudBuildGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CloudBuildClient(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.CloudBuildGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CloudBuildClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.CloudBuildGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CloudBuildClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.CloudBuildGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = CloudBuildClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.CloudBuildGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.CloudBuildGrpcAsyncIOTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [transports.CloudBuildGrpcTransport, transports.CloudBuildGrpcAsyncIOTransport,],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = CloudBuildClient(credentials=credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.CloudBuildGrpcTransport,)


def test_cloud_build_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.CloudBuildTransport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_cloud_build_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.devtools.cloudbuild_v1.services.cloud_build.transports.CloudBuildTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.CloudBuildTransport(
            credentials=credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_build",
        "get_build",
        "list_builds",
        "cancel_build",
        "retry_build",
        "create_build_trigger",
        "get_build_trigger",
        "list_build_triggers",
        "delete_build_trigger",
        "update_build_trigger",
        "run_build_trigger",
        "receive_trigger_webhook",
        "create_worker_pool",
        "get_worker_pool",
        "delete_worker_pool",
        "update_worker_pool",
        "list_worker_pools",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client


def test_cloud_build_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        auth, "load_credentials_from_file"
    ) as load_creds, mock.patch(
        "google.cloud.devtools.cloudbuild_v1.services.cloud_build.transports.CloudBuildTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.CloudBuildTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_cloud_build_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(auth, "default") as adc, mock.patch(
        "google.cloud.devtools.cloudbuild_v1.services.cloud_build.transports.CloudBuildTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.CloudBuildTransport()
        adc.assert_called_once()


def test_cloud_build_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        CloudBuildClient()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


def test_cloud_build_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.CloudBuildGrpcTransport(
            host="squid.clam.whelk", quota_project_id="octopus"
        )
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.CloudBuildGrpcTransport, transports.CloudBuildGrpcAsyncIOTransport],
)
def test_cloud_build_grpc_transport_client_cert_source_for_mtls(transport_class):
    cred = credentials.AnonymousCredentials()

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
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
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


def test_cloud_build_host_no_port():
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="cloudbuild.googleapis.com"
        ),
    )
    assert client.transport._host == "cloudbuild.googleapis.com:443"


def test_cloud_build_host_with_port():
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="cloudbuild.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "cloudbuild.googleapis.com:8000"


def test_cloud_build_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.CloudBuildGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_cloud_build_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.CloudBuildGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [transports.CloudBuildGrpcTransport, transports.CloudBuildGrpcAsyncIOTransport],
)
def test_cloud_build_transport_channel_mtls_with_client_cert_source(transport_class):
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

            cred = credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(auth, "default") as adc:
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
                scopes=("https://www.googleapis.com/auth/cloud-platform",),
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
    [transports.CloudBuildGrpcTransport, transports.CloudBuildGrpcAsyncIOTransport],
)
def test_cloud_build_transport_channel_mtls_with_adc(transport_class):
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
                scopes=("https://www.googleapis.com/auth/cloud-platform",),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_cloud_build_grpc_lro_client():
    client = CloudBuildClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_cloud_build_grpc_lro_async_client():
    client = CloudBuildAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc_asyncio",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsAsyncClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_build_path():
    project = "squid"
    build = "clam"

    expected = "projects/{project}/builds/{build}".format(project=project, build=build,)
    actual = CloudBuildClient.build_path(project, build)
    assert expected == actual


def test_parse_build_path():
    expected = {
        "project": "whelk",
        "build": "octopus",
    }
    path = CloudBuildClient.build_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_build_path(path)
    assert expected == actual


def test_build_trigger_path():
    project = "oyster"
    trigger = "nudibranch"

    expected = "projects/{project}/triggers/{trigger}".format(
        project=project, trigger=trigger,
    )
    actual = CloudBuildClient.build_trigger_path(project, trigger)
    assert expected == actual


def test_parse_build_trigger_path():
    expected = {
        "project": "cuttlefish",
        "trigger": "mussel",
    }
    path = CloudBuildClient.build_trigger_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_build_trigger_path(path)
    assert expected == actual


def test_crypto_key_path():
    project = "winkle"
    location = "nautilus"
    keyring = "scallop"
    key = "abalone"

    expected = "projects/{project}/locations/{location}/keyRings/{keyring}/cryptoKeys/{key}".format(
        project=project, location=location, keyring=keyring, key=key,
    )
    actual = CloudBuildClient.crypto_key_path(project, location, keyring, key)
    assert expected == actual


def test_parse_crypto_key_path():
    expected = {
        "project": "squid",
        "location": "clam",
        "keyring": "whelk",
        "key": "octopus",
    }
    path = CloudBuildClient.crypto_key_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_crypto_key_path(path)
    assert expected == actual


def test_secret_version_path():
    project = "oyster"
    secret = "nudibranch"
    version = "cuttlefish"

    expected = "projects/{project}/secrets/{secret}/versions/{version}".format(
        project=project, secret=secret, version=version,
    )
    actual = CloudBuildClient.secret_version_path(project, secret, version)
    assert expected == actual


def test_parse_secret_version_path():
    expected = {
        "project": "mussel",
        "secret": "winkle",
        "version": "nautilus",
    }
    path = CloudBuildClient.secret_version_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_secret_version_path(path)
    assert expected == actual


def test_service_account_path():
    project = "scallop"
    service_account = "abalone"

    expected = "projects/{project}/serviceAccounts/{service_account}".format(
        project=project, service_account=service_account,
    )
    actual = CloudBuildClient.service_account_path(project, service_account)
    assert expected == actual


def test_parse_service_account_path():
    expected = {
        "project": "squid",
        "service_account": "clam",
    }
    path = CloudBuildClient.service_account_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_service_account_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "whelk"

    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = CloudBuildClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "octopus",
    }
    path = CloudBuildClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "oyster"

    expected = "folders/{folder}".format(folder=folder,)
    actual = CloudBuildClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nudibranch",
    }
    path = CloudBuildClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "cuttlefish"

    expected = "organizations/{organization}".format(organization=organization,)
    actual = CloudBuildClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "mussel",
    }
    path = CloudBuildClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "winkle"

    expected = "projects/{project}".format(project=project,)
    actual = CloudBuildClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nautilus",
    }
    path = CloudBuildClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "scallop"
    location = "abalone"

    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = CloudBuildClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "squid",
        "location": "clam",
    }
    path = CloudBuildClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.CloudBuildTransport, "_prep_wrapped_messages"
    ) as prep:
        client = CloudBuildClient(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.CloudBuildTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = CloudBuildClient.get_transport_class()
        transport = transport_class(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
