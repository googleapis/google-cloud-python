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
from google.api_core import future
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.api_core import operation_async  # type: ignore
from google.api_core import operations_v1
from google.api_core import path_template
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.dataproc_v1.services.job_controller import JobControllerAsyncClient
from google.cloud.dataproc_v1.services.job_controller import JobControllerClient
from google.cloud.dataproc_v1.services.job_controller import pagers
from google.cloud.dataproc_v1.services.job_controller import transports
from google.cloud.dataproc_v1.types import jobs
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
    "client_class", [JobControllerClient, JobControllerAsyncClient,]
)
def test_job_controller_client_from_service_account_info(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "dataproc.googleapis.com:443"


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.JobControllerGrpcTransport, "grpc"),
        (transports.JobControllerGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_job_controller_client_service_account_always_use_jwt(
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
    "client_class", [JobControllerClient, JobControllerAsyncClient,]
)
def test_job_controller_client_from_service_account_file(client_class):
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

        assert client.transport._host == "dataproc.googleapis.com:443"


def test_job_controller_client_get_transport_class():
    transport = JobControllerClient.get_transport_class()
    available_transports = [
        transports.JobControllerGrpcTransport,
    ]
    assert transport in available_transports

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
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
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
        (JobControllerClient, transports.JobControllerGrpcTransport, "grpc", "true"),
        (
            JobControllerAsyncClient,
            transports.JobControllerGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (JobControllerClient, transports.JobControllerGrpcTransport, "grpc", "false"),
        (
            JobControllerAsyncClient,
            transports.JobControllerGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
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
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_job_controller_client_mtls_env_auto(
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


def test_job_controller_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.dataproc_v1.services.job_controller.transports.JobControllerGrpcTransport.__init__"
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
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )


@pytest.mark.parametrize("request_type", [jobs.SubmitJobRequest, dict,])
def test_submit_job(request_type, transport: str = "grpc"):
    client = JobControllerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.submit_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = jobs.Job(
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
    assert response.driver_output_resource_uri == "driver_output_resource_uri_value"
    assert response.driver_control_files_uri == "driver_control_files_uri_value"
    assert response.job_uuid == "job_uuid_value"
    assert response.done is True


def test_submit_job_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = JobControllerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.submit_job), "__call__") as call:
        client.submit_job()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == jobs.SubmitJobRequest()


@pytest.mark.asyncio
async def test_submit_job_async(
    transport: str = "grpc_asyncio", request_type=jobs.SubmitJobRequest
):
    client = JobControllerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.submit_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            jobs.Job(
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
        assert args[0] == jobs.SubmitJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, jobs.Job)
    assert response.driver_output_resource_uri == "driver_output_resource_uri_value"
    assert response.driver_control_files_uri == "driver_control_files_uri_value"
    assert response.job_uuid == "job_uuid_value"
    assert response.done is True


@pytest.mark.asyncio
async def test_submit_job_async_from_dict():
    await test_submit_job_async(request_type=dict)


def test_submit_job_flattened():
    client = JobControllerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.submit_job), "__call__") as call:
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
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].region
        mock_val = "region_value"
        assert arg == mock_val
        arg = args[0].job
        mock_val = jobs.Job(reference=jobs.JobReference(project_id="project_id_value"))
        assert arg == mock_val


def test_submit_job_flattened_error():
    client = JobControllerClient(credentials=ga_credentials.AnonymousCredentials(),)

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
    client = JobControllerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.submit_job), "__call__") as call:
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
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].region
        mock_val = "region_value"
        assert arg == mock_val
        arg = args[0].job
        mock_val = jobs.Job(reference=jobs.JobReference(project_id="project_id_value"))
        assert arg == mock_val


@pytest.mark.asyncio
async def test_submit_job_flattened_error_async():
    client = JobControllerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.submit_job(
            jobs.SubmitJobRequest(),
            project_id="project_id_value",
            region="region_value",
            job=jobs.Job(reference=jobs.JobReference(project_id="project_id_value")),
        )


@pytest.mark.parametrize("request_type", [jobs.SubmitJobRequest, dict,])
def test_submit_job_as_operation(request_type, transport: str = "grpc"):
    client = JobControllerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.submit_job_as_operation), "__call__"
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


def test_submit_job_as_operation_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = JobControllerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.submit_job_as_operation), "__call__"
    ) as call:
        client.submit_job_as_operation()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == jobs.SubmitJobRequest()


@pytest.mark.asyncio
async def test_submit_job_as_operation_async(
    transport: str = "grpc_asyncio", request_type=jobs.SubmitJobRequest
):
    client = JobControllerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.submit_job_as_operation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.submit_job_as_operation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == jobs.SubmitJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_submit_job_as_operation_async_from_dict():
    await test_submit_job_as_operation_async(request_type=dict)


def test_submit_job_as_operation_flattened():
    client = JobControllerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.submit_job_as_operation), "__call__"
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
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].region
        mock_val = "region_value"
        assert arg == mock_val
        arg = args[0].job
        mock_val = jobs.Job(reference=jobs.JobReference(project_id="project_id_value"))
        assert arg == mock_val


def test_submit_job_as_operation_flattened_error():
    client = JobControllerClient(credentials=ga_credentials.AnonymousCredentials(),)

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
    client = JobControllerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.submit_job_as_operation), "__call__"
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
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].region
        mock_val = "region_value"
        assert arg == mock_val
        arg = args[0].job
        mock_val = jobs.Job(reference=jobs.JobReference(project_id="project_id_value"))
        assert arg == mock_val


@pytest.mark.asyncio
async def test_submit_job_as_operation_flattened_error_async():
    client = JobControllerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.submit_job_as_operation(
            jobs.SubmitJobRequest(),
            project_id="project_id_value",
            region="region_value",
            job=jobs.Job(reference=jobs.JobReference(project_id="project_id_value")),
        )


@pytest.mark.parametrize("request_type", [jobs.GetJobRequest, dict,])
def test_get_job(request_type, transport: str = "grpc"):
    client = JobControllerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = jobs.Job(
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
    assert response.driver_output_resource_uri == "driver_output_resource_uri_value"
    assert response.driver_control_files_uri == "driver_control_files_uri_value"
    assert response.job_uuid == "job_uuid_value"
    assert response.done is True


def test_get_job_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = JobControllerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_job), "__call__") as call:
        client.get_job()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == jobs.GetJobRequest()


@pytest.mark.asyncio
async def test_get_job_async(
    transport: str = "grpc_asyncio", request_type=jobs.GetJobRequest
):
    client = JobControllerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            jobs.Job(
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
        assert args[0] == jobs.GetJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, jobs.Job)
    assert response.driver_output_resource_uri == "driver_output_resource_uri_value"
    assert response.driver_control_files_uri == "driver_control_files_uri_value"
    assert response.job_uuid == "job_uuid_value"
    assert response.done is True


@pytest.mark.asyncio
async def test_get_job_async_from_dict():
    await test_get_job_async(request_type=dict)


def test_get_job_flattened():
    client = JobControllerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_job), "__call__") as call:
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
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].region
        mock_val = "region_value"
        assert arg == mock_val
        arg = args[0].job_id
        mock_val = "job_id_value"
        assert arg == mock_val


def test_get_job_flattened_error():
    client = JobControllerClient(credentials=ga_credentials.AnonymousCredentials(),)

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
    client = JobControllerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_job), "__call__") as call:
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
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].region
        mock_val = "region_value"
        assert arg == mock_val
        arg = args[0].job_id
        mock_val = "job_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_job_flattened_error_async():
    client = JobControllerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_job(
            jobs.GetJobRequest(),
            project_id="project_id_value",
            region="region_value",
            job_id="job_id_value",
        )


@pytest.mark.parametrize("request_type", [jobs.ListJobsRequest, dict,])
def test_list_jobs(request_type, transport: str = "grpc"):
    client = JobControllerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_jobs), "__call__") as call:
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


def test_list_jobs_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = JobControllerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_jobs), "__call__") as call:
        client.list_jobs()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == jobs.ListJobsRequest()


@pytest.mark.asyncio
async def test_list_jobs_async(
    transport: str = "grpc_asyncio", request_type=jobs.ListJobsRequest
):
    client = JobControllerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_jobs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            jobs.ListJobsResponse(next_page_token="next_page_token_value",)
        )
        response = await client.list_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == jobs.ListJobsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListJobsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_jobs_async_from_dict():
    await test_list_jobs_async(request_type=dict)


def test_list_jobs_flattened():
    client = JobControllerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_jobs), "__call__") as call:
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
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].region
        mock_val = "region_value"
        assert arg == mock_val
        arg = args[0].filter
        mock_val = "filter_value"
        assert arg == mock_val


def test_list_jobs_flattened_error():
    client = JobControllerClient(credentials=ga_credentials.AnonymousCredentials(),)

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
    client = JobControllerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_jobs), "__call__") as call:
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
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].region
        mock_val = "region_value"
        assert arg == mock_val
        arg = args[0].filter
        mock_val = "filter_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_jobs_flattened_error_async():
    client = JobControllerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_jobs(
            jobs.ListJobsRequest(),
            project_id="project_id_value",
            region="region_value",
            filter="filter_value",
        )


def test_list_jobs_pager(transport_name: str = "grpc"):
    client = JobControllerClient(
        credentials=ga_credentials.AnonymousCredentials, transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_jobs), "__call__") as call:
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


def test_list_jobs_pages(transport_name: str = "grpc"):
    client = JobControllerClient(
        credentials=ga_credentials.AnonymousCredentials, transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_jobs), "__call__") as call:
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
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_jobs_async_pager():
    client = JobControllerAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_jobs), "__call__", new_callable=mock.AsyncMock
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
    client = JobControllerAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_jobs), "__call__", new_callable=mock.AsyncMock
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
        async for page_ in (await client.list_jobs(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize("request_type", [jobs.UpdateJobRequest, dict,])
def test_update_job(request_type, transport: str = "grpc"):
    client = JobControllerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = jobs.Job(
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
    assert response.driver_output_resource_uri == "driver_output_resource_uri_value"
    assert response.driver_control_files_uri == "driver_control_files_uri_value"
    assert response.job_uuid == "job_uuid_value"
    assert response.done is True


def test_update_job_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = JobControllerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_job), "__call__") as call:
        client.update_job()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == jobs.UpdateJobRequest()


@pytest.mark.asyncio
async def test_update_job_async(
    transport: str = "grpc_asyncio", request_type=jobs.UpdateJobRequest
):
    client = JobControllerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            jobs.Job(
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
        assert args[0] == jobs.UpdateJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, jobs.Job)
    assert response.driver_output_resource_uri == "driver_output_resource_uri_value"
    assert response.driver_control_files_uri == "driver_control_files_uri_value"
    assert response.job_uuid == "job_uuid_value"
    assert response.done is True


@pytest.mark.asyncio
async def test_update_job_async_from_dict():
    await test_update_job_async(request_type=dict)


@pytest.mark.parametrize("request_type", [jobs.CancelJobRequest, dict,])
def test_cancel_job(request_type, transport: str = "grpc"):
    client = JobControllerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = jobs.Job(
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
    assert response.driver_output_resource_uri == "driver_output_resource_uri_value"
    assert response.driver_control_files_uri == "driver_control_files_uri_value"
    assert response.job_uuid == "job_uuid_value"
    assert response.done is True


def test_cancel_job_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = JobControllerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_job), "__call__") as call:
        client.cancel_job()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == jobs.CancelJobRequest()


@pytest.mark.asyncio
async def test_cancel_job_async(
    transport: str = "grpc_asyncio", request_type=jobs.CancelJobRequest
):
    client = JobControllerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            jobs.Job(
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
        assert args[0] == jobs.CancelJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, jobs.Job)
    assert response.driver_output_resource_uri == "driver_output_resource_uri_value"
    assert response.driver_control_files_uri == "driver_control_files_uri_value"
    assert response.job_uuid == "job_uuid_value"
    assert response.done is True


@pytest.mark.asyncio
async def test_cancel_job_async_from_dict():
    await test_cancel_job_async(request_type=dict)


def test_cancel_job_flattened():
    client = JobControllerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_job), "__call__") as call:
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
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].region
        mock_val = "region_value"
        assert arg == mock_val
        arg = args[0].job_id
        mock_val = "job_id_value"
        assert arg == mock_val


def test_cancel_job_flattened_error():
    client = JobControllerClient(credentials=ga_credentials.AnonymousCredentials(),)

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
    client = JobControllerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_job), "__call__") as call:
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
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].region
        mock_val = "region_value"
        assert arg == mock_val
        arg = args[0].job_id
        mock_val = "job_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_cancel_job_flattened_error_async():
    client = JobControllerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.cancel_job(
            jobs.CancelJobRequest(),
            project_id="project_id_value",
            region="region_value",
            job_id="job_id_value",
        )


@pytest.mark.parametrize("request_type", [jobs.DeleteJobRequest, dict,])
def test_delete_job(request_type, transport: str = "grpc"):
    client = JobControllerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == jobs.DeleteJobRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_job_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = JobControllerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_job), "__call__") as call:
        client.delete_job()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == jobs.DeleteJobRequest()


@pytest.mark.asyncio
async def test_delete_job_async(
    transport: str = "grpc_asyncio", request_type=jobs.DeleteJobRequest
):
    client = JobControllerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == jobs.DeleteJobRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_job_async_from_dict():
    await test_delete_job_async(request_type=dict)


def test_delete_job_flattened():
    client = JobControllerClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_job), "__call__") as call:
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
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].region
        mock_val = "region_value"
        assert arg == mock_val
        arg = args[0].job_id
        mock_val = "job_id_value"
        assert arg == mock_val


def test_delete_job_flattened_error():
    client = JobControllerClient(credentials=ga_credentials.AnonymousCredentials(),)

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
    client = JobControllerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_job), "__call__") as call:
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
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].region
        mock_val = "region_value"
        assert arg == mock_val
        arg = args[0].job_id
        mock_val = "job_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_job_flattened_error_async():
    client = JobControllerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

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
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = JobControllerClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.JobControllerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = JobControllerClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.JobControllerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = JobControllerClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.JobControllerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = JobControllerClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.JobControllerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.JobControllerGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.JobControllerGrpcTransport,
        transports.JobControllerGrpcAsyncIOTransport,
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
    client = JobControllerClient(credentials=ga_credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.JobControllerGrpcTransport,)


def test_job_controller_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.JobControllerTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_job_controller_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.dataproc_v1.services.job_controller.transports.JobControllerTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.JobControllerTransport(
            credentials=ga_credentials.AnonymousCredentials(),
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

    with pytest.raises(NotImplementedError):
        transport.close()

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client


def test_job_controller_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.dataproc_v1.services.job_controller.transports.JobControllerTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.JobControllerTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_job_controller_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.dataproc_v1.services.job_controller.transports.JobControllerTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.JobControllerTransport()
        adc.assert_called_once()


def test_job_controller_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        JobControllerClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.JobControllerGrpcTransport,
        transports.JobControllerGrpcAsyncIOTransport,
    ],
)
def test_job_controller_transport_auth_adc(transport_class):
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
        (transports.JobControllerGrpcTransport, grpc_helpers),
        (transports.JobControllerGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_job_controller_transport_create_channel(transport_class, grpc_helpers):
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
            "dataproc.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="dataproc.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.JobControllerGrpcTransport,
        transports.JobControllerGrpcAsyncIOTransport,
    ],
)
def test_job_controller_grpc_transport_client_cert_source_for_mtls(transport_class):
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


def test_job_controller_host_no_port():
    client = JobControllerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dataproc.googleapis.com"
        ),
    )
    assert client.transport._host == "dataproc.googleapis.com:443"


def test_job_controller_host_with_port():
    client = JobControllerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dataproc.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "dataproc.googleapis.com:8000"


def test_job_controller_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.JobControllerGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_job_controller_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.JobControllerGrpcAsyncIOTransport(
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
        transports.JobControllerGrpcTransport,
        transports.JobControllerGrpcAsyncIOTransport,
    ],
)
def test_job_controller_transport_channel_mtls_with_client_cert_source(transport_class):
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
        transports.JobControllerGrpcTransport,
        transports.JobControllerGrpcAsyncIOTransport,
    ],
)
def test_job_controller_transport_channel_mtls_with_adc(transport_class):
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


def test_job_controller_grpc_lro_client():
    client = JobControllerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_job_controller_grpc_lro_async_client():
    client = JobControllerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc_asyncio",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsAsyncClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_common_billing_account_path():
    billing_account = "squid"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = JobControllerClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "clam",
    }
    path = JobControllerClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = JobControllerClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "whelk"
    expected = "folders/{folder}".format(folder=folder,)
    actual = JobControllerClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "octopus",
    }
    path = JobControllerClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = JobControllerClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "oyster"
    expected = "organizations/{organization}".format(organization=organization,)
    actual = JobControllerClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nudibranch",
    }
    path = JobControllerClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = JobControllerClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "cuttlefish"
    expected = "projects/{project}".format(project=project,)
    actual = JobControllerClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "mussel",
    }
    path = JobControllerClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = JobControllerClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "winkle"
    location = "nautilus"
    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = JobControllerClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
    }
    path = JobControllerClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = JobControllerClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.JobControllerTransport, "_prep_wrapped_messages"
    ) as prep:
        client = JobControllerClient(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.JobControllerTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = JobControllerClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = JobControllerAsyncClient(
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
        client = JobControllerClient(
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
        client = JobControllerClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()
