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
from google.analytics.data_v1alpha.services.alpha_analytics_data import (
    AlphaAnalyticsDataAsyncClient,
)
from google.analytics.data_v1alpha.services.alpha_analytics_data import (
    AlphaAnalyticsDataClient,
)
from google.analytics.data_v1alpha.services.alpha_analytics_data import transports
from google.analytics.data_v1alpha.types import analytics_data_api
from google.analytics.data_v1alpha.types import data
from google.api_core import client_options
from google.api_core import exceptions
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.auth import credentials
from google.auth.exceptions import MutualTLSChannelError
from google.oauth2 import service_account


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

    assert AlphaAnalyticsDataClient._get_default_mtls_endpoint(None) is None
    assert (
        AlphaAnalyticsDataClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        AlphaAnalyticsDataClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        AlphaAnalyticsDataClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        AlphaAnalyticsDataClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        AlphaAnalyticsDataClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class", [AlphaAnalyticsDataClient, AlphaAnalyticsDataAsyncClient]
)
def test_alpha_analytics_data_client_from_service_account_file(client_class):
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client.transport._credentials == creds

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client.transport._credentials == creds

        assert client.transport._host == "analyticsdata.googleapis.com:443"


def test_alpha_analytics_data_client_get_transport_class():
    transport = AlphaAnalyticsDataClient.get_transport_class()
    assert transport == transports.AlphaAnalyticsDataGrpcTransport

    transport = AlphaAnalyticsDataClient.get_transport_class("grpc")
    assert transport == transports.AlphaAnalyticsDataGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (AlphaAnalyticsDataClient, transports.AlphaAnalyticsDataGrpcTransport, "grpc"),
        (
            AlphaAnalyticsDataAsyncClient,
            transports.AlphaAnalyticsDataGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    AlphaAnalyticsDataClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(AlphaAnalyticsDataClient),
)
@mock.patch.object(
    AlphaAnalyticsDataAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(AlphaAnalyticsDataAsyncClient),
)
def test_alpha_analytics_data_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(AlphaAnalyticsDataClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(AlphaAnalyticsDataClient, "get_transport_class") as gtc:
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
            ssl_channel_credentials=None,
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
                ssl_channel_credentials=None,
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
                ssl_channel_credentials=None,
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
            ssl_channel_credentials=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (
            AlphaAnalyticsDataClient,
            transports.AlphaAnalyticsDataGrpcTransport,
            "grpc",
            "true",
        ),
        (
            AlphaAnalyticsDataAsyncClient,
            transports.AlphaAnalyticsDataGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            AlphaAnalyticsDataClient,
            transports.AlphaAnalyticsDataGrpcTransport,
            "grpc",
            "false",
        ),
        (
            AlphaAnalyticsDataAsyncClient,
            transports.AlphaAnalyticsDataGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    AlphaAnalyticsDataClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(AlphaAnalyticsDataClient),
)
@mock.patch.object(
    AlphaAnalyticsDataAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(AlphaAnalyticsDataAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_alpha_analytics_data_client_mtls_env_auto(
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
            ssl_channel_creds = mock.Mock()
            with mock.patch(
                "grpc.ssl_channel_credentials", return_value=ssl_channel_creds
            ):
                patched.return_value = None
                client = client_class(client_options=options)

                if use_client_cert_env == "false":
                    expected_ssl_channel_creds = None
                    expected_host = client.DEFAULT_ENDPOINT
                else:
                    expected_ssl_channel_creds = ssl_channel_creds
                    expected_host = client.DEFAULT_MTLS_ENDPOINT

                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=expected_host,
                    scopes=None,
                    ssl_channel_credentials=expected_ssl_channel_creds,
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
                "google.auth.transport.grpc.SslCredentials.__init__", return_value=None
            ):
                with mock.patch(
                    "google.auth.transport.grpc.SslCredentials.is_mtls",
                    new_callable=mock.PropertyMock,
                ) as is_mtls_mock:
                    with mock.patch(
                        "google.auth.transport.grpc.SslCredentials.ssl_credentials",
                        new_callable=mock.PropertyMock,
                    ) as ssl_credentials_mock:
                        if use_client_cert_env == "false":
                            is_mtls_mock.return_value = False
                            ssl_credentials_mock.return_value = None
                            expected_host = client.DEFAULT_ENDPOINT
                            expected_ssl_channel_creds = None
                        else:
                            is_mtls_mock.return_value = True
                            ssl_credentials_mock.return_value = mock.Mock()
                            expected_host = client.DEFAULT_MTLS_ENDPOINT
                            expected_ssl_channel_creds = (
                                ssl_credentials_mock.return_value
                            )

                        patched.return_value = None
                        client = client_class()
                        patched.assert_called_once_with(
                            credentials=None,
                            credentials_file=None,
                            host=expected_host,
                            scopes=None,
                            ssl_channel_credentials=expected_ssl_channel_creds,
                            quota_project_id=None,
                            client_info=transports.base.DEFAULT_CLIENT_INFO,
                        )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.grpc.SslCredentials.__init__", return_value=None
            ):
                with mock.patch(
                    "google.auth.transport.grpc.SslCredentials.is_mtls",
                    new_callable=mock.PropertyMock,
                ) as is_mtls_mock:
                    is_mtls_mock.return_value = False
                    patched.return_value = None
                    client = client_class()
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=client.DEFAULT_ENDPOINT,
                        scopes=None,
                        ssl_channel_credentials=None,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                    )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (AlphaAnalyticsDataClient, transports.AlphaAnalyticsDataGrpcTransport, "grpc"),
        (
            AlphaAnalyticsDataAsyncClient,
            transports.AlphaAnalyticsDataGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_alpha_analytics_data_client_client_options_scopes(
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
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (AlphaAnalyticsDataClient, transports.AlphaAnalyticsDataGrpcTransport, "grpc"),
        (
            AlphaAnalyticsDataAsyncClient,
            transports.AlphaAnalyticsDataGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_alpha_analytics_data_client_client_options_credentials_file(
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
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_alpha_analytics_data_client_client_options_from_dict():
    with mock.patch(
        "google.analytics.data_v1alpha.services.alpha_analytics_data.transports.AlphaAnalyticsDataGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = AlphaAnalyticsDataClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_run_report(
    transport: str = "grpc", request_type=analytics_data_api.RunReportRequest
):
    client = AlphaAnalyticsDataClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_report), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_data_api.RunReportResponse(row_count=992,)

        response = client.run_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == analytics_data_api.RunReportRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, analytics_data_api.RunReportResponse)

    assert response.row_count == 992


def test_run_report_from_dict():
    test_run_report(request_type=dict)


@pytest.mark.asyncio
async def test_run_report_async(
    transport: str = "grpc_asyncio", request_type=analytics_data_api.RunReportRequest
):
    client = AlphaAnalyticsDataAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_report), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.RunReportResponse(row_count=992,)
        )

        response = await client.run_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == analytics_data_api.RunReportRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_data_api.RunReportResponse)

    assert response.row_count == 992


@pytest.mark.asyncio
async def test_run_report_async_from_dict():
    await test_run_report_async(request_type=dict)


def test_run_pivot_report(
    transport: str = "grpc", request_type=analytics_data_api.RunPivotReportRequest
):
    client = AlphaAnalyticsDataClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_pivot_report), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_data_api.RunPivotReportResponse()

        response = client.run_pivot_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == analytics_data_api.RunPivotReportRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, analytics_data_api.RunPivotReportResponse)


def test_run_pivot_report_from_dict():
    test_run_pivot_report(request_type=dict)


@pytest.mark.asyncio
async def test_run_pivot_report_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_data_api.RunPivotReportRequest,
):
    client = AlphaAnalyticsDataAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_pivot_report), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.RunPivotReportResponse()
        )

        response = await client.run_pivot_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == analytics_data_api.RunPivotReportRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_data_api.RunPivotReportResponse)


@pytest.mark.asyncio
async def test_run_pivot_report_async_from_dict():
    await test_run_pivot_report_async(request_type=dict)


def test_batch_run_reports(
    transport: str = "grpc", request_type=analytics_data_api.BatchRunReportsRequest
):
    client = AlphaAnalyticsDataClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_run_reports), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_data_api.BatchRunReportsResponse()

        response = client.batch_run_reports(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == analytics_data_api.BatchRunReportsRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, analytics_data_api.BatchRunReportsResponse)


def test_batch_run_reports_from_dict():
    test_batch_run_reports(request_type=dict)


@pytest.mark.asyncio
async def test_batch_run_reports_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_data_api.BatchRunReportsRequest,
):
    client = AlphaAnalyticsDataAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_run_reports), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.BatchRunReportsResponse()
        )

        response = await client.batch_run_reports(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == analytics_data_api.BatchRunReportsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_data_api.BatchRunReportsResponse)


@pytest.mark.asyncio
async def test_batch_run_reports_async_from_dict():
    await test_batch_run_reports_async(request_type=dict)


def test_batch_run_pivot_reports(
    transport: str = "grpc", request_type=analytics_data_api.BatchRunPivotReportsRequest
):
    client = AlphaAnalyticsDataClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_run_pivot_reports), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_data_api.BatchRunPivotReportsResponse()

        response = client.batch_run_pivot_reports(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == analytics_data_api.BatchRunPivotReportsRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, analytics_data_api.BatchRunPivotReportsResponse)


def test_batch_run_pivot_reports_from_dict():
    test_batch_run_pivot_reports(request_type=dict)


@pytest.mark.asyncio
async def test_batch_run_pivot_reports_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_data_api.BatchRunPivotReportsRequest,
):
    client = AlphaAnalyticsDataAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_run_pivot_reports), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.BatchRunPivotReportsResponse()
        )

        response = await client.batch_run_pivot_reports(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == analytics_data_api.BatchRunPivotReportsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_data_api.BatchRunPivotReportsResponse)


@pytest.mark.asyncio
async def test_batch_run_pivot_reports_async_from_dict():
    await test_batch_run_pivot_reports_async(request_type=dict)


def test_get_metadata(
    transport: str = "grpc", request_type=analytics_data_api.GetMetadataRequest
):
    client = AlphaAnalyticsDataClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_metadata), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_data_api.Metadata(name="name_value",)

        response = client.get_metadata(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == analytics_data_api.GetMetadataRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, analytics_data_api.Metadata)

    assert response.name == "name_value"


def test_get_metadata_from_dict():
    test_get_metadata(request_type=dict)


@pytest.mark.asyncio
async def test_get_metadata_async(
    transport: str = "grpc_asyncio", request_type=analytics_data_api.GetMetadataRequest
):
    client = AlphaAnalyticsDataAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_metadata), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.Metadata(name="name_value",)
        )

        response = await client.get_metadata(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == analytics_data_api.GetMetadataRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_data_api.Metadata)

    assert response.name == "name_value"


@pytest.mark.asyncio
async def test_get_metadata_async_from_dict():
    await test_get_metadata_async(request_type=dict)


def test_get_metadata_field_headers():
    client = AlphaAnalyticsDataClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_data_api.GetMetadataRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_metadata), "__call__") as call:
        call.return_value = analytics_data_api.Metadata()

        client.get_metadata(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_metadata_field_headers_async():
    client = AlphaAnalyticsDataAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_data_api.GetMetadataRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_metadata), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.Metadata()
        )

        await client.get_metadata(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_metadata_flattened():
    client = AlphaAnalyticsDataClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_metadata), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_data_api.Metadata()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_metadata(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_metadata_flattened_error():
    client = AlphaAnalyticsDataClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_metadata(
            analytics_data_api.GetMetadataRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_metadata_flattened_async():
    client = AlphaAnalyticsDataAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_metadata), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_data_api.Metadata()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.Metadata()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_metadata(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_metadata_flattened_error_async():
    client = AlphaAnalyticsDataAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_metadata(
            analytics_data_api.GetMetadataRequest(), name="name_value",
        )


def test_run_realtime_report(
    transport: str = "grpc", request_type=analytics_data_api.RunRealtimeReportRequest
):
    client = AlphaAnalyticsDataClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_realtime_report), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = analytics_data_api.RunRealtimeReportResponse(row_count=992,)

        response = client.run_realtime_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == analytics_data_api.RunRealtimeReportRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, analytics_data_api.RunRealtimeReportResponse)

    assert response.row_count == 992


def test_run_realtime_report_from_dict():
    test_run_realtime_report(request_type=dict)


@pytest.mark.asyncio
async def test_run_realtime_report_async(
    transport: str = "grpc_asyncio",
    request_type=analytics_data_api.RunRealtimeReportRequest,
):
    client = AlphaAnalyticsDataAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_realtime_report), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.RunRealtimeReportResponse(row_count=992,)
        )

        response = await client.run_realtime_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == analytics_data_api.RunRealtimeReportRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, analytics_data_api.RunRealtimeReportResponse)

    assert response.row_count == 992


@pytest.mark.asyncio
async def test_run_realtime_report_async_from_dict():
    await test_run_realtime_report_async(request_type=dict)


def test_run_realtime_report_field_headers():
    client = AlphaAnalyticsDataClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_data_api.RunRealtimeReportRequest()
    request.property = "property/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_realtime_report), "__call__"
    ) as call:
        call.return_value = analytics_data_api.RunRealtimeReportResponse()

        client.run_realtime_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "property=property/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_run_realtime_report_field_headers_async():
    client = AlphaAnalyticsDataAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = analytics_data_api.RunRealtimeReportRequest()
    request.property = "property/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_realtime_report), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            analytics_data_api.RunRealtimeReportResponse()
        )

        await client.run_realtime_report(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "property=property/value",) in kw["metadata"]


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.AlphaAnalyticsDataGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AlphaAnalyticsDataClient(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.AlphaAnalyticsDataGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AlphaAnalyticsDataClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.AlphaAnalyticsDataGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AlphaAnalyticsDataClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.AlphaAnalyticsDataGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = AlphaAnalyticsDataClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.AlphaAnalyticsDataGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.AlphaAnalyticsDataGrpcAsyncIOTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.AlphaAnalyticsDataGrpcTransport,
        transports.AlphaAnalyticsDataGrpcAsyncIOTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = AlphaAnalyticsDataClient(credentials=credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.AlphaAnalyticsDataGrpcTransport,)


def test_alpha_analytics_data_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.AlphaAnalyticsDataTransport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_alpha_analytics_data_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.analytics.data_v1alpha.services.alpha_analytics_data.transports.AlphaAnalyticsDataTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.AlphaAnalyticsDataTransport(
            credentials=credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "run_report",
        "run_pivot_report",
        "batch_run_reports",
        "batch_run_pivot_reports",
        "get_metadata",
        "run_realtime_report",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_alpha_analytics_data_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        auth, "load_credentials_from_file"
    ) as load_creds, mock.patch(
        "google.analytics.data_v1alpha.services.alpha_analytics_data.transports.AlphaAnalyticsDataTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.AlphaAnalyticsDataTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=(
                "https://www.googleapis.com/auth/analytics",
                "https://www.googleapis.com/auth/analytics.readonly",
            ),
            quota_project_id="octopus",
        )


def test_alpha_analytics_data_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(auth, "default") as adc, mock.patch(
        "google.analytics.data_v1alpha.services.alpha_analytics_data.transports.AlphaAnalyticsDataTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.AlphaAnalyticsDataTransport()
        adc.assert_called_once()


def test_alpha_analytics_data_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        AlphaAnalyticsDataClient()
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/analytics",
                "https://www.googleapis.com/auth/analytics.readonly",
            ),
            quota_project_id=None,
        )


def test_alpha_analytics_data_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.AlphaAnalyticsDataGrpcTransport(
            host="squid.clam.whelk", quota_project_id="octopus"
        )
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/analytics",
                "https://www.googleapis.com/auth/analytics.readonly",
            ),
            quota_project_id="octopus",
        )


def test_alpha_analytics_data_host_no_port():
    client = AlphaAnalyticsDataClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="analyticsdata.googleapis.com"
        ),
    )
    assert client.transport._host == "analyticsdata.googleapis.com:443"


def test_alpha_analytics_data_host_with_port():
    client = AlphaAnalyticsDataClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="analyticsdata.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "analyticsdata.googleapis.com:8000"


def test_alpha_analytics_data_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")

    # Check that channel is used if provided.
    transport = transports.AlphaAnalyticsDataGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_alpha_analytics_data_grpc_asyncio_transport_channel():
    channel = aio.insecure_channel("http://localhost/")

    # Check that channel is used if provided.
    transport = transports.AlphaAnalyticsDataGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.AlphaAnalyticsDataGrpcTransport,
        transports.AlphaAnalyticsDataGrpcAsyncIOTransport,
    ],
)
def test_alpha_analytics_data_transport_channel_mtls_with_client_cert_source(
    transport_class,
):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel", autospec=True
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
                scopes=(
                    "https://www.googleapis.com/auth/analytics",
                    "https://www.googleapis.com/auth/analytics.readonly",
                ),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.AlphaAnalyticsDataGrpcTransport,
        transports.AlphaAnalyticsDataGrpcAsyncIOTransport,
    ],
)
def test_alpha_analytics_data_transport_channel_mtls_with_adc(transport_class):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel", autospec=True
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
                scopes=(
                    "https://www.googleapis.com/auth/analytics",
                    "https://www.googleapis.com/auth/analytics.readonly",
                ),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_metadata_path():
    property = "squid"

    expected = "properties/{property}/metadata".format(property=property,)
    actual = AlphaAnalyticsDataClient.metadata_path(property)
    assert expected == actual


def test_parse_metadata_path():
    expected = {
        "property": "clam",
    }
    path = AlphaAnalyticsDataClient.metadata_path(**expected)

    # Check that the path construction is reversible.
    actual = AlphaAnalyticsDataClient.parse_metadata_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "whelk"

    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = AlphaAnalyticsDataClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "octopus",
    }
    path = AlphaAnalyticsDataClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = AlphaAnalyticsDataClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "oyster"

    expected = "folders/{folder}".format(folder=folder,)
    actual = AlphaAnalyticsDataClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nudibranch",
    }
    path = AlphaAnalyticsDataClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = AlphaAnalyticsDataClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "cuttlefish"

    expected = "organizations/{organization}".format(organization=organization,)
    actual = AlphaAnalyticsDataClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "mussel",
    }
    path = AlphaAnalyticsDataClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = AlphaAnalyticsDataClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "winkle"

    expected = "projects/{project}".format(project=project,)
    actual = AlphaAnalyticsDataClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nautilus",
    }
    path = AlphaAnalyticsDataClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = AlphaAnalyticsDataClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "scallop"
    location = "abalone"

    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = AlphaAnalyticsDataClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "squid",
        "location": "clam",
    }
    path = AlphaAnalyticsDataClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = AlphaAnalyticsDataClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.AlphaAnalyticsDataTransport, "_prep_wrapped_messages"
    ) as prep:
        client = AlphaAnalyticsDataClient(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.AlphaAnalyticsDataTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = AlphaAnalyticsDataClient.get_transport_class()
        transport = transport_class(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
