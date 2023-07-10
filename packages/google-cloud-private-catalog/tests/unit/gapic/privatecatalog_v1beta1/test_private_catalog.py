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
from google.protobuf import json_format
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest
from requests import PreparedRequest, Request, Response
from requests.sessions import Session

from google.cloud.privatecatalog_v1beta1.services.private_catalog import (
    PrivateCatalogAsyncClient,
    PrivateCatalogClient,
    pagers,
    transports,
)
from google.cloud.privatecatalog_v1beta1.types import private_catalog


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

    assert PrivateCatalogClient._get_default_mtls_endpoint(None) is None
    assert (
        PrivateCatalogClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        PrivateCatalogClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        PrivateCatalogClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        PrivateCatalogClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        PrivateCatalogClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (PrivateCatalogClient, "grpc"),
        (PrivateCatalogAsyncClient, "grpc_asyncio"),
        (PrivateCatalogClient, "rest"),
    ],
)
def test_private_catalog_client_from_service_account_info(client_class, transport_name):
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
            "cloudprivatecatalog.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://cloudprivatecatalog.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.PrivateCatalogGrpcTransport, "grpc"),
        (transports.PrivateCatalogGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.PrivateCatalogRestTransport, "rest"),
    ],
)
def test_private_catalog_client_service_account_always_use_jwt(
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
        (PrivateCatalogClient, "grpc"),
        (PrivateCatalogAsyncClient, "grpc_asyncio"),
        (PrivateCatalogClient, "rest"),
    ],
)
def test_private_catalog_client_from_service_account_file(client_class, transport_name):
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
            "cloudprivatecatalog.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://cloudprivatecatalog.googleapis.com"
        )


def test_private_catalog_client_get_transport_class():
    transport = PrivateCatalogClient.get_transport_class()
    available_transports = [
        transports.PrivateCatalogGrpcTransport,
        transports.PrivateCatalogRestTransport,
    ]
    assert transport in available_transports

    transport = PrivateCatalogClient.get_transport_class("grpc")
    assert transport == transports.PrivateCatalogGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (PrivateCatalogClient, transports.PrivateCatalogGrpcTransport, "grpc"),
        (
            PrivateCatalogAsyncClient,
            transports.PrivateCatalogGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (PrivateCatalogClient, transports.PrivateCatalogRestTransport, "rest"),
    ],
)
@mock.patch.object(
    PrivateCatalogClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(PrivateCatalogClient),
)
@mock.patch.object(
    PrivateCatalogAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(PrivateCatalogAsyncClient),
)
def test_private_catalog_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(PrivateCatalogClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(PrivateCatalogClient, "get_transport_class") as gtc:
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
        (PrivateCatalogClient, transports.PrivateCatalogGrpcTransport, "grpc", "true"),
        (
            PrivateCatalogAsyncClient,
            transports.PrivateCatalogGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (PrivateCatalogClient, transports.PrivateCatalogGrpcTransport, "grpc", "false"),
        (
            PrivateCatalogAsyncClient,
            transports.PrivateCatalogGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (PrivateCatalogClient, transports.PrivateCatalogRestTransport, "rest", "true"),
        (PrivateCatalogClient, transports.PrivateCatalogRestTransport, "rest", "false"),
    ],
)
@mock.patch.object(
    PrivateCatalogClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(PrivateCatalogClient),
)
@mock.patch.object(
    PrivateCatalogAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(PrivateCatalogAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_private_catalog_client_mtls_env_auto(
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
    "client_class", [PrivateCatalogClient, PrivateCatalogAsyncClient]
)
@mock.patch.object(
    PrivateCatalogClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(PrivateCatalogClient),
)
@mock.patch.object(
    PrivateCatalogAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(PrivateCatalogAsyncClient),
)
def test_private_catalog_client_get_mtls_endpoint_and_cert_source(client_class):
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
        (PrivateCatalogClient, transports.PrivateCatalogGrpcTransport, "grpc"),
        (
            PrivateCatalogAsyncClient,
            transports.PrivateCatalogGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (PrivateCatalogClient, transports.PrivateCatalogRestTransport, "rest"),
    ],
)
def test_private_catalog_client_client_options_scopes(
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
            PrivateCatalogClient,
            transports.PrivateCatalogGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            PrivateCatalogAsyncClient,
            transports.PrivateCatalogGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (PrivateCatalogClient, transports.PrivateCatalogRestTransport, "rest", None),
    ],
)
def test_private_catalog_client_client_options_credentials_file(
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


def test_private_catalog_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.privatecatalog_v1beta1.services.private_catalog.transports.PrivateCatalogGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = PrivateCatalogClient(
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
            PrivateCatalogClient,
            transports.PrivateCatalogGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            PrivateCatalogAsyncClient,
            transports.PrivateCatalogGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_private_catalog_client_create_channel_credentials_file(
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
            "cloudprivatecatalog.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="cloudprivatecatalog.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        private_catalog.SearchCatalogsRequest,
        dict,
    ],
)
def test_search_catalogs(request_type, transport: str = "grpc"):
    client = PrivateCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_catalogs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = private_catalog.SearchCatalogsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.search_catalogs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == private_catalog.SearchCatalogsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchCatalogsPager)
    assert response.next_page_token == "next_page_token_value"


def test_search_catalogs_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = PrivateCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_catalogs), "__call__") as call:
        client.search_catalogs()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == private_catalog.SearchCatalogsRequest()


@pytest.mark.asyncio
async def test_search_catalogs_async(
    transport: str = "grpc_asyncio", request_type=private_catalog.SearchCatalogsRequest
):
    client = PrivateCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_catalogs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            private_catalog.SearchCatalogsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.search_catalogs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == private_catalog.SearchCatalogsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchCatalogsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_search_catalogs_async_from_dict():
    await test_search_catalogs_async(request_type=dict)


def test_search_catalogs_field_headers():
    client = PrivateCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = private_catalog.SearchCatalogsRequest()

    request.resource = "resource_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_catalogs), "__call__") as call:
        call.return_value = private_catalog.SearchCatalogsResponse()
        client.search_catalogs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_search_catalogs_field_headers_async():
    client = PrivateCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = private_catalog.SearchCatalogsRequest()

    request.resource = "resource_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_catalogs), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            private_catalog.SearchCatalogsResponse()
        )
        await client.search_catalogs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource_value",
    ) in kw["metadata"]


def test_search_catalogs_pager(transport_name: str = "grpc"):
    client = PrivateCatalogClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_catalogs), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            private_catalog.SearchCatalogsResponse(
                catalogs=[
                    private_catalog.Catalog(),
                    private_catalog.Catalog(),
                    private_catalog.Catalog(),
                ],
                next_page_token="abc",
            ),
            private_catalog.SearchCatalogsResponse(
                catalogs=[],
                next_page_token="def",
            ),
            private_catalog.SearchCatalogsResponse(
                catalogs=[
                    private_catalog.Catalog(),
                ],
                next_page_token="ghi",
            ),
            private_catalog.SearchCatalogsResponse(
                catalogs=[
                    private_catalog.Catalog(),
                    private_catalog.Catalog(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", ""),)),
        )
        pager = client.search_catalogs(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, private_catalog.Catalog) for i in results)


def test_search_catalogs_pages(transport_name: str = "grpc"):
    client = PrivateCatalogClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_catalogs), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            private_catalog.SearchCatalogsResponse(
                catalogs=[
                    private_catalog.Catalog(),
                    private_catalog.Catalog(),
                    private_catalog.Catalog(),
                ],
                next_page_token="abc",
            ),
            private_catalog.SearchCatalogsResponse(
                catalogs=[],
                next_page_token="def",
            ),
            private_catalog.SearchCatalogsResponse(
                catalogs=[
                    private_catalog.Catalog(),
                ],
                next_page_token="ghi",
            ),
            private_catalog.SearchCatalogsResponse(
                catalogs=[
                    private_catalog.Catalog(),
                    private_catalog.Catalog(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.search_catalogs(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_search_catalogs_async_pager():
    client = PrivateCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_catalogs), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            private_catalog.SearchCatalogsResponse(
                catalogs=[
                    private_catalog.Catalog(),
                    private_catalog.Catalog(),
                    private_catalog.Catalog(),
                ],
                next_page_token="abc",
            ),
            private_catalog.SearchCatalogsResponse(
                catalogs=[],
                next_page_token="def",
            ),
            private_catalog.SearchCatalogsResponse(
                catalogs=[
                    private_catalog.Catalog(),
                ],
                next_page_token="ghi",
            ),
            private_catalog.SearchCatalogsResponse(
                catalogs=[
                    private_catalog.Catalog(),
                    private_catalog.Catalog(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.search_catalogs(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, private_catalog.Catalog) for i in responses)


@pytest.mark.asyncio
async def test_search_catalogs_async_pages():
    client = PrivateCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_catalogs), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            private_catalog.SearchCatalogsResponse(
                catalogs=[
                    private_catalog.Catalog(),
                    private_catalog.Catalog(),
                    private_catalog.Catalog(),
                ],
                next_page_token="abc",
            ),
            private_catalog.SearchCatalogsResponse(
                catalogs=[],
                next_page_token="def",
            ),
            private_catalog.SearchCatalogsResponse(
                catalogs=[
                    private_catalog.Catalog(),
                ],
                next_page_token="ghi",
            ),
            private_catalog.SearchCatalogsResponse(
                catalogs=[
                    private_catalog.Catalog(),
                    private_catalog.Catalog(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.search_catalogs(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        private_catalog.SearchProductsRequest,
        dict,
    ],
)
def test_search_products(request_type, transport: str = "grpc"):
    client = PrivateCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_products), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = private_catalog.SearchProductsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.search_products(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == private_catalog.SearchProductsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchProductsPager)
    assert response.next_page_token == "next_page_token_value"


def test_search_products_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = PrivateCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_products), "__call__") as call:
        client.search_products()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == private_catalog.SearchProductsRequest()


@pytest.mark.asyncio
async def test_search_products_async(
    transport: str = "grpc_asyncio", request_type=private_catalog.SearchProductsRequest
):
    client = PrivateCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_products), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            private_catalog.SearchProductsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.search_products(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == private_catalog.SearchProductsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchProductsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_search_products_async_from_dict():
    await test_search_products_async(request_type=dict)


def test_search_products_field_headers():
    client = PrivateCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = private_catalog.SearchProductsRequest()

    request.resource = "resource_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_products), "__call__") as call:
        call.return_value = private_catalog.SearchProductsResponse()
        client.search_products(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_search_products_field_headers_async():
    client = PrivateCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = private_catalog.SearchProductsRequest()

    request.resource = "resource_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_products), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            private_catalog.SearchProductsResponse()
        )
        await client.search_products(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource_value",
    ) in kw["metadata"]


def test_search_products_pager(transport_name: str = "grpc"):
    client = PrivateCatalogClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_products), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            private_catalog.SearchProductsResponse(
                products=[
                    private_catalog.Product(),
                    private_catalog.Product(),
                    private_catalog.Product(),
                ],
                next_page_token="abc",
            ),
            private_catalog.SearchProductsResponse(
                products=[],
                next_page_token="def",
            ),
            private_catalog.SearchProductsResponse(
                products=[
                    private_catalog.Product(),
                ],
                next_page_token="ghi",
            ),
            private_catalog.SearchProductsResponse(
                products=[
                    private_catalog.Product(),
                    private_catalog.Product(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", ""),)),
        )
        pager = client.search_products(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, private_catalog.Product) for i in results)


def test_search_products_pages(transport_name: str = "grpc"):
    client = PrivateCatalogClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_products), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            private_catalog.SearchProductsResponse(
                products=[
                    private_catalog.Product(),
                    private_catalog.Product(),
                    private_catalog.Product(),
                ],
                next_page_token="abc",
            ),
            private_catalog.SearchProductsResponse(
                products=[],
                next_page_token="def",
            ),
            private_catalog.SearchProductsResponse(
                products=[
                    private_catalog.Product(),
                ],
                next_page_token="ghi",
            ),
            private_catalog.SearchProductsResponse(
                products=[
                    private_catalog.Product(),
                    private_catalog.Product(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.search_products(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_search_products_async_pager():
    client = PrivateCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_products), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            private_catalog.SearchProductsResponse(
                products=[
                    private_catalog.Product(),
                    private_catalog.Product(),
                    private_catalog.Product(),
                ],
                next_page_token="abc",
            ),
            private_catalog.SearchProductsResponse(
                products=[],
                next_page_token="def",
            ),
            private_catalog.SearchProductsResponse(
                products=[
                    private_catalog.Product(),
                ],
                next_page_token="ghi",
            ),
            private_catalog.SearchProductsResponse(
                products=[
                    private_catalog.Product(),
                    private_catalog.Product(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.search_products(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, private_catalog.Product) for i in responses)


@pytest.mark.asyncio
async def test_search_products_async_pages():
    client = PrivateCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_products), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            private_catalog.SearchProductsResponse(
                products=[
                    private_catalog.Product(),
                    private_catalog.Product(),
                    private_catalog.Product(),
                ],
                next_page_token="abc",
            ),
            private_catalog.SearchProductsResponse(
                products=[],
                next_page_token="def",
            ),
            private_catalog.SearchProductsResponse(
                products=[
                    private_catalog.Product(),
                ],
                next_page_token="ghi",
            ),
            private_catalog.SearchProductsResponse(
                products=[
                    private_catalog.Product(),
                    private_catalog.Product(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.search_products(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        private_catalog.SearchVersionsRequest,
        dict,
    ],
)
def test_search_versions(request_type, transport: str = "grpc"):
    client = PrivateCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_versions), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = private_catalog.SearchVersionsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.search_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == private_catalog.SearchVersionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchVersionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_search_versions_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = PrivateCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_versions), "__call__") as call:
        client.search_versions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == private_catalog.SearchVersionsRequest()


@pytest.mark.asyncio
async def test_search_versions_async(
    transport: str = "grpc_asyncio", request_type=private_catalog.SearchVersionsRequest
):
    client = PrivateCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_versions), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            private_catalog.SearchVersionsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.search_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == private_catalog.SearchVersionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchVersionsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_search_versions_async_from_dict():
    await test_search_versions_async(request_type=dict)


def test_search_versions_field_headers():
    client = PrivateCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = private_catalog.SearchVersionsRequest()

    request.resource = "resource_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_versions), "__call__") as call:
        call.return_value = private_catalog.SearchVersionsResponse()
        client.search_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_search_versions_field_headers_async():
    client = PrivateCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = private_catalog.SearchVersionsRequest()

    request.resource = "resource_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_versions), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            private_catalog.SearchVersionsResponse()
        )
        await client.search_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource_value",
    ) in kw["metadata"]


def test_search_versions_pager(transport_name: str = "grpc"):
    client = PrivateCatalogClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_versions), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            private_catalog.SearchVersionsResponse(
                versions=[
                    private_catalog.Version(),
                    private_catalog.Version(),
                    private_catalog.Version(),
                ],
                next_page_token="abc",
            ),
            private_catalog.SearchVersionsResponse(
                versions=[],
                next_page_token="def",
            ),
            private_catalog.SearchVersionsResponse(
                versions=[
                    private_catalog.Version(),
                ],
                next_page_token="ghi",
            ),
            private_catalog.SearchVersionsResponse(
                versions=[
                    private_catalog.Version(),
                    private_catalog.Version(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", ""),)),
        )
        pager = client.search_versions(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, private_catalog.Version) for i in results)


def test_search_versions_pages(transport_name: str = "grpc"):
    client = PrivateCatalogClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.search_versions), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            private_catalog.SearchVersionsResponse(
                versions=[
                    private_catalog.Version(),
                    private_catalog.Version(),
                    private_catalog.Version(),
                ],
                next_page_token="abc",
            ),
            private_catalog.SearchVersionsResponse(
                versions=[],
                next_page_token="def",
            ),
            private_catalog.SearchVersionsResponse(
                versions=[
                    private_catalog.Version(),
                ],
                next_page_token="ghi",
            ),
            private_catalog.SearchVersionsResponse(
                versions=[
                    private_catalog.Version(),
                    private_catalog.Version(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.search_versions(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_search_versions_async_pager():
    client = PrivateCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_versions), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            private_catalog.SearchVersionsResponse(
                versions=[
                    private_catalog.Version(),
                    private_catalog.Version(),
                    private_catalog.Version(),
                ],
                next_page_token="abc",
            ),
            private_catalog.SearchVersionsResponse(
                versions=[],
                next_page_token="def",
            ),
            private_catalog.SearchVersionsResponse(
                versions=[
                    private_catalog.Version(),
                ],
                next_page_token="ghi",
            ),
            private_catalog.SearchVersionsResponse(
                versions=[
                    private_catalog.Version(),
                    private_catalog.Version(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.search_versions(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, private_catalog.Version) for i in responses)


@pytest.mark.asyncio
async def test_search_versions_async_pages():
    client = PrivateCatalogAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_versions), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            private_catalog.SearchVersionsResponse(
                versions=[
                    private_catalog.Version(),
                    private_catalog.Version(),
                    private_catalog.Version(),
                ],
                next_page_token="abc",
            ),
            private_catalog.SearchVersionsResponse(
                versions=[],
                next_page_token="def",
            ),
            private_catalog.SearchVersionsResponse(
                versions=[
                    private_catalog.Version(),
                ],
                next_page_token="ghi",
            ),
            private_catalog.SearchVersionsResponse(
                versions=[
                    private_catalog.Version(),
                    private_catalog.Version(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.search_versions(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        private_catalog.SearchCatalogsRequest,
        dict,
    ],
)
def test_search_catalogs_rest(request_type):
    client = PrivateCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"resource": "projects/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = private_catalog.SearchCatalogsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = private_catalog.SearchCatalogsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.search_catalogs(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchCatalogsPager)
    assert response.next_page_token == "next_page_token_value"


def test_search_catalogs_rest_required_fields(
    request_type=private_catalog.SearchCatalogsRequest,
):
    transport_class = transports.PrivateCatalogRestTransport

    request_init = {}
    request_init["resource"] = ""
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
    ).search_catalogs._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["resource"] = "resource_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).search_catalogs._get_unset_required_fields(jsonified_request)
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
    assert "resource" in jsonified_request
    assert jsonified_request["resource"] == "resource_value"

    client = PrivateCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = private_catalog.SearchCatalogsResponse()
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

            pb_return_value = private_catalog.SearchCatalogsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.search_catalogs(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_search_catalogs_rest_unset_required_fields():
    transport = transports.PrivateCatalogRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.search_catalogs._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
                "query",
            )
        )
        & set(("resource",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_search_catalogs_rest_interceptors(null_interceptor):
    transport = transports.PrivateCatalogRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.PrivateCatalogRestInterceptor(),
    )
    client = PrivateCatalogClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.PrivateCatalogRestInterceptor, "post_search_catalogs"
    ) as post, mock.patch.object(
        transports.PrivateCatalogRestInterceptor, "pre_search_catalogs"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = private_catalog.SearchCatalogsRequest.pb(
            private_catalog.SearchCatalogsRequest()
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
        req.return_value._content = private_catalog.SearchCatalogsResponse.to_json(
            private_catalog.SearchCatalogsResponse()
        )

        request = private_catalog.SearchCatalogsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = private_catalog.SearchCatalogsResponse()

        client.search_catalogs(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_search_catalogs_rest_bad_request(
    transport: str = "rest", request_type=private_catalog.SearchCatalogsRequest
):
    client = PrivateCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"resource": "projects/sample1"}
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
        client.search_catalogs(request)


def test_search_catalogs_rest_pager(transport: str = "rest"):
    client = PrivateCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            private_catalog.SearchCatalogsResponse(
                catalogs=[
                    private_catalog.Catalog(),
                    private_catalog.Catalog(),
                    private_catalog.Catalog(),
                ],
                next_page_token="abc",
            ),
            private_catalog.SearchCatalogsResponse(
                catalogs=[],
                next_page_token="def",
            ),
            private_catalog.SearchCatalogsResponse(
                catalogs=[
                    private_catalog.Catalog(),
                ],
                next_page_token="ghi",
            ),
            private_catalog.SearchCatalogsResponse(
                catalogs=[
                    private_catalog.Catalog(),
                    private_catalog.Catalog(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            private_catalog.SearchCatalogsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"resource": "projects/sample1"}

        pager = client.search_catalogs(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, private_catalog.Catalog) for i in results)

        pages = list(client.search_catalogs(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        private_catalog.SearchProductsRequest,
        dict,
    ],
)
def test_search_products_rest(request_type):
    client = PrivateCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"resource": "projects/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = private_catalog.SearchProductsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = private_catalog.SearchProductsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.search_products(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchProductsPager)
    assert response.next_page_token == "next_page_token_value"


def test_search_products_rest_required_fields(
    request_type=private_catalog.SearchProductsRequest,
):
    transport_class = transports.PrivateCatalogRestTransport

    request_init = {}
    request_init["resource"] = ""
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
    ).search_products._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["resource"] = "resource_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).search_products._get_unset_required_fields(jsonified_request)
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
    assert "resource" in jsonified_request
    assert jsonified_request["resource"] == "resource_value"

    client = PrivateCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = private_catalog.SearchProductsResponse()
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

            pb_return_value = private_catalog.SearchProductsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.search_products(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_search_products_rest_unset_required_fields():
    transport = transports.PrivateCatalogRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.search_products._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
                "query",
            )
        )
        & set(("resource",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_search_products_rest_interceptors(null_interceptor):
    transport = transports.PrivateCatalogRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.PrivateCatalogRestInterceptor(),
    )
    client = PrivateCatalogClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.PrivateCatalogRestInterceptor, "post_search_products"
    ) as post, mock.patch.object(
        transports.PrivateCatalogRestInterceptor, "pre_search_products"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = private_catalog.SearchProductsRequest.pb(
            private_catalog.SearchProductsRequest()
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
        req.return_value._content = private_catalog.SearchProductsResponse.to_json(
            private_catalog.SearchProductsResponse()
        )

        request = private_catalog.SearchProductsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = private_catalog.SearchProductsResponse()

        client.search_products(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_search_products_rest_bad_request(
    transport: str = "rest", request_type=private_catalog.SearchProductsRequest
):
    client = PrivateCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"resource": "projects/sample1"}
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
        client.search_products(request)


def test_search_products_rest_pager(transport: str = "rest"):
    client = PrivateCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            private_catalog.SearchProductsResponse(
                products=[
                    private_catalog.Product(),
                    private_catalog.Product(),
                    private_catalog.Product(),
                ],
                next_page_token="abc",
            ),
            private_catalog.SearchProductsResponse(
                products=[],
                next_page_token="def",
            ),
            private_catalog.SearchProductsResponse(
                products=[
                    private_catalog.Product(),
                ],
                next_page_token="ghi",
            ),
            private_catalog.SearchProductsResponse(
                products=[
                    private_catalog.Product(),
                    private_catalog.Product(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            private_catalog.SearchProductsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"resource": "projects/sample1"}

        pager = client.search_products(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, private_catalog.Product) for i in results)

        pages = list(client.search_products(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        private_catalog.SearchVersionsRequest,
        dict,
    ],
)
def test_search_versions_rest(request_type):
    client = PrivateCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"resource": "projects/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = private_catalog.SearchVersionsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = private_catalog.SearchVersionsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.search_versions(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchVersionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_search_versions_rest_required_fields(
    request_type=private_catalog.SearchVersionsRequest,
):
    transport_class = transports.PrivateCatalogRestTransport

    request_init = {}
    request_init["resource"] = ""
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
    ).search_versions._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "query" in jsonified_request
    assert jsonified_request["query"] == request_init["query"]

    jsonified_request["resource"] = "resource_value"
    jsonified_request["query"] = "query_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).search_versions._get_unset_required_fields(jsonified_request)
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
    assert "resource" in jsonified_request
    assert jsonified_request["resource"] == "resource_value"
    assert "query" in jsonified_request
    assert jsonified_request["query"] == "query_value"

    client = PrivateCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = private_catalog.SearchVersionsResponse()
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

            pb_return_value = private_catalog.SearchVersionsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.search_versions(request)

            expected_params = [
                (
                    "query",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_search_versions_rest_unset_required_fields():
    transport = transports.PrivateCatalogRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.search_versions._get_unset_required_fields({})
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
                "resource",
                "query",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_search_versions_rest_interceptors(null_interceptor):
    transport = transports.PrivateCatalogRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.PrivateCatalogRestInterceptor(),
    )
    client = PrivateCatalogClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.PrivateCatalogRestInterceptor, "post_search_versions"
    ) as post, mock.patch.object(
        transports.PrivateCatalogRestInterceptor, "pre_search_versions"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = private_catalog.SearchVersionsRequest.pb(
            private_catalog.SearchVersionsRequest()
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
        req.return_value._content = private_catalog.SearchVersionsResponse.to_json(
            private_catalog.SearchVersionsResponse()
        )

        request = private_catalog.SearchVersionsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = private_catalog.SearchVersionsResponse()

        client.search_versions(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_search_versions_rest_bad_request(
    transport: str = "rest", request_type=private_catalog.SearchVersionsRequest
):
    client = PrivateCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"resource": "projects/sample1"}
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
        client.search_versions(request)


def test_search_versions_rest_pager(transport: str = "rest"):
    client = PrivateCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            private_catalog.SearchVersionsResponse(
                versions=[
                    private_catalog.Version(),
                    private_catalog.Version(),
                    private_catalog.Version(),
                ],
                next_page_token="abc",
            ),
            private_catalog.SearchVersionsResponse(
                versions=[],
                next_page_token="def",
            ),
            private_catalog.SearchVersionsResponse(
                versions=[
                    private_catalog.Version(),
                ],
                next_page_token="ghi",
            ),
            private_catalog.SearchVersionsResponse(
                versions=[
                    private_catalog.Version(),
                    private_catalog.Version(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            private_catalog.SearchVersionsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"resource": "projects/sample1"}

        pager = client.search_versions(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, private_catalog.Version) for i in results)

        pages = list(client.search_versions(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.PrivateCatalogGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = PrivateCatalogClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.PrivateCatalogGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = PrivateCatalogClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.PrivateCatalogGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = PrivateCatalogClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = PrivateCatalogClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.PrivateCatalogGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = PrivateCatalogClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.PrivateCatalogGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = PrivateCatalogClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.PrivateCatalogGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.PrivateCatalogGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.PrivateCatalogGrpcTransport,
        transports.PrivateCatalogGrpcAsyncIOTransport,
        transports.PrivateCatalogRestTransport,
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
    transport = PrivateCatalogClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = PrivateCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.PrivateCatalogGrpcTransport,
    )


def test_private_catalog_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.PrivateCatalogTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_private_catalog_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.privatecatalog_v1beta1.services.private_catalog.transports.PrivateCatalogTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.PrivateCatalogTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "search_catalogs",
        "search_products",
        "search_versions",
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


def test_private_catalog_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.privatecatalog_v1beta1.services.private_catalog.transports.PrivateCatalogTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.PrivateCatalogTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_private_catalog_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.privatecatalog_v1beta1.services.private_catalog.transports.PrivateCatalogTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.PrivateCatalogTransport()
        adc.assert_called_once()


def test_private_catalog_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        PrivateCatalogClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.PrivateCatalogGrpcTransport,
        transports.PrivateCatalogGrpcAsyncIOTransport,
    ],
)
def test_private_catalog_transport_auth_adc(transport_class):
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
        transports.PrivateCatalogGrpcTransport,
        transports.PrivateCatalogGrpcAsyncIOTransport,
        transports.PrivateCatalogRestTransport,
    ],
)
def test_private_catalog_transport_auth_gdch_credentials(transport_class):
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
        (transports.PrivateCatalogGrpcTransport, grpc_helpers),
        (transports.PrivateCatalogGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_private_catalog_transport_create_channel(transport_class, grpc_helpers):
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
            "cloudprivatecatalog.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="cloudprivatecatalog.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.PrivateCatalogGrpcTransport,
        transports.PrivateCatalogGrpcAsyncIOTransport,
    ],
)
def test_private_catalog_grpc_transport_client_cert_source_for_mtls(transport_class):
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


def test_private_catalog_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.PrivateCatalogRestTransport(
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
def test_private_catalog_host_no_port(transport_name):
    client = PrivateCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="cloudprivatecatalog.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "cloudprivatecatalog.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://cloudprivatecatalog.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_private_catalog_host_with_port(transport_name):
    client = PrivateCatalogClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="cloudprivatecatalog.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "cloudprivatecatalog.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://cloudprivatecatalog.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_private_catalog_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = PrivateCatalogClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = PrivateCatalogClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.search_catalogs._session
    session2 = client2.transport.search_catalogs._session
    assert session1 != session2
    session1 = client1.transport.search_products._session
    session2 = client2.transport.search_products._session
    assert session1 != session2
    session1 = client1.transport.search_versions._session
    session2 = client2.transport.search_versions._session
    assert session1 != session2


def test_private_catalog_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.PrivateCatalogGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_private_catalog_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.PrivateCatalogGrpcAsyncIOTransport(
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
        transports.PrivateCatalogGrpcTransport,
        transports.PrivateCatalogGrpcAsyncIOTransport,
    ],
)
def test_private_catalog_transport_channel_mtls_with_client_cert_source(
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
        transports.PrivateCatalogGrpcTransport,
        transports.PrivateCatalogGrpcAsyncIOTransport,
    ],
)
def test_private_catalog_transport_channel_mtls_with_adc(transport_class):
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


def test_catalog_path():
    catalog = "squid"
    expected = "catalogs/{catalog}".format(
        catalog=catalog,
    )
    actual = PrivateCatalogClient.catalog_path(catalog)
    assert expected == actual


def test_parse_catalog_path():
    expected = {
        "catalog": "clam",
    }
    path = PrivateCatalogClient.catalog_path(**expected)

    # Check that the path construction is reversible.
    actual = PrivateCatalogClient.parse_catalog_path(path)
    assert expected == actual


def test_product_path():
    product = "whelk"
    expected = "products/{product}".format(
        product=product,
    )
    actual = PrivateCatalogClient.product_path(product)
    assert expected == actual


def test_parse_product_path():
    expected = {
        "product": "octopus",
    }
    path = PrivateCatalogClient.product_path(**expected)

    # Check that the path construction is reversible.
    actual = PrivateCatalogClient.parse_product_path(path)
    assert expected == actual


def test_version_path():
    catalog = "oyster"
    product = "nudibranch"
    version = "cuttlefish"
    expected = "catalogs/{catalog}/products/{product}/versions/{version}".format(
        catalog=catalog,
        product=product,
        version=version,
    )
    actual = PrivateCatalogClient.version_path(catalog, product, version)
    assert expected == actual


def test_parse_version_path():
    expected = {
        "catalog": "mussel",
        "product": "winkle",
        "version": "nautilus",
    }
    path = PrivateCatalogClient.version_path(**expected)

    # Check that the path construction is reversible.
    actual = PrivateCatalogClient.parse_version_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "scallop"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = PrivateCatalogClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "abalone",
    }
    path = PrivateCatalogClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = PrivateCatalogClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "squid"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = PrivateCatalogClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "clam",
    }
    path = PrivateCatalogClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = PrivateCatalogClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "whelk"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = PrivateCatalogClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "octopus",
    }
    path = PrivateCatalogClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = PrivateCatalogClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "oyster"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = PrivateCatalogClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nudibranch",
    }
    path = PrivateCatalogClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = PrivateCatalogClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "cuttlefish"
    location = "mussel"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = PrivateCatalogClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "winkle",
        "location": "nautilus",
    }
    path = PrivateCatalogClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = PrivateCatalogClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.PrivateCatalogTransport, "_prep_wrapped_messages"
    ) as prep:
        client = PrivateCatalogClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.PrivateCatalogTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = PrivateCatalogClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = PrivateCatalogAsyncClient(
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
        client = PrivateCatalogClient(
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
        client = PrivateCatalogClient(
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
        (PrivateCatalogClient, transports.PrivateCatalogGrpcTransport),
        (PrivateCatalogAsyncClient, transports.PrivateCatalogGrpcAsyncIOTransport),
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
