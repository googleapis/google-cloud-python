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
from google.api_core import client_options
from google.api_core import exceptions
from google.api_core import future
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.api_core import operation_async
from google.api_core import operations_v1
from google.auth import credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.dataproc_v1beta2.services.job_controller import (
    JobControllerAsyncClient,
)
from google.cloud.dataproc_v1beta2.services.job_controller import JobControllerClient
from google.cloud.dataproc_v1beta2.services.job_controller import pagers
from google.cloud.dataproc_v1beta2.services.job_controller import transports
from google.cloud.dataproc_v1beta2.types import jobs
from google.cloud.dataproc_v1beta2.types import jobs as gcd_jobs
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
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

    assert JobControllerClient._get_default_mtls_endpoint(None) is None
    assert (
        JobControllerClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        JobControllerClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        JobControllerClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        JobControllerClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        JobControllerClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class", [JobControllerClient, JobControllerAsyncClient]
)
def test_job_controller_client_from_service_account_file(client_class):
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client._transport._credentials == creds

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client._transport._credentials == creds

        assert client._transport._host == "dataproc.googleapis.com:443"


def test_job_controller_client_get_transport_class():
    transport = JobControllerClient.get_transport_class()
    assert transport == transports.JobControllerGrpcTransport

    transport = JobControllerClient.get_transport_class("grpc")
    assert transport == transports.JobControllerGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (JobControllerClient, transports.JobControllerGrpcTransport, "grpc"),
        (
            JobControllerAsyncClient,
            transports.JobControllerGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    JobControllerClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(JobControllerClient),
)
@mock.patch.object(
    JobControllerAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(JobControllerAsyncClient),
)
def test_job_controller_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(JobControllerClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(JobControllerClient, "get_transport_class") as gtc:
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
            api_mtls_endpoint="squid.clam.whelk",
            client_cert_source=None,
            quota_project_id=None,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                api_mtls_endpoint=client.DEFAULT_ENDPOINT,
                client_cert_source=None,
                quota_project_id=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                api_mtls_endpoint=client.DEFAULT_MTLS_ENDPOINT,
                client_cert_source=None,
                quota_project_id=None,
            )

    # Check the case api_endpoint is not provided, GOOGLE_API_USE_MTLS is
    # "auto", and client_cert_source is provided.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "auto"}):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                api_mtls_endpoint=client.DEFAULT_MTLS_ENDPOINT,
                client_cert_source=client_cert_source_callback,
                quota_project_id=None,
            )

    # Check the case api_endpoint is not provided, GOOGLE_API_USE_MTLS is
    # "auto", and default_client_cert_source is provided.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "auto"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                patched.return_value = None
                client = client_class()
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_MTLS_ENDPOINT,
                    scopes=None,
                    api_mtls_endpoint=client.DEFAULT_MTLS_ENDPOINT,
                    client_cert_source=None,
                    quota_project_id=None,
                )

    # Check the case api_endpoint is not provided, GOOGLE_API_USE_MTLS is
    # "auto", but client_cert_source and default_client_cert_source are None.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "auto"}):
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
                    api_mtls_endpoint=client.DEFAULT_ENDPOINT,
                    client_cert_source=None,
                    quota_project_id=None,
                )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
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
            api_mtls_endpoint=client.DEFAULT_ENDPOINT,
            client_cert_source=None,
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (JobControllerClient, transports.JobControllerGrpcTransport, "grpc"),
        (
            JobControllerAsyncClient,
            transports.JobControllerGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_job_controller_client_client_options_scopes(
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
            api_mtls_endpoint=client.DEFAULT_ENDPOINT,
            client_cert_source=None,
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (JobControllerClient, transports.JobControllerGrpcTransport, "grpc"),
        (
            JobControllerAsyncClient,
            transports.JobControllerGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_job_controller_client_client_options_credentials_file(
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
            api_mtls_endpoint=client.DEFAULT_ENDPOINT,
            client_cert_source=None,
            quota_project_id=None,
        )


def test_job_controller_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.dataproc_v1beta2.services.job_controller.transports.JobControllerGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = JobControllerClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            api_mtls_endpoint="squid.clam.whelk",
            client_cert_source=None,
            quota_project_id=None,
        )


def test_submit_job(transport: str = "grpc", request_type=jobs.SubmitJobRequest):
    client = JobControllerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.submit_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = jobs.Job(
            submitted_by="submitted_by_value",
            driver_output_resource_uri="driver_output_resource_uri_value",
            driver_control_files_uri="driver_control_files_uri_value",
            job_uuid="job_uuid_value",
            done=True,
            hadoop_job=jobs.HadoopJob(main_jar_file_uri="main_jar_file_uri_value"),
        )

        response = client.submit_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == jobs.SubmitJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, jobs.Job)

    assert response.submitted_by == "submitted_by_value"

    assert response.driver_output_resource_uri == "driver_output_resource_uri_value"

    assert response.driver_control_files_uri == "driver_control_files_uri_value"

    assert response.job_uuid == "job_uuid_value"

    assert response.done is True


def test_submit_job_from_dict():
    test_submit_job(request_type=dict)


@pytest.mark.asyncio
async def test_submit_job_async(transport: str = "grpc_asyncio"):
    client = JobControllerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = jobs.SubmitJobRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.submit_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            jobs.Job(
                submitted_by="submitted_by_value",
                driver_output_resource_uri="driver_output_resource_uri_value",
                driver_control_files_uri="driver_control_files_uri_value",
                job_uuid="job_uuid_value",
                done=True,
            )
        )

        response = await client.submit_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, jobs.Job)

    assert response.submitted_by == "submitted_by_value"

    assert response.driver_output_resource_uri == "driver_output_resource_uri_value"

    assert response.driver_control_files_uri == "driver_control_files_uri_value"

    assert response.job_uuid == "job_uuid_value"

    assert response.done is True


def test_submit_job_flattened():
    client = JobControllerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.submit_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = jobs.Job()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.submit_job(
            project_id="project_id_value",
            region="region_value",
            job=jobs.Job(reference=jobs.JobReference(project_id="project_id_value")),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].region == "region_value"

        assert args[0].job == jobs.Job(
            reference=jobs.JobReference(project_id="project_id_value")
        )


def test_submit_job_flattened_error():
    client = JobControllerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.submit_job(
            jobs.SubmitJobRequest(),
            project_id="project_id_value",
            region="region_value",
            job=jobs.Job(reference=jobs.JobReference(project_id="project_id_value")),
        )


@pytest.mark.asyncio
async def test_submit_job_flattened_async():
    client = JobControllerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.submit_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = jobs.Job()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(jobs.Job())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.submit_job(
            project_id="project_id_value",
            region="region_value",
            job=jobs.Job(reference=jobs.JobReference(project_id="project_id_value")),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].region == "region_value"

        assert args[0].job == jobs.Job(
            reference=jobs.JobReference(project_id="project_id_value")
        )


@pytest.mark.asyncio
async def test_submit_job_flattened_error_async():
    client = JobControllerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.submit_job(
            jobs.SubmitJobRequest(),
            project_id="project_id_value",
            region="region_value",
            job=jobs.Job(reference=jobs.JobReference(project_id="project_id_value")),
        )


def test_submit_job_as_operation(
    transport: str = "grpc", request_type=jobs.SubmitJobRequest
):
    client = JobControllerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.submit_job_as_operation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")

        response = client.submit_job_as_operation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == jobs.SubmitJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_submit_job_as_operation_from_dict():
    test_submit_job_as_operation(request_type=dict)


@pytest.mark.asyncio
async def test_submit_job_as_operation_async(transport: str = "grpc_asyncio"):
    client = JobControllerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = jobs.SubmitJobRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.submit_job_as_operation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )

        response = await client.submit_job_as_operation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_submit_job_as_operation_flattened():
    client = JobControllerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.submit_job_as_operation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.submit_job_as_operation(
            project_id="project_id_value",
            region="region_value",
            job=jobs.Job(reference=jobs.JobReference(project_id="project_id_value")),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].region == "region_value"

        assert args[0].job == jobs.Job(
            reference=jobs.JobReference(project_id="project_id_value")
        )


def test_submit_job_as_operation_flattened_error():
    client = JobControllerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.submit_job_as_operation(
            jobs.SubmitJobRequest(),
            project_id="project_id_value",
            region="region_value",
            job=jobs.Job(reference=jobs.JobReference(project_id="project_id_value")),
        )


@pytest.mark.asyncio
async def test_submit_job_as_operation_flattened_async():
    client = JobControllerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.submit_job_as_operation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.submit_job_as_operation(
            project_id="project_id_value",
            region="region_value",
            job=jobs.Job(reference=jobs.JobReference(project_id="project_id_value")),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].region == "region_value"

        assert args[0].job == jobs.Job(
            reference=jobs.JobReference(project_id="project_id_value")
        )


@pytest.mark.asyncio
async def test_submit_job_as_operation_flattened_error_async():
    client = JobControllerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.submit_job_as_operation(
            jobs.SubmitJobRequest(),
            project_id="project_id_value",
            region="region_value",
            job=jobs.Job(reference=jobs.JobReference(project_id="project_id_value")),
        )


def test_get_job(transport: str = "grpc", request_type=jobs.GetJobRequest):
    client = JobControllerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = jobs.Job(
            submitted_by="submitted_by_value",
            driver_output_resource_uri="driver_output_resource_uri_value",
            driver_control_files_uri="driver_control_files_uri_value",
            job_uuid="job_uuid_value",
            done=True,
            hadoop_job=jobs.HadoopJob(main_jar_file_uri="main_jar_file_uri_value"),
        )

        response = client.get_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == jobs.GetJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, jobs.Job)

    assert response.submitted_by == "submitted_by_value"

    assert response.driver_output_resource_uri == "driver_output_resource_uri_value"

    assert response.driver_control_files_uri == "driver_control_files_uri_value"

    assert response.job_uuid == "job_uuid_value"

    assert response.done is True


def test_get_job_from_dict():
    test_get_job(request_type=dict)


@pytest.mark.asyncio
async def test_get_job_async(transport: str = "grpc_asyncio"):
    client = JobControllerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = jobs.GetJobRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._client._transport.get_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            jobs.Job(
                submitted_by="submitted_by_value",
                driver_output_resource_uri="driver_output_resource_uri_value",
                driver_control_files_uri="driver_control_files_uri_value",
                job_uuid="job_uuid_value",
                done=True,
            )
        )

        response = await client.get_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, jobs.Job)

    assert response.submitted_by == "submitted_by_value"

    assert response.driver_output_resource_uri == "driver_output_resource_uri_value"

    assert response.driver_control_files_uri == "driver_control_files_uri_value"

    assert response.job_uuid == "job_uuid_value"

    assert response.done is True


def test_get_job_flattened():
    client = JobControllerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = jobs.Job()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_job(
            project_id="project_id_value", region="region_value", job_id="job_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].region == "region_value"

        assert args[0].job_id == "job_id_value"


def test_get_job_flattened_error():
    client = JobControllerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_job(
            jobs.GetJobRequest(),
            project_id="project_id_value",
            region="region_value",
            job_id="job_id_value",
        )


@pytest.mark.asyncio
async def test_get_job_flattened_async():
    client = JobControllerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._client._transport.get_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = jobs.Job()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(jobs.Job())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_job(
            project_id="project_id_value", region="region_value", job_id="job_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].region == "region_value"

        assert args[0].job_id == "job_id_value"


@pytest.mark.asyncio
async def test_get_job_flattened_error_async():
    client = JobControllerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_job(
            jobs.GetJobRequest(),
            project_id="project_id_value",
            region="region_value",
            job_id="job_id_value",
        )


def test_list_jobs(transport: str = "grpc", request_type=jobs.ListJobsRequest):
    client = JobControllerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_jobs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = jobs.ListJobsResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == jobs.ListJobsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListJobsPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_jobs_from_dict():
    test_list_jobs(request_type=dict)


@pytest.mark.asyncio
async def test_list_jobs_async(transport: str = "grpc_asyncio"):
    client = JobControllerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = jobs.ListJobsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_jobs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            jobs.ListJobsResponse(next_page_token="next_page_token_value",)
        )

        response = await client.list_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListJobsAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_jobs_flattened():
    client = JobControllerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_jobs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = jobs.ListJobsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_jobs(
            project_id="project_id_value", region="region_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].region == "region_value"

        assert args[0].filter == "filter_value"


def test_list_jobs_flattened_error():
    client = JobControllerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_jobs(
            jobs.ListJobsRequest(),
            project_id="project_id_value",
            region="region_value",
            filter="filter_value",
        )


@pytest.mark.asyncio
async def test_list_jobs_flattened_async():
    client = JobControllerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_jobs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = jobs.ListJobsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            jobs.ListJobsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_jobs(
            project_id="project_id_value", region="region_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].region == "region_value"

        assert args[0].filter == "filter_value"


@pytest.mark.asyncio
async def test_list_jobs_flattened_error_async():
    client = JobControllerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_jobs(
            jobs.ListJobsRequest(),
            project_id="project_id_value",
            region="region_value",
            filter="filter_value",
        )


def test_list_jobs_pager():
    client = JobControllerClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_jobs), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            jobs.ListJobsResponse(
                jobs=[jobs.Job(), jobs.Job(), jobs.Job(),], next_page_token="abc",
            ),
            jobs.ListJobsResponse(jobs=[], next_page_token="def",),
            jobs.ListJobsResponse(jobs=[jobs.Job(),], next_page_token="ghi",),
            jobs.ListJobsResponse(jobs=[jobs.Job(), jobs.Job(),],),
            RuntimeError,
        )

        metadata = ()
        pager = client.list_jobs(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, jobs.Job) for i in results)


def test_list_jobs_pages():
    client = JobControllerClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_jobs), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            jobs.ListJobsResponse(
                jobs=[jobs.Job(), jobs.Job(), jobs.Job(),], next_page_token="abc",
            ),
            jobs.ListJobsResponse(jobs=[], next_page_token="def",),
            jobs.ListJobsResponse(jobs=[jobs.Job(),], next_page_token="ghi",),
            jobs.ListJobsResponse(jobs=[jobs.Job(), jobs.Job(),],),
            RuntimeError,
        )
        pages = list(client.list_jobs(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_jobs_async_pager():
    client = JobControllerAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_jobs),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            jobs.ListJobsResponse(
                jobs=[jobs.Job(), jobs.Job(), jobs.Job(),], next_page_token="abc",
            ),
            jobs.ListJobsResponse(jobs=[], next_page_token="def",),
            jobs.ListJobsResponse(jobs=[jobs.Job(),], next_page_token="ghi",),
            jobs.ListJobsResponse(jobs=[jobs.Job(), jobs.Job(),],),
            RuntimeError,
        )
        async_pager = await client.list_jobs(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, jobs.Job) for i in responses)


@pytest.mark.asyncio
async def test_list_jobs_async_pages():
    client = JobControllerAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_jobs),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            jobs.ListJobsResponse(
                jobs=[jobs.Job(), jobs.Job(), jobs.Job(),], next_page_token="abc",
            ),
            jobs.ListJobsResponse(jobs=[], next_page_token="def",),
            jobs.ListJobsResponse(jobs=[jobs.Job(),], next_page_token="ghi",),
            jobs.ListJobsResponse(jobs=[jobs.Job(), jobs.Job(),],),
            RuntimeError,
        )
        pages = []
        async for page in (await client.list_jobs(request={})).pages:
            pages.append(page)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_update_job(transport: str = "grpc", request_type=jobs.UpdateJobRequest):
    client = JobControllerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = jobs.Job(
            submitted_by="submitted_by_value",
            driver_output_resource_uri="driver_output_resource_uri_value",
            driver_control_files_uri="driver_control_files_uri_value",
            job_uuid="job_uuid_value",
            done=True,
            hadoop_job=jobs.HadoopJob(main_jar_file_uri="main_jar_file_uri_value"),
        )

        response = client.update_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == jobs.UpdateJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, jobs.Job)

    assert response.submitted_by == "submitted_by_value"

    assert response.driver_output_resource_uri == "driver_output_resource_uri_value"

    assert response.driver_control_files_uri == "driver_control_files_uri_value"

    assert response.job_uuid == "job_uuid_value"

    assert response.done is True


def test_update_job_from_dict():
    test_update_job(request_type=dict)


@pytest.mark.asyncio
async def test_update_job_async(transport: str = "grpc_asyncio"):
    client = JobControllerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = jobs.UpdateJobRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            jobs.Job(
                submitted_by="submitted_by_value",
                driver_output_resource_uri="driver_output_resource_uri_value",
                driver_control_files_uri="driver_control_files_uri_value",
                job_uuid="job_uuid_value",
                done=True,
            )
        )

        response = await client.update_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, jobs.Job)

    assert response.submitted_by == "submitted_by_value"

    assert response.driver_output_resource_uri == "driver_output_resource_uri_value"

    assert response.driver_control_files_uri == "driver_control_files_uri_value"

    assert response.job_uuid == "job_uuid_value"

    assert response.done is True


def test_cancel_job(transport: str = "grpc", request_type=jobs.CancelJobRequest):
    client = JobControllerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.cancel_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = jobs.Job(
            submitted_by="submitted_by_value",
            driver_output_resource_uri="driver_output_resource_uri_value",
            driver_control_files_uri="driver_control_files_uri_value",
            job_uuid="job_uuid_value",
            done=True,
            hadoop_job=jobs.HadoopJob(main_jar_file_uri="main_jar_file_uri_value"),
        )

        response = client.cancel_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == jobs.CancelJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, jobs.Job)

    assert response.submitted_by == "submitted_by_value"

    assert response.driver_output_resource_uri == "driver_output_resource_uri_value"

    assert response.driver_control_files_uri == "driver_control_files_uri_value"

    assert response.job_uuid == "job_uuid_value"

    assert response.done is True


def test_cancel_job_from_dict():
    test_cancel_job(request_type=dict)


@pytest.mark.asyncio
async def test_cancel_job_async(transport: str = "grpc_asyncio"):
    client = JobControllerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = jobs.CancelJobRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.cancel_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            jobs.Job(
                submitted_by="submitted_by_value",
                driver_output_resource_uri="driver_output_resource_uri_value",
                driver_control_files_uri="driver_control_files_uri_value",
                job_uuid="job_uuid_value",
                done=True,
            )
        )

        response = await client.cancel_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, jobs.Job)

    assert response.submitted_by == "submitted_by_value"

    assert response.driver_output_resource_uri == "driver_output_resource_uri_value"

    assert response.driver_control_files_uri == "driver_control_files_uri_value"

    assert response.job_uuid == "job_uuid_value"

    assert response.done is True


def test_cancel_job_flattened():
    client = JobControllerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.cancel_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = jobs.Job()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.cancel_job(
            project_id="project_id_value", region="region_value", job_id="job_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].region == "region_value"

        assert args[0].job_id == "job_id_value"


def test_cancel_job_flattened_error():
    client = JobControllerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.cancel_job(
            jobs.CancelJobRequest(),
            project_id="project_id_value",
            region="region_value",
            job_id="job_id_value",
        )


@pytest.mark.asyncio
async def test_cancel_job_flattened_async():
    client = JobControllerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.cancel_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = jobs.Job()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(jobs.Job())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.cancel_job(
            project_id="project_id_value", region="region_value", job_id="job_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].region == "region_value"

        assert args[0].job_id == "job_id_value"


@pytest.mark.asyncio
async def test_cancel_job_flattened_error_async():
    client = JobControllerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.cancel_job(
            jobs.CancelJobRequest(),
            project_id="project_id_value",
            region="region_value",
            job_id="job_id_value",
        )


def test_delete_job(transport: str = "grpc", request_type=jobs.DeleteJobRequest):
    client = JobControllerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == jobs.DeleteJobRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_job_from_dict():
    test_delete_job(request_type=dict)


@pytest.mark.asyncio
async def test_delete_job_async(transport: str = "grpc_asyncio"):
    client = JobControllerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = jobs.DeleteJobRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_job_flattened():
    client = JobControllerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_job(
            project_id="project_id_value", region="region_value", job_id="job_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].region == "region_value"

        assert args[0].job_id == "job_id_value"


def test_delete_job_flattened_error():
    client = JobControllerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_job(
            jobs.DeleteJobRequest(),
            project_id="project_id_value",
            region="region_value",
            job_id="job_id_value",
        )


@pytest.mark.asyncio
async def test_delete_job_flattened_async():
    client = JobControllerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_job), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_job(
            project_id="project_id_value", region="region_value", job_id="job_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_id == "project_id_value"

        assert args[0].region == "region_value"

        assert args[0].job_id == "job_id_value"


@pytest.mark.asyncio
async def test_delete_job_flattened_error_async():
    client = JobControllerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_job(
            jobs.DeleteJobRequest(),
            project_id="project_id_value",
            region="region_value",
            job_id="job_id_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.JobControllerGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = JobControllerClient(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.JobControllerGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = JobControllerClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.JobControllerGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = JobControllerClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.JobControllerGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = JobControllerClient(transport=transport)
    assert client._transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.JobControllerGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.JobControllerGrpcAsyncIOTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = JobControllerClient(credentials=credentials.AnonymousCredentials(),)
    assert isinstance(client._transport, transports.JobControllerGrpcTransport,)


def test_job_controller_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.JobControllerTransport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_job_controller_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.dataproc_v1beta2.services.job_controller.transports.JobControllerTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.JobControllerTransport(
            credentials=credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "submit_job",
        "submit_job_as_operation",
        "get_job",
        "list_jobs",
        "update_job",
        "cancel_job",
        "delete_job",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client


def test_job_controller_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        auth, "load_credentials_from_file"
    ) as load_creds, mock.patch(
        "google.cloud.dataproc_v1beta2.services.job_controller.transports.JobControllerTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.JobControllerTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_job_controller_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        JobControllerClient()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


def test_job_controller_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.JobControllerGrpcTransport(
            host="squid.clam.whelk", quota_project_id="octopus"
        )
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_job_controller_host_no_port():
    client = JobControllerClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dataproc.googleapis.com"
        ),
    )
    assert client._transport._host == "dataproc.googleapis.com:443"


def test_job_controller_host_with_port():
    client = JobControllerClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dataproc.googleapis.com:8000"
        ),
    )
    assert client._transport._host == "dataproc.googleapis.com:8000"


def test_job_controller_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")

    # Check that if channel is provided, mtls endpoint and client_cert_source
    # won't be used.
    callback = mock.MagicMock()
    transport = transports.JobControllerGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=callback,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert not callback.called


def test_job_controller_grpc_asyncio_transport_channel():
    channel = aio.insecure_channel("http://localhost/")

    # Check that if channel is provided, mtls endpoint and client_cert_source
    # won't be used.
    callback = mock.MagicMock()
    transport = transports.JobControllerGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=callback,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert not callback.called


@mock.patch("grpc.ssl_channel_credentials", autospec=True)
@mock.patch("google.api_core.grpc_helpers.create_channel", autospec=True)
def test_job_controller_grpc_transport_channel_mtls_with_client_cert_source(
    grpc_create_channel, grpc_ssl_channel_cred
):
    # Check that if channel is None, but api_mtls_endpoint and client_cert_source
    # are provided, then a mTLS channel will be created.
    mock_cred = mock.Mock()

    mock_ssl_cred = mock.Mock()
    grpc_ssl_channel_cred.return_value = mock_ssl_cred

    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    transport = transports.JobControllerGrpcTransport(
        host="squid.clam.whelk",
        credentials=mock_cred,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=client_cert_source_callback,
    )
    grpc_ssl_channel_cred.assert_called_once_with(
        certificate_chain=b"cert bytes", private_key=b"key bytes"
    )
    grpc_create_channel.assert_called_once_with(
        "mtls.squid.clam.whelk:443",
        credentials=mock_cred,
        credentials_file=None,
        scopes=("https://www.googleapis.com/auth/cloud-platform",),
        ssl_credentials=mock_ssl_cred,
        quota_project_id=None,
    )
    assert transport.grpc_channel == mock_grpc_channel


@mock.patch("grpc.ssl_channel_credentials", autospec=True)
@mock.patch("google.api_core.grpc_helpers_async.create_channel", autospec=True)
def test_job_controller_grpc_asyncio_transport_channel_mtls_with_client_cert_source(
    grpc_create_channel, grpc_ssl_channel_cred
):
    # Check that if channel is None, but api_mtls_endpoint and client_cert_source
    # are provided, then a mTLS channel will be created.
    mock_cred = mock.Mock()

    mock_ssl_cred = mock.Mock()
    grpc_ssl_channel_cred.return_value = mock_ssl_cred

    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    transport = transports.JobControllerGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        credentials=mock_cred,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=client_cert_source_callback,
    )
    grpc_ssl_channel_cred.assert_called_once_with(
        certificate_chain=b"cert bytes", private_key=b"key bytes"
    )
    grpc_create_channel.assert_called_once_with(
        "mtls.squid.clam.whelk:443",
        credentials=mock_cred,
        credentials_file=None,
        scopes=("https://www.googleapis.com/auth/cloud-platform",),
        ssl_credentials=mock_ssl_cred,
        quota_project_id=None,
    )
    assert transport.grpc_channel == mock_grpc_channel


@pytest.mark.parametrize(
    "api_mtls_endpoint", ["mtls.squid.clam.whelk", "mtls.squid.clam.whelk:443"]
)
@mock.patch("google.api_core.grpc_helpers.create_channel", autospec=True)
def test_job_controller_grpc_transport_channel_mtls_with_adc(
    grpc_create_channel, api_mtls_endpoint
):
    # Check that if channel and client_cert_source are None, but api_mtls_endpoint
    # is provided, then a mTLS channel will be created with SSL ADC.
    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    # Mock google.auth.transport.grpc.SslCredentials class.
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        mock_cred = mock.Mock()
        transport = transports.JobControllerGrpcTransport(
            host="squid.clam.whelk",
            credentials=mock_cred,
            api_mtls_endpoint=api_mtls_endpoint,
            client_cert_source=None,
        )
        grpc_create_channel.assert_called_once_with(
            "mtls.squid.clam.whelk:443",
            credentials=mock_cred,
            credentials_file=None,
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            ssl_credentials=mock_ssl_cred,
            quota_project_id=None,
        )
        assert transport.grpc_channel == mock_grpc_channel


@pytest.mark.parametrize(
    "api_mtls_endpoint", ["mtls.squid.clam.whelk", "mtls.squid.clam.whelk:443"]
)
@mock.patch("google.api_core.grpc_helpers_async.create_channel", autospec=True)
def test_job_controller_grpc_asyncio_transport_channel_mtls_with_adc(
    grpc_create_channel, api_mtls_endpoint
):
    # Check that if channel and client_cert_source are None, but api_mtls_endpoint
    # is provided, then a mTLS channel will be created with SSL ADC.
    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    # Mock google.auth.transport.grpc.SslCredentials class.
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        mock_cred = mock.Mock()
        transport = transports.JobControllerGrpcAsyncIOTransport(
            host="squid.clam.whelk",
            credentials=mock_cred,
            api_mtls_endpoint=api_mtls_endpoint,
            client_cert_source=None,
        )
        grpc_create_channel.assert_called_once_with(
            "mtls.squid.clam.whelk:443",
            credentials=mock_cred,
            credentials_file=None,
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            ssl_credentials=mock_ssl_cred,
            quota_project_id=None,
        )
        assert transport.grpc_channel == mock_grpc_channel


def test_job_controller_grpc_lro_client():
    client = JobControllerClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )
    transport = client._transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_job_controller_grpc_lro_async_client():
    client = JobControllerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc_asyncio",
    )
    transport = client._client._transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsAsyncClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client
