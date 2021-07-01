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
from google.cloud.websecurityscanner_v1beta.services.web_security_scanner import (
    WebSecurityScannerAsyncClient,
)
from google.cloud.websecurityscanner_v1beta.services.web_security_scanner import (
    WebSecurityScannerClient,
)
from google.cloud.websecurityscanner_v1beta.services.web_security_scanner import pagers
from google.cloud.websecurityscanner_v1beta.services.web_security_scanner import (
    transports,
)
from google.cloud.websecurityscanner_v1beta.services.web_security_scanner.transports.base import (
    _GOOGLE_AUTH_VERSION,
)
from google.cloud.websecurityscanner_v1beta.types import crawled_url
from google.cloud.websecurityscanner_v1beta.types import finding
from google.cloud.websecurityscanner_v1beta.types import finding_addon
from google.cloud.websecurityscanner_v1beta.types import finding_type_stats
from google.cloud.websecurityscanner_v1beta.types import scan_config
from google.cloud.websecurityscanner_v1beta.types import scan_config as gcw_scan_config
from google.cloud.websecurityscanner_v1beta.types import scan_config_error
from google.cloud.websecurityscanner_v1beta.types import scan_run
from google.cloud.websecurityscanner_v1beta.types import scan_run_error_trace
from google.cloud.websecurityscanner_v1beta.types import scan_run_warning_trace
from google.cloud.websecurityscanner_v1beta.types import web_security_scanner
from google.oauth2 import service_account
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

    assert WebSecurityScannerClient._get_default_mtls_endpoint(None) is None
    assert (
        WebSecurityScannerClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        WebSecurityScannerClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        WebSecurityScannerClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        WebSecurityScannerClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        WebSecurityScannerClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class", [WebSecurityScannerClient, WebSecurityScannerAsyncClient,]
)
def test_web_security_scanner_client_from_service_account_info(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "websecurityscanner.googleapis.com:443"


@pytest.mark.parametrize(
    "client_class", [WebSecurityScannerClient, WebSecurityScannerAsyncClient,]
)
def test_web_security_scanner_client_service_account_always_use_jwt(client_class):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        client = client_class(credentials=creds)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.WebSecurityScannerGrpcTransport, "grpc"),
        (transports.WebSecurityScannerGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_web_security_scanner_client_service_account_always_use_jwt_true(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)


@pytest.mark.parametrize(
    "client_class", [WebSecurityScannerClient, WebSecurityScannerAsyncClient,]
)
def test_web_security_scanner_client_from_service_account_file(client_class):
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

        assert client.transport._host == "websecurityscanner.googleapis.com:443"


def test_web_security_scanner_client_get_transport_class():
    transport = WebSecurityScannerClient.get_transport_class()
    available_transports = [
        transports.WebSecurityScannerGrpcTransport,
    ]
    assert transport in available_transports

    transport = WebSecurityScannerClient.get_transport_class("grpc")
    assert transport == transports.WebSecurityScannerGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (WebSecurityScannerClient, transports.WebSecurityScannerGrpcTransport, "grpc"),
        (
            WebSecurityScannerAsyncClient,
            transports.WebSecurityScannerGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    WebSecurityScannerClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(WebSecurityScannerClient),
)
@mock.patch.object(
    WebSecurityScannerAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(WebSecurityScannerAsyncClient),
)
def test_web_security_scanner_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(WebSecurityScannerClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(WebSecurityScannerClient, "get_transport_class") as gtc:
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
            WebSecurityScannerClient,
            transports.WebSecurityScannerGrpcTransport,
            "grpc",
            "true",
        ),
        (
            WebSecurityScannerAsyncClient,
            transports.WebSecurityScannerGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            WebSecurityScannerClient,
            transports.WebSecurityScannerGrpcTransport,
            "grpc",
            "false",
        ),
        (
            WebSecurityScannerAsyncClient,
            transports.WebSecurityScannerGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    WebSecurityScannerClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(WebSecurityScannerClient),
)
@mock.patch.object(
    WebSecurityScannerAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(WebSecurityScannerAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_web_security_scanner_client_mtls_env_auto(
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
        (WebSecurityScannerClient, transports.WebSecurityScannerGrpcTransport, "grpc"),
        (
            WebSecurityScannerAsyncClient,
            transports.WebSecurityScannerGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_web_security_scanner_client_client_options_scopes(
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
        (WebSecurityScannerClient, transports.WebSecurityScannerGrpcTransport, "grpc"),
        (
            WebSecurityScannerAsyncClient,
            transports.WebSecurityScannerGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_web_security_scanner_client_client_options_credentials_file(
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


def test_web_security_scanner_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.websecurityscanner_v1beta.services.web_security_scanner.transports.WebSecurityScannerGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = WebSecurityScannerClient(
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


def test_create_scan_config(
    transport: str = "grpc", request_type=web_security_scanner.CreateScanConfigRequest
):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_scan_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcw_scan_config.ScanConfig(
            name="name_value",
            display_name="display_name_value",
            max_qps=761,
            starting_urls=["starting_urls_value"],
            user_agent=gcw_scan_config.ScanConfig.UserAgent.CHROME_LINUX,
            blacklist_patterns=["blacklist_patterns_value"],
            target_platforms=[gcw_scan_config.ScanConfig.TargetPlatform.APP_ENGINE],
            export_to_security_command_center=gcw_scan_config.ScanConfig.ExportToSecurityCommandCenter.ENABLED,
            risk_level=gcw_scan_config.ScanConfig.RiskLevel.NORMAL,
        )
        response = client.create_scan_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.CreateScanConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcw_scan_config.ScanConfig)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.max_qps == 761
    assert response.starting_urls == ["starting_urls_value"]
    assert response.user_agent == gcw_scan_config.ScanConfig.UserAgent.CHROME_LINUX
    assert response.blacklist_patterns == ["blacklist_patterns_value"]
    assert response.target_platforms == [
        gcw_scan_config.ScanConfig.TargetPlatform.APP_ENGINE
    ]
    assert (
        response.export_to_security_command_center
        == gcw_scan_config.ScanConfig.ExportToSecurityCommandCenter.ENABLED
    )
    assert response.risk_level == gcw_scan_config.ScanConfig.RiskLevel.NORMAL


def test_create_scan_config_from_dict():
    test_create_scan_config(request_type=dict)


def test_create_scan_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_scan_config), "__call__"
    ) as call:
        client.create_scan_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.CreateScanConfigRequest()


@pytest.mark.asyncio
async def test_create_scan_config_async(
    transport: str = "grpc_asyncio",
    request_type=web_security_scanner.CreateScanConfigRequest,
):
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_scan_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcw_scan_config.ScanConfig(
                name="name_value",
                display_name="display_name_value",
                max_qps=761,
                starting_urls=["starting_urls_value"],
                user_agent=gcw_scan_config.ScanConfig.UserAgent.CHROME_LINUX,
                blacklist_patterns=["blacklist_patterns_value"],
                target_platforms=[gcw_scan_config.ScanConfig.TargetPlatform.APP_ENGINE],
                export_to_security_command_center=gcw_scan_config.ScanConfig.ExportToSecurityCommandCenter.ENABLED,
                risk_level=gcw_scan_config.ScanConfig.RiskLevel.NORMAL,
            )
        )
        response = await client.create_scan_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.CreateScanConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcw_scan_config.ScanConfig)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.max_qps == 761
    assert response.starting_urls == ["starting_urls_value"]
    assert response.user_agent == gcw_scan_config.ScanConfig.UserAgent.CHROME_LINUX
    assert response.blacklist_patterns == ["blacklist_patterns_value"]
    assert response.target_platforms == [
        gcw_scan_config.ScanConfig.TargetPlatform.APP_ENGINE
    ]
    assert (
        response.export_to_security_command_center
        == gcw_scan_config.ScanConfig.ExportToSecurityCommandCenter.ENABLED
    )
    assert response.risk_level == gcw_scan_config.ScanConfig.RiskLevel.NORMAL


@pytest.mark.asyncio
async def test_create_scan_config_async_from_dict():
    await test_create_scan_config_async(request_type=dict)


def test_create_scan_config_field_headers():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.CreateScanConfigRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_scan_config), "__call__"
    ) as call:
        call.return_value = gcw_scan_config.ScanConfig()
        client.create_scan_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_scan_config_field_headers_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.CreateScanConfigRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_scan_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcw_scan_config.ScanConfig()
        )
        await client.create_scan_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_scan_config_flattened():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_scan_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcw_scan_config.ScanConfig()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_scan_config(
            parent="parent_value",
            scan_config=gcw_scan_config.ScanConfig(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].scan_config == gcw_scan_config.ScanConfig(name="name_value")


def test_create_scan_config_flattened_error():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_scan_config(
            web_security_scanner.CreateScanConfigRequest(),
            parent="parent_value",
            scan_config=gcw_scan_config.ScanConfig(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_scan_config_flattened_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_scan_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcw_scan_config.ScanConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcw_scan_config.ScanConfig()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_scan_config(
            parent="parent_value",
            scan_config=gcw_scan_config.ScanConfig(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].scan_config == gcw_scan_config.ScanConfig(name="name_value")


@pytest.mark.asyncio
async def test_create_scan_config_flattened_error_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_scan_config(
            web_security_scanner.CreateScanConfigRequest(),
            parent="parent_value",
            scan_config=gcw_scan_config.ScanConfig(name="name_value"),
        )


def test_delete_scan_config(
    transport: str = "grpc", request_type=web_security_scanner.DeleteScanConfigRequest
):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_scan_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_scan_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.DeleteScanConfigRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_scan_config_from_dict():
    test_delete_scan_config(request_type=dict)


def test_delete_scan_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_scan_config), "__call__"
    ) as call:
        client.delete_scan_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.DeleteScanConfigRequest()


@pytest.mark.asyncio
async def test_delete_scan_config_async(
    transport: str = "grpc_asyncio",
    request_type=web_security_scanner.DeleteScanConfigRequest,
):
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_scan_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_scan_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.DeleteScanConfigRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_scan_config_async_from_dict():
    await test_delete_scan_config_async(request_type=dict)


def test_delete_scan_config_field_headers():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.DeleteScanConfigRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_scan_config), "__call__"
    ) as call:
        call.return_value = None
        client.delete_scan_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_scan_config_field_headers_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.DeleteScanConfigRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_scan_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_scan_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_scan_config_flattened():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_scan_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_scan_config(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_scan_config_flattened_error():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_scan_config(
            web_security_scanner.DeleteScanConfigRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_scan_config_flattened_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_scan_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_scan_config(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_scan_config_flattened_error_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_scan_config(
            web_security_scanner.DeleteScanConfigRequest(), name="name_value",
        )


def test_get_scan_config(
    transport: str = "grpc", request_type=web_security_scanner.GetScanConfigRequest
):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_scan_config), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = scan_config.ScanConfig(
            name="name_value",
            display_name="display_name_value",
            max_qps=761,
            starting_urls=["starting_urls_value"],
            user_agent=scan_config.ScanConfig.UserAgent.CHROME_LINUX,
            blacklist_patterns=["blacklist_patterns_value"],
            target_platforms=[scan_config.ScanConfig.TargetPlatform.APP_ENGINE],
            export_to_security_command_center=scan_config.ScanConfig.ExportToSecurityCommandCenter.ENABLED,
            risk_level=scan_config.ScanConfig.RiskLevel.NORMAL,
        )
        response = client.get_scan_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.GetScanConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, scan_config.ScanConfig)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.max_qps == 761
    assert response.starting_urls == ["starting_urls_value"]
    assert response.user_agent == scan_config.ScanConfig.UserAgent.CHROME_LINUX
    assert response.blacklist_patterns == ["blacklist_patterns_value"]
    assert response.target_platforms == [
        scan_config.ScanConfig.TargetPlatform.APP_ENGINE
    ]
    assert (
        response.export_to_security_command_center
        == scan_config.ScanConfig.ExportToSecurityCommandCenter.ENABLED
    )
    assert response.risk_level == scan_config.ScanConfig.RiskLevel.NORMAL


def test_get_scan_config_from_dict():
    test_get_scan_config(request_type=dict)


def test_get_scan_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_scan_config), "__call__") as call:
        client.get_scan_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.GetScanConfigRequest()


@pytest.mark.asyncio
async def test_get_scan_config_async(
    transport: str = "grpc_asyncio",
    request_type=web_security_scanner.GetScanConfigRequest,
):
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_scan_config), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            scan_config.ScanConfig(
                name="name_value",
                display_name="display_name_value",
                max_qps=761,
                starting_urls=["starting_urls_value"],
                user_agent=scan_config.ScanConfig.UserAgent.CHROME_LINUX,
                blacklist_patterns=["blacklist_patterns_value"],
                target_platforms=[scan_config.ScanConfig.TargetPlatform.APP_ENGINE],
                export_to_security_command_center=scan_config.ScanConfig.ExportToSecurityCommandCenter.ENABLED,
                risk_level=scan_config.ScanConfig.RiskLevel.NORMAL,
            )
        )
        response = await client.get_scan_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.GetScanConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, scan_config.ScanConfig)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.max_qps == 761
    assert response.starting_urls == ["starting_urls_value"]
    assert response.user_agent == scan_config.ScanConfig.UserAgent.CHROME_LINUX
    assert response.blacklist_patterns == ["blacklist_patterns_value"]
    assert response.target_platforms == [
        scan_config.ScanConfig.TargetPlatform.APP_ENGINE
    ]
    assert (
        response.export_to_security_command_center
        == scan_config.ScanConfig.ExportToSecurityCommandCenter.ENABLED
    )
    assert response.risk_level == scan_config.ScanConfig.RiskLevel.NORMAL


@pytest.mark.asyncio
async def test_get_scan_config_async_from_dict():
    await test_get_scan_config_async(request_type=dict)


def test_get_scan_config_field_headers():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.GetScanConfigRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_scan_config), "__call__") as call:
        call.return_value = scan_config.ScanConfig()
        client.get_scan_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_scan_config_field_headers_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.GetScanConfigRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_scan_config), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            scan_config.ScanConfig()
        )
        await client.get_scan_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_scan_config_flattened():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_scan_config), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = scan_config.ScanConfig()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_scan_config(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_scan_config_flattened_error():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_scan_config(
            web_security_scanner.GetScanConfigRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_scan_config_flattened_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_scan_config), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = scan_config.ScanConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            scan_config.ScanConfig()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_scan_config(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_scan_config_flattened_error_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_scan_config(
            web_security_scanner.GetScanConfigRequest(), name="name_value",
        )


def test_list_scan_configs(
    transport: str = "grpc", request_type=web_security_scanner.ListScanConfigsRequest
):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_scan_configs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = web_security_scanner.ListScanConfigsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_scan_configs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.ListScanConfigsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListScanConfigsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_scan_configs_from_dict():
    test_list_scan_configs(request_type=dict)


def test_list_scan_configs_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_scan_configs), "__call__"
    ) as call:
        client.list_scan_configs()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.ListScanConfigsRequest()


@pytest.mark.asyncio
async def test_list_scan_configs_async(
    transport: str = "grpc_asyncio",
    request_type=web_security_scanner.ListScanConfigsRequest,
):
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_scan_configs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            web_security_scanner.ListScanConfigsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_scan_configs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.ListScanConfigsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListScanConfigsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_scan_configs_async_from_dict():
    await test_list_scan_configs_async(request_type=dict)


def test_list_scan_configs_field_headers():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.ListScanConfigsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_scan_configs), "__call__"
    ) as call:
        call.return_value = web_security_scanner.ListScanConfigsResponse()
        client.list_scan_configs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_scan_configs_field_headers_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.ListScanConfigsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_scan_configs), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            web_security_scanner.ListScanConfigsResponse()
        )
        await client.list_scan_configs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_scan_configs_flattened():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_scan_configs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = web_security_scanner.ListScanConfigsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_scan_configs(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_scan_configs_flattened_error():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_scan_configs(
            web_security_scanner.ListScanConfigsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_scan_configs_flattened_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_scan_configs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = web_security_scanner.ListScanConfigsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            web_security_scanner.ListScanConfigsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_scan_configs(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_scan_configs_flattened_error_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_scan_configs(
            web_security_scanner.ListScanConfigsRequest(), parent="parent_value",
        )


def test_list_scan_configs_pager():
    client = WebSecurityScannerClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_scan_configs), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            web_security_scanner.ListScanConfigsResponse(
                scan_configs=[
                    scan_config.ScanConfig(),
                    scan_config.ScanConfig(),
                    scan_config.ScanConfig(),
                ],
                next_page_token="abc",
            ),
            web_security_scanner.ListScanConfigsResponse(
                scan_configs=[], next_page_token="def",
            ),
            web_security_scanner.ListScanConfigsResponse(
                scan_configs=[scan_config.ScanConfig(),], next_page_token="ghi",
            ),
            web_security_scanner.ListScanConfigsResponse(
                scan_configs=[scan_config.ScanConfig(), scan_config.ScanConfig(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_scan_configs(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, scan_config.ScanConfig) for i in results)


def test_list_scan_configs_pages():
    client = WebSecurityScannerClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_scan_configs), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            web_security_scanner.ListScanConfigsResponse(
                scan_configs=[
                    scan_config.ScanConfig(),
                    scan_config.ScanConfig(),
                    scan_config.ScanConfig(),
                ],
                next_page_token="abc",
            ),
            web_security_scanner.ListScanConfigsResponse(
                scan_configs=[], next_page_token="def",
            ),
            web_security_scanner.ListScanConfigsResponse(
                scan_configs=[scan_config.ScanConfig(),], next_page_token="ghi",
            ),
            web_security_scanner.ListScanConfigsResponse(
                scan_configs=[scan_config.ScanConfig(), scan_config.ScanConfig(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_scan_configs(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_scan_configs_async_pager():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_scan_configs),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            web_security_scanner.ListScanConfigsResponse(
                scan_configs=[
                    scan_config.ScanConfig(),
                    scan_config.ScanConfig(),
                    scan_config.ScanConfig(),
                ],
                next_page_token="abc",
            ),
            web_security_scanner.ListScanConfigsResponse(
                scan_configs=[], next_page_token="def",
            ),
            web_security_scanner.ListScanConfigsResponse(
                scan_configs=[scan_config.ScanConfig(),], next_page_token="ghi",
            ),
            web_security_scanner.ListScanConfigsResponse(
                scan_configs=[scan_config.ScanConfig(), scan_config.ScanConfig(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_scan_configs(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, scan_config.ScanConfig) for i in responses)


@pytest.mark.asyncio
async def test_list_scan_configs_async_pages():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_scan_configs),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            web_security_scanner.ListScanConfigsResponse(
                scan_configs=[
                    scan_config.ScanConfig(),
                    scan_config.ScanConfig(),
                    scan_config.ScanConfig(),
                ],
                next_page_token="abc",
            ),
            web_security_scanner.ListScanConfigsResponse(
                scan_configs=[], next_page_token="def",
            ),
            web_security_scanner.ListScanConfigsResponse(
                scan_configs=[scan_config.ScanConfig(),], next_page_token="ghi",
            ),
            web_security_scanner.ListScanConfigsResponse(
                scan_configs=[scan_config.ScanConfig(), scan_config.ScanConfig(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_scan_configs(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_update_scan_config(
    transport: str = "grpc", request_type=web_security_scanner.UpdateScanConfigRequest
):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_scan_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcw_scan_config.ScanConfig(
            name="name_value",
            display_name="display_name_value",
            max_qps=761,
            starting_urls=["starting_urls_value"],
            user_agent=gcw_scan_config.ScanConfig.UserAgent.CHROME_LINUX,
            blacklist_patterns=["blacklist_patterns_value"],
            target_platforms=[gcw_scan_config.ScanConfig.TargetPlatform.APP_ENGINE],
            export_to_security_command_center=gcw_scan_config.ScanConfig.ExportToSecurityCommandCenter.ENABLED,
            risk_level=gcw_scan_config.ScanConfig.RiskLevel.NORMAL,
        )
        response = client.update_scan_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.UpdateScanConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcw_scan_config.ScanConfig)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.max_qps == 761
    assert response.starting_urls == ["starting_urls_value"]
    assert response.user_agent == gcw_scan_config.ScanConfig.UserAgent.CHROME_LINUX
    assert response.blacklist_patterns == ["blacklist_patterns_value"]
    assert response.target_platforms == [
        gcw_scan_config.ScanConfig.TargetPlatform.APP_ENGINE
    ]
    assert (
        response.export_to_security_command_center
        == gcw_scan_config.ScanConfig.ExportToSecurityCommandCenter.ENABLED
    )
    assert response.risk_level == gcw_scan_config.ScanConfig.RiskLevel.NORMAL


def test_update_scan_config_from_dict():
    test_update_scan_config(request_type=dict)


def test_update_scan_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_scan_config), "__call__"
    ) as call:
        client.update_scan_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.UpdateScanConfigRequest()


@pytest.mark.asyncio
async def test_update_scan_config_async(
    transport: str = "grpc_asyncio",
    request_type=web_security_scanner.UpdateScanConfigRequest,
):
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_scan_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcw_scan_config.ScanConfig(
                name="name_value",
                display_name="display_name_value",
                max_qps=761,
                starting_urls=["starting_urls_value"],
                user_agent=gcw_scan_config.ScanConfig.UserAgent.CHROME_LINUX,
                blacklist_patterns=["blacklist_patterns_value"],
                target_platforms=[gcw_scan_config.ScanConfig.TargetPlatform.APP_ENGINE],
                export_to_security_command_center=gcw_scan_config.ScanConfig.ExportToSecurityCommandCenter.ENABLED,
                risk_level=gcw_scan_config.ScanConfig.RiskLevel.NORMAL,
            )
        )
        response = await client.update_scan_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.UpdateScanConfigRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcw_scan_config.ScanConfig)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.max_qps == 761
    assert response.starting_urls == ["starting_urls_value"]
    assert response.user_agent == gcw_scan_config.ScanConfig.UserAgent.CHROME_LINUX
    assert response.blacklist_patterns == ["blacklist_patterns_value"]
    assert response.target_platforms == [
        gcw_scan_config.ScanConfig.TargetPlatform.APP_ENGINE
    ]
    assert (
        response.export_to_security_command_center
        == gcw_scan_config.ScanConfig.ExportToSecurityCommandCenter.ENABLED
    )
    assert response.risk_level == gcw_scan_config.ScanConfig.RiskLevel.NORMAL


@pytest.mark.asyncio
async def test_update_scan_config_async_from_dict():
    await test_update_scan_config_async(request_type=dict)


def test_update_scan_config_field_headers():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.UpdateScanConfigRequest()

    request.scan_config.name = "scan_config.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_scan_config), "__call__"
    ) as call:
        call.return_value = gcw_scan_config.ScanConfig()
        client.update_scan_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "scan_config.name=scan_config.name/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_update_scan_config_field_headers_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.UpdateScanConfigRequest()

    request.scan_config.name = "scan_config.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_scan_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcw_scan_config.ScanConfig()
        )
        await client.update_scan_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "scan_config.name=scan_config.name/value",) in kw[
        "metadata"
    ]


def test_update_scan_config_flattened():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_scan_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcw_scan_config.ScanConfig()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_scan_config(
            scan_config=gcw_scan_config.ScanConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].scan_config == gcw_scan_config.ScanConfig(name="name_value")
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


def test_update_scan_config_flattened_error():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_scan_config(
            web_security_scanner.UpdateScanConfigRequest(),
            scan_config=gcw_scan_config.ScanConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_scan_config_flattened_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_scan_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcw_scan_config.ScanConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcw_scan_config.ScanConfig()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_scan_config(
            scan_config=gcw_scan_config.ScanConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].scan_config == gcw_scan_config.ScanConfig(name="name_value")
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_scan_config_flattened_error_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_scan_config(
            web_security_scanner.UpdateScanConfigRequest(),
            scan_config=gcw_scan_config.ScanConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_start_scan_run(
    transport: str = "grpc", request_type=web_security_scanner.StartScanRunRequest
):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.start_scan_run), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = scan_run.ScanRun(
            name="name_value",
            execution_state=scan_run.ScanRun.ExecutionState.QUEUED,
            result_state=scan_run.ScanRun.ResultState.SUCCESS,
            urls_crawled_count=1935,
            urls_tested_count=1846,
            has_vulnerabilities=True,
            progress_percent=1733,
        )
        response = client.start_scan_run(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.StartScanRunRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, scan_run.ScanRun)
    assert response.name == "name_value"
    assert response.execution_state == scan_run.ScanRun.ExecutionState.QUEUED
    assert response.result_state == scan_run.ScanRun.ResultState.SUCCESS
    assert response.urls_crawled_count == 1935
    assert response.urls_tested_count == 1846
    assert response.has_vulnerabilities is True
    assert response.progress_percent == 1733


def test_start_scan_run_from_dict():
    test_start_scan_run(request_type=dict)


def test_start_scan_run_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.start_scan_run), "__call__") as call:
        client.start_scan_run()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.StartScanRunRequest()


@pytest.mark.asyncio
async def test_start_scan_run_async(
    transport: str = "grpc_asyncio",
    request_type=web_security_scanner.StartScanRunRequest,
):
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.start_scan_run), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            scan_run.ScanRun(
                name="name_value",
                execution_state=scan_run.ScanRun.ExecutionState.QUEUED,
                result_state=scan_run.ScanRun.ResultState.SUCCESS,
                urls_crawled_count=1935,
                urls_tested_count=1846,
                has_vulnerabilities=True,
                progress_percent=1733,
            )
        )
        response = await client.start_scan_run(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.StartScanRunRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, scan_run.ScanRun)
    assert response.name == "name_value"
    assert response.execution_state == scan_run.ScanRun.ExecutionState.QUEUED
    assert response.result_state == scan_run.ScanRun.ResultState.SUCCESS
    assert response.urls_crawled_count == 1935
    assert response.urls_tested_count == 1846
    assert response.has_vulnerabilities is True
    assert response.progress_percent == 1733


@pytest.mark.asyncio
async def test_start_scan_run_async_from_dict():
    await test_start_scan_run_async(request_type=dict)


def test_start_scan_run_field_headers():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.StartScanRunRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.start_scan_run), "__call__") as call:
        call.return_value = scan_run.ScanRun()
        client.start_scan_run(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_start_scan_run_field_headers_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.StartScanRunRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.start_scan_run), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(scan_run.ScanRun())
        await client.start_scan_run(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_start_scan_run_flattened():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.start_scan_run), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = scan_run.ScanRun()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.start_scan_run(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_start_scan_run_flattened_error():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.start_scan_run(
            web_security_scanner.StartScanRunRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_start_scan_run_flattened_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.start_scan_run), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = scan_run.ScanRun()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(scan_run.ScanRun())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.start_scan_run(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_start_scan_run_flattened_error_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.start_scan_run(
            web_security_scanner.StartScanRunRequest(), name="name_value",
        )


def test_get_scan_run(
    transport: str = "grpc", request_type=web_security_scanner.GetScanRunRequest
):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_scan_run), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = scan_run.ScanRun(
            name="name_value",
            execution_state=scan_run.ScanRun.ExecutionState.QUEUED,
            result_state=scan_run.ScanRun.ResultState.SUCCESS,
            urls_crawled_count=1935,
            urls_tested_count=1846,
            has_vulnerabilities=True,
            progress_percent=1733,
        )
        response = client.get_scan_run(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.GetScanRunRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, scan_run.ScanRun)
    assert response.name == "name_value"
    assert response.execution_state == scan_run.ScanRun.ExecutionState.QUEUED
    assert response.result_state == scan_run.ScanRun.ResultState.SUCCESS
    assert response.urls_crawled_count == 1935
    assert response.urls_tested_count == 1846
    assert response.has_vulnerabilities is True
    assert response.progress_percent == 1733


def test_get_scan_run_from_dict():
    test_get_scan_run(request_type=dict)


def test_get_scan_run_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_scan_run), "__call__") as call:
        client.get_scan_run()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.GetScanRunRequest()


@pytest.mark.asyncio
async def test_get_scan_run_async(
    transport: str = "grpc_asyncio", request_type=web_security_scanner.GetScanRunRequest
):
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_scan_run), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            scan_run.ScanRun(
                name="name_value",
                execution_state=scan_run.ScanRun.ExecutionState.QUEUED,
                result_state=scan_run.ScanRun.ResultState.SUCCESS,
                urls_crawled_count=1935,
                urls_tested_count=1846,
                has_vulnerabilities=True,
                progress_percent=1733,
            )
        )
        response = await client.get_scan_run(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.GetScanRunRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, scan_run.ScanRun)
    assert response.name == "name_value"
    assert response.execution_state == scan_run.ScanRun.ExecutionState.QUEUED
    assert response.result_state == scan_run.ScanRun.ResultState.SUCCESS
    assert response.urls_crawled_count == 1935
    assert response.urls_tested_count == 1846
    assert response.has_vulnerabilities is True
    assert response.progress_percent == 1733


@pytest.mark.asyncio
async def test_get_scan_run_async_from_dict():
    await test_get_scan_run_async(request_type=dict)


def test_get_scan_run_field_headers():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.GetScanRunRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_scan_run), "__call__") as call:
        call.return_value = scan_run.ScanRun()
        client.get_scan_run(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_scan_run_field_headers_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.GetScanRunRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_scan_run), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(scan_run.ScanRun())
        await client.get_scan_run(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_scan_run_flattened():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_scan_run), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = scan_run.ScanRun()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_scan_run(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_scan_run_flattened_error():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_scan_run(
            web_security_scanner.GetScanRunRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_scan_run_flattened_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_scan_run), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = scan_run.ScanRun()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(scan_run.ScanRun())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_scan_run(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_scan_run_flattened_error_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_scan_run(
            web_security_scanner.GetScanRunRequest(), name="name_value",
        )


def test_list_scan_runs(
    transport: str = "grpc", request_type=web_security_scanner.ListScanRunsRequest
):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_scan_runs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = web_security_scanner.ListScanRunsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_scan_runs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.ListScanRunsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListScanRunsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_scan_runs_from_dict():
    test_list_scan_runs(request_type=dict)


def test_list_scan_runs_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_scan_runs), "__call__") as call:
        client.list_scan_runs()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.ListScanRunsRequest()


@pytest.mark.asyncio
async def test_list_scan_runs_async(
    transport: str = "grpc_asyncio",
    request_type=web_security_scanner.ListScanRunsRequest,
):
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_scan_runs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            web_security_scanner.ListScanRunsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_scan_runs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.ListScanRunsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListScanRunsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_scan_runs_async_from_dict():
    await test_list_scan_runs_async(request_type=dict)


def test_list_scan_runs_field_headers():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.ListScanRunsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_scan_runs), "__call__") as call:
        call.return_value = web_security_scanner.ListScanRunsResponse()
        client.list_scan_runs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_scan_runs_field_headers_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.ListScanRunsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_scan_runs), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            web_security_scanner.ListScanRunsResponse()
        )
        await client.list_scan_runs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_scan_runs_flattened():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_scan_runs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = web_security_scanner.ListScanRunsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_scan_runs(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_scan_runs_flattened_error():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_scan_runs(
            web_security_scanner.ListScanRunsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_scan_runs_flattened_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_scan_runs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = web_security_scanner.ListScanRunsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            web_security_scanner.ListScanRunsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_scan_runs(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_scan_runs_flattened_error_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_scan_runs(
            web_security_scanner.ListScanRunsRequest(), parent="parent_value",
        )


def test_list_scan_runs_pager():
    client = WebSecurityScannerClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_scan_runs), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            web_security_scanner.ListScanRunsResponse(
                scan_runs=[scan_run.ScanRun(), scan_run.ScanRun(), scan_run.ScanRun(),],
                next_page_token="abc",
            ),
            web_security_scanner.ListScanRunsResponse(
                scan_runs=[], next_page_token="def",
            ),
            web_security_scanner.ListScanRunsResponse(
                scan_runs=[scan_run.ScanRun(),], next_page_token="ghi",
            ),
            web_security_scanner.ListScanRunsResponse(
                scan_runs=[scan_run.ScanRun(), scan_run.ScanRun(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_scan_runs(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, scan_run.ScanRun) for i in results)


def test_list_scan_runs_pages():
    client = WebSecurityScannerClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_scan_runs), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            web_security_scanner.ListScanRunsResponse(
                scan_runs=[scan_run.ScanRun(), scan_run.ScanRun(), scan_run.ScanRun(),],
                next_page_token="abc",
            ),
            web_security_scanner.ListScanRunsResponse(
                scan_runs=[], next_page_token="def",
            ),
            web_security_scanner.ListScanRunsResponse(
                scan_runs=[scan_run.ScanRun(),], next_page_token="ghi",
            ),
            web_security_scanner.ListScanRunsResponse(
                scan_runs=[scan_run.ScanRun(), scan_run.ScanRun(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_scan_runs(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_scan_runs_async_pager():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_scan_runs), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            web_security_scanner.ListScanRunsResponse(
                scan_runs=[scan_run.ScanRun(), scan_run.ScanRun(), scan_run.ScanRun(),],
                next_page_token="abc",
            ),
            web_security_scanner.ListScanRunsResponse(
                scan_runs=[], next_page_token="def",
            ),
            web_security_scanner.ListScanRunsResponse(
                scan_runs=[scan_run.ScanRun(),], next_page_token="ghi",
            ),
            web_security_scanner.ListScanRunsResponse(
                scan_runs=[scan_run.ScanRun(), scan_run.ScanRun(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_scan_runs(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, scan_run.ScanRun) for i in responses)


@pytest.mark.asyncio
async def test_list_scan_runs_async_pages():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_scan_runs), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            web_security_scanner.ListScanRunsResponse(
                scan_runs=[scan_run.ScanRun(), scan_run.ScanRun(), scan_run.ScanRun(),],
                next_page_token="abc",
            ),
            web_security_scanner.ListScanRunsResponse(
                scan_runs=[], next_page_token="def",
            ),
            web_security_scanner.ListScanRunsResponse(
                scan_runs=[scan_run.ScanRun(),], next_page_token="ghi",
            ),
            web_security_scanner.ListScanRunsResponse(
                scan_runs=[scan_run.ScanRun(), scan_run.ScanRun(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_scan_runs(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_stop_scan_run(
    transport: str = "grpc", request_type=web_security_scanner.StopScanRunRequest
):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.stop_scan_run), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = scan_run.ScanRun(
            name="name_value",
            execution_state=scan_run.ScanRun.ExecutionState.QUEUED,
            result_state=scan_run.ScanRun.ResultState.SUCCESS,
            urls_crawled_count=1935,
            urls_tested_count=1846,
            has_vulnerabilities=True,
            progress_percent=1733,
        )
        response = client.stop_scan_run(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.StopScanRunRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, scan_run.ScanRun)
    assert response.name == "name_value"
    assert response.execution_state == scan_run.ScanRun.ExecutionState.QUEUED
    assert response.result_state == scan_run.ScanRun.ResultState.SUCCESS
    assert response.urls_crawled_count == 1935
    assert response.urls_tested_count == 1846
    assert response.has_vulnerabilities is True
    assert response.progress_percent == 1733


def test_stop_scan_run_from_dict():
    test_stop_scan_run(request_type=dict)


def test_stop_scan_run_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.stop_scan_run), "__call__") as call:
        client.stop_scan_run()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.StopScanRunRequest()


@pytest.mark.asyncio
async def test_stop_scan_run_async(
    transport: str = "grpc_asyncio",
    request_type=web_security_scanner.StopScanRunRequest,
):
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.stop_scan_run), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            scan_run.ScanRun(
                name="name_value",
                execution_state=scan_run.ScanRun.ExecutionState.QUEUED,
                result_state=scan_run.ScanRun.ResultState.SUCCESS,
                urls_crawled_count=1935,
                urls_tested_count=1846,
                has_vulnerabilities=True,
                progress_percent=1733,
            )
        )
        response = await client.stop_scan_run(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.StopScanRunRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, scan_run.ScanRun)
    assert response.name == "name_value"
    assert response.execution_state == scan_run.ScanRun.ExecutionState.QUEUED
    assert response.result_state == scan_run.ScanRun.ResultState.SUCCESS
    assert response.urls_crawled_count == 1935
    assert response.urls_tested_count == 1846
    assert response.has_vulnerabilities is True
    assert response.progress_percent == 1733


@pytest.mark.asyncio
async def test_stop_scan_run_async_from_dict():
    await test_stop_scan_run_async(request_type=dict)


def test_stop_scan_run_field_headers():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.StopScanRunRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.stop_scan_run), "__call__") as call:
        call.return_value = scan_run.ScanRun()
        client.stop_scan_run(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_stop_scan_run_field_headers_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.StopScanRunRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.stop_scan_run), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(scan_run.ScanRun())
        await client.stop_scan_run(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_stop_scan_run_flattened():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.stop_scan_run), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = scan_run.ScanRun()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.stop_scan_run(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_stop_scan_run_flattened_error():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.stop_scan_run(
            web_security_scanner.StopScanRunRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_stop_scan_run_flattened_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.stop_scan_run), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = scan_run.ScanRun()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(scan_run.ScanRun())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.stop_scan_run(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_stop_scan_run_flattened_error_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.stop_scan_run(
            web_security_scanner.StopScanRunRequest(), name="name_value",
        )


def test_list_crawled_urls(
    transport: str = "grpc", request_type=web_security_scanner.ListCrawledUrlsRequest
):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_crawled_urls), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = web_security_scanner.ListCrawledUrlsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_crawled_urls(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.ListCrawledUrlsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCrawledUrlsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_crawled_urls_from_dict():
    test_list_crawled_urls(request_type=dict)


def test_list_crawled_urls_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_crawled_urls), "__call__"
    ) as call:
        client.list_crawled_urls()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.ListCrawledUrlsRequest()


@pytest.mark.asyncio
async def test_list_crawled_urls_async(
    transport: str = "grpc_asyncio",
    request_type=web_security_scanner.ListCrawledUrlsRequest,
):
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_crawled_urls), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            web_security_scanner.ListCrawledUrlsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_crawled_urls(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.ListCrawledUrlsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCrawledUrlsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_crawled_urls_async_from_dict():
    await test_list_crawled_urls_async(request_type=dict)


def test_list_crawled_urls_field_headers():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.ListCrawledUrlsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_crawled_urls), "__call__"
    ) as call:
        call.return_value = web_security_scanner.ListCrawledUrlsResponse()
        client.list_crawled_urls(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_crawled_urls_field_headers_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.ListCrawledUrlsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_crawled_urls), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            web_security_scanner.ListCrawledUrlsResponse()
        )
        await client.list_crawled_urls(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_crawled_urls_flattened():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_crawled_urls), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = web_security_scanner.ListCrawledUrlsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_crawled_urls(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_crawled_urls_flattened_error():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_crawled_urls(
            web_security_scanner.ListCrawledUrlsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_crawled_urls_flattened_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_crawled_urls), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = web_security_scanner.ListCrawledUrlsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            web_security_scanner.ListCrawledUrlsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_crawled_urls(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_crawled_urls_flattened_error_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_crawled_urls(
            web_security_scanner.ListCrawledUrlsRequest(), parent="parent_value",
        )


def test_list_crawled_urls_pager():
    client = WebSecurityScannerClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_crawled_urls), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            web_security_scanner.ListCrawledUrlsResponse(
                crawled_urls=[
                    crawled_url.CrawledUrl(),
                    crawled_url.CrawledUrl(),
                    crawled_url.CrawledUrl(),
                ],
                next_page_token="abc",
            ),
            web_security_scanner.ListCrawledUrlsResponse(
                crawled_urls=[], next_page_token="def",
            ),
            web_security_scanner.ListCrawledUrlsResponse(
                crawled_urls=[crawled_url.CrawledUrl(),], next_page_token="ghi",
            ),
            web_security_scanner.ListCrawledUrlsResponse(
                crawled_urls=[crawled_url.CrawledUrl(), crawled_url.CrawledUrl(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_crawled_urls(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, crawled_url.CrawledUrl) for i in results)


def test_list_crawled_urls_pages():
    client = WebSecurityScannerClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_crawled_urls), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            web_security_scanner.ListCrawledUrlsResponse(
                crawled_urls=[
                    crawled_url.CrawledUrl(),
                    crawled_url.CrawledUrl(),
                    crawled_url.CrawledUrl(),
                ],
                next_page_token="abc",
            ),
            web_security_scanner.ListCrawledUrlsResponse(
                crawled_urls=[], next_page_token="def",
            ),
            web_security_scanner.ListCrawledUrlsResponse(
                crawled_urls=[crawled_url.CrawledUrl(),], next_page_token="ghi",
            ),
            web_security_scanner.ListCrawledUrlsResponse(
                crawled_urls=[crawled_url.CrawledUrl(), crawled_url.CrawledUrl(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_crawled_urls(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_crawled_urls_async_pager():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_crawled_urls),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            web_security_scanner.ListCrawledUrlsResponse(
                crawled_urls=[
                    crawled_url.CrawledUrl(),
                    crawled_url.CrawledUrl(),
                    crawled_url.CrawledUrl(),
                ],
                next_page_token="abc",
            ),
            web_security_scanner.ListCrawledUrlsResponse(
                crawled_urls=[], next_page_token="def",
            ),
            web_security_scanner.ListCrawledUrlsResponse(
                crawled_urls=[crawled_url.CrawledUrl(),], next_page_token="ghi",
            ),
            web_security_scanner.ListCrawledUrlsResponse(
                crawled_urls=[crawled_url.CrawledUrl(), crawled_url.CrawledUrl(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_crawled_urls(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, crawled_url.CrawledUrl) for i in responses)


@pytest.mark.asyncio
async def test_list_crawled_urls_async_pages():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_crawled_urls),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            web_security_scanner.ListCrawledUrlsResponse(
                crawled_urls=[
                    crawled_url.CrawledUrl(),
                    crawled_url.CrawledUrl(),
                    crawled_url.CrawledUrl(),
                ],
                next_page_token="abc",
            ),
            web_security_scanner.ListCrawledUrlsResponse(
                crawled_urls=[], next_page_token="def",
            ),
            web_security_scanner.ListCrawledUrlsResponse(
                crawled_urls=[crawled_url.CrawledUrl(),], next_page_token="ghi",
            ),
            web_security_scanner.ListCrawledUrlsResponse(
                crawled_urls=[crawled_url.CrawledUrl(), crawled_url.CrawledUrl(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_crawled_urls(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_finding(
    transport: str = "grpc", request_type=web_security_scanner.GetFindingRequest
):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_finding), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = finding.Finding(
            name="name_value",
            finding_type="finding_type_value",
            http_method="http_method_value",
            fuzzed_url="fuzzed_url_value",
            body="body_value",
            description="description_value",
            reproduction_url="reproduction_url_value",
            frame_url="frame_url_value",
            final_url="final_url_value",
            tracking_id="tracking_id_value",
        )
        response = client.get_finding(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.GetFindingRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, finding.Finding)
    assert response.name == "name_value"
    assert response.finding_type == "finding_type_value"
    assert response.http_method == "http_method_value"
    assert response.fuzzed_url == "fuzzed_url_value"
    assert response.body == "body_value"
    assert response.description == "description_value"
    assert response.reproduction_url == "reproduction_url_value"
    assert response.frame_url == "frame_url_value"
    assert response.final_url == "final_url_value"
    assert response.tracking_id == "tracking_id_value"


def test_get_finding_from_dict():
    test_get_finding(request_type=dict)


def test_get_finding_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_finding), "__call__") as call:
        client.get_finding()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.GetFindingRequest()


@pytest.mark.asyncio
async def test_get_finding_async(
    transport: str = "grpc_asyncio", request_type=web_security_scanner.GetFindingRequest
):
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_finding), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            finding.Finding(
                name="name_value",
                finding_type="finding_type_value",
                http_method="http_method_value",
                fuzzed_url="fuzzed_url_value",
                body="body_value",
                description="description_value",
                reproduction_url="reproduction_url_value",
                frame_url="frame_url_value",
                final_url="final_url_value",
                tracking_id="tracking_id_value",
            )
        )
        response = await client.get_finding(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.GetFindingRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, finding.Finding)
    assert response.name == "name_value"
    assert response.finding_type == "finding_type_value"
    assert response.http_method == "http_method_value"
    assert response.fuzzed_url == "fuzzed_url_value"
    assert response.body == "body_value"
    assert response.description == "description_value"
    assert response.reproduction_url == "reproduction_url_value"
    assert response.frame_url == "frame_url_value"
    assert response.final_url == "final_url_value"
    assert response.tracking_id == "tracking_id_value"


@pytest.mark.asyncio
async def test_get_finding_async_from_dict():
    await test_get_finding_async(request_type=dict)


def test_get_finding_field_headers():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.GetFindingRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_finding), "__call__") as call:
        call.return_value = finding.Finding()
        client.get_finding(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_finding_field_headers_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.GetFindingRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_finding), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(finding.Finding())
        await client.get_finding(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_finding_flattened():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_finding), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = finding.Finding()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_finding(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_finding_flattened_error():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_finding(
            web_security_scanner.GetFindingRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_finding_flattened_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_finding), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = finding.Finding()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(finding.Finding())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_finding(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_finding_flattened_error_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_finding(
            web_security_scanner.GetFindingRequest(), name="name_value",
        )


def test_list_findings(
    transport: str = "grpc", request_type=web_security_scanner.ListFindingsRequest
):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_findings), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = web_security_scanner.ListFindingsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_findings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.ListFindingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListFindingsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_findings_from_dict():
    test_list_findings(request_type=dict)


def test_list_findings_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_findings), "__call__") as call:
        client.list_findings()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.ListFindingsRequest()


@pytest.mark.asyncio
async def test_list_findings_async(
    transport: str = "grpc_asyncio",
    request_type=web_security_scanner.ListFindingsRequest,
):
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_findings), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            web_security_scanner.ListFindingsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_findings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.ListFindingsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListFindingsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_findings_async_from_dict():
    await test_list_findings_async(request_type=dict)


def test_list_findings_field_headers():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.ListFindingsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_findings), "__call__") as call:
        call.return_value = web_security_scanner.ListFindingsResponse()
        client.list_findings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_findings_field_headers_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.ListFindingsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_findings), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            web_security_scanner.ListFindingsResponse()
        )
        await client.list_findings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_findings_flattened():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_findings), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = web_security_scanner.ListFindingsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_findings(
            parent="parent_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].filter == "filter_value"


def test_list_findings_flattened_error():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_findings(
            web_security_scanner.ListFindingsRequest(),
            parent="parent_value",
            filter="filter_value",
        )


@pytest.mark.asyncio
async def test_list_findings_flattened_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_findings), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = web_security_scanner.ListFindingsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            web_security_scanner.ListFindingsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_findings(
            parent="parent_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].filter == "filter_value"


@pytest.mark.asyncio
async def test_list_findings_flattened_error_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_findings(
            web_security_scanner.ListFindingsRequest(),
            parent="parent_value",
            filter="filter_value",
        )


def test_list_findings_pager():
    client = WebSecurityScannerClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_findings), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            web_security_scanner.ListFindingsResponse(
                findings=[finding.Finding(), finding.Finding(), finding.Finding(),],
                next_page_token="abc",
            ),
            web_security_scanner.ListFindingsResponse(
                findings=[], next_page_token="def",
            ),
            web_security_scanner.ListFindingsResponse(
                findings=[finding.Finding(),], next_page_token="ghi",
            ),
            web_security_scanner.ListFindingsResponse(
                findings=[finding.Finding(), finding.Finding(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_findings(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, finding.Finding) for i in results)


def test_list_findings_pages():
    client = WebSecurityScannerClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_findings), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            web_security_scanner.ListFindingsResponse(
                findings=[finding.Finding(), finding.Finding(), finding.Finding(),],
                next_page_token="abc",
            ),
            web_security_scanner.ListFindingsResponse(
                findings=[], next_page_token="def",
            ),
            web_security_scanner.ListFindingsResponse(
                findings=[finding.Finding(),], next_page_token="ghi",
            ),
            web_security_scanner.ListFindingsResponse(
                findings=[finding.Finding(), finding.Finding(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_findings(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_findings_async_pager():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_findings), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            web_security_scanner.ListFindingsResponse(
                findings=[finding.Finding(), finding.Finding(), finding.Finding(),],
                next_page_token="abc",
            ),
            web_security_scanner.ListFindingsResponse(
                findings=[], next_page_token="def",
            ),
            web_security_scanner.ListFindingsResponse(
                findings=[finding.Finding(),], next_page_token="ghi",
            ),
            web_security_scanner.ListFindingsResponse(
                findings=[finding.Finding(), finding.Finding(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_findings(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, finding.Finding) for i in responses)


@pytest.mark.asyncio
async def test_list_findings_async_pages():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_findings), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            web_security_scanner.ListFindingsResponse(
                findings=[finding.Finding(), finding.Finding(), finding.Finding(),],
                next_page_token="abc",
            ),
            web_security_scanner.ListFindingsResponse(
                findings=[], next_page_token="def",
            ),
            web_security_scanner.ListFindingsResponse(
                findings=[finding.Finding(),], next_page_token="ghi",
            ),
            web_security_scanner.ListFindingsResponse(
                findings=[finding.Finding(), finding.Finding(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_findings(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_list_finding_type_stats(
    transport: str = "grpc",
    request_type=web_security_scanner.ListFindingTypeStatsRequest,
):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_finding_type_stats), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = web_security_scanner.ListFindingTypeStatsResponse()
        response = client.list_finding_type_stats(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.ListFindingTypeStatsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, web_security_scanner.ListFindingTypeStatsResponse)


def test_list_finding_type_stats_from_dict():
    test_list_finding_type_stats(request_type=dict)


def test_list_finding_type_stats_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_finding_type_stats), "__call__"
    ) as call:
        client.list_finding_type_stats()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.ListFindingTypeStatsRequest()


@pytest.mark.asyncio
async def test_list_finding_type_stats_async(
    transport: str = "grpc_asyncio",
    request_type=web_security_scanner.ListFindingTypeStatsRequest,
):
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_finding_type_stats), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            web_security_scanner.ListFindingTypeStatsResponse()
        )
        response = await client.list_finding_type_stats(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == web_security_scanner.ListFindingTypeStatsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, web_security_scanner.ListFindingTypeStatsResponse)


@pytest.mark.asyncio
async def test_list_finding_type_stats_async_from_dict():
    await test_list_finding_type_stats_async(request_type=dict)


def test_list_finding_type_stats_field_headers():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.ListFindingTypeStatsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_finding_type_stats), "__call__"
    ) as call:
        call.return_value = web_security_scanner.ListFindingTypeStatsResponse()
        client.list_finding_type_stats(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_finding_type_stats_field_headers_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.ListFindingTypeStatsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_finding_type_stats), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            web_security_scanner.ListFindingTypeStatsResponse()
        )
        await client.list_finding_type_stats(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_finding_type_stats_flattened():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_finding_type_stats), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = web_security_scanner.ListFindingTypeStatsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_finding_type_stats(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_finding_type_stats_flattened_error():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_finding_type_stats(
            web_security_scanner.ListFindingTypeStatsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_finding_type_stats_flattened_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_finding_type_stats), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = web_security_scanner.ListFindingTypeStatsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            web_security_scanner.ListFindingTypeStatsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_finding_type_stats(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_finding_type_stats_flattened_error_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_finding_type_stats(
            web_security_scanner.ListFindingTypeStatsRequest(), parent="parent_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.WebSecurityScannerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = WebSecurityScannerClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.WebSecurityScannerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = WebSecurityScannerClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.WebSecurityScannerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = WebSecurityScannerClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.WebSecurityScannerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = WebSecurityScannerClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.WebSecurityScannerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.WebSecurityScannerGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.WebSecurityScannerGrpcTransport,
        transports.WebSecurityScannerGrpcAsyncIOTransport,
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
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(client.transport, transports.WebSecurityScannerGrpcTransport,)


def test_web_security_scanner_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.WebSecurityScannerTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_web_security_scanner_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.websecurityscanner_v1beta.services.web_security_scanner.transports.WebSecurityScannerTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.WebSecurityScannerTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_scan_config",
        "delete_scan_config",
        "get_scan_config",
        "list_scan_configs",
        "update_scan_config",
        "start_scan_run",
        "get_scan_run",
        "list_scan_runs",
        "stop_scan_run",
        "list_crawled_urls",
        "get_finding",
        "list_findings",
        "list_finding_type_stats",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


@requires_google_auth_gte_1_25_0
def test_web_security_scanner_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.websecurityscanner_v1beta.services.web_security_scanner.transports.WebSecurityScannerTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.WebSecurityScannerTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


@requires_google_auth_lt_1_25_0
def test_web_security_scanner_base_transport_with_credentials_file_old_google_auth():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.websecurityscanner_v1beta.services.web_security_scanner.transports.WebSecurityScannerTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.WebSecurityScannerTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_web_security_scanner_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.websecurityscanner_v1beta.services.web_security_scanner.transports.WebSecurityScannerTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.WebSecurityScannerTransport()
        adc.assert_called_once()


@requires_google_auth_gte_1_25_0
def test_web_security_scanner_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        WebSecurityScannerClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@requires_google_auth_lt_1_25_0
def test_web_security_scanner_auth_adc_old_google_auth():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        WebSecurityScannerClient()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.WebSecurityScannerGrpcTransport,
        transports.WebSecurityScannerGrpcAsyncIOTransport,
    ],
)
@requires_google_auth_gte_1_25_0
def test_web_security_scanner_transport_auth_adc(transport_class):
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
        transports.WebSecurityScannerGrpcTransport,
        transports.WebSecurityScannerGrpcAsyncIOTransport,
    ],
)
@requires_google_auth_lt_1_25_0
def test_web_security_scanner_transport_auth_adc_old_google_auth(transport_class):
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
        (transports.WebSecurityScannerGrpcTransport, grpc_helpers),
        (transports.WebSecurityScannerGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_web_security_scanner_transport_create_channel(transport_class, grpc_helpers):
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
            "websecurityscanner.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="websecurityscanner.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.WebSecurityScannerGrpcTransport,
        transports.WebSecurityScannerGrpcAsyncIOTransport,
    ],
)
def test_web_security_scanner_grpc_transport_client_cert_source_for_mtls(
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


def test_web_security_scanner_host_no_port():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="websecurityscanner.googleapis.com"
        ),
    )
    assert client.transport._host == "websecurityscanner.googleapis.com:443"


def test_web_security_scanner_host_with_port():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="websecurityscanner.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "websecurityscanner.googleapis.com:8000"


def test_web_security_scanner_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.WebSecurityScannerGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_web_security_scanner_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.WebSecurityScannerGrpcAsyncIOTransport(
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
        transports.WebSecurityScannerGrpcTransport,
        transports.WebSecurityScannerGrpcAsyncIOTransport,
    ],
)
def test_web_security_scanner_transport_channel_mtls_with_client_cert_source(
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
        transports.WebSecurityScannerGrpcTransport,
        transports.WebSecurityScannerGrpcAsyncIOTransport,
    ],
)
def test_web_security_scanner_transport_channel_mtls_with_adc(transport_class):
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


def test_finding_path():
    project = "squid"
    scan_config = "clam"
    scan_run = "whelk"
    finding = "octopus"
    expected = "projects/{project}/scanConfigs/{scan_config}/scanRuns/{scan_run}/findings/{finding}".format(
        project=project, scan_config=scan_config, scan_run=scan_run, finding=finding,
    )
    actual = WebSecurityScannerClient.finding_path(
        project, scan_config, scan_run, finding
    )
    assert expected == actual


def test_parse_finding_path():
    expected = {
        "project": "oyster",
        "scan_config": "nudibranch",
        "scan_run": "cuttlefish",
        "finding": "mussel",
    }
    path = WebSecurityScannerClient.finding_path(**expected)

    # Check that the path construction is reversible.
    actual = WebSecurityScannerClient.parse_finding_path(path)
    assert expected == actual


def test_scan_config_path():
    project = "winkle"
    scan_config = "nautilus"
    expected = "projects/{project}/scanConfigs/{scan_config}".format(
        project=project, scan_config=scan_config,
    )
    actual = WebSecurityScannerClient.scan_config_path(project, scan_config)
    assert expected == actual


def test_parse_scan_config_path():
    expected = {
        "project": "scallop",
        "scan_config": "abalone",
    }
    path = WebSecurityScannerClient.scan_config_path(**expected)

    # Check that the path construction is reversible.
    actual = WebSecurityScannerClient.parse_scan_config_path(path)
    assert expected == actual


def test_scan_run_path():
    project = "squid"
    scan_config = "clam"
    scan_run = "whelk"
    expected = "projects/{project}/scanConfigs/{scan_config}/scanRuns/{scan_run}".format(
        project=project, scan_config=scan_config, scan_run=scan_run,
    )
    actual = WebSecurityScannerClient.scan_run_path(project, scan_config, scan_run)
    assert expected == actual


def test_parse_scan_run_path():
    expected = {
        "project": "octopus",
        "scan_config": "oyster",
        "scan_run": "nudibranch",
    }
    path = WebSecurityScannerClient.scan_run_path(**expected)

    # Check that the path construction is reversible.
    actual = WebSecurityScannerClient.parse_scan_run_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "cuttlefish"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = WebSecurityScannerClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "mussel",
    }
    path = WebSecurityScannerClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = WebSecurityScannerClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "winkle"
    expected = "folders/{folder}".format(folder=folder,)
    actual = WebSecurityScannerClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nautilus",
    }
    path = WebSecurityScannerClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = WebSecurityScannerClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "scallop"
    expected = "organizations/{organization}".format(organization=organization,)
    actual = WebSecurityScannerClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "abalone",
    }
    path = WebSecurityScannerClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = WebSecurityScannerClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "squid"
    expected = "projects/{project}".format(project=project,)
    actual = WebSecurityScannerClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "clam",
    }
    path = WebSecurityScannerClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = WebSecurityScannerClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "whelk"
    location = "octopus"
    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = WebSecurityScannerClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
    }
    path = WebSecurityScannerClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = WebSecurityScannerClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.WebSecurityScannerTransport, "_prep_wrapped_messages"
    ) as prep:
        client = WebSecurityScannerClient(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.WebSecurityScannerTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = WebSecurityScannerClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
