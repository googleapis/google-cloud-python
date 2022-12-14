# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import json_format
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest
from requests import PreparedRequest, Request, Response
from requests.sessions import Session

from google.cloud.video.stitcher_v1.services.video_stitcher_service import (
    VideoStitcherServiceAsyncClient,
    VideoStitcherServiceClient,
    pagers,
    transports,
)
from google.cloud.video.stitcher_v1.types import (
    ad_tag_details,
    cdn_keys,
    companions,
    events,
    sessions,
    slates,
    stitch_details,
    video_stitcher_service,
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

    assert VideoStitcherServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        VideoStitcherServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        VideoStitcherServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        VideoStitcherServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        VideoStitcherServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        VideoStitcherServiceClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (VideoStitcherServiceClient, "grpc"),
        (VideoStitcherServiceAsyncClient, "grpc_asyncio"),
        (VideoStitcherServiceClient, "rest"),
    ],
)
def test_video_stitcher_service_client_from_service_account_info(
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
            "videostitcher.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://videostitcher.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.VideoStitcherServiceGrpcTransport, "grpc"),
        (transports.VideoStitcherServiceGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.VideoStitcherServiceRestTransport, "rest"),
    ],
)
def test_video_stitcher_service_client_service_account_always_use_jwt(
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
        (VideoStitcherServiceClient, "grpc"),
        (VideoStitcherServiceAsyncClient, "grpc_asyncio"),
        (VideoStitcherServiceClient, "rest"),
    ],
)
def test_video_stitcher_service_client_from_service_account_file(
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
            "videostitcher.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://videostitcher.googleapis.com"
        )


def test_video_stitcher_service_client_get_transport_class():
    transport = VideoStitcherServiceClient.get_transport_class()
    available_transports = [
        transports.VideoStitcherServiceGrpcTransport,
        transports.VideoStitcherServiceRestTransport,
    ]
    assert transport in available_transports

    transport = VideoStitcherServiceClient.get_transport_class("grpc")
    assert transport == transports.VideoStitcherServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            VideoStitcherServiceClient,
            transports.VideoStitcherServiceGrpcTransport,
            "grpc",
        ),
        (
            VideoStitcherServiceAsyncClient,
            transports.VideoStitcherServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (
            VideoStitcherServiceClient,
            transports.VideoStitcherServiceRestTransport,
            "rest",
        ),
    ],
)
@mock.patch.object(
    VideoStitcherServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(VideoStitcherServiceClient),
)
@mock.patch.object(
    VideoStitcherServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(VideoStitcherServiceAsyncClient),
)
def test_video_stitcher_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(VideoStitcherServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(VideoStitcherServiceClient, "get_transport_class") as gtc:
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
            VideoStitcherServiceClient,
            transports.VideoStitcherServiceGrpcTransport,
            "grpc",
            "true",
        ),
        (
            VideoStitcherServiceAsyncClient,
            transports.VideoStitcherServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            VideoStitcherServiceClient,
            transports.VideoStitcherServiceGrpcTransport,
            "grpc",
            "false",
        ),
        (
            VideoStitcherServiceAsyncClient,
            transports.VideoStitcherServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (
            VideoStitcherServiceClient,
            transports.VideoStitcherServiceRestTransport,
            "rest",
            "true",
        ),
        (
            VideoStitcherServiceClient,
            transports.VideoStitcherServiceRestTransport,
            "rest",
            "false",
        ),
    ],
)
@mock.patch.object(
    VideoStitcherServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(VideoStitcherServiceClient),
)
@mock.patch.object(
    VideoStitcherServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(VideoStitcherServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_video_stitcher_service_client_mtls_env_auto(
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
    "client_class", [VideoStitcherServiceClient, VideoStitcherServiceAsyncClient]
)
@mock.patch.object(
    VideoStitcherServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(VideoStitcherServiceClient),
)
@mock.patch.object(
    VideoStitcherServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(VideoStitcherServiceAsyncClient),
)
def test_video_stitcher_service_client_get_mtls_endpoint_and_cert_source(client_class):
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
            VideoStitcherServiceClient,
            transports.VideoStitcherServiceGrpcTransport,
            "grpc",
        ),
        (
            VideoStitcherServiceAsyncClient,
            transports.VideoStitcherServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (
            VideoStitcherServiceClient,
            transports.VideoStitcherServiceRestTransport,
            "rest",
        ),
    ],
)
def test_video_stitcher_service_client_client_options_scopes(
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
            VideoStitcherServiceClient,
            transports.VideoStitcherServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            VideoStitcherServiceAsyncClient,
            transports.VideoStitcherServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (
            VideoStitcherServiceClient,
            transports.VideoStitcherServiceRestTransport,
            "rest",
            None,
        ),
    ],
)
def test_video_stitcher_service_client_client_options_credentials_file(
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


def test_video_stitcher_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.video.stitcher_v1.services.video_stitcher_service.transports.VideoStitcherServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = VideoStitcherServiceClient(
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
            VideoStitcherServiceClient,
            transports.VideoStitcherServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            VideoStitcherServiceAsyncClient,
            transports.VideoStitcherServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_video_stitcher_service_client_create_channel_credentials_file(
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
            "videostitcher.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="videostitcher.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.CreateCdnKeyRequest,
        dict,
    ],
)
def test_create_cdn_key(request_type, transport: str = "grpc"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_cdn_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cdn_keys.CdnKey(
            name="name_value",
            hostname="hostname_value",
            google_cdn_key=cdn_keys.GoogleCdnKey(private_key=b"private_key_blob"),
        )
        response = client.create_cdn_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.CreateCdnKeyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cdn_keys.CdnKey)
    assert response.name == "name_value"
    assert response.hostname == "hostname_value"


def test_create_cdn_key_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_cdn_key), "__call__") as call:
        client.create_cdn_key()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.CreateCdnKeyRequest()


@pytest.mark.asyncio
async def test_create_cdn_key_async(
    transport: str = "grpc_asyncio",
    request_type=video_stitcher_service.CreateCdnKeyRequest,
):
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_cdn_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cdn_keys.CdnKey(
                name="name_value",
                hostname="hostname_value",
            )
        )
        response = await client.create_cdn_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.CreateCdnKeyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cdn_keys.CdnKey)
    assert response.name == "name_value"
    assert response.hostname == "hostname_value"


@pytest.mark.asyncio
async def test_create_cdn_key_async_from_dict():
    await test_create_cdn_key_async(request_type=dict)


def test_create_cdn_key_field_headers():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.CreateCdnKeyRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_cdn_key), "__call__") as call:
        call.return_value = cdn_keys.CdnKey()
        client.create_cdn_key(request)

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
async def test_create_cdn_key_field_headers_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.CreateCdnKeyRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_cdn_key), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(cdn_keys.CdnKey())
        await client.create_cdn_key(request)

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


def test_create_cdn_key_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_cdn_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cdn_keys.CdnKey()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_cdn_key(
            parent="parent_value",
            cdn_key=cdn_keys.CdnKey(
                google_cdn_key=cdn_keys.GoogleCdnKey(private_key=b"private_key_blob")
            ),
            cdn_key_id="cdn_key_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].cdn_key
        mock_val = cdn_keys.CdnKey(
            google_cdn_key=cdn_keys.GoogleCdnKey(private_key=b"private_key_blob")
        )
        assert arg == mock_val
        arg = args[0].cdn_key_id
        mock_val = "cdn_key_id_value"
        assert arg == mock_val


def test_create_cdn_key_flattened_error():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_cdn_key(
            video_stitcher_service.CreateCdnKeyRequest(),
            parent="parent_value",
            cdn_key=cdn_keys.CdnKey(
                google_cdn_key=cdn_keys.GoogleCdnKey(private_key=b"private_key_blob")
            ),
            cdn_key_id="cdn_key_id_value",
        )


@pytest.mark.asyncio
async def test_create_cdn_key_flattened_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_cdn_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cdn_keys.CdnKey()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(cdn_keys.CdnKey())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_cdn_key(
            parent="parent_value",
            cdn_key=cdn_keys.CdnKey(
                google_cdn_key=cdn_keys.GoogleCdnKey(private_key=b"private_key_blob")
            ),
            cdn_key_id="cdn_key_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].cdn_key
        mock_val = cdn_keys.CdnKey(
            google_cdn_key=cdn_keys.GoogleCdnKey(private_key=b"private_key_blob")
        )
        assert arg == mock_val
        arg = args[0].cdn_key_id
        mock_val = "cdn_key_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_cdn_key_flattened_error_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_cdn_key(
            video_stitcher_service.CreateCdnKeyRequest(),
            parent="parent_value",
            cdn_key=cdn_keys.CdnKey(
                google_cdn_key=cdn_keys.GoogleCdnKey(private_key=b"private_key_blob")
            ),
            cdn_key_id="cdn_key_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.ListCdnKeysRequest,
        dict,
    ],
)
def test_list_cdn_keys(request_type, transport: str = "grpc"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_cdn_keys), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = video_stitcher_service.ListCdnKeysResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_cdn_keys(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.ListCdnKeysRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCdnKeysPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_cdn_keys_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_cdn_keys), "__call__") as call:
        client.list_cdn_keys()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.ListCdnKeysRequest()


@pytest.mark.asyncio
async def test_list_cdn_keys_async(
    transport: str = "grpc_asyncio",
    request_type=video_stitcher_service.ListCdnKeysRequest,
):
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_cdn_keys), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            video_stitcher_service.ListCdnKeysResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_cdn_keys(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.ListCdnKeysRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCdnKeysAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_cdn_keys_async_from_dict():
    await test_list_cdn_keys_async(request_type=dict)


def test_list_cdn_keys_field_headers():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.ListCdnKeysRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_cdn_keys), "__call__") as call:
        call.return_value = video_stitcher_service.ListCdnKeysResponse()
        client.list_cdn_keys(request)

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
async def test_list_cdn_keys_field_headers_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.ListCdnKeysRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_cdn_keys), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            video_stitcher_service.ListCdnKeysResponse()
        )
        await client.list_cdn_keys(request)

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


def test_list_cdn_keys_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_cdn_keys), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = video_stitcher_service.ListCdnKeysResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_cdn_keys(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_cdn_keys_flattened_error():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_cdn_keys(
            video_stitcher_service.ListCdnKeysRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_cdn_keys_flattened_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_cdn_keys), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = video_stitcher_service.ListCdnKeysResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            video_stitcher_service.ListCdnKeysResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_cdn_keys(
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
async def test_list_cdn_keys_flattened_error_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_cdn_keys(
            video_stitcher_service.ListCdnKeysRequest(),
            parent="parent_value",
        )


def test_list_cdn_keys_pager(transport_name: str = "grpc"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_cdn_keys), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            video_stitcher_service.ListCdnKeysResponse(
                cdn_keys=[
                    cdn_keys.CdnKey(),
                    cdn_keys.CdnKey(),
                    cdn_keys.CdnKey(),
                ],
                next_page_token="abc",
            ),
            video_stitcher_service.ListCdnKeysResponse(
                cdn_keys=[],
                next_page_token="def",
            ),
            video_stitcher_service.ListCdnKeysResponse(
                cdn_keys=[
                    cdn_keys.CdnKey(),
                ],
                next_page_token="ghi",
            ),
            video_stitcher_service.ListCdnKeysResponse(
                cdn_keys=[
                    cdn_keys.CdnKey(),
                    cdn_keys.CdnKey(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_cdn_keys(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, cdn_keys.CdnKey) for i in results)


def test_list_cdn_keys_pages(transport_name: str = "grpc"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_cdn_keys), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            video_stitcher_service.ListCdnKeysResponse(
                cdn_keys=[
                    cdn_keys.CdnKey(),
                    cdn_keys.CdnKey(),
                    cdn_keys.CdnKey(),
                ],
                next_page_token="abc",
            ),
            video_stitcher_service.ListCdnKeysResponse(
                cdn_keys=[],
                next_page_token="def",
            ),
            video_stitcher_service.ListCdnKeysResponse(
                cdn_keys=[
                    cdn_keys.CdnKey(),
                ],
                next_page_token="ghi",
            ),
            video_stitcher_service.ListCdnKeysResponse(
                cdn_keys=[
                    cdn_keys.CdnKey(),
                    cdn_keys.CdnKey(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_cdn_keys(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_cdn_keys_async_pager():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cdn_keys), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            video_stitcher_service.ListCdnKeysResponse(
                cdn_keys=[
                    cdn_keys.CdnKey(),
                    cdn_keys.CdnKey(),
                    cdn_keys.CdnKey(),
                ],
                next_page_token="abc",
            ),
            video_stitcher_service.ListCdnKeysResponse(
                cdn_keys=[],
                next_page_token="def",
            ),
            video_stitcher_service.ListCdnKeysResponse(
                cdn_keys=[
                    cdn_keys.CdnKey(),
                ],
                next_page_token="ghi",
            ),
            video_stitcher_service.ListCdnKeysResponse(
                cdn_keys=[
                    cdn_keys.CdnKey(),
                    cdn_keys.CdnKey(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_cdn_keys(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, cdn_keys.CdnKey) for i in responses)


@pytest.mark.asyncio
async def test_list_cdn_keys_async_pages():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_cdn_keys), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            video_stitcher_service.ListCdnKeysResponse(
                cdn_keys=[
                    cdn_keys.CdnKey(),
                    cdn_keys.CdnKey(),
                    cdn_keys.CdnKey(),
                ],
                next_page_token="abc",
            ),
            video_stitcher_service.ListCdnKeysResponse(
                cdn_keys=[],
                next_page_token="def",
            ),
            video_stitcher_service.ListCdnKeysResponse(
                cdn_keys=[
                    cdn_keys.CdnKey(),
                ],
                next_page_token="ghi",
            ),
            video_stitcher_service.ListCdnKeysResponse(
                cdn_keys=[
                    cdn_keys.CdnKey(),
                    cdn_keys.CdnKey(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_cdn_keys(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.GetCdnKeyRequest,
        dict,
    ],
)
def test_get_cdn_key(request_type, transport: str = "grpc"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_cdn_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cdn_keys.CdnKey(
            name="name_value",
            hostname="hostname_value",
            google_cdn_key=cdn_keys.GoogleCdnKey(private_key=b"private_key_blob"),
        )
        response = client.get_cdn_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.GetCdnKeyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cdn_keys.CdnKey)
    assert response.name == "name_value"
    assert response.hostname == "hostname_value"


def test_get_cdn_key_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_cdn_key), "__call__") as call:
        client.get_cdn_key()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.GetCdnKeyRequest()


@pytest.mark.asyncio
async def test_get_cdn_key_async(
    transport: str = "grpc_asyncio",
    request_type=video_stitcher_service.GetCdnKeyRequest,
):
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_cdn_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cdn_keys.CdnKey(
                name="name_value",
                hostname="hostname_value",
            )
        )
        response = await client.get_cdn_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.GetCdnKeyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cdn_keys.CdnKey)
    assert response.name == "name_value"
    assert response.hostname == "hostname_value"


@pytest.mark.asyncio
async def test_get_cdn_key_async_from_dict():
    await test_get_cdn_key_async(request_type=dict)


def test_get_cdn_key_field_headers():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.GetCdnKeyRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_cdn_key), "__call__") as call:
        call.return_value = cdn_keys.CdnKey()
        client.get_cdn_key(request)

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
async def test_get_cdn_key_field_headers_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.GetCdnKeyRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_cdn_key), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(cdn_keys.CdnKey())
        await client.get_cdn_key(request)

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


def test_get_cdn_key_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_cdn_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cdn_keys.CdnKey()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_cdn_key(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_cdn_key_flattened_error():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_cdn_key(
            video_stitcher_service.GetCdnKeyRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_cdn_key_flattened_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_cdn_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cdn_keys.CdnKey()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(cdn_keys.CdnKey())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_cdn_key(
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
async def test_get_cdn_key_flattened_error_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_cdn_key(
            video_stitcher_service.GetCdnKeyRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.DeleteCdnKeyRequest,
        dict,
    ],
)
def test_delete_cdn_key(request_type, transport: str = "grpc"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_cdn_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_cdn_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.DeleteCdnKeyRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_cdn_key_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_cdn_key), "__call__") as call:
        client.delete_cdn_key()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.DeleteCdnKeyRequest()


@pytest.mark.asyncio
async def test_delete_cdn_key_async(
    transport: str = "grpc_asyncio",
    request_type=video_stitcher_service.DeleteCdnKeyRequest,
):
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_cdn_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_cdn_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.DeleteCdnKeyRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_cdn_key_async_from_dict():
    await test_delete_cdn_key_async(request_type=dict)


def test_delete_cdn_key_field_headers():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.DeleteCdnKeyRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_cdn_key), "__call__") as call:
        call.return_value = None
        client.delete_cdn_key(request)

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
async def test_delete_cdn_key_field_headers_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.DeleteCdnKeyRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_cdn_key), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_cdn_key(request)

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


def test_delete_cdn_key_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_cdn_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_cdn_key(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_cdn_key_flattened_error():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_cdn_key(
            video_stitcher_service.DeleteCdnKeyRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_cdn_key_flattened_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_cdn_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_cdn_key(
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
async def test_delete_cdn_key_flattened_error_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_cdn_key(
            video_stitcher_service.DeleteCdnKeyRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.UpdateCdnKeyRequest,
        dict,
    ],
)
def test_update_cdn_key(request_type, transport: str = "grpc"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_cdn_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cdn_keys.CdnKey(
            name="name_value",
            hostname="hostname_value",
            google_cdn_key=cdn_keys.GoogleCdnKey(private_key=b"private_key_blob"),
        )
        response = client.update_cdn_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.UpdateCdnKeyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cdn_keys.CdnKey)
    assert response.name == "name_value"
    assert response.hostname == "hostname_value"


def test_update_cdn_key_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_cdn_key), "__call__") as call:
        client.update_cdn_key()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.UpdateCdnKeyRequest()


@pytest.mark.asyncio
async def test_update_cdn_key_async(
    transport: str = "grpc_asyncio",
    request_type=video_stitcher_service.UpdateCdnKeyRequest,
):
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_cdn_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cdn_keys.CdnKey(
                name="name_value",
                hostname="hostname_value",
            )
        )
        response = await client.update_cdn_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.UpdateCdnKeyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cdn_keys.CdnKey)
    assert response.name == "name_value"
    assert response.hostname == "hostname_value"


@pytest.mark.asyncio
async def test_update_cdn_key_async_from_dict():
    await test_update_cdn_key_async(request_type=dict)


def test_update_cdn_key_field_headers():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.UpdateCdnKeyRequest()

    request.cdn_key.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_cdn_key), "__call__") as call:
        call.return_value = cdn_keys.CdnKey()
        client.update_cdn_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "cdn_key.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_cdn_key_field_headers_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.UpdateCdnKeyRequest()

    request.cdn_key.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_cdn_key), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(cdn_keys.CdnKey())
        await client.update_cdn_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "cdn_key.name=name_value",
    ) in kw["metadata"]


def test_update_cdn_key_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_cdn_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cdn_keys.CdnKey()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_cdn_key(
            cdn_key=cdn_keys.CdnKey(
                google_cdn_key=cdn_keys.GoogleCdnKey(private_key=b"private_key_blob")
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].cdn_key
        mock_val = cdn_keys.CdnKey(
            google_cdn_key=cdn_keys.GoogleCdnKey(private_key=b"private_key_blob")
        )
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_cdn_key_flattened_error():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_cdn_key(
            video_stitcher_service.UpdateCdnKeyRequest(),
            cdn_key=cdn_keys.CdnKey(
                google_cdn_key=cdn_keys.GoogleCdnKey(private_key=b"private_key_blob")
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_cdn_key_flattened_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_cdn_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cdn_keys.CdnKey()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(cdn_keys.CdnKey())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_cdn_key(
            cdn_key=cdn_keys.CdnKey(
                google_cdn_key=cdn_keys.GoogleCdnKey(private_key=b"private_key_blob")
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].cdn_key
        mock_val = cdn_keys.CdnKey(
            google_cdn_key=cdn_keys.GoogleCdnKey(private_key=b"private_key_blob")
        )
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_cdn_key_flattened_error_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_cdn_key(
            video_stitcher_service.UpdateCdnKeyRequest(),
            cdn_key=cdn_keys.CdnKey(
                google_cdn_key=cdn_keys.GoogleCdnKey(private_key=b"private_key_blob")
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.CreateVodSessionRequest,
        dict,
    ],
)
def test_create_vod_session(request_type, transport: str = "grpc"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_vod_session), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = sessions.VodSession(
            name="name_value",
            play_uri="play_uri_value",
            source_uri="source_uri_value",
            ad_tag_uri="ad_tag_uri_value",
            client_ad_tracking=True,
            asset_id="asset_id_value",
        )
        response = client.create_vod_session(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.CreateVodSessionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, sessions.VodSession)
    assert response.name == "name_value"
    assert response.play_uri == "play_uri_value"
    assert response.source_uri == "source_uri_value"
    assert response.ad_tag_uri == "ad_tag_uri_value"
    assert response.client_ad_tracking is True
    assert response.asset_id == "asset_id_value"


def test_create_vod_session_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_vod_session), "__call__"
    ) as call:
        client.create_vod_session()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.CreateVodSessionRequest()


@pytest.mark.asyncio
async def test_create_vod_session_async(
    transport: str = "grpc_asyncio",
    request_type=video_stitcher_service.CreateVodSessionRequest,
):
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_vod_session), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            sessions.VodSession(
                name="name_value",
                play_uri="play_uri_value",
                source_uri="source_uri_value",
                ad_tag_uri="ad_tag_uri_value",
                client_ad_tracking=True,
                asset_id="asset_id_value",
            )
        )
        response = await client.create_vod_session(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.CreateVodSessionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, sessions.VodSession)
    assert response.name == "name_value"
    assert response.play_uri == "play_uri_value"
    assert response.source_uri == "source_uri_value"
    assert response.ad_tag_uri == "ad_tag_uri_value"
    assert response.client_ad_tracking is True
    assert response.asset_id == "asset_id_value"


@pytest.mark.asyncio
async def test_create_vod_session_async_from_dict():
    await test_create_vod_session_async(request_type=dict)


def test_create_vod_session_field_headers():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.CreateVodSessionRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_vod_session), "__call__"
    ) as call:
        call.return_value = sessions.VodSession()
        client.create_vod_session(request)

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
async def test_create_vod_session_field_headers_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.CreateVodSessionRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_vod_session), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(sessions.VodSession())
        await client.create_vod_session(request)

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


def test_create_vod_session_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_vod_session), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = sessions.VodSession()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_vod_session(
            parent="parent_value",
            vod_session=sessions.VodSession(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].vod_session
        mock_val = sessions.VodSession(name="name_value")
        assert arg == mock_val


def test_create_vod_session_flattened_error():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_vod_session(
            video_stitcher_service.CreateVodSessionRequest(),
            parent="parent_value",
            vod_session=sessions.VodSession(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_vod_session_flattened_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_vod_session), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = sessions.VodSession()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(sessions.VodSession())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_vod_session(
            parent="parent_value",
            vod_session=sessions.VodSession(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].vod_session
        mock_val = sessions.VodSession(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_vod_session_flattened_error_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_vod_session(
            video_stitcher_service.CreateVodSessionRequest(),
            parent="parent_value",
            vod_session=sessions.VodSession(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.GetVodSessionRequest,
        dict,
    ],
)
def test_get_vod_session(request_type, transport: str = "grpc"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_vod_session), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = sessions.VodSession(
            name="name_value",
            play_uri="play_uri_value",
            source_uri="source_uri_value",
            ad_tag_uri="ad_tag_uri_value",
            client_ad_tracking=True,
            asset_id="asset_id_value",
        )
        response = client.get_vod_session(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.GetVodSessionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, sessions.VodSession)
    assert response.name == "name_value"
    assert response.play_uri == "play_uri_value"
    assert response.source_uri == "source_uri_value"
    assert response.ad_tag_uri == "ad_tag_uri_value"
    assert response.client_ad_tracking is True
    assert response.asset_id == "asset_id_value"


def test_get_vod_session_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_vod_session), "__call__") as call:
        client.get_vod_session()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.GetVodSessionRequest()


@pytest.mark.asyncio
async def test_get_vod_session_async(
    transport: str = "grpc_asyncio",
    request_type=video_stitcher_service.GetVodSessionRequest,
):
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_vod_session), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            sessions.VodSession(
                name="name_value",
                play_uri="play_uri_value",
                source_uri="source_uri_value",
                ad_tag_uri="ad_tag_uri_value",
                client_ad_tracking=True,
                asset_id="asset_id_value",
            )
        )
        response = await client.get_vod_session(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.GetVodSessionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, sessions.VodSession)
    assert response.name == "name_value"
    assert response.play_uri == "play_uri_value"
    assert response.source_uri == "source_uri_value"
    assert response.ad_tag_uri == "ad_tag_uri_value"
    assert response.client_ad_tracking is True
    assert response.asset_id == "asset_id_value"


@pytest.mark.asyncio
async def test_get_vod_session_async_from_dict():
    await test_get_vod_session_async(request_type=dict)


def test_get_vod_session_field_headers():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.GetVodSessionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_vod_session), "__call__") as call:
        call.return_value = sessions.VodSession()
        client.get_vod_session(request)

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
async def test_get_vod_session_field_headers_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.GetVodSessionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_vod_session), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(sessions.VodSession())
        await client.get_vod_session(request)

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


def test_get_vod_session_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_vod_session), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = sessions.VodSession()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_vod_session(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_vod_session_flattened_error():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_vod_session(
            video_stitcher_service.GetVodSessionRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_vod_session_flattened_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_vod_session), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = sessions.VodSession()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(sessions.VodSession())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_vod_session(
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
async def test_get_vod_session_flattened_error_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_vod_session(
            video_stitcher_service.GetVodSessionRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.ListVodStitchDetailsRequest,
        dict,
    ],
)
def test_list_vod_stitch_details(request_type, transport: str = "grpc"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vod_stitch_details), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = video_stitcher_service.ListVodStitchDetailsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_vod_stitch_details(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.ListVodStitchDetailsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListVodStitchDetailsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_vod_stitch_details_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vod_stitch_details), "__call__"
    ) as call:
        client.list_vod_stitch_details()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.ListVodStitchDetailsRequest()


@pytest.mark.asyncio
async def test_list_vod_stitch_details_async(
    transport: str = "grpc_asyncio",
    request_type=video_stitcher_service.ListVodStitchDetailsRequest,
):
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vod_stitch_details), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            video_stitcher_service.ListVodStitchDetailsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_vod_stitch_details(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.ListVodStitchDetailsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListVodStitchDetailsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_vod_stitch_details_async_from_dict():
    await test_list_vod_stitch_details_async(request_type=dict)


def test_list_vod_stitch_details_field_headers():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.ListVodStitchDetailsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vod_stitch_details), "__call__"
    ) as call:
        call.return_value = video_stitcher_service.ListVodStitchDetailsResponse()
        client.list_vod_stitch_details(request)

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
async def test_list_vod_stitch_details_field_headers_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.ListVodStitchDetailsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vod_stitch_details), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            video_stitcher_service.ListVodStitchDetailsResponse()
        )
        await client.list_vod_stitch_details(request)

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


def test_list_vod_stitch_details_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vod_stitch_details), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = video_stitcher_service.ListVodStitchDetailsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_vod_stitch_details(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_vod_stitch_details_flattened_error():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_vod_stitch_details(
            video_stitcher_service.ListVodStitchDetailsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_vod_stitch_details_flattened_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vod_stitch_details), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = video_stitcher_service.ListVodStitchDetailsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            video_stitcher_service.ListVodStitchDetailsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_vod_stitch_details(
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
async def test_list_vod_stitch_details_flattened_error_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_vod_stitch_details(
            video_stitcher_service.ListVodStitchDetailsRequest(),
            parent="parent_value",
        )


def test_list_vod_stitch_details_pager(transport_name: str = "grpc"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vod_stitch_details), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            video_stitcher_service.ListVodStitchDetailsResponse(
                vod_stitch_details=[
                    stitch_details.VodStitchDetail(),
                    stitch_details.VodStitchDetail(),
                    stitch_details.VodStitchDetail(),
                ],
                next_page_token="abc",
            ),
            video_stitcher_service.ListVodStitchDetailsResponse(
                vod_stitch_details=[],
                next_page_token="def",
            ),
            video_stitcher_service.ListVodStitchDetailsResponse(
                vod_stitch_details=[
                    stitch_details.VodStitchDetail(),
                ],
                next_page_token="ghi",
            ),
            video_stitcher_service.ListVodStitchDetailsResponse(
                vod_stitch_details=[
                    stitch_details.VodStitchDetail(),
                    stitch_details.VodStitchDetail(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_vod_stitch_details(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, stitch_details.VodStitchDetail) for i in results)


def test_list_vod_stitch_details_pages(transport_name: str = "grpc"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vod_stitch_details), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            video_stitcher_service.ListVodStitchDetailsResponse(
                vod_stitch_details=[
                    stitch_details.VodStitchDetail(),
                    stitch_details.VodStitchDetail(),
                    stitch_details.VodStitchDetail(),
                ],
                next_page_token="abc",
            ),
            video_stitcher_service.ListVodStitchDetailsResponse(
                vod_stitch_details=[],
                next_page_token="def",
            ),
            video_stitcher_service.ListVodStitchDetailsResponse(
                vod_stitch_details=[
                    stitch_details.VodStitchDetail(),
                ],
                next_page_token="ghi",
            ),
            video_stitcher_service.ListVodStitchDetailsResponse(
                vod_stitch_details=[
                    stitch_details.VodStitchDetail(),
                    stitch_details.VodStitchDetail(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_vod_stitch_details(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_vod_stitch_details_async_pager():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vod_stitch_details),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            video_stitcher_service.ListVodStitchDetailsResponse(
                vod_stitch_details=[
                    stitch_details.VodStitchDetail(),
                    stitch_details.VodStitchDetail(),
                    stitch_details.VodStitchDetail(),
                ],
                next_page_token="abc",
            ),
            video_stitcher_service.ListVodStitchDetailsResponse(
                vod_stitch_details=[],
                next_page_token="def",
            ),
            video_stitcher_service.ListVodStitchDetailsResponse(
                vod_stitch_details=[
                    stitch_details.VodStitchDetail(),
                ],
                next_page_token="ghi",
            ),
            video_stitcher_service.ListVodStitchDetailsResponse(
                vod_stitch_details=[
                    stitch_details.VodStitchDetail(),
                    stitch_details.VodStitchDetail(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_vod_stitch_details(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, stitch_details.VodStitchDetail) for i in responses)


@pytest.mark.asyncio
async def test_list_vod_stitch_details_async_pages():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vod_stitch_details),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            video_stitcher_service.ListVodStitchDetailsResponse(
                vod_stitch_details=[
                    stitch_details.VodStitchDetail(),
                    stitch_details.VodStitchDetail(),
                    stitch_details.VodStitchDetail(),
                ],
                next_page_token="abc",
            ),
            video_stitcher_service.ListVodStitchDetailsResponse(
                vod_stitch_details=[],
                next_page_token="def",
            ),
            video_stitcher_service.ListVodStitchDetailsResponse(
                vod_stitch_details=[
                    stitch_details.VodStitchDetail(),
                ],
                next_page_token="ghi",
            ),
            video_stitcher_service.ListVodStitchDetailsResponse(
                vod_stitch_details=[
                    stitch_details.VodStitchDetail(),
                    stitch_details.VodStitchDetail(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_vod_stitch_details(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.GetVodStitchDetailRequest,
        dict,
    ],
)
def test_get_vod_stitch_detail(request_type, transport: str = "grpc"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_vod_stitch_detail), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = stitch_details.VodStitchDetail(
            name="name_value",
        )
        response = client.get_vod_stitch_detail(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.GetVodStitchDetailRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, stitch_details.VodStitchDetail)
    assert response.name == "name_value"


def test_get_vod_stitch_detail_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_vod_stitch_detail), "__call__"
    ) as call:
        client.get_vod_stitch_detail()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.GetVodStitchDetailRequest()


@pytest.mark.asyncio
async def test_get_vod_stitch_detail_async(
    transport: str = "grpc_asyncio",
    request_type=video_stitcher_service.GetVodStitchDetailRequest,
):
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_vod_stitch_detail), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            stitch_details.VodStitchDetail(
                name="name_value",
            )
        )
        response = await client.get_vod_stitch_detail(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.GetVodStitchDetailRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, stitch_details.VodStitchDetail)
    assert response.name == "name_value"


@pytest.mark.asyncio
async def test_get_vod_stitch_detail_async_from_dict():
    await test_get_vod_stitch_detail_async(request_type=dict)


def test_get_vod_stitch_detail_field_headers():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.GetVodStitchDetailRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_vod_stitch_detail), "__call__"
    ) as call:
        call.return_value = stitch_details.VodStitchDetail()
        client.get_vod_stitch_detail(request)

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
async def test_get_vod_stitch_detail_field_headers_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.GetVodStitchDetailRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_vod_stitch_detail), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            stitch_details.VodStitchDetail()
        )
        await client.get_vod_stitch_detail(request)

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


def test_get_vod_stitch_detail_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_vod_stitch_detail), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = stitch_details.VodStitchDetail()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_vod_stitch_detail(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_vod_stitch_detail_flattened_error():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_vod_stitch_detail(
            video_stitcher_service.GetVodStitchDetailRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_vod_stitch_detail_flattened_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_vod_stitch_detail), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = stitch_details.VodStitchDetail()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            stitch_details.VodStitchDetail()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_vod_stitch_detail(
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
async def test_get_vod_stitch_detail_flattened_error_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_vod_stitch_detail(
            video_stitcher_service.GetVodStitchDetailRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.ListVodAdTagDetailsRequest,
        dict,
    ],
)
def test_list_vod_ad_tag_details(request_type, transport: str = "grpc"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vod_ad_tag_details), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = video_stitcher_service.ListVodAdTagDetailsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_vod_ad_tag_details(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.ListVodAdTagDetailsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListVodAdTagDetailsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_vod_ad_tag_details_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vod_ad_tag_details), "__call__"
    ) as call:
        client.list_vod_ad_tag_details()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.ListVodAdTagDetailsRequest()


@pytest.mark.asyncio
async def test_list_vod_ad_tag_details_async(
    transport: str = "grpc_asyncio",
    request_type=video_stitcher_service.ListVodAdTagDetailsRequest,
):
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vod_ad_tag_details), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            video_stitcher_service.ListVodAdTagDetailsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_vod_ad_tag_details(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.ListVodAdTagDetailsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListVodAdTagDetailsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_vod_ad_tag_details_async_from_dict():
    await test_list_vod_ad_tag_details_async(request_type=dict)


def test_list_vod_ad_tag_details_field_headers():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.ListVodAdTagDetailsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vod_ad_tag_details), "__call__"
    ) as call:
        call.return_value = video_stitcher_service.ListVodAdTagDetailsResponse()
        client.list_vod_ad_tag_details(request)

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
async def test_list_vod_ad_tag_details_field_headers_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.ListVodAdTagDetailsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vod_ad_tag_details), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            video_stitcher_service.ListVodAdTagDetailsResponse()
        )
        await client.list_vod_ad_tag_details(request)

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


def test_list_vod_ad_tag_details_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vod_ad_tag_details), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = video_stitcher_service.ListVodAdTagDetailsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_vod_ad_tag_details(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_vod_ad_tag_details_flattened_error():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_vod_ad_tag_details(
            video_stitcher_service.ListVodAdTagDetailsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_vod_ad_tag_details_flattened_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vod_ad_tag_details), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = video_stitcher_service.ListVodAdTagDetailsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            video_stitcher_service.ListVodAdTagDetailsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_vod_ad_tag_details(
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
async def test_list_vod_ad_tag_details_flattened_error_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_vod_ad_tag_details(
            video_stitcher_service.ListVodAdTagDetailsRequest(),
            parent="parent_value",
        )


def test_list_vod_ad_tag_details_pager(transport_name: str = "grpc"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vod_ad_tag_details), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            video_stitcher_service.ListVodAdTagDetailsResponse(
                vod_ad_tag_details=[
                    ad_tag_details.VodAdTagDetail(),
                    ad_tag_details.VodAdTagDetail(),
                    ad_tag_details.VodAdTagDetail(),
                ],
                next_page_token="abc",
            ),
            video_stitcher_service.ListVodAdTagDetailsResponse(
                vod_ad_tag_details=[],
                next_page_token="def",
            ),
            video_stitcher_service.ListVodAdTagDetailsResponse(
                vod_ad_tag_details=[
                    ad_tag_details.VodAdTagDetail(),
                ],
                next_page_token="ghi",
            ),
            video_stitcher_service.ListVodAdTagDetailsResponse(
                vod_ad_tag_details=[
                    ad_tag_details.VodAdTagDetail(),
                    ad_tag_details.VodAdTagDetail(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_vod_ad_tag_details(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, ad_tag_details.VodAdTagDetail) for i in results)


def test_list_vod_ad_tag_details_pages(transport_name: str = "grpc"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vod_ad_tag_details), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            video_stitcher_service.ListVodAdTagDetailsResponse(
                vod_ad_tag_details=[
                    ad_tag_details.VodAdTagDetail(),
                    ad_tag_details.VodAdTagDetail(),
                    ad_tag_details.VodAdTagDetail(),
                ],
                next_page_token="abc",
            ),
            video_stitcher_service.ListVodAdTagDetailsResponse(
                vod_ad_tag_details=[],
                next_page_token="def",
            ),
            video_stitcher_service.ListVodAdTagDetailsResponse(
                vod_ad_tag_details=[
                    ad_tag_details.VodAdTagDetail(),
                ],
                next_page_token="ghi",
            ),
            video_stitcher_service.ListVodAdTagDetailsResponse(
                vod_ad_tag_details=[
                    ad_tag_details.VodAdTagDetail(),
                    ad_tag_details.VodAdTagDetail(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_vod_ad_tag_details(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_vod_ad_tag_details_async_pager():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vod_ad_tag_details),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            video_stitcher_service.ListVodAdTagDetailsResponse(
                vod_ad_tag_details=[
                    ad_tag_details.VodAdTagDetail(),
                    ad_tag_details.VodAdTagDetail(),
                    ad_tag_details.VodAdTagDetail(),
                ],
                next_page_token="abc",
            ),
            video_stitcher_service.ListVodAdTagDetailsResponse(
                vod_ad_tag_details=[],
                next_page_token="def",
            ),
            video_stitcher_service.ListVodAdTagDetailsResponse(
                vod_ad_tag_details=[
                    ad_tag_details.VodAdTagDetail(),
                ],
                next_page_token="ghi",
            ),
            video_stitcher_service.ListVodAdTagDetailsResponse(
                vod_ad_tag_details=[
                    ad_tag_details.VodAdTagDetail(),
                    ad_tag_details.VodAdTagDetail(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_vod_ad_tag_details(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, ad_tag_details.VodAdTagDetail) for i in responses)


@pytest.mark.asyncio
async def test_list_vod_ad_tag_details_async_pages():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vod_ad_tag_details),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            video_stitcher_service.ListVodAdTagDetailsResponse(
                vod_ad_tag_details=[
                    ad_tag_details.VodAdTagDetail(),
                    ad_tag_details.VodAdTagDetail(),
                    ad_tag_details.VodAdTagDetail(),
                ],
                next_page_token="abc",
            ),
            video_stitcher_service.ListVodAdTagDetailsResponse(
                vod_ad_tag_details=[],
                next_page_token="def",
            ),
            video_stitcher_service.ListVodAdTagDetailsResponse(
                vod_ad_tag_details=[
                    ad_tag_details.VodAdTagDetail(),
                ],
                next_page_token="ghi",
            ),
            video_stitcher_service.ListVodAdTagDetailsResponse(
                vod_ad_tag_details=[
                    ad_tag_details.VodAdTagDetail(),
                    ad_tag_details.VodAdTagDetail(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_vod_ad_tag_details(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.GetVodAdTagDetailRequest,
        dict,
    ],
)
def test_get_vod_ad_tag_detail(request_type, transport: str = "grpc"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_vod_ad_tag_detail), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = ad_tag_details.VodAdTagDetail(
            name="name_value",
        )
        response = client.get_vod_ad_tag_detail(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.GetVodAdTagDetailRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, ad_tag_details.VodAdTagDetail)
    assert response.name == "name_value"


def test_get_vod_ad_tag_detail_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_vod_ad_tag_detail), "__call__"
    ) as call:
        client.get_vod_ad_tag_detail()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.GetVodAdTagDetailRequest()


@pytest.mark.asyncio
async def test_get_vod_ad_tag_detail_async(
    transport: str = "grpc_asyncio",
    request_type=video_stitcher_service.GetVodAdTagDetailRequest,
):
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_vod_ad_tag_detail), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            ad_tag_details.VodAdTagDetail(
                name="name_value",
            )
        )
        response = await client.get_vod_ad_tag_detail(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.GetVodAdTagDetailRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, ad_tag_details.VodAdTagDetail)
    assert response.name == "name_value"


@pytest.mark.asyncio
async def test_get_vod_ad_tag_detail_async_from_dict():
    await test_get_vod_ad_tag_detail_async(request_type=dict)


def test_get_vod_ad_tag_detail_field_headers():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.GetVodAdTagDetailRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_vod_ad_tag_detail), "__call__"
    ) as call:
        call.return_value = ad_tag_details.VodAdTagDetail()
        client.get_vod_ad_tag_detail(request)

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
async def test_get_vod_ad_tag_detail_field_headers_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.GetVodAdTagDetailRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_vod_ad_tag_detail), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            ad_tag_details.VodAdTagDetail()
        )
        await client.get_vod_ad_tag_detail(request)

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


def test_get_vod_ad_tag_detail_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_vod_ad_tag_detail), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = ad_tag_details.VodAdTagDetail()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_vod_ad_tag_detail(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_vod_ad_tag_detail_flattened_error():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_vod_ad_tag_detail(
            video_stitcher_service.GetVodAdTagDetailRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_vod_ad_tag_detail_flattened_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_vod_ad_tag_detail), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = ad_tag_details.VodAdTagDetail()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            ad_tag_details.VodAdTagDetail()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_vod_ad_tag_detail(
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
async def test_get_vod_ad_tag_detail_flattened_error_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_vod_ad_tag_detail(
            video_stitcher_service.GetVodAdTagDetailRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.ListLiveAdTagDetailsRequest,
        dict,
    ],
)
def test_list_live_ad_tag_details(request_type, transport: str = "grpc"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_live_ad_tag_details), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = video_stitcher_service.ListLiveAdTagDetailsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_live_ad_tag_details(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.ListLiveAdTagDetailsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListLiveAdTagDetailsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_live_ad_tag_details_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_live_ad_tag_details), "__call__"
    ) as call:
        client.list_live_ad_tag_details()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.ListLiveAdTagDetailsRequest()


@pytest.mark.asyncio
async def test_list_live_ad_tag_details_async(
    transport: str = "grpc_asyncio",
    request_type=video_stitcher_service.ListLiveAdTagDetailsRequest,
):
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_live_ad_tag_details), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            video_stitcher_service.ListLiveAdTagDetailsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_live_ad_tag_details(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.ListLiveAdTagDetailsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListLiveAdTagDetailsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_live_ad_tag_details_async_from_dict():
    await test_list_live_ad_tag_details_async(request_type=dict)


def test_list_live_ad_tag_details_field_headers():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.ListLiveAdTagDetailsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_live_ad_tag_details), "__call__"
    ) as call:
        call.return_value = video_stitcher_service.ListLiveAdTagDetailsResponse()
        client.list_live_ad_tag_details(request)

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
async def test_list_live_ad_tag_details_field_headers_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.ListLiveAdTagDetailsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_live_ad_tag_details), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            video_stitcher_service.ListLiveAdTagDetailsResponse()
        )
        await client.list_live_ad_tag_details(request)

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


def test_list_live_ad_tag_details_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_live_ad_tag_details), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = video_stitcher_service.ListLiveAdTagDetailsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_live_ad_tag_details(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_live_ad_tag_details_flattened_error():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_live_ad_tag_details(
            video_stitcher_service.ListLiveAdTagDetailsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_live_ad_tag_details_flattened_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_live_ad_tag_details), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = video_stitcher_service.ListLiveAdTagDetailsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            video_stitcher_service.ListLiveAdTagDetailsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_live_ad_tag_details(
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
async def test_list_live_ad_tag_details_flattened_error_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_live_ad_tag_details(
            video_stitcher_service.ListLiveAdTagDetailsRequest(),
            parent="parent_value",
        )


def test_list_live_ad_tag_details_pager(transport_name: str = "grpc"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_live_ad_tag_details), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            video_stitcher_service.ListLiveAdTagDetailsResponse(
                live_ad_tag_details=[
                    ad_tag_details.LiveAdTagDetail(),
                    ad_tag_details.LiveAdTagDetail(),
                    ad_tag_details.LiveAdTagDetail(),
                ],
                next_page_token="abc",
            ),
            video_stitcher_service.ListLiveAdTagDetailsResponse(
                live_ad_tag_details=[],
                next_page_token="def",
            ),
            video_stitcher_service.ListLiveAdTagDetailsResponse(
                live_ad_tag_details=[
                    ad_tag_details.LiveAdTagDetail(),
                ],
                next_page_token="ghi",
            ),
            video_stitcher_service.ListLiveAdTagDetailsResponse(
                live_ad_tag_details=[
                    ad_tag_details.LiveAdTagDetail(),
                    ad_tag_details.LiveAdTagDetail(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_live_ad_tag_details(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, ad_tag_details.LiveAdTagDetail) for i in results)


def test_list_live_ad_tag_details_pages(transport_name: str = "grpc"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_live_ad_tag_details), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            video_stitcher_service.ListLiveAdTagDetailsResponse(
                live_ad_tag_details=[
                    ad_tag_details.LiveAdTagDetail(),
                    ad_tag_details.LiveAdTagDetail(),
                    ad_tag_details.LiveAdTagDetail(),
                ],
                next_page_token="abc",
            ),
            video_stitcher_service.ListLiveAdTagDetailsResponse(
                live_ad_tag_details=[],
                next_page_token="def",
            ),
            video_stitcher_service.ListLiveAdTagDetailsResponse(
                live_ad_tag_details=[
                    ad_tag_details.LiveAdTagDetail(),
                ],
                next_page_token="ghi",
            ),
            video_stitcher_service.ListLiveAdTagDetailsResponse(
                live_ad_tag_details=[
                    ad_tag_details.LiveAdTagDetail(),
                    ad_tag_details.LiveAdTagDetail(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_live_ad_tag_details(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_live_ad_tag_details_async_pager():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_live_ad_tag_details),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            video_stitcher_service.ListLiveAdTagDetailsResponse(
                live_ad_tag_details=[
                    ad_tag_details.LiveAdTagDetail(),
                    ad_tag_details.LiveAdTagDetail(),
                    ad_tag_details.LiveAdTagDetail(),
                ],
                next_page_token="abc",
            ),
            video_stitcher_service.ListLiveAdTagDetailsResponse(
                live_ad_tag_details=[],
                next_page_token="def",
            ),
            video_stitcher_service.ListLiveAdTagDetailsResponse(
                live_ad_tag_details=[
                    ad_tag_details.LiveAdTagDetail(),
                ],
                next_page_token="ghi",
            ),
            video_stitcher_service.ListLiveAdTagDetailsResponse(
                live_ad_tag_details=[
                    ad_tag_details.LiveAdTagDetail(),
                    ad_tag_details.LiveAdTagDetail(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_live_ad_tag_details(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, ad_tag_details.LiveAdTagDetail) for i in responses)


@pytest.mark.asyncio
async def test_list_live_ad_tag_details_async_pages():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_live_ad_tag_details),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            video_stitcher_service.ListLiveAdTagDetailsResponse(
                live_ad_tag_details=[
                    ad_tag_details.LiveAdTagDetail(),
                    ad_tag_details.LiveAdTagDetail(),
                    ad_tag_details.LiveAdTagDetail(),
                ],
                next_page_token="abc",
            ),
            video_stitcher_service.ListLiveAdTagDetailsResponse(
                live_ad_tag_details=[],
                next_page_token="def",
            ),
            video_stitcher_service.ListLiveAdTagDetailsResponse(
                live_ad_tag_details=[
                    ad_tag_details.LiveAdTagDetail(),
                ],
                next_page_token="ghi",
            ),
            video_stitcher_service.ListLiveAdTagDetailsResponse(
                live_ad_tag_details=[
                    ad_tag_details.LiveAdTagDetail(),
                    ad_tag_details.LiveAdTagDetail(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_live_ad_tag_details(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.GetLiveAdTagDetailRequest,
        dict,
    ],
)
def test_get_live_ad_tag_detail(request_type, transport: str = "grpc"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_live_ad_tag_detail), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = ad_tag_details.LiveAdTagDetail(
            name="name_value",
        )
        response = client.get_live_ad_tag_detail(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.GetLiveAdTagDetailRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, ad_tag_details.LiveAdTagDetail)
    assert response.name == "name_value"


def test_get_live_ad_tag_detail_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_live_ad_tag_detail), "__call__"
    ) as call:
        client.get_live_ad_tag_detail()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.GetLiveAdTagDetailRequest()


@pytest.mark.asyncio
async def test_get_live_ad_tag_detail_async(
    transport: str = "grpc_asyncio",
    request_type=video_stitcher_service.GetLiveAdTagDetailRequest,
):
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_live_ad_tag_detail), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            ad_tag_details.LiveAdTagDetail(
                name="name_value",
            )
        )
        response = await client.get_live_ad_tag_detail(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.GetLiveAdTagDetailRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, ad_tag_details.LiveAdTagDetail)
    assert response.name == "name_value"


@pytest.mark.asyncio
async def test_get_live_ad_tag_detail_async_from_dict():
    await test_get_live_ad_tag_detail_async(request_type=dict)


def test_get_live_ad_tag_detail_field_headers():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.GetLiveAdTagDetailRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_live_ad_tag_detail), "__call__"
    ) as call:
        call.return_value = ad_tag_details.LiveAdTagDetail()
        client.get_live_ad_tag_detail(request)

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
async def test_get_live_ad_tag_detail_field_headers_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.GetLiveAdTagDetailRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_live_ad_tag_detail), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            ad_tag_details.LiveAdTagDetail()
        )
        await client.get_live_ad_tag_detail(request)

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


def test_get_live_ad_tag_detail_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_live_ad_tag_detail), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = ad_tag_details.LiveAdTagDetail()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_live_ad_tag_detail(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_live_ad_tag_detail_flattened_error():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_live_ad_tag_detail(
            video_stitcher_service.GetLiveAdTagDetailRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_live_ad_tag_detail_flattened_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_live_ad_tag_detail), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = ad_tag_details.LiveAdTagDetail()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            ad_tag_details.LiveAdTagDetail()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_live_ad_tag_detail(
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
async def test_get_live_ad_tag_detail_flattened_error_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_live_ad_tag_detail(
            video_stitcher_service.GetLiveAdTagDetailRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.CreateSlateRequest,
        dict,
    ],
)
def test_create_slate(request_type, transport: str = "grpc"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_slate), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = slates.Slate(
            name="name_value",
            uri="uri_value",
        )
        response = client.create_slate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.CreateSlateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, slates.Slate)
    assert response.name == "name_value"
    assert response.uri == "uri_value"


def test_create_slate_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_slate), "__call__") as call:
        client.create_slate()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.CreateSlateRequest()


@pytest.mark.asyncio
async def test_create_slate_async(
    transport: str = "grpc_asyncio",
    request_type=video_stitcher_service.CreateSlateRequest,
):
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_slate), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            slates.Slate(
                name="name_value",
                uri="uri_value",
            )
        )
        response = await client.create_slate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.CreateSlateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, slates.Slate)
    assert response.name == "name_value"
    assert response.uri == "uri_value"


@pytest.mark.asyncio
async def test_create_slate_async_from_dict():
    await test_create_slate_async(request_type=dict)


def test_create_slate_field_headers():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.CreateSlateRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_slate), "__call__") as call:
        call.return_value = slates.Slate()
        client.create_slate(request)

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
async def test_create_slate_field_headers_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.CreateSlateRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_slate), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(slates.Slate())
        await client.create_slate(request)

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


def test_create_slate_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_slate), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = slates.Slate()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_slate(
            parent="parent_value",
            slate=slates.Slate(name="name_value"),
            slate_id="slate_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].slate
        mock_val = slates.Slate(name="name_value")
        assert arg == mock_val
        arg = args[0].slate_id
        mock_val = "slate_id_value"
        assert arg == mock_val


def test_create_slate_flattened_error():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_slate(
            video_stitcher_service.CreateSlateRequest(),
            parent="parent_value",
            slate=slates.Slate(name="name_value"),
            slate_id="slate_id_value",
        )


@pytest.mark.asyncio
async def test_create_slate_flattened_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_slate), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = slates.Slate()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(slates.Slate())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_slate(
            parent="parent_value",
            slate=slates.Slate(name="name_value"),
            slate_id="slate_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].slate
        mock_val = slates.Slate(name="name_value")
        assert arg == mock_val
        arg = args[0].slate_id
        mock_val = "slate_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_slate_flattened_error_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_slate(
            video_stitcher_service.CreateSlateRequest(),
            parent="parent_value",
            slate=slates.Slate(name="name_value"),
            slate_id="slate_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.ListSlatesRequest,
        dict,
    ],
)
def test_list_slates(request_type, transport: str = "grpc"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_slates), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = video_stitcher_service.ListSlatesResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_slates(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.ListSlatesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSlatesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_slates_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_slates), "__call__") as call:
        client.list_slates()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.ListSlatesRequest()


@pytest.mark.asyncio
async def test_list_slates_async(
    transport: str = "grpc_asyncio",
    request_type=video_stitcher_service.ListSlatesRequest,
):
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_slates), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            video_stitcher_service.ListSlatesResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_slates(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.ListSlatesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSlatesAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_slates_async_from_dict():
    await test_list_slates_async(request_type=dict)


def test_list_slates_field_headers():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.ListSlatesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_slates), "__call__") as call:
        call.return_value = video_stitcher_service.ListSlatesResponse()
        client.list_slates(request)

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
async def test_list_slates_field_headers_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.ListSlatesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_slates), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            video_stitcher_service.ListSlatesResponse()
        )
        await client.list_slates(request)

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


def test_list_slates_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_slates), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = video_stitcher_service.ListSlatesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_slates(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_slates_flattened_error():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_slates(
            video_stitcher_service.ListSlatesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_slates_flattened_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_slates), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = video_stitcher_service.ListSlatesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            video_stitcher_service.ListSlatesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_slates(
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
async def test_list_slates_flattened_error_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_slates(
            video_stitcher_service.ListSlatesRequest(),
            parent="parent_value",
        )


def test_list_slates_pager(transport_name: str = "grpc"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_slates), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            video_stitcher_service.ListSlatesResponse(
                slates=[
                    slates.Slate(),
                    slates.Slate(),
                    slates.Slate(),
                ],
                next_page_token="abc",
            ),
            video_stitcher_service.ListSlatesResponse(
                slates=[],
                next_page_token="def",
            ),
            video_stitcher_service.ListSlatesResponse(
                slates=[
                    slates.Slate(),
                ],
                next_page_token="ghi",
            ),
            video_stitcher_service.ListSlatesResponse(
                slates=[
                    slates.Slate(),
                    slates.Slate(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_slates(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, slates.Slate) for i in results)


def test_list_slates_pages(transport_name: str = "grpc"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_slates), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            video_stitcher_service.ListSlatesResponse(
                slates=[
                    slates.Slate(),
                    slates.Slate(),
                    slates.Slate(),
                ],
                next_page_token="abc",
            ),
            video_stitcher_service.ListSlatesResponse(
                slates=[],
                next_page_token="def",
            ),
            video_stitcher_service.ListSlatesResponse(
                slates=[
                    slates.Slate(),
                ],
                next_page_token="ghi",
            ),
            video_stitcher_service.ListSlatesResponse(
                slates=[
                    slates.Slate(),
                    slates.Slate(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_slates(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_slates_async_pager():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_slates), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            video_stitcher_service.ListSlatesResponse(
                slates=[
                    slates.Slate(),
                    slates.Slate(),
                    slates.Slate(),
                ],
                next_page_token="abc",
            ),
            video_stitcher_service.ListSlatesResponse(
                slates=[],
                next_page_token="def",
            ),
            video_stitcher_service.ListSlatesResponse(
                slates=[
                    slates.Slate(),
                ],
                next_page_token="ghi",
            ),
            video_stitcher_service.ListSlatesResponse(
                slates=[
                    slates.Slate(),
                    slates.Slate(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_slates(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, slates.Slate) for i in responses)


@pytest.mark.asyncio
async def test_list_slates_async_pages():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_slates), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            video_stitcher_service.ListSlatesResponse(
                slates=[
                    slates.Slate(),
                    slates.Slate(),
                    slates.Slate(),
                ],
                next_page_token="abc",
            ),
            video_stitcher_service.ListSlatesResponse(
                slates=[],
                next_page_token="def",
            ),
            video_stitcher_service.ListSlatesResponse(
                slates=[
                    slates.Slate(),
                ],
                next_page_token="ghi",
            ),
            video_stitcher_service.ListSlatesResponse(
                slates=[
                    slates.Slate(),
                    slates.Slate(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_slates(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.GetSlateRequest,
        dict,
    ],
)
def test_get_slate(request_type, transport: str = "grpc"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_slate), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = slates.Slate(
            name="name_value",
            uri="uri_value",
        )
        response = client.get_slate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.GetSlateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, slates.Slate)
    assert response.name == "name_value"
    assert response.uri == "uri_value"


def test_get_slate_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_slate), "__call__") as call:
        client.get_slate()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.GetSlateRequest()


@pytest.mark.asyncio
async def test_get_slate_async(
    transport: str = "grpc_asyncio", request_type=video_stitcher_service.GetSlateRequest
):
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_slate), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            slates.Slate(
                name="name_value",
                uri="uri_value",
            )
        )
        response = await client.get_slate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.GetSlateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, slates.Slate)
    assert response.name == "name_value"
    assert response.uri == "uri_value"


@pytest.mark.asyncio
async def test_get_slate_async_from_dict():
    await test_get_slate_async(request_type=dict)


def test_get_slate_field_headers():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.GetSlateRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_slate), "__call__") as call:
        call.return_value = slates.Slate()
        client.get_slate(request)

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
async def test_get_slate_field_headers_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.GetSlateRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_slate), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(slates.Slate())
        await client.get_slate(request)

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


def test_get_slate_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_slate), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = slates.Slate()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_slate(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_slate_flattened_error():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_slate(
            video_stitcher_service.GetSlateRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_slate_flattened_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_slate), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = slates.Slate()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(slates.Slate())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_slate(
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
async def test_get_slate_flattened_error_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_slate(
            video_stitcher_service.GetSlateRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.UpdateSlateRequest,
        dict,
    ],
)
def test_update_slate(request_type, transport: str = "grpc"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_slate), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = slates.Slate(
            name="name_value",
            uri="uri_value",
        )
        response = client.update_slate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.UpdateSlateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, slates.Slate)
    assert response.name == "name_value"
    assert response.uri == "uri_value"


def test_update_slate_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_slate), "__call__") as call:
        client.update_slate()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.UpdateSlateRequest()


@pytest.mark.asyncio
async def test_update_slate_async(
    transport: str = "grpc_asyncio",
    request_type=video_stitcher_service.UpdateSlateRequest,
):
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_slate), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            slates.Slate(
                name="name_value",
                uri="uri_value",
            )
        )
        response = await client.update_slate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.UpdateSlateRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, slates.Slate)
    assert response.name == "name_value"
    assert response.uri == "uri_value"


@pytest.mark.asyncio
async def test_update_slate_async_from_dict():
    await test_update_slate_async(request_type=dict)


def test_update_slate_field_headers():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.UpdateSlateRequest()

    request.slate.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_slate), "__call__") as call:
        call.return_value = slates.Slate()
        client.update_slate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "slate.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_slate_field_headers_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.UpdateSlateRequest()

    request.slate.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_slate), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(slates.Slate())
        await client.update_slate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "slate.name=name_value",
    ) in kw["metadata"]


def test_update_slate_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_slate), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = slates.Slate()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_slate(
            slate=slates.Slate(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].slate
        mock_val = slates.Slate(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_slate_flattened_error():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_slate(
            video_stitcher_service.UpdateSlateRequest(),
            slate=slates.Slate(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_slate_flattened_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_slate), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = slates.Slate()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(slates.Slate())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_slate(
            slate=slates.Slate(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].slate
        mock_val = slates.Slate(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_slate_flattened_error_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_slate(
            video_stitcher_service.UpdateSlateRequest(),
            slate=slates.Slate(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.DeleteSlateRequest,
        dict,
    ],
)
def test_delete_slate(request_type, transport: str = "grpc"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_slate), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_slate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.DeleteSlateRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_slate_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_slate), "__call__") as call:
        client.delete_slate()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.DeleteSlateRequest()


@pytest.mark.asyncio
async def test_delete_slate_async(
    transport: str = "grpc_asyncio",
    request_type=video_stitcher_service.DeleteSlateRequest,
):
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_slate), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_slate(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.DeleteSlateRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_slate_async_from_dict():
    await test_delete_slate_async(request_type=dict)


def test_delete_slate_field_headers():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.DeleteSlateRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_slate), "__call__") as call:
        call.return_value = None
        client.delete_slate(request)

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
async def test_delete_slate_field_headers_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.DeleteSlateRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_slate), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_slate(request)

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


def test_delete_slate_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_slate), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_slate(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_slate_flattened_error():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_slate(
            video_stitcher_service.DeleteSlateRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_slate_flattened_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_slate), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_slate(
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
async def test_delete_slate_flattened_error_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_slate(
            video_stitcher_service.DeleteSlateRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.CreateLiveSessionRequest,
        dict,
    ],
)
def test_create_live_session(request_type, transport: str = "grpc"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_live_session), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = sessions.LiveSession(
            name="name_value",
            play_uri="play_uri_value",
            source_uri="source_uri_value",
            default_ad_tag_id="default_ad_tag_id_value",
            client_ad_tracking=True,
            default_slate_id="default_slate_id_value",
            stitching_policy=sessions.LiveSession.StitchingPolicy.COMPLETE_AD,
            stream_id="stream_id_value",
        )
        response = client.create_live_session(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.CreateLiveSessionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, sessions.LiveSession)
    assert response.name == "name_value"
    assert response.play_uri == "play_uri_value"
    assert response.source_uri == "source_uri_value"
    assert response.default_ad_tag_id == "default_ad_tag_id_value"
    assert response.client_ad_tracking is True
    assert response.default_slate_id == "default_slate_id_value"
    assert response.stitching_policy == sessions.LiveSession.StitchingPolicy.COMPLETE_AD
    assert response.stream_id == "stream_id_value"


def test_create_live_session_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_live_session), "__call__"
    ) as call:
        client.create_live_session()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.CreateLiveSessionRequest()


@pytest.mark.asyncio
async def test_create_live_session_async(
    transport: str = "grpc_asyncio",
    request_type=video_stitcher_service.CreateLiveSessionRequest,
):
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_live_session), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            sessions.LiveSession(
                name="name_value",
                play_uri="play_uri_value",
                source_uri="source_uri_value",
                default_ad_tag_id="default_ad_tag_id_value",
                client_ad_tracking=True,
                default_slate_id="default_slate_id_value",
                stitching_policy=sessions.LiveSession.StitchingPolicy.COMPLETE_AD,
                stream_id="stream_id_value",
            )
        )
        response = await client.create_live_session(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.CreateLiveSessionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, sessions.LiveSession)
    assert response.name == "name_value"
    assert response.play_uri == "play_uri_value"
    assert response.source_uri == "source_uri_value"
    assert response.default_ad_tag_id == "default_ad_tag_id_value"
    assert response.client_ad_tracking is True
    assert response.default_slate_id == "default_slate_id_value"
    assert response.stitching_policy == sessions.LiveSession.StitchingPolicy.COMPLETE_AD
    assert response.stream_id == "stream_id_value"


@pytest.mark.asyncio
async def test_create_live_session_async_from_dict():
    await test_create_live_session_async(request_type=dict)


def test_create_live_session_field_headers():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.CreateLiveSessionRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_live_session), "__call__"
    ) as call:
        call.return_value = sessions.LiveSession()
        client.create_live_session(request)

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
async def test_create_live_session_field_headers_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.CreateLiveSessionRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_live_session), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            sessions.LiveSession()
        )
        await client.create_live_session(request)

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


def test_create_live_session_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_live_session), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = sessions.LiveSession()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_live_session(
            parent="parent_value",
            live_session=sessions.LiveSession(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].live_session
        mock_val = sessions.LiveSession(name="name_value")
        assert arg == mock_val


def test_create_live_session_flattened_error():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_live_session(
            video_stitcher_service.CreateLiveSessionRequest(),
            parent="parent_value",
            live_session=sessions.LiveSession(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_live_session_flattened_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_live_session), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = sessions.LiveSession()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            sessions.LiveSession()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_live_session(
            parent="parent_value",
            live_session=sessions.LiveSession(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].live_session
        mock_val = sessions.LiveSession(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_live_session_flattened_error_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_live_session(
            video_stitcher_service.CreateLiveSessionRequest(),
            parent="parent_value",
            live_session=sessions.LiveSession(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.GetLiveSessionRequest,
        dict,
    ],
)
def test_get_live_session(request_type, transport: str = "grpc"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_live_session), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = sessions.LiveSession(
            name="name_value",
            play_uri="play_uri_value",
            source_uri="source_uri_value",
            default_ad_tag_id="default_ad_tag_id_value",
            client_ad_tracking=True,
            default_slate_id="default_slate_id_value",
            stitching_policy=sessions.LiveSession.StitchingPolicy.COMPLETE_AD,
            stream_id="stream_id_value",
        )
        response = client.get_live_session(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.GetLiveSessionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, sessions.LiveSession)
    assert response.name == "name_value"
    assert response.play_uri == "play_uri_value"
    assert response.source_uri == "source_uri_value"
    assert response.default_ad_tag_id == "default_ad_tag_id_value"
    assert response.client_ad_tracking is True
    assert response.default_slate_id == "default_slate_id_value"
    assert response.stitching_policy == sessions.LiveSession.StitchingPolicy.COMPLETE_AD
    assert response.stream_id == "stream_id_value"


def test_get_live_session_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_live_session), "__call__") as call:
        client.get_live_session()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.GetLiveSessionRequest()


@pytest.mark.asyncio
async def test_get_live_session_async(
    transport: str = "grpc_asyncio",
    request_type=video_stitcher_service.GetLiveSessionRequest,
):
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_live_session), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            sessions.LiveSession(
                name="name_value",
                play_uri="play_uri_value",
                source_uri="source_uri_value",
                default_ad_tag_id="default_ad_tag_id_value",
                client_ad_tracking=True,
                default_slate_id="default_slate_id_value",
                stitching_policy=sessions.LiveSession.StitchingPolicy.COMPLETE_AD,
                stream_id="stream_id_value",
            )
        )
        response = await client.get_live_session(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == video_stitcher_service.GetLiveSessionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, sessions.LiveSession)
    assert response.name == "name_value"
    assert response.play_uri == "play_uri_value"
    assert response.source_uri == "source_uri_value"
    assert response.default_ad_tag_id == "default_ad_tag_id_value"
    assert response.client_ad_tracking is True
    assert response.default_slate_id == "default_slate_id_value"
    assert response.stitching_policy == sessions.LiveSession.StitchingPolicy.COMPLETE_AD
    assert response.stream_id == "stream_id_value"


@pytest.mark.asyncio
async def test_get_live_session_async_from_dict():
    await test_get_live_session_async(request_type=dict)


def test_get_live_session_field_headers():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.GetLiveSessionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_live_session), "__call__") as call:
        call.return_value = sessions.LiveSession()
        client.get_live_session(request)

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
async def test_get_live_session_field_headers_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = video_stitcher_service.GetLiveSessionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_live_session), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            sessions.LiveSession()
        )
        await client.get_live_session(request)

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


def test_get_live_session_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_live_session), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = sessions.LiveSession()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_live_session(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_live_session_flattened_error():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_live_session(
            video_stitcher_service.GetLiveSessionRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_live_session_flattened_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_live_session), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = sessions.LiveSession()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            sessions.LiveSession()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_live_session(
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
async def test_get_live_session_flattened_error_async():
    client = VideoStitcherServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_live_session(
            video_stitcher_service.GetLiveSessionRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.CreateCdnKeyRequest,
        dict,
    ],
)
def test_create_cdn_key_rest(request_type):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["cdn_key"] = {
        "google_cdn_key": {
            "private_key": b"private_key_blob",
            "key_name": "key_name_value",
        },
        "akamai_cdn_key": {"token_key": b"token_key_blob"},
        "media_cdn_key": {
            "private_key": b"private_key_blob",
            "key_name": "key_name_value",
        },
        "name": "name_value",
        "hostname": "hostname_value",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cdn_keys.CdnKey(
            name="name_value",
            hostname="hostname_value",
            google_cdn_key=cdn_keys.GoogleCdnKey(private_key=b"private_key_blob"),
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = cdn_keys.CdnKey.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_cdn_key(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, cdn_keys.CdnKey)
    assert response.name == "name_value"
    assert response.hostname == "hostname_value"


def test_create_cdn_key_rest_required_fields(
    request_type=video_stitcher_service.CreateCdnKeyRequest,
):
    transport_class = transports.VideoStitcherServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["cdn_key_id"] = ""
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
    assert "cdnKeyId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_cdn_key._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "cdnKeyId" in jsonified_request
    assert jsonified_request["cdnKeyId"] == request_init["cdn_key_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["cdnKeyId"] = "cdn_key_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_cdn_key._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("cdn_key_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "cdnKeyId" in jsonified_request
    assert jsonified_request["cdnKeyId"] == "cdn_key_id_value"

    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = cdn_keys.CdnKey()
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

            pb_return_value = cdn_keys.CdnKey.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_cdn_key(request)

            expected_params = [
                (
                    "cdnKeyId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_cdn_key_rest_unset_required_fields():
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_cdn_key._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("cdnKeyId",))
        & set(
            (
                "parent",
                "cdnKey",
                "cdnKeyId",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_cdn_key_rest_interceptors(null_interceptor):
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.VideoStitcherServiceRestInterceptor(),
    )
    client = VideoStitcherServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.VideoStitcherServiceRestInterceptor, "post_create_cdn_key"
    ) as post, mock.patch.object(
        transports.VideoStitcherServiceRestInterceptor, "pre_create_cdn_key"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = video_stitcher_service.CreateCdnKeyRequest.pb(
            video_stitcher_service.CreateCdnKeyRequest()
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
        req.return_value._content = cdn_keys.CdnKey.to_json(cdn_keys.CdnKey())

        request = video_stitcher_service.CreateCdnKeyRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = cdn_keys.CdnKey()

        client.create_cdn_key(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_cdn_key_rest_bad_request(
    transport: str = "rest", request_type=video_stitcher_service.CreateCdnKeyRequest
):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["cdn_key"] = {
        "google_cdn_key": {
            "private_key": b"private_key_blob",
            "key_name": "key_name_value",
        },
        "akamai_cdn_key": {"token_key": b"token_key_blob"},
        "media_cdn_key": {
            "private_key": b"private_key_blob",
            "key_name": "key_name_value",
        },
        "name": "name_value",
        "hostname": "hostname_value",
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
        client.create_cdn_key(request)


def test_create_cdn_key_rest_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cdn_keys.CdnKey()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            cdn_key=cdn_keys.CdnKey(
                google_cdn_key=cdn_keys.GoogleCdnKey(private_key=b"private_key_blob")
            ),
            cdn_key_id="cdn_key_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = cdn_keys.CdnKey.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_cdn_key(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/cdnKeys" % client.transport._host,
            args[1],
        )


def test_create_cdn_key_rest_flattened_error(transport: str = "rest"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_cdn_key(
            video_stitcher_service.CreateCdnKeyRequest(),
            parent="parent_value",
            cdn_key=cdn_keys.CdnKey(
                google_cdn_key=cdn_keys.GoogleCdnKey(private_key=b"private_key_blob")
            ),
            cdn_key_id="cdn_key_id_value",
        )


def test_create_cdn_key_rest_error():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.ListCdnKeysRequest,
        dict,
    ],
)
def test_list_cdn_keys_rest(request_type):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = video_stitcher_service.ListCdnKeysResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = video_stitcher_service.ListCdnKeysResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_cdn_keys(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCdnKeysPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_cdn_keys_rest_required_fields(
    request_type=video_stitcher_service.ListCdnKeysRequest,
):
    transport_class = transports.VideoStitcherServiceRestTransport

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
    ).list_cdn_keys._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_cdn_keys._get_unset_required_fields(jsonified_request)
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

    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = video_stitcher_service.ListCdnKeysResponse()
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

            pb_return_value = video_stitcher_service.ListCdnKeysResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_cdn_keys(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_cdn_keys_rest_unset_required_fields():
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_cdn_keys._get_unset_required_fields({})
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
def test_list_cdn_keys_rest_interceptors(null_interceptor):
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.VideoStitcherServiceRestInterceptor(),
    )
    client = VideoStitcherServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.VideoStitcherServiceRestInterceptor, "post_list_cdn_keys"
    ) as post, mock.patch.object(
        transports.VideoStitcherServiceRestInterceptor, "pre_list_cdn_keys"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = video_stitcher_service.ListCdnKeysRequest.pb(
            video_stitcher_service.ListCdnKeysRequest()
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
        req.return_value._content = video_stitcher_service.ListCdnKeysResponse.to_json(
            video_stitcher_service.ListCdnKeysResponse()
        )

        request = video_stitcher_service.ListCdnKeysRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = video_stitcher_service.ListCdnKeysResponse()

        client.list_cdn_keys(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_cdn_keys_rest_bad_request(
    transport: str = "rest", request_type=video_stitcher_service.ListCdnKeysRequest
):
    client = VideoStitcherServiceClient(
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
        client.list_cdn_keys(request)


def test_list_cdn_keys_rest_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = video_stitcher_service.ListCdnKeysResponse()

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
        pb_return_value = video_stitcher_service.ListCdnKeysResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_cdn_keys(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/cdnKeys" % client.transport._host,
            args[1],
        )


def test_list_cdn_keys_rest_flattened_error(transport: str = "rest"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_cdn_keys(
            video_stitcher_service.ListCdnKeysRequest(),
            parent="parent_value",
        )


def test_list_cdn_keys_rest_pager(transport: str = "rest"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            video_stitcher_service.ListCdnKeysResponse(
                cdn_keys=[
                    cdn_keys.CdnKey(),
                    cdn_keys.CdnKey(),
                    cdn_keys.CdnKey(),
                ],
                next_page_token="abc",
            ),
            video_stitcher_service.ListCdnKeysResponse(
                cdn_keys=[],
                next_page_token="def",
            ),
            video_stitcher_service.ListCdnKeysResponse(
                cdn_keys=[
                    cdn_keys.CdnKey(),
                ],
                next_page_token="ghi",
            ),
            video_stitcher_service.ListCdnKeysResponse(
                cdn_keys=[
                    cdn_keys.CdnKey(),
                    cdn_keys.CdnKey(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            video_stitcher_service.ListCdnKeysResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_cdn_keys(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, cdn_keys.CdnKey) for i in results)

        pages = list(client.list_cdn_keys(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.GetCdnKeyRequest,
        dict,
    ],
)
def test_get_cdn_key_rest(request_type):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/cdnKeys/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cdn_keys.CdnKey(
            name="name_value",
            hostname="hostname_value",
            google_cdn_key=cdn_keys.GoogleCdnKey(private_key=b"private_key_blob"),
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = cdn_keys.CdnKey.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_cdn_key(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, cdn_keys.CdnKey)
    assert response.name == "name_value"
    assert response.hostname == "hostname_value"


def test_get_cdn_key_rest_required_fields(
    request_type=video_stitcher_service.GetCdnKeyRequest,
):
    transport_class = transports.VideoStitcherServiceRestTransport

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
    ).get_cdn_key._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_cdn_key._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = cdn_keys.CdnKey()
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

            pb_return_value = cdn_keys.CdnKey.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_cdn_key(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_cdn_key_rest_unset_required_fields():
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_cdn_key._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_cdn_key_rest_interceptors(null_interceptor):
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.VideoStitcherServiceRestInterceptor(),
    )
    client = VideoStitcherServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.VideoStitcherServiceRestInterceptor, "post_get_cdn_key"
    ) as post, mock.patch.object(
        transports.VideoStitcherServiceRestInterceptor, "pre_get_cdn_key"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = video_stitcher_service.GetCdnKeyRequest.pb(
            video_stitcher_service.GetCdnKeyRequest()
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
        req.return_value._content = cdn_keys.CdnKey.to_json(cdn_keys.CdnKey())

        request = video_stitcher_service.GetCdnKeyRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = cdn_keys.CdnKey()

        client.get_cdn_key(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_cdn_key_rest_bad_request(
    transport: str = "rest", request_type=video_stitcher_service.GetCdnKeyRequest
):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/cdnKeys/sample3"}
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
        client.get_cdn_key(request)


def test_get_cdn_key_rest_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cdn_keys.CdnKey()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/locations/sample2/cdnKeys/sample3"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = cdn_keys.CdnKey.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_cdn_key(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/cdnKeys/*}" % client.transport._host,
            args[1],
        )


def test_get_cdn_key_rest_flattened_error(transport: str = "rest"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_cdn_key(
            video_stitcher_service.GetCdnKeyRequest(),
            name="name_value",
        )


def test_get_cdn_key_rest_error():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.DeleteCdnKeyRequest,
        dict,
    ],
)
def test_delete_cdn_key_rest(request_type):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/cdnKeys/sample3"}
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
        response = client.delete_cdn_key(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_cdn_key_rest_required_fields(
    request_type=video_stitcher_service.DeleteCdnKeyRequest,
):
    transport_class = transports.VideoStitcherServiceRestTransport

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
    ).delete_cdn_key._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_cdn_key._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = VideoStitcherServiceClient(
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

            response = client.delete_cdn_key(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_cdn_key_rest_unset_required_fields():
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_cdn_key._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_cdn_key_rest_interceptors(null_interceptor):
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.VideoStitcherServiceRestInterceptor(),
    )
    client = VideoStitcherServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.VideoStitcherServiceRestInterceptor, "pre_delete_cdn_key"
    ) as pre:
        pre.assert_not_called()
        pb_message = video_stitcher_service.DeleteCdnKeyRequest.pb(
            video_stitcher_service.DeleteCdnKeyRequest()
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

        request = video_stitcher_service.DeleteCdnKeyRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_cdn_key(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_delete_cdn_key_rest_bad_request(
    transport: str = "rest", request_type=video_stitcher_service.DeleteCdnKeyRequest
):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/cdnKeys/sample3"}
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
        client.delete_cdn_key(request)


def test_delete_cdn_key_rest_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/locations/sample2/cdnKeys/sample3"}

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

        client.delete_cdn_key(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/cdnKeys/*}" % client.transport._host,
            args[1],
        )


def test_delete_cdn_key_rest_flattened_error(transport: str = "rest"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_cdn_key(
            video_stitcher_service.DeleteCdnKeyRequest(),
            name="name_value",
        )


def test_delete_cdn_key_rest_error():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.UpdateCdnKeyRequest,
        dict,
    ],
)
def test_update_cdn_key_rest(request_type):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "cdn_key": {"name": "projects/sample1/locations/sample2/cdnKeys/sample3"}
    }
    request_init["cdn_key"] = {
        "google_cdn_key": {
            "private_key": b"private_key_blob",
            "key_name": "key_name_value",
        },
        "akamai_cdn_key": {"token_key": b"token_key_blob"},
        "media_cdn_key": {
            "private_key": b"private_key_blob",
            "key_name": "key_name_value",
        },
        "name": "projects/sample1/locations/sample2/cdnKeys/sample3",
        "hostname": "hostname_value",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cdn_keys.CdnKey(
            name="name_value",
            hostname="hostname_value",
            google_cdn_key=cdn_keys.GoogleCdnKey(private_key=b"private_key_blob"),
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = cdn_keys.CdnKey.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_cdn_key(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, cdn_keys.CdnKey)
    assert response.name == "name_value"
    assert response.hostname == "hostname_value"


def test_update_cdn_key_rest_required_fields(
    request_type=video_stitcher_service.UpdateCdnKeyRequest,
):
    transport_class = transports.VideoStitcherServiceRestTransport

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
    ).update_cdn_key._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_cdn_key._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = cdn_keys.CdnKey()
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

            pb_return_value = cdn_keys.CdnKey.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_cdn_key(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_cdn_key_rest_unset_required_fields():
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_cdn_key._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("updateMask",))
        & set(
            (
                "cdnKey",
                "updateMask",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_cdn_key_rest_interceptors(null_interceptor):
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.VideoStitcherServiceRestInterceptor(),
    )
    client = VideoStitcherServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.VideoStitcherServiceRestInterceptor, "post_update_cdn_key"
    ) as post, mock.patch.object(
        transports.VideoStitcherServiceRestInterceptor, "pre_update_cdn_key"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = video_stitcher_service.UpdateCdnKeyRequest.pb(
            video_stitcher_service.UpdateCdnKeyRequest()
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
        req.return_value._content = cdn_keys.CdnKey.to_json(cdn_keys.CdnKey())

        request = video_stitcher_service.UpdateCdnKeyRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = cdn_keys.CdnKey()

        client.update_cdn_key(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_cdn_key_rest_bad_request(
    transport: str = "rest", request_type=video_stitcher_service.UpdateCdnKeyRequest
):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "cdn_key": {"name": "projects/sample1/locations/sample2/cdnKeys/sample3"}
    }
    request_init["cdn_key"] = {
        "google_cdn_key": {
            "private_key": b"private_key_blob",
            "key_name": "key_name_value",
        },
        "akamai_cdn_key": {"token_key": b"token_key_blob"},
        "media_cdn_key": {
            "private_key": b"private_key_blob",
            "key_name": "key_name_value",
        },
        "name": "projects/sample1/locations/sample2/cdnKeys/sample3",
        "hostname": "hostname_value",
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
        client.update_cdn_key(request)


def test_update_cdn_key_rest_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cdn_keys.CdnKey()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "cdn_key": {"name": "projects/sample1/locations/sample2/cdnKeys/sample3"}
        }

        # get truthy value for each flattened field
        mock_args = dict(
            cdn_key=cdn_keys.CdnKey(
                google_cdn_key=cdn_keys.GoogleCdnKey(private_key=b"private_key_blob")
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = cdn_keys.CdnKey.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_cdn_key(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{cdn_key.name=projects/*/locations/*/cdnKeys/*}"
            % client.transport._host,
            args[1],
        )


def test_update_cdn_key_rest_flattened_error(transport: str = "rest"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_cdn_key(
            video_stitcher_service.UpdateCdnKeyRequest(),
            cdn_key=cdn_keys.CdnKey(
                google_cdn_key=cdn_keys.GoogleCdnKey(private_key=b"private_key_blob")
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_cdn_key_rest_error():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.CreateVodSessionRequest,
        dict,
    ],
)
def test_create_vod_session_rest(request_type):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["vod_session"] = {
        "name": "name_value",
        "interstitials": {
            "ad_breaks": [
                {
                    "progress_events": [
                        {
                            "time_offset": {"seconds": 751, "nanos": 543},
                            "events": [
                                {
                                    "type_": 1,
                                    "uri": "uri_value",
                                    "id": "id_value",
                                    "offset": {},
                                }
                            ],
                        }
                    ],
                    "ads": [
                        {
                            "duration": {},
                            "companion_ads": {
                                "display_requirement": 1,
                                "companions": [
                                    {
                                        "iframe_ad_resource": {"uri": "uri_value"},
                                        "static_ad_resource": {
                                            "uri": "uri_value",
                                            "creative_type": "creative_type_value",
                                        },
                                        "html_ad_resource": {
                                            "html_source": "html_source_value"
                                        },
                                        "api_framework": "api_framework_value",
                                        "height_px": 960,
                                        "width_px": 871,
                                        "asset_height_px": 1599,
                                        "expanded_height_px": 1896,
                                        "asset_width_px": 1510,
                                        "expanded_width_px": 1807,
                                        "ad_slot_id": "ad_slot_id_value",
                                        "events": {},
                                    }
                                ],
                            },
                            "activity_events": {},
                        }
                    ],
                    "end_time_offset": {},
                    "start_time_offset": {},
                }
            ],
            "session_content": {"duration": {}},
        },
        "play_uri": "play_uri_value",
        "source_uri": "source_uri_value",
        "ad_tag_uri": "ad_tag_uri_value",
        "ad_tag_macro_map": {},
        "client_ad_tracking": True,
        "manifest_options": {
            "include_renditions": [{"bitrate_bps": 1167, "codecs": "codecs_value"}],
            "bitrate_order": 1,
        },
        "asset_id": "asset_id_value",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = sessions.VodSession(
            name="name_value",
            play_uri="play_uri_value",
            source_uri="source_uri_value",
            ad_tag_uri="ad_tag_uri_value",
            client_ad_tracking=True,
            asset_id="asset_id_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = sessions.VodSession.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_vod_session(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, sessions.VodSession)
    assert response.name == "name_value"
    assert response.play_uri == "play_uri_value"
    assert response.source_uri == "source_uri_value"
    assert response.ad_tag_uri == "ad_tag_uri_value"
    assert response.client_ad_tracking is True
    assert response.asset_id == "asset_id_value"


def test_create_vod_session_rest_required_fields(
    request_type=video_stitcher_service.CreateVodSessionRequest,
):
    transport_class = transports.VideoStitcherServiceRestTransport

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
    ).create_vod_session._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_vod_session._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = sessions.VodSession()
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

            pb_return_value = sessions.VodSession.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_vod_session(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_vod_session_rest_unset_required_fields():
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_vod_session._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "vodSession",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_vod_session_rest_interceptors(null_interceptor):
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.VideoStitcherServiceRestInterceptor(),
    )
    client = VideoStitcherServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.VideoStitcherServiceRestInterceptor, "post_create_vod_session"
    ) as post, mock.patch.object(
        transports.VideoStitcherServiceRestInterceptor, "pre_create_vod_session"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = video_stitcher_service.CreateVodSessionRequest.pb(
            video_stitcher_service.CreateVodSessionRequest()
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
        req.return_value._content = sessions.VodSession.to_json(sessions.VodSession())

        request = video_stitcher_service.CreateVodSessionRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = sessions.VodSession()

        client.create_vod_session(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_vod_session_rest_bad_request(
    transport: str = "rest", request_type=video_stitcher_service.CreateVodSessionRequest
):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["vod_session"] = {
        "name": "name_value",
        "interstitials": {
            "ad_breaks": [
                {
                    "progress_events": [
                        {
                            "time_offset": {"seconds": 751, "nanos": 543},
                            "events": [
                                {
                                    "type_": 1,
                                    "uri": "uri_value",
                                    "id": "id_value",
                                    "offset": {},
                                }
                            ],
                        }
                    ],
                    "ads": [
                        {
                            "duration": {},
                            "companion_ads": {
                                "display_requirement": 1,
                                "companions": [
                                    {
                                        "iframe_ad_resource": {"uri": "uri_value"},
                                        "static_ad_resource": {
                                            "uri": "uri_value",
                                            "creative_type": "creative_type_value",
                                        },
                                        "html_ad_resource": {
                                            "html_source": "html_source_value"
                                        },
                                        "api_framework": "api_framework_value",
                                        "height_px": 960,
                                        "width_px": 871,
                                        "asset_height_px": 1599,
                                        "expanded_height_px": 1896,
                                        "asset_width_px": 1510,
                                        "expanded_width_px": 1807,
                                        "ad_slot_id": "ad_slot_id_value",
                                        "events": {},
                                    }
                                ],
                            },
                            "activity_events": {},
                        }
                    ],
                    "end_time_offset": {},
                    "start_time_offset": {},
                }
            ],
            "session_content": {"duration": {}},
        },
        "play_uri": "play_uri_value",
        "source_uri": "source_uri_value",
        "ad_tag_uri": "ad_tag_uri_value",
        "ad_tag_macro_map": {},
        "client_ad_tracking": True,
        "manifest_options": {
            "include_renditions": [{"bitrate_bps": 1167, "codecs": "codecs_value"}],
            "bitrate_order": 1,
        },
        "asset_id": "asset_id_value",
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
        client.create_vod_session(request)


def test_create_vod_session_rest_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = sessions.VodSession()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            vod_session=sessions.VodSession(name="name_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = sessions.VodSession.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_vod_session(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/vodSessions"
            % client.transport._host,
            args[1],
        )


def test_create_vod_session_rest_flattened_error(transport: str = "rest"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_vod_session(
            video_stitcher_service.CreateVodSessionRequest(),
            parent="parent_value",
            vod_session=sessions.VodSession(name="name_value"),
        )


def test_create_vod_session_rest_error():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.GetVodSessionRequest,
        dict,
    ],
)
def test_get_vod_session_rest(request_type):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/vodSessions/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = sessions.VodSession(
            name="name_value",
            play_uri="play_uri_value",
            source_uri="source_uri_value",
            ad_tag_uri="ad_tag_uri_value",
            client_ad_tracking=True,
            asset_id="asset_id_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = sessions.VodSession.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_vod_session(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, sessions.VodSession)
    assert response.name == "name_value"
    assert response.play_uri == "play_uri_value"
    assert response.source_uri == "source_uri_value"
    assert response.ad_tag_uri == "ad_tag_uri_value"
    assert response.client_ad_tracking is True
    assert response.asset_id == "asset_id_value"


def test_get_vod_session_rest_required_fields(
    request_type=video_stitcher_service.GetVodSessionRequest,
):
    transport_class = transports.VideoStitcherServiceRestTransport

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
    ).get_vod_session._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_vod_session._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = sessions.VodSession()
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

            pb_return_value = sessions.VodSession.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_vod_session(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_vod_session_rest_unset_required_fields():
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_vod_session._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_vod_session_rest_interceptors(null_interceptor):
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.VideoStitcherServiceRestInterceptor(),
    )
    client = VideoStitcherServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.VideoStitcherServiceRestInterceptor, "post_get_vod_session"
    ) as post, mock.patch.object(
        transports.VideoStitcherServiceRestInterceptor, "pre_get_vod_session"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = video_stitcher_service.GetVodSessionRequest.pb(
            video_stitcher_service.GetVodSessionRequest()
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
        req.return_value._content = sessions.VodSession.to_json(sessions.VodSession())

        request = video_stitcher_service.GetVodSessionRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = sessions.VodSession()

        client.get_vod_session(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_vod_session_rest_bad_request(
    transport: str = "rest", request_type=video_stitcher_service.GetVodSessionRequest
):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/vodSessions/sample3"}
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
        client.get_vod_session(request)


def test_get_vod_session_rest_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = sessions.VodSession()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/vodSessions/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = sessions.VodSession.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_vod_session(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/vodSessions/*}"
            % client.transport._host,
            args[1],
        )


def test_get_vod_session_rest_flattened_error(transport: str = "rest"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_vod_session(
            video_stitcher_service.GetVodSessionRequest(),
            name="name_value",
        )


def test_get_vod_session_rest_error():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.ListVodStitchDetailsRequest,
        dict,
    ],
)
def test_list_vod_stitch_details_rest(request_type):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/vodSessions/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = video_stitcher_service.ListVodStitchDetailsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = video_stitcher_service.ListVodStitchDetailsResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_vod_stitch_details(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListVodStitchDetailsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_vod_stitch_details_rest_required_fields(
    request_type=video_stitcher_service.ListVodStitchDetailsRequest,
):
    transport_class = transports.VideoStitcherServiceRestTransport

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
    ).list_vod_stitch_details._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_vod_stitch_details._get_unset_required_fields(jsonified_request)
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

    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = video_stitcher_service.ListVodStitchDetailsResponse()
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

            pb_return_value = video_stitcher_service.ListVodStitchDetailsResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_vod_stitch_details(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_vod_stitch_details_rest_unset_required_fields():
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_vod_stitch_details._get_unset_required_fields({})
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
def test_list_vod_stitch_details_rest_interceptors(null_interceptor):
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.VideoStitcherServiceRestInterceptor(),
    )
    client = VideoStitcherServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.VideoStitcherServiceRestInterceptor, "post_list_vod_stitch_details"
    ) as post, mock.patch.object(
        transports.VideoStitcherServiceRestInterceptor, "pre_list_vod_stitch_details"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = video_stitcher_service.ListVodStitchDetailsRequest.pb(
            video_stitcher_service.ListVodStitchDetailsRequest()
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
            video_stitcher_service.ListVodStitchDetailsResponse.to_json(
                video_stitcher_service.ListVodStitchDetailsResponse()
            )
        )

        request = video_stitcher_service.ListVodStitchDetailsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = video_stitcher_service.ListVodStitchDetailsResponse()

        client.list_vod_stitch_details(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_vod_stitch_details_rest_bad_request(
    transport: str = "rest",
    request_type=video_stitcher_service.ListVodStitchDetailsRequest,
):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/vodSessions/sample3"}
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
        client.list_vod_stitch_details(request)


def test_list_vod_stitch_details_rest_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = video_stitcher_service.ListVodStitchDetailsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/vodSessions/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = video_stitcher_service.ListVodStitchDetailsResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_vod_stitch_details(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/vodSessions/*}/vodStitchDetails"
            % client.transport._host,
            args[1],
        )


def test_list_vod_stitch_details_rest_flattened_error(transport: str = "rest"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_vod_stitch_details(
            video_stitcher_service.ListVodStitchDetailsRequest(),
            parent="parent_value",
        )


def test_list_vod_stitch_details_rest_pager(transport: str = "rest"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            video_stitcher_service.ListVodStitchDetailsResponse(
                vod_stitch_details=[
                    stitch_details.VodStitchDetail(),
                    stitch_details.VodStitchDetail(),
                    stitch_details.VodStitchDetail(),
                ],
                next_page_token="abc",
            ),
            video_stitcher_service.ListVodStitchDetailsResponse(
                vod_stitch_details=[],
                next_page_token="def",
            ),
            video_stitcher_service.ListVodStitchDetailsResponse(
                vod_stitch_details=[
                    stitch_details.VodStitchDetail(),
                ],
                next_page_token="ghi",
            ),
            video_stitcher_service.ListVodStitchDetailsResponse(
                vod_stitch_details=[
                    stitch_details.VodStitchDetail(),
                    stitch_details.VodStitchDetail(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            video_stitcher_service.ListVodStitchDetailsResponse.to_json(x)
            for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/vodSessions/sample3"
        }

        pager = client.list_vod_stitch_details(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, stitch_details.VodStitchDetail) for i in results)

        pages = list(client.list_vod_stitch_details(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.GetVodStitchDetailRequest,
        dict,
    ],
)
def test_get_vod_stitch_detail_rest(request_type):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/vodSessions/sample3/vodStitchDetails/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = stitch_details.VodStitchDetail(
            name="name_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = stitch_details.VodStitchDetail.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_vod_stitch_detail(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, stitch_details.VodStitchDetail)
    assert response.name == "name_value"


def test_get_vod_stitch_detail_rest_required_fields(
    request_type=video_stitcher_service.GetVodStitchDetailRequest,
):
    transport_class = transports.VideoStitcherServiceRestTransport

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
    ).get_vod_stitch_detail._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_vod_stitch_detail._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = stitch_details.VodStitchDetail()
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

            pb_return_value = stitch_details.VodStitchDetail.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_vod_stitch_detail(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_vod_stitch_detail_rest_unset_required_fields():
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_vod_stitch_detail._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_vod_stitch_detail_rest_interceptors(null_interceptor):
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.VideoStitcherServiceRestInterceptor(),
    )
    client = VideoStitcherServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.VideoStitcherServiceRestInterceptor, "post_get_vod_stitch_detail"
    ) as post, mock.patch.object(
        transports.VideoStitcherServiceRestInterceptor, "pre_get_vod_stitch_detail"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = video_stitcher_service.GetVodStitchDetailRequest.pb(
            video_stitcher_service.GetVodStitchDetailRequest()
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
        req.return_value._content = stitch_details.VodStitchDetail.to_json(
            stitch_details.VodStitchDetail()
        )

        request = video_stitcher_service.GetVodStitchDetailRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = stitch_details.VodStitchDetail()

        client.get_vod_stitch_detail(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_vod_stitch_detail_rest_bad_request(
    transport: str = "rest",
    request_type=video_stitcher_service.GetVodStitchDetailRequest,
):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/vodSessions/sample3/vodStitchDetails/sample4"
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
        client.get_vod_stitch_detail(request)


def test_get_vod_stitch_detail_rest_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = stitch_details.VodStitchDetail()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/vodSessions/sample3/vodStitchDetails/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = stitch_details.VodStitchDetail.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_vod_stitch_detail(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/vodSessions/*/vodStitchDetails/*}"
            % client.transport._host,
            args[1],
        )


def test_get_vod_stitch_detail_rest_flattened_error(transport: str = "rest"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_vod_stitch_detail(
            video_stitcher_service.GetVodStitchDetailRequest(),
            name="name_value",
        )


def test_get_vod_stitch_detail_rest_error():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.ListVodAdTagDetailsRequest,
        dict,
    ],
)
def test_list_vod_ad_tag_details_rest(request_type):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/vodSessions/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = video_stitcher_service.ListVodAdTagDetailsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = video_stitcher_service.ListVodAdTagDetailsResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_vod_ad_tag_details(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListVodAdTagDetailsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_vod_ad_tag_details_rest_required_fields(
    request_type=video_stitcher_service.ListVodAdTagDetailsRequest,
):
    transport_class = transports.VideoStitcherServiceRestTransport

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
    ).list_vod_ad_tag_details._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_vod_ad_tag_details._get_unset_required_fields(jsonified_request)
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

    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = video_stitcher_service.ListVodAdTagDetailsResponse()
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

            pb_return_value = video_stitcher_service.ListVodAdTagDetailsResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_vod_ad_tag_details(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_vod_ad_tag_details_rest_unset_required_fields():
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_vod_ad_tag_details._get_unset_required_fields({})
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
def test_list_vod_ad_tag_details_rest_interceptors(null_interceptor):
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.VideoStitcherServiceRestInterceptor(),
    )
    client = VideoStitcherServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.VideoStitcherServiceRestInterceptor, "post_list_vod_ad_tag_details"
    ) as post, mock.patch.object(
        transports.VideoStitcherServiceRestInterceptor, "pre_list_vod_ad_tag_details"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = video_stitcher_service.ListVodAdTagDetailsRequest.pb(
            video_stitcher_service.ListVodAdTagDetailsRequest()
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
            video_stitcher_service.ListVodAdTagDetailsResponse.to_json(
                video_stitcher_service.ListVodAdTagDetailsResponse()
            )
        )

        request = video_stitcher_service.ListVodAdTagDetailsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = video_stitcher_service.ListVodAdTagDetailsResponse()

        client.list_vod_ad_tag_details(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_vod_ad_tag_details_rest_bad_request(
    transport: str = "rest",
    request_type=video_stitcher_service.ListVodAdTagDetailsRequest,
):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/vodSessions/sample3"}
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
        client.list_vod_ad_tag_details(request)


def test_list_vod_ad_tag_details_rest_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = video_stitcher_service.ListVodAdTagDetailsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/vodSessions/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = video_stitcher_service.ListVodAdTagDetailsResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_vod_ad_tag_details(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/vodSessions/*}/vodAdTagDetails"
            % client.transport._host,
            args[1],
        )


def test_list_vod_ad_tag_details_rest_flattened_error(transport: str = "rest"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_vod_ad_tag_details(
            video_stitcher_service.ListVodAdTagDetailsRequest(),
            parent="parent_value",
        )


def test_list_vod_ad_tag_details_rest_pager(transport: str = "rest"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            video_stitcher_service.ListVodAdTagDetailsResponse(
                vod_ad_tag_details=[
                    ad_tag_details.VodAdTagDetail(),
                    ad_tag_details.VodAdTagDetail(),
                    ad_tag_details.VodAdTagDetail(),
                ],
                next_page_token="abc",
            ),
            video_stitcher_service.ListVodAdTagDetailsResponse(
                vod_ad_tag_details=[],
                next_page_token="def",
            ),
            video_stitcher_service.ListVodAdTagDetailsResponse(
                vod_ad_tag_details=[
                    ad_tag_details.VodAdTagDetail(),
                ],
                next_page_token="ghi",
            ),
            video_stitcher_service.ListVodAdTagDetailsResponse(
                vod_ad_tag_details=[
                    ad_tag_details.VodAdTagDetail(),
                    ad_tag_details.VodAdTagDetail(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            video_stitcher_service.ListVodAdTagDetailsResponse.to_json(x)
            for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/vodSessions/sample3"
        }

        pager = client.list_vod_ad_tag_details(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, ad_tag_details.VodAdTagDetail) for i in results)

        pages = list(client.list_vod_ad_tag_details(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.GetVodAdTagDetailRequest,
        dict,
    ],
)
def test_get_vod_ad_tag_detail_rest(request_type):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/vodSessions/sample3/vodAdTagDetails/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = ad_tag_details.VodAdTagDetail(
            name="name_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = ad_tag_details.VodAdTagDetail.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_vod_ad_tag_detail(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, ad_tag_details.VodAdTagDetail)
    assert response.name == "name_value"


def test_get_vod_ad_tag_detail_rest_required_fields(
    request_type=video_stitcher_service.GetVodAdTagDetailRequest,
):
    transport_class = transports.VideoStitcherServiceRestTransport

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
    ).get_vod_ad_tag_detail._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_vod_ad_tag_detail._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = ad_tag_details.VodAdTagDetail()
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

            pb_return_value = ad_tag_details.VodAdTagDetail.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_vod_ad_tag_detail(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_vod_ad_tag_detail_rest_unset_required_fields():
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_vod_ad_tag_detail._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_vod_ad_tag_detail_rest_interceptors(null_interceptor):
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.VideoStitcherServiceRestInterceptor(),
    )
    client = VideoStitcherServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.VideoStitcherServiceRestInterceptor, "post_get_vod_ad_tag_detail"
    ) as post, mock.patch.object(
        transports.VideoStitcherServiceRestInterceptor, "pre_get_vod_ad_tag_detail"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = video_stitcher_service.GetVodAdTagDetailRequest.pb(
            video_stitcher_service.GetVodAdTagDetailRequest()
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
        req.return_value._content = ad_tag_details.VodAdTagDetail.to_json(
            ad_tag_details.VodAdTagDetail()
        )

        request = video_stitcher_service.GetVodAdTagDetailRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = ad_tag_details.VodAdTagDetail()

        client.get_vod_ad_tag_detail(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_vod_ad_tag_detail_rest_bad_request(
    transport: str = "rest",
    request_type=video_stitcher_service.GetVodAdTagDetailRequest,
):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/vodSessions/sample3/vodAdTagDetails/sample4"
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
        client.get_vod_ad_tag_detail(request)


def test_get_vod_ad_tag_detail_rest_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = ad_tag_details.VodAdTagDetail()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/vodSessions/sample3/vodAdTagDetails/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = ad_tag_details.VodAdTagDetail.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_vod_ad_tag_detail(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/vodSessions/*/vodAdTagDetails/*}"
            % client.transport._host,
            args[1],
        )


def test_get_vod_ad_tag_detail_rest_flattened_error(transport: str = "rest"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_vod_ad_tag_detail(
            video_stitcher_service.GetVodAdTagDetailRequest(),
            name="name_value",
        )


def test_get_vod_ad_tag_detail_rest_error():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.ListLiveAdTagDetailsRequest,
        dict,
    ],
)
def test_list_live_ad_tag_details_rest(request_type):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/liveSessions/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = video_stitcher_service.ListLiveAdTagDetailsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = video_stitcher_service.ListLiveAdTagDetailsResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_live_ad_tag_details(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListLiveAdTagDetailsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_live_ad_tag_details_rest_required_fields(
    request_type=video_stitcher_service.ListLiveAdTagDetailsRequest,
):
    transport_class = transports.VideoStitcherServiceRestTransport

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
    ).list_live_ad_tag_details._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_live_ad_tag_details._get_unset_required_fields(jsonified_request)
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

    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = video_stitcher_service.ListLiveAdTagDetailsResponse()
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

            pb_return_value = video_stitcher_service.ListLiveAdTagDetailsResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_live_ad_tag_details(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_live_ad_tag_details_rest_unset_required_fields():
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_live_ad_tag_details._get_unset_required_fields({})
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
def test_list_live_ad_tag_details_rest_interceptors(null_interceptor):
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.VideoStitcherServiceRestInterceptor(),
    )
    client = VideoStitcherServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.VideoStitcherServiceRestInterceptor, "post_list_live_ad_tag_details"
    ) as post, mock.patch.object(
        transports.VideoStitcherServiceRestInterceptor, "pre_list_live_ad_tag_details"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = video_stitcher_service.ListLiveAdTagDetailsRequest.pb(
            video_stitcher_service.ListLiveAdTagDetailsRequest()
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
            video_stitcher_service.ListLiveAdTagDetailsResponse.to_json(
                video_stitcher_service.ListLiveAdTagDetailsResponse()
            )
        )

        request = video_stitcher_service.ListLiveAdTagDetailsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = video_stitcher_service.ListLiveAdTagDetailsResponse()

        client.list_live_ad_tag_details(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_live_ad_tag_details_rest_bad_request(
    transport: str = "rest",
    request_type=video_stitcher_service.ListLiveAdTagDetailsRequest,
):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/liveSessions/sample3"}
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
        client.list_live_ad_tag_details(request)


def test_list_live_ad_tag_details_rest_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = video_stitcher_service.ListLiveAdTagDetailsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/liveSessions/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = video_stitcher_service.ListLiveAdTagDetailsResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_live_ad_tag_details(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/liveSessions/*}/liveAdTagDetails"
            % client.transport._host,
            args[1],
        )


def test_list_live_ad_tag_details_rest_flattened_error(transport: str = "rest"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_live_ad_tag_details(
            video_stitcher_service.ListLiveAdTagDetailsRequest(),
            parent="parent_value",
        )


def test_list_live_ad_tag_details_rest_pager(transport: str = "rest"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            video_stitcher_service.ListLiveAdTagDetailsResponse(
                live_ad_tag_details=[
                    ad_tag_details.LiveAdTagDetail(),
                    ad_tag_details.LiveAdTagDetail(),
                    ad_tag_details.LiveAdTagDetail(),
                ],
                next_page_token="abc",
            ),
            video_stitcher_service.ListLiveAdTagDetailsResponse(
                live_ad_tag_details=[],
                next_page_token="def",
            ),
            video_stitcher_service.ListLiveAdTagDetailsResponse(
                live_ad_tag_details=[
                    ad_tag_details.LiveAdTagDetail(),
                ],
                next_page_token="ghi",
            ),
            video_stitcher_service.ListLiveAdTagDetailsResponse(
                live_ad_tag_details=[
                    ad_tag_details.LiveAdTagDetail(),
                    ad_tag_details.LiveAdTagDetail(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            video_stitcher_service.ListLiveAdTagDetailsResponse.to_json(x)
            for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/liveSessions/sample3"
        }

        pager = client.list_live_ad_tag_details(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, ad_tag_details.LiveAdTagDetail) for i in results)

        pages = list(client.list_live_ad_tag_details(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.GetLiveAdTagDetailRequest,
        dict,
    ],
)
def test_get_live_ad_tag_detail_rest(request_type):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/liveSessions/sample3/liveAdTagDetails/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = ad_tag_details.LiveAdTagDetail(
            name="name_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = ad_tag_details.LiveAdTagDetail.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_live_ad_tag_detail(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, ad_tag_details.LiveAdTagDetail)
    assert response.name == "name_value"


def test_get_live_ad_tag_detail_rest_required_fields(
    request_type=video_stitcher_service.GetLiveAdTagDetailRequest,
):
    transport_class = transports.VideoStitcherServiceRestTransport

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
    ).get_live_ad_tag_detail._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_live_ad_tag_detail._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = ad_tag_details.LiveAdTagDetail()
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

            pb_return_value = ad_tag_details.LiveAdTagDetail.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_live_ad_tag_detail(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_live_ad_tag_detail_rest_unset_required_fields():
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_live_ad_tag_detail._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_live_ad_tag_detail_rest_interceptors(null_interceptor):
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.VideoStitcherServiceRestInterceptor(),
    )
    client = VideoStitcherServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.VideoStitcherServiceRestInterceptor, "post_get_live_ad_tag_detail"
    ) as post, mock.patch.object(
        transports.VideoStitcherServiceRestInterceptor, "pre_get_live_ad_tag_detail"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = video_stitcher_service.GetLiveAdTagDetailRequest.pb(
            video_stitcher_service.GetLiveAdTagDetailRequest()
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
        req.return_value._content = ad_tag_details.LiveAdTagDetail.to_json(
            ad_tag_details.LiveAdTagDetail()
        )

        request = video_stitcher_service.GetLiveAdTagDetailRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = ad_tag_details.LiveAdTagDetail()

        client.get_live_ad_tag_detail(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_live_ad_tag_detail_rest_bad_request(
    transport: str = "rest",
    request_type=video_stitcher_service.GetLiveAdTagDetailRequest,
):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/liveSessions/sample3/liveAdTagDetails/sample4"
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
        client.get_live_ad_tag_detail(request)


def test_get_live_ad_tag_detail_rest_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = ad_tag_details.LiveAdTagDetail()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/liveSessions/sample3/liveAdTagDetails/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = ad_tag_details.LiveAdTagDetail.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_live_ad_tag_detail(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/liveSessions/*/liveAdTagDetails/*}"
            % client.transport._host,
            args[1],
        )


def test_get_live_ad_tag_detail_rest_flattened_error(transport: str = "rest"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_live_ad_tag_detail(
            video_stitcher_service.GetLiveAdTagDetailRequest(),
            name="name_value",
        )


def test_get_live_ad_tag_detail_rest_error():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.CreateSlateRequest,
        dict,
    ],
)
def test_create_slate_rest(request_type):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["slate"] = {"name": "name_value", "uri": "uri_value"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = slates.Slate(
            name="name_value",
            uri="uri_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = slates.Slate.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_slate(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, slates.Slate)
    assert response.name == "name_value"
    assert response.uri == "uri_value"


def test_create_slate_rest_required_fields(
    request_type=video_stitcher_service.CreateSlateRequest,
):
    transport_class = transports.VideoStitcherServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["slate_id"] = ""
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
    assert "slateId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_slate._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "slateId" in jsonified_request
    assert jsonified_request["slateId"] == request_init["slate_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["slateId"] = "slate_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_slate._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("slate_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "slateId" in jsonified_request
    assert jsonified_request["slateId"] == "slate_id_value"

    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = slates.Slate()
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

            pb_return_value = slates.Slate.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_slate(request)

            expected_params = [
                (
                    "slateId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_slate_rest_unset_required_fields():
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_slate._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("slateId",))
        & set(
            (
                "parent",
                "slateId",
                "slate",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_slate_rest_interceptors(null_interceptor):
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.VideoStitcherServiceRestInterceptor(),
    )
    client = VideoStitcherServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.VideoStitcherServiceRestInterceptor, "post_create_slate"
    ) as post, mock.patch.object(
        transports.VideoStitcherServiceRestInterceptor, "pre_create_slate"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = video_stitcher_service.CreateSlateRequest.pb(
            video_stitcher_service.CreateSlateRequest()
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
        req.return_value._content = slates.Slate.to_json(slates.Slate())

        request = video_stitcher_service.CreateSlateRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = slates.Slate()

        client.create_slate(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_slate_rest_bad_request(
    transport: str = "rest", request_type=video_stitcher_service.CreateSlateRequest
):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["slate"] = {"name": "name_value", "uri": "uri_value"}
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
        client.create_slate(request)


def test_create_slate_rest_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = slates.Slate()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            slate=slates.Slate(name="name_value"),
            slate_id="slate_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = slates.Slate.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_slate(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/slates" % client.transport._host,
            args[1],
        )


def test_create_slate_rest_flattened_error(transport: str = "rest"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_slate(
            video_stitcher_service.CreateSlateRequest(),
            parent="parent_value",
            slate=slates.Slate(name="name_value"),
            slate_id="slate_id_value",
        )


def test_create_slate_rest_error():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.ListSlatesRequest,
        dict,
    ],
)
def test_list_slates_rest(request_type):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = video_stitcher_service.ListSlatesResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = video_stitcher_service.ListSlatesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_slates(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListSlatesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_slates_rest_required_fields(
    request_type=video_stitcher_service.ListSlatesRequest,
):
    transport_class = transports.VideoStitcherServiceRestTransport

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
    ).list_slates._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_slates._get_unset_required_fields(jsonified_request)
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

    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = video_stitcher_service.ListSlatesResponse()
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

            pb_return_value = video_stitcher_service.ListSlatesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_slates(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_slates_rest_unset_required_fields():
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_slates._get_unset_required_fields({})
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
def test_list_slates_rest_interceptors(null_interceptor):
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.VideoStitcherServiceRestInterceptor(),
    )
    client = VideoStitcherServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.VideoStitcherServiceRestInterceptor, "post_list_slates"
    ) as post, mock.patch.object(
        transports.VideoStitcherServiceRestInterceptor, "pre_list_slates"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = video_stitcher_service.ListSlatesRequest.pb(
            video_stitcher_service.ListSlatesRequest()
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
        req.return_value._content = video_stitcher_service.ListSlatesResponse.to_json(
            video_stitcher_service.ListSlatesResponse()
        )

        request = video_stitcher_service.ListSlatesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = video_stitcher_service.ListSlatesResponse()

        client.list_slates(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_slates_rest_bad_request(
    transport: str = "rest", request_type=video_stitcher_service.ListSlatesRequest
):
    client = VideoStitcherServiceClient(
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
        client.list_slates(request)


def test_list_slates_rest_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = video_stitcher_service.ListSlatesResponse()

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
        pb_return_value = video_stitcher_service.ListSlatesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_slates(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/slates" % client.transport._host,
            args[1],
        )


def test_list_slates_rest_flattened_error(transport: str = "rest"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_slates(
            video_stitcher_service.ListSlatesRequest(),
            parent="parent_value",
        )


def test_list_slates_rest_pager(transport: str = "rest"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            video_stitcher_service.ListSlatesResponse(
                slates=[
                    slates.Slate(),
                    slates.Slate(),
                    slates.Slate(),
                ],
                next_page_token="abc",
            ),
            video_stitcher_service.ListSlatesResponse(
                slates=[],
                next_page_token="def",
            ),
            video_stitcher_service.ListSlatesResponse(
                slates=[
                    slates.Slate(),
                ],
                next_page_token="ghi",
            ),
            video_stitcher_service.ListSlatesResponse(
                slates=[
                    slates.Slate(),
                    slates.Slate(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            video_stitcher_service.ListSlatesResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_slates(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, slates.Slate) for i in results)

        pages = list(client.list_slates(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.GetSlateRequest,
        dict,
    ],
)
def test_get_slate_rest(request_type):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/slates/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = slates.Slate(
            name="name_value",
            uri="uri_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = slates.Slate.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_slate(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, slates.Slate)
    assert response.name == "name_value"
    assert response.uri == "uri_value"


def test_get_slate_rest_required_fields(
    request_type=video_stitcher_service.GetSlateRequest,
):
    transport_class = transports.VideoStitcherServiceRestTransport

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
    ).get_slate._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_slate._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = slates.Slate()
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

            pb_return_value = slates.Slate.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_slate(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_slate_rest_unset_required_fields():
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_slate._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_slate_rest_interceptors(null_interceptor):
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.VideoStitcherServiceRestInterceptor(),
    )
    client = VideoStitcherServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.VideoStitcherServiceRestInterceptor, "post_get_slate"
    ) as post, mock.patch.object(
        transports.VideoStitcherServiceRestInterceptor, "pre_get_slate"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = video_stitcher_service.GetSlateRequest.pb(
            video_stitcher_service.GetSlateRequest()
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
        req.return_value._content = slates.Slate.to_json(slates.Slate())

        request = video_stitcher_service.GetSlateRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = slates.Slate()

        client.get_slate(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_slate_rest_bad_request(
    transport: str = "rest", request_type=video_stitcher_service.GetSlateRequest
):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/slates/sample3"}
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
        client.get_slate(request)


def test_get_slate_rest_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = slates.Slate()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/locations/sample2/slates/sample3"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = slates.Slate.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_slate(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/slates/*}" % client.transport._host,
            args[1],
        )


def test_get_slate_rest_flattened_error(transport: str = "rest"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_slate(
            video_stitcher_service.GetSlateRequest(),
            name="name_value",
        )


def test_get_slate_rest_error():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.UpdateSlateRequest,
        dict,
    ],
)
def test_update_slate_rest(request_type):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "slate": {"name": "projects/sample1/locations/sample2/slates/sample3"}
    }
    request_init["slate"] = {
        "name": "projects/sample1/locations/sample2/slates/sample3",
        "uri": "uri_value",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = slates.Slate(
            name="name_value",
            uri="uri_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = slates.Slate.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_slate(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, slates.Slate)
    assert response.name == "name_value"
    assert response.uri == "uri_value"


def test_update_slate_rest_required_fields(
    request_type=video_stitcher_service.UpdateSlateRequest,
):
    transport_class = transports.VideoStitcherServiceRestTransport

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
    ).update_slate._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_slate._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = slates.Slate()
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

            pb_return_value = slates.Slate.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_slate(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_slate_rest_unset_required_fields():
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_slate._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("updateMask",))
        & set(
            (
                "slate",
                "updateMask",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_slate_rest_interceptors(null_interceptor):
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.VideoStitcherServiceRestInterceptor(),
    )
    client = VideoStitcherServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.VideoStitcherServiceRestInterceptor, "post_update_slate"
    ) as post, mock.patch.object(
        transports.VideoStitcherServiceRestInterceptor, "pre_update_slate"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = video_stitcher_service.UpdateSlateRequest.pb(
            video_stitcher_service.UpdateSlateRequest()
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
        req.return_value._content = slates.Slate.to_json(slates.Slate())

        request = video_stitcher_service.UpdateSlateRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = slates.Slate()

        client.update_slate(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_slate_rest_bad_request(
    transport: str = "rest", request_type=video_stitcher_service.UpdateSlateRequest
):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "slate": {"name": "projects/sample1/locations/sample2/slates/sample3"}
    }
    request_init["slate"] = {
        "name": "projects/sample1/locations/sample2/slates/sample3",
        "uri": "uri_value",
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
        client.update_slate(request)


def test_update_slate_rest_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = slates.Slate()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "slate": {"name": "projects/sample1/locations/sample2/slates/sample3"}
        }

        # get truthy value for each flattened field
        mock_args = dict(
            slate=slates.Slate(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = slates.Slate.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_slate(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{slate.name=projects/*/locations/*/slates/*}"
            % client.transport._host,
            args[1],
        )


def test_update_slate_rest_flattened_error(transport: str = "rest"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_slate(
            video_stitcher_service.UpdateSlateRequest(),
            slate=slates.Slate(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_slate_rest_error():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.DeleteSlateRequest,
        dict,
    ],
)
def test_delete_slate_rest(request_type):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/slates/sample3"}
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
        response = client.delete_slate(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_slate_rest_required_fields(
    request_type=video_stitcher_service.DeleteSlateRequest,
):
    transport_class = transports.VideoStitcherServiceRestTransport

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
    ).delete_slate._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_slate._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = VideoStitcherServiceClient(
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

            response = client.delete_slate(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_slate_rest_unset_required_fields():
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_slate._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_slate_rest_interceptors(null_interceptor):
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.VideoStitcherServiceRestInterceptor(),
    )
    client = VideoStitcherServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.VideoStitcherServiceRestInterceptor, "pre_delete_slate"
    ) as pre:
        pre.assert_not_called()
        pb_message = video_stitcher_service.DeleteSlateRequest.pb(
            video_stitcher_service.DeleteSlateRequest()
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

        request = video_stitcher_service.DeleteSlateRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_slate(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_delete_slate_rest_bad_request(
    transport: str = "rest", request_type=video_stitcher_service.DeleteSlateRequest
):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/slates/sample3"}
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
        client.delete_slate(request)


def test_delete_slate_rest_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/locations/sample2/slates/sample3"}

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

        client.delete_slate(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/slates/*}" % client.transport._host,
            args[1],
        )


def test_delete_slate_rest_flattened_error(transport: str = "rest"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_slate(
            video_stitcher_service.DeleteSlateRequest(),
            name="name_value",
        )


def test_delete_slate_rest_error():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.CreateLiveSessionRequest,
        dict,
    ],
)
def test_create_live_session_rest(request_type):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["live_session"] = {
        "name": "name_value",
        "play_uri": "play_uri_value",
        "source_uri": "source_uri_value",
        "default_ad_tag_id": "default_ad_tag_id_value",
        "ad_tag_map": {},
        "ad_tag_macros": {},
        "client_ad_tracking": True,
        "default_slate_id": "default_slate_id_value",
        "stitching_policy": 1,
        "manifest_options": {
            "include_renditions": [{"bitrate_bps": 1167, "codecs": "codecs_value"}],
            "bitrate_order": 1,
        },
        "stream_id": "stream_id_value",
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = sessions.LiveSession(
            name="name_value",
            play_uri="play_uri_value",
            source_uri="source_uri_value",
            default_ad_tag_id="default_ad_tag_id_value",
            client_ad_tracking=True,
            default_slate_id="default_slate_id_value",
            stitching_policy=sessions.LiveSession.StitchingPolicy.COMPLETE_AD,
            stream_id="stream_id_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = sessions.LiveSession.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_live_session(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, sessions.LiveSession)
    assert response.name == "name_value"
    assert response.play_uri == "play_uri_value"
    assert response.source_uri == "source_uri_value"
    assert response.default_ad_tag_id == "default_ad_tag_id_value"
    assert response.client_ad_tracking is True
    assert response.default_slate_id == "default_slate_id_value"
    assert response.stitching_policy == sessions.LiveSession.StitchingPolicy.COMPLETE_AD
    assert response.stream_id == "stream_id_value"


def test_create_live_session_rest_required_fields(
    request_type=video_stitcher_service.CreateLiveSessionRequest,
):
    transport_class = transports.VideoStitcherServiceRestTransport

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
    ).create_live_session._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_live_session._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = sessions.LiveSession()
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

            pb_return_value = sessions.LiveSession.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_live_session(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_live_session_rest_unset_required_fields():
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_live_session._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "liveSession",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_live_session_rest_interceptors(null_interceptor):
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.VideoStitcherServiceRestInterceptor(),
    )
    client = VideoStitcherServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.VideoStitcherServiceRestInterceptor, "post_create_live_session"
    ) as post, mock.patch.object(
        transports.VideoStitcherServiceRestInterceptor, "pre_create_live_session"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = video_stitcher_service.CreateLiveSessionRequest.pb(
            video_stitcher_service.CreateLiveSessionRequest()
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
        req.return_value._content = sessions.LiveSession.to_json(sessions.LiveSession())

        request = video_stitcher_service.CreateLiveSessionRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = sessions.LiveSession()

        client.create_live_session(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_live_session_rest_bad_request(
    transport: str = "rest",
    request_type=video_stitcher_service.CreateLiveSessionRequest,
):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["live_session"] = {
        "name": "name_value",
        "play_uri": "play_uri_value",
        "source_uri": "source_uri_value",
        "default_ad_tag_id": "default_ad_tag_id_value",
        "ad_tag_map": {},
        "ad_tag_macros": {},
        "client_ad_tracking": True,
        "default_slate_id": "default_slate_id_value",
        "stitching_policy": 1,
        "manifest_options": {
            "include_renditions": [{"bitrate_bps": 1167, "codecs": "codecs_value"}],
            "bitrate_order": 1,
        },
        "stream_id": "stream_id_value",
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
        client.create_live_session(request)


def test_create_live_session_rest_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = sessions.LiveSession()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            live_session=sessions.LiveSession(name="name_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = sessions.LiveSession.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_live_session(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/liveSessions"
            % client.transport._host,
            args[1],
        )


def test_create_live_session_rest_flattened_error(transport: str = "rest"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_live_session(
            video_stitcher_service.CreateLiveSessionRequest(),
            parent="parent_value",
            live_session=sessions.LiveSession(name="name_value"),
        )


def test_create_live_session_rest_error():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        video_stitcher_service.GetLiveSessionRequest,
        dict,
    ],
)
def test_get_live_session_rest(request_type):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/liveSessions/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = sessions.LiveSession(
            name="name_value",
            play_uri="play_uri_value",
            source_uri="source_uri_value",
            default_ad_tag_id="default_ad_tag_id_value",
            client_ad_tracking=True,
            default_slate_id="default_slate_id_value",
            stitching_policy=sessions.LiveSession.StitchingPolicy.COMPLETE_AD,
            stream_id="stream_id_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = sessions.LiveSession.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_live_session(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, sessions.LiveSession)
    assert response.name == "name_value"
    assert response.play_uri == "play_uri_value"
    assert response.source_uri == "source_uri_value"
    assert response.default_ad_tag_id == "default_ad_tag_id_value"
    assert response.client_ad_tracking is True
    assert response.default_slate_id == "default_slate_id_value"
    assert response.stitching_policy == sessions.LiveSession.StitchingPolicy.COMPLETE_AD
    assert response.stream_id == "stream_id_value"


def test_get_live_session_rest_required_fields(
    request_type=video_stitcher_service.GetLiveSessionRequest,
):
    transport_class = transports.VideoStitcherServiceRestTransport

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
    ).get_live_session._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_live_session._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = sessions.LiveSession()
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

            pb_return_value = sessions.LiveSession.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_live_session(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_live_session_rest_unset_required_fields():
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_live_session._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_live_session_rest_interceptors(null_interceptor):
    transport = transports.VideoStitcherServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.VideoStitcherServiceRestInterceptor(),
    )
    client = VideoStitcherServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.VideoStitcherServiceRestInterceptor, "post_get_live_session"
    ) as post, mock.patch.object(
        transports.VideoStitcherServiceRestInterceptor, "pre_get_live_session"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = video_stitcher_service.GetLiveSessionRequest.pb(
            video_stitcher_service.GetLiveSessionRequest()
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
        req.return_value._content = sessions.LiveSession.to_json(sessions.LiveSession())

        request = video_stitcher_service.GetLiveSessionRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = sessions.LiveSession()

        client.get_live_session(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_live_session_rest_bad_request(
    transport: str = "rest", request_type=video_stitcher_service.GetLiveSessionRequest
):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/liveSessions/sample3"}
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
        client.get_live_session(request)


def test_get_live_session_rest_flattened():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = sessions.LiveSession()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/liveSessions/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = sessions.LiveSession.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_live_session(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/liveSessions/*}"
            % client.transport._host,
            args[1],
        )


def test_get_live_session_rest_flattened_error(transport: str = "rest"):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_live_session(
            video_stitcher_service.GetLiveSessionRequest(),
            name="name_value",
        )


def test_get_live_session_rest_error():
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.VideoStitcherServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = VideoStitcherServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.VideoStitcherServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = VideoStitcherServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.VideoStitcherServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = VideoStitcherServiceClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = VideoStitcherServiceClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.VideoStitcherServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = VideoStitcherServiceClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.VideoStitcherServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = VideoStitcherServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.VideoStitcherServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.VideoStitcherServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.VideoStitcherServiceGrpcTransport,
        transports.VideoStitcherServiceGrpcAsyncIOTransport,
        transports.VideoStitcherServiceRestTransport,
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
    transport = VideoStitcherServiceClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.VideoStitcherServiceGrpcTransport,
    )


def test_video_stitcher_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.VideoStitcherServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_video_stitcher_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.video.stitcher_v1.services.video_stitcher_service.transports.VideoStitcherServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.VideoStitcherServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_cdn_key",
        "list_cdn_keys",
        "get_cdn_key",
        "delete_cdn_key",
        "update_cdn_key",
        "create_vod_session",
        "get_vod_session",
        "list_vod_stitch_details",
        "get_vod_stitch_detail",
        "list_vod_ad_tag_details",
        "get_vod_ad_tag_detail",
        "list_live_ad_tag_details",
        "get_live_ad_tag_detail",
        "create_slate",
        "list_slates",
        "get_slate",
        "update_slate",
        "delete_slate",
        "create_live_session",
        "get_live_session",
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


def test_video_stitcher_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.video.stitcher_v1.services.video_stitcher_service.transports.VideoStitcherServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.VideoStitcherServiceTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_video_stitcher_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.video.stitcher_v1.services.video_stitcher_service.transports.VideoStitcherServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.VideoStitcherServiceTransport()
        adc.assert_called_once()


def test_video_stitcher_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        VideoStitcherServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.VideoStitcherServiceGrpcTransport,
        transports.VideoStitcherServiceGrpcAsyncIOTransport,
    ],
)
def test_video_stitcher_service_transport_auth_adc(transport_class):
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
        transports.VideoStitcherServiceGrpcTransport,
        transports.VideoStitcherServiceGrpcAsyncIOTransport,
        transports.VideoStitcherServiceRestTransport,
    ],
)
def test_video_stitcher_service_transport_auth_gdch_credentials(transport_class):
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
        (transports.VideoStitcherServiceGrpcTransport, grpc_helpers),
        (transports.VideoStitcherServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_video_stitcher_service_transport_create_channel(transport_class, grpc_helpers):
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
            "videostitcher.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="videostitcher.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.VideoStitcherServiceGrpcTransport,
        transports.VideoStitcherServiceGrpcAsyncIOTransport,
    ],
)
def test_video_stitcher_service_grpc_transport_client_cert_source_for_mtls(
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


def test_video_stitcher_service_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.VideoStitcherServiceRestTransport(
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
def test_video_stitcher_service_host_no_port(transport_name):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="videostitcher.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "videostitcher.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://videostitcher.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_video_stitcher_service_host_with_port(transport_name):
    client = VideoStitcherServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="videostitcher.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "videostitcher.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://videostitcher.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_video_stitcher_service_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = VideoStitcherServiceClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = VideoStitcherServiceClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.create_cdn_key._session
    session2 = client2.transport.create_cdn_key._session
    assert session1 != session2
    session1 = client1.transport.list_cdn_keys._session
    session2 = client2.transport.list_cdn_keys._session
    assert session1 != session2
    session1 = client1.transport.get_cdn_key._session
    session2 = client2.transport.get_cdn_key._session
    assert session1 != session2
    session1 = client1.transport.delete_cdn_key._session
    session2 = client2.transport.delete_cdn_key._session
    assert session1 != session2
    session1 = client1.transport.update_cdn_key._session
    session2 = client2.transport.update_cdn_key._session
    assert session1 != session2
    session1 = client1.transport.create_vod_session._session
    session2 = client2.transport.create_vod_session._session
    assert session1 != session2
    session1 = client1.transport.get_vod_session._session
    session2 = client2.transport.get_vod_session._session
    assert session1 != session2
    session1 = client1.transport.list_vod_stitch_details._session
    session2 = client2.transport.list_vod_stitch_details._session
    assert session1 != session2
    session1 = client1.transport.get_vod_stitch_detail._session
    session2 = client2.transport.get_vod_stitch_detail._session
    assert session1 != session2
    session1 = client1.transport.list_vod_ad_tag_details._session
    session2 = client2.transport.list_vod_ad_tag_details._session
    assert session1 != session2
    session1 = client1.transport.get_vod_ad_tag_detail._session
    session2 = client2.transport.get_vod_ad_tag_detail._session
    assert session1 != session2
    session1 = client1.transport.list_live_ad_tag_details._session
    session2 = client2.transport.list_live_ad_tag_details._session
    assert session1 != session2
    session1 = client1.transport.get_live_ad_tag_detail._session
    session2 = client2.transport.get_live_ad_tag_detail._session
    assert session1 != session2
    session1 = client1.transport.create_slate._session
    session2 = client2.transport.create_slate._session
    assert session1 != session2
    session1 = client1.transport.list_slates._session
    session2 = client2.transport.list_slates._session
    assert session1 != session2
    session1 = client1.transport.get_slate._session
    session2 = client2.transport.get_slate._session
    assert session1 != session2
    session1 = client1.transport.update_slate._session
    session2 = client2.transport.update_slate._session
    assert session1 != session2
    session1 = client1.transport.delete_slate._session
    session2 = client2.transport.delete_slate._session
    assert session1 != session2
    session1 = client1.transport.create_live_session._session
    session2 = client2.transport.create_live_session._session
    assert session1 != session2
    session1 = client1.transport.get_live_session._session
    session2 = client2.transport.get_live_session._session
    assert session1 != session2


def test_video_stitcher_service_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.VideoStitcherServiceGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_video_stitcher_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.VideoStitcherServiceGrpcAsyncIOTransport(
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
        transports.VideoStitcherServiceGrpcTransport,
        transports.VideoStitcherServiceGrpcAsyncIOTransport,
    ],
)
def test_video_stitcher_service_transport_channel_mtls_with_client_cert_source(
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
        transports.VideoStitcherServiceGrpcTransport,
        transports.VideoStitcherServiceGrpcAsyncIOTransport,
    ],
)
def test_video_stitcher_service_transport_channel_mtls_with_adc(transport_class):
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


def test_cdn_key_path():
    project = "squid"
    location = "clam"
    cdn_key = "whelk"
    expected = "projects/{project}/locations/{location}/cdnKeys/{cdn_key}".format(
        project=project,
        location=location,
        cdn_key=cdn_key,
    )
    actual = VideoStitcherServiceClient.cdn_key_path(project, location, cdn_key)
    assert expected == actual


def test_parse_cdn_key_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "cdn_key": "nudibranch",
    }
    path = VideoStitcherServiceClient.cdn_key_path(**expected)

    # Check that the path construction is reversible.
    actual = VideoStitcherServiceClient.parse_cdn_key_path(path)
    assert expected == actual


def test_live_ad_tag_detail_path():
    project = "cuttlefish"
    location = "mussel"
    live_session = "winkle"
    live_ad_tag_detail = "nautilus"
    expected = "projects/{project}/locations/{location}/liveSessions/{live_session}/liveAdTagDetails/{live_ad_tag_detail}".format(
        project=project,
        location=location,
        live_session=live_session,
        live_ad_tag_detail=live_ad_tag_detail,
    )
    actual = VideoStitcherServiceClient.live_ad_tag_detail_path(
        project, location, live_session, live_ad_tag_detail
    )
    assert expected == actual


def test_parse_live_ad_tag_detail_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
        "live_session": "squid",
        "live_ad_tag_detail": "clam",
    }
    path = VideoStitcherServiceClient.live_ad_tag_detail_path(**expected)

    # Check that the path construction is reversible.
    actual = VideoStitcherServiceClient.parse_live_ad_tag_detail_path(path)
    assert expected == actual


def test_live_session_path():
    project = "whelk"
    location = "octopus"
    live_session = "oyster"
    expected = (
        "projects/{project}/locations/{location}/liveSessions/{live_session}".format(
            project=project,
            location=location,
            live_session=live_session,
        )
    )
    actual = VideoStitcherServiceClient.live_session_path(
        project, location, live_session
    )
    assert expected == actual


def test_parse_live_session_path():
    expected = {
        "project": "nudibranch",
        "location": "cuttlefish",
        "live_session": "mussel",
    }
    path = VideoStitcherServiceClient.live_session_path(**expected)

    # Check that the path construction is reversible.
    actual = VideoStitcherServiceClient.parse_live_session_path(path)
    assert expected == actual


def test_slate_path():
    project = "winkle"
    location = "nautilus"
    slate = "scallop"
    expected = "projects/{project}/locations/{location}/slates/{slate}".format(
        project=project,
        location=location,
        slate=slate,
    )
    actual = VideoStitcherServiceClient.slate_path(project, location, slate)
    assert expected == actual


def test_parse_slate_path():
    expected = {
        "project": "abalone",
        "location": "squid",
        "slate": "clam",
    }
    path = VideoStitcherServiceClient.slate_path(**expected)

    # Check that the path construction is reversible.
    actual = VideoStitcherServiceClient.parse_slate_path(path)
    assert expected == actual


def test_vod_ad_tag_detail_path():
    project = "whelk"
    location = "octopus"
    vod_session = "oyster"
    vod_ad_tag_detail = "nudibranch"
    expected = "projects/{project}/locations/{location}/vodSessions/{vod_session}/vodAdTagDetails/{vod_ad_tag_detail}".format(
        project=project,
        location=location,
        vod_session=vod_session,
        vod_ad_tag_detail=vod_ad_tag_detail,
    )
    actual = VideoStitcherServiceClient.vod_ad_tag_detail_path(
        project, location, vod_session, vod_ad_tag_detail
    )
    assert expected == actual


def test_parse_vod_ad_tag_detail_path():
    expected = {
        "project": "cuttlefish",
        "location": "mussel",
        "vod_session": "winkle",
        "vod_ad_tag_detail": "nautilus",
    }
    path = VideoStitcherServiceClient.vod_ad_tag_detail_path(**expected)

    # Check that the path construction is reversible.
    actual = VideoStitcherServiceClient.parse_vod_ad_tag_detail_path(path)
    assert expected == actual


def test_vod_session_path():
    project = "scallop"
    location = "abalone"
    vod_session = "squid"
    expected = (
        "projects/{project}/locations/{location}/vodSessions/{vod_session}".format(
            project=project,
            location=location,
            vod_session=vod_session,
        )
    )
    actual = VideoStitcherServiceClient.vod_session_path(project, location, vod_session)
    assert expected == actual


def test_parse_vod_session_path():
    expected = {
        "project": "clam",
        "location": "whelk",
        "vod_session": "octopus",
    }
    path = VideoStitcherServiceClient.vod_session_path(**expected)

    # Check that the path construction is reversible.
    actual = VideoStitcherServiceClient.parse_vod_session_path(path)
    assert expected == actual


def test_vod_stitch_detail_path():
    project = "oyster"
    location = "nudibranch"
    vod_session = "cuttlefish"
    vod_stitch_detail = "mussel"
    expected = "projects/{project}/locations/{location}/vodSessions/{vod_session}/vodStitchDetails/{vod_stitch_detail}".format(
        project=project,
        location=location,
        vod_session=vod_session,
        vod_stitch_detail=vod_stitch_detail,
    )
    actual = VideoStitcherServiceClient.vod_stitch_detail_path(
        project, location, vod_session, vod_stitch_detail
    )
    assert expected == actual


def test_parse_vod_stitch_detail_path():
    expected = {
        "project": "winkle",
        "location": "nautilus",
        "vod_session": "scallop",
        "vod_stitch_detail": "abalone",
    }
    path = VideoStitcherServiceClient.vod_stitch_detail_path(**expected)

    # Check that the path construction is reversible.
    actual = VideoStitcherServiceClient.parse_vod_stitch_detail_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "squid"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = VideoStitcherServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "clam",
    }
    path = VideoStitcherServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = VideoStitcherServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "whelk"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = VideoStitcherServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "octopus",
    }
    path = VideoStitcherServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = VideoStitcherServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "oyster"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = VideoStitcherServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nudibranch",
    }
    path = VideoStitcherServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = VideoStitcherServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "cuttlefish"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = VideoStitcherServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "mussel",
    }
    path = VideoStitcherServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = VideoStitcherServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "winkle"
    location = "nautilus"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = VideoStitcherServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
    }
    path = VideoStitcherServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = VideoStitcherServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.VideoStitcherServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = VideoStitcherServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.VideoStitcherServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = VideoStitcherServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = VideoStitcherServiceAsyncClient(
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
        client = VideoStitcherServiceClient(
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
        client = VideoStitcherServiceClient(
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
        (VideoStitcherServiceClient, transports.VideoStitcherServiceGrpcTransport),
        (
            VideoStitcherServiceAsyncClient,
            transports.VideoStitcherServiceGrpcAsyncIOTransport,
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
