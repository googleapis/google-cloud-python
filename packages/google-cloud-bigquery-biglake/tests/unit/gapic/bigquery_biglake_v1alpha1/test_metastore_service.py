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

from google.cloud.bigquery_biglake_v1alpha1.services.metastore_service import (
    MetastoreServiceAsyncClient,
    MetastoreServiceClient,
    pagers,
    transports,
)
from google.cloud.bigquery_biglake_v1alpha1.types import metastore


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

    assert MetastoreServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        MetastoreServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        MetastoreServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        MetastoreServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        MetastoreServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        MetastoreServiceClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (MetastoreServiceClient, "grpc"),
        (MetastoreServiceAsyncClient, "grpc_asyncio"),
        (MetastoreServiceClient, "rest"),
    ],
)
def test_metastore_service_client_from_service_account_info(
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
            "biglake.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://biglake.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.MetastoreServiceGrpcTransport, "grpc"),
        (transports.MetastoreServiceGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.MetastoreServiceRestTransport, "rest"),
    ],
)
def test_metastore_service_client_service_account_always_use_jwt(
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
        (MetastoreServiceClient, "grpc"),
        (MetastoreServiceAsyncClient, "grpc_asyncio"),
        (MetastoreServiceClient, "rest"),
    ],
)
def test_metastore_service_client_from_service_account_file(
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
            "biglake.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://biglake.googleapis.com"
        )


def test_metastore_service_client_get_transport_class():
    transport = MetastoreServiceClient.get_transport_class()
    available_transports = [
        transports.MetastoreServiceGrpcTransport,
        transports.MetastoreServiceRestTransport,
    ]
    assert transport in available_transports

    transport = MetastoreServiceClient.get_transport_class("grpc")
    assert transport == transports.MetastoreServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (MetastoreServiceClient, transports.MetastoreServiceGrpcTransport, "grpc"),
        (
            MetastoreServiceAsyncClient,
            transports.MetastoreServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (MetastoreServiceClient, transports.MetastoreServiceRestTransport, "rest"),
    ],
)
@mock.patch.object(
    MetastoreServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(MetastoreServiceClient),
)
@mock.patch.object(
    MetastoreServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(MetastoreServiceAsyncClient),
)
def test_metastore_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(MetastoreServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(MetastoreServiceClient, "get_transport_class") as gtc:
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
            MetastoreServiceClient,
            transports.MetastoreServiceGrpcTransport,
            "grpc",
            "true",
        ),
        (
            MetastoreServiceAsyncClient,
            transports.MetastoreServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            MetastoreServiceClient,
            transports.MetastoreServiceGrpcTransport,
            "grpc",
            "false",
        ),
        (
            MetastoreServiceAsyncClient,
            transports.MetastoreServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (
            MetastoreServiceClient,
            transports.MetastoreServiceRestTransport,
            "rest",
            "true",
        ),
        (
            MetastoreServiceClient,
            transports.MetastoreServiceRestTransport,
            "rest",
            "false",
        ),
    ],
)
@mock.patch.object(
    MetastoreServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(MetastoreServiceClient),
)
@mock.patch.object(
    MetastoreServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(MetastoreServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_metastore_service_client_mtls_env_auto(
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
    "client_class", [MetastoreServiceClient, MetastoreServiceAsyncClient]
)
@mock.patch.object(
    MetastoreServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(MetastoreServiceClient),
)
@mock.patch.object(
    MetastoreServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(MetastoreServiceAsyncClient),
)
def test_metastore_service_client_get_mtls_endpoint_and_cert_source(client_class):
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
        (MetastoreServiceClient, transports.MetastoreServiceGrpcTransport, "grpc"),
        (
            MetastoreServiceAsyncClient,
            transports.MetastoreServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (MetastoreServiceClient, transports.MetastoreServiceRestTransport, "rest"),
    ],
)
def test_metastore_service_client_client_options_scopes(
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
            MetastoreServiceClient,
            transports.MetastoreServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            MetastoreServiceAsyncClient,
            transports.MetastoreServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (
            MetastoreServiceClient,
            transports.MetastoreServiceRestTransport,
            "rest",
            None,
        ),
    ],
)
def test_metastore_service_client_client_options_credentials_file(
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


def test_metastore_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.bigquery_biglake_v1alpha1.services.metastore_service.transports.MetastoreServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = MetastoreServiceClient(
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
            MetastoreServiceClient,
            transports.MetastoreServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            MetastoreServiceAsyncClient,
            transports.MetastoreServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_metastore_service_client_create_channel_credentials_file(
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
            "biglake.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=(
                "https://www.googleapis.com/auth/bigquery",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            scopes=None,
            default_host="biglake.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.CreateCatalogRequest,
        dict,
    ],
)
def test_create_catalog(request_type, transport: str = "grpc"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_catalog), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Catalog(
            name="name_value",
        )
        response = client.create_catalog(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.CreateCatalogRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Catalog)
    assert response.name == "name_value"


def test_create_catalog_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_catalog), "__call__") as call:
        client.create_catalog()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.CreateCatalogRequest()


@pytest.mark.asyncio
async def test_create_catalog_async(
    transport: str = "grpc_asyncio", request_type=metastore.CreateCatalogRequest
):
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_catalog), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.Catalog(
                name="name_value",
            )
        )
        response = await client.create_catalog(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.CreateCatalogRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Catalog)
    assert response.name == "name_value"


@pytest.mark.asyncio
async def test_create_catalog_async_from_dict():
    await test_create_catalog_async(request_type=dict)


def test_create_catalog_field_headers():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.CreateCatalogRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_catalog), "__call__") as call:
        call.return_value = metastore.Catalog()
        client.create_catalog(request)

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
async def test_create_catalog_field_headers_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.CreateCatalogRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_catalog), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore.Catalog())
        await client.create_catalog(request)

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


def test_create_catalog_flattened():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_catalog), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Catalog()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_catalog(
            parent="parent_value",
            catalog=metastore.Catalog(name="name_value"),
            catalog_id="catalog_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].catalog
        mock_val = metastore.Catalog(name="name_value")
        assert arg == mock_val
        arg = args[0].catalog_id
        mock_val = "catalog_id_value"
        assert arg == mock_val


def test_create_catalog_flattened_error():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_catalog(
            metastore.CreateCatalogRequest(),
            parent="parent_value",
            catalog=metastore.Catalog(name="name_value"),
            catalog_id="catalog_id_value",
        )


@pytest.mark.asyncio
async def test_create_catalog_flattened_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_catalog), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Catalog()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore.Catalog())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_catalog(
            parent="parent_value",
            catalog=metastore.Catalog(name="name_value"),
            catalog_id="catalog_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].catalog
        mock_val = metastore.Catalog(name="name_value")
        assert arg == mock_val
        arg = args[0].catalog_id
        mock_val = "catalog_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_catalog_flattened_error_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_catalog(
            metastore.CreateCatalogRequest(),
            parent="parent_value",
            catalog=metastore.Catalog(name="name_value"),
            catalog_id="catalog_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.DeleteCatalogRequest,
        dict,
    ],
)
def test_delete_catalog(request_type, transport: str = "grpc"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_catalog), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Catalog(
            name="name_value",
        )
        response = client.delete_catalog(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.DeleteCatalogRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Catalog)
    assert response.name == "name_value"


def test_delete_catalog_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_catalog), "__call__") as call:
        client.delete_catalog()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.DeleteCatalogRequest()


@pytest.mark.asyncio
async def test_delete_catalog_async(
    transport: str = "grpc_asyncio", request_type=metastore.DeleteCatalogRequest
):
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_catalog), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.Catalog(
                name="name_value",
            )
        )
        response = await client.delete_catalog(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.DeleteCatalogRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Catalog)
    assert response.name == "name_value"


@pytest.mark.asyncio
async def test_delete_catalog_async_from_dict():
    await test_delete_catalog_async(request_type=dict)


def test_delete_catalog_field_headers():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.DeleteCatalogRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_catalog), "__call__") as call:
        call.return_value = metastore.Catalog()
        client.delete_catalog(request)

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
async def test_delete_catalog_field_headers_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.DeleteCatalogRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_catalog), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore.Catalog())
        await client.delete_catalog(request)

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


def test_delete_catalog_flattened():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_catalog), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Catalog()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_catalog(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_catalog_flattened_error():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_catalog(
            metastore.DeleteCatalogRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_catalog_flattened_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_catalog), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Catalog()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore.Catalog())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_catalog(
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
async def test_delete_catalog_flattened_error_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_catalog(
            metastore.DeleteCatalogRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.GetCatalogRequest,
        dict,
    ],
)
def test_get_catalog(request_type, transport: str = "grpc"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_catalog), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Catalog(
            name="name_value",
        )
        response = client.get_catalog(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.GetCatalogRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Catalog)
    assert response.name == "name_value"


def test_get_catalog_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_catalog), "__call__") as call:
        client.get_catalog()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.GetCatalogRequest()


@pytest.mark.asyncio
async def test_get_catalog_async(
    transport: str = "grpc_asyncio", request_type=metastore.GetCatalogRequest
):
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_catalog), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.Catalog(
                name="name_value",
            )
        )
        response = await client.get_catalog(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.GetCatalogRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Catalog)
    assert response.name == "name_value"


@pytest.mark.asyncio
async def test_get_catalog_async_from_dict():
    await test_get_catalog_async(request_type=dict)


def test_get_catalog_field_headers():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.GetCatalogRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_catalog), "__call__") as call:
        call.return_value = metastore.Catalog()
        client.get_catalog(request)

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
async def test_get_catalog_field_headers_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.GetCatalogRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_catalog), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore.Catalog())
        await client.get_catalog(request)

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


def test_get_catalog_flattened():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_catalog), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Catalog()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_catalog(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_catalog_flattened_error():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_catalog(
            metastore.GetCatalogRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_catalog_flattened_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_catalog), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Catalog()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore.Catalog())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_catalog(
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
async def test_get_catalog_flattened_error_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_catalog(
            metastore.GetCatalogRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.ListCatalogsRequest,
        dict,
    ],
)
def test_list_catalogs(request_type, transport: str = "grpc"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_catalogs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.ListCatalogsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_catalogs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.ListCatalogsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCatalogsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_catalogs_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_catalogs), "__call__") as call:
        client.list_catalogs()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.ListCatalogsRequest()


@pytest.mark.asyncio
async def test_list_catalogs_async(
    transport: str = "grpc_asyncio", request_type=metastore.ListCatalogsRequest
):
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_catalogs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.ListCatalogsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_catalogs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.ListCatalogsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCatalogsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_catalogs_async_from_dict():
    await test_list_catalogs_async(request_type=dict)


def test_list_catalogs_field_headers():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.ListCatalogsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_catalogs), "__call__") as call:
        call.return_value = metastore.ListCatalogsResponse()
        client.list_catalogs(request)

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
async def test_list_catalogs_field_headers_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.ListCatalogsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_catalogs), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.ListCatalogsResponse()
        )
        await client.list_catalogs(request)

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


def test_list_catalogs_flattened():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_catalogs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.ListCatalogsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_catalogs(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_catalogs_flattened_error():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_catalogs(
            metastore.ListCatalogsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_catalogs_flattened_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_catalogs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.ListCatalogsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.ListCatalogsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_catalogs(
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
async def test_list_catalogs_flattened_error_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_catalogs(
            metastore.ListCatalogsRequest(),
            parent="parent_value",
        )


def test_list_catalogs_pager(transport_name: str = "grpc"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_catalogs), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListCatalogsResponse(
                catalogs=[
                    metastore.Catalog(),
                    metastore.Catalog(),
                    metastore.Catalog(),
                ],
                next_page_token="abc",
            ),
            metastore.ListCatalogsResponse(
                catalogs=[],
                next_page_token="def",
            ),
            metastore.ListCatalogsResponse(
                catalogs=[
                    metastore.Catalog(),
                ],
                next_page_token="ghi",
            ),
            metastore.ListCatalogsResponse(
                catalogs=[
                    metastore.Catalog(),
                    metastore.Catalog(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_catalogs(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, metastore.Catalog) for i in results)


def test_list_catalogs_pages(transport_name: str = "grpc"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_catalogs), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListCatalogsResponse(
                catalogs=[
                    metastore.Catalog(),
                    metastore.Catalog(),
                    metastore.Catalog(),
                ],
                next_page_token="abc",
            ),
            metastore.ListCatalogsResponse(
                catalogs=[],
                next_page_token="def",
            ),
            metastore.ListCatalogsResponse(
                catalogs=[
                    metastore.Catalog(),
                ],
                next_page_token="ghi",
            ),
            metastore.ListCatalogsResponse(
                catalogs=[
                    metastore.Catalog(),
                    metastore.Catalog(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_catalogs(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_catalogs_async_pager():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_catalogs), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListCatalogsResponse(
                catalogs=[
                    metastore.Catalog(),
                    metastore.Catalog(),
                    metastore.Catalog(),
                ],
                next_page_token="abc",
            ),
            metastore.ListCatalogsResponse(
                catalogs=[],
                next_page_token="def",
            ),
            metastore.ListCatalogsResponse(
                catalogs=[
                    metastore.Catalog(),
                ],
                next_page_token="ghi",
            ),
            metastore.ListCatalogsResponse(
                catalogs=[
                    metastore.Catalog(),
                    metastore.Catalog(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_catalogs(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, metastore.Catalog) for i in responses)


@pytest.mark.asyncio
async def test_list_catalogs_async_pages():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_catalogs), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListCatalogsResponse(
                catalogs=[
                    metastore.Catalog(),
                    metastore.Catalog(),
                    metastore.Catalog(),
                ],
                next_page_token="abc",
            ),
            metastore.ListCatalogsResponse(
                catalogs=[],
                next_page_token="def",
            ),
            metastore.ListCatalogsResponse(
                catalogs=[
                    metastore.Catalog(),
                ],
                next_page_token="ghi",
            ),
            metastore.ListCatalogsResponse(
                catalogs=[
                    metastore.Catalog(),
                    metastore.Catalog(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_catalogs(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.CreateDatabaseRequest,
        dict,
    ],
)
def test_create_database(request_type, transport: str = "grpc"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_database), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Database(
            name="name_value",
            type_=metastore.Database.Type.HIVE,
        )
        response = client.create_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.CreateDatabaseRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Database)
    assert response.name == "name_value"
    assert response.type_ == metastore.Database.Type.HIVE


def test_create_database_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_database), "__call__") as call:
        client.create_database()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.CreateDatabaseRequest()


@pytest.mark.asyncio
async def test_create_database_async(
    transport: str = "grpc_asyncio", request_type=metastore.CreateDatabaseRequest
):
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_database), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.Database(
                name="name_value",
                type_=metastore.Database.Type.HIVE,
            )
        )
        response = await client.create_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.CreateDatabaseRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Database)
    assert response.name == "name_value"
    assert response.type_ == metastore.Database.Type.HIVE


@pytest.mark.asyncio
async def test_create_database_async_from_dict():
    await test_create_database_async(request_type=dict)


def test_create_database_field_headers():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.CreateDatabaseRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_database), "__call__") as call:
        call.return_value = metastore.Database()
        client.create_database(request)

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
async def test_create_database_field_headers_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.CreateDatabaseRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_database), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore.Database())
        await client.create_database(request)

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


def test_create_database_flattened():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_database), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Database()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_database(
            parent="parent_value",
            database=metastore.Database(
                hive_options=metastore.HiveDatabaseOptions(
                    location_uri="location_uri_value"
                )
            ),
            database_id="database_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].database
        mock_val = metastore.Database(
            hive_options=metastore.HiveDatabaseOptions(
                location_uri="location_uri_value"
            )
        )
        assert arg == mock_val
        arg = args[0].database_id
        mock_val = "database_id_value"
        assert arg == mock_val


def test_create_database_flattened_error():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_database(
            metastore.CreateDatabaseRequest(),
            parent="parent_value",
            database=metastore.Database(
                hive_options=metastore.HiveDatabaseOptions(
                    location_uri="location_uri_value"
                )
            ),
            database_id="database_id_value",
        )


@pytest.mark.asyncio
async def test_create_database_flattened_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_database), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Database()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore.Database())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_database(
            parent="parent_value",
            database=metastore.Database(
                hive_options=metastore.HiveDatabaseOptions(
                    location_uri="location_uri_value"
                )
            ),
            database_id="database_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].database
        mock_val = metastore.Database(
            hive_options=metastore.HiveDatabaseOptions(
                location_uri="location_uri_value"
            )
        )
        assert arg == mock_val
        arg = args[0].database_id
        mock_val = "database_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_database_flattened_error_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_database(
            metastore.CreateDatabaseRequest(),
            parent="parent_value",
            database=metastore.Database(
                hive_options=metastore.HiveDatabaseOptions(
                    location_uri="location_uri_value"
                )
            ),
            database_id="database_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.DeleteDatabaseRequest,
        dict,
    ],
)
def test_delete_database(request_type, transport: str = "grpc"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_database), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Database(
            name="name_value",
            type_=metastore.Database.Type.HIVE,
        )
        response = client.delete_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.DeleteDatabaseRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Database)
    assert response.name == "name_value"
    assert response.type_ == metastore.Database.Type.HIVE


def test_delete_database_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_database), "__call__") as call:
        client.delete_database()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.DeleteDatabaseRequest()


@pytest.mark.asyncio
async def test_delete_database_async(
    transport: str = "grpc_asyncio", request_type=metastore.DeleteDatabaseRequest
):
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_database), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.Database(
                name="name_value",
                type_=metastore.Database.Type.HIVE,
            )
        )
        response = await client.delete_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.DeleteDatabaseRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Database)
    assert response.name == "name_value"
    assert response.type_ == metastore.Database.Type.HIVE


@pytest.mark.asyncio
async def test_delete_database_async_from_dict():
    await test_delete_database_async(request_type=dict)


def test_delete_database_field_headers():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.DeleteDatabaseRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_database), "__call__") as call:
        call.return_value = metastore.Database()
        client.delete_database(request)

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
async def test_delete_database_field_headers_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.DeleteDatabaseRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_database), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore.Database())
        await client.delete_database(request)

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


def test_delete_database_flattened():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_database), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Database()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_database(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_database_flattened_error():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_database(
            metastore.DeleteDatabaseRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_database_flattened_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_database), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Database()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore.Database())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_database(
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
async def test_delete_database_flattened_error_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_database(
            metastore.DeleteDatabaseRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.UpdateDatabaseRequest,
        dict,
    ],
)
def test_update_database(request_type, transport: str = "grpc"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_database), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Database(
            name="name_value",
            type_=metastore.Database.Type.HIVE,
        )
        response = client.update_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.UpdateDatabaseRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Database)
    assert response.name == "name_value"
    assert response.type_ == metastore.Database.Type.HIVE


def test_update_database_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_database), "__call__") as call:
        client.update_database()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.UpdateDatabaseRequest()


@pytest.mark.asyncio
async def test_update_database_async(
    transport: str = "grpc_asyncio", request_type=metastore.UpdateDatabaseRequest
):
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_database), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.Database(
                name="name_value",
                type_=metastore.Database.Type.HIVE,
            )
        )
        response = await client.update_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.UpdateDatabaseRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Database)
    assert response.name == "name_value"
    assert response.type_ == metastore.Database.Type.HIVE


@pytest.mark.asyncio
async def test_update_database_async_from_dict():
    await test_update_database_async(request_type=dict)


def test_update_database_field_headers():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.UpdateDatabaseRequest()

    request.database.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_database), "__call__") as call:
        call.return_value = metastore.Database()
        client.update_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "database.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_database_field_headers_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.UpdateDatabaseRequest()

    request.database.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_database), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore.Database())
        await client.update_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "database.name=name_value",
    ) in kw["metadata"]


def test_update_database_flattened():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_database), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Database()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_database(
            database=metastore.Database(
                hive_options=metastore.HiveDatabaseOptions(
                    location_uri="location_uri_value"
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].database
        mock_val = metastore.Database(
            hive_options=metastore.HiveDatabaseOptions(
                location_uri="location_uri_value"
            )
        )
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_database_flattened_error():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_database(
            metastore.UpdateDatabaseRequest(),
            database=metastore.Database(
                hive_options=metastore.HiveDatabaseOptions(
                    location_uri="location_uri_value"
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_database_flattened_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_database), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Database()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore.Database())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_database(
            database=metastore.Database(
                hive_options=metastore.HiveDatabaseOptions(
                    location_uri="location_uri_value"
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].database
        mock_val = metastore.Database(
            hive_options=metastore.HiveDatabaseOptions(
                location_uri="location_uri_value"
            )
        )
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_database_flattened_error_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_database(
            metastore.UpdateDatabaseRequest(),
            database=metastore.Database(
                hive_options=metastore.HiveDatabaseOptions(
                    location_uri="location_uri_value"
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.GetDatabaseRequest,
        dict,
    ],
)
def test_get_database(request_type, transport: str = "grpc"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_database), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Database(
            name="name_value",
            type_=metastore.Database.Type.HIVE,
        )
        response = client.get_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.GetDatabaseRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Database)
    assert response.name == "name_value"
    assert response.type_ == metastore.Database.Type.HIVE


def test_get_database_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_database), "__call__") as call:
        client.get_database()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.GetDatabaseRequest()


@pytest.mark.asyncio
async def test_get_database_async(
    transport: str = "grpc_asyncio", request_type=metastore.GetDatabaseRequest
):
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_database), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.Database(
                name="name_value",
                type_=metastore.Database.Type.HIVE,
            )
        )
        response = await client.get_database(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.GetDatabaseRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Database)
    assert response.name == "name_value"
    assert response.type_ == metastore.Database.Type.HIVE


@pytest.mark.asyncio
async def test_get_database_async_from_dict():
    await test_get_database_async(request_type=dict)


def test_get_database_field_headers():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.GetDatabaseRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_database), "__call__") as call:
        call.return_value = metastore.Database()
        client.get_database(request)

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
async def test_get_database_field_headers_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.GetDatabaseRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_database), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore.Database())
        await client.get_database(request)

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


def test_get_database_flattened():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_database), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Database()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_database(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_database_flattened_error():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_database(
            metastore.GetDatabaseRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_database_flattened_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_database), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Database()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore.Database())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_database(
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
async def test_get_database_flattened_error_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_database(
            metastore.GetDatabaseRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.ListDatabasesRequest,
        dict,
    ],
)
def test_list_databases(request_type, transport: str = "grpc"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_databases), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.ListDatabasesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_databases(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.ListDatabasesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDatabasesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_databases_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_databases), "__call__") as call:
        client.list_databases()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.ListDatabasesRequest()


@pytest.mark.asyncio
async def test_list_databases_async(
    transport: str = "grpc_asyncio", request_type=metastore.ListDatabasesRequest
):
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_databases), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.ListDatabasesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_databases(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.ListDatabasesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDatabasesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_databases_async_from_dict():
    await test_list_databases_async(request_type=dict)


def test_list_databases_field_headers():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.ListDatabasesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_databases), "__call__") as call:
        call.return_value = metastore.ListDatabasesResponse()
        client.list_databases(request)

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
async def test_list_databases_field_headers_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.ListDatabasesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_databases), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.ListDatabasesResponse()
        )
        await client.list_databases(request)

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


def test_list_databases_flattened():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_databases), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.ListDatabasesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_databases(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_databases_flattened_error():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_databases(
            metastore.ListDatabasesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_databases_flattened_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_databases), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.ListDatabasesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.ListDatabasesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_databases(
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
async def test_list_databases_flattened_error_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_databases(
            metastore.ListDatabasesRequest(),
            parent="parent_value",
        )


def test_list_databases_pager(transport_name: str = "grpc"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_databases), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListDatabasesResponse(
                databases=[
                    metastore.Database(),
                    metastore.Database(),
                    metastore.Database(),
                ],
                next_page_token="abc",
            ),
            metastore.ListDatabasesResponse(
                databases=[],
                next_page_token="def",
            ),
            metastore.ListDatabasesResponse(
                databases=[
                    metastore.Database(),
                ],
                next_page_token="ghi",
            ),
            metastore.ListDatabasesResponse(
                databases=[
                    metastore.Database(),
                    metastore.Database(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_databases(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, metastore.Database) for i in results)


def test_list_databases_pages(transport_name: str = "grpc"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_databases), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListDatabasesResponse(
                databases=[
                    metastore.Database(),
                    metastore.Database(),
                    metastore.Database(),
                ],
                next_page_token="abc",
            ),
            metastore.ListDatabasesResponse(
                databases=[],
                next_page_token="def",
            ),
            metastore.ListDatabasesResponse(
                databases=[
                    metastore.Database(),
                ],
                next_page_token="ghi",
            ),
            metastore.ListDatabasesResponse(
                databases=[
                    metastore.Database(),
                    metastore.Database(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_databases(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_databases_async_pager():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_databases), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListDatabasesResponse(
                databases=[
                    metastore.Database(),
                    metastore.Database(),
                    metastore.Database(),
                ],
                next_page_token="abc",
            ),
            metastore.ListDatabasesResponse(
                databases=[],
                next_page_token="def",
            ),
            metastore.ListDatabasesResponse(
                databases=[
                    metastore.Database(),
                ],
                next_page_token="ghi",
            ),
            metastore.ListDatabasesResponse(
                databases=[
                    metastore.Database(),
                    metastore.Database(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_databases(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, metastore.Database) for i in responses)


@pytest.mark.asyncio
async def test_list_databases_async_pages():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_databases), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListDatabasesResponse(
                databases=[
                    metastore.Database(),
                    metastore.Database(),
                    metastore.Database(),
                ],
                next_page_token="abc",
            ),
            metastore.ListDatabasesResponse(
                databases=[],
                next_page_token="def",
            ),
            metastore.ListDatabasesResponse(
                databases=[
                    metastore.Database(),
                ],
                next_page_token="ghi",
            ),
            metastore.ListDatabasesResponse(
                databases=[
                    metastore.Database(),
                    metastore.Database(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_databases(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.CreateTableRequest,
        dict,
    ],
)
def test_create_table(request_type, transport: str = "grpc"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_table), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Table(
            name="name_value",
            type_=metastore.Table.Type.HIVE,
            etag="etag_value",
        )
        response = client.create_table(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.CreateTableRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Table)
    assert response.name == "name_value"
    assert response.type_ == metastore.Table.Type.HIVE
    assert response.etag == "etag_value"


def test_create_table_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_table), "__call__") as call:
        client.create_table()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.CreateTableRequest()


@pytest.mark.asyncio
async def test_create_table_async(
    transport: str = "grpc_asyncio", request_type=metastore.CreateTableRequest
):
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_table), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.Table(
                name="name_value",
                type_=metastore.Table.Type.HIVE,
                etag="etag_value",
            )
        )
        response = await client.create_table(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.CreateTableRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Table)
    assert response.name == "name_value"
    assert response.type_ == metastore.Table.Type.HIVE
    assert response.etag == "etag_value"


@pytest.mark.asyncio
async def test_create_table_async_from_dict():
    await test_create_table_async(request_type=dict)


def test_create_table_field_headers():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.CreateTableRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_table), "__call__") as call:
        call.return_value = metastore.Table()
        client.create_table(request)

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
async def test_create_table_field_headers_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.CreateTableRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_table), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore.Table())
        await client.create_table(request)

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


def test_create_table_flattened():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_table), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Table()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_table(
            parent="parent_value",
            table=metastore.Table(
                hive_options=metastore.HiveTableOptions(
                    parameters={"key_value": "value_value"}
                )
            ),
            table_id="table_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].table
        mock_val = metastore.Table(
            hive_options=metastore.HiveTableOptions(
                parameters={"key_value": "value_value"}
            )
        )
        assert arg == mock_val
        arg = args[0].table_id
        mock_val = "table_id_value"
        assert arg == mock_val


def test_create_table_flattened_error():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_table(
            metastore.CreateTableRequest(),
            parent="parent_value",
            table=metastore.Table(
                hive_options=metastore.HiveTableOptions(
                    parameters={"key_value": "value_value"}
                )
            ),
            table_id="table_id_value",
        )


@pytest.mark.asyncio
async def test_create_table_flattened_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_table), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Table()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore.Table())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_table(
            parent="parent_value",
            table=metastore.Table(
                hive_options=metastore.HiveTableOptions(
                    parameters={"key_value": "value_value"}
                )
            ),
            table_id="table_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].table
        mock_val = metastore.Table(
            hive_options=metastore.HiveTableOptions(
                parameters={"key_value": "value_value"}
            )
        )
        assert arg == mock_val
        arg = args[0].table_id
        mock_val = "table_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_table_flattened_error_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_table(
            metastore.CreateTableRequest(),
            parent="parent_value",
            table=metastore.Table(
                hive_options=metastore.HiveTableOptions(
                    parameters={"key_value": "value_value"}
                )
            ),
            table_id="table_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.DeleteTableRequest,
        dict,
    ],
)
def test_delete_table(request_type, transport: str = "grpc"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_table), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Table(
            name="name_value",
            type_=metastore.Table.Type.HIVE,
            etag="etag_value",
        )
        response = client.delete_table(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.DeleteTableRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Table)
    assert response.name == "name_value"
    assert response.type_ == metastore.Table.Type.HIVE
    assert response.etag == "etag_value"


def test_delete_table_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_table), "__call__") as call:
        client.delete_table()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.DeleteTableRequest()


@pytest.mark.asyncio
async def test_delete_table_async(
    transport: str = "grpc_asyncio", request_type=metastore.DeleteTableRequest
):
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_table), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.Table(
                name="name_value",
                type_=metastore.Table.Type.HIVE,
                etag="etag_value",
            )
        )
        response = await client.delete_table(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.DeleteTableRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Table)
    assert response.name == "name_value"
    assert response.type_ == metastore.Table.Type.HIVE
    assert response.etag == "etag_value"


@pytest.mark.asyncio
async def test_delete_table_async_from_dict():
    await test_delete_table_async(request_type=dict)


def test_delete_table_field_headers():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.DeleteTableRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_table), "__call__") as call:
        call.return_value = metastore.Table()
        client.delete_table(request)

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
async def test_delete_table_field_headers_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.DeleteTableRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_table), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore.Table())
        await client.delete_table(request)

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


def test_delete_table_flattened():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_table), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Table()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_table(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_table_flattened_error():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_table(
            metastore.DeleteTableRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_table_flattened_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_table), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Table()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore.Table())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_table(
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
async def test_delete_table_flattened_error_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_table(
            metastore.DeleteTableRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.UpdateTableRequest,
        dict,
    ],
)
def test_update_table(request_type, transport: str = "grpc"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_table), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Table(
            name="name_value",
            type_=metastore.Table.Type.HIVE,
            etag="etag_value",
        )
        response = client.update_table(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.UpdateTableRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Table)
    assert response.name == "name_value"
    assert response.type_ == metastore.Table.Type.HIVE
    assert response.etag == "etag_value"


def test_update_table_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_table), "__call__") as call:
        client.update_table()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.UpdateTableRequest()


@pytest.mark.asyncio
async def test_update_table_async(
    transport: str = "grpc_asyncio", request_type=metastore.UpdateTableRequest
):
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_table), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.Table(
                name="name_value",
                type_=metastore.Table.Type.HIVE,
                etag="etag_value",
            )
        )
        response = await client.update_table(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.UpdateTableRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Table)
    assert response.name == "name_value"
    assert response.type_ == metastore.Table.Type.HIVE
    assert response.etag == "etag_value"


@pytest.mark.asyncio
async def test_update_table_async_from_dict():
    await test_update_table_async(request_type=dict)


def test_update_table_field_headers():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.UpdateTableRequest()

    request.table.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_table), "__call__") as call:
        call.return_value = metastore.Table()
        client.update_table(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "table.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_table_field_headers_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.UpdateTableRequest()

    request.table.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_table), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore.Table())
        await client.update_table(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "table.name=name_value",
    ) in kw["metadata"]


def test_update_table_flattened():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_table), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Table()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_table(
            table=metastore.Table(
                hive_options=metastore.HiveTableOptions(
                    parameters={"key_value": "value_value"}
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].table
        mock_val = metastore.Table(
            hive_options=metastore.HiveTableOptions(
                parameters={"key_value": "value_value"}
            )
        )
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_table_flattened_error():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_table(
            metastore.UpdateTableRequest(),
            table=metastore.Table(
                hive_options=metastore.HiveTableOptions(
                    parameters={"key_value": "value_value"}
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_table_flattened_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_table), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Table()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore.Table())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_table(
            table=metastore.Table(
                hive_options=metastore.HiveTableOptions(
                    parameters={"key_value": "value_value"}
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].table
        mock_val = metastore.Table(
            hive_options=metastore.HiveTableOptions(
                parameters={"key_value": "value_value"}
            )
        )
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_table_flattened_error_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_table(
            metastore.UpdateTableRequest(),
            table=metastore.Table(
                hive_options=metastore.HiveTableOptions(
                    parameters={"key_value": "value_value"}
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.RenameTableRequest,
        dict,
    ],
)
def test_rename_table(request_type, transport: str = "grpc"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rename_table), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Table(
            name="name_value",
            type_=metastore.Table.Type.HIVE,
            etag="etag_value",
        )
        response = client.rename_table(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.RenameTableRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Table)
    assert response.name == "name_value"
    assert response.type_ == metastore.Table.Type.HIVE
    assert response.etag == "etag_value"


def test_rename_table_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rename_table), "__call__") as call:
        client.rename_table()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.RenameTableRequest()


@pytest.mark.asyncio
async def test_rename_table_async(
    transport: str = "grpc_asyncio", request_type=metastore.RenameTableRequest
):
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rename_table), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.Table(
                name="name_value",
                type_=metastore.Table.Type.HIVE,
                etag="etag_value",
            )
        )
        response = await client.rename_table(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.RenameTableRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Table)
    assert response.name == "name_value"
    assert response.type_ == metastore.Table.Type.HIVE
    assert response.etag == "etag_value"


@pytest.mark.asyncio
async def test_rename_table_async_from_dict():
    await test_rename_table_async(request_type=dict)


def test_rename_table_field_headers():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.RenameTableRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rename_table), "__call__") as call:
        call.return_value = metastore.Table()
        client.rename_table(request)

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
async def test_rename_table_field_headers_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.RenameTableRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rename_table), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore.Table())
        await client.rename_table(request)

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


def test_rename_table_flattened():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rename_table), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Table()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.rename_table(
            name="name_value",
            new_name="new_name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].new_name
        mock_val = "new_name_value"
        assert arg == mock_val


def test_rename_table_flattened_error():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.rename_table(
            metastore.RenameTableRequest(),
            name="name_value",
            new_name="new_name_value",
        )


@pytest.mark.asyncio
async def test_rename_table_flattened_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.rename_table), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Table()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore.Table())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.rename_table(
            name="name_value",
            new_name="new_name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].new_name
        mock_val = "new_name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_rename_table_flattened_error_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.rename_table(
            metastore.RenameTableRequest(),
            name="name_value",
            new_name="new_name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.GetTableRequest,
        dict,
    ],
)
def test_get_table(request_type, transport: str = "grpc"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_table), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Table(
            name="name_value",
            type_=metastore.Table.Type.HIVE,
            etag="etag_value",
        )
        response = client.get_table(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.GetTableRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Table)
    assert response.name == "name_value"
    assert response.type_ == metastore.Table.Type.HIVE
    assert response.etag == "etag_value"


def test_get_table_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_table), "__call__") as call:
        client.get_table()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.GetTableRequest()


@pytest.mark.asyncio
async def test_get_table_async(
    transport: str = "grpc_asyncio", request_type=metastore.GetTableRequest
):
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_table), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.Table(
                name="name_value",
                type_=metastore.Table.Type.HIVE,
                etag="etag_value",
            )
        )
        response = await client.get_table(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.GetTableRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Table)
    assert response.name == "name_value"
    assert response.type_ == metastore.Table.Type.HIVE
    assert response.etag == "etag_value"


@pytest.mark.asyncio
async def test_get_table_async_from_dict():
    await test_get_table_async(request_type=dict)


def test_get_table_field_headers():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.GetTableRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_table), "__call__") as call:
        call.return_value = metastore.Table()
        client.get_table(request)

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
async def test_get_table_field_headers_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.GetTableRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_table), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore.Table())
        await client.get_table(request)

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


def test_get_table_flattened():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_table), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Table()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_table(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_table_flattened_error():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_table(
            metastore.GetTableRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_table_flattened_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_table), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Table()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore.Table())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_table(
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
async def test_get_table_flattened_error_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_table(
            metastore.GetTableRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.ListTablesRequest,
        dict,
    ],
)
def test_list_tables(request_type, transport: str = "grpc"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tables), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.ListTablesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_tables(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.ListTablesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTablesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_tables_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tables), "__call__") as call:
        client.list_tables()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.ListTablesRequest()


@pytest.mark.asyncio
async def test_list_tables_async(
    transport: str = "grpc_asyncio", request_type=metastore.ListTablesRequest
):
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tables), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.ListTablesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_tables(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.ListTablesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTablesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_tables_async_from_dict():
    await test_list_tables_async(request_type=dict)


def test_list_tables_field_headers():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.ListTablesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tables), "__call__") as call:
        call.return_value = metastore.ListTablesResponse()
        client.list_tables(request)

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
async def test_list_tables_field_headers_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.ListTablesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tables), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.ListTablesResponse()
        )
        await client.list_tables(request)

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


def test_list_tables_flattened():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tables), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.ListTablesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_tables(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_tables_flattened_error():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_tables(
            metastore.ListTablesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_tables_flattened_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tables), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.ListTablesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.ListTablesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_tables(
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
async def test_list_tables_flattened_error_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_tables(
            metastore.ListTablesRequest(),
            parent="parent_value",
        )


def test_list_tables_pager(transport_name: str = "grpc"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tables), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListTablesResponse(
                tables=[
                    metastore.Table(),
                    metastore.Table(),
                    metastore.Table(),
                ],
                next_page_token="abc",
            ),
            metastore.ListTablesResponse(
                tables=[],
                next_page_token="def",
            ),
            metastore.ListTablesResponse(
                tables=[
                    metastore.Table(),
                ],
                next_page_token="ghi",
            ),
            metastore.ListTablesResponse(
                tables=[
                    metastore.Table(),
                    metastore.Table(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_tables(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, metastore.Table) for i in results)


def test_list_tables_pages(transport_name: str = "grpc"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_tables), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListTablesResponse(
                tables=[
                    metastore.Table(),
                    metastore.Table(),
                    metastore.Table(),
                ],
                next_page_token="abc",
            ),
            metastore.ListTablesResponse(
                tables=[],
                next_page_token="def",
            ),
            metastore.ListTablesResponse(
                tables=[
                    metastore.Table(),
                ],
                next_page_token="ghi",
            ),
            metastore.ListTablesResponse(
                tables=[
                    metastore.Table(),
                    metastore.Table(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_tables(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_tables_async_pager():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tables), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListTablesResponse(
                tables=[
                    metastore.Table(),
                    metastore.Table(),
                    metastore.Table(),
                ],
                next_page_token="abc",
            ),
            metastore.ListTablesResponse(
                tables=[],
                next_page_token="def",
            ),
            metastore.ListTablesResponse(
                tables=[
                    metastore.Table(),
                ],
                next_page_token="ghi",
            ),
            metastore.ListTablesResponse(
                tables=[
                    metastore.Table(),
                    metastore.Table(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_tables(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, metastore.Table) for i in responses)


@pytest.mark.asyncio
async def test_list_tables_async_pages():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tables), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListTablesResponse(
                tables=[
                    metastore.Table(),
                    metastore.Table(),
                    metastore.Table(),
                ],
                next_page_token="abc",
            ),
            metastore.ListTablesResponse(
                tables=[],
                next_page_token="def",
            ),
            metastore.ListTablesResponse(
                tables=[
                    metastore.Table(),
                ],
                next_page_token="ghi",
            ),
            metastore.ListTablesResponse(
                tables=[
                    metastore.Table(),
                    metastore.Table(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_tables(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.CreateLockRequest,
        dict,
    ],
)
def test_create_lock(request_type, transport: str = "grpc"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_lock), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Lock(
            name="name_value",
            type_=metastore.Lock.Type.EXCLUSIVE,
            state=metastore.Lock.State.WAITING,
            table_id="table_id_value",
        )
        response = client.create_lock(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.CreateLockRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Lock)
    assert response.name == "name_value"
    assert response.type_ == metastore.Lock.Type.EXCLUSIVE
    assert response.state == metastore.Lock.State.WAITING


def test_create_lock_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_lock), "__call__") as call:
        client.create_lock()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.CreateLockRequest()


@pytest.mark.asyncio
async def test_create_lock_async(
    transport: str = "grpc_asyncio", request_type=metastore.CreateLockRequest
):
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_lock), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.Lock(
                name="name_value",
                type_=metastore.Lock.Type.EXCLUSIVE,
                state=metastore.Lock.State.WAITING,
            )
        )
        response = await client.create_lock(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.CreateLockRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Lock)
    assert response.name == "name_value"
    assert response.type_ == metastore.Lock.Type.EXCLUSIVE
    assert response.state == metastore.Lock.State.WAITING


@pytest.mark.asyncio
async def test_create_lock_async_from_dict():
    await test_create_lock_async(request_type=dict)


def test_create_lock_field_headers():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.CreateLockRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_lock), "__call__") as call:
        call.return_value = metastore.Lock()
        client.create_lock(request)

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
async def test_create_lock_field_headers_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.CreateLockRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_lock), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore.Lock())
        await client.create_lock(request)

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


def test_create_lock_flattened():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_lock), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Lock()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_lock(
            parent="parent_value",
            lock=metastore.Lock(table_id="table_id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].lock
        mock_val = metastore.Lock(table_id="table_id_value")
        assert arg == mock_val


def test_create_lock_flattened_error():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_lock(
            metastore.CreateLockRequest(),
            parent="parent_value",
            lock=metastore.Lock(table_id="table_id_value"),
        )


@pytest.mark.asyncio
async def test_create_lock_flattened_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_lock), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Lock()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore.Lock())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_lock(
            parent="parent_value",
            lock=metastore.Lock(table_id="table_id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].lock
        mock_val = metastore.Lock(table_id="table_id_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_lock_flattened_error_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_lock(
            metastore.CreateLockRequest(),
            parent="parent_value",
            lock=metastore.Lock(table_id="table_id_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.DeleteLockRequest,
        dict,
    ],
)
def test_delete_lock(request_type, transport: str = "grpc"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_lock), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_lock(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.DeleteLockRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_lock_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_lock), "__call__") as call:
        client.delete_lock()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.DeleteLockRequest()


@pytest.mark.asyncio
async def test_delete_lock_async(
    transport: str = "grpc_asyncio", request_type=metastore.DeleteLockRequest
):
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_lock), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_lock(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.DeleteLockRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_lock_async_from_dict():
    await test_delete_lock_async(request_type=dict)


def test_delete_lock_field_headers():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.DeleteLockRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_lock), "__call__") as call:
        call.return_value = None
        client.delete_lock(request)

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
async def test_delete_lock_field_headers_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.DeleteLockRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_lock), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_lock(request)

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


def test_delete_lock_flattened():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_lock), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_lock(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_lock_flattened_error():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_lock(
            metastore.DeleteLockRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_lock_flattened_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_lock), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_lock(
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
async def test_delete_lock_flattened_error_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_lock(
            metastore.DeleteLockRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.CheckLockRequest,
        dict,
    ],
)
def test_check_lock(request_type, transport: str = "grpc"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.check_lock), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Lock(
            name="name_value",
            type_=metastore.Lock.Type.EXCLUSIVE,
            state=metastore.Lock.State.WAITING,
            table_id="table_id_value",
        )
        response = client.check_lock(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.CheckLockRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Lock)
    assert response.name == "name_value"
    assert response.type_ == metastore.Lock.Type.EXCLUSIVE
    assert response.state == metastore.Lock.State.WAITING


def test_check_lock_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.check_lock), "__call__") as call:
        client.check_lock()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.CheckLockRequest()


@pytest.mark.asyncio
async def test_check_lock_async(
    transport: str = "grpc_asyncio", request_type=metastore.CheckLockRequest
):
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.check_lock), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.Lock(
                name="name_value",
                type_=metastore.Lock.Type.EXCLUSIVE,
                state=metastore.Lock.State.WAITING,
            )
        )
        response = await client.check_lock(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.CheckLockRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Lock)
    assert response.name == "name_value"
    assert response.type_ == metastore.Lock.Type.EXCLUSIVE
    assert response.state == metastore.Lock.State.WAITING


@pytest.mark.asyncio
async def test_check_lock_async_from_dict():
    await test_check_lock_async(request_type=dict)


def test_check_lock_field_headers():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.CheckLockRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.check_lock), "__call__") as call:
        call.return_value = metastore.Lock()
        client.check_lock(request)

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
async def test_check_lock_field_headers_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.CheckLockRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.check_lock), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore.Lock())
        await client.check_lock(request)

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


def test_check_lock_flattened():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.check_lock), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Lock()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.check_lock(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_check_lock_flattened_error():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.check_lock(
            metastore.CheckLockRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_check_lock_flattened_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.check_lock), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.Lock()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore.Lock())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.check_lock(
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
async def test_check_lock_flattened_error_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.check_lock(
            metastore.CheckLockRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.ListLocksRequest,
        dict,
    ],
)
def test_list_locks(request_type, transport: str = "grpc"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locks), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.ListLocksResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_locks(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.ListLocksRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListLocksPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_locks_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locks), "__call__") as call:
        client.list_locks()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.ListLocksRequest()


@pytest.mark.asyncio
async def test_list_locks_async(
    transport: str = "grpc_asyncio", request_type=metastore.ListLocksRequest
):
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locks), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.ListLocksResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_locks(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore.ListLocksRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListLocksAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_locks_async_from_dict():
    await test_list_locks_async(request_type=dict)


def test_list_locks_field_headers():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.ListLocksRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locks), "__call__") as call:
        call.return_value = metastore.ListLocksResponse()
        client.list_locks(request)

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
async def test_list_locks_field_headers_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore.ListLocksRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locks), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.ListLocksResponse()
        )
        await client.list_locks(request)

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


def test_list_locks_flattened():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locks), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.ListLocksResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_locks(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_locks_flattened_error():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_locks(
            metastore.ListLocksRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_locks_flattened_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locks), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore.ListLocksResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            metastore.ListLocksResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_locks(
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
async def test_list_locks_flattened_error_async():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_locks(
            metastore.ListLocksRequest(),
            parent="parent_value",
        )


def test_list_locks_pager(transport_name: str = "grpc"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locks), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListLocksResponse(
                locks=[
                    metastore.Lock(),
                    metastore.Lock(),
                    metastore.Lock(),
                ],
                next_page_token="abc",
            ),
            metastore.ListLocksResponse(
                locks=[],
                next_page_token="def",
            ),
            metastore.ListLocksResponse(
                locks=[
                    metastore.Lock(),
                ],
                next_page_token="ghi",
            ),
            metastore.ListLocksResponse(
                locks=[
                    metastore.Lock(),
                    metastore.Lock(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_locks(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, metastore.Lock) for i in results)


def test_list_locks_pages(transport_name: str = "grpc"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locks), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListLocksResponse(
                locks=[
                    metastore.Lock(),
                    metastore.Lock(),
                    metastore.Lock(),
                ],
                next_page_token="abc",
            ),
            metastore.ListLocksResponse(
                locks=[],
                next_page_token="def",
            ),
            metastore.ListLocksResponse(
                locks=[
                    metastore.Lock(),
                ],
                next_page_token="ghi",
            ),
            metastore.ListLocksResponse(
                locks=[
                    metastore.Lock(),
                    metastore.Lock(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_locks(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_locks_async_pager():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_locks), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListLocksResponse(
                locks=[
                    metastore.Lock(),
                    metastore.Lock(),
                    metastore.Lock(),
                ],
                next_page_token="abc",
            ),
            metastore.ListLocksResponse(
                locks=[],
                next_page_token="def",
            ),
            metastore.ListLocksResponse(
                locks=[
                    metastore.Lock(),
                ],
                next_page_token="ghi",
            ),
            metastore.ListLocksResponse(
                locks=[
                    metastore.Lock(),
                    metastore.Lock(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_locks(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, metastore.Lock) for i in responses)


@pytest.mark.asyncio
async def test_list_locks_async_pages():
    client = MetastoreServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_locks), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            metastore.ListLocksResponse(
                locks=[
                    metastore.Lock(),
                    metastore.Lock(),
                    metastore.Lock(),
                ],
                next_page_token="abc",
            ),
            metastore.ListLocksResponse(
                locks=[],
                next_page_token="def",
            ),
            metastore.ListLocksResponse(
                locks=[
                    metastore.Lock(),
                ],
                next_page_token="ghi",
            ),
            metastore.ListLocksResponse(
                locks=[
                    metastore.Lock(),
                    metastore.Lock(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_locks(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.CreateCatalogRequest,
        dict,
    ],
)
def test_create_catalog_rest(request_type):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["catalog"] = {
        "name": "name_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "delete_time": {},
        "expire_time": {},
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.Catalog(
            name="name_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.Catalog.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_catalog(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Catalog)
    assert response.name == "name_value"


def test_create_catalog_rest_required_fields(
    request_type=metastore.CreateCatalogRequest,
):
    transport_class = transports.MetastoreServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["catalog_id"] = ""
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
    assert "catalogId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_catalog._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "catalogId" in jsonified_request
    assert jsonified_request["catalogId"] == request_init["catalog_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["catalogId"] = "catalog_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_catalog._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("catalog_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "catalogId" in jsonified_request
    assert jsonified_request["catalogId"] == "catalog_id_value"

    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = metastore.Catalog()
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

            pb_return_value = metastore.Catalog.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_catalog(request)

            expected_params = [
                (
                    "catalogId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_catalog_rest_unset_required_fields():
    transport = transports.MetastoreServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_catalog._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("catalogId",))
        & set(
            (
                "parent",
                "catalog",
                "catalogId",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_catalog_rest_interceptors(null_interceptor):
    transport = transports.MetastoreServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.MetastoreServiceRestInterceptor(),
    )
    client = MetastoreServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.MetastoreServiceRestInterceptor, "post_create_catalog"
    ) as post, mock.patch.object(
        transports.MetastoreServiceRestInterceptor, "pre_create_catalog"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore.CreateCatalogRequest.pb(metastore.CreateCatalogRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = metastore.Catalog.to_json(metastore.Catalog())

        request = metastore.CreateCatalogRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = metastore.Catalog()

        client.create_catalog(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_catalog_rest_bad_request(
    transport: str = "rest", request_type=metastore.CreateCatalogRequest
):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["catalog"] = {
        "name": "name_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "delete_time": {},
        "expire_time": {},
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
        client.create_catalog(request)


def test_create_catalog_rest_flattened():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.Catalog()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            catalog=metastore.Catalog(name="name_value"),
            catalog_id="catalog_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.Catalog.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_catalog(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha1/{parent=projects/*/locations/*}/catalogs"
            % client.transport._host,
            args[1],
        )


def test_create_catalog_rest_flattened_error(transport: str = "rest"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_catalog(
            metastore.CreateCatalogRequest(),
            parent="parent_value",
            catalog=metastore.Catalog(name="name_value"),
            catalog_id="catalog_id_value",
        )


def test_create_catalog_rest_error():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.DeleteCatalogRequest,
        dict,
    ],
)
def test_delete_catalog_rest(request_type):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/catalogs/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.Catalog(
            name="name_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.Catalog.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_catalog(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Catalog)
    assert response.name == "name_value"


def test_delete_catalog_rest_required_fields(
    request_type=metastore.DeleteCatalogRequest,
):
    transport_class = transports.MetastoreServiceRestTransport

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
    ).delete_catalog._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_catalog._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = metastore.Catalog()
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

            pb_return_value = metastore.Catalog.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_catalog(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_catalog_rest_unset_required_fields():
    transport = transports.MetastoreServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_catalog._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_catalog_rest_interceptors(null_interceptor):
    transport = transports.MetastoreServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.MetastoreServiceRestInterceptor(),
    )
    client = MetastoreServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.MetastoreServiceRestInterceptor, "post_delete_catalog"
    ) as post, mock.patch.object(
        transports.MetastoreServiceRestInterceptor, "pre_delete_catalog"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore.DeleteCatalogRequest.pb(metastore.DeleteCatalogRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = metastore.Catalog.to_json(metastore.Catalog())

        request = metastore.DeleteCatalogRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = metastore.Catalog()

        client.delete_catalog(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_catalog_rest_bad_request(
    transport: str = "rest", request_type=metastore.DeleteCatalogRequest
):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/catalogs/sample3"}
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
        client.delete_catalog(request)


def test_delete_catalog_rest_flattened():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.Catalog()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/locations/sample2/catalogs/sample3"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.Catalog.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_catalog(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha1/{name=projects/*/locations/*/catalogs/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_catalog_rest_flattened_error(transport: str = "rest"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_catalog(
            metastore.DeleteCatalogRequest(),
            name="name_value",
        )


def test_delete_catalog_rest_error():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.GetCatalogRequest,
        dict,
    ],
)
def test_get_catalog_rest(request_type):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/catalogs/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.Catalog(
            name="name_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.Catalog.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_catalog(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Catalog)
    assert response.name == "name_value"


def test_get_catalog_rest_required_fields(request_type=metastore.GetCatalogRequest):
    transport_class = transports.MetastoreServiceRestTransport

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
    ).get_catalog._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_catalog._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = metastore.Catalog()
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

            pb_return_value = metastore.Catalog.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_catalog(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_catalog_rest_unset_required_fields():
    transport = transports.MetastoreServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_catalog._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_catalog_rest_interceptors(null_interceptor):
    transport = transports.MetastoreServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.MetastoreServiceRestInterceptor(),
    )
    client = MetastoreServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.MetastoreServiceRestInterceptor, "post_get_catalog"
    ) as post, mock.patch.object(
        transports.MetastoreServiceRestInterceptor, "pre_get_catalog"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore.GetCatalogRequest.pb(metastore.GetCatalogRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = metastore.Catalog.to_json(metastore.Catalog())

        request = metastore.GetCatalogRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = metastore.Catalog()

        client.get_catalog(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_catalog_rest_bad_request(
    transport: str = "rest", request_type=metastore.GetCatalogRequest
):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/catalogs/sample3"}
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
        client.get_catalog(request)


def test_get_catalog_rest_flattened():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.Catalog()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/locations/sample2/catalogs/sample3"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.Catalog.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_catalog(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha1/{name=projects/*/locations/*/catalogs/*}"
            % client.transport._host,
            args[1],
        )


def test_get_catalog_rest_flattened_error(transport: str = "rest"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_catalog(
            metastore.GetCatalogRequest(),
            name="name_value",
        )


def test_get_catalog_rest_error():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.ListCatalogsRequest,
        dict,
    ],
)
def test_list_catalogs_rest(request_type):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.ListCatalogsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.ListCatalogsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_catalogs(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCatalogsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_catalogs_rest_required_fields(request_type=metastore.ListCatalogsRequest):
    transport_class = transports.MetastoreServiceRestTransport

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
    ).list_catalogs._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_catalogs._get_unset_required_fields(jsonified_request)
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

    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = metastore.ListCatalogsResponse()
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

            pb_return_value = metastore.ListCatalogsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_catalogs(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_catalogs_rest_unset_required_fields():
    transport = transports.MetastoreServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_catalogs._get_unset_required_fields({})
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
def test_list_catalogs_rest_interceptors(null_interceptor):
    transport = transports.MetastoreServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.MetastoreServiceRestInterceptor(),
    )
    client = MetastoreServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.MetastoreServiceRestInterceptor, "post_list_catalogs"
    ) as post, mock.patch.object(
        transports.MetastoreServiceRestInterceptor, "pre_list_catalogs"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore.ListCatalogsRequest.pb(metastore.ListCatalogsRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = metastore.ListCatalogsResponse.to_json(
            metastore.ListCatalogsResponse()
        )

        request = metastore.ListCatalogsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = metastore.ListCatalogsResponse()

        client.list_catalogs(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_catalogs_rest_bad_request(
    transport: str = "rest", request_type=metastore.ListCatalogsRequest
):
    client = MetastoreServiceClient(
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
        client.list_catalogs(request)


def test_list_catalogs_rest_flattened():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.ListCatalogsResponse()

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
        pb_return_value = metastore.ListCatalogsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_catalogs(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha1/{parent=projects/*/locations/*}/catalogs"
            % client.transport._host,
            args[1],
        )


def test_list_catalogs_rest_flattened_error(transport: str = "rest"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_catalogs(
            metastore.ListCatalogsRequest(),
            parent="parent_value",
        )


def test_list_catalogs_rest_pager(transport: str = "rest"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            metastore.ListCatalogsResponse(
                catalogs=[
                    metastore.Catalog(),
                    metastore.Catalog(),
                    metastore.Catalog(),
                ],
                next_page_token="abc",
            ),
            metastore.ListCatalogsResponse(
                catalogs=[],
                next_page_token="def",
            ),
            metastore.ListCatalogsResponse(
                catalogs=[
                    metastore.Catalog(),
                ],
                next_page_token="ghi",
            ),
            metastore.ListCatalogsResponse(
                catalogs=[
                    metastore.Catalog(),
                    metastore.Catalog(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(metastore.ListCatalogsResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_catalogs(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, metastore.Catalog) for i in results)

        pages = list(client.list_catalogs(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.CreateDatabaseRequest,
        dict,
    ],
)
def test_create_database_rest(request_type):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/catalogs/sample3"}
    request_init["database"] = {
        "hive_options": {"location_uri": "location_uri_value", "parameters": {}},
        "name": "name_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "delete_time": {},
        "expire_time": {},
        "type_": 1,
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.Database(
            name="name_value",
            type_=metastore.Database.Type.HIVE,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.Database.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_database(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Database)
    assert response.name == "name_value"
    assert response.type_ == metastore.Database.Type.HIVE


def test_create_database_rest_required_fields(
    request_type=metastore.CreateDatabaseRequest,
):
    transport_class = transports.MetastoreServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["database_id"] = ""
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
    assert "databaseId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_database._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "databaseId" in jsonified_request
    assert jsonified_request["databaseId"] == request_init["database_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["databaseId"] = "database_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_database._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("database_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "databaseId" in jsonified_request
    assert jsonified_request["databaseId"] == "database_id_value"

    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = metastore.Database()
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

            pb_return_value = metastore.Database.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_database(request)

            expected_params = [
                (
                    "databaseId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_database_rest_unset_required_fields():
    transport = transports.MetastoreServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_database._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("databaseId",))
        & set(
            (
                "parent",
                "database",
                "databaseId",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_database_rest_interceptors(null_interceptor):
    transport = transports.MetastoreServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.MetastoreServiceRestInterceptor(),
    )
    client = MetastoreServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.MetastoreServiceRestInterceptor, "post_create_database"
    ) as post, mock.patch.object(
        transports.MetastoreServiceRestInterceptor, "pre_create_database"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore.CreateDatabaseRequest.pb(
            metastore.CreateDatabaseRequest()
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
        req.return_value._content = metastore.Database.to_json(metastore.Database())

        request = metastore.CreateDatabaseRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = metastore.Database()

        client.create_database(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_database_rest_bad_request(
    transport: str = "rest", request_type=metastore.CreateDatabaseRequest
):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/catalogs/sample3"}
    request_init["database"] = {
        "hive_options": {"location_uri": "location_uri_value", "parameters": {}},
        "name": "name_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "delete_time": {},
        "expire_time": {},
        "type_": 1,
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
        client.create_database(request)


def test_create_database_rest_flattened():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.Database()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/catalogs/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            database=metastore.Database(
                hive_options=metastore.HiveDatabaseOptions(
                    location_uri="location_uri_value"
                )
            ),
            database_id="database_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.Database.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_database(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha1/{parent=projects/*/locations/*/catalogs/*}/databases"
            % client.transport._host,
            args[1],
        )


def test_create_database_rest_flattened_error(transport: str = "rest"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_database(
            metastore.CreateDatabaseRequest(),
            parent="parent_value",
            database=metastore.Database(
                hive_options=metastore.HiveDatabaseOptions(
                    location_uri="location_uri_value"
                )
            ),
            database_id="database_id_value",
        )


def test_create_database_rest_error():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.DeleteDatabaseRequest,
        dict,
    ],
)
def test_delete_database_rest(request_type):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.Database(
            name="name_value",
            type_=metastore.Database.Type.HIVE,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.Database.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_database(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Database)
    assert response.name == "name_value"
    assert response.type_ == metastore.Database.Type.HIVE


def test_delete_database_rest_required_fields(
    request_type=metastore.DeleteDatabaseRequest,
):
    transport_class = transports.MetastoreServiceRestTransport

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
    ).delete_database._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_database._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = metastore.Database()
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

            pb_return_value = metastore.Database.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_database(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_database_rest_unset_required_fields():
    transport = transports.MetastoreServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_database._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_database_rest_interceptors(null_interceptor):
    transport = transports.MetastoreServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.MetastoreServiceRestInterceptor(),
    )
    client = MetastoreServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.MetastoreServiceRestInterceptor, "post_delete_database"
    ) as post, mock.patch.object(
        transports.MetastoreServiceRestInterceptor, "pre_delete_database"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore.DeleteDatabaseRequest.pb(
            metastore.DeleteDatabaseRequest()
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
        req.return_value._content = metastore.Database.to_json(metastore.Database())

        request = metastore.DeleteDatabaseRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = metastore.Database()

        client.delete_database(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_database_rest_bad_request(
    transport: str = "rest", request_type=metastore.DeleteDatabaseRequest
):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4"
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
        client.delete_database(request)


def test_delete_database_rest_flattened():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.Database()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.Database.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_database(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha1/{name=projects/*/locations/*/catalogs/*/databases/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_database_rest_flattened_error(transport: str = "rest"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_database(
            metastore.DeleteDatabaseRequest(),
            name="name_value",
        )


def test_delete_database_rest_error():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.UpdateDatabaseRequest,
        dict,
    ],
)
def test_update_database_rest(request_type):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "database": {
            "name": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4"
        }
    }
    request_init["database"] = {
        "hive_options": {"location_uri": "location_uri_value", "parameters": {}},
        "name": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "delete_time": {},
        "expire_time": {},
        "type_": 1,
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.Database(
            name="name_value",
            type_=metastore.Database.Type.HIVE,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.Database.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_database(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Database)
    assert response.name == "name_value"
    assert response.type_ == metastore.Database.Type.HIVE


def test_update_database_rest_required_fields(
    request_type=metastore.UpdateDatabaseRequest,
):
    transport_class = transports.MetastoreServiceRestTransport

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
    ).update_database._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_database._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = metastore.Database()
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

            pb_return_value = metastore.Database.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_database(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_database_rest_unset_required_fields():
    transport = transports.MetastoreServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_database._get_unset_required_fields({})
    assert set(unset_fields) == (set(("updateMask",)) & set(("database",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_database_rest_interceptors(null_interceptor):
    transport = transports.MetastoreServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.MetastoreServiceRestInterceptor(),
    )
    client = MetastoreServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.MetastoreServiceRestInterceptor, "post_update_database"
    ) as post, mock.patch.object(
        transports.MetastoreServiceRestInterceptor, "pre_update_database"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore.UpdateDatabaseRequest.pb(
            metastore.UpdateDatabaseRequest()
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
        req.return_value._content = metastore.Database.to_json(metastore.Database())

        request = metastore.UpdateDatabaseRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = metastore.Database()

        client.update_database(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_database_rest_bad_request(
    transport: str = "rest", request_type=metastore.UpdateDatabaseRequest
):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "database": {
            "name": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4"
        }
    }
    request_init["database"] = {
        "hive_options": {"location_uri": "location_uri_value", "parameters": {}},
        "name": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "delete_time": {},
        "expire_time": {},
        "type_": 1,
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
        client.update_database(request)


def test_update_database_rest_flattened():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.Database()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "database": {
                "name": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            database=metastore.Database(
                hive_options=metastore.HiveDatabaseOptions(
                    location_uri="location_uri_value"
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.Database.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_database(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha1/{database.name=projects/*/locations/*/catalogs/*/databases/*}"
            % client.transport._host,
            args[1],
        )


def test_update_database_rest_flattened_error(transport: str = "rest"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_database(
            metastore.UpdateDatabaseRequest(),
            database=metastore.Database(
                hive_options=metastore.HiveDatabaseOptions(
                    location_uri="location_uri_value"
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_database_rest_error():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.GetDatabaseRequest,
        dict,
    ],
)
def test_get_database_rest(request_type):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.Database(
            name="name_value",
            type_=metastore.Database.Type.HIVE,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.Database.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_database(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Database)
    assert response.name == "name_value"
    assert response.type_ == metastore.Database.Type.HIVE


def test_get_database_rest_required_fields(request_type=metastore.GetDatabaseRequest):
    transport_class = transports.MetastoreServiceRestTransport

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
    ).get_database._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_database._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = metastore.Database()
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

            pb_return_value = metastore.Database.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_database(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_database_rest_unset_required_fields():
    transport = transports.MetastoreServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_database._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_database_rest_interceptors(null_interceptor):
    transport = transports.MetastoreServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.MetastoreServiceRestInterceptor(),
    )
    client = MetastoreServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.MetastoreServiceRestInterceptor, "post_get_database"
    ) as post, mock.patch.object(
        transports.MetastoreServiceRestInterceptor, "pre_get_database"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore.GetDatabaseRequest.pb(metastore.GetDatabaseRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = metastore.Database.to_json(metastore.Database())

        request = metastore.GetDatabaseRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = metastore.Database()

        client.get_database(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_database_rest_bad_request(
    transport: str = "rest", request_type=metastore.GetDatabaseRequest
):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4"
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
        client.get_database(request)


def test_get_database_rest_flattened():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.Database()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.Database.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_database(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha1/{name=projects/*/locations/*/catalogs/*/databases/*}"
            % client.transport._host,
            args[1],
        )


def test_get_database_rest_flattened_error(transport: str = "rest"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_database(
            metastore.GetDatabaseRequest(),
            name="name_value",
        )


def test_get_database_rest_error():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.ListDatabasesRequest,
        dict,
    ],
)
def test_list_databases_rest(request_type):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/catalogs/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.ListDatabasesResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.ListDatabasesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_databases(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDatabasesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_databases_rest_required_fields(
    request_type=metastore.ListDatabasesRequest,
):
    transport_class = transports.MetastoreServiceRestTransport

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
    ).list_databases._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_databases._get_unset_required_fields(jsonified_request)
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

    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = metastore.ListDatabasesResponse()
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

            pb_return_value = metastore.ListDatabasesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_databases(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_databases_rest_unset_required_fields():
    transport = transports.MetastoreServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_databases._get_unset_required_fields({})
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
def test_list_databases_rest_interceptors(null_interceptor):
    transport = transports.MetastoreServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.MetastoreServiceRestInterceptor(),
    )
    client = MetastoreServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.MetastoreServiceRestInterceptor, "post_list_databases"
    ) as post, mock.patch.object(
        transports.MetastoreServiceRestInterceptor, "pre_list_databases"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore.ListDatabasesRequest.pb(metastore.ListDatabasesRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = metastore.ListDatabasesResponse.to_json(
            metastore.ListDatabasesResponse()
        )

        request = metastore.ListDatabasesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = metastore.ListDatabasesResponse()

        client.list_databases(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_databases_rest_bad_request(
    transport: str = "rest", request_type=metastore.ListDatabasesRequest
):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/catalogs/sample3"}
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
        client.list_databases(request)


def test_list_databases_rest_flattened():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.ListDatabasesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/catalogs/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.ListDatabasesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_databases(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha1/{parent=projects/*/locations/*/catalogs/*}/databases"
            % client.transport._host,
            args[1],
        )


def test_list_databases_rest_flattened_error(transport: str = "rest"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_databases(
            metastore.ListDatabasesRequest(),
            parent="parent_value",
        )


def test_list_databases_rest_pager(transport: str = "rest"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            metastore.ListDatabasesResponse(
                databases=[
                    metastore.Database(),
                    metastore.Database(),
                    metastore.Database(),
                ],
                next_page_token="abc",
            ),
            metastore.ListDatabasesResponse(
                databases=[],
                next_page_token="def",
            ),
            metastore.ListDatabasesResponse(
                databases=[
                    metastore.Database(),
                ],
                next_page_token="ghi",
            ),
            metastore.ListDatabasesResponse(
                databases=[
                    metastore.Database(),
                    metastore.Database(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(metastore.ListDatabasesResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/catalogs/sample3"
        }

        pager = client.list_databases(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, metastore.Database) for i in results)

        pages = list(client.list_databases(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.CreateTableRequest,
        dict,
    ],
)
def test_create_table_rest(request_type):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4"
    }
    request_init["table"] = {
        "hive_options": {
            "parameters": {},
            "table_type": "table_type_value",
            "storage_descriptor": {
                "location_uri": "location_uri_value",
                "input_format": "input_format_value",
                "output_format": "output_format_value",
                "serde_info": {"serialization_lib": "serialization_lib_value"},
            },
        },
        "name": "name_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "delete_time": {},
        "expire_time": {},
        "type_": 1,
        "etag": "etag_value",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.Table(
            name="name_value",
            type_=metastore.Table.Type.HIVE,
            etag="etag_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.Table.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_table(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Table)
    assert response.name == "name_value"
    assert response.type_ == metastore.Table.Type.HIVE
    assert response.etag == "etag_value"


def test_create_table_rest_required_fields(request_type=metastore.CreateTableRequest):
    transport_class = transports.MetastoreServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["table_id"] = ""
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
    assert "tableId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_table._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "tableId" in jsonified_request
    assert jsonified_request["tableId"] == request_init["table_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["tableId"] = "table_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_table._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("table_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "tableId" in jsonified_request
    assert jsonified_request["tableId"] == "table_id_value"

    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = metastore.Table()
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

            pb_return_value = metastore.Table.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_table(request)

            expected_params = [
                (
                    "tableId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_table_rest_unset_required_fields():
    transport = transports.MetastoreServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_table._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("tableId",))
        & set(
            (
                "parent",
                "table",
                "tableId",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_table_rest_interceptors(null_interceptor):
    transport = transports.MetastoreServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.MetastoreServiceRestInterceptor(),
    )
    client = MetastoreServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.MetastoreServiceRestInterceptor, "post_create_table"
    ) as post, mock.patch.object(
        transports.MetastoreServiceRestInterceptor, "pre_create_table"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore.CreateTableRequest.pb(metastore.CreateTableRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = metastore.Table.to_json(metastore.Table())

        request = metastore.CreateTableRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = metastore.Table()

        client.create_table(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_table_rest_bad_request(
    transport: str = "rest", request_type=metastore.CreateTableRequest
):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4"
    }
    request_init["table"] = {
        "hive_options": {
            "parameters": {},
            "table_type": "table_type_value",
            "storage_descriptor": {
                "location_uri": "location_uri_value",
                "input_format": "input_format_value",
                "output_format": "output_format_value",
                "serde_info": {"serialization_lib": "serialization_lib_value"},
            },
        },
        "name": "name_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "delete_time": {},
        "expire_time": {},
        "type_": 1,
        "etag": "etag_value",
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
        client.create_table(request)


def test_create_table_rest_flattened():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.Table()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            table=metastore.Table(
                hive_options=metastore.HiveTableOptions(
                    parameters={"key_value": "value_value"}
                )
            ),
            table_id="table_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.Table.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_table(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha1/{parent=projects/*/locations/*/catalogs/*/databases/*}/tables"
            % client.transport._host,
            args[1],
        )


def test_create_table_rest_flattened_error(transport: str = "rest"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_table(
            metastore.CreateTableRequest(),
            parent="parent_value",
            table=metastore.Table(
                hive_options=metastore.HiveTableOptions(
                    parameters={"key_value": "value_value"}
                )
            ),
            table_id="table_id_value",
        )


def test_create_table_rest_error():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.DeleteTableRequest,
        dict,
    ],
)
def test_delete_table_rest(request_type):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4/tables/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.Table(
            name="name_value",
            type_=metastore.Table.Type.HIVE,
            etag="etag_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.Table.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_table(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Table)
    assert response.name == "name_value"
    assert response.type_ == metastore.Table.Type.HIVE
    assert response.etag == "etag_value"


def test_delete_table_rest_required_fields(request_type=metastore.DeleteTableRequest):
    transport_class = transports.MetastoreServiceRestTransport

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
    ).delete_table._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_table._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = metastore.Table()
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

            pb_return_value = metastore.Table.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_table(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_table_rest_unset_required_fields():
    transport = transports.MetastoreServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_table._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_table_rest_interceptors(null_interceptor):
    transport = transports.MetastoreServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.MetastoreServiceRestInterceptor(),
    )
    client = MetastoreServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.MetastoreServiceRestInterceptor, "post_delete_table"
    ) as post, mock.patch.object(
        transports.MetastoreServiceRestInterceptor, "pre_delete_table"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore.DeleteTableRequest.pb(metastore.DeleteTableRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = metastore.Table.to_json(metastore.Table())

        request = metastore.DeleteTableRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = metastore.Table()

        client.delete_table(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_table_rest_bad_request(
    transport: str = "rest", request_type=metastore.DeleteTableRequest
):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4/tables/sample5"
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
        client.delete_table(request)


def test_delete_table_rest_flattened():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.Table()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4/tables/sample5"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.Table.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_table(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha1/{name=projects/*/locations/*/catalogs/*/databases/*/tables/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_table_rest_flattened_error(transport: str = "rest"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_table(
            metastore.DeleteTableRequest(),
            name="name_value",
        )


def test_delete_table_rest_error():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.UpdateTableRequest,
        dict,
    ],
)
def test_update_table_rest(request_type):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "table": {
            "name": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4/tables/sample5"
        }
    }
    request_init["table"] = {
        "hive_options": {
            "parameters": {},
            "table_type": "table_type_value",
            "storage_descriptor": {
                "location_uri": "location_uri_value",
                "input_format": "input_format_value",
                "output_format": "output_format_value",
                "serde_info": {"serialization_lib": "serialization_lib_value"},
            },
        },
        "name": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4/tables/sample5",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "delete_time": {},
        "expire_time": {},
        "type_": 1,
        "etag": "etag_value",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.Table(
            name="name_value",
            type_=metastore.Table.Type.HIVE,
            etag="etag_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.Table.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_table(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Table)
    assert response.name == "name_value"
    assert response.type_ == metastore.Table.Type.HIVE
    assert response.etag == "etag_value"


def test_update_table_rest_required_fields(request_type=metastore.UpdateTableRequest):
    transport_class = transports.MetastoreServiceRestTransport

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
    ).update_table._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_table._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = metastore.Table()
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

            pb_return_value = metastore.Table.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_table(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_table_rest_unset_required_fields():
    transport = transports.MetastoreServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_table._get_unset_required_fields({})
    assert set(unset_fields) == (set(("updateMask",)) & set(("table",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_table_rest_interceptors(null_interceptor):
    transport = transports.MetastoreServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.MetastoreServiceRestInterceptor(),
    )
    client = MetastoreServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.MetastoreServiceRestInterceptor, "post_update_table"
    ) as post, mock.patch.object(
        transports.MetastoreServiceRestInterceptor, "pre_update_table"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore.UpdateTableRequest.pb(metastore.UpdateTableRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = metastore.Table.to_json(metastore.Table())

        request = metastore.UpdateTableRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = metastore.Table()

        client.update_table(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_table_rest_bad_request(
    transport: str = "rest", request_type=metastore.UpdateTableRequest
):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "table": {
            "name": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4/tables/sample5"
        }
    }
    request_init["table"] = {
        "hive_options": {
            "parameters": {},
            "table_type": "table_type_value",
            "storage_descriptor": {
                "location_uri": "location_uri_value",
                "input_format": "input_format_value",
                "output_format": "output_format_value",
                "serde_info": {"serialization_lib": "serialization_lib_value"},
            },
        },
        "name": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4/tables/sample5",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "delete_time": {},
        "expire_time": {},
        "type_": 1,
        "etag": "etag_value",
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
        client.update_table(request)


def test_update_table_rest_flattened():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.Table()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "table": {
                "name": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4/tables/sample5"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            table=metastore.Table(
                hive_options=metastore.HiveTableOptions(
                    parameters={"key_value": "value_value"}
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.Table.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_table(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha1/{table.name=projects/*/locations/*/catalogs/*/databases/*/tables/*}"
            % client.transport._host,
            args[1],
        )


def test_update_table_rest_flattened_error(transport: str = "rest"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_table(
            metastore.UpdateTableRequest(),
            table=metastore.Table(
                hive_options=metastore.HiveTableOptions(
                    parameters={"key_value": "value_value"}
                )
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_table_rest_error():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.RenameTableRequest,
        dict,
    ],
)
def test_rename_table_rest(request_type):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4/tables/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.Table(
            name="name_value",
            type_=metastore.Table.Type.HIVE,
            etag="etag_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.Table.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.rename_table(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Table)
    assert response.name == "name_value"
    assert response.type_ == metastore.Table.Type.HIVE
    assert response.etag == "etag_value"


def test_rename_table_rest_required_fields(request_type=metastore.RenameTableRequest):
    transport_class = transports.MetastoreServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request_init["new_name"] = ""
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
    ).rename_table._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"
    jsonified_request["newName"] = "new_name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).rename_table._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"
    assert "newName" in jsonified_request
    assert jsonified_request["newName"] == "new_name_value"

    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = metastore.Table()
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

            pb_return_value = metastore.Table.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.rename_table(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_rename_table_rest_unset_required_fields():
    transport = transports.MetastoreServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.rename_table._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "name",
                "newName",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_rename_table_rest_interceptors(null_interceptor):
    transport = transports.MetastoreServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.MetastoreServiceRestInterceptor(),
    )
    client = MetastoreServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.MetastoreServiceRestInterceptor, "post_rename_table"
    ) as post, mock.patch.object(
        transports.MetastoreServiceRestInterceptor, "pre_rename_table"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore.RenameTableRequest.pb(metastore.RenameTableRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = metastore.Table.to_json(metastore.Table())

        request = metastore.RenameTableRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = metastore.Table()

        client.rename_table(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_rename_table_rest_bad_request(
    transport: str = "rest", request_type=metastore.RenameTableRequest
):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4/tables/sample5"
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
        client.rename_table(request)


def test_rename_table_rest_flattened():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.Table()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4/tables/sample5"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
            new_name="new_name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.Table.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.rename_table(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha1/{name=projects/*/locations/*/catalogs/*/databases/*/tables/*}:rename"
            % client.transport._host,
            args[1],
        )


def test_rename_table_rest_flattened_error(transport: str = "rest"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.rename_table(
            metastore.RenameTableRequest(),
            name="name_value",
            new_name="new_name_value",
        )


def test_rename_table_rest_error():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.GetTableRequest,
        dict,
    ],
)
def test_get_table_rest(request_type):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4/tables/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.Table(
            name="name_value",
            type_=metastore.Table.Type.HIVE,
            etag="etag_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.Table.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_table(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Table)
    assert response.name == "name_value"
    assert response.type_ == metastore.Table.Type.HIVE
    assert response.etag == "etag_value"


def test_get_table_rest_required_fields(request_type=metastore.GetTableRequest):
    transport_class = transports.MetastoreServiceRestTransport

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
    ).get_table._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_table._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = metastore.Table()
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

            pb_return_value = metastore.Table.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_table(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_table_rest_unset_required_fields():
    transport = transports.MetastoreServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_table._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_table_rest_interceptors(null_interceptor):
    transport = transports.MetastoreServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.MetastoreServiceRestInterceptor(),
    )
    client = MetastoreServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.MetastoreServiceRestInterceptor, "post_get_table"
    ) as post, mock.patch.object(
        transports.MetastoreServiceRestInterceptor, "pre_get_table"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore.GetTableRequest.pb(metastore.GetTableRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = metastore.Table.to_json(metastore.Table())

        request = metastore.GetTableRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = metastore.Table()

        client.get_table(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_table_rest_bad_request(
    transport: str = "rest", request_type=metastore.GetTableRequest
):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4/tables/sample5"
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
        client.get_table(request)


def test_get_table_rest_flattened():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.Table()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4/tables/sample5"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.Table.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_table(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha1/{name=projects/*/locations/*/catalogs/*/databases/*/tables/*}"
            % client.transport._host,
            args[1],
        )


def test_get_table_rest_flattened_error(transport: str = "rest"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_table(
            metastore.GetTableRequest(),
            name="name_value",
        )


def test_get_table_rest_error():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.ListTablesRequest,
        dict,
    ],
)
def test_list_tables_rest(request_type):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.ListTablesResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.ListTablesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_tables(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTablesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_tables_rest_required_fields(request_type=metastore.ListTablesRequest):
    transport_class = transports.MetastoreServiceRestTransport

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
    ).list_tables._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_tables._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
            "view",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = metastore.ListTablesResponse()
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

            pb_return_value = metastore.ListTablesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_tables(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_tables_rest_unset_required_fields():
    transport = transports.MetastoreServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_tables._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
                "view",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_tables_rest_interceptors(null_interceptor):
    transport = transports.MetastoreServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.MetastoreServiceRestInterceptor(),
    )
    client = MetastoreServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.MetastoreServiceRestInterceptor, "post_list_tables"
    ) as post, mock.patch.object(
        transports.MetastoreServiceRestInterceptor, "pre_list_tables"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore.ListTablesRequest.pb(metastore.ListTablesRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = metastore.ListTablesResponse.to_json(
            metastore.ListTablesResponse()
        )

        request = metastore.ListTablesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = metastore.ListTablesResponse()

        client.list_tables(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_tables_rest_bad_request(
    transport: str = "rest", request_type=metastore.ListTablesRequest
):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4"
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
        client.list_tables(request)


def test_list_tables_rest_flattened():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.ListTablesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.ListTablesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_tables(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha1/{parent=projects/*/locations/*/catalogs/*/databases/*}/tables"
            % client.transport._host,
            args[1],
        )


def test_list_tables_rest_flattened_error(transport: str = "rest"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_tables(
            metastore.ListTablesRequest(),
            parent="parent_value",
        )


def test_list_tables_rest_pager(transport: str = "rest"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            metastore.ListTablesResponse(
                tables=[
                    metastore.Table(),
                    metastore.Table(),
                    metastore.Table(),
                ],
                next_page_token="abc",
            ),
            metastore.ListTablesResponse(
                tables=[],
                next_page_token="def",
            ),
            metastore.ListTablesResponse(
                tables=[
                    metastore.Table(),
                ],
                next_page_token="ghi",
            ),
            metastore.ListTablesResponse(
                tables=[
                    metastore.Table(),
                    metastore.Table(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(metastore.ListTablesResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4"
        }

        pager = client.list_tables(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, metastore.Table) for i in results)

        pages = list(client.list_tables(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.CreateLockRequest,
        dict,
    ],
)
def test_create_lock_rest(request_type):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4"
    }
    request_init["lock"] = {
        "table_id": "table_id_value",
        "name": "name_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "type_": 1,
        "state": 1,
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.Lock(
            name="name_value",
            type_=metastore.Lock.Type.EXCLUSIVE,
            state=metastore.Lock.State.WAITING,
            table_id="table_id_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.Lock.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_lock(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Lock)
    assert response.name == "name_value"
    assert response.type_ == metastore.Lock.Type.EXCLUSIVE
    assert response.state == metastore.Lock.State.WAITING


def test_create_lock_rest_required_fields(request_type=metastore.CreateLockRequest):
    transport_class = transports.MetastoreServiceRestTransport

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
    ).create_lock._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_lock._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = metastore.Lock()
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

            pb_return_value = metastore.Lock.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_lock(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_lock_rest_unset_required_fields():
    transport = transports.MetastoreServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_lock._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "lock",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_lock_rest_interceptors(null_interceptor):
    transport = transports.MetastoreServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.MetastoreServiceRestInterceptor(),
    )
    client = MetastoreServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.MetastoreServiceRestInterceptor, "post_create_lock"
    ) as post, mock.patch.object(
        transports.MetastoreServiceRestInterceptor, "pre_create_lock"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore.CreateLockRequest.pb(metastore.CreateLockRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = metastore.Lock.to_json(metastore.Lock())

        request = metastore.CreateLockRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = metastore.Lock()

        client.create_lock(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_lock_rest_bad_request(
    transport: str = "rest", request_type=metastore.CreateLockRequest
):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4"
    }
    request_init["lock"] = {
        "table_id": "table_id_value",
        "name": "name_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "type_": 1,
        "state": 1,
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
        client.create_lock(request)


def test_create_lock_rest_flattened():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.Lock()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            lock=metastore.Lock(table_id="table_id_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.Lock.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_lock(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha1/{parent=projects/*/locations/*/catalogs/*/databases/*}/locks"
            % client.transport._host,
            args[1],
        )


def test_create_lock_rest_flattened_error(transport: str = "rest"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_lock(
            metastore.CreateLockRequest(),
            parent="parent_value",
            lock=metastore.Lock(table_id="table_id_value"),
        )


def test_create_lock_rest_error():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.DeleteLockRequest,
        dict,
    ],
)
def test_delete_lock_rest(request_type):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4/locks/sample5"
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
        response = client.delete_lock(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_lock_rest_required_fields(request_type=metastore.DeleteLockRequest):
    transport_class = transports.MetastoreServiceRestTransport

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
    ).delete_lock._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_lock._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = MetastoreServiceClient(
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

            response = client.delete_lock(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_lock_rest_unset_required_fields():
    transport = transports.MetastoreServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_lock._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_lock_rest_interceptors(null_interceptor):
    transport = transports.MetastoreServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.MetastoreServiceRestInterceptor(),
    )
    client = MetastoreServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.MetastoreServiceRestInterceptor, "pre_delete_lock"
    ) as pre:
        pre.assert_not_called()
        pb_message = metastore.DeleteLockRequest.pb(metastore.DeleteLockRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()

        request = metastore.DeleteLockRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_lock(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_delete_lock_rest_bad_request(
    transport: str = "rest", request_type=metastore.DeleteLockRequest
):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4/locks/sample5"
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
        client.delete_lock(request)


def test_delete_lock_rest_flattened():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4/locks/sample5"
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

        client.delete_lock(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha1/{name=projects/*/locations/*/catalogs/*/databases/*/locks/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_lock_rest_flattened_error(transport: str = "rest"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_lock(
            metastore.DeleteLockRequest(),
            name="name_value",
        )


def test_delete_lock_rest_error():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.CheckLockRequest,
        dict,
    ],
)
def test_check_lock_rest(request_type):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4/locks/sample5"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.Lock(
            name="name_value",
            type_=metastore.Lock.Type.EXCLUSIVE,
            state=metastore.Lock.State.WAITING,
            table_id="table_id_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.Lock.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.check_lock(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore.Lock)
    assert response.name == "name_value"
    assert response.type_ == metastore.Lock.Type.EXCLUSIVE
    assert response.state == metastore.Lock.State.WAITING


def test_check_lock_rest_required_fields(request_type=metastore.CheckLockRequest):
    transport_class = transports.MetastoreServiceRestTransport

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
    ).check_lock._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).check_lock._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = metastore.Lock()
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

            pb_return_value = metastore.Lock.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.check_lock(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_check_lock_rest_unset_required_fields():
    transport = transports.MetastoreServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.check_lock._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_check_lock_rest_interceptors(null_interceptor):
    transport = transports.MetastoreServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.MetastoreServiceRestInterceptor(),
    )
    client = MetastoreServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.MetastoreServiceRestInterceptor, "post_check_lock"
    ) as post, mock.patch.object(
        transports.MetastoreServiceRestInterceptor, "pre_check_lock"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore.CheckLockRequest.pb(metastore.CheckLockRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = metastore.Lock.to_json(metastore.Lock())

        request = metastore.CheckLockRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = metastore.Lock()

        client.check_lock(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_check_lock_rest_bad_request(
    transport: str = "rest", request_type=metastore.CheckLockRequest
):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4/locks/sample5"
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
        client.check_lock(request)


def test_check_lock_rest_flattened():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.Lock()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4/locks/sample5"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.Lock.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.check_lock(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha1/{name=projects/*/locations/*/catalogs/*/databases/*/locks/*}:check"
            % client.transport._host,
            args[1],
        )


def test_check_lock_rest_flattened_error(transport: str = "rest"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.check_lock(
            metastore.CheckLockRequest(),
            name="name_value",
        )


def test_check_lock_rest_error():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        metastore.ListLocksRequest,
        dict,
    ],
)
def test_list_locks_rest(request_type):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.ListLocksResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.ListLocksResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_locks(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListLocksPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_locks_rest_required_fields(request_type=metastore.ListLocksRequest):
    transport_class = transports.MetastoreServiceRestTransport

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
    ).list_locks._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_locks._get_unset_required_fields(jsonified_request)
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

    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = metastore.ListLocksResponse()
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

            pb_return_value = metastore.ListLocksResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_locks(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_locks_rest_unset_required_fields():
    transport = transports.MetastoreServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_locks._get_unset_required_fields({})
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
def test_list_locks_rest_interceptors(null_interceptor):
    transport = transports.MetastoreServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.MetastoreServiceRestInterceptor(),
    )
    client = MetastoreServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.MetastoreServiceRestInterceptor, "post_list_locks"
    ) as post, mock.patch.object(
        transports.MetastoreServiceRestInterceptor, "pre_list_locks"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore.ListLocksRequest.pb(metastore.ListLocksRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = metastore.ListLocksResponse.to_json(
            metastore.ListLocksResponse()
        )

        request = metastore.ListLocksRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = metastore.ListLocksResponse()

        client.list_locks(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_locks_rest_bad_request(
    transport: str = "rest", request_type=metastore.ListLocksRequest
):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "parent": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4"
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
        client.list_locks(request)


def test_list_locks_rest_flattened():
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore.ListLocksResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = metastore.ListLocksResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_locks(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha1/{parent=projects/*/locations/*/catalogs/*/databases/*}/locks"
            % client.transport._host,
            args[1],
        )


def test_list_locks_rest_flattened_error(transport: str = "rest"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_locks(
            metastore.ListLocksRequest(),
            parent="parent_value",
        )


def test_list_locks_rest_pager(transport: str = "rest"):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            metastore.ListLocksResponse(
                locks=[
                    metastore.Lock(),
                    metastore.Lock(),
                    metastore.Lock(),
                ],
                next_page_token="abc",
            ),
            metastore.ListLocksResponse(
                locks=[],
                next_page_token="def",
            ),
            metastore.ListLocksResponse(
                locks=[
                    metastore.Lock(),
                ],
                next_page_token="ghi",
            ),
            metastore.ListLocksResponse(
                locks=[
                    metastore.Lock(),
                    metastore.Lock(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(metastore.ListLocksResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/catalogs/sample3/databases/sample4"
        }

        pager = client.list_locks(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, metastore.Lock) for i in results)

        pages = list(client.list_locks(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.MetastoreServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = MetastoreServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.MetastoreServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = MetastoreServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.MetastoreServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = MetastoreServiceClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = MetastoreServiceClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.MetastoreServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = MetastoreServiceClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.MetastoreServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = MetastoreServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.MetastoreServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.MetastoreServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.MetastoreServiceGrpcTransport,
        transports.MetastoreServiceGrpcAsyncIOTransport,
        transports.MetastoreServiceRestTransport,
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
    transport = MetastoreServiceClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.MetastoreServiceGrpcTransport,
    )


def test_metastore_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.MetastoreServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_metastore_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.bigquery_biglake_v1alpha1.services.metastore_service.transports.MetastoreServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.MetastoreServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_catalog",
        "delete_catalog",
        "get_catalog",
        "list_catalogs",
        "create_database",
        "delete_database",
        "update_database",
        "get_database",
        "list_databases",
        "create_table",
        "delete_table",
        "update_table",
        "rename_table",
        "get_table",
        "list_tables",
        "create_lock",
        "delete_lock",
        "check_lock",
        "list_locks",
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


def test_metastore_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.bigquery_biglake_v1alpha1.services.metastore_service.transports.MetastoreServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.MetastoreServiceTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/bigquery",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id="octopus",
        )


def test_metastore_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.bigquery_biglake_v1alpha1.services.metastore_service.transports.MetastoreServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.MetastoreServiceTransport()
        adc.assert_called_once()


def test_metastore_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        MetastoreServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/bigquery",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.MetastoreServiceGrpcTransport,
        transports.MetastoreServiceGrpcAsyncIOTransport,
    ],
)
def test_metastore_service_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=(
                "https://www.googleapis.com/auth/bigquery",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.MetastoreServiceGrpcTransport,
        transports.MetastoreServiceGrpcAsyncIOTransport,
        transports.MetastoreServiceRestTransport,
    ],
)
def test_metastore_service_transport_auth_gdch_credentials(transport_class):
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
        (transports.MetastoreServiceGrpcTransport, grpc_helpers),
        (transports.MetastoreServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_metastore_service_transport_create_channel(transport_class, grpc_helpers):
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
            "biglake.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=(
                "https://www.googleapis.com/auth/bigquery",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            scopes=["1", "2"],
            default_host="biglake.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.MetastoreServiceGrpcTransport,
        transports.MetastoreServiceGrpcAsyncIOTransport,
    ],
)
def test_metastore_service_grpc_transport_client_cert_source_for_mtls(transport_class):
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


def test_metastore_service_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.MetastoreServiceRestTransport(
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
def test_metastore_service_host_no_port(transport_name):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="biglake.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "biglake.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://biglake.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_metastore_service_host_with_port(transport_name):
    client = MetastoreServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="biglake.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "biglake.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://biglake.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_metastore_service_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = MetastoreServiceClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = MetastoreServiceClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.create_catalog._session
    session2 = client2.transport.create_catalog._session
    assert session1 != session2
    session1 = client1.transport.delete_catalog._session
    session2 = client2.transport.delete_catalog._session
    assert session1 != session2
    session1 = client1.transport.get_catalog._session
    session2 = client2.transport.get_catalog._session
    assert session1 != session2
    session1 = client1.transport.list_catalogs._session
    session2 = client2.transport.list_catalogs._session
    assert session1 != session2
    session1 = client1.transport.create_database._session
    session2 = client2.transport.create_database._session
    assert session1 != session2
    session1 = client1.transport.delete_database._session
    session2 = client2.transport.delete_database._session
    assert session1 != session2
    session1 = client1.transport.update_database._session
    session2 = client2.transport.update_database._session
    assert session1 != session2
    session1 = client1.transport.get_database._session
    session2 = client2.transport.get_database._session
    assert session1 != session2
    session1 = client1.transport.list_databases._session
    session2 = client2.transport.list_databases._session
    assert session1 != session2
    session1 = client1.transport.create_table._session
    session2 = client2.transport.create_table._session
    assert session1 != session2
    session1 = client1.transport.delete_table._session
    session2 = client2.transport.delete_table._session
    assert session1 != session2
    session1 = client1.transport.update_table._session
    session2 = client2.transport.update_table._session
    assert session1 != session2
    session1 = client1.transport.rename_table._session
    session2 = client2.transport.rename_table._session
    assert session1 != session2
    session1 = client1.transport.get_table._session
    session2 = client2.transport.get_table._session
    assert session1 != session2
    session1 = client1.transport.list_tables._session
    session2 = client2.transport.list_tables._session
    assert session1 != session2
    session1 = client1.transport.create_lock._session
    session2 = client2.transport.create_lock._session
    assert session1 != session2
    session1 = client1.transport.delete_lock._session
    session2 = client2.transport.delete_lock._session
    assert session1 != session2
    session1 = client1.transport.check_lock._session
    session2 = client2.transport.check_lock._session
    assert session1 != session2
    session1 = client1.transport.list_locks._session
    session2 = client2.transport.list_locks._session
    assert session1 != session2


def test_metastore_service_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.MetastoreServiceGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_metastore_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.MetastoreServiceGrpcAsyncIOTransport(
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
        transports.MetastoreServiceGrpcTransport,
        transports.MetastoreServiceGrpcAsyncIOTransport,
    ],
)
def test_metastore_service_transport_channel_mtls_with_client_cert_source(
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
        transports.MetastoreServiceGrpcTransport,
        transports.MetastoreServiceGrpcAsyncIOTransport,
    ],
)
def test_metastore_service_transport_channel_mtls_with_adc(transport_class):
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
    project = "squid"
    location = "clam"
    catalog = "whelk"
    expected = "projects/{project}/locations/{location}/catalogs/{catalog}".format(
        project=project,
        location=location,
        catalog=catalog,
    )
    actual = MetastoreServiceClient.catalog_path(project, location, catalog)
    assert expected == actual


def test_parse_catalog_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "catalog": "nudibranch",
    }
    path = MetastoreServiceClient.catalog_path(**expected)

    # Check that the path construction is reversible.
    actual = MetastoreServiceClient.parse_catalog_path(path)
    assert expected == actual


def test_database_path():
    project = "cuttlefish"
    location = "mussel"
    catalog = "winkle"
    database = "nautilus"
    expected = "projects/{project}/locations/{location}/catalogs/{catalog}/databases/{database}".format(
        project=project,
        location=location,
        catalog=catalog,
        database=database,
    )
    actual = MetastoreServiceClient.database_path(project, location, catalog, database)
    assert expected == actual


def test_parse_database_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
        "catalog": "squid",
        "database": "clam",
    }
    path = MetastoreServiceClient.database_path(**expected)

    # Check that the path construction is reversible.
    actual = MetastoreServiceClient.parse_database_path(path)
    assert expected == actual


def test_lock_path():
    project = "whelk"
    location = "octopus"
    catalog = "oyster"
    database = "nudibranch"
    lock = "cuttlefish"
    expected = "projects/{project}/locations/{location}/catalogs/{catalog}/databases/{database}/locks/{lock}".format(
        project=project,
        location=location,
        catalog=catalog,
        database=database,
        lock=lock,
    )
    actual = MetastoreServiceClient.lock_path(
        project, location, catalog, database, lock
    )
    assert expected == actual


def test_parse_lock_path():
    expected = {
        "project": "mussel",
        "location": "winkle",
        "catalog": "nautilus",
        "database": "scallop",
        "lock": "abalone",
    }
    path = MetastoreServiceClient.lock_path(**expected)

    # Check that the path construction is reversible.
    actual = MetastoreServiceClient.parse_lock_path(path)
    assert expected == actual


def test_table_path():
    project = "squid"
    location = "clam"
    catalog = "whelk"
    database = "octopus"
    table = "oyster"
    expected = "projects/{project}/locations/{location}/catalogs/{catalog}/databases/{database}/tables/{table}".format(
        project=project,
        location=location,
        catalog=catalog,
        database=database,
        table=table,
    )
    actual = MetastoreServiceClient.table_path(
        project, location, catalog, database, table
    )
    assert expected == actual


def test_parse_table_path():
    expected = {
        "project": "nudibranch",
        "location": "cuttlefish",
        "catalog": "mussel",
        "database": "winkle",
        "table": "nautilus",
    }
    path = MetastoreServiceClient.table_path(**expected)

    # Check that the path construction is reversible.
    actual = MetastoreServiceClient.parse_table_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "scallop"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = MetastoreServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "abalone",
    }
    path = MetastoreServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = MetastoreServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "squid"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = MetastoreServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "clam",
    }
    path = MetastoreServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = MetastoreServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "whelk"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = MetastoreServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "octopus",
    }
    path = MetastoreServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = MetastoreServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "oyster"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = MetastoreServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nudibranch",
    }
    path = MetastoreServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = MetastoreServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "cuttlefish"
    location = "mussel"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = MetastoreServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "winkle",
        "location": "nautilus",
    }
    path = MetastoreServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = MetastoreServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.MetastoreServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = MetastoreServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.MetastoreServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = MetastoreServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = MetastoreServiceAsyncClient(
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
        client = MetastoreServiceClient(
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
        client = MetastoreServiceClient(
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
        (MetastoreServiceClient, transports.MetastoreServiceGrpcTransport),
        (MetastoreServiceAsyncClient, transports.MetastoreServiceGrpcAsyncIOTransport),
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
