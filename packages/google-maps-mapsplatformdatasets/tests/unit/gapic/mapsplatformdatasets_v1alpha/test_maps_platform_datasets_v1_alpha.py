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

from google.maps.mapsplatformdatasets_v1alpha.services.maps_platform_datasets_v1_alpha import (
    MapsPlatformDatasetsV1AlphaAsyncClient,
    MapsPlatformDatasetsV1AlphaClient,
    pagers,
    transports,
)
from google.maps.mapsplatformdatasets_v1alpha.types import dataset as gmm_dataset
from google.maps.mapsplatformdatasets_v1alpha.types import maps_platform_datasets
from google.maps.mapsplatformdatasets_v1alpha.types import data_source
from google.maps.mapsplatformdatasets_v1alpha.types import dataset


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

    assert MapsPlatformDatasetsV1AlphaClient._get_default_mtls_endpoint(None) is None
    assert (
        MapsPlatformDatasetsV1AlphaClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        MapsPlatformDatasetsV1AlphaClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        MapsPlatformDatasetsV1AlphaClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        MapsPlatformDatasetsV1AlphaClient._get_default_mtls_endpoint(
            sandbox_mtls_endpoint
        )
        == sandbox_mtls_endpoint
    )
    assert (
        MapsPlatformDatasetsV1AlphaClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (MapsPlatformDatasetsV1AlphaClient, "grpc"),
        (MapsPlatformDatasetsV1AlphaAsyncClient, "grpc_asyncio"),
        (MapsPlatformDatasetsV1AlphaClient, "rest"),
    ],
)
def test_maps_platform_datasets_v1_alpha_client_from_service_account_info(
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
            "mapsplatformdatasets.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://mapsplatformdatasets.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.MapsPlatformDatasetsV1AlphaGrpcTransport, "grpc"),
        (transports.MapsPlatformDatasetsV1AlphaGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.MapsPlatformDatasetsV1AlphaRestTransport, "rest"),
    ],
)
def test_maps_platform_datasets_v1_alpha_client_service_account_always_use_jwt(
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
        (MapsPlatformDatasetsV1AlphaClient, "grpc"),
        (MapsPlatformDatasetsV1AlphaAsyncClient, "grpc_asyncio"),
        (MapsPlatformDatasetsV1AlphaClient, "rest"),
    ],
)
def test_maps_platform_datasets_v1_alpha_client_from_service_account_file(
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
            "mapsplatformdatasets.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://mapsplatformdatasets.googleapis.com"
        )


def test_maps_platform_datasets_v1_alpha_client_get_transport_class():
    transport = MapsPlatformDatasetsV1AlphaClient.get_transport_class()
    available_transports = [
        transports.MapsPlatformDatasetsV1AlphaGrpcTransport,
        transports.MapsPlatformDatasetsV1AlphaRestTransport,
    ]
    assert transport in available_transports

    transport = MapsPlatformDatasetsV1AlphaClient.get_transport_class("grpc")
    assert transport == transports.MapsPlatformDatasetsV1AlphaGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            MapsPlatformDatasetsV1AlphaClient,
            transports.MapsPlatformDatasetsV1AlphaGrpcTransport,
            "grpc",
        ),
        (
            MapsPlatformDatasetsV1AlphaAsyncClient,
            transports.MapsPlatformDatasetsV1AlphaGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (
            MapsPlatformDatasetsV1AlphaClient,
            transports.MapsPlatformDatasetsV1AlphaRestTransport,
            "rest",
        ),
    ],
)
@mock.patch.object(
    MapsPlatformDatasetsV1AlphaClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(MapsPlatformDatasetsV1AlphaClient),
)
@mock.patch.object(
    MapsPlatformDatasetsV1AlphaAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(MapsPlatformDatasetsV1AlphaAsyncClient),
)
def test_maps_platform_datasets_v1_alpha_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(
        MapsPlatformDatasetsV1AlphaClient, "get_transport_class"
    ) as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(
        MapsPlatformDatasetsV1AlphaClient, "get_transport_class"
    ) as gtc:
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
            MapsPlatformDatasetsV1AlphaClient,
            transports.MapsPlatformDatasetsV1AlphaGrpcTransport,
            "grpc",
            "true",
        ),
        (
            MapsPlatformDatasetsV1AlphaAsyncClient,
            transports.MapsPlatformDatasetsV1AlphaGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            MapsPlatformDatasetsV1AlphaClient,
            transports.MapsPlatformDatasetsV1AlphaGrpcTransport,
            "grpc",
            "false",
        ),
        (
            MapsPlatformDatasetsV1AlphaAsyncClient,
            transports.MapsPlatformDatasetsV1AlphaGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (
            MapsPlatformDatasetsV1AlphaClient,
            transports.MapsPlatformDatasetsV1AlphaRestTransport,
            "rest",
            "true",
        ),
        (
            MapsPlatformDatasetsV1AlphaClient,
            transports.MapsPlatformDatasetsV1AlphaRestTransport,
            "rest",
            "false",
        ),
    ],
)
@mock.patch.object(
    MapsPlatformDatasetsV1AlphaClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(MapsPlatformDatasetsV1AlphaClient),
)
@mock.patch.object(
    MapsPlatformDatasetsV1AlphaAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(MapsPlatformDatasetsV1AlphaAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_maps_platform_datasets_v1_alpha_client_mtls_env_auto(
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
    "client_class",
    [MapsPlatformDatasetsV1AlphaClient, MapsPlatformDatasetsV1AlphaAsyncClient],
)
@mock.patch.object(
    MapsPlatformDatasetsV1AlphaClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(MapsPlatformDatasetsV1AlphaClient),
)
@mock.patch.object(
    MapsPlatformDatasetsV1AlphaAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(MapsPlatformDatasetsV1AlphaAsyncClient),
)
def test_maps_platform_datasets_v1_alpha_client_get_mtls_endpoint_and_cert_source(
    client_class,
):
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
        (
            MapsPlatformDatasetsV1AlphaClient,
            transports.MapsPlatformDatasetsV1AlphaGrpcTransport,
            "grpc",
        ),
        (
            MapsPlatformDatasetsV1AlphaAsyncClient,
            transports.MapsPlatformDatasetsV1AlphaGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (
            MapsPlatformDatasetsV1AlphaClient,
            transports.MapsPlatformDatasetsV1AlphaRestTransport,
            "rest",
        ),
    ],
)
def test_maps_platform_datasets_v1_alpha_client_client_options_scopes(
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
            MapsPlatformDatasetsV1AlphaClient,
            transports.MapsPlatformDatasetsV1AlphaGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            MapsPlatformDatasetsV1AlphaAsyncClient,
            transports.MapsPlatformDatasetsV1AlphaGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (
            MapsPlatformDatasetsV1AlphaClient,
            transports.MapsPlatformDatasetsV1AlphaRestTransport,
            "rest",
            None,
        ),
    ],
)
def test_maps_platform_datasets_v1_alpha_client_client_options_credentials_file(
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


def test_maps_platform_datasets_v1_alpha_client_client_options_from_dict():
    with mock.patch(
        "google.maps.mapsplatformdatasets_v1alpha.services.maps_platform_datasets_v1_alpha.transports.MapsPlatformDatasetsV1AlphaGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = MapsPlatformDatasetsV1AlphaClient(
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
            MapsPlatformDatasetsV1AlphaClient,
            transports.MapsPlatformDatasetsV1AlphaGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            MapsPlatformDatasetsV1AlphaAsyncClient,
            transports.MapsPlatformDatasetsV1AlphaGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_maps_platform_datasets_v1_alpha_client_create_channel_credentials_file(
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
            "mapsplatformdatasets.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="mapsplatformdatasets.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        maps_platform_datasets.CreateDatasetRequest,
        dict,
    ],
)
def test_create_dataset(request_type, transport: str = "grpc"):
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_dataset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gmm_dataset.Dataset(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            version_id="version_id_value",
            usage=[gmm_dataset.Usage.USAGE_DATA_DRIVEN_STYLING],
            status=gmm_dataset.State.STATE_IMPORTING,
            version_description="version_description_value",
        )
        response = client.create_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == maps_platform_datasets.CreateDatasetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gmm_dataset.Dataset)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.version_id == "version_id_value"
    assert response.usage == [gmm_dataset.Usage.USAGE_DATA_DRIVEN_STYLING]
    assert response.status == gmm_dataset.State.STATE_IMPORTING
    assert response.version_description == "version_description_value"


def test_create_dataset_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_dataset), "__call__") as call:
        client.create_dataset()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == maps_platform_datasets.CreateDatasetRequest()


@pytest.mark.asyncio
async def test_create_dataset_async(
    transport: str = "grpc_asyncio",
    request_type=maps_platform_datasets.CreateDatasetRequest,
):
    client = MapsPlatformDatasetsV1AlphaAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_dataset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gmm_dataset.Dataset(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                version_id="version_id_value",
                usage=[gmm_dataset.Usage.USAGE_DATA_DRIVEN_STYLING],
                status=gmm_dataset.State.STATE_IMPORTING,
                version_description="version_description_value",
            )
        )
        response = await client.create_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == maps_platform_datasets.CreateDatasetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gmm_dataset.Dataset)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.version_id == "version_id_value"
    assert response.usage == [gmm_dataset.Usage.USAGE_DATA_DRIVEN_STYLING]
    assert response.status == gmm_dataset.State.STATE_IMPORTING
    assert response.version_description == "version_description_value"


@pytest.mark.asyncio
async def test_create_dataset_async_from_dict():
    await test_create_dataset_async(request_type=dict)


def test_create_dataset_field_headers():
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = maps_platform_datasets.CreateDatasetRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_dataset), "__call__") as call:
        call.return_value = gmm_dataset.Dataset()
        client.create_dataset(request)

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
async def test_create_dataset_field_headers_async():
    client = MapsPlatformDatasetsV1AlphaAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = maps_platform_datasets.CreateDatasetRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_dataset), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gmm_dataset.Dataset())
        await client.create_dataset(request)

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


def test_create_dataset_flattened():
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_dataset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gmm_dataset.Dataset()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_dataset(
            parent="parent_value",
            dataset=gmm_dataset.Dataset(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].dataset
        mock_val = gmm_dataset.Dataset(name="name_value")
        assert arg == mock_val


def test_create_dataset_flattened_error():
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_dataset(
            maps_platform_datasets.CreateDatasetRequest(),
            parent="parent_value",
            dataset=gmm_dataset.Dataset(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_dataset_flattened_async():
    client = MapsPlatformDatasetsV1AlphaAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_dataset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gmm_dataset.Dataset()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gmm_dataset.Dataset())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_dataset(
            parent="parent_value",
            dataset=gmm_dataset.Dataset(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].dataset
        mock_val = gmm_dataset.Dataset(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_dataset_flattened_error_async():
    client = MapsPlatformDatasetsV1AlphaAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_dataset(
            maps_platform_datasets.CreateDatasetRequest(),
            parent="parent_value",
            dataset=gmm_dataset.Dataset(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        maps_platform_datasets.UpdateDatasetMetadataRequest,
        dict,
    ],
)
def test_update_dataset_metadata(request_type, transport: str = "grpc"):
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_dataset_metadata), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gmm_dataset.Dataset(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            version_id="version_id_value",
            usage=[gmm_dataset.Usage.USAGE_DATA_DRIVEN_STYLING],
            status=gmm_dataset.State.STATE_IMPORTING,
            version_description="version_description_value",
        )
        response = client.update_dataset_metadata(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == maps_platform_datasets.UpdateDatasetMetadataRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gmm_dataset.Dataset)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.version_id == "version_id_value"
    assert response.usage == [gmm_dataset.Usage.USAGE_DATA_DRIVEN_STYLING]
    assert response.status == gmm_dataset.State.STATE_IMPORTING
    assert response.version_description == "version_description_value"


def test_update_dataset_metadata_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_dataset_metadata), "__call__"
    ) as call:
        client.update_dataset_metadata()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == maps_platform_datasets.UpdateDatasetMetadataRequest()


@pytest.mark.asyncio
async def test_update_dataset_metadata_async(
    transport: str = "grpc_asyncio",
    request_type=maps_platform_datasets.UpdateDatasetMetadataRequest,
):
    client = MapsPlatformDatasetsV1AlphaAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_dataset_metadata), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gmm_dataset.Dataset(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                version_id="version_id_value",
                usage=[gmm_dataset.Usage.USAGE_DATA_DRIVEN_STYLING],
                status=gmm_dataset.State.STATE_IMPORTING,
                version_description="version_description_value",
            )
        )
        response = await client.update_dataset_metadata(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == maps_platform_datasets.UpdateDatasetMetadataRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gmm_dataset.Dataset)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.version_id == "version_id_value"
    assert response.usage == [gmm_dataset.Usage.USAGE_DATA_DRIVEN_STYLING]
    assert response.status == gmm_dataset.State.STATE_IMPORTING
    assert response.version_description == "version_description_value"


@pytest.mark.asyncio
async def test_update_dataset_metadata_async_from_dict():
    await test_update_dataset_metadata_async(request_type=dict)


def test_update_dataset_metadata_field_headers():
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = maps_platform_datasets.UpdateDatasetMetadataRequest()

    request.dataset.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_dataset_metadata), "__call__"
    ) as call:
        call.return_value = gmm_dataset.Dataset()
        client.update_dataset_metadata(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "dataset.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_dataset_metadata_field_headers_async():
    client = MapsPlatformDatasetsV1AlphaAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = maps_platform_datasets.UpdateDatasetMetadataRequest()

    request.dataset.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_dataset_metadata), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gmm_dataset.Dataset())
        await client.update_dataset_metadata(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "dataset.name=name_value",
    ) in kw["metadata"]


def test_update_dataset_metadata_flattened():
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_dataset_metadata), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gmm_dataset.Dataset()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_dataset_metadata(
            dataset=gmm_dataset.Dataset(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].dataset
        mock_val = gmm_dataset.Dataset(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_dataset_metadata_flattened_error():
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_dataset_metadata(
            maps_platform_datasets.UpdateDatasetMetadataRequest(),
            dataset=gmm_dataset.Dataset(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_dataset_metadata_flattened_async():
    client = MapsPlatformDatasetsV1AlphaAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_dataset_metadata), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gmm_dataset.Dataset()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gmm_dataset.Dataset())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_dataset_metadata(
            dataset=gmm_dataset.Dataset(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].dataset
        mock_val = gmm_dataset.Dataset(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_dataset_metadata_flattened_error_async():
    client = MapsPlatformDatasetsV1AlphaAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_dataset_metadata(
            maps_platform_datasets.UpdateDatasetMetadataRequest(),
            dataset=gmm_dataset.Dataset(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        maps_platform_datasets.GetDatasetRequest,
        dict,
    ],
)
def test_get_dataset(request_type, transport: str = "grpc"):
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_dataset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataset.Dataset(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            version_id="version_id_value",
            usage=[dataset.Usage.USAGE_DATA_DRIVEN_STYLING],
            status=dataset.State.STATE_IMPORTING,
            version_description="version_description_value",
        )
        response = client.get_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == maps_platform_datasets.GetDatasetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataset.Dataset)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.version_id == "version_id_value"
    assert response.usage == [dataset.Usage.USAGE_DATA_DRIVEN_STYLING]
    assert response.status == dataset.State.STATE_IMPORTING
    assert response.version_description == "version_description_value"


def test_get_dataset_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_dataset), "__call__") as call:
        client.get_dataset()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == maps_platform_datasets.GetDatasetRequest()


@pytest.mark.asyncio
async def test_get_dataset_async(
    transport: str = "grpc_asyncio",
    request_type=maps_platform_datasets.GetDatasetRequest,
):
    client = MapsPlatformDatasetsV1AlphaAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_dataset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataset.Dataset(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                version_id="version_id_value",
                usage=[dataset.Usage.USAGE_DATA_DRIVEN_STYLING],
                status=dataset.State.STATE_IMPORTING,
                version_description="version_description_value",
            )
        )
        response = await client.get_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == maps_platform_datasets.GetDatasetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataset.Dataset)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.version_id == "version_id_value"
    assert response.usage == [dataset.Usage.USAGE_DATA_DRIVEN_STYLING]
    assert response.status == dataset.State.STATE_IMPORTING
    assert response.version_description == "version_description_value"


@pytest.mark.asyncio
async def test_get_dataset_async_from_dict():
    await test_get_dataset_async(request_type=dict)


def test_get_dataset_field_headers():
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = maps_platform_datasets.GetDatasetRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_dataset), "__call__") as call:
        call.return_value = dataset.Dataset()
        client.get_dataset(request)

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
async def test_get_dataset_field_headers_async():
    client = MapsPlatformDatasetsV1AlphaAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = maps_platform_datasets.GetDatasetRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_dataset), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dataset.Dataset())
        await client.get_dataset(request)

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


def test_get_dataset_flattened():
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_dataset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataset.Dataset()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_dataset(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_dataset_flattened_error():
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_dataset(
            maps_platform_datasets.GetDatasetRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_dataset_flattened_async():
    client = MapsPlatformDatasetsV1AlphaAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_dataset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataset.Dataset()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dataset.Dataset())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_dataset(
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
async def test_get_dataset_flattened_error_async():
    client = MapsPlatformDatasetsV1AlphaAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_dataset(
            maps_platform_datasets.GetDatasetRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        maps_platform_datasets.ListDatasetVersionsRequest,
        dict,
    ],
)
def test_list_dataset_versions(request_type, transport: str = "grpc"):
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_dataset_versions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = maps_platform_datasets.ListDatasetVersionsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_dataset_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == maps_platform_datasets.ListDatasetVersionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDatasetVersionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_dataset_versions_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_dataset_versions), "__call__"
    ) as call:
        client.list_dataset_versions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == maps_platform_datasets.ListDatasetVersionsRequest()


@pytest.mark.asyncio
async def test_list_dataset_versions_async(
    transport: str = "grpc_asyncio",
    request_type=maps_platform_datasets.ListDatasetVersionsRequest,
):
    client = MapsPlatformDatasetsV1AlphaAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_dataset_versions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            maps_platform_datasets.ListDatasetVersionsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_dataset_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == maps_platform_datasets.ListDatasetVersionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDatasetVersionsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_dataset_versions_async_from_dict():
    await test_list_dataset_versions_async(request_type=dict)


def test_list_dataset_versions_field_headers():
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = maps_platform_datasets.ListDatasetVersionsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_dataset_versions), "__call__"
    ) as call:
        call.return_value = maps_platform_datasets.ListDatasetVersionsResponse()
        client.list_dataset_versions(request)

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
async def test_list_dataset_versions_field_headers_async():
    client = MapsPlatformDatasetsV1AlphaAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = maps_platform_datasets.ListDatasetVersionsRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_dataset_versions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            maps_platform_datasets.ListDatasetVersionsResponse()
        )
        await client.list_dataset_versions(request)

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


def test_list_dataset_versions_flattened():
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_dataset_versions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = maps_platform_datasets.ListDatasetVersionsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_dataset_versions(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_list_dataset_versions_flattened_error():
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_dataset_versions(
            maps_platform_datasets.ListDatasetVersionsRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_list_dataset_versions_flattened_async():
    client = MapsPlatformDatasetsV1AlphaAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_dataset_versions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = maps_platform_datasets.ListDatasetVersionsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            maps_platform_datasets.ListDatasetVersionsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_dataset_versions(
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
async def test_list_dataset_versions_flattened_error_async():
    client = MapsPlatformDatasetsV1AlphaAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_dataset_versions(
            maps_platform_datasets.ListDatasetVersionsRequest(),
            name="name_value",
        )


def test_list_dataset_versions_pager(transport_name: str = "grpc"):
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_dataset_versions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            maps_platform_datasets.ListDatasetVersionsResponse(
                datasets=[
                    dataset.Dataset(),
                    dataset.Dataset(),
                    dataset.Dataset(),
                ],
                next_page_token="abc",
            ),
            maps_platform_datasets.ListDatasetVersionsResponse(
                datasets=[],
                next_page_token="def",
            ),
            maps_platform_datasets.ListDatasetVersionsResponse(
                datasets=[
                    dataset.Dataset(),
                ],
                next_page_token="ghi",
            ),
            maps_platform_datasets.ListDatasetVersionsResponse(
                datasets=[
                    dataset.Dataset(),
                    dataset.Dataset(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", ""),)),
        )
        pager = client.list_dataset_versions(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, dataset.Dataset) for i in results)


def test_list_dataset_versions_pages(transport_name: str = "grpc"):
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_dataset_versions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            maps_platform_datasets.ListDatasetVersionsResponse(
                datasets=[
                    dataset.Dataset(),
                    dataset.Dataset(),
                    dataset.Dataset(),
                ],
                next_page_token="abc",
            ),
            maps_platform_datasets.ListDatasetVersionsResponse(
                datasets=[],
                next_page_token="def",
            ),
            maps_platform_datasets.ListDatasetVersionsResponse(
                datasets=[
                    dataset.Dataset(),
                ],
                next_page_token="ghi",
            ),
            maps_platform_datasets.ListDatasetVersionsResponse(
                datasets=[
                    dataset.Dataset(),
                    dataset.Dataset(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_dataset_versions(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_dataset_versions_async_pager():
    client = MapsPlatformDatasetsV1AlphaAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_dataset_versions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            maps_platform_datasets.ListDatasetVersionsResponse(
                datasets=[
                    dataset.Dataset(),
                    dataset.Dataset(),
                    dataset.Dataset(),
                ],
                next_page_token="abc",
            ),
            maps_platform_datasets.ListDatasetVersionsResponse(
                datasets=[],
                next_page_token="def",
            ),
            maps_platform_datasets.ListDatasetVersionsResponse(
                datasets=[
                    dataset.Dataset(),
                ],
                next_page_token="ghi",
            ),
            maps_platform_datasets.ListDatasetVersionsResponse(
                datasets=[
                    dataset.Dataset(),
                    dataset.Dataset(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_dataset_versions(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, dataset.Dataset) for i in responses)


@pytest.mark.asyncio
async def test_list_dataset_versions_async_pages():
    client = MapsPlatformDatasetsV1AlphaAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_dataset_versions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            maps_platform_datasets.ListDatasetVersionsResponse(
                datasets=[
                    dataset.Dataset(),
                    dataset.Dataset(),
                    dataset.Dataset(),
                ],
                next_page_token="abc",
            ),
            maps_platform_datasets.ListDatasetVersionsResponse(
                datasets=[],
                next_page_token="def",
            ),
            maps_platform_datasets.ListDatasetVersionsResponse(
                datasets=[
                    dataset.Dataset(),
                ],
                next_page_token="ghi",
            ),
            maps_platform_datasets.ListDatasetVersionsResponse(
                datasets=[
                    dataset.Dataset(),
                    dataset.Dataset(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_dataset_versions(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        maps_platform_datasets.ListDatasetsRequest,
        dict,
    ],
)
def test_list_datasets(request_type, transport: str = "grpc"):
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_datasets), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = maps_platform_datasets.ListDatasetsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_datasets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == maps_platform_datasets.ListDatasetsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDatasetsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_datasets_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_datasets), "__call__") as call:
        client.list_datasets()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == maps_platform_datasets.ListDatasetsRequest()


@pytest.mark.asyncio
async def test_list_datasets_async(
    transport: str = "grpc_asyncio",
    request_type=maps_platform_datasets.ListDatasetsRequest,
):
    client = MapsPlatformDatasetsV1AlphaAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_datasets), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            maps_platform_datasets.ListDatasetsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_datasets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == maps_platform_datasets.ListDatasetsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDatasetsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_datasets_async_from_dict():
    await test_list_datasets_async(request_type=dict)


def test_list_datasets_field_headers():
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = maps_platform_datasets.ListDatasetsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_datasets), "__call__") as call:
        call.return_value = maps_platform_datasets.ListDatasetsResponse()
        client.list_datasets(request)

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
async def test_list_datasets_field_headers_async():
    client = MapsPlatformDatasetsV1AlphaAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = maps_platform_datasets.ListDatasetsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_datasets), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            maps_platform_datasets.ListDatasetsResponse()
        )
        await client.list_datasets(request)

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


def test_list_datasets_flattened():
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_datasets), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = maps_platform_datasets.ListDatasetsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_datasets(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_datasets_flattened_error():
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_datasets(
            maps_platform_datasets.ListDatasetsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_datasets_flattened_async():
    client = MapsPlatformDatasetsV1AlphaAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_datasets), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = maps_platform_datasets.ListDatasetsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            maps_platform_datasets.ListDatasetsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_datasets(
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
async def test_list_datasets_flattened_error_async():
    client = MapsPlatformDatasetsV1AlphaAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_datasets(
            maps_platform_datasets.ListDatasetsRequest(),
            parent="parent_value",
        )


def test_list_datasets_pager(transport_name: str = "grpc"):
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_datasets), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            maps_platform_datasets.ListDatasetsResponse(
                datasets=[
                    dataset.Dataset(),
                    dataset.Dataset(),
                    dataset.Dataset(),
                ],
                next_page_token="abc",
            ),
            maps_platform_datasets.ListDatasetsResponse(
                datasets=[],
                next_page_token="def",
            ),
            maps_platform_datasets.ListDatasetsResponse(
                datasets=[
                    dataset.Dataset(),
                ],
                next_page_token="ghi",
            ),
            maps_platform_datasets.ListDatasetsResponse(
                datasets=[
                    dataset.Dataset(),
                    dataset.Dataset(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_datasets(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, dataset.Dataset) for i in results)


def test_list_datasets_pages(transport_name: str = "grpc"):
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_datasets), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            maps_platform_datasets.ListDatasetsResponse(
                datasets=[
                    dataset.Dataset(),
                    dataset.Dataset(),
                    dataset.Dataset(),
                ],
                next_page_token="abc",
            ),
            maps_platform_datasets.ListDatasetsResponse(
                datasets=[],
                next_page_token="def",
            ),
            maps_platform_datasets.ListDatasetsResponse(
                datasets=[
                    dataset.Dataset(),
                ],
                next_page_token="ghi",
            ),
            maps_platform_datasets.ListDatasetsResponse(
                datasets=[
                    dataset.Dataset(),
                    dataset.Dataset(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_datasets(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_datasets_async_pager():
    client = MapsPlatformDatasetsV1AlphaAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_datasets), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            maps_platform_datasets.ListDatasetsResponse(
                datasets=[
                    dataset.Dataset(),
                    dataset.Dataset(),
                    dataset.Dataset(),
                ],
                next_page_token="abc",
            ),
            maps_platform_datasets.ListDatasetsResponse(
                datasets=[],
                next_page_token="def",
            ),
            maps_platform_datasets.ListDatasetsResponse(
                datasets=[
                    dataset.Dataset(),
                ],
                next_page_token="ghi",
            ),
            maps_platform_datasets.ListDatasetsResponse(
                datasets=[
                    dataset.Dataset(),
                    dataset.Dataset(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_datasets(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, dataset.Dataset) for i in responses)


@pytest.mark.asyncio
async def test_list_datasets_async_pages():
    client = MapsPlatformDatasetsV1AlphaAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_datasets), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            maps_platform_datasets.ListDatasetsResponse(
                datasets=[
                    dataset.Dataset(),
                    dataset.Dataset(),
                    dataset.Dataset(),
                ],
                next_page_token="abc",
            ),
            maps_platform_datasets.ListDatasetsResponse(
                datasets=[],
                next_page_token="def",
            ),
            maps_platform_datasets.ListDatasetsResponse(
                datasets=[
                    dataset.Dataset(),
                ],
                next_page_token="ghi",
            ),
            maps_platform_datasets.ListDatasetsResponse(
                datasets=[
                    dataset.Dataset(),
                    dataset.Dataset(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_datasets(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        maps_platform_datasets.DeleteDatasetRequest,
        dict,
    ],
)
def test_delete_dataset(request_type, transport: str = "grpc"):
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_dataset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == maps_platform_datasets.DeleteDatasetRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_dataset_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_dataset), "__call__") as call:
        client.delete_dataset()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == maps_platform_datasets.DeleteDatasetRequest()


@pytest.mark.asyncio
async def test_delete_dataset_async(
    transport: str = "grpc_asyncio",
    request_type=maps_platform_datasets.DeleteDatasetRequest,
):
    client = MapsPlatformDatasetsV1AlphaAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_dataset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == maps_platform_datasets.DeleteDatasetRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_dataset_async_from_dict():
    await test_delete_dataset_async(request_type=dict)


def test_delete_dataset_field_headers():
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = maps_platform_datasets.DeleteDatasetRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_dataset), "__call__") as call:
        call.return_value = None
        client.delete_dataset(request)

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
async def test_delete_dataset_field_headers_async():
    client = MapsPlatformDatasetsV1AlphaAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = maps_platform_datasets.DeleteDatasetRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_dataset), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_dataset(request)

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


def test_delete_dataset_flattened():
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_dataset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_dataset(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_dataset_flattened_error():
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_dataset(
            maps_platform_datasets.DeleteDatasetRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_dataset_flattened_async():
    client = MapsPlatformDatasetsV1AlphaAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_dataset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_dataset(
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
async def test_delete_dataset_flattened_error_async():
    client = MapsPlatformDatasetsV1AlphaAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_dataset(
            maps_platform_datasets.DeleteDatasetRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        maps_platform_datasets.DeleteDatasetVersionRequest,
        dict,
    ],
)
def test_delete_dataset_version(request_type, transport: str = "grpc"):
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_dataset_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_dataset_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == maps_platform_datasets.DeleteDatasetVersionRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_dataset_version_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_dataset_version), "__call__"
    ) as call:
        client.delete_dataset_version()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == maps_platform_datasets.DeleteDatasetVersionRequest()


@pytest.mark.asyncio
async def test_delete_dataset_version_async(
    transport: str = "grpc_asyncio",
    request_type=maps_platform_datasets.DeleteDatasetVersionRequest,
):
    client = MapsPlatformDatasetsV1AlphaAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_dataset_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_dataset_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == maps_platform_datasets.DeleteDatasetVersionRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_dataset_version_async_from_dict():
    await test_delete_dataset_version_async(request_type=dict)


def test_delete_dataset_version_field_headers():
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = maps_platform_datasets.DeleteDatasetVersionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_dataset_version), "__call__"
    ) as call:
        call.return_value = None
        client.delete_dataset_version(request)

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
async def test_delete_dataset_version_field_headers_async():
    client = MapsPlatformDatasetsV1AlphaAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = maps_platform_datasets.DeleteDatasetVersionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_dataset_version), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_dataset_version(request)

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


def test_delete_dataset_version_flattened():
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_dataset_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_dataset_version(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_dataset_version_flattened_error():
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_dataset_version(
            maps_platform_datasets.DeleteDatasetVersionRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_dataset_version_flattened_async():
    client = MapsPlatformDatasetsV1AlphaAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_dataset_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_dataset_version(
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
async def test_delete_dataset_version_flattened_error_async():
    client = MapsPlatformDatasetsV1AlphaAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_dataset_version(
            maps_platform_datasets.DeleteDatasetVersionRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        maps_platform_datasets.CreateDatasetRequest,
        dict,
    ],
)
def test_create_dataset_rest(request_type):
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1"}
    request_init["dataset"] = {
        "name": "name_value",
        "display_name": "display_name_value",
        "description": "description_value",
        "version_id": "version_id_value",
        "usage": [1],
        "local_file_source": {"filename": "filename_value", "file_format": 1},
        "gcs_source": {"input_uri": "input_uri_value", "file_format": 1},
        "status": 1,
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "version_create_time": {},
        "version_description": "version_description_value",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gmm_dataset.Dataset(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            version_id="version_id_value",
            usage=[gmm_dataset.Usage.USAGE_DATA_DRIVEN_STYLING],
            status=gmm_dataset.State.STATE_IMPORTING,
            version_description="version_description_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gmm_dataset.Dataset.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_dataset(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, gmm_dataset.Dataset)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.version_id == "version_id_value"
    assert response.usage == [gmm_dataset.Usage.USAGE_DATA_DRIVEN_STYLING]
    assert response.status == gmm_dataset.State.STATE_IMPORTING
    assert response.version_description == "version_description_value"


def test_create_dataset_rest_required_fields(
    request_type=maps_platform_datasets.CreateDatasetRequest,
):
    transport_class = transports.MapsPlatformDatasetsV1AlphaRestTransport

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
    ).create_dataset._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_dataset._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gmm_dataset.Dataset()
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

            pb_return_value = gmm_dataset.Dataset.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_dataset(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_dataset_rest_unset_required_fields():
    transport = transports.MapsPlatformDatasetsV1AlphaRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_dataset._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "dataset",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_dataset_rest_interceptors(null_interceptor):
    transport = transports.MapsPlatformDatasetsV1AlphaRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.MapsPlatformDatasetsV1AlphaRestInterceptor(),
    )
    client = MapsPlatformDatasetsV1AlphaClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.MapsPlatformDatasetsV1AlphaRestInterceptor, "post_create_dataset"
    ) as post, mock.patch.object(
        transports.MapsPlatformDatasetsV1AlphaRestInterceptor, "pre_create_dataset"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = maps_platform_datasets.CreateDatasetRequest.pb(
            maps_platform_datasets.CreateDatasetRequest()
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
        req.return_value._content = gmm_dataset.Dataset.to_json(gmm_dataset.Dataset())

        request = maps_platform_datasets.CreateDatasetRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gmm_dataset.Dataset()

        client.create_dataset(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_dataset_rest_bad_request(
    transport: str = "rest", request_type=maps_platform_datasets.CreateDatasetRequest
):
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1"}
    request_init["dataset"] = {
        "name": "name_value",
        "display_name": "display_name_value",
        "description": "description_value",
        "version_id": "version_id_value",
        "usage": [1],
        "local_file_source": {"filename": "filename_value", "file_format": 1},
        "gcs_source": {"input_uri": "input_uri_value", "file_format": 1},
        "status": 1,
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "version_create_time": {},
        "version_description": "version_description_value",
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
        client.create_dataset(request)


def test_create_dataset_rest_flattened():
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gmm_dataset.Dataset()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            dataset=gmm_dataset.Dataset(name="name_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gmm_dataset.Dataset.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_dataset(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha/{parent=projects/*}/datasets" % client.transport._host, args[1]
        )


def test_create_dataset_rest_flattened_error(transport: str = "rest"):
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_dataset(
            maps_platform_datasets.CreateDatasetRequest(),
            parent="parent_value",
            dataset=gmm_dataset.Dataset(name="name_value"),
        )


def test_create_dataset_rest_error():
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        maps_platform_datasets.UpdateDatasetMetadataRequest,
        dict,
    ],
)
def test_update_dataset_metadata_rest(request_type):
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"dataset": {"name": "projects/sample1/datasets/sample2"}}
    request_init["dataset"] = {
        "name": "projects/sample1/datasets/sample2",
        "display_name": "display_name_value",
        "description": "description_value",
        "version_id": "version_id_value",
        "usage": [1],
        "local_file_source": {"filename": "filename_value", "file_format": 1},
        "gcs_source": {"input_uri": "input_uri_value", "file_format": 1},
        "status": 1,
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "version_create_time": {},
        "version_description": "version_description_value",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gmm_dataset.Dataset(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            version_id="version_id_value",
            usage=[gmm_dataset.Usage.USAGE_DATA_DRIVEN_STYLING],
            status=gmm_dataset.State.STATE_IMPORTING,
            version_description="version_description_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gmm_dataset.Dataset.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_dataset_metadata(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, gmm_dataset.Dataset)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.version_id == "version_id_value"
    assert response.usage == [gmm_dataset.Usage.USAGE_DATA_DRIVEN_STYLING]
    assert response.status == gmm_dataset.State.STATE_IMPORTING
    assert response.version_description == "version_description_value"


def test_update_dataset_metadata_rest_required_fields(
    request_type=maps_platform_datasets.UpdateDatasetMetadataRequest,
):
    transport_class = transports.MapsPlatformDatasetsV1AlphaRestTransport

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
    ).update_dataset_metadata._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_dataset_metadata._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gmm_dataset.Dataset()
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

            pb_return_value = gmm_dataset.Dataset.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_dataset_metadata(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_dataset_metadata_rest_unset_required_fields():
    transport = transports.MapsPlatformDatasetsV1AlphaRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_dataset_metadata._get_unset_required_fields({})
    assert set(unset_fields) == (set(("updateMask",)) & set(("dataset",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_dataset_metadata_rest_interceptors(null_interceptor):
    transport = transports.MapsPlatformDatasetsV1AlphaRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.MapsPlatformDatasetsV1AlphaRestInterceptor(),
    )
    client = MapsPlatformDatasetsV1AlphaClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.MapsPlatformDatasetsV1AlphaRestInterceptor,
        "post_update_dataset_metadata",
    ) as post, mock.patch.object(
        transports.MapsPlatformDatasetsV1AlphaRestInterceptor,
        "pre_update_dataset_metadata",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = maps_platform_datasets.UpdateDatasetMetadataRequest.pb(
            maps_platform_datasets.UpdateDatasetMetadataRequest()
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
        req.return_value._content = gmm_dataset.Dataset.to_json(gmm_dataset.Dataset())

        request = maps_platform_datasets.UpdateDatasetMetadataRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gmm_dataset.Dataset()

        client.update_dataset_metadata(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_dataset_metadata_rest_bad_request(
    transport: str = "rest",
    request_type=maps_platform_datasets.UpdateDatasetMetadataRequest,
):
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"dataset": {"name": "projects/sample1/datasets/sample2"}}
    request_init["dataset"] = {
        "name": "projects/sample1/datasets/sample2",
        "display_name": "display_name_value",
        "description": "description_value",
        "version_id": "version_id_value",
        "usage": [1],
        "local_file_source": {"filename": "filename_value", "file_format": 1},
        "gcs_source": {"input_uri": "input_uri_value", "file_format": 1},
        "status": 1,
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "version_create_time": {},
        "version_description": "version_description_value",
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
        client.update_dataset_metadata(request)


def test_update_dataset_metadata_rest_flattened():
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = gmm_dataset.Dataset()

        # get arguments that satisfy an http rule for this method
        sample_request = {"dataset": {"name": "projects/sample1/datasets/sample2"}}

        # get truthy value for each flattened field
        mock_args = dict(
            dataset=gmm_dataset.Dataset(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gmm_dataset.Dataset.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_dataset_metadata(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha/{dataset.name=projects/*/datasets/*}" % client.transport._host,
            args[1],
        )


def test_update_dataset_metadata_rest_flattened_error(transport: str = "rest"):
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_dataset_metadata(
            maps_platform_datasets.UpdateDatasetMetadataRequest(),
            dataset=gmm_dataset.Dataset(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_dataset_metadata_rest_error():
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        maps_platform_datasets.GetDatasetRequest,
        dict,
    ],
)
def test_get_dataset_rest(request_type):
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/datasets/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataset.Dataset(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            version_id="version_id_value",
            usage=[dataset.Usage.USAGE_DATA_DRIVEN_STYLING],
            status=dataset.State.STATE_IMPORTING,
            version_description="version_description_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataset.Dataset.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_dataset(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataset.Dataset)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.version_id == "version_id_value"
    assert response.usage == [dataset.Usage.USAGE_DATA_DRIVEN_STYLING]
    assert response.status == dataset.State.STATE_IMPORTING
    assert response.version_description == "version_description_value"


def test_get_dataset_rest_required_fields(
    request_type=maps_platform_datasets.GetDatasetRequest,
):
    transport_class = transports.MapsPlatformDatasetsV1AlphaRestTransport

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
    ).get_dataset._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_dataset._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("published_usage",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = dataset.Dataset()
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

            pb_return_value = dataset.Dataset.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_dataset(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_dataset_rest_unset_required_fields():
    transport = transports.MapsPlatformDatasetsV1AlphaRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_dataset._get_unset_required_fields({})
    assert set(unset_fields) == (set(("publishedUsage",)) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_dataset_rest_interceptors(null_interceptor):
    transport = transports.MapsPlatformDatasetsV1AlphaRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.MapsPlatformDatasetsV1AlphaRestInterceptor(),
    )
    client = MapsPlatformDatasetsV1AlphaClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.MapsPlatformDatasetsV1AlphaRestInterceptor, "post_get_dataset"
    ) as post, mock.patch.object(
        transports.MapsPlatformDatasetsV1AlphaRestInterceptor, "pre_get_dataset"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = maps_platform_datasets.GetDatasetRequest.pb(
            maps_platform_datasets.GetDatasetRequest()
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
        req.return_value._content = dataset.Dataset.to_json(dataset.Dataset())

        request = maps_platform_datasets.GetDatasetRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = dataset.Dataset()

        client.get_dataset(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_dataset_rest_bad_request(
    transport: str = "rest", request_type=maps_platform_datasets.GetDatasetRequest
):
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/datasets/sample2"}
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
        client.get_dataset(request)


def test_get_dataset_rest_flattened():
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = dataset.Dataset()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/datasets/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = dataset.Dataset.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_dataset(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha/{name=projects/*/datasets/*}" % client.transport._host, args[1]
        )


def test_get_dataset_rest_flattened_error(transport: str = "rest"):
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_dataset(
            maps_platform_datasets.GetDatasetRequest(),
            name="name_value",
        )


def test_get_dataset_rest_error():
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        maps_platform_datasets.ListDatasetVersionsRequest,
        dict,
    ],
)
def test_list_dataset_versions_rest(request_type):
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/datasets/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = maps_platform_datasets.ListDatasetVersionsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = maps_platform_datasets.ListDatasetVersionsResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_dataset_versions(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDatasetVersionsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_dataset_versions_rest_required_fields(
    request_type=maps_platform_datasets.ListDatasetVersionsRequest,
):
    transport_class = transports.MapsPlatformDatasetsV1AlphaRestTransport

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
    ).list_dataset_versions._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_dataset_versions._get_unset_required_fields(jsonified_request)
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

    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = maps_platform_datasets.ListDatasetVersionsResponse()
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

            pb_return_value = maps_platform_datasets.ListDatasetVersionsResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_dataset_versions(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_dataset_versions_rest_unset_required_fields():
    transport = transports.MapsPlatformDatasetsV1AlphaRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_dataset_versions._get_unset_required_fields({})
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
def test_list_dataset_versions_rest_interceptors(null_interceptor):
    transport = transports.MapsPlatformDatasetsV1AlphaRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.MapsPlatformDatasetsV1AlphaRestInterceptor(),
    )
    client = MapsPlatformDatasetsV1AlphaClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.MapsPlatformDatasetsV1AlphaRestInterceptor,
        "post_list_dataset_versions",
    ) as post, mock.patch.object(
        transports.MapsPlatformDatasetsV1AlphaRestInterceptor,
        "pre_list_dataset_versions",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = maps_platform_datasets.ListDatasetVersionsRequest.pb(
            maps_platform_datasets.ListDatasetVersionsRequest()
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
            maps_platform_datasets.ListDatasetVersionsResponse.to_json(
                maps_platform_datasets.ListDatasetVersionsResponse()
            )
        )

        request = maps_platform_datasets.ListDatasetVersionsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = maps_platform_datasets.ListDatasetVersionsResponse()

        client.list_dataset_versions(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_dataset_versions_rest_bad_request(
    transport: str = "rest",
    request_type=maps_platform_datasets.ListDatasetVersionsRequest,
):
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/datasets/sample2"}
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
        client.list_dataset_versions(request)


def test_list_dataset_versions_rest_flattened():
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = maps_platform_datasets.ListDatasetVersionsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/datasets/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = maps_platform_datasets.ListDatasetVersionsResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_dataset_versions(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha/{name=projects/*/datasets/*}:listVersions"
            % client.transport._host,
            args[1],
        )


def test_list_dataset_versions_rest_flattened_error(transport: str = "rest"):
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_dataset_versions(
            maps_platform_datasets.ListDatasetVersionsRequest(),
            name="name_value",
        )


def test_list_dataset_versions_rest_pager(transport: str = "rest"):
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            maps_platform_datasets.ListDatasetVersionsResponse(
                datasets=[
                    dataset.Dataset(),
                    dataset.Dataset(),
                    dataset.Dataset(),
                ],
                next_page_token="abc",
            ),
            maps_platform_datasets.ListDatasetVersionsResponse(
                datasets=[],
                next_page_token="def",
            ),
            maps_platform_datasets.ListDatasetVersionsResponse(
                datasets=[
                    dataset.Dataset(),
                ],
                next_page_token="ghi",
            ),
            maps_platform_datasets.ListDatasetVersionsResponse(
                datasets=[
                    dataset.Dataset(),
                    dataset.Dataset(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            maps_platform_datasets.ListDatasetVersionsResponse.to_json(x)
            for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"name": "projects/sample1/datasets/sample2"}

        pager = client.list_dataset_versions(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, dataset.Dataset) for i in results)

        pages = list(client.list_dataset_versions(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        maps_platform_datasets.ListDatasetsRequest,
        dict,
    ],
)
def test_list_datasets_rest(request_type):
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = maps_platform_datasets.ListDatasetsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = maps_platform_datasets.ListDatasetsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_datasets(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDatasetsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_datasets_rest_required_fields(
    request_type=maps_platform_datasets.ListDatasetsRequest,
):
    transport_class = transports.MapsPlatformDatasetsV1AlphaRestTransport

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
    ).list_datasets._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_datasets._get_unset_required_fields(jsonified_request)
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

    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = maps_platform_datasets.ListDatasetsResponse()
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

            pb_return_value = maps_platform_datasets.ListDatasetsResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_datasets(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_datasets_rest_unset_required_fields():
    transport = transports.MapsPlatformDatasetsV1AlphaRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_datasets._get_unset_required_fields({})
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
def test_list_datasets_rest_interceptors(null_interceptor):
    transport = transports.MapsPlatformDatasetsV1AlphaRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.MapsPlatformDatasetsV1AlphaRestInterceptor(),
    )
    client = MapsPlatformDatasetsV1AlphaClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.MapsPlatformDatasetsV1AlphaRestInterceptor, "post_list_datasets"
    ) as post, mock.patch.object(
        transports.MapsPlatformDatasetsV1AlphaRestInterceptor, "pre_list_datasets"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = maps_platform_datasets.ListDatasetsRequest.pb(
            maps_platform_datasets.ListDatasetsRequest()
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
        req.return_value._content = maps_platform_datasets.ListDatasetsResponse.to_json(
            maps_platform_datasets.ListDatasetsResponse()
        )

        request = maps_platform_datasets.ListDatasetsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = maps_platform_datasets.ListDatasetsResponse()

        client.list_datasets(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_datasets_rest_bad_request(
    transport: str = "rest", request_type=maps_platform_datasets.ListDatasetsRequest
):
    client = MapsPlatformDatasetsV1AlphaClient(
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
        client.list_datasets(request)


def test_list_datasets_rest_flattened():
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = maps_platform_datasets.ListDatasetsResponse()

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
        pb_return_value = maps_platform_datasets.ListDatasetsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_datasets(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha/{parent=projects/*}/datasets" % client.transport._host, args[1]
        )


def test_list_datasets_rest_flattened_error(transport: str = "rest"):
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_datasets(
            maps_platform_datasets.ListDatasetsRequest(),
            parent="parent_value",
        )


def test_list_datasets_rest_pager(transport: str = "rest"):
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            maps_platform_datasets.ListDatasetsResponse(
                datasets=[
                    dataset.Dataset(),
                    dataset.Dataset(),
                    dataset.Dataset(),
                ],
                next_page_token="abc",
            ),
            maps_platform_datasets.ListDatasetsResponse(
                datasets=[],
                next_page_token="def",
            ),
            maps_platform_datasets.ListDatasetsResponse(
                datasets=[
                    dataset.Dataset(),
                ],
                next_page_token="ghi",
            ),
            maps_platform_datasets.ListDatasetsResponse(
                datasets=[
                    dataset.Dataset(),
                    dataset.Dataset(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            maps_platform_datasets.ListDatasetsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1"}

        pager = client.list_datasets(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, dataset.Dataset) for i in results)

        pages = list(client.list_datasets(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        maps_platform_datasets.DeleteDatasetRequest,
        dict,
    ],
)
def test_delete_dataset_rest(request_type):
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/datasets/sample2"}
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
        response = client.delete_dataset(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_dataset_rest_required_fields(
    request_type=maps_platform_datasets.DeleteDatasetRequest,
):
    transport_class = transports.MapsPlatformDatasetsV1AlphaRestTransport

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
    ).delete_dataset._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_dataset._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("force",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = MapsPlatformDatasetsV1AlphaClient(
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

            response = client.delete_dataset(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_dataset_rest_unset_required_fields():
    transport = transports.MapsPlatformDatasetsV1AlphaRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_dataset._get_unset_required_fields({})
    assert set(unset_fields) == (set(("force",)) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_dataset_rest_interceptors(null_interceptor):
    transport = transports.MapsPlatformDatasetsV1AlphaRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.MapsPlatformDatasetsV1AlphaRestInterceptor(),
    )
    client = MapsPlatformDatasetsV1AlphaClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.MapsPlatformDatasetsV1AlphaRestInterceptor, "pre_delete_dataset"
    ) as pre:
        pre.assert_not_called()
        pb_message = maps_platform_datasets.DeleteDatasetRequest.pb(
            maps_platform_datasets.DeleteDatasetRequest()
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

        request = maps_platform_datasets.DeleteDatasetRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_dataset(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_delete_dataset_rest_bad_request(
    transport: str = "rest", request_type=maps_platform_datasets.DeleteDatasetRequest
):
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/datasets/sample2"}
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
        client.delete_dataset(request)


def test_delete_dataset_rest_flattened():
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/datasets/sample2"}

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

        client.delete_dataset(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha/{name=projects/*/datasets/*}" % client.transport._host, args[1]
        )


def test_delete_dataset_rest_flattened_error(transport: str = "rest"):
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_dataset(
            maps_platform_datasets.DeleteDatasetRequest(),
            name="name_value",
        )


def test_delete_dataset_rest_error():
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        maps_platform_datasets.DeleteDatasetVersionRequest,
        dict,
    ],
)
def test_delete_dataset_version_rest(request_type):
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/datasets/sample2"}
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
        response = client.delete_dataset_version(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_dataset_version_rest_required_fields(
    request_type=maps_platform_datasets.DeleteDatasetVersionRequest,
):
    transport_class = transports.MapsPlatformDatasetsV1AlphaRestTransport

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
    ).delete_dataset_version._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_dataset_version._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = MapsPlatformDatasetsV1AlphaClient(
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

            response = client.delete_dataset_version(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_dataset_version_rest_unset_required_fields():
    transport = transports.MapsPlatformDatasetsV1AlphaRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_dataset_version._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_dataset_version_rest_interceptors(null_interceptor):
    transport = transports.MapsPlatformDatasetsV1AlphaRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.MapsPlatformDatasetsV1AlphaRestInterceptor(),
    )
    client = MapsPlatformDatasetsV1AlphaClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.MapsPlatformDatasetsV1AlphaRestInterceptor,
        "pre_delete_dataset_version",
    ) as pre:
        pre.assert_not_called()
        pb_message = maps_platform_datasets.DeleteDatasetVersionRequest.pb(
            maps_platform_datasets.DeleteDatasetVersionRequest()
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

        request = maps_platform_datasets.DeleteDatasetVersionRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_dataset_version(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_delete_dataset_version_rest_bad_request(
    transport: str = "rest",
    request_type=maps_platform_datasets.DeleteDatasetVersionRequest,
):
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/datasets/sample2"}
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
        client.delete_dataset_version(request)


def test_delete_dataset_version_rest_flattened():
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/datasets/sample2"}

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

        client.delete_dataset_version(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1alpha/{name=projects/*/datasets/*}:deleteVersion"
            % client.transport._host,
            args[1],
        )


def test_delete_dataset_version_rest_flattened_error(transport: str = "rest"):
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_dataset_version(
            maps_platform_datasets.DeleteDatasetVersionRequest(),
            name="name_value",
        )


def test_delete_dataset_version_rest_error():
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.MapsPlatformDatasetsV1AlphaGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = MapsPlatformDatasetsV1AlphaClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.MapsPlatformDatasetsV1AlphaGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = MapsPlatformDatasetsV1AlphaClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.MapsPlatformDatasetsV1AlphaGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = MapsPlatformDatasetsV1AlphaClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = MapsPlatformDatasetsV1AlphaClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.MapsPlatformDatasetsV1AlphaGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = MapsPlatformDatasetsV1AlphaClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.MapsPlatformDatasetsV1AlphaGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = MapsPlatformDatasetsV1AlphaClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.MapsPlatformDatasetsV1AlphaGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.MapsPlatformDatasetsV1AlphaGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.MapsPlatformDatasetsV1AlphaGrpcTransport,
        transports.MapsPlatformDatasetsV1AlphaGrpcAsyncIOTransport,
        transports.MapsPlatformDatasetsV1AlphaRestTransport,
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
    transport = MapsPlatformDatasetsV1AlphaClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.MapsPlatformDatasetsV1AlphaGrpcTransport,
    )


def test_maps_platform_datasets_v1_alpha_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.MapsPlatformDatasetsV1AlphaTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_maps_platform_datasets_v1_alpha_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.maps.mapsplatformdatasets_v1alpha.services.maps_platform_datasets_v1_alpha.transports.MapsPlatformDatasetsV1AlphaTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.MapsPlatformDatasetsV1AlphaTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_dataset",
        "update_dataset_metadata",
        "get_dataset",
        "list_dataset_versions",
        "list_datasets",
        "delete_dataset",
        "delete_dataset_version",
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


def test_maps_platform_datasets_v1_alpha_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.maps.mapsplatformdatasets_v1alpha.services.maps_platform_datasets_v1_alpha.transports.MapsPlatformDatasetsV1AlphaTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.MapsPlatformDatasetsV1AlphaTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_maps_platform_datasets_v1_alpha_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.maps.mapsplatformdatasets_v1alpha.services.maps_platform_datasets_v1_alpha.transports.MapsPlatformDatasetsV1AlphaTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.MapsPlatformDatasetsV1AlphaTransport()
        adc.assert_called_once()


def test_maps_platform_datasets_v1_alpha_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        MapsPlatformDatasetsV1AlphaClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.MapsPlatformDatasetsV1AlphaGrpcTransport,
        transports.MapsPlatformDatasetsV1AlphaGrpcAsyncIOTransport,
    ],
)
def test_maps_platform_datasets_v1_alpha_transport_auth_adc(transport_class):
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
        transports.MapsPlatformDatasetsV1AlphaGrpcTransport,
        transports.MapsPlatformDatasetsV1AlphaGrpcAsyncIOTransport,
        transports.MapsPlatformDatasetsV1AlphaRestTransport,
    ],
)
def test_maps_platform_datasets_v1_alpha_transport_auth_gdch_credentials(
    transport_class,
):
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
        (transports.MapsPlatformDatasetsV1AlphaGrpcTransport, grpc_helpers),
        (
            transports.MapsPlatformDatasetsV1AlphaGrpcAsyncIOTransport,
            grpc_helpers_async,
        ),
    ],
)
def test_maps_platform_datasets_v1_alpha_transport_create_channel(
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
            "mapsplatformdatasets.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="mapsplatformdatasets.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.MapsPlatformDatasetsV1AlphaGrpcTransport,
        transports.MapsPlatformDatasetsV1AlphaGrpcAsyncIOTransport,
    ],
)
def test_maps_platform_datasets_v1_alpha_grpc_transport_client_cert_source_for_mtls(
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


def test_maps_platform_datasets_v1_alpha_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.MapsPlatformDatasetsV1AlphaRestTransport(
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
def test_maps_platform_datasets_v1_alpha_host_no_port(transport_name):
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="mapsplatformdatasets.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "mapsplatformdatasets.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://mapsplatformdatasets.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_maps_platform_datasets_v1_alpha_host_with_port(transport_name):
    client = MapsPlatformDatasetsV1AlphaClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="mapsplatformdatasets.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "mapsplatformdatasets.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://mapsplatformdatasets.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_maps_platform_datasets_v1_alpha_client_transport_session_collision(
    transport_name,
):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = MapsPlatformDatasetsV1AlphaClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = MapsPlatformDatasetsV1AlphaClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.create_dataset._session
    session2 = client2.transport.create_dataset._session
    assert session1 != session2
    session1 = client1.transport.update_dataset_metadata._session
    session2 = client2.transport.update_dataset_metadata._session
    assert session1 != session2
    session1 = client1.transport.get_dataset._session
    session2 = client2.transport.get_dataset._session
    assert session1 != session2
    session1 = client1.transport.list_dataset_versions._session
    session2 = client2.transport.list_dataset_versions._session
    assert session1 != session2
    session1 = client1.transport.list_datasets._session
    session2 = client2.transport.list_datasets._session
    assert session1 != session2
    session1 = client1.transport.delete_dataset._session
    session2 = client2.transport.delete_dataset._session
    assert session1 != session2
    session1 = client1.transport.delete_dataset_version._session
    session2 = client2.transport.delete_dataset_version._session
    assert session1 != session2


def test_maps_platform_datasets_v1_alpha_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.MapsPlatformDatasetsV1AlphaGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_maps_platform_datasets_v1_alpha_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.MapsPlatformDatasetsV1AlphaGrpcAsyncIOTransport(
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
        transports.MapsPlatformDatasetsV1AlphaGrpcTransport,
        transports.MapsPlatformDatasetsV1AlphaGrpcAsyncIOTransport,
    ],
)
def test_maps_platform_datasets_v1_alpha_transport_channel_mtls_with_client_cert_source(
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
        transports.MapsPlatformDatasetsV1AlphaGrpcTransport,
        transports.MapsPlatformDatasetsV1AlphaGrpcAsyncIOTransport,
    ],
)
def test_maps_platform_datasets_v1_alpha_transport_channel_mtls_with_adc(
    transport_class,
):
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


def test_dataset_path():
    project = "squid"
    dataset = "clam"
    expected = "projects/{project}/datasets/{dataset}".format(
        project=project,
        dataset=dataset,
    )
    actual = MapsPlatformDatasetsV1AlphaClient.dataset_path(project, dataset)
    assert expected == actual


def test_parse_dataset_path():
    expected = {
        "project": "whelk",
        "dataset": "octopus",
    }
    path = MapsPlatformDatasetsV1AlphaClient.dataset_path(**expected)

    # Check that the path construction is reversible.
    actual = MapsPlatformDatasetsV1AlphaClient.parse_dataset_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "oyster"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = MapsPlatformDatasetsV1AlphaClient.common_billing_account_path(
        billing_account
    )
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "nudibranch",
    }
    path = MapsPlatformDatasetsV1AlphaClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = MapsPlatformDatasetsV1AlphaClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "cuttlefish"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = MapsPlatformDatasetsV1AlphaClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "mussel",
    }
    path = MapsPlatformDatasetsV1AlphaClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = MapsPlatformDatasetsV1AlphaClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "winkle"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = MapsPlatformDatasetsV1AlphaClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nautilus",
    }
    path = MapsPlatformDatasetsV1AlphaClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = MapsPlatformDatasetsV1AlphaClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "scallop"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = MapsPlatformDatasetsV1AlphaClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "abalone",
    }
    path = MapsPlatformDatasetsV1AlphaClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = MapsPlatformDatasetsV1AlphaClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "squid"
    location = "clam"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = MapsPlatformDatasetsV1AlphaClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "whelk",
        "location": "octopus",
    }
    path = MapsPlatformDatasetsV1AlphaClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = MapsPlatformDatasetsV1AlphaClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.MapsPlatformDatasetsV1AlphaTransport, "_prep_wrapped_messages"
    ) as prep:
        client = MapsPlatformDatasetsV1AlphaClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.MapsPlatformDatasetsV1AlphaTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = MapsPlatformDatasetsV1AlphaClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = MapsPlatformDatasetsV1AlphaAsyncClient(
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
        client = MapsPlatformDatasetsV1AlphaClient(
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
        client = MapsPlatformDatasetsV1AlphaClient(
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
        (
            MapsPlatformDatasetsV1AlphaClient,
            transports.MapsPlatformDatasetsV1AlphaGrpcTransport,
        ),
        (
            MapsPlatformDatasetsV1AlphaAsyncClient,
            transports.MapsPlatformDatasetsV1AlphaGrpcAsyncIOTransport,
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
