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

from google.api_core import (
    future,
    gapic_v1,
    grpc_helpers,
    grpc_helpers_async,
    operation,
    operations_v1,
    path_template,
)
from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import operation_async  # type: ignore
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.location import locations_pb2
from google.longrunning import operations_pb2  # type: ignore
from google.oauth2 import service_account
from google.protobuf import empty_pb2  # type: ignore
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

from google.cloud.telcoautomation_v1.services.telco_automation import (
    TelcoAutomationAsyncClient,
    TelcoAutomationClient,
    pagers,
    transports,
)
from google.cloud.telcoautomation_v1.types import telcoautomation


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

    assert TelcoAutomationClient._get_default_mtls_endpoint(None) is None
    assert (
        TelcoAutomationClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        TelcoAutomationClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        TelcoAutomationClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        TelcoAutomationClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        TelcoAutomationClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (TelcoAutomationClient, "grpc"),
        (TelcoAutomationAsyncClient, "grpc_asyncio"),
        (TelcoAutomationClient, "rest"),
    ],
)
def test_telco_automation_client_from_service_account_info(
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
            "telcoautomation.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://telcoautomation.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.TelcoAutomationGrpcTransport, "grpc"),
        (transports.TelcoAutomationGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.TelcoAutomationRestTransport, "rest"),
    ],
)
def test_telco_automation_client_service_account_always_use_jwt(
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
        (TelcoAutomationClient, "grpc"),
        (TelcoAutomationAsyncClient, "grpc_asyncio"),
        (TelcoAutomationClient, "rest"),
    ],
)
def test_telco_automation_client_from_service_account_file(
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
            "telcoautomation.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://telcoautomation.googleapis.com"
        )


def test_telco_automation_client_get_transport_class():
    transport = TelcoAutomationClient.get_transport_class()
    available_transports = [
        transports.TelcoAutomationGrpcTransport,
        transports.TelcoAutomationRestTransport,
    ]
    assert transport in available_transports

    transport = TelcoAutomationClient.get_transport_class("grpc")
    assert transport == transports.TelcoAutomationGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (TelcoAutomationClient, transports.TelcoAutomationGrpcTransport, "grpc"),
        (
            TelcoAutomationAsyncClient,
            transports.TelcoAutomationGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (TelcoAutomationClient, transports.TelcoAutomationRestTransport, "rest"),
    ],
)
@mock.patch.object(
    TelcoAutomationClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(TelcoAutomationClient),
)
@mock.patch.object(
    TelcoAutomationAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(TelcoAutomationAsyncClient),
)
def test_telco_automation_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(TelcoAutomationClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(TelcoAutomationClient, "get_transport_class") as gtc:
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
            TelcoAutomationClient,
            transports.TelcoAutomationGrpcTransport,
            "grpc",
            "true",
        ),
        (
            TelcoAutomationAsyncClient,
            transports.TelcoAutomationGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            TelcoAutomationClient,
            transports.TelcoAutomationGrpcTransport,
            "grpc",
            "false",
        ),
        (
            TelcoAutomationAsyncClient,
            transports.TelcoAutomationGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (
            TelcoAutomationClient,
            transports.TelcoAutomationRestTransport,
            "rest",
            "true",
        ),
        (
            TelcoAutomationClient,
            transports.TelcoAutomationRestTransport,
            "rest",
            "false",
        ),
    ],
)
@mock.patch.object(
    TelcoAutomationClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(TelcoAutomationClient),
)
@mock.patch.object(
    TelcoAutomationAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(TelcoAutomationAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_telco_automation_client_mtls_env_auto(
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
    "client_class", [TelcoAutomationClient, TelcoAutomationAsyncClient]
)
@mock.patch.object(
    TelcoAutomationClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(TelcoAutomationClient),
)
@mock.patch.object(
    TelcoAutomationAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(TelcoAutomationAsyncClient),
)
def test_telco_automation_client_get_mtls_endpoint_and_cert_source(client_class):
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
        (TelcoAutomationClient, transports.TelcoAutomationGrpcTransport, "grpc"),
        (
            TelcoAutomationAsyncClient,
            transports.TelcoAutomationGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (TelcoAutomationClient, transports.TelcoAutomationRestTransport, "rest"),
    ],
)
def test_telco_automation_client_client_options_scopes(
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
            TelcoAutomationClient,
            transports.TelcoAutomationGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            TelcoAutomationAsyncClient,
            transports.TelcoAutomationGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (TelcoAutomationClient, transports.TelcoAutomationRestTransport, "rest", None),
    ],
)
def test_telco_automation_client_client_options_credentials_file(
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


def test_telco_automation_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.telcoautomation_v1.services.telco_automation.transports.TelcoAutomationGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = TelcoAutomationClient(
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
            TelcoAutomationClient,
            transports.TelcoAutomationGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            TelcoAutomationAsyncClient,
            transports.TelcoAutomationGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_telco_automation_client_create_channel_credentials_file(
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
            "telcoautomation.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="telcoautomation.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.ListOrchestrationClustersRequest,
        dict,
    ],
)
def test_list_orchestration_clusters(request_type, transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_orchestration_clusters), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.ListOrchestrationClustersResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_orchestration_clusters(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ListOrchestrationClustersRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListOrchestrationClustersPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_orchestration_clusters_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_orchestration_clusters), "__call__"
    ) as call:
        client.list_orchestration_clusters()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ListOrchestrationClustersRequest()


@pytest.mark.asyncio
async def test_list_orchestration_clusters_async(
    transport: str = "grpc_asyncio",
    request_type=telcoautomation.ListOrchestrationClustersRequest,
):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_orchestration_clusters), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.ListOrchestrationClustersResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_orchestration_clusters(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ListOrchestrationClustersRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListOrchestrationClustersAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_orchestration_clusters_async_from_dict():
    await test_list_orchestration_clusters_async(request_type=dict)


def test_list_orchestration_clusters_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.ListOrchestrationClustersRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_orchestration_clusters), "__call__"
    ) as call:
        call.return_value = telcoautomation.ListOrchestrationClustersResponse()
        client.list_orchestration_clusters(request)

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
async def test_list_orchestration_clusters_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.ListOrchestrationClustersRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_orchestration_clusters), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.ListOrchestrationClustersResponse()
        )
        await client.list_orchestration_clusters(request)

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


def test_list_orchestration_clusters_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_orchestration_clusters), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.ListOrchestrationClustersResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_orchestration_clusters(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_orchestration_clusters_flattened_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_orchestration_clusters(
            telcoautomation.ListOrchestrationClustersRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_orchestration_clusters_flattened_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_orchestration_clusters), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.ListOrchestrationClustersResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.ListOrchestrationClustersResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_orchestration_clusters(
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
async def test_list_orchestration_clusters_flattened_error_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_orchestration_clusters(
            telcoautomation.ListOrchestrationClustersRequest(),
            parent="parent_value",
        )


def test_list_orchestration_clusters_pager(transport_name: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_orchestration_clusters), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.ListOrchestrationClustersResponse(
                orchestration_clusters=[
                    telcoautomation.OrchestrationCluster(),
                    telcoautomation.OrchestrationCluster(),
                    telcoautomation.OrchestrationCluster(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListOrchestrationClustersResponse(
                orchestration_clusters=[],
                next_page_token="def",
            ),
            telcoautomation.ListOrchestrationClustersResponse(
                orchestration_clusters=[
                    telcoautomation.OrchestrationCluster(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListOrchestrationClustersResponse(
                orchestration_clusters=[
                    telcoautomation.OrchestrationCluster(),
                    telcoautomation.OrchestrationCluster(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_orchestration_clusters(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, telcoautomation.OrchestrationCluster) for i in results)


def test_list_orchestration_clusters_pages(transport_name: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_orchestration_clusters), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.ListOrchestrationClustersResponse(
                orchestration_clusters=[
                    telcoautomation.OrchestrationCluster(),
                    telcoautomation.OrchestrationCluster(),
                    telcoautomation.OrchestrationCluster(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListOrchestrationClustersResponse(
                orchestration_clusters=[],
                next_page_token="def",
            ),
            telcoautomation.ListOrchestrationClustersResponse(
                orchestration_clusters=[
                    telcoautomation.OrchestrationCluster(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListOrchestrationClustersResponse(
                orchestration_clusters=[
                    telcoautomation.OrchestrationCluster(),
                    telcoautomation.OrchestrationCluster(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_orchestration_clusters(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_orchestration_clusters_async_pager():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_orchestration_clusters),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.ListOrchestrationClustersResponse(
                orchestration_clusters=[
                    telcoautomation.OrchestrationCluster(),
                    telcoautomation.OrchestrationCluster(),
                    telcoautomation.OrchestrationCluster(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListOrchestrationClustersResponse(
                orchestration_clusters=[],
                next_page_token="def",
            ),
            telcoautomation.ListOrchestrationClustersResponse(
                orchestration_clusters=[
                    telcoautomation.OrchestrationCluster(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListOrchestrationClustersResponse(
                orchestration_clusters=[
                    telcoautomation.OrchestrationCluster(),
                    telcoautomation.OrchestrationCluster(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_orchestration_clusters(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, telcoautomation.OrchestrationCluster) for i in responses
        )


@pytest.mark.asyncio
async def test_list_orchestration_clusters_async_pages():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_orchestration_clusters),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.ListOrchestrationClustersResponse(
                orchestration_clusters=[
                    telcoautomation.OrchestrationCluster(),
                    telcoautomation.OrchestrationCluster(),
                    telcoautomation.OrchestrationCluster(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListOrchestrationClustersResponse(
                orchestration_clusters=[],
                next_page_token="def",
            ),
            telcoautomation.ListOrchestrationClustersResponse(
                orchestration_clusters=[
                    telcoautomation.OrchestrationCluster(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListOrchestrationClustersResponse(
                orchestration_clusters=[
                    telcoautomation.OrchestrationCluster(),
                    telcoautomation.OrchestrationCluster(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_orchestration_clusters(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.GetOrchestrationClusterRequest,
        dict,
    ],
)
def test_get_orchestration_cluster(request_type, transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_orchestration_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.OrchestrationCluster(
            name="name_value",
            tna_version="tna_version_value",
            state=telcoautomation.OrchestrationCluster.State.CREATING,
        )
        response = client.get_orchestration_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.GetOrchestrationClusterRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.OrchestrationCluster)
    assert response.name == "name_value"
    assert response.tna_version == "tna_version_value"
    assert response.state == telcoautomation.OrchestrationCluster.State.CREATING


def test_get_orchestration_cluster_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_orchestration_cluster), "__call__"
    ) as call:
        client.get_orchestration_cluster()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.GetOrchestrationClusterRequest()


@pytest.mark.asyncio
async def test_get_orchestration_cluster_async(
    transport: str = "grpc_asyncio",
    request_type=telcoautomation.GetOrchestrationClusterRequest,
):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_orchestration_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.OrchestrationCluster(
                name="name_value",
                tna_version="tna_version_value",
                state=telcoautomation.OrchestrationCluster.State.CREATING,
            )
        )
        response = await client.get_orchestration_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.GetOrchestrationClusterRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.OrchestrationCluster)
    assert response.name == "name_value"
    assert response.tna_version == "tna_version_value"
    assert response.state == telcoautomation.OrchestrationCluster.State.CREATING


@pytest.mark.asyncio
async def test_get_orchestration_cluster_async_from_dict():
    await test_get_orchestration_cluster_async(request_type=dict)


def test_get_orchestration_cluster_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.GetOrchestrationClusterRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_orchestration_cluster), "__call__"
    ) as call:
        call.return_value = telcoautomation.OrchestrationCluster()
        client.get_orchestration_cluster(request)

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
async def test_get_orchestration_cluster_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.GetOrchestrationClusterRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_orchestration_cluster), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.OrchestrationCluster()
        )
        await client.get_orchestration_cluster(request)

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


def test_get_orchestration_cluster_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_orchestration_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.OrchestrationCluster()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_orchestration_cluster(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_orchestration_cluster_flattened_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_orchestration_cluster(
            telcoautomation.GetOrchestrationClusterRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_orchestration_cluster_flattened_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_orchestration_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.OrchestrationCluster()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.OrchestrationCluster()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_orchestration_cluster(
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
async def test_get_orchestration_cluster_flattened_error_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_orchestration_cluster(
            telcoautomation.GetOrchestrationClusterRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.CreateOrchestrationClusterRequest,
        dict,
    ],
)
def test_create_orchestration_cluster(request_type, transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_orchestration_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_orchestration_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.CreateOrchestrationClusterRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_orchestration_cluster_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_orchestration_cluster), "__call__"
    ) as call:
        client.create_orchestration_cluster()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.CreateOrchestrationClusterRequest()


@pytest.mark.asyncio
async def test_create_orchestration_cluster_async(
    transport: str = "grpc_asyncio",
    request_type=telcoautomation.CreateOrchestrationClusterRequest,
):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_orchestration_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_orchestration_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.CreateOrchestrationClusterRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_orchestration_cluster_async_from_dict():
    await test_create_orchestration_cluster_async(request_type=dict)


def test_create_orchestration_cluster_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.CreateOrchestrationClusterRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_orchestration_cluster), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_orchestration_cluster(request)

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
async def test_create_orchestration_cluster_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.CreateOrchestrationClusterRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_orchestration_cluster), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_orchestration_cluster(request)

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


def test_create_orchestration_cluster_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_orchestration_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_orchestration_cluster(
            parent="parent_value",
            orchestration_cluster=telcoautomation.OrchestrationCluster(
                name="name_value"
            ),
            orchestration_cluster_id="orchestration_cluster_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].orchestration_cluster
        mock_val = telcoautomation.OrchestrationCluster(name="name_value")
        assert arg == mock_val
        arg = args[0].orchestration_cluster_id
        mock_val = "orchestration_cluster_id_value"
        assert arg == mock_val


def test_create_orchestration_cluster_flattened_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_orchestration_cluster(
            telcoautomation.CreateOrchestrationClusterRequest(),
            parent="parent_value",
            orchestration_cluster=telcoautomation.OrchestrationCluster(
                name="name_value"
            ),
            orchestration_cluster_id="orchestration_cluster_id_value",
        )


@pytest.mark.asyncio
async def test_create_orchestration_cluster_flattened_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_orchestration_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_orchestration_cluster(
            parent="parent_value",
            orchestration_cluster=telcoautomation.OrchestrationCluster(
                name="name_value"
            ),
            orchestration_cluster_id="orchestration_cluster_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].orchestration_cluster
        mock_val = telcoautomation.OrchestrationCluster(name="name_value")
        assert arg == mock_val
        arg = args[0].orchestration_cluster_id
        mock_val = "orchestration_cluster_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_orchestration_cluster_flattened_error_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_orchestration_cluster(
            telcoautomation.CreateOrchestrationClusterRequest(),
            parent="parent_value",
            orchestration_cluster=telcoautomation.OrchestrationCluster(
                name="name_value"
            ),
            orchestration_cluster_id="orchestration_cluster_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.DeleteOrchestrationClusterRequest,
        dict,
    ],
)
def test_delete_orchestration_cluster(request_type, transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_orchestration_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_orchestration_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.DeleteOrchestrationClusterRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_orchestration_cluster_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_orchestration_cluster), "__call__"
    ) as call:
        client.delete_orchestration_cluster()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.DeleteOrchestrationClusterRequest()


@pytest.mark.asyncio
async def test_delete_orchestration_cluster_async(
    transport: str = "grpc_asyncio",
    request_type=telcoautomation.DeleteOrchestrationClusterRequest,
):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_orchestration_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_orchestration_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.DeleteOrchestrationClusterRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_orchestration_cluster_async_from_dict():
    await test_delete_orchestration_cluster_async(request_type=dict)


def test_delete_orchestration_cluster_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.DeleteOrchestrationClusterRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_orchestration_cluster), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_orchestration_cluster(request)

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
async def test_delete_orchestration_cluster_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.DeleteOrchestrationClusterRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_orchestration_cluster), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_orchestration_cluster(request)

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


def test_delete_orchestration_cluster_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_orchestration_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_orchestration_cluster(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_orchestration_cluster_flattened_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_orchestration_cluster(
            telcoautomation.DeleteOrchestrationClusterRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_orchestration_cluster_flattened_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_orchestration_cluster), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_orchestration_cluster(
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
async def test_delete_orchestration_cluster_flattened_error_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_orchestration_cluster(
            telcoautomation.DeleteOrchestrationClusterRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.ListEdgeSlmsRequest,
        dict,
    ],
)
def test_list_edge_slms(request_type, transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_edge_slms), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.ListEdgeSlmsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_edge_slms(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ListEdgeSlmsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListEdgeSlmsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_edge_slms_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_edge_slms), "__call__") as call:
        client.list_edge_slms()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ListEdgeSlmsRequest()


@pytest.mark.asyncio
async def test_list_edge_slms_async(
    transport: str = "grpc_asyncio", request_type=telcoautomation.ListEdgeSlmsRequest
):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_edge_slms), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.ListEdgeSlmsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_edge_slms(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ListEdgeSlmsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListEdgeSlmsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_edge_slms_async_from_dict():
    await test_list_edge_slms_async(request_type=dict)


def test_list_edge_slms_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.ListEdgeSlmsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_edge_slms), "__call__") as call:
        call.return_value = telcoautomation.ListEdgeSlmsResponse()
        client.list_edge_slms(request)

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
async def test_list_edge_slms_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.ListEdgeSlmsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_edge_slms), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.ListEdgeSlmsResponse()
        )
        await client.list_edge_slms(request)

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


def test_list_edge_slms_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_edge_slms), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.ListEdgeSlmsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_edge_slms(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_edge_slms_flattened_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_edge_slms(
            telcoautomation.ListEdgeSlmsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_edge_slms_flattened_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_edge_slms), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.ListEdgeSlmsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.ListEdgeSlmsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_edge_slms(
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
async def test_list_edge_slms_flattened_error_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_edge_slms(
            telcoautomation.ListEdgeSlmsRequest(),
            parent="parent_value",
        )


def test_list_edge_slms_pager(transport_name: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_edge_slms), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.ListEdgeSlmsResponse(
                edge_slms=[
                    telcoautomation.EdgeSlm(),
                    telcoautomation.EdgeSlm(),
                    telcoautomation.EdgeSlm(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListEdgeSlmsResponse(
                edge_slms=[],
                next_page_token="def",
            ),
            telcoautomation.ListEdgeSlmsResponse(
                edge_slms=[
                    telcoautomation.EdgeSlm(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListEdgeSlmsResponse(
                edge_slms=[
                    telcoautomation.EdgeSlm(),
                    telcoautomation.EdgeSlm(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_edge_slms(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, telcoautomation.EdgeSlm) for i in results)


def test_list_edge_slms_pages(transport_name: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_edge_slms), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.ListEdgeSlmsResponse(
                edge_slms=[
                    telcoautomation.EdgeSlm(),
                    telcoautomation.EdgeSlm(),
                    telcoautomation.EdgeSlm(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListEdgeSlmsResponse(
                edge_slms=[],
                next_page_token="def",
            ),
            telcoautomation.ListEdgeSlmsResponse(
                edge_slms=[
                    telcoautomation.EdgeSlm(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListEdgeSlmsResponse(
                edge_slms=[
                    telcoautomation.EdgeSlm(),
                    telcoautomation.EdgeSlm(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_edge_slms(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_edge_slms_async_pager():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_edge_slms), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.ListEdgeSlmsResponse(
                edge_slms=[
                    telcoautomation.EdgeSlm(),
                    telcoautomation.EdgeSlm(),
                    telcoautomation.EdgeSlm(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListEdgeSlmsResponse(
                edge_slms=[],
                next_page_token="def",
            ),
            telcoautomation.ListEdgeSlmsResponse(
                edge_slms=[
                    telcoautomation.EdgeSlm(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListEdgeSlmsResponse(
                edge_slms=[
                    telcoautomation.EdgeSlm(),
                    telcoautomation.EdgeSlm(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_edge_slms(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, telcoautomation.EdgeSlm) for i in responses)


@pytest.mark.asyncio
async def test_list_edge_slms_async_pages():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_edge_slms), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.ListEdgeSlmsResponse(
                edge_slms=[
                    telcoautomation.EdgeSlm(),
                    telcoautomation.EdgeSlm(),
                    telcoautomation.EdgeSlm(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListEdgeSlmsResponse(
                edge_slms=[],
                next_page_token="def",
            ),
            telcoautomation.ListEdgeSlmsResponse(
                edge_slms=[
                    telcoautomation.EdgeSlm(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListEdgeSlmsResponse(
                edge_slms=[
                    telcoautomation.EdgeSlm(),
                    telcoautomation.EdgeSlm(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_edge_slms(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.GetEdgeSlmRequest,
        dict,
    ],
)
def test_get_edge_slm(request_type, transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_edge_slm), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.EdgeSlm(
            name="name_value",
            orchestration_cluster="orchestration_cluster_value",
            tna_version="tna_version_value",
            state=telcoautomation.EdgeSlm.State.CREATING,
            workload_cluster_type=telcoautomation.EdgeSlm.WorkloadClusterType.GDCE,
        )
        response = client.get_edge_slm(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.GetEdgeSlmRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.EdgeSlm)
    assert response.name == "name_value"
    assert response.orchestration_cluster == "orchestration_cluster_value"
    assert response.tna_version == "tna_version_value"
    assert response.state == telcoautomation.EdgeSlm.State.CREATING
    assert (
        response.workload_cluster_type
        == telcoautomation.EdgeSlm.WorkloadClusterType.GDCE
    )


def test_get_edge_slm_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_edge_slm), "__call__") as call:
        client.get_edge_slm()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.GetEdgeSlmRequest()


@pytest.mark.asyncio
async def test_get_edge_slm_async(
    transport: str = "grpc_asyncio", request_type=telcoautomation.GetEdgeSlmRequest
):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_edge_slm), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.EdgeSlm(
                name="name_value",
                orchestration_cluster="orchestration_cluster_value",
                tna_version="tna_version_value",
                state=telcoautomation.EdgeSlm.State.CREATING,
                workload_cluster_type=telcoautomation.EdgeSlm.WorkloadClusterType.GDCE,
            )
        )
        response = await client.get_edge_slm(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.GetEdgeSlmRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.EdgeSlm)
    assert response.name == "name_value"
    assert response.orchestration_cluster == "orchestration_cluster_value"
    assert response.tna_version == "tna_version_value"
    assert response.state == telcoautomation.EdgeSlm.State.CREATING
    assert (
        response.workload_cluster_type
        == telcoautomation.EdgeSlm.WorkloadClusterType.GDCE
    )


@pytest.mark.asyncio
async def test_get_edge_slm_async_from_dict():
    await test_get_edge_slm_async(request_type=dict)


def test_get_edge_slm_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.GetEdgeSlmRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_edge_slm), "__call__") as call:
        call.return_value = telcoautomation.EdgeSlm()
        client.get_edge_slm(request)

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
async def test_get_edge_slm_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.GetEdgeSlmRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_edge_slm), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.EdgeSlm()
        )
        await client.get_edge_slm(request)

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


def test_get_edge_slm_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_edge_slm), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.EdgeSlm()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_edge_slm(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_edge_slm_flattened_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_edge_slm(
            telcoautomation.GetEdgeSlmRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_edge_slm_flattened_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_edge_slm), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.EdgeSlm()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.EdgeSlm()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_edge_slm(
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
async def test_get_edge_slm_flattened_error_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_edge_slm(
            telcoautomation.GetEdgeSlmRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.CreateEdgeSlmRequest,
        dict,
    ],
)
def test_create_edge_slm(request_type, transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_edge_slm), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_edge_slm(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.CreateEdgeSlmRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_edge_slm_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_edge_slm), "__call__") as call:
        client.create_edge_slm()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.CreateEdgeSlmRequest()


@pytest.mark.asyncio
async def test_create_edge_slm_async(
    transport: str = "grpc_asyncio", request_type=telcoautomation.CreateEdgeSlmRequest
):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_edge_slm), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_edge_slm(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.CreateEdgeSlmRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_edge_slm_async_from_dict():
    await test_create_edge_slm_async(request_type=dict)


def test_create_edge_slm_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.CreateEdgeSlmRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_edge_slm), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_edge_slm(request)

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
async def test_create_edge_slm_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.CreateEdgeSlmRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_edge_slm), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_edge_slm(request)

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


def test_create_edge_slm_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_edge_slm), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_edge_slm(
            parent="parent_value",
            edge_slm=telcoautomation.EdgeSlm(name="name_value"),
            edge_slm_id="edge_slm_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].edge_slm
        mock_val = telcoautomation.EdgeSlm(name="name_value")
        assert arg == mock_val
        arg = args[0].edge_slm_id
        mock_val = "edge_slm_id_value"
        assert arg == mock_val


def test_create_edge_slm_flattened_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_edge_slm(
            telcoautomation.CreateEdgeSlmRequest(),
            parent="parent_value",
            edge_slm=telcoautomation.EdgeSlm(name="name_value"),
            edge_slm_id="edge_slm_id_value",
        )


@pytest.mark.asyncio
async def test_create_edge_slm_flattened_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_edge_slm), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_edge_slm(
            parent="parent_value",
            edge_slm=telcoautomation.EdgeSlm(name="name_value"),
            edge_slm_id="edge_slm_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].edge_slm
        mock_val = telcoautomation.EdgeSlm(name="name_value")
        assert arg == mock_val
        arg = args[0].edge_slm_id
        mock_val = "edge_slm_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_edge_slm_flattened_error_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_edge_slm(
            telcoautomation.CreateEdgeSlmRequest(),
            parent="parent_value",
            edge_slm=telcoautomation.EdgeSlm(name="name_value"),
            edge_slm_id="edge_slm_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.DeleteEdgeSlmRequest,
        dict,
    ],
)
def test_delete_edge_slm(request_type, transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_edge_slm), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_edge_slm(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.DeleteEdgeSlmRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_edge_slm_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_edge_slm), "__call__") as call:
        client.delete_edge_slm()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.DeleteEdgeSlmRequest()


@pytest.mark.asyncio
async def test_delete_edge_slm_async(
    transport: str = "grpc_asyncio", request_type=telcoautomation.DeleteEdgeSlmRequest
):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_edge_slm), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_edge_slm(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.DeleteEdgeSlmRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_edge_slm_async_from_dict():
    await test_delete_edge_slm_async(request_type=dict)


def test_delete_edge_slm_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.DeleteEdgeSlmRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_edge_slm), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_edge_slm(request)

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
async def test_delete_edge_slm_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.DeleteEdgeSlmRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_edge_slm), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_edge_slm(request)

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


def test_delete_edge_slm_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_edge_slm), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_edge_slm(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_edge_slm_flattened_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_edge_slm(
            telcoautomation.DeleteEdgeSlmRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_edge_slm_flattened_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_edge_slm), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_edge_slm(
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
async def test_delete_edge_slm_flattened_error_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_edge_slm(
            telcoautomation.DeleteEdgeSlmRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.CreateBlueprintRequest,
        dict,
    ],
)
def test_create_blueprint(request_type, transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_blueprint), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.Blueprint(
            name="name_value",
            revision_id="revision_id_value",
            source_blueprint="source_blueprint_value",
            approval_state=telcoautomation.Blueprint.ApprovalState.DRAFT,
            display_name="display_name_value",
            repository="repository_value",
            source_provider="source_provider_value",
            deployment_level=telcoautomation.DeploymentLevel.HYDRATION,
            rollback_support=True,
        )
        response = client.create_blueprint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.CreateBlueprintRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.Blueprint)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.source_blueprint == "source_blueprint_value"
    assert response.approval_state == telcoautomation.Blueprint.ApprovalState.DRAFT
    assert response.display_name == "display_name_value"
    assert response.repository == "repository_value"
    assert response.source_provider == "source_provider_value"
    assert response.deployment_level == telcoautomation.DeploymentLevel.HYDRATION
    assert response.rollback_support is True


def test_create_blueprint_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_blueprint), "__call__") as call:
        client.create_blueprint()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.CreateBlueprintRequest()


@pytest.mark.asyncio
async def test_create_blueprint_async(
    transport: str = "grpc_asyncio", request_type=telcoautomation.CreateBlueprintRequest
):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_blueprint), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.Blueprint(
                name="name_value",
                revision_id="revision_id_value",
                source_blueprint="source_blueprint_value",
                approval_state=telcoautomation.Blueprint.ApprovalState.DRAFT,
                display_name="display_name_value",
                repository="repository_value",
                source_provider="source_provider_value",
                deployment_level=telcoautomation.DeploymentLevel.HYDRATION,
                rollback_support=True,
            )
        )
        response = await client.create_blueprint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.CreateBlueprintRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.Blueprint)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.source_blueprint == "source_blueprint_value"
    assert response.approval_state == telcoautomation.Blueprint.ApprovalState.DRAFT
    assert response.display_name == "display_name_value"
    assert response.repository == "repository_value"
    assert response.source_provider == "source_provider_value"
    assert response.deployment_level == telcoautomation.DeploymentLevel.HYDRATION
    assert response.rollback_support is True


@pytest.mark.asyncio
async def test_create_blueprint_async_from_dict():
    await test_create_blueprint_async(request_type=dict)


def test_create_blueprint_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.CreateBlueprintRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_blueprint), "__call__") as call:
        call.return_value = telcoautomation.Blueprint()
        client.create_blueprint(request)

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
async def test_create_blueprint_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.CreateBlueprintRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_blueprint), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.Blueprint()
        )
        await client.create_blueprint(request)

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


def test_create_blueprint_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_blueprint), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.Blueprint()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_blueprint(
            parent="parent_value",
            blueprint=telcoautomation.Blueprint(name="name_value"),
            blueprint_id="blueprint_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].blueprint
        mock_val = telcoautomation.Blueprint(name="name_value")
        assert arg == mock_val
        arg = args[0].blueprint_id
        mock_val = "blueprint_id_value"
        assert arg == mock_val


def test_create_blueprint_flattened_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_blueprint(
            telcoautomation.CreateBlueprintRequest(),
            parent="parent_value",
            blueprint=telcoautomation.Blueprint(name="name_value"),
            blueprint_id="blueprint_id_value",
        )


@pytest.mark.asyncio
async def test_create_blueprint_flattened_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_blueprint), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.Blueprint()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.Blueprint()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_blueprint(
            parent="parent_value",
            blueprint=telcoautomation.Blueprint(name="name_value"),
            blueprint_id="blueprint_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].blueprint
        mock_val = telcoautomation.Blueprint(name="name_value")
        assert arg == mock_val
        arg = args[0].blueprint_id
        mock_val = "blueprint_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_blueprint_flattened_error_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_blueprint(
            telcoautomation.CreateBlueprintRequest(),
            parent="parent_value",
            blueprint=telcoautomation.Blueprint(name="name_value"),
            blueprint_id="blueprint_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.UpdateBlueprintRequest,
        dict,
    ],
)
def test_update_blueprint(request_type, transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_blueprint), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.Blueprint(
            name="name_value",
            revision_id="revision_id_value",
            source_blueprint="source_blueprint_value",
            approval_state=telcoautomation.Blueprint.ApprovalState.DRAFT,
            display_name="display_name_value",
            repository="repository_value",
            source_provider="source_provider_value",
            deployment_level=telcoautomation.DeploymentLevel.HYDRATION,
            rollback_support=True,
        )
        response = client.update_blueprint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.UpdateBlueprintRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.Blueprint)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.source_blueprint == "source_blueprint_value"
    assert response.approval_state == telcoautomation.Blueprint.ApprovalState.DRAFT
    assert response.display_name == "display_name_value"
    assert response.repository == "repository_value"
    assert response.source_provider == "source_provider_value"
    assert response.deployment_level == telcoautomation.DeploymentLevel.HYDRATION
    assert response.rollback_support is True


def test_update_blueprint_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_blueprint), "__call__") as call:
        client.update_blueprint()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.UpdateBlueprintRequest()


@pytest.mark.asyncio
async def test_update_blueprint_async(
    transport: str = "grpc_asyncio", request_type=telcoautomation.UpdateBlueprintRequest
):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_blueprint), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.Blueprint(
                name="name_value",
                revision_id="revision_id_value",
                source_blueprint="source_blueprint_value",
                approval_state=telcoautomation.Blueprint.ApprovalState.DRAFT,
                display_name="display_name_value",
                repository="repository_value",
                source_provider="source_provider_value",
                deployment_level=telcoautomation.DeploymentLevel.HYDRATION,
                rollback_support=True,
            )
        )
        response = await client.update_blueprint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.UpdateBlueprintRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.Blueprint)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.source_blueprint == "source_blueprint_value"
    assert response.approval_state == telcoautomation.Blueprint.ApprovalState.DRAFT
    assert response.display_name == "display_name_value"
    assert response.repository == "repository_value"
    assert response.source_provider == "source_provider_value"
    assert response.deployment_level == telcoautomation.DeploymentLevel.HYDRATION
    assert response.rollback_support is True


@pytest.mark.asyncio
async def test_update_blueprint_async_from_dict():
    await test_update_blueprint_async(request_type=dict)


def test_update_blueprint_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.UpdateBlueprintRequest()

    request.blueprint.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_blueprint), "__call__") as call:
        call.return_value = telcoautomation.Blueprint()
        client.update_blueprint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "blueprint.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_blueprint_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.UpdateBlueprintRequest()

    request.blueprint.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_blueprint), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.Blueprint()
        )
        await client.update_blueprint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "blueprint.name=name_value",
    ) in kw["metadata"]


def test_update_blueprint_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_blueprint), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.Blueprint()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_blueprint(
            blueprint=telcoautomation.Blueprint(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].blueprint
        mock_val = telcoautomation.Blueprint(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_blueprint_flattened_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_blueprint(
            telcoautomation.UpdateBlueprintRequest(),
            blueprint=telcoautomation.Blueprint(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_blueprint_flattened_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_blueprint), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.Blueprint()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.Blueprint()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_blueprint(
            blueprint=telcoautomation.Blueprint(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].blueprint
        mock_val = telcoautomation.Blueprint(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_blueprint_flattened_error_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_blueprint(
            telcoautomation.UpdateBlueprintRequest(),
            blueprint=telcoautomation.Blueprint(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.GetBlueprintRequest,
        dict,
    ],
)
def test_get_blueprint(request_type, transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_blueprint), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.Blueprint(
            name="name_value",
            revision_id="revision_id_value",
            source_blueprint="source_blueprint_value",
            approval_state=telcoautomation.Blueprint.ApprovalState.DRAFT,
            display_name="display_name_value",
            repository="repository_value",
            source_provider="source_provider_value",
            deployment_level=telcoautomation.DeploymentLevel.HYDRATION,
            rollback_support=True,
        )
        response = client.get_blueprint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.GetBlueprintRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.Blueprint)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.source_blueprint == "source_blueprint_value"
    assert response.approval_state == telcoautomation.Blueprint.ApprovalState.DRAFT
    assert response.display_name == "display_name_value"
    assert response.repository == "repository_value"
    assert response.source_provider == "source_provider_value"
    assert response.deployment_level == telcoautomation.DeploymentLevel.HYDRATION
    assert response.rollback_support is True


def test_get_blueprint_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_blueprint), "__call__") as call:
        client.get_blueprint()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.GetBlueprintRequest()


@pytest.mark.asyncio
async def test_get_blueprint_async(
    transport: str = "grpc_asyncio", request_type=telcoautomation.GetBlueprintRequest
):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_blueprint), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.Blueprint(
                name="name_value",
                revision_id="revision_id_value",
                source_blueprint="source_blueprint_value",
                approval_state=telcoautomation.Blueprint.ApprovalState.DRAFT,
                display_name="display_name_value",
                repository="repository_value",
                source_provider="source_provider_value",
                deployment_level=telcoautomation.DeploymentLevel.HYDRATION,
                rollback_support=True,
            )
        )
        response = await client.get_blueprint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.GetBlueprintRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.Blueprint)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.source_blueprint == "source_blueprint_value"
    assert response.approval_state == telcoautomation.Blueprint.ApprovalState.DRAFT
    assert response.display_name == "display_name_value"
    assert response.repository == "repository_value"
    assert response.source_provider == "source_provider_value"
    assert response.deployment_level == telcoautomation.DeploymentLevel.HYDRATION
    assert response.rollback_support is True


@pytest.mark.asyncio
async def test_get_blueprint_async_from_dict():
    await test_get_blueprint_async(request_type=dict)


def test_get_blueprint_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.GetBlueprintRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_blueprint), "__call__") as call:
        call.return_value = telcoautomation.Blueprint()
        client.get_blueprint(request)

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
async def test_get_blueprint_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.GetBlueprintRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_blueprint), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.Blueprint()
        )
        await client.get_blueprint(request)

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


def test_get_blueprint_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_blueprint), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.Blueprint()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_blueprint(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_blueprint_flattened_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_blueprint(
            telcoautomation.GetBlueprintRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_blueprint_flattened_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_blueprint), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.Blueprint()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.Blueprint()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_blueprint(
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
async def test_get_blueprint_flattened_error_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_blueprint(
            telcoautomation.GetBlueprintRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.DeleteBlueprintRequest,
        dict,
    ],
)
def test_delete_blueprint(request_type, transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_blueprint), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_blueprint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.DeleteBlueprintRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_blueprint_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_blueprint), "__call__") as call:
        client.delete_blueprint()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.DeleteBlueprintRequest()


@pytest.mark.asyncio
async def test_delete_blueprint_async(
    transport: str = "grpc_asyncio", request_type=telcoautomation.DeleteBlueprintRequest
):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_blueprint), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_blueprint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.DeleteBlueprintRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_blueprint_async_from_dict():
    await test_delete_blueprint_async(request_type=dict)


def test_delete_blueprint_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.DeleteBlueprintRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_blueprint), "__call__") as call:
        call.return_value = None
        client.delete_blueprint(request)

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
async def test_delete_blueprint_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.DeleteBlueprintRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_blueprint), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_blueprint(request)

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


def test_delete_blueprint_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_blueprint), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_blueprint(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_blueprint_flattened_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_blueprint(
            telcoautomation.DeleteBlueprintRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_blueprint_flattened_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_blueprint), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_blueprint(
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
async def test_delete_blueprint_flattened_error_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_blueprint(
            telcoautomation.DeleteBlueprintRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.ListBlueprintsRequest,
        dict,
    ],
)
def test_list_blueprints(request_type, transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_blueprints), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.ListBlueprintsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_blueprints(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ListBlueprintsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBlueprintsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_blueprints_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_blueprints), "__call__") as call:
        client.list_blueprints()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ListBlueprintsRequest()


@pytest.mark.asyncio
async def test_list_blueprints_async(
    transport: str = "grpc_asyncio", request_type=telcoautomation.ListBlueprintsRequest
):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_blueprints), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.ListBlueprintsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_blueprints(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ListBlueprintsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBlueprintsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_blueprints_async_from_dict():
    await test_list_blueprints_async(request_type=dict)


def test_list_blueprints_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.ListBlueprintsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_blueprints), "__call__") as call:
        call.return_value = telcoautomation.ListBlueprintsResponse()
        client.list_blueprints(request)

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
async def test_list_blueprints_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.ListBlueprintsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_blueprints), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.ListBlueprintsResponse()
        )
        await client.list_blueprints(request)

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


def test_list_blueprints_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_blueprints), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.ListBlueprintsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_blueprints(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_blueprints_flattened_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_blueprints(
            telcoautomation.ListBlueprintsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_blueprints_flattened_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_blueprints), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.ListBlueprintsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.ListBlueprintsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_blueprints(
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
async def test_list_blueprints_flattened_error_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_blueprints(
            telcoautomation.ListBlueprintsRequest(),
            parent="parent_value",
        )


def test_list_blueprints_pager(transport_name: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_blueprints), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.ListBlueprintsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListBlueprintsResponse(
                blueprints=[],
                next_page_token="def",
            ),
            telcoautomation.ListBlueprintsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListBlueprintsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_blueprints(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, telcoautomation.Blueprint) for i in results)


def test_list_blueprints_pages(transport_name: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_blueprints), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.ListBlueprintsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListBlueprintsResponse(
                blueprints=[],
                next_page_token="def",
            ),
            telcoautomation.ListBlueprintsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListBlueprintsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_blueprints(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_blueprints_async_pager():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_blueprints), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.ListBlueprintsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListBlueprintsResponse(
                blueprints=[],
                next_page_token="def",
            ),
            telcoautomation.ListBlueprintsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListBlueprintsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_blueprints(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, telcoautomation.Blueprint) for i in responses)


@pytest.mark.asyncio
async def test_list_blueprints_async_pages():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_blueprints), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.ListBlueprintsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListBlueprintsResponse(
                blueprints=[],
                next_page_token="def",
            ),
            telcoautomation.ListBlueprintsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListBlueprintsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_blueprints(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.ApproveBlueprintRequest,
        dict,
    ],
)
def test_approve_blueprint(request_type, transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.approve_blueprint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.Blueprint(
            name="name_value",
            revision_id="revision_id_value",
            source_blueprint="source_blueprint_value",
            approval_state=telcoautomation.Blueprint.ApprovalState.DRAFT,
            display_name="display_name_value",
            repository="repository_value",
            source_provider="source_provider_value",
            deployment_level=telcoautomation.DeploymentLevel.HYDRATION,
            rollback_support=True,
        )
        response = client.approve_blueprint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ApproveBlueprintRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.Blueprint)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.source_blueprint == "source_blueprint_value"
    assert response.approval_state == telcoautomation.Blueprint.ApprovalState.DRAFT
    assert response.display_name == "display_name_value"
    assert response.repository == "repository_value"
    assert response.source_provider == "source_provider_value"
    assert response.deployment_level == telcoautomation.DeploymentLevel.HYDRATION
    assert response.rollback_support is True


def test_approve_blueprint_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.approve_blueprint), "__call__"
    ) as call:
        client.approve_blueprint()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ApproveBlueprintRequest()


@pytest.mark.asyncio
async def test_approve_blueprint_async(
    transport: str = "grpc_asyncio",
    request_type=telcoautomation.ApproveBlueprintRequest,
):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.approve_blueprint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.Blueprint(
                name="name_value",
                revision_id="revision_id_value",
                source_blueprint="source_blueprint_value",
                approval_state=telcoautomation.Blueprint.ApprovalState.DRAFT,
                display_name="display_name_value",
                repository="repository_value",
                source_provider="source_provider_value",
                deployment_level=telcoautomation.DeploymentLevel.HYDRATION,
                rollback_support=True,
            )
        )
        response = await client.approve_blueprint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ApproveBlueprintRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.Blueprint)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.source_blueprint == "source_blueprint_value"
    assert response.approval_state == telcoautomation.Blueprint.ApprovalState.DRAFT
    assert response.display_name == "display_name_value"
    assert response.repository == "repository_value"
    assert response.source_provider == "source_provider_value"
    assert response.deployment_level == telcoautomation.DeploymentLevel.HYDRATION
    assert response.rollback_support is True


@pytest.mark.asyncio
async def test_approve_blueprint_async_from_dict():
    await test_approve_blueprint_async(request_type=dict)


def test_approve_blueprint_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.ApproveBlueprintRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.approve_blueprint), "__call__"
    ) as call:
        call.return_value = telcoautomation.Blueprint()
        client.approve_blueprint(request)

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
async def test_approve_blueprint_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.ApproveBlueprintRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.approve_blueprint), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.Blueprint()
        )
        await client.approve_blueprint(request)

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


def test_approve_blueprint_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.approve_blueprint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.Blueprint()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.approve_blueprint(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_approve_blueprint_flattened_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.approve_blueprint(
            telcoautomation.ApproveBlueprintRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_approve_blueprint_flattened_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.approve_blueprint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.Blueprint()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.Blueprint()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.approve_blueprint(
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
async def test_approve_blueprint_flattened_error_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.approve_blueprint(
            telcoautomation.ApproveBlueprintRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.ProposeBlueprintRequest,
        dict,
    ],
)
def test_propose_blueprint(request_type, transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.propose_blueprint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.Blueprint(
            name="name_value",
            revision_id="revision_id_value",
            source_blueprint="source_blueprint_value",
            approval_state=telcoautomation.Blueprint.ApprovalState.DRAFT,
            display_name="display_name_value",
            repository="repository_value",
            source_provider="source_provider_value",
            deployment_level=telcoautomation.DeploymentLevel.HYDRATION,
            rollback_support=True,
        )
        response = client.propose_blueprint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ProposeBlueprintRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.Blueprint)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.source_blueprint == "source_blueprint_value"
    assert response.approval_state == telcoautomation.Blueprint.ApprovalState.DRAFT
    assert response.display_name == "display_name_value"
    assert response.repository == "repository_value"
    assert response.source_provider == "source_provider_value"
    assert response.deployment_level == telcoautomation.DeploymentLevel.HYDRATION
    assert response.rollback_support is True


def test_propose_blueprint_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.propose_blueprint), "__call__"
    ) as call:
        client.propose_blueprint()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ProposeBlueprintRequest()


@pytest.mark.asyncio
async def test_propose_blueprint_async(
    transport: str = "grpc_asyncio",
    request_type=telcoautomation.ProposeBlueprintRequest,
):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.propose_blueprint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.Blueprint(
                name="name_value",
                revision_id="revision_id_value",
                source_blueprint="source_blueprint_value",
                approval_state=telcoautomation.Blueprint.ApprovalState.DRAFT,
                display_name="display_name_value",
                repository="repository_value",
                source_provider="source_provider_value",
                deployment_level=telcoautomation.DeploymentLevel.HYDRATION,
                rollback_support=True,
            )
        )
        response = await client.propose_blueprint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ProposeBlueprintRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.Blueprint)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.source_blueprint == "source_blueprint_value"
    assert response.approval_state == telcoautomation.Blueprint.ApprovalState.DRAFT
    assert response.display_name == "display_name_value"
    assert response.repository == "repository_value"
    assert response.source_provider == "source_provider_value"
    assert response.deployment_level == telcoautomation.DeploymentLevel.HYDRATION
    assert response.rollback_support is True


@pytest.mark.asyncio
async def test_propose_blueprint_async_from_dict():
    await test_propose_blueprint_async(request_type=dict)


def test_propose_blueprint_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.ProposeBlueprintRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.propose_blueprint), "__call__"
    ) as call:
        call.return_value = telcoautomation.Blueprint()
        client.propose_blueprint(request)

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
async def test_propose_blueprint_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.ProposeBlueprintRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.propose_blueprint), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.Blueprint()
        )
        await client.propose_blueprint(request)

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


def test_propose_blueprint_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.propose_blueprint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.Blueprint()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.propose_blueprint(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_propose_blueprint_flattened_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.propose_blueprint(
            telcoautomation.ProposeBlueprintRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_propose_blueprint_flattened_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.propose_blueprint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.Blueprint()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.Blueprint()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.propose_blueprint(
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
async def test_propose_blueprint_flattened_error_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.propose_blueprint(
            telcoautomation.ProposeBlueprintRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.RejectBlueprintRequest,
        dict,
    ],
)
def test_reject_blueprint(request_type, transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.reject_blueprint), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.Blueprint(
            name="name_value",
            revision_id="revision_id_value",
            source_blueprint="source_blueprint_value",
            approval_state=telcoautomation.Blueprint.ApprovalState.DRAFT,
            display_name="display_name_value",
            repository="repository_value",
            source_provider="source_provider_value",
            deployment_level=telcoautomation.DeploymentLevel.HYDRATION,
            rollback_support=True,
        )
        response = client.reject_blueprint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.RejectBlueprintRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.Blueprint)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.source_blueprint == "source_blueprint_value"
    assert response.approval_state == telcoautomation.Blueprint.ApprovalState.DRAFT
    assert response.display_name == "display_name_value"
    assert response.repository == "repository_value"
    assert response.source_provider == "source_provider_value"
    assert response.deployment_level == telcoautomation.DeploymentLevel.HYDRATION
    assert response.rollback_support is True


def test_reject_blueprint_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.reject_blueprint), "__call__") as call:
        client.reject_blueprint()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.RejectBlueprintRequest()


@pytest.mark.asyncio
async def test_reject_blueprint_async(
    transport: str = "grpc_asyncio", request_type=telcoautomation.RejectBlueprintRequest
):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.reject_blueprint), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.Blueprint(
                name="name_value",
                revision_id="revision_id_value",
                source_blueprint="source_blueprint_value",
                approval_state=telcoautomation.Blueprint.ApprovalState.DRAFT,
                display_name="display_name_value",
                repository="repository_value",
                source_provider="source_provider_value",
                deployment_level=telcoautomation.DeploymentLevel.HYDRATION,
                rollback_support=True,
            )
        )
        response = await client.reject_blueprint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.RejectBlueprintRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.Blueprint)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.source_blueprint == "source_blueprint_value"
    assert response.approval_state == telcoautomation.Blueprint.ApprovalState.DRAFT
    assert response.display_name == "display_name_value"
    assert response.repository == "repository_value"
    assert response.source_provider == "source_provider_value"
    assert response.deployment_level == telcoautomation.DeploymentLevel.HYDRATION
    assert response.rollback_support is True


@pytest.mark.asyncio
async def test_reject_blueprint_async_from_dict():
    await test_reject_blueprint_async(request_type=dict)


def test_reject_blueprint_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.RejectBlueprintRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.reject_blueprint), "__call__") as call:
        call.return_value = telcoautomation.Blueprint()
        client.reject_blueprint(request)

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
async def test_reject_blueprint_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.RejectBlueprintRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.reject_blueprint), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.Blueprint()
        )
        await client.reject_blueprint(request)

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


def test_reject_blueprint_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.reject_blueprint), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.Blueprint()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.reject_blueprint(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_reject_blueprint_flattened_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.reject_blueprint(
            telcoautomation.RejectBlueprintRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_reject_blueprint_flattened_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.reject_blueprint), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.Blueprint()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.Blueprint()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.reject_blueprint(
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
async def test_reject_blueprint_flattened_error_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.reject_blueprint(
            telcoautomation.RejectBlueprintRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.ListBlueprintRevisionsRequest,
        dict,
    ],
)
def test_list_blueprint_revisions(request_type, transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_blueprint_revisions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.ListBlueprintRevisionsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_blueprint_revisions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ListBlueprintRevisionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBlueprintRevisionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_blueprint_revisions_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_blueprint_revisions), "__call__"
    ) as call:
        client.list_blueprint_revisions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ListBlueprintRevisionsRequest()


@pytest.mark.asyncio
async def test_list_blueprint_revisions_async(
    transport: str = "grpc_asyncio",
    request_type=telcoautomation.ListBlueprintRevisionsRequest,
):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_blueprint_revisions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.ListBlueprintRevisionsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_blueprint_revisions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ListBlueprintRevisionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBlueprintRevisionsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_blueprint_revisions_async_from_dict():
    await test_list_blueprint_revisions_async(request_type=dict)


def test_list_blueprint_revisions_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.ListBlueprintRevisionsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_blueprint_revisions), "__call__"
    ) as call:
        call.return_value = telcoautomation.ListBlueprintRevisionsResponse()
        client.list_blueprint_revisions(request)

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
async def test_list_blueprint_revisions_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.ListBlueprintRevisionsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_blueprint_revisions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.ListBlueprintRevisionsResponse()
        )
        await client.list_blueprint_revisions(request)

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


def test_list_blueprint_revisions_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_blueprint_revisions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.ListBlueprintRevisionsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_blueprint_revisions(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_list_blueprint_revisions_flattened_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_blueprint_revisions(
            telcoautomation.ListBlueprintRevisionsRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_list_blueprint_revisions_flattened_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_blueprint_revisions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.ListBlueprintRevisionsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.ListBlueprintRevisionsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_blueprint_revisions(
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
async def test_list_blueprint_revisions_flattened_error_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_blueprint_revisions(
            telcoautomation.ListBlueprintRevisionsRequest(),
            name="name_value",
        )


def test_list_blueprint_revisions_pager(transport_name: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_blueprint_revisions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.ListBlueprintRevisionsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListBlueprintRevisionsResponse(
                blueprints=[],
                next_page_token="def",
            ),
            telcoautomation.ListBlueprintRevisionsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListBlueprintRevisionsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", ""),)),
        )
        pager = client.list_blueprint_revisions(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, telcoautomation.Blueprint) for i in results)


def test_list_blueprint_revisions_pages(transport_name: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_blueprint_revisions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.ListBlueprintRevisionsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListBlueprintRevisionsResponse(
                blueprints=[],
                next_page_token="def",
            ),
            telcoautomation.ListBlueprintRevisionsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListBlueprintRevisionsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_blueprint_revisions(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_blueprint_revisions_async_pager():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_blueprint_revisions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.ListBlueprintRevisionsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListBlueprintRevisionsResponse(
                blueprints=[],
                next_page_token="def",
            ),
            telcoautomation.ListBlueprintRevisionsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListBlueprintRevisionsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_blueprint_revisions(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, telcoautomation.Blueprint) for i in responses)


@pytest.mark.asyncio
async def test_list_blueprint_revisions_async_pages():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_blueprint_revisions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.ListBlueprintRevisionsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListBlueprintRevisionsResponse(
                blueprints=[],
                next_page_token="def",
            ),
            telcoautomation.ListBlueprintRevisionsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListBlueprintRevisionsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_blueprint_revisions(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.SearchBlueprintRevisionsRequest,
        dict,
    ],
)
def test_search_blueprint_revisions(request_type, transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_blueprint_revisions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.SearchBlueprintRevisionsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.search_blueprint_revisions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.SearchBlueprintRevisionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchBlueprintRevisionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_search_blueprint_revisions_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_blueprint_revisions), "__call__"
    ) as call:
        client.search_blueprint_revisions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.SearchBlueprintRevisionsRequest()


@pytest.mark.asyncio
async def test_search_blueprint_revisions_async(
    transport: str = "grpc_asyncio",
    request_type=telcoautomation.SearchBlueprintRevisionsRequest,
):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_blueprint_revisions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.SearchBlueprintRevisionsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.search_blueprint_revisions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.SearchBlueprintRevisionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchBlueprintRevisionsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_search_blueprint_revisions_async_from_dict():
    await test_search_blueprint_revisions_async(request_type=dict)


def test_search_blueprint_revisions_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.SearchBlueprintRevisionsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_blueprint_revisions), "__call__"
    ) as call:
        call.return_value = telcoautomation.SearchBlueprintRevisionsResponse()
        client.search_blueprint_revisions(request)

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
async def test_search_blueprint_revisions_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.SearchBlueprintRevisionsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_blueprint_revisions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.SearchBlueprintRevisionsResponse()
        )
        await client.search_blueprint_revisions(request)

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


def test_search_blueprint_revisions_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_blueprint_revisions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.SearchBlueprintRevisionsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.search_blueprint_revisions(
            parent="parent_value",
            query="query_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].query
        mock_val = "query_value"
        assert arg == mock_val


def test_search_blueprint_revisions_flattened_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.search_blueprint_revisions(
            telcoautomation.SearchBlueprintRevisionsRequest(),
            parent="parent_value",
            query="query_value",
        )


@pytest.mark.asyncio
async def test_search_blueprint_revisions_flattened_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_blueprint_revisions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.SearchBlueprintRevisionsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.SearchBlueprintRevisionsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.search_blueprint_revisions(
            parent="parent_value",
            query="query_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].query
        mock_val = "query_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_search_blueprint_revisions_flattened_error_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.search_blueprint_revisions(
            telcoautomation.SearchBlueprintRevisionsRequest(),
            parent="parent_value",
            query="query_value",
        )


def test_search_blueprint_revisions_pager(transport_name: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_blueprint_revisions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.SearchBlueprintRevisionsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.SearchBlueprintRevisionsResponse(
                blueprints=[],
                next_page_token="def",
            ),
            telcoautomation.SearchBlueprintRevisionsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.SearchBlueprintRevisionsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.search_blueprint_revisions(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, telcoautomation.Blueprint) for i in results)


def test_search_blueprint_revisions_pages(transport_name: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_blueprint_revisions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.SearchBlueprintRevisionsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.SearchBlueprintRevisionsResponse(
                blueprints=[],
                next_page_token="def",
            ),
            telcoautomation.SearchBlueprintRevisionsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.SearchBlueprintRevisionsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.search_blueprint_revisions(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_search_blueprint_revisions_async_pager():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_blueprint_revisions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.SearchBlueprintRevisionsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.SearchBlueprintRevisionsResponse(
                blueprints=[],
                next_page_token="def",
            ),
            telcoautomation.SearchBlueprintRevisionsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.SearchBlueprintRevisionsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.search_blueprint_revisions(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, telcoautomation.Blueprint) for i in responses)


@pytest.mark.asyncio
async def test_search_blueprint_revisions_async_pages():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_blueprint_revisions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.SearchBlueprintRevisionsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.SearchBlueprintRevisionsResponse(
                blueprints=[],
                next_page_token="def",
            ),
            telcoautomation.SearchBlueprintRevisionsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.SearchBlueprintRevisionsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.search_blueprint_revisions(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.SearchDeploymentRevisionsRequest,
        dict,
    ],
)
def test_search_deployment_revisions(request_type, transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_deployment_revisions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.SearchDeploymentRevisionsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.search_deployment_revisions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.SearchDeploymentRevisionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchDeploymentRevisionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_search_deployment_revisions_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_deployment_revisions), "__call__"
    ) as call:
        client.search_deployment_revisions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.SearchDeploymentRevisionsRequest()


@pytest.mark.asyncio
async def test_search_deployment_revisions_async(
    transport: str = "grpc_asyncio",
    request_type=telcoautomation.SearchDeploymentRevisionsRequest,
):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_deployment_revisions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.SearchDeploymentRevisionsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.search_deployment_revisions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.SearchDeploymentRevisionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchDeploymentRevisionsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_search_deployment_revisions_async_from_dict():
    await test_search_deployment_revisions_async(request_type=dict)


def test_search_deployment_revisions_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.SearchDeploymentRevisionsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_deployment_revisions), "__call__"
    ) as call:
        call.return_value = telcoautomation.SearchDeploymentRevisionsResponse()
        client.search_deployment_revisions(request)

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
async def test_search_deployment_revisions_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.SearchDeploymentRevisionsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_deployment_revisions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.SearchDeploymentRevisionsResponse()
        )
        await client.search_deployment_revisions(request)

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


def test_search_deployment_revisions_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_deployment_revisions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.SearchDeploymentRevisionsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.search_deployment_revisions(
            parent="parent_value",
            query="query_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].query
        mock_val = "query_value"
        assert arg == mock_val


def test_search_deployment_revisions_flattened_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.search_deployment_revisions(
            telcoautomation.SearchDeploymentRevisionsRequest(),
            parent="parent_value",
            query="query_value",
        )


@pytest.mark.asyncio
async def test_search_deployment_revisions_flattened_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_deployment_revisions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.SearchDeploymentRevisionsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.SearchDeploymentRevisionsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.search_deployment_revisions(
            parent="parent_value",
            query="query_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].query
        mock_val = "query_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_search_deployment_revisions_flattened_error_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.search_deployment_revisions(
            telcoautomation.SearchDeploymentRevisionsRequest(),
            parent="parent_value",
            query="query_value",
        )


def test_search_deployment_revisions_pager(transport_name: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_deployment_revisions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.SearchDeploymentRevisionsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.SearchDeploymentRevisionsResponse(
                deployments=[],
                next_page_token="def",
            ),
            telcoautomation.SearchDeploymentRevisionsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.SearchDeploymentRevisionsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.search_deployment_revisions(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, telcoautomation.Deployment) for i in results)


def test_search_deployment_revisions_pages(transport_name: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_deployment_revisions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.SearchDeploymentRevisionsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.SearchDeploymentRevisionsResponse(
                deployments=[],
                next_page_token="def",
            ),
            telcoautomation.SearchDeploymentRevisionsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.SearchDeploymentRevisionsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.search_deployment_revisions(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_search_deployment_revisions_async_pager():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_deployment_revisions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.SearchDeploymentRevisionsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.SearchDeploymentRevisionsResponse(
                deployments=[],
                next_page_token="def",
            ),
            telcoautomation.SearchDeploymentRevisionsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.SearchDeploymentRevisionsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.search_deployment_revisions(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, telcoautomation.Deployment) for i in responses)


@pytest.mark.asyncio
async def test_search_deployment_revisions_async_pages():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_deployment_revisions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.SearchDeploymentRevisionsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.SearchDeploymentRevisionsResponse(
                deployments=[],
                next_page_token="def",
            ),
            telcoautomation.SearchDeploymentRevisionsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.SearchDeploymentRevisionsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.search_deployment_revisions(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.DiscardBlueprintChangesRequest,
        dict,
    ],
)
def test_discard_blueprint_changes(request_type, transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.discard_blueprint_changes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.DiscardBlueprintChangesResponse()
        response = client.discard_blueprint_changes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.DiscardBlueprintChangesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.DiscardBlueprintChangesResponse)


def test_discard_blueprint_changes_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.discard_blueprint_changes), "__call__"
    ) as call:
        client.discard_blueprint_changes()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.DiscardBlueprintChangesRequest()


@pytest.mark.asyncio
async def test_discard_blueprint_changes_async(
    transport: str = "grpc_asyncio",
    request_type=telcoautomation.DiscardBlueprintChangesRequest,
):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.discard_blueprint_changes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.DiscardBlueprintChangesResponse()
        )
        response = await client.discard_blueprint_changes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.DiscardBlueprintChangesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.DiscardBlueprintChangesResponse)


@pytest.mark.asyncio
async def test_discard_blueprint_changes_async_from_dict():
    await test_discard_blueprint_changes_async(request_type=dict)


def test_discard_blueprint_changes_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.DiscardBlueprintChangesRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.discard_blueprint_changes), "__call__"
    ) as call:
        call.return_value = telcoautomation.DiscardBlueprintChangesResponse()
        client.discard_blueprint_changes(request)

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
async def test_discard_blueprint_changes_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.DiscardBlueprintChangesRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.discard_blueprint_changes), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.DiscardBlueprintChangesResponse()
        )
        await client.discard_blueprint_changes(request)

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


def test_discard_blueprint_changes_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.discard_blueprint_changes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.DiscardBlueprintChangesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.discard_blueprint_changes(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_discard_blueprint_changes_flattened_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.discard_blueprint_changes(
            telcoautomation.DiscardBlueprintChangesRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_discard_blueprint_changes_flattened_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.discard_blueprint_changes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.DiscardBlueprintChangesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.DiscardBlueprintChangesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.discard_blueprint_changes(
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
async def test_discard_blueprint_changes_flattened_error_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.discard_blueprint_changes(
            telcoautomation.DiscardBlueprintChangesRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.ListPublicBlueprintsRequest,
        dict,
    ],
)
def test_list_public_blueprints(request_type, transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_public_blueprints), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.ListPublicBlueprintsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_public_blueprints(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ListPublicBlueprintsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPublicBlueprintsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_public_blueprints_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_public_blueprints), "__call__"
    ) as call:
        client.list_public_blueprints()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ListPublicBlueprintsRequest()


@pytest.mark.asyncio
async def test_list_public_blueprints_async(
    transport: str = "grpc_asyncio",
    request_type=telcoautomation.ListPublicBlueprintsRequest,
):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_public_blueprints), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.ListPublicBlueprintsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_public_blueprints(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ListPublicBlueprintsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPublicBlueprintsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_public_blueprints_async_from_dict():
    await test_list_public_blueprints_async(request_type=dict)


def test_list_public_blueprints_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.ListPublicBlueprintsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_public_blueprints), "__call__"
    ) as call:
        call.return_value = telcoautomation.ListPublicBlueprintsResponse()
        client.list_public_blueprints(request)

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
async def test_list_public_blueprints_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.ListPublicBlueprintsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_public_blueprints), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.ListPublicBlueprintsResponse()
        )
        await client.list_public_blueprints(request)

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


def test_list_public_blueprints_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_public_blueprints), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.ListPublicBlueprintsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_public_blueprints(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_public_blueprints_flattened_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_public_blueprints(
            telcoautomation.ListPublicBlueprintsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_public_blueprints_flattened_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_public_blueprints), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.ListPublicBlueprintsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.ListPublicBlueprintsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_public_blueprints(
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
async def test_list_public_blueprints_flattened_error_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_public_blueprints(
            telcoautomation.ListPublicBlueprintsRequest(),
            parent="parent_value",
        )


def test_list_public_blueprints_pager(transport_name: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_public_blueprints), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.ListPublicBlueprintsResponse(
                public_blueprints=[
                    telcoautomation.PublicBlueprint(),
                    telcoautomation.PublicBlueprint(),
                    telcoautomation.PublicBlueprint(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListPublicBlueprintsResponse(
                public_blueprints=[],
                next_page_token="def",
            ),
            telcoautomation.ListPublicBlueprintsResponse(
                public_blueprints=[
                    telcoautomation.PublicBlueprint(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListPublicBlueprintsResponse(
                public_blueprints=[
                    telcoautomation.PublicBlueprint(),
                    telcoautomation.PublicBlueprint(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_public_blueprints(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, telcoautomation.PublicBlueprint) for i in results)


def test_list_public_blueprints_pages(transport_name: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_public_blueprints), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.ListPublicBlueprintsResponse(
                public_blueprints=[
                    telcoautomation.PublicBlueprint(),
                    telcoautomation.PublicBlueprint(),
                    telcoautomation.PublicBlueprint(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListPublicBlueprintsResponse(
                public_blueprints=[],
                next_page_token="def",
            ),
            telcoautomation.ListPublicBlueprintsResponse(
                public_blueprints=[
                    telcoautomation.PublicBlueprint(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListPublicBlueprintsResponse(
                public_blueprints=[
                    telcoautomation.PublicBlueprint(),
                    telcoautomation.PublicBlueprint(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_public_blueprints(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_public_blueprints_async_pager():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_public_blueprints),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.ListPublicBlueprintsResponse(
                public_blueprints=[
                    telcoautomation.PublicBlueprint(),
                    telcoautomation.PublicBlueprint(),
                    telcoautomation.PublicBlueprint(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListPublicBlueprintsResponse(
                public_blueprints=[],
                next_page_token="def",
            ),
            telcoautomation.ListPublicBlueprintsResponse(
                public_blueprints=[
                    telcoautomation.PublicBlueprint(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListPublicBlueprintsResponse(
                public_blueprints=[
                    telcoautomation.PublicBlueprint(),
                    telcoautomation.PublicBlueprint(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_public_blueprints(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, telcoautomation.PublicBlueprint) for i in responses)


@pytest.mark.asyncio
async def test_list_public_blueprints_async_pages():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_public_blueprints),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.ListPublicBlueprintsResponse(
                public_blueprints=[
                    telcoautomation.PublicBlueprint(),
                    telcoautomation.PublicBlueprint(),
                    telcoautomation.PublicBlueprint(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListPublicBlueprintsResponse(
                public_blueprints=[],
                next_page_token="def",
            ),
            telcoautomation.ListPublicBlueprintsResponse(
                public_blueprints=[
                    telcoautomation.PublicBlueprint(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListPublicBlueprintsResponse(
                public_blueprints=[
                    telcoautomation.PublicBlueprint(),
                    telcoautomation.PublicBlueprint(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_public_blueprints(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.GetPublicBlueprintRequest,
        dict,
    ],
)
def test_get_public_blueprint(request_type, transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_public_blueprint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.PublicBlueprint(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            deployment_level=telcoautomation.DeploymentLevel.HYDRATION,
            source_provider="source_provider_value",
            rollback_support=True,
        )
        response = client.get_public_blueprint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.GetPublicBlueprintRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.PublicBlueprint)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.deployment_level == telcoautomation.DeploymentLevel.HYDRATION
    assert response.source_provider == "source_provider_value"
    assert response.rollback_support is True


def test_get_public_blueprint_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_public_blueprint), "__call__"
    ) as call:
        client.get_public_blueprint()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.GetPublicBlueprintRequest()


@pytest.mark.asyncio
async def test_get_public_blueprint_async(
    transport: str = "grpc_asyncio",
    request_type=telcoautomation.GetPublicBlueprintRequest,
):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_public_blueprint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.PublicBlueprint(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                deployment_level=telcoautomation.DeploymentLevel.HYDRATION,
                source_provider="source_provider_value",
                rollback_support=True,
            )
        )
        response = await client.get_public_blueprint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.GetPublicBlueprintRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.PublicBlueprint)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.deployment_level == telcoautomation.DeploymentLevel.HYDRATION
    assert response.source_provider == "source_provider_value"
    assert response.rollback_support is True


@pytest.mark.asyncio
async def test_get_public_blueprint_async_from_dict():
    await test_get_public_blueprint_async(request_type=dict)


def test_get_public_blueprint_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.GetPublicBlueprintRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_public_blueprint), "__call__"
    ) as call:
        call.return_value = telcoautomation.PublicBlueprint()
        client.get_public_blueprint(request)

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
async def test_get_public_blueprint_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.GetPublicBlueprintRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_public_blueprint), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.PublicBlueprint()
        )
        await client.get_public_blueprint(request)

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


def test_get_public_blueprint_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_public_blueprint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.PublicBlueprint()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_public_blueprint(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_public_blueprint_flattened_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_public_blueprint(
            telcoautomation.GetPublicBlueprintRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_public_blueprint_flattened_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_public_blueprint), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.PublicBlueprint()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.PublicBlueprint()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_public_blueprint(
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
async def test_get_public_blueprint_flattened_error_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_public_blueprint(
            telcoautomation.GetPublicBlueprintRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.CreateDeploymentRequest,
        dict,
    ],
)
def test_create_deployment(request_type, transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.Deployment(
            name="name_value",
            revision_id="revision_id_value",
            source_blueprint_revision="source_blueprint_revision_value",
            state=telcoautomation.Deployment.State.DRAFT,
            display_name="display_name_value",
            repository="repository_value",
            source_provider="source_provider_value",
            workload_cluster="workload_cluster_value",
            deployment_level=telcoautomation.DeploymentLevel.HYDRATION,
            rollback_support=True,
        )
        response = client.create_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.CreateDeploymentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.Deployment)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.source_blueprint_revision == "source_blueprint_revision_value"
    assert response.state == telcoautomation.Deployment.State.DRAFT
    assert response.display_name == "display_name_value"
    assert response.repository == "repository_value"
    assert response.source_provider == "source_provider_value"
    assert response.workload_cluster == "workload_cluster_value"
    assert response.deployment_level == telcoautomation.DeploymentLevel.HYDRATION
    assert response.rollback_support is True


def test_create_deployment_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_deployment), "__call__"
    ) as call:
        client.create_deployment()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.CreateDeploymentRequest()


@pytest.mark.asyncio
async def test_create_deployment_async(
    transport: str = "grpc_asyncio",
    request_type=telcoautomation.CreateDeploymentRequest,
):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.Deployment(
                name="name_value",
                revision_id="revision_id_value",
                source_blueprint_revision="source_blueprint_revision_value",
                state=telcoautomation.Deployment.State.DRAFT,
                display_name="display_name_value",
                repository="repository_value",
                source_provider="source_provider_value",
                workload_cluster="workload_cluster_value",
                deployment_level=telcoautomation.DeploymentLevel.HYDRATION,
                rollback_support=True,
            )
        )
        response = await client.create_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.CreateDeploymentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.Deployment)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.source_blueprint_revision == "source_blueprint_revision_value"
    assert response.state == telcoautomation.Deployment.State.DRAFT
    assert response.display_name == "display_name_value"
    assert response.repository == "repository_value"
    assert response.source_provider == "source_provider_value"
    assert response.workload_cluster == "workload_cluster_value"
    assert response.deployment_level == telcoautomation.DeploymentLevel.HYDRATION
    assert response.rollback_support is True


@pytest.mark.asyncio
async def test_create_deployment_async_from_dict():
    await test_create_deployment_async(request_type=dict)


def test_create_deployment_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.CreateDeploymentRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_deployment), "__call__"
    ) as call:
        call.return_value = telcoautomation.Deployment()
        client.create_deployment(request)

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
async def test_create_deployment_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.CreateDeploymentRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_deployment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.Deployment()
        )
        await client.create_deployment(request)

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


def test_create_deployment_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.Deployment()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_deployment(
            parent="parent_value",
            deployment=telcoautomation.Deployment(name="name_value"),
            deployment_id="deployment_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].deployment
        mock_val = telcoautomation.Deployment(name="name_value")
        assert arg == mock_val
        arg = args[0].deployment_id
        mock_val = "deployment_id_value"
        assert arg == mock_val


def test_create_deployment_flattened_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_deployment(
            telcoautomation.CreateDeploymentRequest(),
            parent="parent_value",
            deployment=telcoautomation.Deployment(name="name_value"),
            deployment_id="deployment_id_value",
        )


@pytest.mark.asyncio
async def test_create_deployment_flattened_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.Deployment()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.Deployment()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_deployment(
            parent="parent_value",
            deployment=telcoautomation.Deployment(name="name_value"),
            deployment_id="deployment_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].deployment
        mock_val = telcoautomation.Deployment(name="name_value")
        assert arg == mock_val
        arg = args[0].deployment_id
        mock_val = "deployment_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_deployment_flattened_error_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_deployment(
            telcoautomation.CreateDeploymentRequest(),
            parent="parent_value",
            deployment=telcoautomation.Deployment(name="name_value"),
            deployment_id="deployment_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.UpdateDeploymentRequest,
        dict,
    ],
)
def test_update_deployment(request_type, transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.Deployment(
            name="name_value",
            revision_id="revision_id_value",
            source_blueprint_revision="source_blueprint_revision_value",
            state=telcoautomation.Deployment.State.DRAFT,
            display_name="display_name_value",
            repository="repository_value",
            source_provider="source_provider_value",
            workload_cluster="workload_cluster_value",
            deployment_level=telcoautomation.DeploymentLevel.HYDRATION,
            rollback_support=True,
        )
        response = client.update_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.UpdateDeploymentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.Deployment)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.source_blueprint_revision == "source_blueprint_revision_value"
    assert response.state == telcoautomation.Deployment.State.DRAFT
    assert response.display_name == "display_name_value"
    assert response.repository == "repository_value"
    assert response.source_provider == "source_provider_value"
    assert response.workload_cluster == "workload_cluster_value"
    assert response.deployment_level == telcoautomation.DeploymentLevel.HYDRATION
    assert response.rollback_support is True


def test_update_deployment_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_deployment), "__call__"
    ) as call:
        client.update_deployment()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.UpdateDeploymentRequest()


@pytest.mark.asyncio
async def test_update_deployment_async(
    transport: str = "grpc_asyncio",
    request_type=telcoautomation.UpdateDeploymentRequest,
):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.Deployment(
                name="name_value",
                revision_id="revision_id_value",
                source_blueprint_revision="source_blueprint_revision_value",
                state=telcoautomation.Deployment.State.DRAFT,
                display_name="display_name_value",
                repository="repository_value",
                source_provider="source_provider_value",
                workload_cluster="workload_cluster_value",
                deployment_level=telcoautomation.DeploymentLevel.HYDRATION,
                rollback_support=True,
            )
        )
        response = await client.update_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.UpdateDeploymentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.Deployment)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.source_blueprint_revision == "source_blueprint_revision_value"
    assert response.state == telcoautomation.Deployment.State.DRAFT
    assert response.display_name == "display_name_value"
    assert response.repository == "repository_value"
    assert response.source_provider == "source_provider_value"
    assert response.workload_cluster == "workload_cluster_value"
    assert response.deployment_level == telcoautomation.DeploymentLevel.HYDRATION
    assert response.rollback_support is True


@pytest.mark.asyncio
async def test_update_deployment_async_from_dict():
    await test_update_deployment_async(request_type=dict)


def test_update_deployment_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.UpdateDeploymentRequest()

    request.deployment.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_deployment), "__call__"
    ) as call:
        call.return_value = telcoautomation.Deployment()
        client.update_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "deployment.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_deployment_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.UpdateDeploymentRequest()

    request.deployment.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_deployment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.Deployment()
        )
        await client.update_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "deployment.name=name_value",
    ) in kw["metadata"]


def test_update_deployment_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.Deployment()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_deployment(
            deployment=telcoautomation.Deployment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].deployment
        mock_val = telcoautomation.Deployment(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_deployment_flattened_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_deployment(
            telcoautomation.UpdateDeploymentRequest(),
            deployment=telcoautomation.Deployment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_deployment_flattened_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.Deployment()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.Deployment()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_deployment(
            deployment=telcoautomation.Deployment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].deployment
        mock_val = telcoautomation.Deployment(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_deployment_flattened_error_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_deployment(
            telcoautomation.UpdateDeploymentRequest(),
            deployment=telcoautomation.Deployment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.GetDeploymentRequest,
        dict,
    ],
)
def test_get_deployment(request_type, transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_deployment), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.Deployment(
            name="name_value",
            revision_id="revision_id_value",
            source_blueprint_revision="source_blueprint_revision_value",
            state=telcoautomation.Deployment.State.DRAFT,
            display_name="display_name_value",
            repository="repository_value",
            source_provider="source_provider_value",
            workload_cluster="workload_cluster_value",
            deployment_level=telcoautomation.DeploymentLevel.HYDRATION,
            rollback_support=True,
        )
        response = client.get_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.GetDeploymentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.Deployment)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.source_blueprint_revision == "source_blueprint_revision_value"
    assert response.state == telcoautomation.Deployment.State.DRAFT
    assert response.display_name == "display_name_value"
    assert response.repository == "repository_value"
    assert response.source_provider == "source_provider_value"
    assert response.workload_cluster == "workload_cluster_value"
    assert response.deployment_level == telcoautomation.DeploymentLevel.HYDRATION
    assert response.rollback_support is True


def test_get_deployment_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_deployment), "__call__") as call:
        client.get_deployment()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.GetDeploymentRequest()


@pytest.mark.asyncio
async def test_get_deployment_async(
    transport: str = "grpc_asyncio", request_type=telcoautomation.GetDeploymentRequest
):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_deployment), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.Deployment(
                name="name_value",
                revision_id="revision_id_value",
                source_blueprint_revision="source_blueprint_revision_value",
                state=telcoautomation.Deployment.State.DRAFT,
                display_name="display_name_value",
                repository="repository_value",
                source_provider="source_provider_value",
                workload_cluster="workload_cluster_value",
                deployment_level=telcoautomation.DeploymentLevel.HYDRATION,
                rollback_support=True,
            )
        )
        response = await client.get_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.GetDeploymentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.Deployment)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.source_blueprint_revision == "source_blueprint_revision_value"
    assert response.state == telcoautomation.Deployment.State.DRAFT
    assert response.display_name == "display_name_value"
    assert response.repository == "repository_value"
    assert response.source_provider == "source_provider_value"
    assert response.workload_cluster == "workload_cluster_value"
    assert response.deployment_level == telcoautomation.DeploymentLevel.HYDRATION
    assert response.rollback_support is True


@pytest.mark.asyncio
async def test_get_deployment_async_from_dict():
    await test_get_deployment_async(request_type=dict)


def test_get_deployment_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.GetDeploymentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_deployment), "__call__") as call:
        call.return_value = telcoautomation.Deployment()
        client.get_deployment(request)

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
async def test_get_deployment_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.GetDeploymentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_deployment), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.Deployment()
        )
        await client.get_deployment(request)

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


def test_get_deployment_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_deployment), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.Deployment()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_deployment(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_deployment_flattened_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_deployment(
            telcoautomation.GetDeploymentRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_deployment_flattened_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_deployment), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.Deployment()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.Deployment()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_deployment(
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
async def test_get_deployment_flattened_error_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_deployment(
            telcoautomation.GetDeploymentRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.RemoveDeploymentRequest,
        dict,
    ],
)
def test_remove_deployment(request_type, transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.remove_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.remove_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.RemoveDeploymentRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_remove_deployment_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.remove_deployment), "__call__"
    ) as call:
        client.remove_deployment()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.RemoveDeploymentRequest()


@pytest.mark.asyncio
async def test_remove_deployment_async(
    transport: str = "grpc_asyncio",
    request_type=telcoautomation.RemoveDeploymentRequest,
):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.remove_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.remove_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.RemoveDeploymentRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_remove_deployment_async_from_dict():
    await test_remove_deployment_async(request_type=dict)


def test_remove_deployment_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.RemoveDeploymentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.remove_deployment), "__call__"
    ) as call:
        call.return_value = None
        client.remove_deployment(request)

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
async def test_remove_deployment_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.RemoveDeploymentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.remove_deployment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.remove_deployment(request)

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


def test_remove_deployment_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.remove_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.remove_deployment(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_remove_deployment_flattened_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.remove_deployment(
            telcoautomation.RemoveDeploymentRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_remove_deployment_flattened_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.remove_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.remove_deployment(
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
async def test_remove_deployment_flattened_error_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.remove_deployment(
            telcoautomation.RemoveDeploymentRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.ListDeploymentsRequest,
        dict,
    ],
)
def test_list_deployments(request_type, transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_deployments), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.ListDeploymentsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_deployments(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ListDeploymentsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDeploymentsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_deployments_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_deployments), "__call__") as call:
        client.list_deployments()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ListDeploymentsRequest()


@pytest.mark.asyncio
async def test_list_deployments_async(
    transport: str = "grpc_asyncio", request_type=telcoautomation.ListDeploymentsRequest
):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_deployments), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.ListDeploymentsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_deployments(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ListDeploymentsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDeploymentsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_deployments_async_from_dict():
    await test_list_deployments_async(request_type=dict)


def test_list_deployments_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.ListDeploymentsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_deployments), "__call__") as call:
        call.return_value = telcoautomation.ListDeploymentsResponse()
        client.list_deployments(request)

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
async def test_list_deployments_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.ListDeploymentsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_deployments), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.ListDeploymentsResponse()
        )
        await client.list_deployments(request)

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


def test_list_deployments_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_deployments), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.ListDeploymentsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_deployments(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_deployments_flattened_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_deployments(
            telcoautomation.ListDeploymentsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_deployments_flattened_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_deployments), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.ListDeploymentsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.ListDeploymentsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_deployments(
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
async def test_list_deployments_flattened_error_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_deployments(
            telcoautomation.ListDeploymentsRequest(),
            parent="parent_value",
        )


def test_list_deployments_pager(transport_name: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_deployments), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.ListDeploymentsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListDeploymentsResponse(
                deployments=[],
                next_page_token="def",
            ),
            telcoautomation.ListDeploymentsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListDeploymentsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_deployments(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, telcoautomation.Deployment) for i in results)


def test_list_deployments_pages(transport_name: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_deployments), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.ListDeploymentsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListDeploymentsResponse(
                deployments=[],
                next_page_token="def",
            ),
            telcoautomation.ListDeploymentsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListDeploymentsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_deployments(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_deployments_async_pager():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_deployments), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.ListDeploymentsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListDeploymentsResponse(
                deployments=[],
                next_page_token="def",
            ),
            telcoautomation.ListDeploymentsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListDeploymentsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_deployments(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, telcoautomation.Deployment) for i in responses)


@pytest.mark.asyncio
async def test_list_deployments_async_pages():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_deployments), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.ListDeploymentsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListDeploymentsResponse(
                deployments=[],
                next_page_token="def",
            ),
            telcoautomation.ListDeploymentsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListDeploymentsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_deployments(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.ListDeploymentRevisionsRequest,
        dict,
    ],
)
def test_list_deployment_revisions(request_type, transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_deployment_revisions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.ListDeploymentRevisionsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_deployment_revisions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ListDeploymentRevisionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDeploymentRevisionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_deployment_revisions_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_deployment_revisions), "__call__"
    ) as call:
        client.list_deployment_revisions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ListDeploymentRevisionsRequest()


@pytest.mark.asyncio
async def test_list_deployment_revisions_async(
    transport: str = "grpc_asyncio",
    request_type=telcoautomation.ListDeploymentRevisionsRequest,
):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_deployment_revisions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.ListDeploymentRevisionsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_deployment_revisions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ListDeploymentRevisionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDeploymentRevisionsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_deployment_revisions_async_from_dict():
    await test_list_deployment_revisions_async(request_type=dict)


def test_list_deployment_revisions_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.ListDeploymentRevisionsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_deployment_revisions), "__call__"
    ) as call:
        call.return_value = telcoautomation.ListDeploymentRevisionsResponse()
        client.list_deployment_revisions(request)

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
async def test_list_deployment_revisions_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.ListDeploymentRevisionsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_deployment_revisions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.ListDeploymentRevisionsResponse()
        )
        await client.list_deployment_revisions(request)

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


def test_list_deployment_revisions_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_deployment_revisions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.ListDeploymentRevisionsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_deployment_revisions(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_list_deployment_revisions_flattened_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_deployment_revisions(
            telcoautomation.ListDeploymentRevisionsRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_list_deployment_revisions_flattened_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_deployment_revisions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.ListDeploymentRevisionsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.ListDeploymentRevisionsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_deployment_revisions(
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
async def test_list_deployment_revisions_flattened_error_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_deployment_revisions(
            telcoautomation.ListDeploymentRevisionsRequest(),
            name="name_value",
        )


def test_list_deployment_revisions_pager(transport_name: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_deployment_revisions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.ListDeploymentRevisionsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListDeploymentRevisionsResponse(
                deployments=[],
                next_page_token="def",
            ),
            telcoautomation.ListDeploymentRevisionsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListDeploymentRevisionsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", ""),)),
        )
        pager = client.list_deployment_revisions(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, telcoautomation.Deployment) for i in results)


def test_list_deployment_revisions_pages(transport_name: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_deployment_revisions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.ListDeploymentRevisionsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListDeploymentRevisionsResponse(
                deployments=[],
                next_page_token="def",
            ),
            telcoautomation.ListDeploymentRevisionsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListDeploymentRevisionsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_deployment_revisions(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_deployment_revisions_async_pager():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_deployment_revisions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.ListDeploymentRevisionsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListDeploymentRevisionsResponse(
                deployments=[],
                next_page_token="def",
            ),
            telcoautomation.ListDeploymentRevisionsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListDeploymentRevisionsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_deployment_revisions(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, telcoautomation.Deployment) for i in responses)


@pytest.mark.asyncio
async def test_list_deployment_revisions_async_pages():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_deployment_revisions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.ListDeploymentRevisionsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListDeploymentRevisionsResponse(
                deployments=[],
                next_page_token="def",
            ),
            telcoautomation.ListDeploymentRevisionsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListDeploymentRevisionsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_deployment_revisions(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.DiscardDeploymentChangesRequest,
        dict,
    ],
)
def test_discard_deployment_changes(request_type, transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.discard_deployment_changes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.DiscardDeploymentChangesResponse()
        response = client.discard_deployment_changes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.DiscardDeploymentChangesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.DiscardDeploymentChangesResponse)


def test_discard_deployment_changes_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.discard_deployment_changes), "__call__"
    ) as call:
        client.discard_deployment_changes()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.DiscardDeploymentChangesRequest()


@pytest.mark.asyncio
async def test_discard_deployment_changes_async(
    transport: str = "grpc_asyncio",
    request_type=telcoautomation.DiscardDeploymentChangesRequest,
):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.discard_deployment_changes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.DiscardDeploymentChangesResponse()
        )
        response = await client.discard_deployment_changes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.DiscardDeploymentChangesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.DiscardDeploymentChangesResponse)


@pytest.mark.asyncio
async def test_discard_deployment_changes_async_from_dict():
    await test_discard_deployment_changes_async(request_type=dict)


def test_discard_deployment_changes_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.DiscardDeploymentChangesRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.discard_deployment_changes), "__call__"
    ) as call:
        call.return_value = telcoautomation.DiscardDeploymentChangesResponse()
        client.discard_deployment_changes(request)

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
async def test_discard_deployment_changes_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.DiscardDeploymentChangesRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.discard_deployment_changes), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.DiscardDeploymentChangesResponse()
        )
        await client.discard_deployment_changes(request)

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


def test_discard_deployment_changes_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.discard_deployment_changes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.DiscardDeploymentChangesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.discard_deployment_changes(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_discard_deployment_changes_flattened_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.discard_deployment_changes(
            telcoautomation.DiscardDeploymentChangesRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_discard_deployment_changes_flattened_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.discard_deployment_changes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.DiscardDeploymentChangesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.DiscardDeploymentChangesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.discard_deployment_changes(
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
async def test_discard_deployment_changes_flattened_error_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.discard_deployment_changes(
            telcoautomation.DiscardDeploymentChangesRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.ApplyDeploymentRequest,
        dict,
    ],
)
def test_apply_deployment(request_type, transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.apply_deployment), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.Deployment(
            name="name_value",
            revision_id="revision_id_value",
            source_blueprint_revision="source_blueprint_revision_value",
            state=telcoautomation.Deployment.State.DRAFT,
            display_name="display_name_value",
            repository="repository_value",
            source_provider="source_provider_value",
            workload_cluster="workload_cluster_value",
            deployment_level=telcoautomation.DeploymentLevel.HYDRATION,
            rollback_support=True,
        )
        response = client.apply_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ApplyDeploymentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.Deployment)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.source_blueprint_revision == "source_blueprint_revision_value"
    assert response.state == telcoautomation.Deployment.State.DRAFT
    assert response.display_name == "display_name_value"
    assert response.repository == "repository_value"
    assert response.source_provider == "source_provider_value"
    assert response.workload_cluster == "workload_cluster_value"
    assert response.deployment_level == telcoautomation.DeploymentLevel.HYDRATION
    assert response.rollback_support is True


def test_apply_deployment_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.apply_deployment), "__call__") as call:
        client.apply_deployment()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ApplyDeploymentRequest()


@pytest.mark.asyncio
async def test_apply_deployment_async(
    transport: str = "grpc_asyncio", request_type=telcoautomation.ApplyDeploymentRequest
):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.apply_deployment), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.Deployment(
                name="name_value",
                revision_id="revision_id_value",
                source_blueprint_revision="source_blueprint_revision_value",
                state=telcoautomation.Deployment.State.DRAFT,
                display_name="display_name_value",
                repository="repository_value",
                source_provider="source_provider_value",
                workload_cluster="workload_cluster_value",
                deployment_level=telcoautomation.DeploymentLevel.HYDRATION,
                rollback_support=True,
            )
        )
        response = await client.apply_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ApplyDeploymentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.Deployment)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.source_blueprint_revision == "source_blueprint_revision_value"
    assert response.state == telcoautomation.Deployment.State.DRAFT
    assert response.display_name == "display_name_value"
    assert response.repository == "repository_value"
    assert response.source_provider == "source_provider_value"
    assert response.workload_cluster == "workload_cluster_value"
    assert response.deployment_level == telcoautomation.DeploymentLevel.HYDRATION
    assert response.rollback_support is True


@pytest.mark.asyncio
async def test_apply_deployment_async_from_dict():
    await test_apply_deployment_async(request_type=dict)


def test_apply_deployment_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.ApplyDeploymentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.apply_deployment), "__call__") as call:
        call.return_value = telcoautomation.Deployment()
        client.apply_deployment(request)

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
async def test_apply_deployment_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.ApplyDeploymentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.apply_deployment), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.Deployment()
        )
        await client.apply_deployment(request)

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


def test_apply_deployment_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.apply_deployment), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.Deployment()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.apply_deployment(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_apply_deployment_flattened_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.apply_deployment(
            telcoautomation.ApplyDeploymentRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_apply_deployment_flattened_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.apply_deployment), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.Deployment()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.Deployment()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.apply_deployment(
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
async def test_apply_deployment_flattened_error_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.apply_deployment(
            telcoautomation.ApplyDeploymentRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.ComputeDeploymentStatusRequest,
        dict,
    ],
)
def test_compute_deployment_status(request_type, transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.compute_deployment_status), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.ComputeDeploymentStatusResponse(
            name="name_value",
            aggregated_status=telcoautomation.Status.STATUS_IN_PROGRESS,
        )
        response = client.compute_deployment_status(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ComputeDeploymentStatusRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.ComputeDeploymentStatusResponse)
    assert response.name == "name_value"
    assert response.aggregated_status == telcoautomation.Status.STATUS_IN_PROGRESS


def test_compute_deployment_status_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.compute_deployment_status), "__call__"
    ) as call:
        client.compute_deployment_status()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ComputeDeploymentStatusRequest()


@pytest.mark.asyncio
async def test_compute_deployment_status_async(
    transport: str = "grpc_asyncio",
    request_type=telcoautomation.ComputeDeploymentStatusRequest,
):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.compute_deployment_status), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.ComputeDeploymentStatusResponse(
                name="name_value",
                aggregated_status=telcoautomation.Status.STATUS_IN_PROGRESS,
            )
        )
        response = await client.compute_deployment_status(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ComputeDeploymentStatusRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.ComputeDeploymentStatusResponse)
    assert response.name == "name_value"
    assert response.aggregated_status == telcoautomation.Status.STATUS_IN_PROGRESS


@pytest.mark.asyncio
async def test_compute_deployment_status_async_from_dict():
    await test_compute_deployment_status_async(request_type=dict)


def test_compute_deployment_status_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.ComputeDeploymentStatusRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.compute_deployment_status), "__call__"
    ) as call:
        call.return_value = telcoautomation.ComputeDeploymentStatusResponse()
        client.compute_deployment_status(request)

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
async def test_compute_deployment_status_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.ComputeDeploymentStatusRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.compute_deployment_status), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.ComputeDeploymentStatusResponse()
        )
        await client.compute_deployment_status(request)

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


def test_compute_deployment_status_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.compute_deployment_status), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.ComputeDeploymentStatusResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.compute_deployment_status(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_compute_deployment_status_flattened_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.compute_deployment_status(
            telcoautomation.ComputeDeploymentStatusRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_compute_deployment_status_flattened_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.compute_deployment_status), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.ComputeDeploymentStatusResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.ComputeDeploymentStatusResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.compute_deployment_status(
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
async def test_compute_deployment_status_flattened_error_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.compute_deployment_status(
            telcoautomation.ComputeDeploymentStatusRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.RollbackDeploymentRequest,
        dict,
    ],
)
def test_rollback_deployment(request_type, transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rollback_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.Deployment(
            name="name_value",
            revision_id="revision_id_value",
            source_blueprint_revision="source_blueprint_revision_value",
            state=telcoautomation.Deployment.State.DRAFT,
            display_name="display_name_value",
            repository="repository_value",
            source_provider="source_provider_value",
            workload_cluster="workload_cluster_value",
            deployment_level=telcoautomation.DeploymentLevel.HYDRATION,
            rollback_support=True,
        )
        response = client.rollback_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.RollbackDeploymentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.Deployment)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.source_blueprint_revision == "source_blueprint_revision_value"
    assert response.state == telcoautomation.Deployment.State.DRAFT
    assert response.display_name == "display_name_value"
    assert response.repository == "repository_value"
    assert response.source_provider == "source_provider_value"
    assert response.workload_cluster == "workload_cluster_value"
    assert response.deployment_level == telcoautomation.DeploymentLevel.HYDRATION
    assert response.rollback_support is True


def test_rollback_deployment_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rollback_deployment), "__call__"
    ) as call:
        client.rollback_deployment()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.RollbackDeploymentRequest()


@pytest.mark.asyncio
async def test_rollback_deployment_async(
    transport: str = "grpc_asyncio",
    request_type=telcoautomation.RollbackDeploymentRequest,
):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rollback_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.Deployment(
                name="name_value",
                revision_id="revision_id_value",
                source_blueprint_revision="source_blueprint_revision_value",
                state=telcoautomation.Deployment.State.DRAFT,
                display_name="display_name_value",
                repository="repository_value",
                source_provider="source_provider_value",
                workload_cluster="workload_cluster_value",
                deployment_level=telcoautomation.DeploymentLevel.HYDRATION,
                rollback_support=True,
            )
        )
        response = await client.rollback_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.RollbackDeploymentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.Deployment)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.source_blueprint_revision == "source_blueprint_revision_value"
    assert response.state == telcoautomation.Deployment.State.DRAFT
    assert response.display_name == "display_name_value"
    assert response.repository == "repository_value"
    assert response.source_provider == "source_provider_value"
    assert response.workload_cluster == "workload_cluster_value"
    assert response.deployment_level == telcoautomation.DeploymentLevel.HYDRATION
    assert response.rollback_support is True


@pytest.mark.asyncio
async def test_rollback_deployment_async_from_dict():
    await test_rollback_deployment_async(request_type=dict)


def test_rollback_deployment_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.RollbackDeploymentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rollback_deployment), "__call__"
    ) as call:
        call.return_value = telcoautomation.Deployment()
        client.rollback_deployment(request)

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
async def test_rollback_deployment_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.RollbackDeploymentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rollback_deployment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.Deployment()
        )
        await client.rollback_deployment(request)

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


def test_rollback_deployment_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rollback_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.Deployment()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.rollback_deployment(
            name="name_value",
            revision_id="revision_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].revision_id
        mock_val = "revision_id_value"
        assert arg == mock_val


def test_rollback_deployment_flattened_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.rollback_deployment(
            telcoautomation.RollbackDeploymentRequest(),
            name="name_value",
            revision_id="revision_id_value",
        )


@pytest.mark.asyncio
async def test_rollback_deployment_flattened_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.rollback_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.Deployment()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.Deployment()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.rollback_deployment(
            name="name_value",
            revision_id="revision_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].revision_id
        mock_val = "revision_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_rollback_deployment_flattened_error_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.rollback_deployment(
            telcoautomation.RollbackDeploymentRequest(),
            name="name_value",
            revision_id="revision_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.GetHydratedDeploymentRequest,
        dict,
    ],
)
def test_get_hydrated_deployment(request_type, transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_hydrated_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.HydratedDeployment(
            name="name_value",
            state=telcoautomation.HydratedDeployment.State.DRAFT,
            workload_cluster="workload_cluster_value",
        )
        response = client.get_hydrated_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.GetHydratedDeploymentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.HydratedDeployment)
    assert response.name == "name_value"
    assert response.state == telcoautomation.HydratedDeployment.State.DRAFT
    assert response.workload_cluster == "workload_cluster_value"


def test_get_hydrated_deployment_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_hydrated_deployment), "__call__"
    ) as call:
        client.get_hydrated_deployment()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.GetHydratedDeploymentRequest()


@pytest.mark.asyncio
async def test_get_hydrated_deployment_async(
    transport: str = "grpc_asyncio",
    request_type=telcoautomation.GetHydratedDeploymentRequest,
):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_hydrated_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.HydratedDeployment(
                name="name_value",
                state=telcoautomation.HydratedDeployment.State.DRAFT,
                workload_cluster="workload_cluster_value",
            )
        )
        response = await client.get_hydrated_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.GetHydratedDeploymentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.HydratedDeployment)
    assert response.name == "name_value"
    assert response.state == telcoautomation.HydratedDeployment.State.DRAFT
    assert response.workload_cluster == "workload_cluster_value"


@pytest.mark.asyncio
async def test_get_hydrated_deployment_async_from_dict():
    await test_get_hydrated_deployment_async(request_type=dict)


def test_get_hydrated_deployment_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.GetHydratedDeploymentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_hydrated_deployment), "__call__"
    ) as call:
        call.return_value = telcoautomation.HydratedDeployment()
        client.get_hydrated_deployment(request)

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
async def test_get_hydrated_deployment_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.GetHydratedDeploymentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_hydrated_deployment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.HydratedDeployment()
        )
        await client.get_hydrated_deployment(request)

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


def test_get_hydrated_deployment_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_hydrated_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.HydratedDeployment()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_hydrated_deployment(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_hydrated_deployment_flattened_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_hydrated_deployment(
            telcoautomation.GetHydratedDeploymentRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_hydrated_deployment_flattened_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_hydrated_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.HydratedDeployment()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.HydratedDeployment()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_hydrated_deployment(
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
async def test_get_hydrated_deployment_flattened_error_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_hydrated_deployment(
            telcoautomation.GetHydratedDeploymentRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.ListHydratedDeploymentsRequest,
        dict,
    ],
)
def test_list_hydrated_deployments(request_type, transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_hydrated_deployments), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.ListHydratedDeploymentsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_hydrated_deployments(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ListHydratedDeploymentsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListHydratedDeploymentsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_hydrated_deployments_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_hydrated_deployments), "__call__"
    ) as call:
        client.list_hydrated_deployments()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ListHydratedDeploymentsRequest()


@pytest.mark.asyncio
async def test_list_hydrated_deployments_async(
    transport: str = "grpc_asyncio",
    request_type=telcoautomation.ListHydratedDeploymentsRequest,
):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_hydrated_deployments), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.ListHydratedDeploymentsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_hydrated_deployments(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ListHydratedDeploymentsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListHydratedDeploymentsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_hydrated_deployments_async_from_dict():
    await test_list_hydrated_deployments_async(request_type=dict)


def test_list_hydrated_deployments_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.ListHydratedDeploymentsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_hydrated_deployments), "__call__"
    ) as call:
        call.return_value = telcoautomation.ListHydratedDeploymentsResponse()
        client.list_hydrated_deployments(request)

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
async def test_list_hydrated_deployments_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.ListHydratedDeploymentsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_hydrated_deployments), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.ListHydratedDeploymentsResponse()
        )
        await client.list_hydrated_deployments(request)

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


def test_list_hydrated_deployments_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_hydrated_deployments), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.ListHydratedDeploymentsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_hydrated_deployments(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_hydrated_deployments_flattened_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_hydrated_deployments(
            telcoautomation.ListHydratedDeploymentsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_hydrated_deployments_flattened_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_hydrated_deployments), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.ListHydratedDeploymentsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.ListHydratedDeploymentsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_hydrated_deployments(
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
async def test_list_hydrated_deployments_flattened_error_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_hydrated_deployments(
            telcoautomation.ListHydratedDeploymentsRequest(),
            parent="parent_value",
        )


def test_list_hydrated_deployments_pager(transport_name: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_hydrated_deployments), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.ListHydratedDeploymentsResponse(
                hydrated_deployments=[
                    telcoautomation.HydratedDeployment(),
                    telcoautomation.HydratedDeployment(),
                    telcoautomation.HydratedDeployment(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListHydratedDeploymentsResponse(
                hydrated_deployments=[],
                next_page_token="def",
            ),
            telcoautomation.ListHydratedDeploymentsResponse(
                hydrated_deployments=[
                    telcoautomation.HydratedDeployment(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListHydratedDeploymentsResponse(
                hydrated_deployments=[
                    telcoautomation.HydratedDeployment(),
                    telcoautomation.HydratedDeployment(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_hydrated_deployments(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, telcoautomation.HydratedDeployment) for i in results)


def test_list_hydrated_deployments_pages(transport_name: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_hydrated_deployments), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.ListHydratedDeploymentsResponse(
                hydrated_deployments=[
                    telcoautomation.HydratedDeployment(),
                    telcoautomation.HydratedDeployment(),
                    telcoautomation.HydratedDeployment(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListHydratedDeploymentsResponse(
                hydrated_deployments=[],
                next_page_token="def",
            ),
            telcoautomation.ListHydratedDeploymentsResponse(
                hydrated_deployments=[
                    telcoautomation.HydratedDeployment(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListHydratedDeploymentsResponse(
                hydrated_deployments=[
                    telcoautomation.HydratedDeployment(),
                    telcoautomation.HydratedDeployment(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_hydrated_deployments(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_hydrated_deployments_async_pager():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_hydrated_deployments),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.ListHydratedDeploymentsResponse(
                hydrated_deployments=[
                    telcoautomation.HydratedDeployment(),
                    telcoautomation.HydratedDeployment(),
                    telcoautomation.HydratedDeployment(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListHydratedDeploymentsResponse(
                hydrated_deployments=[],
                next_page_token="def",
            ),
            telcoautomation.ListHydratedDeploymentsResponse(
                hydrated_deployments=[
                    telcoautomation.HydratedDeployment(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListHydratedDeploymentsResponse(
                hydrated_deployments=[
                    telcoautomation.HydratedDeployment(),
                    telcoautomation.HydratedDeployment(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_hydrated_deployments(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, telcoautomation.HydratedDeployment) for i in responses)


@pytest.mark.asyncio
async def test_list_hydrated_deployments_async_pages():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_hydrated_deployments),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            telcoautomation.ListHydratedDeploymentsResponse(
                hydrated_deployments=[
                    telcoautomation.HydratedDeployment(),
                    telcoautomation.HydratedDeployment(),
                    telcoautomation.HydratedDeployment(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListHydratedDeploymentsResponse(
                hydrated_deployments=[],
                next_page_token="def",
            ),
            telcoautomation.ListHydratedDeploymentsResponse(
                hydrated_deployments=[
                    telcoautomation.HydratedDeployment(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListHydratedDeploymentsResponse(
                hydrated_deployments=[
                    telcoautomation.HydratedDeployment(),
                    telcoautomation.HydratedDeployment(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_hydrated_deployments(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.UpdateHydratedDeploymentRequest,
        dict,
    ],
)
def test_update_hydrated_deployment(request_type, transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_hydrated_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.HydratedDeployment(
            name="name_value",
            state=telcoautomation.HydratedDeployment.State.DRAFT,
            workload_cluster="workload_cluster_value",
        )
        response = client.update_hydrated_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.UpdateHydratedDeploymentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.HydratedDeployment)
    assert response.name == "name_value"
    assert response.state == telcoautomation.HydratedDeployment.State.DRAFT
    assert response.workload_cluster == "workload_cluster_value"


def test_update_hydrated_deployment_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_hydrated_deployment), "__call__"
    ) as call:
        client.update_hydrated_deployment()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.UpdateHydratedDeploymentRequest()


@pytest.mark.asyncio
async def test_update_hydrated_deployment_async(
    transport: str = "grpc_asyncio",
    request_type=telcoautomation.UpdateHydratedDeploymentRequest,
):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_hydrated_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.HydratedDeployment(
                name="name_value",
                state=telcoautomation.HydratedDeployment.State.DRAFT,
                workload_cluster="workload_cluster_value",
            )
        )
        response = await client.update_hydrated_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.UpdateHydratedDeploymentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.HydratedDeployment)
    assert response.name == "name_value"
    assert response.state == telcoautomation.HydratedDeployment.State.DRAFT
    assert response.workload_cluster == "workload_cluster_value"


@pytest.mark.asyncio
async def test_update_hydrated_deployment_async_from_dict():
    await test_update_hydrated_deployment_async(request_type=dict)


def test_update_hydrated_deployment_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.UpdateHydratedDeploymentRequest()

    request.hydrated_deployment.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_hydrated_deployment), "__call__"
    ) as call:
        call.return_value = telcoautomation.HydratedDeployment()
        client.update_hydrated_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "hydrated_deployment.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_hydrated_deployment_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.UpdateHydratedDeploymentRequest()

    request.hydrated_deployment.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_hydrated_deployment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.HydratedDeployment()
        )
        await client.update_hydrated_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "hydrated_deployment.name=name_value",
    ) in kw["metadata"]


def test_update_hydrated_deployment_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_hydrated_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.HydratedDeployment()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_hydrated_deployment(
            hydrated_deployment=telcoautomation.HydratedDeployment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].hydrated_deployment
        mock_val = telcoautomation.HydratedDeployment(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_hydrated_deployment_flattened_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_hydrated_deployment(
            telcoautomation.UpdateHydratedDeploymentRequest(),
            hydrated_deployment=telcoautomation.HydratedDeployment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_hydrated_deployment_flattened_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_hydrated_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.HydratedDeployment()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.HydratedDeployment()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_hydrated_deployment(
            hydrated_deployment=telcoautomation.HydratedDeployment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].hydrated_deployment
        mock_val = telcoautomation.HydratedDeployment(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_hydrated_deployment_flattened_error_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_hydrated_deployment(
            telcoautomation.UpdateHydratedDeploymentRequest(),
            hydrated_deployment=telcoautomation.HydratedDeployment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.ApplyHydratedDeploymentRequest,
        dict,
    ],
)
def test_apply_hydrated_deployment(request_type, transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.apply_hydrated_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.HydratedDeployment(
            name="name_value",
            state=telcoautomation.HydratedDeployment.State.DRAFT,
            workload_cluster="workload_cluster_value",
        )
        response = client.apply_hydrated_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ApplyHydratedDeploymentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.HydratedDeployment)
    assert response.name == "name_value"
    assert response.state == telcoautomation.HydratedDeployment.State.DRAFT
    assert response.workload_cluster == "workload_cluster_value"


def test_apply_hydrated_deployment_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.apply_hydrated_deployment), "__call__"
    ) as call:
        client.apply_hydrated_deployment()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ApplyHydratedDeploymentRequest()


@pytest.mark.asyncio
async def test_apply_hydrated_deployment_async(
    transport: str = "grpc_asyncio",
    request_type=telcoautomation.ApplyHydratedDeploymentRequest,
):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.apply_hydrated_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.HydratedDeployment(
                name="name_value",
                state=telcoautomation.HydratedDeployment.State.DRAFT,
                workload_cluster="workload_cluster_value",
            )
        )
        response = await client.apply_hydrated_deployment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == telcoautomation.ApplyHydratedDeploymentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.HydratedDeployment)
    assert response.name == "name_value"
    assert response.state == telcoautomation.HydratedDeployment.State.DRAFT
    assert response.workload_cluster == "workload_cluster_value"


@pytest.mark.asyncio
async def test_apply_hydrated_deployment_async_from_dict():
    await test_apply_hydrated_deployment_async(request_type=dict)


def test_apply_hydrated_deployment_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.ApplyHydratedDeploymentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.apply_hydrated_deployment), "__call__"
    ) as call:
        call.return_value = telcoautomation.HydratedDeployment()
        client.apply_hydrated_deployment(request)

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
async def test_apply_hydrated_deployment_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = telcoautomation.ApplyHydratedDeploymentRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.apply_hydrated_deployment), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.HydratedDeployment()
        )
        await client.apply_hydrated_deployment(request)

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


def test_apply_hydrated_deployment_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.apply_hydrated_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.HydratedDeployment()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.apply_hydrated_deployment(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_apply_hydrated_deployment_flattened_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.apply_hydrated_deployment(
            telcoautomation.ApplyHydratedDeploymentRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_apply_hydrated_deployment_flattened_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.apply_hydrated_deployment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = telcoautomation.HydratedDeployment()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            telcoautomation.HydratedDeployment()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.apply_hydrated_deployment(
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
async def test_apply_hydrated_deployment_flattened_error_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.apply_hydrated_deployment(
            telcoautomation.ApplyHydratedDeploymentRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.ListOrchestrationClustersRequest,
        dict,
    ],
)
def test_list_orchestration_clusters_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.ListOrchestrationClustersResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.ListOrchestrationClustersResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_orchestration_clusters(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListOrchestrationClustersPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_orchestration_clusters_rest_required_fields(
    request_type=telcoautomation.ListOrchestrationClustersRequest,
):
    transport_class = transports.TelcoAutomationRestTransport

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
    ).list_orchestration_clusters._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_orchestration_clusters._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "order_by",
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = telcoautomation.ListOrchestrationClustersResponse()
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

            # Convert return value to protobuf type
            return_value = telcoautomation.ListOrchestrationClustersResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_orchestration_clusters(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_orchestration_clusters_rest_unset_required_fields():
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_orchestration_clusters._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "orderBy",
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_orchestration_clusters_rest_interceptors(null_interceptor):
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TelcoAutomationRestInterceptor(),
    )
    client = TelcoAutomationClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "post_list_orchestration_clusters"
    ) as post, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "pre_list_orchestration_clusters"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = telcoautomation.ListOrchestrationClustersRequest.pb(
            telcoautomation.ListOrchestrationClustersRequest()
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
            telcoautomation.ListOrchestrationClustersResponse.to_json(
                telcoautomation.ListOrchestrationClustersResponse()
            )
        )

        request = telcoautomation.ListOrchestrationClustersRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = telcoautomation.ListOrchestrationClustersResponse()

        client.list_orchestration_clusters(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_orchestration_clusters_rest_bad_request(
    transport: str = "rest",
    request_type=telcoautomation.ListOrchestrationClustersRequest,
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
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
        client.list_orchestration_clusters(request)


def test_list_orchestration_clusters_rest_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.ListOrchestrationClustersResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.ListOrchestrationClustersResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_orchestration_clusters(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/orchestrationClusters"
            % client.transport._host,
            args[1],
        )


def test_list_orchestration_clusters_rest_flattened_error(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_orchestration_clusters(
            telcoautomation.ListOrchestrationClustersRequest(),
            parent="parent_value",
        )


def test_list_orchestration_clusters_rest_pager(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            telcoautomation.ListOrchestrationClustersResponse(
                orchestration_clusters=[
                    telcoautomation.OrchestrationCluster(),
                    telcoautomation.OrchestrationCluster(),
                    telcoautomation.OrchestrationCluster(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListOrchestrationClustersResponse(
                orchestration_clusters=[],
                next_page_token="def",
            ),
            telcoautomation.ListOrchestrationClustersResponse(
                orchestration_clusters=[
                    telcoautomation.OrchestrationCluster(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListOrchestrationClustersResponse(
                orchestration_clusters=[
                    telcoautomation.OrchestrationCluster(),
                    telcoautomation.OrchestrationCluster(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            telcoautomation.ListOrchestrationClustersResponse.to_json(x)
            for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_orchestration_clusters(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, telcoautomation.OrchestrationCluster) for i in results)

        pages = list(client.list_orchestration_clusters(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.GetOrchestrationClusterRequest,
        dict,
    ],
)
def test_get_orchestration_cluster_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.OrchestrationCluster(
            name="name_value",
            tna_version="tna_version_value",
            state=telcoautomation.OrchestrationCluster.State.CREATING,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.OrchestrationCluster.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_orchestration_cluster(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.OrchestrationCluster)
    assert response.name == "name_value"
    assert response.tna_version == "tna_version_value"
    assert response.state == telcoautomation.OrchestrationCluster.State.CREATING


def test_get_orchestration_cluster_rest_required_fields(
    request_type=telcoautomation.GetOrchestrationClusterRequest,
):
    transport_class = transports.TelcoAutomationRestTransport

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
    ).get_orchestration_cluster._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_orchestration_cluster._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = telcoautomation.OrchestrationCluster()
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

            # Convert return value to protobuf type
            return_value = telcoautomation.OrchestrationCluster.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_orchestration_cluster(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_orchestration_cluster_rest_unset_required_fields():
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_orchestration_cluster._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_orchestration_cluster_rest_interceptors(null_interceptor):
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TelcoAutomationRestInterceptor(),
    )
    client = TelcoAutomationClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "post_get_orchestration_cluster"
    ) as post, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "pre_get_orchestration_cluster"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = telcoautomation.GetOrchestrationClusterRequest.pb(
            telcoautomation.GetOrchestrationClusterRequest()
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
        req.return_value._content = telcoautomation.OrchestrationCluster.to_json(
            telcoautomation.OrchestrationCluster()
        )

        request = telcoautomation.GetOrchestrationClusterRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = telcoautomation.OrchestrationCluster()

        client.get_orchestration_cluster(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_orchestration_cluster_rest_bad_request(
    transport: str = "rest", request_type=telcoautomation.GetOrchestrationClusterRequest
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3"
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
        client.get_orchestration_cluster(request)


def test_get_orchestration_cluster_rest_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.OrchestrationCluster()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.OrchestrationCluster.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_orchestration_cluster(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/orchestrationClusters/*}"
            % client.transport._host,
            args[1],
        )


def test_get_orchestration_cluster_rest_flattened_error(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_orchestration_cluster(
            telcoautomation.GetOrchestrationClusterRequest(),
            name="name_value",
        )


def test_get_orchestration_cluster_rest_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.CreateOrchestrationClusterRequest,
        dict,
    ],
)
def test_create_orchestration_cluster_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["orchestration_cluster"] = {
        "name": "name_value",
        "management_config": {
            "standard_management_config": {
                "network": "network_value",
                "subnet": "subnet_value",
                "master_ipv4_cidr_block": "master_ipv4_cidr_block_value",
                "cluster_cidr_block": "cluster_cidr_block_value",
                "services_cidr_block": "services_cidr_block_value",
                "cluster_named_range": "cluster_named_range_value",
                "services_named_range": "services_named_range_value",
                "master_authorized_networks_config": {
                    "cidr_blocks": [
                        {
                            "display_name": "display_name_value",
                            "cidr_block": "cidr_block_value",
                        }
                    ]
                },
            },
            "full_management_config": {
                "network": "network_value",
                "subnet": "subnet_value",
                "master_ipv4_cidr_block": "master_ipv4_cidr_block_value",
                "cluster_cidr_block": "cluster_cidr_block_value",
                "services_cidr_block": "services_cidr_block_value",
                "cluster_named_range": "cluster_named_range_value",
                "services_named_range": "services_named_range_value",
                "master_authorized_networks_config": {},
            },
        },
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "tna_version": "tna_version_value",
        "state": 1,
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = telcoautomation.CreateOrchestrationClusterRequest.meta.fields[
        "orchestration_cluster"
    ]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init[
        "orchestration_cluster"
    ].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["orchestration_cluster"][field])):
                    del request_init["orchestration_cluster"][field][i][subfield]
            else:
                del request_init["orchestration_cluster"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_orchestration_cluster(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_orchestration_cluster_rest_required_fields(
    request_type=telcoautomation.CreateOrchestrationClusterRequest,
):
    transport_class = transports.TelcoAutomationRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["orchestration_cluster_id"] = ""
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
    assert "orchestrationClusterId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_orchestration_cluster._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "orchestrationClusterId" in jsonified_request
    assert (
        jsonified_request["orchestrationClusterId"]
        == request_init["orchestration_cluster_id"]
    )

    jsonified_request["parent"] = "parent_value"
    jsonified_request["orchestrationClusterId"] = "orchestration_cluster_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_orchestration_cluster._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "orchestration_cluster_id",
            "request_id",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "orchestrationClusterId" in jsonified_request
    assert (
        jsonified_request["orchestrationClusterId"] == "orchestration_cluster_id_value"
    )

    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
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
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_orchestration_cluster(request)

            expected_params = [
                (
                    "orchestrationClusterId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_orchestration_cluster_rest_unset_required_fields():
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_orchestration_cluster._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "orchestrationClusterId",
                "requestId",
            )
        )
        & set(
            (
                "parent",
                "orchestrationClusterId",
                "orchestrationCluster",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_orchestration_cluster_rest_interceptors(null_interceptor):
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TelcoAutomationRestInterceptor(),
    )
    client = TelcoAutomationClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "post_create_orchestration_cluster"
    ) as post, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "pre_create_orchestration_cluster"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = telcoautomation.CreateOrchestrationClusterRequest.pb(
            telcoautomation.CreateOrchestrationClusterRequest()
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
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = telcoautomation.CreateOrchestrationClusterRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_orchestration_cluster(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_orchestration_cluster_rest_bad_request(
    transport: str = "rest",
    request_type=telcoautomation.CreateOrchestrationClusterRequest,
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
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
        client.create_orchestration_cluster(request)


def test_create_orchestration_cluster_rest_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            orchestration_cluster=telcoautomation.OrchestrationCluster(
                name="name_value"
            ),
            orchestration_cluster_id="orchestration_cluster_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_orchestration_cluster(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/orchestrationClusters"
            % client.transport._host,
            args[1],
        )


def test_create_orchestration_cluster_rest_flattened_error(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_orchestration_cluster(
            telcoautomation.CreateOrchestrationClusterRequest(),
            parent="parent_value",
            orchestration_cluster=telcoautomation.OrchestrationCluster(
                name="name_value"
            ),
            orchestration_cluster_id="orchestration_cluster_id_value",
        )


def test_create_orchestration_cluster_rest_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.DeleteOrchestrationClusterRequest,
        dict,
    ],
)
def test_delete_orchestration_cluster_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_orchestration_cluster(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_orchestration_cluster_rest_required_fields(
    request_type=telcoautomation.DeleteOrchestrationClusterRequest,
):
    transport_class = transports.TelcoAutomationRestTransport

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
    ).delete_orchestration_cluster._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_orchestration_cluster._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
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
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_orchestration_cluster(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_orchestration_cluster_rest_unset_required_fields():
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_orchestration_cluster._get_unset_required_fields({})
    assert set(unset_fields) == (set(("requestId",)) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_orchestration_cluster_rest_interceptors(null_interceptor):
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TelcoAutomationRestInterceptor(),
    )
    client = TelcoAutomationClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "post_delete_orchestration_cluster"
    ) as post, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "pre_delete_orchestration_cluster"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = telcoautomation.DeleteOrchestrationClusterRequest.pb(
            telcoautomation.DeleteOrchestrationClusterRequest()
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
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = telcoautomation.DeleteOrchestrationClusterRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_orchestration_cluster(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_orchestration_cluster_rest_bad_request(
    transport: str = "rest",
    request_type=telcoautomation.DeleteOrchestrationClusterRequest,
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3"
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
        client.delete_orchestration_cluster(request)


def test_delete_orchestration_cluster_rest_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_orchestration_cluster(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/orchestrationClusters/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_orchestration_cluster_rest_flattened_error(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_orchestration_cluster(
            telcoautomation.DeleteOrchestrationClusterRequest(),
            name="name_value",
        )


def test_delete_orchestration_cluster_rest_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.ListEdgeSlmsRequest,
        dict,
    ],
)
def test_list_edge_slms_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.ListEdgeSlmsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.ListEdgeSlmsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_edge_slms(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListEdgeSlmsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_edge_slms_rest_required_fields(
    request_type=telcoautomation.ListEdgeSlmsRequest,
):
    transport_class = transports.TelcoAutomationRestTransport

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
    ).list_edge_slms._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_edge_slms._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "order_by",
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = telcoautomation.ListEdgeSlmsResponse()
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

            # Convert return value to protobuf type
            return_value = telcoautomation.ListEdgeSlmsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_edge_slms(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_edge_slms_rest_unset_required_fields():
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_edge_slms._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "orderBy",
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_edge_slms_rest_interceptors(null_interceptor):
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TelcoAutomationRestInterceptor(),
    )
    client = TelcoAutomationClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "post_list_edge_slms"
    ) as post, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "pre_list_edge_slms"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = telcoautomation.ListEdgeSlmsRequest.pb(
            telcoautomation.ListEdgeSlmsRequest()
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
        req.return_value._content = telcoautomation.ListEdgeSlmsResponse.to_json(
            telcoautomation.ListEdgeSlmsResponse()
        )

        request = telcoautomation.ListEdgeSlmsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = telcoautomation.ListEdgeSlmsResponse()

        client.list_edge_slms(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_edge_slms_rest_bad_request(
    transport: str = "rest", request_type=telcoautomation.ListEdgeSlmsRequest
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
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
        client.list_edge_slms(request)


def test_list_edge_slms_rest_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.ListEdgeSlmsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.ListEdgeSlmsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_edge_slms(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/edgeSlms" % client.transport._host,
            args[1],
        )


def test_list_edge_slms_rest_flattened_error(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_edge_slms(
            telcoautomation.ListEdgeSlmsRequest(),
            parent="parent_value",
        )


def test_list_edge_slms_rest_pager(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            telcoautomation.ListEdgeSlmsResponse(
                edge_slms=[
                    telcoautomation.EdgeSlm(),
                    telcoautomation.EdgeSlm(),
                    telcoautomation.EdgeSlm(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListEdgeSlmsResponse(
                edge_slms=[],
                next_page_token="def",
            ),
            telcoautomation.ListEdgeSlmsResponse(
                edge_slms=[
                    telcoautomation.EdgeSlm(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListEdgeSlmsResponse(
                edge_slms=[
                    telcoautomation.EdgeSlm(),
                    telcoautomation.EdgeSlm(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            telcoautomation.ListEdgeSlmsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_edge_slms(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, telcoautomation.EdgeSlm) for i in results)

        pages = list(client.list_edge_slms(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.GetEdgeSlmRequest,
        dict,
    ],
)
def test_get_edge_slm_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/edgeSlms/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.EdgeSlm(
            name="name_value",
            orchestration_cluster="orchestration_cluster_value",
            tna_version="tna_version_value",
            state=telcoautomation.EdgeSlm.State.CREATING,
            workload_cluster_type=telcoautomation.EdgeSlm.WorkloadClusterType.GDCE,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.EdgeSlm.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_edge_slm(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.EdgeSlm)
    assert response.name == "name_value"
    assert response.orchestration_cluster == "orchestration_cluster_value"
    assert response.tna_version == "tna_version_value"
    assert response.state == telcoautomation.EdgeSlm.State.CREATING
    assert (
        response.workload_cluster_type
        == telcoautomation.EdgeSlm.WorkloadClusterType.GDCE
    )


def test_get_edge_slm_rest_required_fields(
    request_type=telcoautomation.GetEdgeSlmRequest,
):
    transport_class = transports.TelcoAutomationRestTransport

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
    ).get_edge_slm._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_edge_slm._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = telcoautomation.EdgeSlm()
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

            # Convert return value to protobuf type
            return_value = telcoautomation.EdgeSlm.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_edge_slm(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_edge_slm_rest_unset_required_fields():
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_edge_slm._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_edge_slm_rest_interceptors(null_interceptor):
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TelcoAutomationRestInterceptor(),
    )
    client = TelcoAutomationClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "post_get_edge_slm"
    ) as post, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "pre_get_edge_slm"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = telcoautomation.GetEdgeSlmRequest.pb(
            telcoautomation.GetEdgeSlmRequest()
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
        req.return_value._content = telcoautomation.EdgeSlm.to_json(
            telcoautomation.EdgeSlm()
        )

        request = telcoautomation.GetEdgeSlmRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = telcoautomation.EdgeSlm()

        client.get_edge_slm(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_edge_slm_rest_bad_request(
    transport: str = "rest", request_type=telcoautomation.GetEdgeSlmRequest
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/edgeSlms/sample3"}
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
        client.get_edge_slm(request)


def test_get_edge_slm_rest_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.EdgeSlm()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/locations/sample2/edgeSlms/sample3"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.EdgeSlm.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_edge_slm(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/edgeSlms/*}" % client.transport._host,
            args[1],
        )


def test_get_edge_slm_rest_flattened_error(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_edge_slm(
            telcoautomation.GetEdgeSlmRequest(),
            name="name_value",
        )


def test_get_edge_slm_rest_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.CreateEdgeSlmRequest,
        dict,
    ],
)
def test_create_edge_slm_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["edge_slm"] = {
        "name": "name_value",
        "orchestration_cluster": "orchestration_cluster_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "tna_version": "tna_version_value",
        "state": 1,
        "workload_cluster_type": 1,
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = telcoautomation.CreateEdgeSlmRequest.meta.fields["edge_slm"]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["edge_slm"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["edge_slm"][field])):
                    del request_init["edge_slm"][field][i][subfield]
            else:
                del request_init["edge_slm"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_edge_slm(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_edge_slm_rest_required_fields(
    request_type=telcoautomation.CreateEdgeSlmRequest,
):
    transport_class = transports.TelcoAutomationRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["edge_slm_id"] = ""
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
    assert "edgeSlmId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_edge_slm._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "edgeSlmId" in jsonified_request
    assert jsonified_request["edgeSlmId"] == request_init["edge_slm_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["edgeSlmId"] = "edge_slm_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_edge_slm._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "edge_slm_id",
            "request_id",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "edgeSlmId" in jsonified_request
    assert jsonified_request["edgeSlmId"] == "edge_slm_id_value"

    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
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
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_edge_slm(request)

            expected_params = [
                (
                    "edgeSlmId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_edge_slm_rest_unset_required_fields():
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_edge_slm._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "edgeSlmId",
                "requestId",
            )
        )
        & set(
            (
                "parent",
                "edgeSlmId",
                "edgeSlm",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_edge_slm_rest_interceptors(null_interceptor):
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TelcoAutomationRestInterceptor(),
    )
    client = TelcoAutomationClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "post_create_edge_slm"
    ) as post, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "pre_create_edge_slm"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = telcoautomation.CreateEdgeSlmRequest.pb(
            telcoautomation.CreateEdgeSlmRequest()
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
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = telcoautomation.CreateEdgeSlmRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_edge_slm(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_edge_slm_rest_bad_request(
    transport: str = "rest", request_type=telcoautomation.CreateEdgeSlmRequest
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
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
        client.create_edge_slm(request)


def test_create_edge_slm_rest_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            edge_slm=telcoautomation.EdgeSlm(name="name_value"),
            edge_slm_id="edge_slm_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_edge_slm(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/edgeSlms" % client.transport._host,
            args[1],
        )


def test_create_edge_slm_rest_flattened_error(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_edge_slm(
            telcoautomation.CreateEdgeSlmRequest(),
            parent="parent_value",
            edge_slm=telcoautomation.EdgeSlm(name="name_value"),
            edge_slm_id="edge_slm_id_value",
        )


def test_create_edge_slm_rest_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.DeleteEdgeSlmRequest,
        dict,
    ],
)
def test_delete_edge_slm_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/edgeSlms/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_edge_slm(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_edge_slm_rest_required_fields(
    request_type=telcoautomation.DeleteEdgeSlmRequest,
):
    transport_class = transports.TelcoAutomationRestTransport

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
    ).delete_edge_slm._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_edge_slm._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
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
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_edge_slm(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_edge_slm_rest_unset_required_fields():
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_edge_slm._get_unset_required_fields({})
    assert set(unset_fields) == (set(("requestId",)) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_edge_slm_rest_interceptors(null_interceptor):
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TelcoAutomationRestInterceptor(),
    )
    client = TelcoAutomationClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "post_delete_edge_slm"
    ) as post, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "pre_delete_edge_slm"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = telcoautomation.DeleteEdgeSlmRequest.pb(
            telcoautomation.DeleteEdgeSlmRequest()
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
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = telcoautomation.DeleteEdgeSlmRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_edge_slm(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_edge_slm_rest_bad_request(
    transport: str = "rest", request_type=telcoautomation.DeleteEdgeSlmRequest
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/edgeSlms/sample3"}
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
        client.delete_edge_slm(request)


def test_delete_edge_slm_rest_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/locations/sample2/edgeSlms/sample3"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_edge_slm(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/edgeSlms/*}" % client.transport._host,
            args[1],
        )


def test_delete_edge_slm_rest_flattened_error(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_edge_slm(
            telcoautomation.DeleteEdgeSlmRequest(),
            name="name_value",
        )


def test_delete_edge_slm_rest_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.CreateBlueprintRequest,
        dict,
    ],
)
def test_create_blueprint_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/orchestrationClusters/sample3"
    }
    request_init["blueprint"] = {
        "name": "name_value",
        "revision_id": "revision_id_value",
        "source_blueprint": "source_blueprint_value",
        "revision_create_time": {"seconds": 751, "nanos": 543},
        "approval_state": 1,
        "display_name": "display_name_value",
        "repository": "repository_value",
        "files": [
            {
                "path": "path_value",
                "content": "content_value",
                "deleted": True,
                "editable": True,
            }
        ],
        "labels": {},
        "create_time": {},
        "update_time": {},
        "source_provider": "source_provider_value",
        "deployment_level": 1,
        "rollback_support": True,
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = telcoautomation.CreateBlueprintRequest.meta.fields["blueprint"]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["blueprint"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["blueprint"][field])):
                    del request_init["blueprint"][field][i][subfield]
            else:
                del request_init["blueprint"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.Blueprint(
            name="name_value",
            revision_id="revision_id_value",
            source_blueprint="source_blueprint_value",
            approval_state=telcoautomation.Blueprint.ApprovalState.DRAFT,
            display_name="display_name_value",
            repository="repository_value",
            source_provider="source_provider_value",
            deployment_level=telcoautomation.DeploymentLevel.HYDRATION,
            rollback_support=True,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.Blueprint.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_blueprint(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.Blueprint)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.source_blueprint == "source_blueprint_value"
    assert response.approval_state == telcoautomation.Blueprint.ApprovalState.DRAFT
    assert response.display_name == "display_name_value"
    assert response.repository == "repository_value"
    assert response.source_provider == "source_provider_value"
    assert response.deployment_level == telcoautomation.DeploymentLevel.HYDRATION
    assert response.rollback_support is True


def test_create_blueprint_rest_required_fields(
    request_type=telcoautomation.CreateBlueprintRequest,
):
    transport_class = transports.TelcoAutomationRestTransport

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
    ).create_blueprint._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_blueprint._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("blueprint_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = telcoautomation.Blueprint()
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

            # Convert return value to protobuf type
            return_value = telcoautomation.Blueprint.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_blueprint(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_blueprint_rest_unset_required_fields():
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_blueprint._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("blueprintId",))
        & set(
            (
                "parent",
                "blueprint",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_blueprint_rest_interceptors(null_interceptor):
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TelcoAutomationRestInterceptor(),
    )
    client = TelcoAutomationClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "post_create_blueprint"
    ) as post, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "pre_create_blueprint"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = telcoautomation.CreateBlueprintRequest.pb(
            telcoautomation.CreateBlueprintRequest()
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
        req.return_value._content = telcoautomation.Blueprint.to_json(
            telcoautomation.Blueprint()
        )

        request = telcoautomation.CreateBlueprintRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = telcoautomation.Blueprint()

        client.create_blueprint(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_blueprint_rest_bad_request(
    transport: str = "rest", request_type=telcoautomation.CreateBlueprintRequest
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/orchestrationClusters/sample3"
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
        client.create_blueprint(request)


def test_create_blueprint_rest_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.Blueprint()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/orchestrationClusters/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            blueprint=telcoautomation.Blueprint(name="name_value"),
            blueprint_id="blueprint_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.Blueprint.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_blueprint(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/orchestrationClusters/*}/blueprints"
            % client.transport._host,
            args[1],
        )


def test_create_blueprint_rest_flattened_error(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_blueprint(
            telcoautomation.CreateBlueprintRequest(),
            parent="parent_value",
            blueprint=telcoautomation.Blueprint(name="name_value"),
            blueprint_id="blueprint_id_value",
        )


def test_create_blueprint_rest_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.UpdateBlueprintRequest,
        dict,
    ],
)
def test_update_blueprint_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "blueprint": {
            "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/blueprints/sample4"
        }
    }
    request_init["blueprint"] = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/blueprints/sample4",
        "revision_id": "revision_id_value",
        "source_blueprint": "source_blueprint_value",
        "revision_create_time": {"seconds": 751, "nanos": 543},
        "approval_state": 1,
        "display_name": "display_name_value",
        "repository": "repository_value",
        "files": [
            {
                "path": "path_value",
                "content": "content_value",
                "deleted": True,
                "editable": True,
            }
        ],
        "labels": {},
        "create_time": {},
        "update_time": {},
        "source_provider": "source_provider_value",
        "deployment_level": 1,
        "rollback_support": True,
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = telcoautomation.UpdateBlueprintRequest.meta.fields["blueprint"]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["blueprint"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["blueprint"][field])):
                    del request_init["blueprint"][field][i][subfield]
            else:
                del request_init["blueprint"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.Blueprint(
            name="name_value",
            revision_id="revision_id_value",
            source_blueprint="source_blueprint_value",
            approval_state=telcoautomation.Blueprint.ApprovalState.DRAFT,
            display_name="display_name_value",
            repository="repository_value",
            source_provider="source_provider_value",
            deployment_level=telcoautomation.DeploymentLevel.HYDRATION,
            rollback_support=True,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.Blueprint.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_blueprint(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.Blueprint)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.source_blueprint == "source_blueprint_value"
    assert response.approval_state == telcoautomation.Blueprint.ApprovalState.DRAFT
    assert response.display_name == "display_name_value"
    assert response.repository == "repository_value"
    assert response.source_provider == "source_provider_value"
    assert response.deployment_level == telcoautomation.DeploymentLevel.HYDRATION
    assert response.rollback_support is True


def test_update_blueprint_rest_required_fields(
    request_type=telcoautomation.UpdateBlueprintRequest,
):
    transport_class = transports.TelcoAutomationRestTransport

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
    ).update_blueprint._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_blueprint._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = telcoautomation.Blueprint()
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

            # Convert return value to protobuf type
            return_value = telcoautomation.Blueprint.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_blueprint(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_blueprint_rest_unset_required_fields():
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_blueprint._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("updateMask",))
        & set(
            (
                "blueprint",
                "updateMask",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_blueprint_rest_interceptors(null_interceptor):
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TelcoAutomationRestInterceptor(),
    )
    client = TelcoAutomationClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "post_update_blueprint"
    ) as post, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "pre_update_blueprint"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = telcoautomation.UpdateBlueprintRequest.pb(
            telcoautomation.UpdateBlueprintRequest()
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
        req.return_value._content = telcoautomation.Blueprint.to_json(
            telcoautomation.Blueprint()
        )

        request = telcoautomation.UpdateBlueprintRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = telcoautomation.Blueprint()

        client.update_blueprint(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_blueprint_rest_bad_request(
    transport: str = "rest", request_type=telcoautomation.UpdateBlueprintRequest
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "blueprint": {
            "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/blueprints/sample4"
        }
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
        client.update_blueprint(request)


def test_update_blueprint_rest_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.Blueprint()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "blueprint": {
                "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/blueprints/sample4"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            blueprint=telcoautomation.Blueprint(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.Blueprint.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_blueprint(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{blueprint.name=projects/*/locations/*/orchestrationClusters/*/blueprints/*}"
            % client.transport._host,
            args[1],
        )


def test_update_blueprint_rest_flattened_error(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_blueprint(
            telcoautomation.UpdateBlueprintRequest(),
            blueprint=telcoautomation.Blueprint(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_blueprint_rest_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.GetBlueprintRequest,
        dict,
    ],
)
def test_get_blueprint_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/blueprints/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.Blueprint(
            name="name_value",
            revision_id="revision_id_value",
            source_blueprint="source_blueprint_value",
            approval_state=telcoautomation.Blueprint.ApprovalState.DRAFT,
            display_name="display_name_value",
            repository="repository_value",
            source_provider="source_provider_value",
            deployment_level=telcoautomation.DeploymentLevel.HYDRATION,
            rollback_support=True,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.Blueprint.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_blueprint(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.Blueprint)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.source_blueprint == "source_blueprint_value"
    assert response.approval_state == telcoautomation.Blueprint.ApprovalState.DRAFT
    assert response.display_name == "display_name_value"
    assert response.repository == "repository_value"
    assert response.source_provider == "source_provider_value"
    assert response.deployment_level == telcoautomation.DeploymentLevel.HYDRATION
    assert response.rollback_support is True


def test_get_blueprint_rest_required_fields(
    request_type=telcoautomation.GetBlueprintRequest,
):
    transport_class = transports.TelcoAutomationRestTransport

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
    ).get_blueprint._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_blueprint._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("view",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = telcoautomation.Blueprint()
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

            # Convert return value to protobuf type
            return_value = telcoautomation.Blueprint.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_blueprint(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_blueprint_rest_unset_required_fields():
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_blueprint._get_unset_required_fields({})
    assert set(unset_fields) == (set(("view",)) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_blueprint_rest_interceptors(null_interceptor):
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TelcoAutomationRestInterceptor(),
    )
    client = TelcoAutomationClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "post_get_blueprint"
    ) as post, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "pre_get_blueprint"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = telcoautomation.GetBlueprintRequest.pb(
            telcoautomation.GetBlueprintRequest()
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
        req.return_value._content = telcoautomation.Blueprint.to_json(
            telcoautomation.Blueprint()
        )

        request = telcoautomation.GetBlueprintRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = telcoautomation.Blueprint()

        client.get_blueprint(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_blueprint_rest_bad_request(
    transport: str = "rest", request_type=telcoautomation.GetBlueprintRequest
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/blueprints/sample4"
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
        client.get_blueprint(request)


def test_get_blueprint_rest_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.Blueprint()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/blueprints/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.Blueprint.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_blueprint(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/orchestrationClusters/*/blueprints/*}"
            % client.transport._host,
            args[1],
        )


def test_get_blueprint_rest_flattened_error(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_blueprint(
            telcoautomation.GetBlueprintRequest(),
            name="name_value",
        )


def test_get_blueprint_rest_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.DeleteBlueprintRequest,
        dict,
    ],
)
def test_delete_blueprint_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/blueprints/sample4"
    }
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
        response = client.delete_blueprint(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_blueprint_rest_required_fields(
    request_type=telcoautomation.DeleteBlueprintRequest,
):
    transport_class = transports.TelcoAutomationRestTransport

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
    ).delete_blueprint._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_blueprint._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = TelcoAutomationClient(
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

            response = client.delete_blueprint(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_blueprint_rest_unset_required_fields():
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_blueprint._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_blueprint_rest_interceptors(null_interceptor):
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TelcoAutomationRestInterceptor(),
    )
    client = TelcoAutomationClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "pre_delete_blueprint"
    ) as pre:
        pre.assert_not_called()
        pb_message = telcoautomation.DeleteBlueprintRequest.pb(
            telcoautomation.DeleteBlueprintRequest()
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

        request = telcoautomation.DeleteBlueprintRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_blueprint(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_delete_blueprint_rest_bad_request(
    transport: str = "rest", request_type=telcoautomation.DeleteBlueprintRequest
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/blueprints/sample4"
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
        client.delete_blueprint(request)


def test_delete_blueprint_rest_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/blueprints/sample4"
        }

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

        client.delete_blueprint(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/orchestrationClusters/*/blueprints/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_blueprint_rest_flattened_error(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_blueprint(
            telcoautomation.DeleteBlueprintRequest(),
            name="name_value",
        )


def test_delete_blueprint_rest_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.ListBlueprintsRequest,
        dict,
    ],
)
def test_list_blueprints_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/orchestrationClusters/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.ListBlueprintsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.ListBlueprintsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_blueprints(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBlueprintsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_blueprints_rest_required_fields(
    request_type=telcoautomation.ListBlueprintsRequest,
):
    transport_class = transports.TelcoAutomationRestTransport

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
    ).list_blueprints._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_blueprints._get_unset_required_fields(jsonified_request)
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

    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = telcoautomation.ListBlueprintsResponse()
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

            # Convert return value to protobuf type
            return_value = telcoautomation.ListBlueprintsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_blueprints(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_blueprints_rest_unset_required_fields():
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_blueprints._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_blueprints_rest_interceptors(null_interceptor):
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TelcoAutomationRestInterceptor(),
    )
    client = TelcoAutomationClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "post_list_blueprints"
    ) as post, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "pre_list_blueprints"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = telcoautomation.ListBlueprintsRequest.pb(
            telcoautomation.ListBlueprintsRequest()
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
        req.return_value._content = telcoautomation.ListBlueprintsResponse.to_json(
            telcoautomation.ListBlueprintsResponse()
        )

        request = telcoautomation.ListBlueprintsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = telcoautomation.ListBlueprintsResponse()

        client.list_blueprints(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_blueprints_rest_bad_request(
    transport: str = "rest", request_type=telcoautomation.ListBlueprintsRequest
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/orchestrationClusters/sample3"
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
        client.list_blueprints(request)


def test_list_blueprints_rest_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.ListBlueprintsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/orchestrationClusters/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.ListBlueprintsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_blueprints(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/orchestrationClusters/*}/blueprints"
            % client.transport._host,
            args[1],
        )


def test_list_blueprints_rest_flattened_error(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_blueprints(
            telcoautomation.ListBlueprintsRequest(),
            parent="parent_value",
        )


def test_list_blueprints_rest_pager(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            telcoautomation.ListBlueprintsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListBlueprintsResponse(
                blueprints=[],
                next_page_token="def",
            ),
            telcoautomation.ListBlueprintsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListBlueprintsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            telcoautomation.ListBlueprintsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/orchestrationClusters/sample3"
        }

        pager = client.list_blueprints(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, telcoautomation.Blueprint) for i in results)

        pages = list(client.list_blueprints(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.ApproveBlueprintRequest,
        dict,
    ],
)
def test_approve_blueprint_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/blueprints/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.Blueprint(
            name="name_value",
            revision_id="revision_id_value",
            source_blueprint="source_blueprint_value",
            approval_state=telcoautomation.Blueprint.ApprovalState.DRAFT,
            display_name="display_name_value",
            repository="repository_value",
            source_provider="source_provider_value",
            deployment_level=telcoautomation.DeploymentLevel.HYDRATION,
            rollback_support=True,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.Blueprint.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.approve_blueprint(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.Blueprint)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.source_blueprint == "source_blueprint_value"
    assert response.approval_state == telcoautomation.Blueprint.ApprovalState.DRAFT
    assert response.display_name == "display_name_value"
    assert response.repository == "repository_value"
    assert response.source_provider == "source_provider_value"
    assert response.deployment_level == telcoautomation.DeploymentLevel.HYDRATION
    assert response.rollback_support is True


def test_approve_blueprint_rest_required_fields(
    request_type=telcoautomation.ApproveBlueprintRequest,
):
    transport_class = transports.TelcoAutomationRestTransport

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
    ).approve_blueprint._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).approve_blueprint._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = telcoautomation.Blueprint()
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

            # Convert return value to protobuf type
            return_value = telcoautomation.Blueprint.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.approve_blueprint(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_approve_blueprint_rest_unset_required_fields():
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.approve_blueprint._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_approve_blueprint_rest_interceptors(null_interceptor):
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TelcoAutomationRestInterceptor(),
    )
    client = TelcoAutomationClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "post_approve_blueprint"
    ) as post, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "pre_approve_blueprint"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = telcoautomation.ApproveBlueprintRequest.pb(
            telcoautomation.ApproveBlueprintRequest()
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
        req.return_value._content = telcoautomation.Blueprint.to_json(
            telcoautomation.Blueprint()
        )

        request = telcoautomation.ApproveBlueprintRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = telcoautomation.Blueprint()

        client.approve_blueprint(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_approve_blueprint_rest_bad_request(
    transport: str = "rest", request_type=telcoautomation.ApproveBlueprintRequest
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/blueprints/sample4"
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
        client.approve_blueprint(request)


def test_approve_blueprint_rest_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.Blueprint()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/blueprints/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.Blueprint.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.approve_blueprint(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/orchestrationClusters/*/blueprints/*}:approve"
            % client.transport._host,
            args[1],
        )


def test_approve_blueprint_rest_flattened_error(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.approve_blueprint(
            telcoautomation.ApproveBlueprintRequest(),
            name="name_value",
        )


def test_approve_blueprint_rest_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.ProposeBlueprintRequest,
        dict,
    ],
)
def test_propose_blueprint_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/blueprints/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.Blueprint(
            name="name_value",
            revision_id="revision_id_value",
            source_blueprint="source_blueprint_value",
            approval_state=telcoautomation.Blueprint.ApprovalState.DRAFT,
            display_name="display_name_value",
            repository="repository_value",
            source_provider="source_provider_value",
            deployment_level=telcoautomation.DeploymentLevel.HYDRATION,
            rollback_support=True,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.Blueprint.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.propose_blueprint(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.Blueprint)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.source_blueprint == "source_blueprint_value"
    assert response.approval_state == telcoautomation.Blueprint.ApprovalState.DRAFT
    assert response.display_name == "display_name_value"
    assert response.repository == "repository_value"
    assert response.source_provider == "source_provider_value"
    assert response.deployment_level == telcoautomation.DeploymentLevel.HYDRATION
    assert response.rollback_support is True


def test_propose_blueprint_rest_required_fields(
    request_type=telcoautomation.ProposeBlueprintRequest,
):
    transport_class = transports.TelcoAutomationRestTransport

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
    ).propose_blueprint._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).propose_blueprint._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = telcoautomation.Blueprint()
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

            # Convert return value to protobuf type
            return_value = telcoautomation.Blueprint.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.propose_blueprint(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_propose_blueprint_rest_unset_required_fields():
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.propose_blueprint._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_propose_blueprint_rest_interceptors(null_interceptor):
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TelcoAutomationRestInterceptor(),
    )
    client = TelcoAutomationClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "post_propose_blueprint"
    ) as post, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "pre_propose_blueprint"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = telcoautomation.ProposeBlueprintRequest.pb(
            telcoautomation.ProposeBlueprintRequest()
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
        req.return_value._content = telcoautomation.Blueprint.to_json(
            telcoautomation.Blueprint()
        )

        request = telcoautomation.ProposeBlueprintRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = telcoautomation.Blueprint()

        client.propose_blueprint(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_propose_blueprint_rest_bad_request(
    transport: str = "rest", request_type=telcoautomation.ProposeBlueprintRequest
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/blueprints/sample4"
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
        client.propose_blueprint(request)


def test_propose_blueprint_rest_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.Blueprint()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/blueprints/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.Blueprint.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.propose_blueprint(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/orchestrationClusters/*/blueprints/*}:propose"
            % client.transport._host,
            args[1],
        )


def test_propose_blueprint_rest_flattened_error(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.propose_blueprint(
            telcoautomation.ProposeBlueprintRequest(),
            name="name_value",
        )


def test_propose_blueprint_rest_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.RejectBlueprintRequest,
        dict,
    ],
)
def test_reject_blueprint_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/blueprints/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.Blueprint(
            name="name_value",
            revision_id="revision_id_value",
            source_blueprint="source_blueprint_value",
            approval_state=telcoautomation.Blueprint.ApprovalState.DRAFT,
            display_name="display_name_value",
            repository="repository_value",
            source_provider="source_provider_value",
            deployment_level=telcoautomation.DeploymentLevel.HYDRATION,
            rollback_support=True,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.Blueprint.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.reject_blueprint(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.Blueprint)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.source_blueprint == "source_blueprint_value"
    assert response.approval_state == telcoautomation.Blueprint.ApprovalState.DRAFT
    assert response.display_name == "display_name_value"
    assert response.repository == "repository_value"
    assert response.source_provider == "source_provider_value"
    assert response.deployment_level == telcoautomation.DeploymentLevel.HYDRATION
    assert response.rollback_support is True


def test_reject_blueprint_rest_required_fields(
    request_type=telcoautomation.RejectBlueprintRequest,
):
    transport_class = transports.TelcoAutomationRestTransport

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
    ).reject_blueprint._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).reject_blueprint._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = telcoautomation.Blueprint()
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

            # Convert return value to protobuf type
            return_value = telcoautomation.Blueprint.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.reject_blueprint(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_reject_blueprint_rest_unset_required_fields():
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.reject_blueprint._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_reject_blueprint_rest_interceptors(null_interceptor):
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TelcoAutomationRestInterceptor(),
    )
    client = TelcoAutomationClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "post_reject_blueprint"
    ) as post, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "pre_reject_blueprint"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = telcoautomation.RejectBlueprintRequest.pb(
            telcoautomation.RejectBlueprintRequest()
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
        req.return_value._content = telcoautomation.Blueprint.to_json(
            telcoautomation.Blueprint()
        )

        request = telcoautomation.RejectBlueprintRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = telcoautomation.Blueprint()

        client.reject_blueprint(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_reject_blueprint_rest_bad_request(
    transport: str = "rest", request_type=telcoautomation.RejectBlueprintRequest
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/blueprints/sample4"
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
        client.reject_blueprint(request)


def test_reject_blueprint_rest_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.Blueprint()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/blueprints/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.Blueprint.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.reject_blueprint(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/orchestrationClusters/*/blueprints/*}:reject"
            % client.transport._host,
            args[1],
        )


def test_reject_blueprint_rest_flattened_error(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.reject_blueprint(
            telcoautomation.RejectBlueprintRequest(),
            name="name_value",
        )


def test_reject_blueprint_rest_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.ListBlueprintRevisionsRequest,
        dict,
    ],
)
def test_list_blueprint_revisions_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/blueprints/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.ListBlueprintRevisionsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.ListBlueprintRevisionsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_blueprint_revisions(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBlueprintRevisionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_blueprint_revisions_rest_required_fields(
    request_type=telcoautomation.ListBlueprintRevisionsRequest,
):
    transport_class = transports.TelcoAutomationRestTransport

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
    ).list_blueprint_revisions._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_blueprint_revisions._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = telcoautomation.ListBlueprintRevisionsResponse()
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

            # Convert return value to protobuf type
            return_value = telcoautomation.ListBlueprintRevisionsResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_blueprint_revisions(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_blueprint_revisions_rest_unset_required_fields():
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_blueprint_revisions._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("name",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_blueprint_revisions_rest_interceptors(null_interceptor):
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TelcoAutomationRestInterceptor(),
    )
    client = TelcoAutomationClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "post_list_blueprint_revisions"
    ) as post, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "pre_list_blueprint_revisions"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = telcoautomation.ListBlueprintRevisionsRequest.pb(
            telcoautomation.ListBlueprintRevisionsRequest()
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
            telcoautomation.ListBlueprintRevisionsResponse.to_json(
                telcoautomation.ListBlueprintRevisionsResponse()
            )
        )

        request = telcoautomation.ListBlueprintRevisionsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = telcoautomation.ListBlueprintRevisionsResponse()

        client.list_blueprint_revisions(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_blueprint_revisions_rest_bad_request(
    transport: str = "rest", request_type=telcoautomation.ListBlueprintRevisionsRequest
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/blueprints/sample4"
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
        client.list_blueprint_revisions(request)


def test_list_blueprint_revisions_rest_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.ListBlueprintRevisionsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/blueprints/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.ListBlueprintRevisionsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_blueprint_revisions(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/orchestrationClusters/*/blueprints/*}:listRevisions"
            % client.transport._host,
            args[1],
        )


def test_list_blueprint_revisions_rest_flattened_error(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_blueprint_revisions(
            telcoautomation.ListBlueprintRevisionsRequest(),
            name="name_value",
        )


def test_list_blueprint_revisions_rest_pager(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            telcoautomation.ListBlueprintRevisionsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListBlueprintRevisionsResponse(
                blueprints=[],
                next_page_token="def",
            ),
            telcoautomation.ListBlueprintRevisionsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListBlueprintRevisionsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            telcoautomation.ListBlueprintRevisionsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/blueprints/sample4"
        }

        pager = client.list_blueprint_revisions(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, telcoautomation.Blueprint) for i in results)

        pages = list(client.list_blueprint_revisions(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.SearchBlueprintRevisionsRequest,
        dict,
    ],
)
def test_search_blueprint_revisions_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/orchestrationClusters/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.SearchBlueprintRevisionsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.SearchBlueprintRevisionsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.search_blueprint_revisions(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchBlueprintRevisionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_search_blueprint_revisions_rest_required_fields(
    request_type=telcoautomation.SearchBlueprintRevisionsRequest,
):
    transport_class = transports.TelcoAutomationRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["query"] = ""
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
    assert "query" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).search_blueprint_revisions._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "query" in jsonified_request
    assert jsonified_request["query"] == request_init["query"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["query"] = "query_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).search_blueprint_revisions._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
            "query",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "query" in jsonified_request
    assert jsonified_request["query"] == "query_value"

    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = telcoautomation.SearchBlueprintRevisionsResponse()
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

            # Convert return value to protobuf type
            return_value = telcoautomation.SearchBlueprintRevisionsResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.search_blueprint_revisions(request)

            expected_params = [
                (
                    "query",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_search_blueprint_revisions_rest_unset_required_fields():
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.search_blueprint_revisions._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
                "query",
            )
        )
        & set(
            (
                "parent",
                "query",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_search_blueprint_revisions_rest_interceptors(null_interceptor):
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TelcoAutomationRestInterceptor(),
    )
    client = TelcoAutomationClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "post_search_blueprint_revisions"
    ) as post, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "pre_search_blueprint_revisions"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = telcoautomation.SearchBlueprintRevisionsRequest.pb(
            telcoautomation.SearchBlueprintRevisionsRequest()
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
            telcoautomation.SearchBlueprintRevisionsResponse.to_json(
                telcoautomation.SearchBlueprintRevisionsResponse()
            )
        )

        request = telcoautomation.SearchBlueprintRevisionsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = telcoautomation.SearchBlueprintRevisionsResponse()

        client.search_blueprint_revisions(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_search_blueprint_revisions_rest_bad_request(
    transport: str = "rest",
    request_type=telcoautomation.SearchBlueprintRevisionsRequest,
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/orchestrationClusters/sample3"
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
        client.search_blueprint_revisions(request)


def test_search_blueprint_revisions_rest_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.SearchBlueprintRevisionsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/orchestrationClusters/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            query="query_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.SearchBlueprintRevisionsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.search_blueprint_revisions(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/orchestrationClusters/*}/blueprints:searchRevisions"
            % client.transport._host,
            args[1],
        )


def test_search_blueprint_revisions_rest_flattened_error(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.search_blueprint_revisions(
            telcoautomation.SearchBlueprintRevisionsRequest(),
            parent="parent_value",
            query="query_value",
        )


def test_search_blueprint_revisions_rest_pager(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            telcoautomation.SearchBlueprintRevisionsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.SearchBlueprintRevisionsResponse(
                blueprints=[],
                next_page_token="def",
            ),
            telcoautomation.SearchBlueprintRevisionsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.SearchBlueprintRevisionsResponse(
                blueprints=[
                    telcoautomation.Blueprint(),
                    telcoautomation.Blueprint(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            telcoautomation.SearchBlueprintRevisionsResponse.to_json(x)
            for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/orchestrationClusters/sample3"
        }

        pager = client.search_blueprint_revisions(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, telcoautomation.Blueprint) for i in results)

        pages = list(client.search_blueprint_revisions(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.SearchDeploymentRevisionsRequest,
        dict,
    ],
)
def test_search_deployment_revisions_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/orchestrationClusters/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.SearchDeploymentRevisionsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.SearchDeploymentRevisionsResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.search_deployment_revisions(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchDeploymentRevisionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_search_deployment_revisions_rest_required_fields(
    request_type=telcoautomation.SearchDeploymentRevisionsRequest,
):
    transport_class = transports.TelcoAutomationRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["query"] = ""
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
    assert "query" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).search_deployment_revisions._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "query" in jsonified_request
    assert jsonified_request["query"] == request_init["query"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["query"] = "query_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).search_deployment_revisions._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
            "query",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "query" in jsonified_request
    assert jsonified_request["query"] == "query_value"

    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = telcoautomation.SearchDeploymentRevisionsResponse()
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

            # Convert return value to protobuf type
            return_value = telcoautomation.SearchDeploymentRevisionsResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.search_deployment_revisions(request)

            expected_params = [
                (
                    "query",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_search_deployment_revisions_rest_unset_required_fields():
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.search_deployment_revisions._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
                "query",
            )
        )
        & set(
            (
                "parent",
                "query",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_search_deployment_revisions_rest_interceptors(null_interceptor):
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TelcoAutomationRestInterceptor(),
    )
    client = TelcoAutomationClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "post_search_deployment_revisions"
    ) as post, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "pre_search_deployment_revisions"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = telcoautomation.SearchDeploymentRevisionsRequest.pb(
            telcoautomation.SearchDeploymentRevisionsRequest()
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
            telcoautomation.SearchDeploymentRevisionsResponse.to_json(
                telcoautomation.SearchDeploymentRevisionsResponse()
            )
        )

        request = telcoautomation.SearchDeploymentRevisionsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = telcoautomation.SearchDeploymentRevisionsResponse()

        client.search_deployment_revisions(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_search_deployment_revisions_rest_bad_request(
    transport: str = "rest",
    request_type=telcoautomation.SearchDeploymentRevisionsRequest,
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/orchestrationClusters/sample3"
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
        client.search_deployment_revisions(request)


def test_search_deployment_revisions_rest_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.SearchDeploymentRevisionsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/orchestrationClusters/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            query="query_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.SearchDeploymentRevisionsResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.search_deployment_revisions(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/orchestrationClusters/*}/deployments:searchRevisions"
            % client.transport._host,
            args[1],
        )


def test_search_deployment_revisions_rest_flattened_error(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.search_deployment_revisions(
            telcoautomation.SearchDeploymentRevisionsRequest(),
            parent="parent_value",
            query="query_value",
        )


def test_search_deployment_revisions_rest_pager(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            telcoautomation.SearchDeploymentRevisionsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.SearchDeploymentRevisionsResponse(
                deployments=[],
                next_page_token="def",
            ),
            telcoautomation.SearchDeploymentRevisionsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.SearchDeploymentRevisionsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            telcoautomation.SearchDeploymentRevisionsResponse.to_json(x)
            for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/orchestrationClusters/sample3"
        }

        pager = client.search_deployment_revisions(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, telcoautomation.Deployment) for i in results)

        pages = list(client.search_deployment_revisions(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.DiscardBlueprintChangesRequest,
        dict,
    ],
)
def test_discard_blueprint_changes_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/blueprints/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.DiscardBlueprintChangesResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.DiscardBlueprintChangesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.discard_blueprint_changes(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.DiscardBlueprintChangesResponse)


def test_discard_blueprint_changes_rest_required_fields(
    request_type=telcoautomation.DiscardBlueprintChangesRequest,
):
    transport_class = transports.TelcoAutomationRestTransport

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
    ).discard_blueprint_changes._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).discard_blueprint_changes._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = telcoautomation.DiscardBlueprintChangesResponse()
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

            # Convert return value to protobuf type
            return_value = telcoautomation.DiscardBlueprintChangesResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.discard_blueprint_changes(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_discard_blueprint_changes_rest_unset_required_fields():
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.discard_blueprint_changes._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_discard_blueprint_changes_rest_interceptors(null_interceptor):
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TelcoAutomationRestInterceptor(),
    )
    client = TelcoAutomationClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "post_discard_blueprint_changes"
    ) as post, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "pre_discard_blueprint_changes"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = telcoautomation.DiscardBlueprintChangesRequest.pb(
            telcoautomation.DiscardBlueprintChangesRequest()
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
            telcoautomation.DiscardBlueprintChangesResponse.to_json(
                telcoautomation.DiscardBlueprintChangesResponse()
            )
        )

        request = telcoautomation.DiscardBlueprintChangesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = telcoautomation.DiscardBlueprintChangesResponse()

        client.discard_blueprint_changes(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_discard_blueprint_changes_rest_bad_request(
    transport: str = "rest", request_type=telcoautomation.DiscardBlueprintChangesRequest
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/blueprints/sample4"
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
        client.discard_blueprint_changes(request)


def test_discard_blueprint_changes_rest_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.DiscardBlueprintChangesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/blueprints/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.DiscardBlueprintChangesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.discard_blueprint_changes(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/orchestrationClusters/*/blueprints/*}:discard"
            % client.transport._host,
            args[1],
        )


def test_discard_blueprint_changes_rest_flattened_error(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.discard_blueprint_changes(
            telcoautomation.DiscardBlueprintChangesRequest(),
            name="name_value",
        )


def test_discard_blueprint_changes_rest_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.ListPublicBlueprintsRequest,
        dict,
    ],
)
def test_list_public_blueprints_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.ListPublicBlueprintsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.ListPublicBlueprintsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_public_blueprints(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPublicBlueprintsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_public_blueprints_rest_required_fields(
    request_type=telcoautomation.ListPublicBlueprintsRequest,
):
    transport_class = transports.TelcoAutomationRestTransport

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
    ).list_public_blueprints._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_public_blueprints._get_unset_required_fields(jsonified_request)
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

    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = telcoautomation.ListPublicBlueprintsResponse()
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

            # Convert return value to protobuf type
            return_value = telcoautomation.ListPublicBlueprintsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_public_blueprints(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_public_blueprints_rest_unset_required_fields():
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_public_blueprints._get_unset_required_fields({})
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
def test_list_public_blueprints_rest_interceptors(null_interceptor):
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TelcoAutomationRestInterceptor(),
    )
    client = TelcoAutomationClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "post_list_public_blueprints"
    ) as post, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "pre_list_public_blueprints"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = telcoautomation.ListPublicBlueprintsRequest.pb(
            telcoautomation.ListPublicBlueprintsRequest()
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
            telcoautomation.ListPublicBlueprintsResponse.to_json(
                telcoautomation.ListPublicBlueprintsResponse()
            )
        )

        request = telcoautomation.ListPublicBlueprintsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = telcoautomation.ListPublicBlueprintsResponse()

        client.list_public_blueprints(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_public_blueprints_rest_bad_request(
    transport: str = "rest", request_type=telcoautomation.ListPublicBlueprintsRequest
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
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
        client.list_public_blueprints(request)


def test_list_public_blueprints_rest_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.ListPublicBlueprintsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.ListPublicBlueprintsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_public_blueprints(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/publicBlueprints"
            % client.transport._host,
            args[1],
        )


def test_list_public_blueprints_rest_flattened_error(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_public_blueprints(
            telcoautomation.ListPublicBlueprintsRequest(),
            parent="parent_value",
        )


def test_list_public_blueprints_rest_pager(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            telcoautomation.ListPublicBlueprintsResponse(
                public_blueprints=[
                    telcoautomation.PublicBlueprint(),
                    telcoautomation.PublicBlueprint(),
                    telcoautomation.PublicBlueprint(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListPublicBlueprintsResponse(
                public_blueprints=[],
                next_page_token="def",
            ),
            telcoautomation.ListPublicBlueprintsResponse(
                public_blueprints=[
                    telcoautomation.PublicBlueprint(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListPublicBlueprintsResponse(
                public_blueprints=[
                    telcoautomation.PublicBlueprint(),
                    telcoautomation.PublicBlueprint(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            telcoautomation.ListPublicBlueprintsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_public_blueprints(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, telcoautomation.PublicBlueprint) for i in results)

        pages = list(client.list_public_blueprints(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.GetPublicBlueprintRequest,
        dict,
    ],
)
def test_get_public_blueprint_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/publicBlueprints/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.PublicBlueprint(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            deployment_level=telcoautomation.DeploymentLevel.HYDRATION,
            source_provider="source_provider_value",
            rollback_support=True,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.PublicBlueprint.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_public_blueprint(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.PublicBlueprint)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.deployment_level == telcoautomation.DeploymentLevel.HYDRATION
    assert response.source_provider == "source_provider_value"
    assert response.rollback_support is True


def test_get_public_blueprint_rest_required_fields(
    request_type=telcoautomation.GetPublicBlueprintRequest,
):
    transport_class = transports.TelcoAutomationRestTransport

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
    ).get_public_blueprint._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_public_blueprint._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = telcoautomation.PublicBlueprint()
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

            # Convert return value to protobuf type
            return_value = telcoautomation.PublicBlueprint.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_public_blueprint(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_public_blueprint_rest_unset_required_fields():
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_public_blueprint._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_public_blueprint_rest_interceptors(null_interceptor):
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TelcoAutomationRestInterceptor(),
    )
    client = TelcoAutomationClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "post_get_public_blueprint"
    ) as post, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "pre_get_public_blueprint"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = telcoautomation.GetPublicBlueprintRequest.pb(
            telcoautomation.GetPublicBlueprintRequest()
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
        req.return_value._content = telcoautomation.PublicBlueprint.to_json(
            telcoautomation.PublicBlueprint()
        )

        request = telcoautomation.GetPublicBlueprintRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = telcoautomation.PublicBlueprint()

        client.get_public_blueprint(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_public_blueprint_rest_bad_request(
    transport: str = "rest", request_type=telcoautomation.GetPublicBlueprintRequest
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/publicBlueprints/sample3"
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
        client.get_public_blueprint(request)


def test_get_public_blueprint_rest_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.PublicBlueprint()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/publicBlueprints/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.PublicBlueprint.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_public_blueprint(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/publicBlueprints/*}"
            % client.transport._host,
            args[1],
        )


def test_get_public_blueprint_rest_flattened_error(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_public_blueprint(
            telcoautomation.GetPublicBlueprintRequest(),
            name="name_value",
        )


def test_get_public_blueprint_rest_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.CreateDeploymentRequest,
        dict,
    ],
)
def test_create_deployment_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/orchestrationClusters/sample3"
    }
    request_init["deployment"] = {
        "name": "name_value",
        "revision_id": "revision_id_value",
        "source_blueprint_revision": "source_blueprint_revision_value",
        "revision_create_time": {"seconds": 751, "nanos": 543},
        "state": 1,
        "display_name": "display_name_value",
        "repository": "repository_value",
        "files": [
            {
                "path": "path_value",
                "content": "content_value",
                "deleted": True,
                "editable": True,
            }
        ],
        "labels": {},
        "create_time": {},
        "update_time": {},
        "source_provider": "source_provider_value",
        "workload_cluster": "workload_cluster_value",
        "deployment_level": 1,
        "rollback_support": True,
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = telcoautomation.CreateDeploymentRequest.meta.fields["deployment"]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["deployment"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["deployment"][field])):
                    del request_init["deployment"][field][i][subfield]
            else:
                del request_init["deployment"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.Deployment(
            name="name_value",
            revision_id="revision_id_value",
            source_blueprint_revision="source_blueprint_revision_value",
            state=telcoautomation.Deployment.State.DRAFT,
            display_name="display_name_value",
            repository="repository_value",
            source_provider="source_provider_value",
            workload_cluster="workload_cluster_value",
            deployment_level=telcoautomation.DeploymentLevel.HYDRATION,
            rollback_support=True,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.Deployment.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_deployment(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.Deployment)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.source_blueprint_revision == "source_blueprint_revision_value"
    assert response.state == telcoautomation.Deployment.State.DRAFT
    assert response.display_name == "display_name_value"
    assert response.repository == "repository_value"
    assert response.source_provider == "source_provider_value"
    assert response.workload_cluster == "workload_cluster_value"
    assert response.deployment_level == telcoautomation.DeploymentLevel.HYDRATION
    assert response.rollback_support is True


def test_create_deployment_rest_required_fields(
    request_type=telcoautomation.CreateDeploymentRequest,
):
    transport_class = transports.TelcoAutomationRestTransport

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
    ).create_deployment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_deployment._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("deployment_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = telcoautomation.Deployment()
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

            # Convert return value to protobuf type
            return_value = telcoautomation.Deployment.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_deployment(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_deployment_rest_unset_required_fields():
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_deployment._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("deploymentId",))
        & set(
            (
                "parent",
                "deployment",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_deployment_rest_interceptors(null_interceptor):
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TelcoAutomationRestInterceptor(),
    )
    client = TelcoAutomationClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "post_create_deployment"
    ) as post, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "pre_create_deployment"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = telcoautomation.CreateDeploymentRequest.pb(
            telcoautomation.CreateDeploymentRequest()
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
        req.return_value._content = telcoautomation.Deployment.to_json(
            telcoautomation.Deployment()
        )

        request = telcoautomation.CreateDeploymentRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = telcoautomation.Deployment()

        client.create_deployment(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_deployment_rest_bad_request(
    transport: str = "rest", request_type=telcoautomation.CreateDeploymentRequest
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/orchestrationClusters/sample3"
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
        client.create_deployment(request)


def test_create_deployment_rest_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.Deployment()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/orchestrationClusters/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            deployment=telcoautomation.Deployment(name="name_value"),
            deployment_id="deployment_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.Deployment.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_deployment(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/orchestrationClusters/*}/deployments"
            % client.transport._host,
            args[1],
        )


def test_create_deployment_rest_flattened_error(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_deployment(
            telcoautomation.CreateDeploymentRequest(),
            parent="parent_value",
            deployment=telcoautomation.Deployment(name="name_value"),
            deployment_id="deployment_id_value",
        )


def test_create_deployment_rest_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.UpdateDeploymentRequest,
        dict,
    ],
)
def test_update_deployment_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "deployment": {
            "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4"
        }
    }
    request_init["deployment"] = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4",
        "revision_id": "revision_id_value",
        "source_blueprint_revision": "source_blueprint_revision_value",
        "revision_create_time": {"seconds": 751, "nanos": 543},
        "state": 1,
        "display_name": "display_name_value",
        "repository": "repository_value",
        "files": [
            {
                "path": "path_value",
                "content": "content_value",
                "deleted": True,
                "editable": True,
            }
        ],
        "labels": {},
        "create_time": {},
        "update_time": {},
        "source_provider": "source_provider_value",
        "workload_cluster": "workload_cluster_value",
        "deployment_level": 1,
        "rollback_support": True,
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = telcoautomation.UpdateDeploymentRequest.meta.fields["deployment"]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["deployment"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["deployment"][field])):
                    del request_init["deployment"][field][i][subfield]
            else:
                del request_init["deployment"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.Deployment(
            name="name_value",
            revision_id="revision_id_value",
            source_blueprint_revision="source_blueprint_revision_value",
            state=telcoautomation.Deployment.State.DRAFT,
            display_name="display_name_value",
            repository="repository_value",
            source_provider="source_provider_value",
            workload_cluster="workload_cluster_value",
            deployment_level=telcoautomation.DeploymentLevel.HYDRATION,
            rollback_support=True,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.Deployment.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_deployment(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.Deployment)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.source_blueprint_revision == "source_blueprint_revision_value"
    assert response.state == telcoautomation.Deployment.State.DRAFT
    assert response.display_name == "display_name_value"
    assert response.repository == "repository_value"
    assert response.source_provider == "source_provider_value"
    assert response.workload_cluster == "workload_cluster_value"
    assert response.deployment_level == telcoautomation.DeploymentLevel.HYDRATION
    assert response.rollback_support is True


def test_update_deployment_rest_required_fields(
    request_type=telcoautomation.UpdateDeploymentRequest,
):
    transport_class = transports.TelcoAutomationRestTransport

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
    ).update_deployment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_deployment._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = telcoautomation.Deployment()
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

            # Convert return value to protobuf type
            return_value = telcoautomation.Deployment.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_deployment(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_deployment_rest_unset_required_fields():
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_deployment._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("updateMask",))
        & set(
            (
                "deployment",
                "updateMask",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_deployment_rest_interceptors(null_interceptor):
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TelcoAutomationRestInterceptor(),
    )
    client = TelcoAutomationClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "post_update_deployment"
    ) as post, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "pre_update_deployment"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = telcoautomation.UpdateDeploymentRequest.pb(
            telcoautomation.UpdateDeploymentRequest()
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
        req.return_value._content = telcoautomation.Deployment.to_json(
            telcoautomation.Deployment()
        )

        request = telcoautomation.UpdateDeploymentRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = telcoautomation.Deployment()

        client.update_deployment(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_deployment_rest_bad_request(
    transport: str = "rest", request_type=telcoautomation.UpdateDeploymentRequest
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "deployment": {
            "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4"
        }
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
        client.update_deployment(request)


def test_update_deployment_rest_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.Deployment()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "deployment": {
                "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            deployment=telcoautomation.Deployment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.Deployment.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_deployment(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{deployment.name=projects/*/locations/*/orchestrationClusters/*/deployments/*}"
            % client.transport._host,
            args[1],
        )


def test_update_deployment_rest_flattened_error(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_deployment(
            telcoautomation.UpdateDeploymentRequest(),
            deployment=telcoautomation.Deployment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_deployment_rest_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.GetDeploymentRequest,
        dict,
    ],
)
def test_get_deployment_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.Deployment(
            name="name_value",
            revision_id="revision_id_value",
            source_blueprint_revision="source_blueprint_revision_value",
            state=telcoautomation.Deployment.State.DRAFT,
            display_name="display_name_value",
            repository="repository_value",
            source_provider="source_provider_value",
            workload_cluster="workload_cluster_value",
            deployment_level=telcoautomation.DeploymentLevel.HYDRATION,
            rollback_support=True,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.Deployment.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_deployment(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.Deployment)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.source_blueprint_revision == "source_blueprint_revision_value"
    assert response.state == telcoautomation.Deployment.State.DRAFT
    assert response.display_name == "display_name_value"
    assert response.repository == "repository_value"
    assert response.source_provider == "source_provider_value"
    assert response.workload_cluster == "workload_cluster_value"
    assert response.deployment_level == telcoautomation.DeploymentLevel.HYDRATION
    assert response.rollback_support is True


def test_get_deployment_rest_required_fields(
    request_type=telcoautomation.GetDeploymentRequest,
):
    transport_class = transports.TelcoAutomationRestTransport

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
    ).get_deployment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_deployment._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("view",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = telcoautomation.Deployment()
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

            # Convert return value to protobuf type
            return_value = telcoautomation.Deployment.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_deployment(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_deployment_rest_unset_required_fields():
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_deployment._get_unset_required_fields({})
    assert set(unset_fields) == (set(("view",)) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_deployment_rest_interceptors(null_interceptor):
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TelcoAutomationRestInterceptor(),
    )
    client = TelcoAutomationClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "post_get_deployment"
    ) as post, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "pre_get_deployment"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = telcoautomation.GetDeploymentRequest.pb(
            telcoautomation.GetDeploymentRequest()
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
        req.return_value._content = telcoautomation.Deployment.to_json(
            telcoautomation.Deployment()
        )

        request = telcoautomation.GetDeploymentRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = telcoautomation.Deployment()

        client.get_deployment(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_deployment_rest_bad_request(
    transport: str = "rest", request_type=telcoautomation.GetDeploymentRequest
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4"
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
        client.get_deployment(request)


def test_get_deployment_rest_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.Deployment()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.Deployment.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_deployment(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/orchestrationClusters/*/deployments/*}"
            % client.transport._host,
            args[1],
        )


def test_get_deployment_rest_flattened_error(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_deployment(
            telcoautomation.GetDeploymentRequest(),
            name="name_value",
        )


def test_get_deployment_rest_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.RemoveDeploymentRequest,
        dict,
    ],
)
def test_remove_deployment_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4"
    }
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
        response = client.remove_deployment(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_remove_deployment_rest_required_fields(
    request_type=telcoautomation.RemoveDeploymentRequest,
):
    transport_class = transports.TelcoAutomationRestTransport

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
    ).remove_deployment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).remove_deployment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = TelcoAutomationClient(
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
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = ""

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.remove_deployment(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_remove_deployment_rest_unset_required_fields():
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.remove_deployment._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_remove_deployment_rest_interceptors(null_interceptor):
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TelcoAutomationRestInterceptor(),
    )
    client = TelcoAutomationClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "pre_remove_deployment"
    ) as pre:
        pre.assert_not_called()
        pb_message = telcoautomation.RemoveDeploymentRequest.pb(
            telcoautomation.RemoveDeploymentRequest()
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

        request = telcoautomation.RemoveDeploymentRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.remove_deployment(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_remove_deployment_rest_bad_request(
    transport: str = "rest", request_type=telcoautomation.RemoveDeploymentRequest
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4"
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
        client.remove_deployment(request)


def test_remove_deployment_rest_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4"
        }

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

        client.remove_deployment(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/orchestrationClusters/*/deployments/*}:remove"
            % client.transport._host,
            args[1],
        )


def test_remove_deployment_rest_flattened_error(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.remove_deployment(
            telcoautomation.RemoveDeploymentRequest(),
            name="name_value",
        )


def test_remove_deployment_rest_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.ListDeploymentsRequest,
        dict,
    ],
)
def test_list_deployments_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/orchestrationClusters/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.ListDeploymentsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.ListDeploymentsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_deployments(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDeploymentsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_deployments_rest_required_fields(
    request_type=telcoautomation.ListDeploymentsRequest,
):
    transport_class = transports.TelcoAutomationRestTransport

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
    ).list_deployments._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_deployments._get_unset_required_fields(jsonified_request)
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

    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = telcoautomation.ListDeploymentsResponse()
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

            # Convert return value to protobuf type
            return_value = telcoautomation.ListDeploymentsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_deployments(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_deployments_rest_unset_required_fields():
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_deployments._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_deployments_rest_interceptors(null_interceptor):
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TelcoAutomationRestInterceptor(),
    )
    client = TelcoAutomationClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "post_list_deployments"
    ) as post, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "pre_list_deployments"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = telcoautomation.ListDeploymentsRequest.pb(
            telcoautomation.ListDeploymentsRequest()
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
        req.return_value._content = telcoautomation.ListDeploymentsResponse.to_json(
            telcoautomation.ListDeploymentsResponse()
        )

        request = telcoautomation.ListDeploymentsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = telcoautomation.ListDeploymentsResponse()

        client.list_deployments(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_deployments_rest_bad_request(
    transport: str = "rest", request_type=telcoautomation.ListDeploymentsRequest
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/orchestrationClusters/sample3"
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
        client.list_deployments(request)


def test_list_deployments_rest_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.ListDeploymentsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/orchestrationClusters/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.ListDeploymentsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_deployments(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/orchestrationClusters/*}/deployments"
            % client.transport._host,
            args[1],
        )


def test_list_deployments_rest_flattened_error(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_deployments(
            telcoautomation.ListDeploymentsRequest(),
            parent="parent_value",
        )


def test_list_deployments_rest_pager(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            telcoautomation.ListDeploymentsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListDeploymentsResponse(
                deployments=[],
                next_page_token="def",
            ),
            telcoautomation.ListDeploymentsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListDeploymentsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            telcoautomation.ListDeploymentsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/orchestrationClusters/sample3"
        }

        pager = client.list_deployments(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, telcoautomation.Deployment) for i in results)

        pages = list(client.list_deployments(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.ListDeploymentRevisionsRequest,
        dict,
    ],
)
def test_list_deployment_revisions_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.ListDeploymentRevisionsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.ListDeploymentRevisionsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_deployment_revisions(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDeploymentRevisionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_deployment_revisions_rest_required_fields(
    request_type=telcoautomation.ListDeploymentRevisionsRequest,
):
    transport_class = transports.TelcoAutomationRestTransport

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
    ).list_deployment_revisions._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_deployment_revisions._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = telcoautomation.ListDeploymentRevisionsResponse()
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

            # Convert return value to protobuf type
            return_value = telcoautomation.ListDeploymentRevisionsResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_deployment_revisions(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_deployment_revisions_rest_unset_required_fields():
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_deployment_revisions._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("name",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_deployment_revisions_rest_interceptors(null_interceptor):
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TelcoAutomationRestInterceptor(),
    )
    client = TelcoAutomationClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "post_list_deployment_revisions"
    ) as post, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "pre_list_deployment_revisions"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = telcoautomation.ListDeploymentRevisionsRequest.pb(
            telcoautomation.ListDeploymentRevisionsRequest()
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
            telcoautomation.ListDeploymentRevisionsResponse.to_json(
                telcoautomation.ListDeploymentRevisionsResponse()
            )
        )

        request = telcoautomation.ListDeploymentRevisionsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = telcoautomation.ListDeploymentRevisionsResponse()

        client.list_deployment_revisions(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_deployment_revisions_rest_bad_request(
    transport: str = "rest", request_type=telcoautomation.ListDeploymentRevisionsRequest
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4"
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
        client.list_deployment_revisions(request)


def test_list_deployment_revisions_rest_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.ListDeploymentRevisionsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.ListDeploymentRevisionsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_deployment_revisions(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/orchestrationClusters/*/deployments/*}:listRevisions"
            % client.transport._host,
            args[1],
        )


def test_list_deployment_revisions_rest_flattened_error(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_deployment_revisions(
            telcoautomation.ListDeploymentRevisionsRequest(),
            name="name_value",
        )


def test_list_deployment_revisions_rest_pager(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            telcoautomation.ListDeploymentRevisionsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListDeploymentRevisionsResponse(
                deployments=[],
                next_page_token="def",
            ),
            telcoautomation.ListDeploymentRevisionsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListDeploymentRevisionsResponse(
                deployments=[
                    telcoautomation.Deployment(),
                    telcoautomation.Deployment(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            telcoautomation.ListDeploymentRevisionsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4"
        }

        pager = client.list_deployment_revisions(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, telcoautomation.Deployment) for i in results)

        pages = list(client.list_deployment_revisions(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.DiscardDeploymentChangesRequest,
        dict,
    ],
)
def test_discard_deployment_changes_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.DiscardDeploymentChangesResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.DiscardDeploymentChangesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.discard_deployment_changes(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.DiscardDeploymentChangesResponse)


def test_discard_deployment_changes_rest_required_fields(
    request_type=telcoautomation.DiscardDeploymentChangesRequest,
):
    transport_class = transports.TelcoAutomationRestTransport

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
    ).discard_deployment_changes._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).discard_deployment_changes._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = telcoautomation.DiscardDeploymentChangesResponse()
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

            # Convert return value to protobuf type
            return_value = telcoautomation.DiscardDeploymentChangesResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.discard_deployment_changes(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_discard_deployment_changes_rest_unset_required_fields():
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.discard_deployment_changes._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_discard_deployment_changes_rest_interceptors(null_interceptor):
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TelcoAutomationRestInterceptor(),
    )
    client = TelcoAutomationClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "post_discard_deployment_changes"
    ) as post, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "pre_discard_deployment_changes"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = telcoautomation.DiscardDeploymentChangesRequest.pb(
            telcoautomation.DiscardDeploymentChangesRequest()
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
            telcoautomation.DiscardDeploymentChangesResponse.to_json(
                telcoautomation.DiscardDeploymentChangesResponse()
            )
        )

        request = telcoautomation.DiscardDeploymentChangesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = telcoautomation.DiscardDeploymentChangesResponse()

        client.discard_deployment_changes(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_discard_deployment_changes_rest_bad_request(
    transport: str = "rest",
    request_type=telcoautomation.DiscardDeploymentChangesRequest,
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4"
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
        client.discard_deployment_changes(request)


def test_discard_deployment_changes_rest_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.DiscardDeploymentChangesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.DiscardDeploymentChangesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.discard_deployment_changes(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/orchestrationClusters/*/deployments/*}:discard"
            % client.transport._host,
            args[1],
        )


def test_discard_deployment_changes_rest_flattened_error(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.discard_deployment_changes(
            telcoautomation.DiscardDeploymentChangesRequest(),
            name="name_value",
        )


def test_discard_deployment_changes_rest_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.ApplyDeploymentRequest,
        dict,
    ],
)
def test_apply_deployment_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.Deployment(
            name="name_value",
            revision_id="revision_id_value",
            source_blueprint_revision="source_blueprint_revision_value",
            state=telcoautomation.Deployment.State.DRAFT,
            display_name="display_name_value",
            repository="repository_value",
            source_provider="source_provider_value",
            workload_cluster="workload_cluster_value",
            deployment_level=telcoautomation.DeploymentLevel.HYDRATION,
            rollback_support=True,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.Deployment.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.apply_deployment(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.Deployment)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.source_blueprint_revision == "source_blueprint_revision_value"
    assert response.state == telcoautomation.Deployment.State.DRAFT
    assert response.display_name == "display_name_value"
    assert response.repository == "repository_value"
    assert response.source_provider == "source_provider_value"
    assert response.workload_cluster == "workload_cluster_value"
    assert response.deployment_level == telcoautomation.DeploymentLevel.HYDRATION
    assert response.rollback_support is True


def test_apply_deployment_rest_required_fields(
    request_type=telcoautomation.ApplyDeploymentRequest,
):
    transport_class = transports.TelcoAutomationRestTransport

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
    ).apply_deployment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).apply_deployment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = telcoautomation.Deployment()
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

            # Convert return value to protobuf type
            return_value = telcoautomation.Deployment.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.apply_deployment(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_apply_deployment_rest_unset_required_fields():
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.apply_deployment._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_apply_deployment_rest_interceptors(null_interceptor):
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TelcoAutomationRestInterceptor(),
    )
    client = TelcoAutomationClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "post_apply_deployment"
    ) as post, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "pre_apply_deployment"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = telcoautomation.ApplyDeploymentRequest.pb(
            telcoautomation.ApplyDeploymentRequest()
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
        req.return_value._content = telcoautomation.Deployment.to_json(
            telcoautomation.Deployment()
        )

        request = telcoautomation.ApplyDeploymentRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = telcoautomation.Deployment()

        client.apply_deployment(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_apply_deployment_rest_bad_request(
    transport: str = "rest", request_type=telcoautomation.ApplyDeploymentRequest
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4"
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
        client.apply_deployment(request)


def test_apply_deployment_rest_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.Deployment()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.Deployment.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.apply_deployment(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/orchestrationClusters/*/deployments/*}:apply"
            % client.transport._host,
            args[1],
        )


def test_apply_deployment_rest_flattened_error(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.apply_deployment(
            telcoautomation.ApplyDeploymentRequest(),
            name="name_value",
        )


def test_apply_deployment_rest_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.ComputeDeploymentStatusRequest,
        dict,
    ],
)
def test_compute_deployment_status_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.ComputeDeploymentStatusResponse(
            name="name_value",
            aggregated_status=telcoautomation.Status.STATUS_IN_PROGRESS,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.ComputeDeploymentStatusResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.compute_deployment_status(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.ComputeDeploymentStatusResponse)
    assert response.name == "name_value"
    assert response.aggregated_status == telcoautomation.Status.STATUS_IN_PROGRESS


def test_compute_deployment_status_rest_required_fields(
    request_type=telcoautomation.ComputeDeploymentStatusRequest,
):
    transport_class = transports.TelcoAutomationRestTransport

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
    ).compute_deployment_status._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).compute_deployment_status._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = telcoautomation.ComputeDeploymentStatusResponse()
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

            # Convert return value to protobuf type
            return_value = telcoautomation.ComputeDeploymentStatusResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.compute_deployment_status(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_compute_deployment_status_rest_unset_required_fields():
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.compute_deployment_status._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_compute_deployment_status_rest_interceptors(null_interceptor):
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TelcoAutomationRestInterceptor(),
    )
    client = TelcoAutomationClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "post_compute_deployment_status"
    ) as post, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "pre_compute_deployment_status"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = telcoautomation.ComputeDeploymentStatusRequest.pb(
            telcoautomation.ComputeDeploymentStatusRequest()
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
            telcoautomation.ComputeDeploymentStatusResponse.to_json(
                telcoautomation.ComputeDeploymentStatusResponse()
            )
        )

        request = telcoautomation.ComputeDeploymentStatusRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = telcoautomation.ComputeDeploymentStatusResponse()

        client.compute_deployment_status(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_compute_deployment_status_rest_bad_request(
    transport: str = "rest", request_type=telcoautomation.ComputeDeploymentStatusRequest
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4"
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
        client.compute_deployment_status(request)


def test_compute_deployment_status_rest_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.ComputeDeploymentStatusResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.ComputeDeploymentStatusResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.compute_deployment_status(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/orchestrationClusters/*/deployments/*}:computeDeploymentStatus"
            % client.transport._host,
            args[1],
        )


def test_compute_deployment_status_rest_flattened_error(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.compute_deployment_status(
            telcoautomation.ComputeDeploymentStatusRequest(),
            name="name_value",
        )


def test_compute_deployment_status_rest_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.RollbackDeploymentRequest,
        dict,
    ],
)
def test_rollback_deployment_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.Deployment(
            name="name_value",
            revision_id="revision_id_value",
            source_blueprint_revision="source_blueprint_revision_value",
            state=telcoautomation.Deployment.State.DRAFT,
            display_name="display_name_value",
            repository="repository_value",
            source_provider="source_provider_value",
            workload_cluster="workload_cluster_value",
            deployment_level=telcoautomation.DeploymentLevel.HYDRATION,
            rollback_support=True,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.Deployment.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.rollback_deployment(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.Deployment)
    assert response.name == "name_value"
    assert response.revision_id == "revision_id_value"
    assert response.source_blueprint_revision == "source_blueprint_revision_value"
    assert response.state == telcoautomation.Deployment.State.DRAFT
    assert response.display_name == "display_name_value"
    assert response.repository == "repository_value"
    assert response.source_provider == "source_provider_value"
    assert response.workload_cluster == "workload_cluster_value"
    assert response.deployment_level == telcoautomation.DeploymentLevel.HYDRATION
    assert response.rollback_support is True


def test_rollback_deployment_rest_required_fields(
    request_type=telcoautomation.RollbackDeploymentRequest,
):
    transport_class = transports.TelcoAutomationRestTransport

    request_init = {}
    request_init["name"] = ""
    request_init["revision_id"] = ""
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
    ).rollback_deployment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"
    jsonified_request["revisionId"] = "revision_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).rollback_deployment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"
    assert "revisionId" in jsonified_request
    assert jsonified_request["revisionId"] == "revision_id_value"

    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = telcoautomation.Deployment()
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

            # Convert return value to protobuf type
            return_value = telcoautomation.Deployment.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.rollback_deployment(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_rollback_deployment_rest_unset_required_fields():
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.rollback_deployment._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "name",
                "revisionId",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_rollback_deployment_rest_interceptors(null_interceptor):
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TelcoAutomationRestInterceptor(),
    )
    client = TelcoAutomationClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "post_rollback_deployment"
    ) as post, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "pre_rollback_deployment"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = telcoautomation.RollbackDeploymentRequest.pb(
            telcoautomation.RollbackDeploymentRequest()
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
        req.return_value._content = telcoautomation.Deployment.to_json(
            telcoautomation.Deployment()
        )

        request = telcoautomation.RollbackDeploymentRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = telcoautomation.Deployment()

        client.rollback_deployment(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_rollback_deployment_rest_bad_request(
    transport: str = "rest", request_type=telcoautomation.RollbackDeploymentRequest
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4"
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
        client.rollback_deployment(request)


def test_rollback_deployment_rest_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.Deployment()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
            revision_id="revision_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.Deployment.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.rollback_deployment(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/orchestrationClusters/*/deployments/*}:rollback"
            % client.transport._host,
            args[1],
        )


def test_rollback_deployment_rest_flattened_error(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.rollback_deployment(
            telcoautomation.RollbackDeploymentRequest(),
            name="name_value",
            revision_id="revision_id_value",
        )


def test_rollback_deployment_rest_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.GetHydratedDeploymentRequest,
        dict,
    ],
)
def test_get_hydrated_deployment_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4/hydratedDeployments/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.HydratedDeployment(
            name="name_value",
            state=telcoautomation.HydratedDeployment.State.DRAFT,
            workload_cluster="workload_cluster_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.HydratedDeployment.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_hydrated_deployment(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.HydratedDeployment)
    assert response.name == "name_value"
    assert response.state == telcoautomation.HydratedDeployment.State.DRAFT
    assert response.workload_cluster == "workload_cluster_value"


def test_get_hydrated_deployment_rest_required_fields(
    request_type=telcoautomation.GetHydratedDeploymentRequest,
):
    transport_class = transports.TelcoAutomationRestTransport

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
    ).get_hydrated_deployment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_hydrated_deployment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = telcoautomation.HydratedDeployment()
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

            # Convert return value to protobuf type
            return_value = telcoautomation.HydratedDeployment.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_hydrated_deployment(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_hydrated_deployment_rest_unset_required_fields():
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_hydrated_deployment._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_hydrated_deployment_rest_interceptors(null_interceptor):
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TelcoAutomationRestInterceptor(),
    )
    client = TelcoAutomationClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "post_get_hydrated_deployment"
    ) as post, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "pre_get_hydrated_deployment"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = telcoautomation.GetHydratedDeploymentRequest.pb(
            telcoautomation.GetHydratedDeploymentRequest()
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
        req.return_value._content = telcoautomation.HydratedDeployment.to_json(
            telcoautomation.HydratedDeployment()
        )

        request = telcoautomation.GetHydratedDeploymentRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = telcoautomation.HydratedDeployment()

        client.get_hydrated_deployment(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_hydrated_deployment_rest_bad_request(
    transport: str = "rest", request_type=telcoautomation.GetHydratedDeploymentRequest
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4/hydratedDeployments/sample5"
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
        client.get_hydrated_deployment(request)


def test_get_hydrated_deployment_rest_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.HydratedDeployment()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4/hydratedDeployments/sample5"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.HydratedDeployment.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_hydrated_deployment(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/orchestrationClusters/*/deployments/*/hydratedDeployments/*}"
            % client.transport._host,
            args[1],
        )


def test_get_hydrated_deployment_rest_flattened_error(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_hydrated_deployment(
            telcoautomation.GetHydratedDeploymentRequest(),
            name="name_value",
        )


def test_get_hydrated_deployment_rest_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.ListHydratedDeploymentsRequest,
        dict,
    ],
)
def test_list_hydrated_deployments_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.ListHydratedDeploymentsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.ListHydratedDeploymentsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_hydrated_deployments(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListHydratedDeploymentsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_hydrated_deployments_rest_required_fields(
    request_type=telcoautomation.ListHydratedDeploymentsRequest,
):
    transport_class = transports.TelcoAutomationRestTransport

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
    ).list_hydrated_deployments._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_hydrated_deployments._get_unset_required_fields(jsonified_request)
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

    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = telcoautomation.ListHydratedDeploymentsResponse()
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

            # Convert return value to protobuf type
            return_value = telcoautomation.ListHydratedDeploymentsResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_hydrated_deployments(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_hydrated_deployments_rest_unset_required_fields():
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_hydrated_deployments._get_unset_required_fields({})
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
def test_list_hydrated_deployments_rest_interceptors(null_interceptor):
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TelcoAutomationRestInterceptor(),
    )
    client = TelcoAutomationClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "post_list_hydrated_deployments"
    ) as post, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "pre_list_hydrated_deployments"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = telcoautomation.ListHydratedDeploymentsRequest.pb(
            telcoautomation.ListHydratedDeploymentsRequest()
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
            telcoautomation.ListHydratedDeploymentsResponse.to_json(
                telcoautomation.ListHydratedDeploymentsResponse()
            )
        )

        request = telcoautomation.ListHydratedDeploymentsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = telcoautomation.ListHydratedDeploymentsResponse()

        client.list_hydrated_deployments(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_hydrated_deployments_rest_bad_request(
    transport: str = "rest", request_type=telcoautomation.ListHydratedDeploymentsRequest
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4"
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
        client.list_hydrated_deployments(request)


def test_list_hydrated_deployments_rest_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.ListHydratedDeploymentsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.ListHydratedDeploymentsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_hydrated_deployments(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/orchestrationClusters/*/deployments/*}/hydratedDeployments"
            % client.transport._host,
            args[1],
        )


def test_list_hydrated_deployments_rest_flattened_error(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_hydrated_deployments(
            telcoautomation.ListHydratedDeploymentsRequest(),
            parent="parent_value",
        )


def test_list_hydrated_deployments_rest_pager(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            telcoautomation.ListHydratedDeploymentsResponse(
                hydrated_deployments=[
                    telcoautomation.HydratedDeployment(),
                    telcoautomation.HydratedDeployment(),
                    telcoautomation.HydratedDeployment(),
                ],
                next_page_token="abc",
            ),
            telcoautomation.ListHydratedDeploymentsResponse(
                hydrated_deployments=[],
                next_page_token="def",
            ),
            telcoautomation.ListHydratedDeploymentsResponse(
                hydrated_deployments=[
                    telcoautomation.HydratedDeployment(),
                ],
                next_page_token="ghi",
            ),
            telcoautomation.ListHydratedDeploymentsResponse(
                hydrated_deployments=[
                    telcoautomation.HydratedDeployment(),
                    telcoautomation.HydratedDeployment(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            telcoautomation.ListHydratedDeploymentsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4"
        }

        pager = client.list_hydrated_deployments(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, telcoautomation.HydratedDeployment) for i in results)

        pages = list(client.list_hydrated_deployments(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.UpdateHydratedDeploymentRequest,
        dict,
    ],
)
def test_update_hydrated_deployment_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "hydrated_deployment": {
            "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4/hydratedDeployments/sample5"
        }
    }
    request_init["hydrated_deployment"] = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4/hydratedDeployments/sample5",
        "state": 1,
        "files": [
            {
                "path": "path_value",
                "content": "content_value",
                "deleted": True,
                "editable": True,
            }
        ],
        "workload_cluster": "workload_cluster_value",
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = telcoautomation.UpdateHydratedDeploymentRequest.meta.fields[
        "hydrated_deployment"
    ]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["hydrated_deployment"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["hydrated_deployment"][field])):
                    del request_init["hydrated_deployment"][field][i][subfield]
            else:
                del request_init["hydrated_deployment"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.HydratedDeployment(
            name="name_value",
            state=telcoautomation.HydratedDeployment.State.DRAFT,
            workload_cluster="workload_cluster_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.HydratedDeployment.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_hydrated_deployment(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.HydratedDeployment)
    assert response.name == "name_value"
    assert response.state == telcoautomation.HydratedDeployment.State.DRAFT
    assert response.workload_cluster == "workload_cluster_value"


def test_update_hydrated_deployment_rest_required_fields(
    request_type=telcoautomation.UpdateHydratedDeploymentRequest,
):
    transport_class = transports.TelcoAutomationRestTransport

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
    ).update_hydrated_deployment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_hydrated_deployment._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = telcoautomation.HydratedDeployment()
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

            # Convert return value to protobuf type
            return_value = telcoautomation.HydratedDeployment.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_hydrated_deployment(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_hydrated_deployment_rest_unset_required_fields():
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_hydrated_deployment._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("updateMask",))
        & set(
            (
                "hydratedDeployment",
                "updateMask",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_hydrated_deployment_rest_interceptors(null_interceptor):
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TelcoAutomationRestInterceptor(),
    )
    client = TelcoAutomationClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "post_update_hydrated_deployment"
    ) as post, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "pre_update_hydrated_deployment"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = telcoautomation.UpdateHydratedDeploymentRequest.pb(
            telcoautomation.UpdateHydratedDeploymentRequest()
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
        req.return_value._content = telcoautomation.HydratedDeployment.to_json(
            telcoautomation.HydratedDeployment()
        )

        request = telcoautomation.UpdateHydratedDeploymentRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = telcoautomation.HydratedDeployment()

        client.update_hydrated_deployment(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_hydrated_deployment_rest_bad_request(
    transport: str = "rest",
    request_type=telcoautomation.UpdateHydratedDeploymentRequest,
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "hydrated_deployment": {
            "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4/hydratedDeployments/sample5"
        }
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
        client.update_hydrated_deployment(request)


def test_update_hydrated_deployment_rest_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.HydratedDeployment()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "hydrated_deployment": {
                "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4/hydratedDeployments/sample5"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            hydrated_deployment=telcoautomation.HydratedDeployment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.HydratedDeployment.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_hydrated_deployment(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{hydrated_deployment.name=projects/*/locations/*/orchestrationClusters/*/deployments/*/hydratedDeployments/*}"
            % client.transport._host,
            args[1],
        )


def test_update_hydrated_deployment_rest_flattened_error(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_hydrated_deployment(
            telcoautomation.UpdateHydratedDeploymentRequest(),
            hydrated_deployment=telcoautomation.HydratedDeployment(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_hydrated_deployment_rest_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        telcoautomation.ApplyHydratedDeploymentRequest,
        dict,
    ],
)
def test_apply_hydrated_deployment_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4/hydratedDeployments/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.HydratedDeployment(
            name="name_value",
            state=telcoautomation.HydratedDeployment.State.DRAFT,
            workload_cluster="workload_cluster_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.HydratedDeployment.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.apply_hydrated_deployment(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, telcoautomation.HydratedDeployment)
    assert response.name == "name_value"
    assert response.state == telcoautomation.HydratedDeployment.State.DRAFT
    assert response.workload_cluster == "workload_cluster_value"


def test_apply_hydrated_deployment_rest_required_fields(
    request_type=telcoautomation.ApplyHydratedDeploymentRequest,
):
    transport_class = transports.TelcoAutomationRestTransport

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
    ).apply_hydrated_deployment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).apply_hydrated_deployment._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = telcoautomation.HydratedDeployment()
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

            # Convert return value to protobuf type
            return_value = telcoautomation.HydratedDeployment.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.apply_hydrated_deployment(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_apply_hydrated_deployment_rest_unset_required_fields():
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.apply_hydrated_deployment._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_apply_hydrated_deployment_rest_interceptors(null_interceptor):
    transport = transports.TelcoAutomationRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.TelcoAutomationRestInterceptor(),
    )
    client = TelcoAutomationClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "post_apply_hydrated_deployment"
    ) as post, mock.patch.object(
        transports.TelcoAutomationRestInterceptor, "pre_apply_hydrated_deployment"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = telcoautomation.ApplyHydratedDeploymentRequest.pb(
            telcoautomation.ApplyHydratedDeploymentRequest()
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
        req.return_value._content = telcoautomation.HydratedDeployment.to_json(
            telcoautomation.HydratedDeployment()
        )

        request = telcoautomation.ApplyHydratedDeploymentRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = telcoautomation.HydratedDeployment()

        client.apply_hydrated_deployment(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_apply_hydrated_deployment_rest_bad_request(
    transport: str = "rest", request_type=telcoautomation.ApplyHydratedDeploymentRequest
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4/hydratedDeployments/sample5"
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
        client.apply_hydrated_deployment(request)


def test_apply_hydrated_deployment_rest_flattened():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = telcoautomation.HydratedDeployment()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/orchestrationClusters/sample3/deployments/sample4/hydratedDeployments/sample5"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = telcoautomation.HydratedDeployment.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.apply_hydrated_deployment(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/orchestrationClusters/*/deployments/*/hydratedDeployments/*}:apply"
            % client.transport._host,
            args[1],
        )


def test_apply_hydrated_deployment_rest_flattened_error(transport: str = "rest"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.apply_hydrated_deployment(
            telcoautomation.ApplyHydratedDeploymentRequest(),
            name="name_value",
        )


def test_apply_hydrated_deployment_rest_error():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.TelcoAutomationGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = TelcoAutomationClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.TelcoAutomationGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = TelcoAutomationClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.TelcoAutomationGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = TelcoAutomationClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = TelcoAutomationClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.TelcoAutomationGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = TelcoAutomationClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.TelcoAutomationGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = TelcoAutomationClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.TelcoAutomationGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.TelcoAutomationGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.TelcoAutomationGrpcTransport,
        transports.TelcoAutomationGrpcAsyncIOTransport,
        transports.TelcoAutomationRestTransport,
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
    transport = TelcoAutomationClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.TelcoAutomationGrpcTransport,
    )


def test_telco_automation_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.TelcoAutomationTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_telco_automation_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.telcoautomation_v1.services.telco_automation.transports.TelcoAutomationTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.TelcoAutomationTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_orchestration_clusters",
        "get_orchestration_cluster",
        "create_orchestration_cluster",
        "delete_orchestration_cluster",
        "list_edge_slms",
        "get_edge_slm",
        "create_edge_slm",
        "delete_edge_slm",
        "create_blueprint",
        "update_blueprint",
        "get_blueprint",
        "delete_blueprint",
        "list_blueprints",
        "approve_blueprint",
        "propose_blueprint",
        "reject_blueprint",
        "list_blueprint_revisions",
        "search_blueprint_revisions",
        "search_deployment_revisions",
        "discard_blueprint_changes",
        "list_public_blueprints",
        "get_public_blueprint",
        "create_deployment",
        "update_deployment",
        "get_deployment",
        "remove_deployment",
        "list_deployments",
        "list_deployment_revisions",
        "discard_deployment_changes",
        "apply_deployment",
        "compute_deployment_status",
        "rollback_deployment",
        "get_hydrated_deployment",
        "list_hydrated_deployments",
        "update_hydrated_deployment",
        "apply_hydrated_deployment",
        "get_location",
        "list_locations",
        "get_operation",
        "cancel_operation",
        "delete_operation",
        "list_operations",
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

    # Catch all for all remaining methods and properties
    remainder = [
        "kind",
    ]
    for r in remainder:
        with pytest.raises(NotImplementedError):
            getattr(transport, r)()


def test_telco_automation_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.telcoautomation_v1.services.telco_automation.transports.TelcoAutomationTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.TelcoAutomationTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_telco_automation_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.telcoautomation_v1.services.telco_automation.transports.TelcoAutomationTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.TelcoAutomationTransport()
        adc.assert_called_once()


def test_telco_automation_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        TelcoAutomationClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.TelcoAutomationGrpcTransport,
        transports.TelcoAutomationGrpcAsyncIOTransport,
    ],
)
def test_telco_automation_transport_auth_adc(transport_class):
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
        transports.TelcoAutomationGrpcTransport,
        transports.TelcoAutomationGrpcAsyncIOTransport,
        transports.TelcoAutomationRestTransport,
    ],
)
def test_telco_automation_transport_auth_gdch_credentials(transport_class):
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
        (transports.TelcoAutomationGrpcTransport, grpc_helpers),
        (transports.TelcoAutomationGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_telco_automation_transport_create_channel(transport_class, grpc_helpers):
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
            "telcoautomation.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="telcoautomation.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.TelcoAutomationGrpcTransport,
        transports.TelcoAutomationGrpcAsyncIOTransport,
    ],
)
def test_telco_automation_grpc_transport_client_cert_source_for_mtls(transport_class):
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


def test_telco_automation_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.TelcoAutomationRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


def test_telco_automation_rest_lro_client():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.AbstractOperationsClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_telco_automation_host_no_port(transport_name):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="telcoautomation.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "telcoautomation.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://telcoautomation.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_telco_automation_host_with_port(transport_name):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="telcoautomation.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "telcoautomation.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://telcoautomation.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_telco_automation_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = TelcoAutomationClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = TelcoAutomationClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.list_orchestration_clusters._session
    session2 = client2.transport.list_orchestration_clusters._session
    assert session1 != session2
    session1 = client1.transport.get_orchestration_cluster._session
    session2 = client2.transport.get_orchestration_cluster._session
    assert session1 != session2
    session1 = client1.transport.create_orchestration_cluster._session
    session2 = client2.transport.create_orchestration_cluster._session
    assert session1 != session2
    session1 = client1.transport.delete_orchestration_cluster._session
    session2 = client2.transport.delete_orchestration_cluster._session
    assert session1 != session2
    session1 = client1.transport.list_edge_slms._session
    session2 = client2.transport.list_edge_slms._session
    assert session1 != session2
    session1 = client1.transport.get_edge_slm._session
    session2 = client2.transport.get_edge_slm._session
    assert session1 != session2
    session1 = client1.transport.create_edge_slm._session
    session2 = client2.transport.create_edge_slm._session
    assert session1 != session2
    session1 = client1.transport.delete_edge_slm._session
    session2 = client2.transport.delete_edge_slm._session
    assert session1 != session2
    session1 = client1.transport.create_blueprint._session
    session2 = client2.transport.create_blueprint._session
    assert session1 != session2
    session1 = client1.transport.update_blueprint._session
    session2 = client2.transport.update_blueprint._session
    assert session1 != session2
    session1 = client1.transport.get_blueprint._session
    session2 = client2.transport.get_blueprint._session
    assert session1 != session2
    session1 = client1.transport.delete_blueprint._session
    session2 = client2.transport.delete_blueprint._session
    assert session1 != session2
    session1 = client1.transport.list_blueprints._session
    session2 = client2.transport.list_blueprints._session
    assert session1 != session2
    session1 = client1.transport.approve_blueprint._session
    session2 = client2.transport.approve_blueprint._session
    assert session1 != session2
    session1 = client1.transport.propose_blueprint._session
    session2 = client2.transport.propose_blueprint._session
    assert session1 != session2
    session1 = client1.transport.reject_blueprint._session
    session2 = client2.transport.reject_blueprint._session
    assert session1 != session2
    session1 = client1.transport.list_blueprint_revisions._session
    session2 = client2.transport.list_blueprint_revisions._session
    assert session1 != session2
    session1 = client1.transport.search_blueprint_revisions._session
    session2 = client2.transport.search_blueprint_revisions._session
    assert session1 != session2
    session1 = client1.transport.search_deployment_revisions._session
    session2 = client2.transport.search_deployment_revisions._session
    assert session1 != session2
    session1 = client1.transport.discard_blueprint_changes._session
    session2 = client2.transport.discard_blueprint_changes._session
    assert session1 != session2
    session1 = client1.transport.list_public_blueprints._session
    session2 = client2.transport.list_public_blueprints._session
    assert session1 != session2
    session1 = client1.transport.get_public_blueprint._session
    session2 = client2.transport.get_public_blueprint._session
    assert session1 != session2
    session1 = client1.transport.create_deployment._session
    session2 = client2.transport.create_deployment._session
    assert session1 != session2
    session1 = client1.transport.update_deployment._session
    session2 = client2.transport.update_deployment._session
    assert session1 != session2
    session1 = client1.transport.get_deployment._session
    session2 = client2.transport.get_deployment._session
    assert session1 != session2
    session1 = client1.transport.remove_deployment._session
    session2 = client2.transport.remove_deployment._session
    assert session1 != session2
    session1 = client1.transport.list_deployments._session
    session2 = client2.transport.list_deployments._session
    assert session1 != session2
    session1 = client1.transport.list_deployment_revisions._session
    session2 = client2.transport.list_deployment_revisions._session
    assert session1 != session2
    session1 = client1.transport.discard_deployment_changes._session
    session2 = client2.transport.discard_deployment_changes._session
    assert session1 != session2
    session1 = client1.transport.apply_deployment._session
    session2 = client2.transport.apply_deployment._session
    assert session1 != session2
    session1 = client1.transport.compute_deployment_status._session
    session2 = client2.transport.compute_deployment_status._session
    assert session1 != session2
    session1 = client1.transport.rollback_deployment._session
    session2 = client2.transport.rollback_deployment._session
    assert session1 != session2
    session1 = client1.transport.get_hydrated_deployment._session
    session2 = client2.transport.get_hydrated_deployment._session
    assert session1 != session2
    session1 = client1.transport.list_hydrated_deployments._session
    session2 = client2.transport.list_hydrated_deployments._session
    assert session1 != session2
    session1 = client1.transport.update_hydrated_deployment._session
    session2 = client2.transport.update_hydrated_deployment._session
    assert session1 != session2
    session1 = client1.transport.apply_hydrated_deployment._session
    session2 = client2.transport.apply_hydrated_deployment._session
    assert session1 != session2


def test_telco_automation_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.TelcoAutomationGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_telco_automation_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.TelcoAutomationGrpcAsyncIOTransport(
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
        transports.TelcoAutomationGrpcTransport,
        transports.TelcoAutomationGrpcAsyncIOTransport,
    ],
)
def test_telco_automation_transport_channel_mtls_with_client_cert_source(
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
        transports.TelcoAutomationGrpcTransport,
        transports.TelcoAutomationGrpcAsyncIOTransport,
    ],
)
def test_telco_automation_transport_channel_mtls_with_adc(transport_class):
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


def test_telco_automation_grpc_lro_client():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.OperationsClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_telco_automation_grpc_lro_async_client():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.OperationsAsyncClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_blueprint_path():
    project = "squid"
    location = "clam"
    orchestration_cluster = "whelk"
    blueprint = "octopus"
    expected = "projects/{project}/locations/{location}/orchestrationClusters/{orchestration_cluster}/blueprints/{blueprint}".format(
        project=project,
        location=location,
        orchestration_cluster=orchestration_cluster,
        blueprint=blueprint,
    )
    actual = TelcoAutomationClient.blueprint_path(
        project, location, orchestration_cluster, blueprint
    )
    assert expected == actual


def test_parse_blueprint_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
        "orchestration_cluster": "cuttlefish",
        "blueprint": "mussel",
    }
    path = TelcoAutomationClient.blueprint_path(**expected)

    # Check that the path construction is reversible.
    actual = TelcoAutomationClient.parse_blueprint_path(path)
    assert expected == actual


def test_deployment_path():
    project = "winkle"
    location = "nautilus"
    orchestration_cluster = "scallop"
    deployment = "abalone"
    expected = "projects/{project}/locations/{location}/orchestrationClusters/{orchestration_cluster}/deployments/{deployment}".format(
        project=project,
        location=location,
        orchestration_cluster=orchestration_cluster,
        deployment=deployment,
    )
    actual = TelcoAutomationClient.deployment_path(
        project, location, orchestration_cluster, deployment
    )
    assert expected == actual


def test_parse_deployment_path():
    expected = {
        "project": "squid",
        "location": "clam",
        "orchestration_cluster": "whelk",
        "deployment": "octopus",
    }
    path = TelcoAutomationClient.deployment_path(**expected)

    # Check that the path construction is reversible.
    actual = TelcoAutomationClient.parse_deployment_path(path)
    assert expected == actual


def test_edge_slm_path():
    project = "oyster"
    location = "nudibranch"
    edge_slm = "cuttlefish"
    expected = "projects/{project}/locations/{location}/edgeSlms/{edge_slm}".format(
        project=project,
        location=location,
        edge_slm=edge_slm,
    )
    actual = TelcoAutomationClient.edge_slm_path(project, location, edge_slm)
    assert expected == actual


def test_parse_edge_slm_path():
    expected = {
        "project": "mussel",
        "location": "winkle",
        "edge_slm": "nautilus",
    }
    path = TelcoAutomationClient.edge_slm_path(**expected)

    # Check that the path construction is reversible.
    actual = TelcoAutomationClient.parse_edge_slm_path(path)
    assert expected == actual


def test_hydrated_deployment_path():
    project = "scallop"
    location = "abalone"
    orchestration_cluster = "squid"
    deployment = "clam"
    hydrated_deployment = "whelk"
    expected = "projects/{project}/locations/{location}/orchestrationClusters/{orchestration_cluster}/deployments/{deployment}/hydratedDeployments/{hydrated_deployment}".format(
        project=project,
        location=location,
        orchestration_cluster=orchestration_cluster,
        deployment=deployment,
        hydrated_deployment=hydrated_deployment,
    )
    actual = TelcoAutomationClient.hydrated_deployment_path(
        project, location, orchestration_cluster, deployment, hydrated_deployment
    )
    assert expected == actual


def test_parse_hydrated_deployment_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "orchestration_cluster": "nudibranch",
        "deployment": "cuttlefish",
        "hydrated_deployment": "mussel",
    }
    path = TelcoAutomationClient.hydrated_deployment_path(**expected)

    # Check that the path construction is reversible.
    actual = TelcoAutomationClient.parse_hydrated_deployment_path(path)
    assert expected == actual


def test_orchestration_cluster_path():
    project = "winkle"
    location = "nautilus"
    orchestration_cluster = "scallop"
    expected = "projects/{project}/locations/{location}/orchestrationClusters/{orchestration_cluster}".format(
        project=project,
        location=location,
        orchestration_cluster=orchestration_cluster,
    )
    actual = TelcoAutomationClient.orchestration_cluster_path(
        project, location, orchestration_cluster
    )
    assert expected == actual


def test_parse_orchestration_cluster_path():
    expected = {
        "project": "abalone",
        "location": "squid",
        "orchestration_cluster": "clam",
    }
    path = TelcoAutomationClient.orchestration_cluster_path(**expected)

    # Check that the path construction is reversible.
    actual = TelcoAutomationClient.parse_orchestration_cluster_path(path)
    assert expected == actual


def test_public_blueprint_path():
    project = "whelk"
    location = "octopus"
    public_lueprint = "oyster"
    expected = "projects/{project}/locations/{location}/publicBlueprints/{public_lueprint}".format(
        project=project,
        location=location,
        public_lueprint=public_lueprint,
    )
    actual = TelcoAutomationClient.public_blueprint_path(
        project, location, public_lueprint
    )
    assert expected == actual


def test_parse_public_blueprint_path():
    expected = {
        "project": "nudibranch",
        "location": "cuttlefish",
        "public_lueprint": "mussel",
    }
    path = TelcoAutomationClient.public_blueprint_path(**expected)

    # Check that the path construction is reversible.
    actual = TelcoAutomationClient.parse_public_blueprint_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "winkle"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = TelcoAutomationClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "nautilus",
    }
    path = TelcoAutomationClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = TelcoAutomationClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "scallop"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = TelcoAutomationClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "abalone",
    }
    path = TelcoAutomationClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = TelcoAutomationClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "squid"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = TelcoAutomationClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "clam",
    }
    path = TelcoAutomationClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = TelcoAutomationClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "whelk"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = TelcoAutomationClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "octopus",
    }
    path = TelcoAutomationClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = TelcoAutomationClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "oyster"
    location = "nudibranch"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = TelcoAutomationClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "cuttlefish",
        "location": "mussel",
    }
    path = TelcoAutomationClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = TelcoAutomationClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.TelcoAutomationTransport, "_prep_wrapped_messages"
    ) as prep:
        client = TelcoAutomationClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.TelcoAutomationTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = TelcoAutomationClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(
        type(getattr(client.transport, "grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_get_location_rest_bad_request(
    transport: str = "rest", request_type=locations_pb2.GetLocationRequest
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/locations/sample2"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_location(request)


@pytest.mark.parametrize(
    "request_type",
    [
        locations_pb2.GetLocationRequest,
        dict,
    ],
)
def test_get_location_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = locations_pb2.Location()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.get_location(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.Location)


def test_list_locations_rest_bad_request(
    transport: str = "rest", request_type=locations_pb2.ListLocationsRequest
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict({"name": "projects/sample1/locations"}, request)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_locations(request)


@pytest.mark.parametrize(
    "request_type",
    [
        locations_pb2.ListLocationsRequest,
        dict,
    ],
)
def test_list_locations_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = locations_pb2.ListLocationsResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.list_locations(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.ListLocationsResponse)


def test_cancel_operation_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.CancelOperationRequest
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/locations/sample2/operations/sample3"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.cancel_operation(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.CancelOperationRequest,
        dict,
    ],
)
def test_cancel_operation_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations/sample2/operations/sample3"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = "{}"

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.cancel_operation(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_operation_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.DeleteOperationRequest
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/locations/sample2/operations/sample3"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_operation(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.DeleteOperationRequest,
        dict,
    ],
)
def test_delete_operation_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations/sample2/operations/sample3"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = "{}"

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.delete_operation(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_get_operation_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.GetOperationRequest
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/locations/sample2/operations/sample3"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_operation(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.GetOperationRequest,
        dict,
    ],
)
def test_get_operation_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations/sample2/operations/sample3"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.get_operation(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


def test_list_operations_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.ListOperationsRequest
):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/locations/sample2/operations"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_operations(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.ListOperationsRequest,
        dict,
    ],
)
def test_list_operations_rest(request_type):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations/sample2/operations"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.ListOperationsResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.list_operations(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


def test_delete_operation(transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.DeleteOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_operation_async(transport: str = "grpc"):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.DeleteOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_operation_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.DeleteOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        call.return_value = None

        client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_operation_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.DeleteOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_delete_operation_from_dict():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_delete_operation_from_dict_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_cancel_operation(transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.CancelOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_cancel_operation_async(transport: str = "grpc"):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.CancelOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_cancel_operation_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.CancelOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        call.return_value = None

        client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_cancel_operation_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.CancelOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_cancel_operation_from_dict():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.cancel_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_cancel_operation_from_dict_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.cancel_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_get_operation(transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.GetOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation()
        response = client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


@pytest.mark.asyncio
async def test_get_operation_async(transport: str = "grpc"):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.GetOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        response = await client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


def test_get_operation_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.GetOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        call.return_value = operations_pb2.Operation()

        client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_operation_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.GetOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        await client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_get_operation_from_dict():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation()

        response = client.get_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_get_operation_from_dict_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        response = await client.get_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_list_operations(transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.ListOperationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.ListOperationsResponse()
        response = client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


@pytest.mark.asyncio
async def test_list_operations_async(transport: str = "grpc"):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.ListOperationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        response = await client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


def test_list_operations_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.ListOperationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        call.return_value = operations_pb2.ListOperationsResponse()

        client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_operations_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.ListOperationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        await client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_list_operations_from_dict():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.ListOperationsResponse()

        response = client.list_operations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_list_operations_from_dict_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        response = await client.list_operations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_list_locations(transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = locations_pb2.ListLocationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = locations_pb2.ListLocationsResponse()
        response = client.list_locations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.ListLocationsResponse)


@pytest.mark.asyncio
async def test_list_locations_async(transport: str = "grpc"):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = locations_pb2.ListLocationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.ListLocationsResponse()
        )
        response = await client.list_locations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.ListLocationsResponse)


def test_list_locations_field_headers():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = locations_pb2.ListLocationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        call.return_value = locations_pb2.ListLocationsResponse()

        client.list_locations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_locations_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = locations_pb2.ListLocationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.ListLocationsResponse()
        )
        await client.list_locations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_list_locations_from_dict():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = locations_pb2.ListLocationsResponse()

        response = client.list_locations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_list_locations_from_dict_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.ListLocationsResponse()
        )
        response = await client.list_locations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_get_location(transport: str = "grpc"):
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = locations_pb2.GetLocationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_location), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = locations_pb2.Location()
        response = client.get_location(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.Location)


@pytest.mark.asyncio
async def test_get_location_async(transport: str = "grpc_asyncio"):
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = locations_pb2.GetLocationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_location), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.Location()
        )
        response = await client.get_location(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.Location)


def test_get_location_field_headers():
    client = TelcoAutomationClient(credentials=ga_credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = locations_pb2.GetLocationRequest()
    request.name = "locations/abc"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_location), "__call__") as call:
        call.return_value = locations_pb2.Location()

        client.get_location(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations/abc",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_location_field_headers_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials()
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = locations_pb2.GetLocationRequest()
    request.name = "locations/abc"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_location), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.Location()
        )
        await client.get_location(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations/abc",
    ) in kw["metadata"]


def test_get_location_from_dict():
    client = TelcoAutomationClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = locations_pb2.Location()

        response = client.get_location(
            request={
                "name": "locations/abc",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_get_location_from_dict_async():
    client = TelcoAutomationAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.Location()
        )
        response = await client.get_location(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_transport_close():
    transports = {
        "rest": "_session",
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = TelcoAutomationClient(
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
        client = TelcoAutomationClient(
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
        (TelcoAutomationClient, transports.TelcoAutomationGrpcTransport),
        (TelcoAutomationAsyncClient, transports.TelcoAutomationGrpcAsyncIOTransport),
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
