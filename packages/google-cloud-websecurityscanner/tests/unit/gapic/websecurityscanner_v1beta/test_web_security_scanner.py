# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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

# try/except added for compatibility with python < 3.8
try:
    from unittest import mock
    from unittest.mock import AsyncMock  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    import mock

from collections.abc import Iterable
import json
import math

from google.api_core import gapic_v1, grpc_helpers, grpc_helpers_async, path_template
from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import json_format
from google.protobuf import timestamp_pb2  # type: ignore
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest
from requests import PreparedRequest, Request, Response
from requests.sessions import Session

from google.cloud.websecurityscanner_v1beta.services.web_security_scanner import (
    WebSecurityScannerAsyncClient,
    WebSecurityScannerClient,
    pagers,
    transports,
)
from google.cloud.websecurityscanner_v1beta.types import (
    scan_config_error,
    scan_run,
    scan_run_error_trace,
    scan_run_warning_trace,
    web_security_scanner,
)
from google.cloud.websecurityscanner_v1beta.types import (
    crawled_url,
    finding,
    finding_addon,
    finding_type_stats,
)
from google.cloud.websecurityscanner_v1beta.types import scan_config as gcw_scan_config
from google.cloud.websecurityscanner_v1beta.types import scan_config


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
    "client_class,transport_name",
    [
        (WebSecurityScannerClient, "grpc"),
        (WebSecurityScannerAsyncClient, "grpc_asyncio"),
        (WebSecurityScannerClient, "rest"),
    ],
)
def test_web_security_scanner_client_from_service_account_info(
    client_class, transport_name
):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            "websecurityscanner.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://websecurityscanner.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.WebSecurityScannerGrpcTransport, "grpc"),
        (transports.WebSecurityScannerGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.WebSecurityScannerRestTransport, "rest"),
    ],
)
def test_web_security_scanner_client_service_account_always_use_jwt(
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
    "client_class,transport_name",
    [
        (WebSecurityScannerClient, "grpc"),
        (WebSecurityScannerAsyncClient, "grpc_asyncio"),
        (WebSecurityScannerClient, "rest"),
    ],
)
def test_web_security_scanner_client_from_service_account_file(
    client_class, transport_name
):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            "websecurityscanner.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://websecurityscanner.googleapis.com"
        )


def test_web_security_scanner_client_get_transport_class():
    transport = WebSecurityScannerClient.get_transport_class()
    available_transports = [
        transports.WebSecurityScannerGrpcTransport,
        transports.WebSecurityScannerRestTransport,
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
        (WebSecurityScannerClient, transports.WebSecurityScannerRestTransport, "rest"),
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
            api_audience=None,
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
                api_audience=None,
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
                api_audience=None,
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
            api_audience=None,
        )
    # Check the case api_endpoint is provided
    options = client_options.ClientOptions(
        api_audience="https://language.googleapis.com"
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience="https://language.googleapis.com",
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
        (
            WebSecurityScannerClient,
            transports.WebSecurityScannerRestTransport,
            "rest",
            "true",
        ),
        (
            WebSecurityScannerClient,
            transports.WebSecurityScannerRestTransport,
            "rest",
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
                api_audience=None,
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
                        api_audience=None,
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
                    api_audience=None,
                )


@pytest.mark.parametrize(
    "client_class", [WebSecurityScannerClient, WebSecurityScannerAsyncClient]
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
def test_web_security_scanner_client_get_mtls_endpoint_and_cert_source(client_class):
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
        (WebSecurityScannerClient, transports.WebSecurityScannerGrpcTransport, "grpc"),
        (
            WebSecurityScannerAsyncClient,
            transports.WebSecurityScannerGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (WebSecurityScannerClient, transports.WebSecurityScannerRestTransport, "rest"),
    ],
)
def test_web_security_scanner_client_client_options_scopes(
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
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (
            WebSecurityScannerClient,
            transports.WebSecurityScannerGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            WebSecurityScannerAsyncClient,
            transports.WebSecurityScannerGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (
            WebSecurityScannerClient,
            transports.WebSecurityScannerRestTransport,
            "rest",
            None,
        ),
    ],
)
def test_web_security_scanner_client_client_options_credentials_file(
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
            api_audience=None,
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
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (
            WebSecurityScannerClient,
            transports.WebSecurityScannerGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            WebSecurityScannerAsyncClient,
            transports.WebSecurityScannerGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_web_security_scanner_client_create_channel_credentials_file(
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
            api_audience=None,
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
            "websecurityscanner.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="websecurityscanner.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        web_security_scanner.CreateScanConfigRequest,
        dict,
    ],
)
def test_create_scan_config(request_type, transport: str = "grpc"):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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


def test_create_scan_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
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
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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

    request.parent = "parent_value"

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
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_scan_config_field_headers_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.CreateScanConfigRequest()

    request.parent = "parent_value"

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
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


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
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].scan_config
        mock_val = gcw_scan_config.ScanConfig(name="name_value")
        assert arg == mock_val


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
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].scan_config
        mock_val = gcw_scan_config.ScanConfig(name="name_value")
        assert arg == mock_val


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


@pytest.mark.parametrize(
    "request_type",
    [
        web_security_scanner.DeleteScanConfigRequest,
        dict,
    ],
)
def test_delete_scan_config(request_type, transport: str = "grpc"):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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


def test_delete_scan_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
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
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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

    request.name = "name_value"

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
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_scan_config_field_headers_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.DeleteScanConfigRequest()

    request.name = "name_value"

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
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


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
        client.delete_scan_config(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_scan_config_flattened_error():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_scan_config(
            web_security_scanner.DeleteScanConfigRequest(),
            name="name_value",
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
        response = await client.delete_scan_config(
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
async def test_delete_scan_config_flattened_error_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_scan_config(
            web_security_scanner.DeleteScanConfigRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        web_security_scanner.GetScanConfigRequest,
        dict,
    ],
)
def test_get_scan_config(request_type, transport: str = "grpc"):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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


def test_get_scan_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
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
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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

    request.name = "name_value"

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
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_scan_config_field_headers_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.GetScanConfigRequest()

    request.name = "name_value"

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
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


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
        client.get_scan_config(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_scan_config_flattened_error():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_scan_config(
            web_security_scanner.GetScanConfigRequest(),
            name="name_value",
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
        response = await client.get_scan_config(
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
async def test_get_scan_config_flattened_error_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_scan_config(
            web_security_scanner.GetScanConfigRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        web_security_scanner.ListScanConfigsRequest,
        dict,
    ],
)
def test_list_scan_configs(request_type, transport: str = "grpc"):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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


def test_list_scan_configs_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
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
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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

    request.parent = "parent_value"

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
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_scan_configs_field_headers_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.ListScanConfigsRequest()

    request.parent = "parent_value"

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
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


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
        client.list_scan_configs(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_scan_configs_flattened_error():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_scan_configs(
            web_security_scanner.ListScanConfigsRequest(),
            parent="parent_value",
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
        response = await client.list_scan_configs(
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
async def test_list_scan_configs_flattened_error_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_scan_configs(
            web_security_scanner.ListScanConfigsRequest(),
            parent="parent_value",
        )


def test_list_scan_configs_pager(transport_name: str = "grpc"):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

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
                scan_configs=[],
                next_page_token="def",
            ),
            web_security_scanner.ListScanConfigsResponse(
                scan_configs=[
                    scan_config.ScanConfig(),
                ],
                next_page_token="ghi",
            ),
            web_security_scanner.ListScanConfigsResponse(
                scan_configs=[
                    scan_config.ScanConfig(),
                    scan_config.ScanConfig(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_scan_configs(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, scan_config.ScanConfig) for i in results)


def test_list_scan_configs_pages(transport_name: str = "grpc"):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

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
                scan_configs=[],
                next_page_token="def",
            ),
            web_security_scanner.ListScanConfigsResponse(
                scan_configs=[
                    scan_config.ScanConfig(),
                ],
                next_page_token="ghi",
            ),
            web_security_scanner.ListScanConfigsResponse(
                scan_configs=[
                    scan_config.ScanConfig(),
                    scan_config.ScanConfig(),
                ],
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
                scan_configs=[],
                next_page_token="def",
            ),
            web_security_scanner.ListScanConfigsResponse(
                scan_configs=[
                    scan_config.ScanConfig(),
                ],
                next_page_token="ghi",
            ),
            web_security_scanner.ListScanConfigsResponse(
                scan_configs=[
                    scan_config.ScanConfig(),
                    scan_config.ScanConfig(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_scan_configs(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
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
                scan_configs=[],
                next_page_token="def",
            ),
            web_security_scanner.ListScanConfigsResponse(
                scan_configs=[
                    scan_config.ScanConfig(),
                ],
                next_page_token="ghi",
            ),
            web_security_scanner.ListScanConfigsResponse(
                scan_configs=[
                    scan_config.ScanConfig(),
                    scan_config.ScanConfig(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_scan_configs(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        web_security_scanner.UpdateScanConfigRequest,
        dict,
    ],
)
def test_update_scan_config(request_type, transport: str = "grpc"):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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


def test_update_scan_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
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
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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

    request.scan_config.name = "name_value"

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
    assert (
        "x-goog-request-params",
        "scan_config.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_scan_config_field_headers_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.UpdateScanConfigRequest()

    request.scan_config.name = "name_value"

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
    assert (
        "x-goog-request-params",
        "scan_config.name=name_value",
    ) in kw["metadata"]


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
        arg = args[0].scan_config
        mock_val = gcw_scan_config.ScanConfig(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


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
        arg = args[0].scan_config
        mock_val = gcw_scan_config.ScanConfig(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


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


@pytest.mark.parametrize(
    "request_type",
    [
        web_security_scanner.StartScanRunRequest,
        dict,
    ],
)
def test_start_scan_run(request_type, transport: str = "grpc"):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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


def test_start_scan_run_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
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
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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

    request.name = "name_value"

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
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_start_scan_run_field_headers_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.StartScanRunRequest()

    request.name = "name_value"

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
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


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
        client.start_scan_run(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_start_scan_run_flattened_error():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.start_scan_run(
            web_security_scanner.StartScanRunRequest(),
            name="name_value",
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
        response = await client.start_scan_run(
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
async def test_start_scan_run_flattened_error_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.start_scan_run(
            web_security_scanner.StartScanRunRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        web_security_scanner.GetScanRunRequest,
        dict,
    ],
)
def test_get_scan_run(request_type, transport: str = "grpc"):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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


def test_get_scan_run_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
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
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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

    request.name = "name_value"

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
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_scan_run_field_headers_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.GetScanRunRequest()

    request.name = "name_value"

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
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


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
        client.get_scan_run(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_scan_run_flattened_error():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_scan_run(
            web_security_scanner.GetScanRunRequest(),
            name="name_value",
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
        response = await client.get_scan_run(
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
async def test_get_scan_run_flattened_error_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_scan_run(
            web_security_scanner.GetScanRunRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        web_security_scanner.ListScanRunsRequest,
        dict,
    ],
)
def test_list_scan_runs(request_type, transport: str = "grpc"):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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


def test_list_scan_runs_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
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
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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

    request.parent = "parent_value"

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
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_scan_runs_field_headers_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.ListScanRunsRequest()

    request.parent = "parent_value"

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
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


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
        client.list_scan_runs(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_scan_runs_flattened_error():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_scan_runs(
            web_security_scanner.ListScanRunsRequest(),
            parent="parent_value",
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
        response = await client.list_scan_runs(
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
async def test_list_scan_runs_flattened_error_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_scan_runs(
            web_security_scanner.ListScanRunsRequest(),
            parent="parent_value",
        )


def test_list_scan_runs_pager(transport_name: str = "grpc"):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_scan_runs), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            web_security_scanner.ListScanRunsResponse(
                scan_runs=[
                    scan_run.ScanRun(),
                    scan_run.ScanRun(),
                    scan_run.ScanRun(),
                ],
                next_page_token="abc",
            ),
            web_security_scanner.ListScanRunsResponse(
                scan_runs=[],
                next_page_token="def",
            ),
            web_security_scanner.ListScanRunsResponse(
                scan_runs=[
                    scan_run.ScanRun(),
                ],
                next_page_token="ghi",
            ),
            web_security_scanner.ListScanRunsResponse(
                scan_runs=[
                    scan_run.ScanRun(),
                    scan_run.ScanRun(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_scan_runs(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, scan_run.ScanRun) for i in results)


def test_list_scan_runs_pages(transport_name: str = "grpc"):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_scan_runs), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            web_security_scanner.ListScanRunsResponse(
                scan_runs=[
                    scan_run.ScanRun(),
                    scan_run.ScanRun(),
                    scan_run.ScanRun(),
                ],
                next_page_token="abc",
            ),
            web_security_scanner.ListScanRunsResponse(
                scan_runs=[],
                next_page_token="def",
            ),
            web_security_scanner.ListScanRunsResponse(
                scan_runs=[
                    scan_run.ScanRun(),
                ],
                next_page_token="ghi",
            ),
            web_security_scanner.ListScanRunsResponse(
                scan_runs=[
                    scan_run.ScanRun(),
                    scan_run.ScanRun(),
                ],
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
                scan_runs=[
                    scan_run.ScanRun(),
                    scan_run.ScanRun(),
                    scan_run.ScanRun(),
                ],
                next_page_token="abc",
            ),
            web_security_scanner.ListScanRunsResponse(
                scan_runs=[],
                next_page_token="def",
            ),
            web_security_scanner.ListScanRunsResponse(
                scan_runs=[
                    scan_run.ScanRun(),
                ],
                next_page_token="ghi",
            ),
            web_security_scanner.ListScanRunsResponse(
                scan_runs=[
                    scan_run.ScanRun(),
                    scan_run.ScanRun(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_scan_runs(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
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
                scan_runs=[
                    scan_run.ScanRun(),
                    scan_run.ScanRun(),
                    scan_run.ScanRun(),
                ],
                next_page_token="abc",
            ),
            web_security_scanner.ListScanRunsResponse(
                scan_runs=[],
                next_page_token="def",
            ),
            web_security_scanner.ListScanRunsResponse(
                scan_runs=[
                    scan_run.ScanRun(),
                ],
                next_page_token="ghi",
            ),
            web_security_scanner.ListScanRunsResponse(
                scan_runs=[
                    scan_run.ScanRun(),
                    scan_run.ScanRun(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_scan_runs(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        web_security_scanner.StopScanRunRequest,
        dict,
    ],
)
def test_stop_scan_run(request_type, transport: str = "grpc"):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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


def test_stop_scan_run_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
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
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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

    request.name = "name_value"

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
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_stop_scan_run_field_headers_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.StopScanRunRequest()

    request.name = "name_value"

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
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


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
        client.stop_scan_run(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_stop_scan_run_flattened_error():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.stop_scan_run(
            web_security_scanner.StopScanRunRequest(),
            name="name_value",
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
        response = await client.stop_scan_run(
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
async def test_stop_scan_run_flattened_error_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.stop_scan_run(
            web_security_scanner.StopScanRunRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        web_security_scanner.ListCrawledUrlsRequest,
        dict,
    ],
)
def test_list_crawled_urls(request_type, transport: str = "grpc"):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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


def test_list_crawled_urls_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
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
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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

    request.parent = "parent_value"

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
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_crawled_urls_field_headers_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.ListCrawledUrlsRequest()

    request.parent = "parent_value"

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
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


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
        client.list_crawled_urls(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_crawled_urls_flattened_error():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_crawled_urls(
            web_security_scanner.ListCrawledUrlsRequest(),
            parent="parent_value",
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
        response = await client.list_crawled_urls(
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
async def test_list_crawled_urls_flattened_error_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_crawled_urls(
            web_security_scanner.ListCrawledUrlsRequest(),
            parent="parent_value",
        )


def test_list_crawled_urls_pager(transport_name: str = "grpc"):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

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
                crawled_urls=[],
                next_page_token="def",
            ),
            web_security_scanner.ListCrawledUrlsResponse(
                crawled_urls=[
                    crawled_url.CrawledUrl(),
                ],
                next_page_token="ghi",
            ),
            web_security_scanner.ListCrawledUrlsResponse(
                crawled_urls=[
                    crawled_url.CrawledUrl(),
                    crawled_url.CrawledUrl(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_crawled_urls(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, crawled_url.CrawledUrl) for i in results)


def test_list_crawled_urls_pages(transport_name: str = "grpc"):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

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
                crawled_urls=[],
                next_page_token="def",
            ),
            web_security_scanner.ListCrawledUrlsResponse(
                crawled_urls=[
                    crawled_url.CrawledUrl(),
                ],
                next_page_token="ghi",
            ),
            web_security_scanner.ListCrawledUrlsResponse(
                crawled_urls=[
                    crawled_url.CrawledUrl(),
                    crawled_url.CrawledUrl(),
                ],
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
                crawled_urls=[],
                next_page_token="def",
            ),
            web_security_scanner.ListCrawledUrlsResponse(
                crawled_urls=[
                    crawled_url.CrawledUrl(),
                ],
                next_page_token="ghi",
            ),
            web_security_scanner.ListCrawledUrlsResponse(
                crawled_urls=[
                    crawled_url.CrawledUrl(),
                    crawled_url.CrawledUrl(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_crawled_urls(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
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
                crawled_urls=[],
                next_page_token="def",
            ),
            web_security_scanner.ListCrawledUrlsResponse(
                crawled_urls=[
                    crawled_url.CrawledUrl(),
                ],
                next_page_token="ghi",
            ),
            web_security_scanner.ListCrawledUrlsResponse(
                crawled_urls=[
                    crawled_url.CrawledUrl(),
                    crawled_url.CrawledUrl(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_crawled_urls(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        web_security_scanner.GetFindingRequest,
        dict,
    ],
)
def test_get_finding(request_type, transport: str = "grpc"):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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


def test_get_finding_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
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
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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

    request.name = "name_value"

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
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_finding_field_headers_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.GetFindingRequest()

    request.name = "name_value"

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
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


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
        client.get_finding(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_finding_flattened_error():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_finding(
            web_security_scanner.GetFindingRequest(),
            name="name_value",
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
        response = await client.get_finding(
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
async def test_get_finding_flattened_error_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_finding(
            web_security_scanner.GetFindingRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        web_security_scanner.ListFindingsRequest,
        dict,
    ],
)
def test_list_findings(request_type, transport: str = "grpc"):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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


def test_list_findings_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
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
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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

    request.parent = "parent_value"

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
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_findings_field_headers_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.ListFindingsRequest()

    request.parent = "parent_value"

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
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


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
            parent="parent_value",
            filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].filter
        mock_val = "filter_value"
        assert arg == mock_val


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
            parent="parent_value",
            filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].filter
        mock_val = "filter_value"
        assert arg == mock_val


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


def test_list_findings_pager(transport_name: str = "grpc"):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_findings), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            web_security_scanner.ListFindingsResponse(
                findings=[
                    finding.Finding(),
                    finding.Finding(),
                    finding.Finding(),
                ],
                next_page_token="abc",
            ),
            web_security_scanner.ListFindingsResponse(
                findings=[],
                next_page_token="def",
            ),
            web_security_scanner.ListFindingsResponse(
                findings=[
                    finding.Finding(),
                ],
                next_page_token="ghi",
            ),
            web_security_scanner.ListFindingsResponse(
                findings=[
                    finding.Finding(),
                    finding.Finding(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_findings(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, finding.Finding) for i in results)


def test_list_findings_pages(transport_name: str = "grpc"):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_findings), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            web_security_scanner.ListFindingsResponse(
                findings=[
                    finding.Finding(),
                    finding.Finding(),
                    finding.Finding(),
                ],
                next_page_token="abc",
            ),
            web_security_scanner.ListFindingsResponse(
                findings=[],
                next_page_token="def",
            ),
            web_security_scanner.ListFindingsResponse(
                findings=[
                    finding.Finding(),
                ],
                next_page_token="ghi",
            ),
            web_security_scanner.ListFindingsResponse(
                findings=[
                    finding.Finding(),
                    finding.Finding(),
                ],
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
                findings=[
                    finding.Finding(),
                    finding.Finding(),
                    finding.Finding(),
                ],
                next_page_token="abc",
            ),
            web_security_scanner.ListFindingsResponse(
                findings=[],
                next_page_token="def",
            ),
            web_security_scanner.ListFindingsResponse(
                findings=[
                    finding.Finding(),
                ],
                next_page_token="ghi",
            ),
            web_security_scanner.ListFindingsResponse(
                findings=[
                    finding.Finding(),
                    finding.Finding(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_findings(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
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
                findings=[
                    finding.Finding(),
                    finding.Finding(),
                    finding.Finding(),
                ],
                next_page_token="abc",
            ),
            web_security_scanner.ListFindingsResponse(
                findings=[],
                next_page_token="def",
            ),
            web_security_scanner.ListFindingsResponse(
                findings=[
                    finding.Finding(),
                ],
                next_page_token="ghi",
            ),
            web_security_scanner.ListFindingsResponse(
                findings=[
                    finding.Finding(),
                    finding.Finding(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_findings(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        web_security_scanner.ListFindingTypeStatsRequest,
        dict,
    ],
)
def test_list_finding_type_stats(request_type, transport: str = "grpc"):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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


def test_list_finding_type_stats_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
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
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
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

    request.parent = "parent_value"

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
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_finding_type_stats_field_headers_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = web_security_scanner.ListFindingTypeStatsRequest()

    request.parent = "parent_value"

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
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


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
        client.list_finding_type_stats(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_finding_type_stats_flattened_error():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_finding_type_stats(
            web_security_scanner.ListFindingTypeStatsRequest(),
            parent="parent_value",
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
        response = await client.list_finding_type_stats(
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
async def test_list_finding_type_stats_flattened_error_async():
    client = WebSecurityScannerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_finding_type_stats(
            web_security_scanner.ListFindingTypeStatsRequest(),
            parent="parent_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        web_security_scanner.CreateScanConfigRequest,
        dict,
    ],
)
def test_create_scan_config_rest(request_type):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1"}
    request_init["scan_config"] = {
        "name": "name_value",
        "display_name": "display_name_value",
        "max_qps": 761,
        "starting_urls": ["starting_urls_value1", "starting_urls_value2"],
        "authentication": {
            "google_account": {
                "username": "username_value",
                "password": "password_value",
            },
            "custom_account": {
                "username": "username_value",
                "password": "password_value",
                "login_url": "login_url_value",
            },
        },
        "user_agent": 1,
        "blacklist_patterns": [
            "blacklist_patterns_value1",
            "blacklist_patterns_value2",
        ],
        "schedule": {
            "schedule_time": {"seconds": 751, "nanos": 543},
            "interval_duration_days": 2362,
        },
        "target_platforms": [1],
        "export_to_security_command_center": 1,
        "latest_run": {
            "name": "name_value",
            "execution_state": 1,
            "result_state": 1,
            "start_time": {},
            "end_time": {},
            "urls_crawled_count": 1935,
            "urls_tested_count": 1846,
            "has_vulnerabilities": True,
            "progress_percent": 1733,
            "error_trace": {
                "code": 1,
                "scan_config_error": {"code": 1, "field_name": "field_name_value"},
                "most_common_http_error_code": 2893,
            },
            "warning_traces": [{"code": 1}],
        },
        "risk_level": 1,
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gcw_scan_config.ScanConfig(
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

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gcw_scan_config.ScanConfig.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_scan_config(request)

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


def test_create_scan_config_rest_required_fields(
    request_type=web_security_scanner.CreateScanConfigRequest,
):
    transport_class = transports.WebSecurityScannerRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_scan_config._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_scan_config._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gcw_scan_config.ScanConfig()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = gcw_scan_config.ScanConfig.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_scan_config(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_scan_config_rest_unset_required_fields():
    transport = transports.WebSecurityScannerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_scan_config._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "scanConfig",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_scan_config_rest_interceptors(null_interceptor):
    transport = transports.WebSecurityScannerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.WebSecurityScannerRestInterceptor(),
    )
    client = WebSecurityScannerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.WebSecurityScannerRestInterceptor, "post_create_scan_config"
    ) as post, mock.patch.object(
        transports.WebSecurityScannerRestInterceptor, "pre_create_scan_config"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = web_security_scanner.CreateScanConfigRequest.pb(
            web_security_scanner.CreateScanConfigRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = gcw_scan_config.ScanConfig.to_json(
            gcw_scan_config.ScanConfig()
        )

        request = web_security_scanner.CreateScanConfigRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gcw_scan_config.ScanConfig()

        client.create_scan_config(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_scan_config_rest_bad_request(
    transport: str = "rest", request_type=web_security_scanner.CreateScanConfigRequest
):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1"}
    request_init["scan_config"] = {
        "name": "name_value",
        "display_name": "display_name_value",
        "max_qps": 761,
        "starting_urls": ["starting_urls_value1", "starting_urls_value2"],
        "authentication": {
            "google_account": {
                "username": "username_value",
                "password": "password_value",
            },
            "custom_account": {
                "username": "username_value",
                "password": "password_value",
                "login_url": "login_url_value",
            },
        },
        "user_agent": 1,
        "blacklist_patterns": [
            "blacklist_patterns_value1",
            "blacklist_patterns_value2",
        ],
        "schedule": {
            "schedule_time": {"seconds": 751, "nanos": 543},
            "interval_duration_days": 2362,
        },
        "target_platforms": [1],
        "export_to_security_command_center": 1,
        "latest_run": {
            "name": "name_value",
            "execution_state": 1,
            "result_state": 1,
            "start_time": {},
            "end_time": {},
            "urls_crawled_count": 1935,
            "urls_tested_count": 1846,
            "has_vulnerabilities": True,
            "progress_percent": 1733,
            "error_trace": {
                "code": 1,
                "scan_config_error": {"code": 1, "field_name": "field_name_value"},
                "most_common_http_error_code": 2893,
            },
            "warning_traces": [{"code": 1}],
        },
        "risk_level": 1,
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_scan_config(request)


def test_create_scan_config_rest_flattened():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gcw_scan_config.ScanConfig()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            scan_config=gcw_scan_config.ScanConfig(name="name_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gcw_scan_config.ScanConfig.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_scan_config(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1beta/{parent=projects/*}/scanConfigs" % client.transport._host,
            args[1],
        )


def test_create_scan_config_rest_flattened_error(transport: str = "rest"):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_scan_config(
            web_security_scanner.CreateScanConfigRequest(),
            parent="parent_value",
            scan_config=gcw_scan_config.ScanConfig(name="name_value"),
        )


def test_create_scan_config_rest_error():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        web_security_scanner.DeleteScanConfigRequest,
        dict,
    ],
)
def test_delete_scan_config_rest(request_type):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/scanConfigs/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_scan_config(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_scan_config_rest_required_fields(
    request_type=web_security_scanner.DeleteScanConfigRequest,
):
    transport_class = transports.WebSecurityScannerRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_scan_config._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_scan_config._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = None
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "delete",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = ""

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_scan_config(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_scan_config_rest_unset_required_fields():
    transport = transports.WebSecurityScannerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_scan_config._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_scan_config_rest_interceptors(null_interceptor):
    transport = transports.WebSecurityScannerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.WebSecurityScannerRestInterceptor(),
    )
    client = WebSecurityScannerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.WebSecurityScannerRestInterceptor, "pre_delete_scan_config"
    ) as pre:
        pre.assert_not_called()
        pb_message = web_security_scanner.DeleteScanConfigRequest.pb(
            web_security_scanner.DeleteScanConfigRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()

        request = web_security_scanner.DeleteScanConfigRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_scan_config(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_delete_scan_config_rest_bad_request(
    transport: str = "rest", request_type=web_security_scanner.DeleteScanConfigRequest
):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/scanConfigs/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_scan_config(request)


def test_delete_scan_config_rest_flattened():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/scanConfigs/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_scan_config(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1beta/{name=projects/*/scanConfigs/*}" % client.transport._host,
            args[1],
        )


def test_delete_scan_config_rest_flattened_error(transport: str = "rest"):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_scan_config(
            web_security_scanner.DeleteScanConfigRequest(),
            name="name_value",
        )


def test_delete_scan_config_rest_error():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        web_security_scanner.GetScanConfigRequest,
        dict,
    ],
)
def test_get_scan_config_rest(request_type):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/scanConfigs/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = scan_config.ScanConfig(
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

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = scan_config.ScanConfig.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_scan_config(request)

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


def test_get_scan_config_rest_required_fields(
    request_type=web_security_scanner.GetScanConfigRequest,
):
    transport_class = transports.WebSecurityScannerRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_scan_config._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_scan_config._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = scan_config.ScanConfig()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = scan_config.ScanConfig.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_scan_config(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_scan_config_rest_unset_required_fields():
    transport = transports.WebSecurityScannerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_scan_config._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_scan_config_rest_interceptors(null_interceptor):
    transport = transports.WebSecurityScannerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.WebSecurityScannerRestInterceptor(),
    )
    client = WebSecurityScannerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.WebSecurityScannerRestInterceptor, "post_get_scan_config"
    ) as post, mock.patch.object(
        transports.WebSecurityScannerRestInterceptor, "pre_get_scan_config"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = web_security_scanner.GetScanConfigRequest.pb(
            web_security_scanner.GetScanConfigRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = scan_config.ScanConfig.to_json(
            scan_config.ScanConfig()
        )

        request = web_security_scanner.GetScanConfigRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = scan_config.ScanConfig()

        client.get_scan_config(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_scan_config_rest_bad_request(
    transport: str = "rest", request_type=web_security_scanner.GetScanConfigRequest
):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/scanConfigs/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_scan_config(request)


def test_get_scan_config_rest_flattened():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = scan_config.ScanConfig()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/scanConfigs/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = scan_config.ScanConfig.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_scan_config(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1beta/{name=projects/*/scanConfigs/*}" % client.transport._host,
            args[1],
        )


def test_get_scan_config_rest_flattened_error(transport: str = "rest"):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_scan_config(
            web_security_scanner.GetScanConfigRequest(),
            name="name_value",
        )


def test_get_scan_config_rest_error():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        web_security_scanner.ListScanConfigsRequest,
        dict,
    ],
)
def test_list_scan_configs_rest(request_type):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = web_security_scanner.ListScanConfigsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = web_security_scanner.ListScanConfigsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_scan_configs(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListScanConfigsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_scan_configs_rest_required_fields(
    request_type=web_security_scanner.ListScanConfigsRequest,
):
    transport_class = transports.WebSecurityScannerRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_scan_configs._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_scan_configs._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = web_security_scanner.ListScanConfigsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = web_security_scanner.ListScanConfigsResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_scan_configs(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_scan_configs_rest_unset_required_fields():
    transport = transports.WebSecurityScannerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_scan_configs._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_scan_configs_rest_interceptors(null_interceptor):
    transport = transports.WebSecurityScannerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.WebSecurityScannerRestInterceptor(),
    )
    client = WebSecurityScannerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.WebSecurityScannerRestInterceptor, "post_list_scan_configs"
    ) as post, mock.patch.object(
        transports.WebSecurityScannerRestInterceptor, "pre_list_scan_configs"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = web_security_scanner.ListScanConfigsRequest.pb(
            web_security_scanner.ListScanConfigsRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = (
            web_security_scanner.ListScanConfigsResponse.to_json(
                web_security_scanner.ListScanConfigsResponse()
            )
        )

        request = web_security_scanner.ListScanConfigsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = web_security_scanner.ListScanConfigsResponse()

        client.list_scan_configs(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_scan_configs_rest_bad_request(
    transport: str = "rest", request_type=web_security_scanner.ListScanConfigsRequest
):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_scan_configs(request)


def test_list_scan_configs_rest_flattened():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = web_security_scanner.ListScanConfigsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = web_security_scanner.ListScanConfigsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_scan_configs(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1beta/{parent=projects/*}/scanConfigs" % client.transport._host,
            args[1],
        )


def test_list_scan_configs_rest_flattened_error(transport: str = "rest"):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_scan_configs(
            web_security_scanner.ListScanConfigsRequest(),
            parent="parent_value",
        )


def test_list_scan_configs_rest_pager(transport: str = "rest"):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            web_security_scanner.ListScanConfigsResponse(
                scan_configs=[
                    scan_config.ScanConfig(),
                    scan_config.ScanConfig(),
                    scan_config.ScanConfig(),
                ],
                next_page_token="abc",
            ),
            web_security_scanner.ListScanConfigsResponse(
                scan_configs=[],
                next_page_token="def",
            ),
            web_security_scanner.ListScanConfigsResponse(
                scan_configs=[
                    scan_config.ScanConfig(),
                ],
                next_page_token="ghi",
            ),
            web_security_scanner.ListScanConfigsResponse(
                scan_configs=[
                    scan_config.ScanConfig(),
                    scan_config.ScanConfig(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            web_security_scanner.ListScanConfigsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1"}

        pager = client.list_scan_configs(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, scan_config.ScanConfig) for i in results)

        pages = list(client.list_scan_configs(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        web_security_scanner.UpdateScanConfigRequest,
        dict,
    ],
)
def test_update_scan_config_rest(request_type):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"scan_config": {"name": "projects/sample1/scanConfigs/sample2"}}
    request_init["scan_config"] = {
        "name": "projects/sample1/scanConfigs/sample2",
        "display_name": "display_name_value",
        "max_qps": 761,
        "starting_urls": ["starting_urls_value1", "starting_urls_value2"],
        "authentication": {
            "google_account": {
                "username": "username_value",
                "password": "password_value",
            },
            "custom_account": {
                "username": "username_value",
                "password": "password_value",
                "login_url": "login_url_value",
            },
        },
        "user_agent": 1,
        "blacklist_patterns": [
            "blacklist_patterns_value1",
            "blacklist_patterns_value2",
        ],
        "schedule": {
            "schedule_time": {"seconds": 751, "nanos": 543},
            "interval_duration_days": 2362,
        },
        "target_platforms": [1],
        "export_to_security_command_center": 1,
        "latest_run": {
            "name": "name_value",
            "execution_state": 1,
            "result_state": 1,
            "start_time": {},
            "end_time": {},
            "urls_crawled_count": 1935,
            "urls_tested_count": 1846,
            "has_vulnerabilities": True,
            "progress_percent": 1733,
            "error_trace": {
                "code": 1,
                "scan_config_error": {"code": 1, "field_name": "field_name_value"},
                "most_common_http_error_code": 2893,
            },
            "warning_traces": [{"code": 1}],
        },
        "risk_level": 1,
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gcw_scan_config.ScanConfig(
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

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gcw_scan_config.ScanConfig.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_scan_config(request)

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


def test_update_scan_config_rest_required_fields(
    request_type=web_security_scanner.UpdateScanConfigRequest,
):
    transport_class = transports.WebSecurityScannerRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_scan_config._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_scan_config._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gcw_scan_config.ScanConfig()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "patch",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = gcw_scan_config.ScanConfig.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_scan_config(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_scan_config_rest_unset_required_fields():
    transport = transports.WebSecurityScannerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_scan_config._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("updateMask",))
        & set(
            (
                "scanConfig",
                "updateMask",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_scan_config_rest_interceptors(null_interceptor):
    transport = transports.WebSecurityScannerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.WebSecurityScannerRestInterceptor(),
    )
    client = WebSecurityScannerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.WebSecurityScannerRestInterceptor, "post_update_scan_config"
    ) as post, mock.patch.object(
        transports.WebSecurityScannerRestInterceptor, "pre_update_scan_config"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = web_security_scanner.UpdateScanConfigRequest.pb(
            web_security_scanner.UpdateScanConfigRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = gcw_scan_config.ScanConfig.to_json(
            gcw_scan_config.ScanConfig()
        )

        request = web_security_scanner.UpdateScanConfigRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gcw_scan_config.ScanConfig()

        client.update_scan_config(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_scan_config_rest_bad_request(
    transport: str = "rest", request_type=web_security_scanner.UpdateScanConfigRequest
):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"scan_config": {"name": "projects/sample1/scanConfigs/sample2"}}
    request_init["scan_config"] = {
        "name": "projects/sample1/scanConfigs/sample2",
        "display_name": "display_name_value",
        "max_qps": 761,
        "starting_urls": ["starting_urls_value1", "starting_urls_value2"],
        "authentication": {
            "google_account": {
                "username": "username_value",
                "password": "password_value",
            },
            "custom_account": {
                "username": "username_value",
                "password": "password_value",
                "login_url": "login_url_value",
            },
        },
        "user_agent": 1,
        "blacklist_patterns": [
            "blacklist_patterns_value1",
            "blacklist_patterns_value2",
        ],
        "schedule": {
            "schedule_time": {"seconds": 751, "nanos": 543},
            "interval_duration_days": 2362,
        },
        "target_platforms": [1],
        "export_to_security_command_center": 1,
        "latest_run": {
            "name": "name_value",
            "execution_state": 1,
            "result_state": 1,
            "start_time": {},
            "end_time": {},
            "urls_crawled_count": 1935,
            "urls_tested_count": 1846,
            "has_vulnerabilities": True,
            "progress_percent": 1733,
            "error_trace": {
                "code": 1,
                "scan_config_error": {"code": 1, "field_name": "field_name_value"},
                "most_common_http_error_code": 2893,
            },
            "warning_traces": [{"code": 1}],
        },
        "risk_level": 1,
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_scan_config(request)


def test_update_scan_config_rest_flattened():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gcw_scan_config.ScanConfig()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "scan_config": {"name": "projects/sample1/scanConfigs/sample2"}
        }

        # get truthy value for each flattened field
        mock_args = dict(
            scan_config=gcw_scan_config.ScanConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gcw_scan_config.ScanConfig.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_scan_config(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1beta/{scan_config.name=projects/*/scanConfigs/*}"
            % client.transport._host,
            args[1],
        )


def test_update_scan_config_rest_flattened_error(transport: str = "rest"):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_scan_config(
            web_security_scanner.UpdateScanConfigRequest(),
            scan_config=gcw_scan_config.ScanConfig(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_scan_config_rest_error():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        web_security_scanner.StartScanRunRequest,
        dict,
    ],
)
def test_start_scan_run_rest(request_type):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/scanConfigs/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = scan_run.ScanRun(
            name="name_value",
            execution_state=scan_run.ScanRun.ExecutionState.QUEUED,
            result_state=scan_run.ScanRun.ResultState.SUCCESS,
            urls_crawled_count=1935,
            urls_tested_count=1846,
            has_vulnerabilities=True,
            progress_percent=1733,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = scan_run.ScanRun.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.start_scan_run(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, scan_run.ScanRun)
    assert response.name == "name_value"
    assert response.execution_state == scan_run.ScanRun.ExecutionState.QUEUED
    assert response.result_state == scan_run.ScanRun.ResultState.SUCCESS
    assert response.urls_crawled_count == 1935
    assert response.urls_tested_count == 1846
    assert response.has_vulnerabilities is True
    assert response.progress_percent == 1733


def test_start_scan_run_rest_required_fields(
    request_type=web_security_scanner.StartScanRunRequest,
):
    transport_class = transports.WebSecurityScannerRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).start_scan_run._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).start_scan_run._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = scan_run.ScanRun()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = scan_run.ScanRun.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.start_scan_run(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_start_scan_run_rest_unset_required_fields():
    transport = transports.WebSecurityScannerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.start_scan_run._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_start_scan_run_rest_interceptors(null_interceptor):
    transport = transports.WebSecurityScannerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.WebSecurityScannerRestInterceptor(),
    )
    client = WebSecurityScannerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.WebSecurityScannerRestInterceptor, "post_start_scan_run"
    ) as post, mock.patch.object(
        transports.WebSecurityScannerRestInterceptor, "pre_start_scan_run"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = web_security_scanner.StartScanRunRequest.pb(
            web_security_scanner.StartScanRunRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = scan_run.ScanRun.to_json(scan_run.ScanRun())

        request = web_security_scanner.StartScanRunRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = scan_run.ScanRun()

        client.start_scan_run(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_start_scan_run_rest_bad_request(
    transport: str = "rest", request_type=web_security_scanner.StartScanRunRequest
):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/scanConfigs/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.start_scan_run(request)


def test_start_scan_run_rest_flattened():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = scan_run.ScanRun()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/scanConfigs/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = scan_run.ScanRun.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.start_scan_run(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1beta/{name=projects/*/scanConfigs/*}:start" % client.transport._host,
            args[1],
        )


def test_start_scan_run_rest_flattened_error(transport: str = "rest"):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.start_scan_run(
            web_security_scanner.StartScanRunRequest(),
            name="name_value",
        )


def test_start_scan_run_rest_error():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        web_security_scanner.GetScanRunRequest,
        dict,
    ],
)
def test_get_scan_run_rest(request_type):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/scanConfigs/sample2/scanRuns/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = scan_run.ScanRun(
            name="name_value",
            execution_state=scan_run.ScanRun.ExecutionState.QUEUED,
            result_state=scan_run.ScanRun.ResultState.SUCCESS,
            urls_crawled_count=1935,
            urls_tested_count=1846,
            has_vulnerabilities=True,
            progress_percent=1733,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = scan_run.ScanRun.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_scan_run(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, scan_run.ScanRun)
    assert response.name == "name_value"
    assert response.execution_state == scan_run.ScanRun.ExecutionState.QUEUED
    assert response.result_state == scan_run.ScanRun.ResultState.SUCCESS
    assert response.urls_crawled_count == 1935
    assert response.urls_tested_count == 1846
    assert response.has_vulnerabilities is True
    assert response.progress_percent == 1733


def test_get_scan_run_rest_required_fields(
    request_type=web_security_scanner.GetScanRunRequest,
):
    transport_class = transports.WebSecurityScannerRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_scan_run._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_scan_run._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = scan_run.ScanRun()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = scan_run.ScanRun.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_scan_run(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_scan_run_rest_unset_required_fields():
    transport = transports.WebSecurityScannerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_scan_run._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_scan_run_rest_interceptors(null_interceptor):
    transport = transports.WebSecurityScannerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.WebSecurityScannerRestInterceptor(),
    )
    client = WebSecurityScannerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.WebSecurityScannerRestInterceptor, "post_get_scan_run"
    ) as post, mock.patch.object(
        transports.WebSecurityScannerRestInterceptor, "pre_get_scan_run"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = web_security_scanner.GetScanRunRequest.pb(
            web_security_scanner.GetScanRunRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = scan_run.ScanRun.to_json(scan_run.ScanRun())

        request = web_security_scanner.GetScanRunRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = scan_run.ScanRun()

        client.get_scan_run(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_scan_run_rest_bad_request(
    transport: str = "rest", request_type=web_security_scanner.GetScanRunRequest
):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/scanConfigs/sample2/scanRuns/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_scan_run(request)


def test_get_scan_run_rest_flattened():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = scan_run.ScanRun()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/scanConfigs/sample2/scanRuns/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = scan_run.ScanRun.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_scan_run(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1beta/{name=projects/*/scanConfigs/*/scanRuns/*}"
            % client.transport._host,
            args[1],
        )


def test_get_scan_run_rest_flattened_error(transport: str = "rest"):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_scan_run(
            web_security_scanner.GetScanRunRequest(),
            name="name_value",
        )


def test_get_scan_run_rest_error():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        web_security_scanner.ListScanRunsRequest,
        dict,
    ],
)
def test_list_scan_runs_rest(request_type):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/scanConfigs/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = web_security_scanner.ListScanRunsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = web_security_scanner.ListScanRunsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_scan_runs(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListScanRunsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_scan_runs_rest_required_fields(
    request_type=web_security_scanner.ListScanRunsRequest,
):
    transport_class = transports.WebSecurityScannerRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_scan_runs._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_scan_runs._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = web_security_scanner.ListScanRunsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = web_security_scanner.ListScanRunsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_scan_runs(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_scan_runs_rest_unset_required_fields():
    transport = transports.WebSecurityScannerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_scan_runs._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_scan_runs_rest_interceptors(null_interceptor):
    transport = transports.WebSecurityScannerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.WebSecurityScannerRestInterceptor(),
    )
    client = WebSecurityScannerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.WebSecurityScannerRestInterceptor, "post_list_scan_runs"
    ) as post, mock.patch.object(
        transports.WebSecurityScannerRestInterceptor, "pre_list_scan_runs"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = web_security_scanner.ListScanRunsRequest.pb(
            web_security_scanner.ListScanRunsRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = web_security_scanner.ListScanRunsResponse.to_json(
            web_security_scanner.ListScanRunsResponse()
        )

        request = web_security_scanner.ListScanRunsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = web_security_scanner.ListScanRunsResponse()

        client.list_scan_runs(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_scan_runs_rest_bad_request(
    transport: str = "rest", request_type=web_security_scanner.ListScanRunsRequest
):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/scanConfigs/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_scan_runs(request)


def test_list_scan_runs_rest_flattened():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = web_security_scanner.ListScanRunsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/scanConfigs/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = web_security_scanner.ListScanRunsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_scan_runs(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1beta/{parent=projects/*/scanConfigs/*}/scanRuns"
            % client.transport._host,
            args[1],
        )


def test_list_scan_runs_rest_flattened_error(transport: str = "rest"):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_scan_runs(
            web_security_scanner.ListScanRunsRequest(),
            parent="parent_value",
        )


def test_list_scan_runs_rest_pager(transport: str = "rest"):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            web_security_scanner.ListScanRunsResponse(
                scan_runs=[
                    scan_run.ScanRun(),
                    scan_run.ScanRun(),
                    scan_run.ScanRun(),
                ],
                next_page_token="abc",
            ),
            web_security_scanner.ListScanRunsResponse(
                scan_runs=[],
                next_page_token="def",
            ),
            web_security_scanner.ListScanRunsResponse(
                scan_runs=[
                    scan_run.ScanRun(),
                ],
                next_page_token="ghi",
            ),
            web_security_scanner.ListScanRunsResponse(
                scan_runs=[
                    scan_run.ScanRun(),
                    scan_run.ScanRun(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            web_security_scanner.ListScanRunsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/scanConfigs/sample2"}

        pager = client.list_scan_runs(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, scan_run.ScanRun) for i in results)

        pages = list(client.list_scan_runs(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        web_security_scanner.StopScanRunRequest,
        dict,
    ],
)
def test_stop_scan_run_rest(request_type):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/scanConfigs/sample2/scanRuns/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = scan_run.ScanRun(
            name="name_value",
            execution_state=scan_run.ScanRun.ExecutionState.QUEUED,
            result_state=scan_run.ScanRun.ResultState.SUCCESS,
            urls_crawled_count=1935,
            urls_tested_count=1846,
            has_vulnerabilities=True,
            progress_percent=1733,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = scan_run.ScanRun.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.stop_scan_run(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, scan_run.ScanRun)
    assert response.name == "name_value"
    assert response.execution_state == scan_run.ScanRun.ExecutionState.QUEUED
    assert response.result_state == scan_run.ScanRun.ResultState.SUCCESS
    assert response.urls_crawled_count == 1935
    assert response.urls_tested_count == 1846
    assert response.has_vulnerabilities is True
    assert response.progress_percent == 1733


def test_stop_scan_run_rest_required_fields(
    request_type=web_security_scanner.StopScanRunRequest,
):
    transport_class = transports.WebSecurityScannerRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).stop_scan_run._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).stop_scan_run._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = scan_run.ScanRun()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = scan_run.ScanRun.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.stop_scan_run(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_stop_scan_run_rest_unset_required_fields():
    transport = transports.WebSecurityScannerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.stop_scan_run._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_stop_scan_run_rest_interceptors(null_interceptor):
    transport = transports.WebSecurityScannerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.WebSecurityScannerRestInterceptor(),
    )
    client = WebSecurityScannerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.WebSecurityScannerRestInterceptor, "post_stop_scan_run"
    ) as post, mock.patch.object(
        transports.WebSecurityScannerRestInterceptor, "pre_stop_scan_run"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = web_security_scanner.StopScanRunRequest.pb(
            web_security_scanner.StopScanRunRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = scan_run.ScanRun.to_json(scan_run.ScanRun())

        request = web_security_scanner.StopScanRunRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = scan_run.ScanRun()

        client.stop_scan_run(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_stop_scan_run_rest_bad_request(
    transport: str = "rest", request_type=web_security_scanner.StopScanRunRequest
):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/scanConfigs/sample2/scanRuns/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.stop_scan_run(request)


def test_stop_scan_run_rest_flattened():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = scan_run.ScanRun()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/scanConfigs/sample2/scanRuns/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = scan_run.ScanRun.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.stop_scan_run(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1beta/{name=projects/*/scanConfigs/*/scanRuns/*}:stop"
            % client.transport._host,
            args[1],
        )


def test_stop_scan_run_rest_flattened_error(transport: str = "rest"):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.stop_scan_run(
            web_security_scanner.StopScanRunRequest(),
            name="name_value",
        )


def test_stop_scan_run_rest_error():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        web_security_scanner.ListCrawledUrlsRequest,
        dict,
    ],
)
def test_list_crawled_urls_rest(request_type):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/scanConfigs/sample2/scanRuns/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = web_security_scanner.ListCrawledUrlsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = web_security_scanner.ListCrawledUrlsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_crawled_urls(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCrawledUrlsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_crawled_urls_rest_required_fields(
    request_type=web_security_scanner.ListCrawledUrlsRequest,
):
    transport_class = transports.WebSecurityScannerRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_crawled_urls._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_crawled_urls._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = web_security_scanner.ListCrawledUrlsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = web_security_scanner.ListCrawledUrlsResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_crawled_urls(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_crawled_urls_rest_unset_required_fields():
    transport = transports.WebSecurityScannerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_crawled_urls._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_crawled_urls_rest_interceptors(null_interceptor):
    transport = transports.WebSecurityScannerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.WebSecurityScannerRestInterceptor(),
    )
    client = WebSecurityScannerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.WebSecurityScannerRestInterceptor, "post_list_crawled_urls"
    ) as post, mock.patch.object(
        transports.WebSecurityScannerRestInterceptor, "pre_list_crawled_urls"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = web_security_scanner.ListCrawledUrlsRequest.pb(
            web_security_scanner.ListCrawledUrlsRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = (
            web_security_scanner.ListCrawledUrlsResponse.to_json(
                web_security_scanner.ListCrawledUrlsResponse()
            )
        )

        request = web_security_scanner.ListCrawledUrlsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = web_security_scanner.ListCrawledUrlsResponse()

        client.list_crawled_urls(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_crawled_urls_rest_bad_request(
    transport: str = "rest", request_type=web_security_scanner.ListCrawledUrlsRequest
):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/scanConfigs/sample2/scanRuns/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_crawled_urls(request)


def test_list_crawled_urls_rest_flattened():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = web_security_scanner.ListCrawledUrlsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/scanConfigs/sample2/scanRuns/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = web_security_scanner.ListCrawledUrlsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_crawled_urls(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1beta/{parent=projects/*/scanConfigs/*/scanRuns/*}/crawledUrls"
            % client.transport._host,
            args[1],
        )


def test_list_crawled_urls_rest_flattened_error(transport: str = "rest"):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_crawled_urls(
            web_security_scanner.ListCrawledUrlsRequest(),
            parent="parent_value",
        )


def test_list_crawled_urls_rest_pager(transport: str = "rest"):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            web_security_scanner.ListCrawledUrlsResponse(
                crawled_urls=[
                    crawled_url.CrawledUrl(),
                    crawled_url.CrawledUrl(),
                    crawled_url.CrawledUrl(),
                ],
                next_page_token="abc",
            ),
            web_security_scanner.ListCrawledUrlsResponse(
                crawled_urls=[],
                next_page_token="def",
            ),
            web_security_scanner.ListCrawledUrlsResponse(
                crawled_urls=[
                    crawled_url.CrawledUrl(),
                ],
                next_page_token="ghi",
            ),
            web_security_scanner.ListCrawledUrlsResponse(
                crawled_urls=[
                    crawled_url.CrawledUrl(),
                    crawled_url.CrawledUrl(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            web_security_scanner.ListCrawledUrlsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/scanConfigs/sample2/scanRuns/sample3"
        }

        pager = client.list_crawled_urls(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, crawled_url.CrawledUrl) for i in results)

        pages = list(client.list_crawled_urls(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        web_security_scanner.GetFindingRequest,
        dict,
    ],
)
def test_get_finding_rest(request_type):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/scanConfigs/sample2/scanRuns/sample3/findings/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = finding.Finding(
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

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = finding.Finding.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_finding(request)

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


def test_get_finding_rest_required_fields(
    request_type=web_security_scanner.GetFindingRequest,
):
    transport_class = transports.WebSecurityScannerRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_finding._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_finding._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = finding.Finding()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = finding.Finding.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_finding(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_finding_rest_unset_required_fields():
    transport = transports.WebSecurityScannerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_finding._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_finding_rest_interceptors(null_interceptor):
    transport = transports.WebSecurityScannerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.WebSecurityScannerRestInterceptor(),
    )
    client = WebSecurityScannerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.WebSecurityScannerRestInterceptor, "post_get_finding"
    ) as post, mock.patch.object(
        transports.WebSecurityScannerRestInterceptor, "pre_get_finding"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = web_security_scanner.GetFindingRequest.pb(
            web_security_scanner.GetFindingRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = finding.Finding.to_json(finding.Finding())

        request = web_security_scanner.GetFindingRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = finding.Finding()

        client.get_finding(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_finding_rest_bad_request(
    transport: str = "rest", request_type=web_security_scanner.GetFindingRequest
):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/scanConfigs/sample2/scanRuns/sample3/findings/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_finding(request)


def test_get_finding_rest_flattened():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = finding.Finding()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/scanConfigs/sample2/scanRuns/sample3/findings/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = finding.Finding.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_finding(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1beta/{name=projects/*/scanConfigs/*/scanRuns/*/findings/*}"
            % client.transport._host,
            args[1],
        )


def test_get_finding_rest_flattened_error(transport: str = "rest"):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_finding(
            web_security_scanner.GetFindingRequest(),
            name="name_value",
        )


def test_get_finding_rest_error():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        web_security_scanner.ListFindingsRequest,
        dict,
    ],
)
def test_list_findings_rest(request_type):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/scanConfigs/sample2/scanRuns/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = web_security_scanner.ListFindingsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = web_security_scanner.ListFindingsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_findings(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListFindingsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_findings_rest_required_fields(
    request_type=web_security_scanner.ListFindingsRequest,
):
    transport_class = transports.WebSecurityScannerRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["filter"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped
    assert "filter" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_findings._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "filter" in jsonified_request
    assert jsonified_request["filter"] == request_init["filter"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["filter"] = "filter_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_findings._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "filter" in jsonified_request
    assert jsonified_request["filter"] == "filter_value"

    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = web_security_scanner.ListFindingsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = web_security_scanner.ListFindingsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_findings(request)

            expected_params = [
                (
                    "filter",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_findings_rest_unset_required_fields():
    transport = transports.WebSecurityScannerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_findings._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "pageSize",
                "pageToken",
            )
        )
        & set(
            (
                "parent",
                "filter",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_findings_rest_interceptors(null_interceptor):
    transport = transports.WebSecurityScannerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.WebSecurityScannerRestInterceptor(),
    )
    client = WebSecurityScannerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.WebSecurityScannerRestInterceptor, "post_list_findings"
    ) as post, mock.patch.object(
        transports.WebSecurityScannerRestInterceptor, "pre_list_findings"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = web_security_scanner.ListFindingsRequest.pb(
            web_security_scanner.ListFindingsRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = web_security_scanner.ListFindingsResponse.to_json(
            web_security_scanner.ListFindingsResponse()
        )

        request = web_security_scanner.ListFindingsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = web_security_scanner.ListFindingsResponse()

        client.list_findings(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_findings_rest_bad_request(
    transport: str = "rest", request_type=web_security_scanner.ListFindingsRequest
):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/scanConfigs/sample2/scanRuns/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_findings(request)


def test_list_findings_rest_flattened():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = web_security_scanner.ListFindingsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/scanConfigs/sample2/scanRuns/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            filter="filter_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = web_security_scanner.ListFindingsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_findings(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1beta/{parent=projects/*/scanConfigs/*/scanRuns/*}/findings"
            % client.transport._host,
            args[1],
        )


def test_list_findings_rest_flattened_error(transport: str = "rest"):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_findings(
            web_security_scanner.ListFindingsRequest(),
            parent="parent_value",
            filter="filter_value",
        )


def test_list_findings_rest_pager(transport: str = "rest"):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            web_security_scanner.ListFindingsResponse(
                findings=[
                    finding.Finding(),
                    finding.Finding(),
                    finding.Finding(),
                ],
                next_page_token="abc",
            ),
            web_security_scanner.ListFindingsResponse(
                findings=[],
                next_page_token="def",
            ),
            web_security_scanner.ListFindingsResponse(
                findings=[
                    finding.Finding(),
                ],
                next_page_token="ghi",
            ),
            web_security_scanner.ListFindingsResponse(
                findings=[
                    finding.Finding(),
                    finding.Finding(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            web_security_scanner.ListFindingsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/scanConfigs/sample2/scanRuns/sample3"
        }

        pager = client.list_findings(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, finding.Finding) for i in results)

        pages = list(client.list_findings(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        web_security_scanner.ListFindingTypeStatsRequest,
        dict,
    ],
)
def test_list_finding_type_stats_rest(request_type):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/scanConfigs/sample2/scanRuns/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = web_security_scanner.ListFindingTypeStatsResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = web_security_scanner.ListFindingTypeStatsResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_finding_type_stats(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, web_security_scanner.ListFindingTypeStatsResponse)


def test_list_finding_type_stats_rest_required_fields(
    request_type=web_security_scanner.ListFindingTypeStatsRequest,
):
    transport_class = transports.WebSecurityScannerRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_finding_type_stats._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_finding_type_stats._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = web_security_scanner.ListFindingTypeStatsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = web_security_scanner.ListFindingTypeStatsResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_finding_type_stats(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_finding_type_stats_rest_unset_required_fields():
    transport = transports.WebSecurityScannerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_finding_type_stats._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("parent",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_finding_type_stats_rest_interceptors(null_interceptor):
    transport = transports.WebSecurityScannerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.WebSecurityScannerRestInterceptor(),
    )
    client = WebSecurityScannerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.WebSecurityScannerRestInterceptor, "post_list_finding_type_stats"
    ) as post, mock.patch.object(
        transports.WebSecurityScannerRestInterceptor, "pre_list_finding_type_stats"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = web_security_scanner.ListFindingTypeStatsRequest.pb(
            web_security_scanner.ListFindingTypeStatsRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = (
            web_security_scanner.ListFindingTypeStatsResponse.to_json(
                web_security_scanner.ListFindingTypeStatsResponse()
            )
        )

        request = web_security_scanner.ListFindingTypeStatsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = web_security_scanner.ListFindingTypeStatsResponse()

        client.list_finding_type_stats(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_finding_type_stats_rest_bad_request(
    transport: str = "rest",
    request_type=web_security_scanner.ListFindingTypeStatsRequest,
):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/scanConfigs/sample2/scanRuns/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_finding_type_stats(request)


def test_list_finding_type_stats_rest_flattened():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = web_security_scanner.ListFindingTypeStatsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/scanConfigs/sample2/scanRuns/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = web_security_scanner.ListFindingTypeStatsResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_finding_type_stats(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1beta/{parent=projects/*/scanConfigs/*/scanRuns/*}/findingTypeStats"
            % client.transport._host,
            args[1],
        )


def test_list_finding_type_stats_rest_flattened_error(transport: str = "rest"):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_finding_type_stats(
            web_security_scanner.ListFindingTypeStatsRequest(),
            parent="parent_value",
        )


def test_list_finding_type_stats_rest_error():
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.WebSecurityScannerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = WebSecurityScannerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
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

    # It is an error to provide an api_key and a transport instance.
    transport = transports.WebSecurityScannerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = WebSecurityScannerClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = WebSecurityScannerClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.WebSecurityScannerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = WebSecurityScannerClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
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
        transports.WebSecurityScannerRestTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "rest",
    ],
)
def test_transport_kind(transport_name):
    transport = WebSecurityScannerClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.WebSecurityScannerGrpcTransport,
    )


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

    with pytest.raises(NotImplementedError):
        transport.close()

    # Catch all for all remaining methods and properties
    remainder = [
        "kind",
    ]
    for r in remainder:
        with pytest.raises(NotImplementedError):
            getattr(transport, r)()


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
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
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


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.WebSecurityScannerGrpcTransport,
        transports.WebSecurityScannerGrpcAsyncIOTransport,
    ],
)
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
        transports.WebSecurityScannerRestTransport,
    ],
)
def test_web_security_scanner_transport_auth_gdch_credentials(transport_class):
    host = "https://language.com"
    api_audience_tests = [None, "https://language2.com"]
    api_audience_expect = [host, "https://language2.com"]
    for t, e in zip(api_audience_tests, api_audience_expect):
        with mock.patch.object(google.auth, "default", autospec=True) as adc:
            gdch_mock = mock.MagicMock()
            type(gdch_mock).with_gdch_audience = mock.PropertyMock(
                return_value=gdch_mock
            )
            adc.return_value = (gdch_mock, None)
            transport_class(host=host, api_audience=t)
            gdch_mock.with_gdch_audience.assert_called_once_with(e)


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


def test_web_security_scanner_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.WebSecurityScannerRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_web_security_scanner_host_no_port(transport_name):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="websecurityscanner.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "websecurityscanner.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://websecurityscanner.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_web_security_scanner_host_with_port(transport_name):
    client = WebSecurityScannerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="websecurityscanner.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "websecurityscanner.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://websecurityscanner.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_web_security_scanner_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = WebSecurityScannerClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = WebSecurityScannerClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.create_scan_config._session
    session2 = client2.transport.create_scan_config._session
    assert session1 != session2
    session1 = client1.transport.delete_scan_config._session
    session2 = client2.transport.delete_scan_config._session
    assert session1 != session2
    session1 = client1.transport.get_scan_config._session
    session2 = client2.transport.get_scan_config._session
    assert session1 != session2
    session1 = client1.transport.list_scan_configs._session
    session2 = client2.transport.list_scan_configs._session
    assert session1 != session2
    session1 = client1.transport.update_scan_config._session
    session2 = client2.transport.update_scan_config._session
    assert session1 != session2
    session1 = client1.transport.start_scan_run._session
    session2 = client2.transport.start_scan_run._session
    assert session1 != session2
    session1 = client1.transport.get_scan_run._session
    session2 = client2.transport.get_scan_run._session
    assert session1 != session2
    session1 = client1.transport.list_scan_runs._session
    session2 = client2.transport.list_scan_runs._session
    assert session1 != session2
    session1 = client1.transport.stop_scan_run._session
    session2 = client2.transport.stop_scan_run._session
    assert session1 != session2
    session1 = client1.transport.list_crawled_urls._session
    session2 = client2.transport.list_crawled_urls._session
    assert session1 != session2
    session1 = client1.transport.get_finding._session
    session2 = client2.transport.get_finding._session
    assert session1 != session2
    session1 = client1.transport.list_findings._session
    session2 = client2.transport.list_findings._session
    assert session1 != session2
    session1 = client1.transport.list_finding_type_stats._session
    session2 = client2.transport.list_finding_type_stats._session
    assert session1 != session2


def test_web_security_scanner_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.WebSecurityScannerGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_web_security_scanner_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.WebSecurityScannerGrpcAsyncIOTransport(
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
        project=project,
        scan_config=scan_config,
        scan_run=scan_run,
        finding=finding,
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
        project=project,
        scan_config=scan_config,
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
    expected = (
        "projects/{project}/scanConfigs/{scan_config}/scanRuns/{scan_run}".format(
            project=project,
            scan_config=scan_config,
            scan_run=scan_run,
        )
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
    expected = "folders/{folder}".format(
        folder=folder,
    )
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
    expected = "organizations/{organization}".format(
        organization=organization,
    )
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
    expected = "projects/{project}".format(
        project=project,
    )
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
        project=project,
        location=location,
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


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.WebSecurityScannerTransport, "_prep_wrapped_messages"
    ) as prep:
        client = WebSecurityScannerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.WebSecurityScannerTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = WebSecurityScannerClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = WebSecurityScannerAsyncClient(
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
        "rest": "_session",
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = WebSecurityScannerClient(
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
        "rest",
        "grpc",
    ]
    for transport in transports:
        client = WebSecurityScannerClient(
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
        (WebSecurityScannerClient, transports.WebSecurityScannerGrpcTransport),
        (
            WebSecurityScannerAsyncClient,
            transports.WebSecurityScannerGrpcAsyncIOTransport,
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
                api_audience=None,
            )
