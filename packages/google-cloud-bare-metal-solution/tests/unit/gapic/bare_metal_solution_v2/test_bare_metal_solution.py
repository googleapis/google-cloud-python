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
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import options_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2
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

from google.cloud.bare_metal_solution_v2.services.bare_metal_solution import (
    BareMetalSolutionAsyncClient,
    BareMetalSolutionClient,
    pagers,
    transports,
)
from google.cloud.bare_metal_solution_v2.types import nfs_share as gcb_nfs_share
from google.cloud.bare_metal_solution_v2.types import baremetalsolution
from google.cloud.bare_metal_solution_v2.types import instance
from google.cloud.bare_metal_solution_v2.types import instance as gcb_instance
from google.cloud.bare_metal_solution_v2.types import lun
from google.cloud.bare_metal_solution_v2.types import network
from google.cloud.bare_metal_solution_v2.types import network as gcb_network
from google.cloud.bare_metal_solution_v2.types import nfs_share
from google.cloud.bare_metal_solution_v2.types import volume
from google.cloud.bare_metal_solution_v2.types import volume as gcb_volume


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

    assert BareMetalSolutionClient._get_default_mtls_endpoint(None) is None
    assert (
        BareMetalSolutionClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        BareMetalSolutionClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        BareMetalSolutionClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        BareMetalSolutionClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        BareMetalSolutionClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (BareMetalSolutionClient, "grpc"),
        (BareMetalSolutionAsyncClient, "grpc_asyncio"),
        (BareMetalSolutionClient, "rest"),
    ],
)
def test_bare_metal_solution_client_from_service_account_info(
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
            "baremetalsolution.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://baremetalsolution.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.BareMetalSolutionGrpcTransport, "grpc"),
        (transports.BareMetalSolutionGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.BareMetalSolutionRestTransport, "rest"),
    ],
)
def test_bare_metal_solution_client_service_account_always_use_jwt(
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
        (BareMetalSolutionClient, "grpc"),
        (BareMetalSolutionAsyncClient, "grpc_asyncio"),
        (BareMetalSolutionClient, "rest"),
    ],
)
def test_bare_metal_solution_client_from_service_account_file(
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
            "baremetalsolution.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://baremetalsolution.googleapis.com"
        )


def test_bare_metal_solution_client_get_transport_class():
    transport = BareMetalSolutionClient.get_transport_class()
    available_transports = [
        transports.BareMetalSolutionGrpcTransport,
        transports.BareMetalSolutionRestTransport,
    ]
    assert transport in available_transports

    transport = BareMetalSolutionClient.get_transport_class("grpc")
    assert transport == transports.BareMetalSolutionGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (BareMetalSolutionClient, transports.BareMetalSolutionGrpcTransport, "grpc"),
        (
            BareMetalSolutionAsyncClient,
            transports.BareMetalSolutionGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (BareMetalSolutionClient, transports.BareMetalSolutionRestTransport, "rest"),
    ],
)
@mock.patch.object(
    BareMetalSolutionClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(BareMetalSolutionClient),
)
@mock.patch.object(
    BareMetalSolutionAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(BareMetalSolutionAsyncClient),
)
def test_bare_metal_solution_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(BareMetalSolutionClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(BareMetalSolutionClient, "get_transport_class") as gtc:
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
            BareMetalSolutionClient,
            transports.BareMetalSolutionGrpcTransport,
            "grpc",
            "true",
        ),
        (
            BareMetalSolutionAsyncClient,
            transports.BareMetalSolutionGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            BareMetalSolutionClient,
            transports.BareMetalSolutionGrpcTransport,
            "grpc",
            "false",
        ),
        (
            BareMetalSolutionAsyncClient,
            transports.BareMetalSolutionGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (
            BareMetalSolutionClient,
            transports.BareMetalSolutionRestTransport,
            "rest",
            "true",
        ),
        (
            BareMetalSolutionClient,
            transports.BareMetalSolutionRestTransport,
            "rest",
            "false",
        ),
    ],
)
@mock.patch.object(
    BareMetalSolutionClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(BareMetalSolutionClient),
)
@mock.patch.object(
    BareMetalSolutionAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(BareMetalSolutionAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_bare_metal_solution_client_mtls_env_auto(
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
    "client_class", [BareMetalSolutionClient, BareMetalSolutionAsyncClient]
)
@mock.patch.object(
    BareMetalSolutionClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(BareMetalSolutionClient),
)
@mock.patch.object(
    BareMetalSolutionAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(BareMetalSolutionAsyncClient),
)
def test_bare_metal_solution_client_get_mtls_endpoint_and_cert_source(client_class):
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
        (BareMetalSolutionClient, transports.BareMetalSolutionGrpcTransport, "grpc"),
        (
            BareMetalSolutionAsyncClient,
            transports.BareMetalSolutionGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (BareMetalSolutionClient, transports.BareMetalSolutionRestTransport, "rest"),
    ],
)
def test_bare_metal_solution_client_client_options_scopes(
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
            BareMetalSolutionClient,
            transports.BareMetalSolutionGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            BareMetalSolutionAsyncClient,
            transports.BareMetalSolutionGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (
            BareMetalSolutionClient,
            transports.BareMetalSolutionRestTransport,
            "rest",
            None,
        ),
    ],
)
def test_bare_metal_solution_client_client_options_credentials_file(
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


def test_bare_metal_solution_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.bare_metal_solution_v2.services.bare_metal_solution.transports.BareMetalSolutionGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = BareMetalSolutionClient(
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
            BareMetalSolutionClient,
            transports.BareMetalSolutionGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            BareMetalSolutionAsyncClient,
            transports.BareMetalSolutionGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_bare_metal_solution_client_create_channel_credentials_file(
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
            "baremetalsolution.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="baremetalsolution.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        instance.ListInstancesRequest,
        dict,
    ],
)
def test_list_instances(request_type, transport: str = "grpc"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_instances), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = instance.ListInstancesResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_instances(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == instance.ListInstancesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListInstancesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_instances_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_instances), "__call__") as call:
        client.list_instances()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == instance.ListInstancesRequest()


@pytest.mark.asyncio
async def test_list_instances_async(
    transport: str = "grpc_asyncio", request_type=instance.ListInstancesRequest
):
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_instances), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            instance.ListInstancesResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_instances(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == instance.ListInstancesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListInstancesAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_instances_async_from_dict():
    await test_list_instances_async(request_type=dict)


def test_list_instances_field_headers():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = instance.ListInstancesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_instances), "__call__") as call:
        call.return_value = instance.ListInstancesResponse()
        client.list_instances(request)

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
async def test_list_instances_field_headers_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = instance.ListInstancesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_instances), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            instance.ListInstancesResponse()
        )
        await client.list_instances(request)

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


def test_list_instances_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_instances), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = instance.ListInstancesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_instances(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_instances_flattened_error():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_instances(
            instance.ListInstancesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_instances_flattened_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_instances), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = instance.ListInstancesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            instance.ListInstancesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_instances(
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
async def test_list_instances_flattened_error_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_instances(
            instance.ListInstancesRequest(),
            parent="parent_value",
        )


def test_list_instances_pager(transport_name: str = "grpc"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_instances), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            instance.ListInstancesResponse(
                instances=[
                    instance.Instance(),
                    instance.Instance(),
                    instance.Instance(),
                ],
                next_page_token="abc",
            ),
            instance.ListInstancesResponse(
                instances=[],
                next_page_token="def",
            ),
            instance.ListInstancesResponse(
                instances=[
                    instance.Instance(),
                ],
                next_page_token="ghi",
            ),
            instance.ListInstancesResponse(
                instances=[
                    instance.Instance(),
                    instance.Instance(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_instances(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, instance.Instance) for i in results)


def test_list_instances_pages(transport_name: str = "grpc"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_instances), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            instance.ListInstancesResponse(
                instances=[
                    instance.Instance(),
                    instance.Instance(),
                    instance.Instance(),
                ],
                next_page_token="abc",
            ),
            instance.ListInstancesResponse(
                instances=[],
                next_page_token="def",
            ),
            instance.ListInstancesResponse(
                instances=[
                    instance.Instance(),
                ],
                next_page_token="ghi",
            ),
            instance.ListInstancesResponse(
                instances=[
                    instance.Instance(),
                    instance.Instance(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_instances(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_instances_async_pager():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_instances), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            instance.ListInstancesResponse(
                instances=[
                    instance.Instance(),
                    instance.Instance(),
                    instance.Instance(),
                ],
                next_page_token="abc",
            ),
            instance.ListInstancesResponse(
                instances=[],
                next_page_token="def",
            ),
            instance.ListInstancesResponse(
                instances=[
                    instance.Instance(),
                ],
                next_page_token="ghi",
            ),
            instance.ListInstancesResponse(
                instances=[
                    instance.Instance(),
                    instance.Instance(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_instances(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, instance.Instance) for i in responses)


@pytest.mark.asyncio
async def test_list_instances_async_pages():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_instances), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            instance.ListInstancesResponse(
                instances=[
                    instance.Instance(),
                    instance.Instance(),
                    instance.Instance(),
                ],
                next_page_token="abc",
            ),
            instance.ListInstancesResponse(
                instances=[],
                next_page_token="def",
            ),
            instance.ListInstancesResponse(
                instances=[
                    instance.Instance(),
                ],
                next_page_token="ghi",
            ),
            instance.ListInstancesResponse(
                instances=[
                    instance.Instance(),
                    instance.Instance(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_instances(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        instance.GetInstanceRequest,
        dict,
    ],
)
def test_get_instance(request_type, transport: str = "grpc"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_instance), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = instance.Instance(
            name="name_value",
            id="id_value",
            machine_type="machine_type_value",
            state=instance.Instance.State.PROVISIONING,
            hyperthreading_enabled=True,
            interactive_serial_console_enabled=True,
            os_image="os_image_value",
            pod="pod_value",
            network_template="network_template_value",
        )
        response = client.get_instance(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == instance.GetInstanceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, instance.Instance)
    assert response.name == "name_value"
    assert response.id == "id_value"
    assert response.machine_type == "machine_type_value"
    assert response.state == instance.Instance.State.PROVISIONING
    assert response.hyperthreading_enabled is True
    assert response.interactive_serial_console_enabled is True
    assert response.os_image == "os_image_value"
    assert response.pod == "pod_value"
    assert response.network_template == "network_template_value"


def test_get_instance_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_instance), "__call__") as call:
        client.get_instance()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == instance.GetInstanceRequest()


@pytest.mark.asyncio
async def test_get_instance_async(
    transport: str = "grpc_asyncio", request_type=instance.GetInstanceRequest
):
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_instance), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            instance.Instance(
                name="name_value",
                id="id_value",
                machine_type="machine_type_value",
                state=instance.Instance.State.PROVISIONING,
                hyperthreading_enabled=True,
                interactive_serial_console_enabled=True,
                os_image="os_image_value",
                pod="pod_value",
                network_template="network_template_value",
            )
        )
        response = await client.get_instance(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == instance.GetInstanceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, instance.Instance)
    assert response.name == "name_value"
    assert response.id == "id_value"
    assert response.machine_type == "machine_type_value"
    assert response.state == instance.Instance.State.PROVISIONING
    assert response.hyperthreading_enabled is True
    assert response.interactive_serial_console_enabled is True
    assert response.os_image == "os_image_value"
    assert response.pod == "pod_value"
    assert response.network_template == "network_template_value"


@pytest.mark.asyncio
async def test_get_instance_async_from_dict():
    await test_get_instance_async(request_type=dict)


def test_get_instance_field_headers():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = instance.GetInstanceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_instance), "__call__") as call:
        call.return_value = instance.Instance()
        client.get_instance(request)

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
async def test_get_instance_field_headers_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = instance.GetInstanceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_instance), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(instance.Instance())
        await client.get_instance(request)

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


def test_get_instance_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_instance), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = instance.Instance()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_instance(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_instance_flattened_error():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_instance(
            instance.GetInstanceRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_instance_flattened_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_instance), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = instance.Instance()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(instance.Instance())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_instance(
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
async def test_get_instance_flattened_error_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_instance(
            instance.GetInstanceRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gcb_instance.UpdateInstanceRequest,
        dict,
    ],
)
def test_update_instance(request_type, transport: str = "grpc"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_instance), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_instance(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcb_instance.UpdateInstanceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_instance_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_instance), "__call__") as call:
        client.update_instance()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcb_instance.UpdateInstanceRequest()


@pytest.mark.asyncio
async def test_update_instance_async(
    transport: str = "grpc_asyncio", request_type=gcb_instance.UpdateInstanceRequest
):
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_instance), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_instance(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcb_instance.UpdateInstanceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_instance_async_from_dict():
    await test_update_instance_async(request_type=dict)


def test_update_instance_field_headers():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcb_instance.UpdateInstanceRequest()

    request.instance.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_instance), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_instance(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "instance.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_instance_field_headers_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcb_instance.UpdateInstanceRequest()

    request.instance.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_instance), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_instance(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "instance.name=name_value",
    ) in kw["metadata"]


def test_update_instance_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_instance), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_instance(
            instance=gcb_instance.Instance(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].instance
        mock_val = gcb_instance.Instance(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_instance_flattened_error():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_instance(
            gcb_instance.UpdateInstanceRequest(),
            instance=gcb_instance.Instance(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_instance_flattened_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_instance), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_instance(
            instance=gcb_instance.Instance(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].instance
        mock_val = gcb_instance.Instance(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_instance_flattened_error_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_instance(
            gcb_instance.UpdateInstanceRequest(),
            instance=gcb_instance.Instance(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        instance.ResetInstanceRequest,
        dict,
    ],
)
def test_reset_instance(request_type, transport: str = "grpc"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.reset_instance), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.reset_instance(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == instance.ResetInstanceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_reset_instance_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.reset_instance), "__call__") as call:
        client.reset_instance()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == instance.ResetInstanceRequest()


@pytest.mark.asyncio
async def test_reset_instance_async(
    transport: str = "grpc_asyncio", request_type=instance.ResetInstanceRequest
):
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.reset_instance), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.reset_instance(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == instance.ResetInstanceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_reset_instance_async_from_dict():
    await test_reset_instance_async(request_type=dict)


def test_reset_instance_field_headers():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = instance.ResetInstanceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.reset_instance), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.reset_instance(request)

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
async def test_reset_instance_field_headers_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = instance.ResetInstanceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.reset_instance), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.reset_instance(request)

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


def test_reset_instance_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.reset_instance), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.reset_instance(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_reset_instance_flattened_error():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.reset_instance(
            instance.ResetInstanceRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_reset_instance_flattened_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.reset_instance), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.reset_instance(
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
async def test_reset_instance_flattened_error_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.reset_instance(
            instance.ResetInstanceRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        instance.StartInstanceRequest,
        dict,
    ],
)
def test_start_instance(request_type, transport: str = "grpc"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.start_instance), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.start_instance(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == instance.StartInstanceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_start_instance_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.start_instance), "__call__") as call:
        client.start_instance()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == instance.StartInstanceRequest()


@pytest.mark.asyncio
async def test_start_instance_async(
    transport: str = "grpc_asyncio", request_type=instance.StartInstanceRequest
):
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.start_instance), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.start_instance(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == instance.StartInstanceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_start_instance_async_from_dict():
    await test_start_instance_async(request_type=dict)


def test_start_instance_field_headers():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = instance.StartInstanceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.start_instance), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.start_instance(request)

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
async def test_start_instance_field_headers_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = instance.StartInstanceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.start_instance), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.start_instance(request)

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


def test_start_instance_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.start_instance), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.start_instance(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_start_instance_flattened_error():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.start_instance(
            instance.StartInstanceRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_start_instance_flattened_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.start_instance), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.start_instance(
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
async def test_start_instance_flattened_error_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.start_instance(
            instance.StartInstanceRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        instance.StopInstanceRequest,
        dict,
    ],
)
def test_stop_instance(request_type, transport: str = "grpc"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.stop_instance), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.stop_instance(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == instance.StopInstanceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_stop_instance_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.stop_instance), "__call__") as call:
        client.stop_instance()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == instance.StopInstanceRequest()


@pytest.mark.asyncio
async def test_stop_instance_async(
    transport: str = "grpc_asyncio", request_type=instance.StopInstanceRequest
):
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.stop_instance), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.stop_instance(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == instance.StopInstanceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_stop_instance_async_from_dict():
    await test_stop_instance_async(request_type=dict)


def test_stop_instance_field_headers():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = instance.StopInstanceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.stop_instance), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.stop_instance(request)

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
async def test_stop_instance_field_headers_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = instance.StopInstanceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.stop_instance), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.stop_instance(request)

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


def test_stop_instance_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.stop_instance), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.stop_instance(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_stop_instance_flattened_error():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.stop_instance(
            instance.StopInstanceRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_stop_instance_flattened_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.stop_instance), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.stop_instance(
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
async def test_stop_instance_flattened_error_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.stop_instance(
            instance.StopInstanceRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gcb_instance.DetachLunRequest,
        dict,
    ],
)
def test_detach_lun(request_type, transport: str = "grpc"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.detach_lun), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.detach_lun(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcb_instance.DetachLunRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_detach_lun_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.detach_lun), "__call__") as call:
        client.detach_lun()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcb_instance.DetachLunRequest()


@pytest.mark.asyncio
async def test_detach_lun_async(
    transport: str = "grpc_asyncio", request_type=gcb_instance.DetachLunRequest
):
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.detach_lun), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.detach_lun(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcb_instance.DetachLunRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_detach_lun_async_from_dict():
    await test_detach_lun_async(request_type=dict)


def test_detach_lun_field_headers():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcb_instance.DetachLunRequest()

    request.instance = "instance_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.detach_lun), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.detach_lun(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "instance=instance_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_detach_lun_field_headers_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcb_instance.DetachLunRequest()

    request.instance = "instance_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.detach_lun), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.detach_lun(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "instance=instance_value",
    ) in kw["metadata"]


def test_detach_lun_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.detach_lun), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.detach_lun(
            instance="instance_value",
            lun="lun_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].instance
        mock_val = "instance_value"
        assert arg == mock_val
        arg = args[0].lun
        mock_val = "lun_value"
        assert arg == mock_val


def test_detach_lun_flattened_error():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.detach_lun(
            gcb_instance.DetachLunRequest(),
            instance="instance_value",
            lun="lun_value",
        )


@pytest.mark.asyncio
async def test_detach_lun_flattened_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.detach_lun), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.detach_lun(
            instance="instance_value",
            lun="lun_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].instance
        mock_val = "instance_value"
        assert arg == mock_val
        arg = args[0].lun
        mock_val = "lun_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_detach_lun_flattened_error_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.detach_lun(
            gcb_instance.DetachLunRequest(),
            instance="instance_value",
            lun="lun_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        volume.ListVolumesRequest,
        dict,
    ],
)
def test_list_volumes(request_type, transport: str = "grpc"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_volumes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = volume.ListVolumesResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_volumes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == volume.ListVolumesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListVolumesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_volumes_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_volumes), "__call__") as call:
        client.list_volumes()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == volume.ListVolumesRequest()


@pytest.mark.asyncio
async def test_list_volumes_async(
    transport: str = "grpc_asyncio", request_type=volume.ListVolumesRequest
):
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_volumes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            volume.ListVolumesResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_volumes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == volume.ListVolumesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListVolumesAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_volumes_async_from_dict():
    await test_list_volumes_async(request_type=dict)


def test_list_volumes_field_headers():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = volume.ListVolumesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_volumes), "__call__") as call:
        call.return_value = volume.ListVolumesResponse()
        client.list_volumes(request)

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
async def test_list_volumes_field_headers_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = volume.ListVolumesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_volumes), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            volume.ListVolumesResponse()
        )
        await client.list_volumes(request)

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


def test_list_volumes_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_volumes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = volume.ListVolumesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_volumes(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_volumes_flattened_error():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_volumes(
            volume.ListVolumesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_volumes_flattened_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_volumes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = volume.ListVolumesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            volume.ListVolumesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_volumes(
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
async def test_list_volumes_flattened_error_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_volumes(
            volume.ListVolumesRequest(),
            parent="parent_value",
        )


def test_list_volumes_pager(transport_name: str = "grpc"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_volumes), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            volume.ListVolumesResponse(
                volumes=[
                    volume.Volume(),
                    volume.Volume(),
                    volume.Volume(),
                ],
                next_page_token="abc",
            ),
            volume.ListVolumesResponse(
                volumes=[],
                next_page_token="def",
            ),
            volume.ListVolumesResponse(
                volumes=[
                    volume.Volume(),
                ],
                next_page_token="ghi",
            ),
            volume.ListVolumesResponse(
                volumes=[
                    volume.Volume(),
                    volume.Volume(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_volumes(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, volume.Volume) for i in results)


def test_list_volumes_pages(transport_name: str = "grpc"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_volumes), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            volume.ListVolumesResponse(
                volumes=[
                    volume.Volume(),
                    volume.Volume(),
                    volume.Volume(),
                ],
                next_page_token="abc",
            ),
            volume.ListVolumesResponse(
                volumes=[],
                next_page_token="def",
            ),
            volume.ListVolumesResponse(
                volumes=[
                    volume.Volume(),
                ],
                next_page_token="ghi",
            ),
            volume.ListVolumesResponse(
                volumes=[
                    volume.Volume(),
                    volume.Volume(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_volumes(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_volumes_async_pager():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_volumes), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            volume.ListVolumesResponse(
                volumes=[
                    volume.Volume(),
                    volume.Volume(),
                    volume.Volume(),
                ],
                next_page_token="abc",
            ),
            volume.ListVolumesResponse(
                volumes=[],
                next_page_token="def",
            ),
            volume.ListVolumesResponse(
                volumes=[
                    volume.Volume(),
                ],
                next_page_token="ghi",
            ),
            volume.ListVolumesResponse(
                volumes=[
                    volume.Volume(),
                    volume.Volume(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_volumes(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, volume.Volume) for i in responses)


@pytest.mark.asyncio
async def test_list_volumes_async_pages():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_volumes), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            volume.ListVolumesResponse(
                volumes=[
                    volume.Volume(),
                    volume.Volume(),
                    volume.Volume(),
                ],
                next_page_token="abc",
            ),
            volume.ListVolumesResponse(
                volumes=[],
                next_page_token="def",
            ),
            volume.ListVolumesResponse(
                volumes=[
                    volume.Volume(),
                ],
                next_page_token="ghi",
            ),
            volume.ListVolumesResponse(
                volumes=[
                    volume.Volume(),
                    volume.Volume(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_volumes(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        volume.GetVolumeRequest,
        dict,
    ],
)
def test_get_volume(request_type, transport: str = "grpc"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_volume), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = volume.Volume(
            name="name_value",
            id="id_value",
            storage_type=volume.Volume.StorageType.SSD,
            state=volume.Volume.State.CREATING,
            requested_size_gib=1917,
            current_size_gib=1710,
            emergency_size_gib=1898,
            auto_grown_size_gib=2032,
            remaining_space_gib=1974,
            snapshot_auto_delete_behavior=volume.Volume.SnapshotAutoDeleteBehavior.DISABLED,
            snapshot_enabled=True,
            pod="pod_value",
        )
        response = client.get_volume(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == volume.GetVolumeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, volume.Volume)
    assert response.name == "name_value"
    assert response.id == "id_value"
    assert response.storage_type == volume.Volume.StorageType.SSD
    assert response.state == volume.Volume.State.CREATING
    assert response.requested_size_gib == 1917
    assert response.current_size_gib == 1710
    assert response.emergency_size_gib == 1898
    assert response.auto_grown_size_gib == 2032
    assert response.remaining_space_gib == 1974
    assert (
        response.snapshot_auto_delete_behavior
        == volume.Volume.SnapshotAutoDeleteBehavior.DISABLED
    )
    assert response.snapshot_enabled is True
    assert response.pod == "pod_value"


def test_get_volume_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_volume), "__call__") as call:
        client.get_volume()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == volume.GetVolumeRequest()


@pytest.mark.asyncio
async def test_get_volume_async(
    transport: str = "grpc_asyncio", request_type=volume.GetVolumeRequest
):
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_volume), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            volume.Volume(
                name="name_value",
                id="id_value",
                storage_type=volume.Volume.StorageType.SSD,
                state=volume.Volume.State.CREATING,
                requested_size_gib=1917,
                current_size_gib=1710,
                emergency_size_gib=1898,
                auto_grown_size_gib=2032,
                remaining_space_gib=1974,
                snapshot_auto_delete_behavior=volume.Volume.SnapshotAutoDeleteBehavior.DISABLED,
                snapshot_enabled=True,
                pod="pod_value",
            )
        )
        response = await client.get_volume(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == volume.GetVolumeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, volume.Volume)
    assert response.name == "name_value"
    assert response.id == "id_value"
    assert response.storage_type == volume.Volume.StorageType.SSD
    assert response.state == volume.Volume.State.CREATING
    assert response.requested_size_gib == 1917
    assert response.current_size_gib == 1710
    assert response.emergency_size_gib == 1898
    assert response.auto_grown_size_gib == 2032
    assert response.remaining_space_gib == 1974
    assert (
        response.snapshot_auto_delete_behavior
        == volume.Volume.SnapshotAutoDeleteBehavior.DISABLED
    )
    assert response.snapshot_enabled is True
    assert response.pod == "pod_value"


@pytest.mark.asyncio
async def test_get_volume_async_from_dict():
    await test_get_volume_async(request_type=dict)


def test_get_volume_field_headers():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = volume.GetVolumeRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_volume), "__call__") as call:
        call.return_value = volume.Volume()
        client.get_volume(request)

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
async def test_get_volume_field_headers_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = volume.GetVolumeRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_volume), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(volume.Volume())
        await client.get_volume(request)

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


def test_get_volume_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_volume), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = volume.Volume()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_volume(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_volume_flattened_error():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_volume(
            volume.GetVolumeRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_volume_flattened_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_volume), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = volume.Volume()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(volume.Volume())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_volume(
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
async def test_get_volume_flattened_error_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_volume(
            volume.GetVolumeRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gcb_volume.UpdateVolumeRequest,
        dict,
    ],
)
def test_update_volume(request_type, transport: str = "grpc"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_volume), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_volume(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcb_volume.UpdateVolumeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_volume_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_volume), "__call__") as call:
        client.update_volume()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcb_volume.UpdateVolumeRequest()


@pytest.mark.asyncio
async def test_update_volume_async(
    transport: str = "grpc_asyncio", request_type=gcb_volume.UpdateVolumeRequest
):
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_volume), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_volume(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcb_volume.UpdateVolumeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_volume_async_from_dict():
    await test_update_volume_async(request_type=dict)


def test_update_volume_field_headers():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcb_volume.UpdateVolumeRequest()

    request.volume.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_volume), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_volume(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "volume.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_volume_field_headers_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcb_volume.UpdateVolumeRequest()

    request.volume.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_volume), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_volume(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "volume.name=name_value",
    ) in kw["metadata"]


def test_update_volume_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_volume), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_volume(
            volume=gcb_volume.Volume(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].volume
        mock_val = gcb_volume.Volume(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_volume_flattened_error():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_volume(
            gcb_volume.UpdateVolumeRequest(),
            volume=gcb_volume.Volume(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_volume_flattened_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_volume), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_volume(
            volume=gcb_volume.Volume(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].volume
        mock_val = gcb_volume.Volume(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_volume_flattened_error_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_volume(
            gcb_volume.UpdateVolumeRequest(),
            volume=gcb_volume.Volume(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gcb_volume.ResizeVolumeRequest,
        dict,
    ],
)
def test_resize_volume(request_type, transport: str = "grpc"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.resize_volume), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.resize_volume(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcb_volume.ResizeVolumeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_resize_volume_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.resize_volume), "__call__") as call:
        client.resize_volume()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcb_volume.ResizeVolumeRequest()


@pytest.mark.asyncio
async def test_resize_volume_async(
    transport: str = "grpc_asyncio", request_type=gcb_volume.ResizeVolumeRequest
):
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.resize_volume), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.resize_volume(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcb_volume.ResizeVolumeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_resize_volume_async_from_dict():
    await test_resize_volume_async(request_type=dict)


def test_resize_volume_field_headers():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcb_volume.ResizeVolumeRequest()

    request.volume = "volume_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.resize_volume), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.resize_volume(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "volume=volume_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_resize_volume_field_headers_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcb_volume.ResizeVolumeRequest()

    request.volume = "volume_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.resize_volume), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.resize_volume(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "volume=volume_value",
    ) in kw["metadata"]


def test_resize_volume_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.resize_volume), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.resize_volume(
            volume="volume_value",
            size_gib=844,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].volume
        mock_val = "volume_value"
        assert arg == mock_val
        arg = args[0].size_gib
        mock_val = 844
        assert arg == mock_val


def test_resize_volume_flattened_error():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.resize_volume(
            gcb_volume.ResizeVolumeRequest(),
            volume="volume_value",
            size_gib=844,
        )


@pytest.mark.asyncio
async def test_resize_volume_flattened_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.resize_volume), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.resize_volume(
            volume="volume_value",
            size_gib=844,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].volume
        mock_val = "volume_value"
        assert arg == mock_val
        arg = args[0].size_gib
        mock_val = 844
        assert arg == mock_val


@pytest.mark.asyncio
async def test_resize_volume_flattened_error_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.resize_volume(
            gcb_volume.ResizeVolumeRequest(),
            volume="volume_value",
            size_gib=844,
        )


@pytest.mark.parametrize(
    "request_type",
    [
        network.ListNetworksRequest,
        dict,
    ],
)
def test_list_networks(request_type, transport: str = "grpc"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_networks), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = network.ListNetworksResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_networks(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == network.ListNetworksRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListNetworksPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_networks_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_networks), "__call__") as call:
        client.list_networks()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == network.ListNetworksRequest()


@pytest.mark.asyncio
async def test_list_networks_async(
    transport: str = "grpc_asyncio", request_type=network.ListNetworksRequest
):
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_networks), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            network.ListNetworksResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_networks(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == network.ListNetworksRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListNetworksAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_networks_async_from_dict():
    await test_list_networks_async(request_type=dict)


def test_list_networks_field_headers():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = network.ListNetworksRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_networks), "__call__") as call:
        call.return_value = network.ListNetworksResponse()
        client.list_networks(request)

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
async def test_list_networks_field_headers_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = network.ListNetworksRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_networks), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            network.ListNetworksResponse()
        )
        await client.list_networks(request)

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


def test_list_networks_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_networks), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = network.ListNetworksResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_networks(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_networks_flattened_error():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_networks(
            network.ListNetworksRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_networks_flattened_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_networks), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = network.ListNetworksResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            network.ListNetworksResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_networks(
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
async def test_list_networks_flattened_error_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_networks(
            network.ListNetworksRequest(),
            parent="parent_value",
        )


def test_list_networks_pager(transport_name: str = "grpc"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_networks), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            network.ListNetworksResponse(
                networks=[
                    network.Network(),
                    network.Network(),
                    network.Network(),
                ],
                next_page_token="abc",
            ),
            network.ListNetworksResponse(
                networks=[],
                next_page_token="def",
            ),
            network.ListNetworksResponse(
                networks=[
                    network.Network(),
                ],
                next_page_token="ghi",
            ),
            network.ListNetworksResponse(
                networks=[
                    network.Network(),
                    network.Network(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_networks(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, network.Network) for i in results)


def test_list_networks_pages(transport_name: str = "grpc"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_networks), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            network.ListNetworksResponse(
                networks=[
                    network.Network(),
                    network.Network(),
                    network.Network(),
                ],
                next_page_token="abc",
            ),
            network.ListNetworksResponse(
                networks=[],
                next_page_token="def",
            ),
            network.ListNetworksResponse(
                networks=[
                    network.Network(),
                ],
                next_page_token="ghi",
            ),
            network.ListNetworksResponse(
                networks=[
                    network.Network(),
                    network.Network(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_networks(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_networks_async_pager():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_networks), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            network.ListNetworksResponse(
                networks=[
                    network.Network(),
                    network.Network(),
                    network.Network(),
                ],
                next_page_token="abc",
            ),
            network.ListNetworksResponse(
                networks=[],
                next_page_token="def",
            ),
            network.ListNetworksResponse(
                networks=[
                    network.Network(),
                ],
                next_page_token="ghi",
            ),
            network.ListNetworksResponse(
                networks=[
                    network.Network(),
                    network.Network(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_networks(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, network.Network) for i in responses)


@pytest.mark.asyncio
async def test_list_networks_async_pages():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_networks), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            network.ListNetworksResponse(
                networks=[
                    network.Network(),
                    network.Network(),
                    network.Network(),
                ],
                next_page_token="abc",
            ),
            network.ListNetworksResponse(
                networks=[],
                next_page_token="def",
            ),
            network.ListNetworksResponse(
                networks=[
                    network.Network(),
                ],
                next_page_token="ghi",
            ),
            network.ListNetworksResponse(
                networks=[
                    network.Network(),
                    network.Network(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_networks(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        network.ListNetworkUsageRequest,
        dict,
    ],
)
def test_list_network_usage(request_type, transport: str = "grpc"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_network_usage), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = network.ListNetworkUsageResponse()
        response = client.list_network_usage(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == network.ListNetworkUsageRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, network.ListNetworkUsageResponse)


def test_list_network_usage_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_network_usage), "__call__"
    ) as call:
        client.list_network_usage()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == network.ListNetworkUsageRequest()


@pytest.mark.asyncio
async def test_list_network_usage_async(
    transport: str = "grpc_asyncio", request_type=network.ListNetworkUsageRequest
):
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_network_usage), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            network.ListNetworkUsageResponse()
        )
        response = await client.list_network_usage(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == network.ListNetworkUsageRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, network.ListNetworkUsageResponse)


@pytest.mark.asyncio
async def test_list_network_usage_async_from_dict():
    await test_list_network_usage_async(request_type=dict)


def test_list_network_usage_field_headers():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = network.ListNetworkUsageRequest()

    request.location = "location_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_network_usage), "__call__"
    ) as call:
        call.return_value = network.ListNetworkUsageResponse()
        client.list_network_usage(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "location=location_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_network_usage_field_headers_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = network.ListNetworkUsageRequest()

    request.location = "location_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_network_usage), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            network.ListNetworkUsageResponse()
        )
        await client.list_network_usage(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "location=location_value",
    ) in kw["metadata"]


def test_list_network_usage_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_network_usage), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = network.ListNetworkUsageResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_network_usage(
            location="location_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].location
        mock_val = "location_value"
        assert arg == mock_val


def test_list_network_usage_flattened_error():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_network_usage(
            network.ListNetworkUsageRequest(),
            location="location_value",
        )


@pytest.mark.asyncio
async def test_list_network_usage_flattened_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_network_usage), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = network.ListNetworkUsageResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            network.ListNetworkUsageResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_network_usage(
            location="location_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].location
        mock_val = "location_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_network_usage_flattened_error_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_network_usage(
            network.ListNetworkUsageRequest(),
            location="location_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        network.GetNetworkRequest,
        dict,
    ],
)
def test_get_network(request_type, transport: str = "grpc"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_network), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = network.Network(
            name="name_value",
            id="id_value",
            type_=network.Network.Type.CLIENT,
            ip_address="ip_address_value",
            mac_address=["mac_address_value"],
            state=network.Network.State.PROVISIONING,
            vlan_id="vlan_id_value",
            cidr="cidr_value",
            services_cidr="services_cidr_value",
        )
        response = client.get_network(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == network.GetNetworkRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, network.Network)
    assert response.name == "name_value"
    assert response.id == "id_value"
    assert response.type_ == network.Network.Type.CLIENT
    assert response.ip_address == "ip_address_value"
    assert response.mac_address == ["mac_address_value"]
    assert response.state == network.Network.State.PROVISIONING
    assert response.vlan_id == "vlan_id_value"
    assert response.cidr == "cidr_value"
    assert response.services_cidr == "services_cidr_value"


def test_get_network_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_network), "__call__") as call:
        client.get_network()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == network.GetNetworkRequest()


@pytest.mark.asyncio
async def test_get_network_async(
    transport: str = "grpc_asyncio", request_type=network.GetNetworkRequest
):
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_network), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            network.Network(
                name="name_value",
                id="id_value",
                type_=network.Network.Type.CLIENT,
                ip_address="ip_address_value",
                mac_address=["mac_address_value"],
                state=network.Network.State.PROVISIONING,
                vlan_id="vlan_id_value",
                cidr="cidr_value",
                services_cidr="services_cidr_value",
            )
        )
        response = await client.get_network(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == network.GetNetworkRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, network.Network)
    assert response.name == "name_value"
    assert response.id == "id_value"
    assert response.type_ == network.Network.Type.CLIENT
    assert response.ip_address == "ip_address_value"
    assert response.mac_address == ["mac_address_value"]
    assert response.state == network.Network.State.PROVISIONING
    assert response.vlan_id == "vlan_id_value"
    assert response.cidr == "cidr_value"
    assert response.services_cidr == "services_cidr_value"


@pytest.mark.asyncio
async def test_get_network_async_from_dict():
    await test_get_network_async(request_type=dict)


def test_get_network_field_headers():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = network.GetNetworkRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_network), "__call__") as call:
        call.return_value = network.Network()
        client.get_network(request)

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
async def test_get_network_field_headers_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = network.GetNetworkRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_network), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(network.Network())
        await client.get_network(request)

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


def test_get_network_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_network), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = network.Network()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_network(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_network_flattened_error():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_network(
            network.GetNetworkRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_network_flattened_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_network), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = network.Network()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(network.Network())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_network(
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
async def test_get_network_flattened_error_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_network(
            network.GetNetworkRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gcb_network.UpdateNetworkRequest,
        dict,
    ],
)
def test_update_network(request_type, transport: str = "grpc"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_network), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_network(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcb_network.UpdateNetworkRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_network_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_network), "__call__") as call:
        client.update_network()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcb_network.UpdateNetworkRequest()


@pytest.mark.asyncio
async def test_update_network_async(
    transport: str = "grpc_asyncio", request_type=gcb_network.UpdateNetworkRequest
):
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_network), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_network(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcb_network.UpdateNetworkRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_network_async_from_dict():
    await test_update_network_async(request_type=dict)


def test_update_network_field_headers():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcb_network.UpdateNetworkRequest()

    request.network.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_network), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_network(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "network.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_network_field_headers_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcb_network.UpdateNetworkRequest()

    request.network.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_network), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_network(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "network.name=name_value",
    ) in kw["metadata"]


def test_update_network_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_network), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_network(
            network=gcb_network.Network(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].network
        mock_val = gcb_network.Network(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_network_flattened_error():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_network(
            gcb_network.UpdateNetworkRequest(),
            network=gcb_network.Network(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_network_flattened_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_network), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_network(
            network=gcb_network.Network(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].network
        mock_val = gcb_network.Network(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_network_flattened_error_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_network(
            gcb_network.UpdateNetworkRequest(),
            network=gcb_network.Network(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        lun.GetLunRequest,
        dict,
    ],
)
def test_get_lun(request_type, transport: str = "grpc"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_lun), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = lun.Lun(
            name="name_value",
            id="id_value",
            state=lun.Lun.State.CREATING,
            size_gb=739,
            multiprotocol_type=lun.Lun.MultiprotocolType.LINUX,
            storage_volume="storage_volume_value",
            shareable=True,
            boot_lun=True,
            storage_type=lun.Lun.StorageType.SSD,
            wwid="wwid_value",
        )
        response = client.get_lun(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == lun.GetLunRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, lun.Lun)
    assert response.name == "name_value"
    assert response.id == "id_value"
    assert response.state == lun.Lun.State.CREATING
    assert response.size_gb == 739
    assert response.multiprotocol_type == lun.Lun.MultiprotocolType.LINUX
    assert response.storage_volume == "storage_volume_value"
    assert response.shareable is True
    assert response.boot_lun is True
    assert response.storage_type == lun.Lun.StorageType.SSD
    assert response.wwid == "wwid_value"


def test_get_lun_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_lun), "__call__") as call:
        client.get_lun()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == lun.GetLunRequest()


@pytest.mark.asyncio
async def test_get_lun_async(
    transport: str = "grpc_asyncio", request_type=lun.GetLunRequest
):
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_lun), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            lun.Lun(
                name="name_value",
                id="id_value",
                state=lun.Lun.State.CREATING,
                size_gb=739,
                multiprotocol_type=lun.Lun.MultiprotocolType.LINUX,
                storage_volume="storage_volume_value",
                shareable=True,
                boot_lun=True,
                storage_type=lun.Lun.StorageType.SSD,
                wwid="wwid_value",
            )
        )
        response = await client.get_lun(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == lun.GetLunRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, lun.Lun)
    assert response.name == "name_value"
    assert response.id == "id_value"
    assert response.state == lun.Lun.State.CREATING
    assert response.size_gb == 739
    assert response.multiprotocol_type == lun.Lun.MultiprotocolType.LINUX
    assert response.storage_volume == "storage_volume_value"
    assert response.shareable is True
    assert response.boot_lun is True
    assert response.storage_type == lun.Lun.StorageType.SSD
    assert response.wwid == "wwid_value"


@pytest.mark.asyncio
async def test_get_lun_async_from_dict():
    await test_get_lun_async(request_type=dict)


def test_get_lun_field_headers():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = lun.GetLunRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_lun), "__call__") as call:
        call.return_value = lun.Lun()
        client.get_lun(request)

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
async def test_get_lun_field_headers_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = lun.GetLunRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_lun), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(lun.Lun())
        await client.get_lun(request)

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


def test_get_lun_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_lun), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = lun.Lun()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_lun(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_lun_flattened_error():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_lun(
            lun.GetLunRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_lun_flattened_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_lun), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = lun.Lun()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(lun.Lun())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_lun(
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
async def test_get_lun_flattened_error_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_lun(
            lun.GetLunRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        lun.ListLunsRequest,
        dict,
    ],
)
def test_list_luns(request_type, transport: str = "grpc"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_luns), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = lun.ListLunsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_luns(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == lun.ListLunsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListLunsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_luns_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_luns), "__call__") as call:
        client.list_luns()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == lun.ListLunsRequest()


@pytest.mark.asyncio
async def test_list_luns_async(
    transport: str = "grpc_asyncio", request_type=lun.ListLunsRequest
):
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_luns), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            lun.ListLunsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_luns(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == lun.ListLunsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListLunsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_luns_async_from_dict():
    await test_list_luns_async(request_type=dict)


def test_list_luns_field_headers():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = lun.ListLunsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_luns), "__call__") as call:
        call.return_value = lun.ListLunsResponse()
        client.list_luns(request)

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
async def test_list_luns_field_headers_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = lun.ListLunsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_luns), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            lun.ListLunsResponse()
        )
        await client.list_luns(request)

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


def test_list_luns_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_luns), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = lun.ListLunsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_luns(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_luns_flattened_error():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_luns(
            lun.ListLunsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_luns_flattened_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_luns), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = lun.ListLunsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            lun.ListLunsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_luns(
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
async def test_list_luns_flattened_error_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_luns(
            lun.ListLunsRequest(),
            parent="parent_value",
        )


def test_list_luns_pager(transport_name: str = "grpc"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_luns), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            lun.ListLunsResponse(
                luns=[
                    lun.Lun(),
                    lun.Lun(),
                    lun.Lun(),
                ],
                next_page_token="abc",
            ),
            lun.ListLunsResponse(
                luns=[],
                next_page_token="def",
            ),
            lun.ListLunsResponse(
                luns=[
                    lun.Lun(),
                ],
                next_page_token="ghi",
            ),
            lun.ListLunsResponse(
                luns=[
                    lun.Lun(),
                    lun.Lun(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_luns(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, lun.Lun) for i in results)


def test_list_luns_pages(transport_name: str = "grpc"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_luns), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            lun.ListLunsResponse(
                luns=[
                    lun.Lun(),
                    lun.Lun(),
                    lun.Lun(),
                ],
                next_page_token="abc",
            ),
            lun.ListLunsResponse(
                luns=[],
                next_page_token="def",
            ),
            lun.ListLunsResponse(
                luns=[
                    lun.Lun(),
                ],
                next_page_token="ghi",
            ),
            lun.ListLunsResponse(
                luns=[
                    lun.Lun(),
                    lun.Lun(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_luns(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_luns_async_pager():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_luns), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            lun.ListLunsResponse(
                luns=[
                    lun.Lun(),
                    lun.Lun(),
                    lun.Lun(),
                ],
                next_page_token="abc",
            ),
            lun.ListLunsResponse(
                luns=[],
                next_page_token="def",
            ),
            lun.ListLunsResponse(
                luns=[
                    lun.Lun(),
                ],
                next_page_token="ghi",
            ),
            lun.ListLunsResponse(
                luns=[
                    lun.Lun(),
                    lun.Lun(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_luns(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, lun.Lun) for i in responses)


@pytest.mark.asyncio
async def test_list_luns_async_pages():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_luns), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            lun.ListLunsResponse(
                luns=[
                    lun.Lun(),
                    lun.Lun(),
                    lun.Lun(),
                ],
                next_page_token="abc",
            ),
            lun.ListLunsResponse(
                luns=[],
                next_page_token="def",
            ),
            lun.ListLunsResponse(
                luns=[
                    lun.Lun(),
                ],
                next_page_token="ghi",
            ),
            lun.ListLunsResponse(
                luns=[
                    lun.Lun(),
                    lun.Lun(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_luns(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        nfs_share.GetNfsShareRequest,
        dict,
    ],
)
def test_get_nfs_share(request_type, transport: str = "grpc"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_nfs_share), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = nfs_share.NfsShare(
            name="name_value",
            nfs_share_id="nfs_share_id_value",
            state=nfs_share.NfsShare.State.PROVISIONED,
            volume="volume_value",
        )
        response = client.get_nfs_share(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == nfs_share.GetNfsShareRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, nfs_share.NfsShare)
    assert response.name == "name_value"
    assert response.nfs_share_id == "nfs_share_id_value"
    assert response.state == nfs_share.NfsShare.State.PROVISIONED
    assert response.volume == "volume_value"


def test_get_nfs_share_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_nfs_share), "__call__") as call:
        client.get_nfs_share()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == nfs_share.GetNfsShareRequest()


@pytest.mark.asyncio
async def test_get_nfs_share_async(
    transport: str = "grpc_asyncio", request_type=nfs_share.GetNfsShareRequest
):
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_nfs_share), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            nfs_share.NfsShare(
                name="name_value",
                nfs_share_id="nfs_share_id_value",
                state=nfs_share.NfsShare.State.PROVISIONED,
                volume="volume_value",
            )
        )
        response = await client.get_nfs_share(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == nfs_share.GetNfsShareRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, nfs_share.NfsShare)
    assert response.name == "name_value"
    assert response.nfs_share_id == "nfs_share_id_value"
    assert response.state == nfs_share.NfsShare.State.PROVISIONED
    assert response.volume == "volume_value"


@pytest.mark.asyncio
async def test_get_nfs_share_async_from_dict():
    await test_get_nfs_share_async(request_type=dict)


def test_get_nfs_share_field_headers():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = nfs_share.GetNfsShareRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_nfs_share), "__call__") as call:
        call.return_value = nfs_share.NfsShare()
        client.get_nfs_share(request)

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
async def test_get_nfs_share_field_headers_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = nfs_share.GetNfsShareRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_nfs_share), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(nfs_share.NfsShare())
        await client.get_nfs_share(request)

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


def test_get_nfs_share_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_nfs_share), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = nfs_share.NfsShare()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_nfs_share(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_nfs_share_flattened_error():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_nfs_share(
            nfs_share.GetNfsShareRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_nfs_share_flattened_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_nfs_share), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = nfs_share.NfsShare()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(nfs_share.NfsShare())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_nfs_share(
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
async def test_get_nfs_share_flattened_error_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_nfs_share(
            nfs_share.GetNfsShareRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        nfs_share.ListNfsSharesRequest,
        dict,
    ],
)
def test_list_nfs_shares(request_type, transport: str = "grpc"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_nfs_shares), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = nfs_share.ListNfsSharesResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_nfs_shares(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == nfs_share.ListNfsSharesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListNfsSharesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_nfs_shares_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_nfs_shares), "__call__") as call:
        client.list_nfs_shares()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == nfs_share.ListNfsSharesRequest()


@pytest.mark.asyncio
async def test_list_nfs_shares_async(
    transport: str = "grpc_asyncio", request_type=nfs_share.ListNfsSharesRequest
):
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_nfs_shares), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            nfs_share.ListNfsSharesResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_nfs_shares(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == nfs_share.ListNfsSharesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListNfsSharesAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_nfs_shares_async_from_dict():
    await test_list_nfs_shares_async(request_type=dict)


def test_list_nfs_shares_field_headers():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = nfs_share.ListNfsSharesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_nfs_shares), "__call__") as call:
        call.return_value = nfs_share.ListNfsSharesResponse()
        client.list_nfs_shares(request)

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
async def test_list_nfs_shares_field_headers_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = nfs_share.ListNfsSharesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_nfs_shares), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            nfs_share.ListNfsSharesResponse()
        )
        await client.list_nfs_shares(request)

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


def test_list_nfs_shares_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_nfs_shares), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = nfs_share.ListNfsSharesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_nfs_shares(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_nfs_shares_flattened_error():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_nfs_shares(
            nfs_share.ListNfsSharesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_nfs_shares_flattened_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_nfs_shares), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = nfs_share.ListNfsSharesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            nfs_share.ListNfsSharesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_nfs_shares(
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
async def test_list_nfs_shares_flattened_error_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_nfs_shares(
            nfs_share.ListNfsSharesRequest(),
            parent="parent_value",
        )


def test_list_nfs_shares_pager(transport_name: str = "grpc"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_nfs_shares), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            nfs_share.ListNfsSharesResponse(
                nfs_shares=[
                    nfs_share.NfsShare(),
                    nfs_share.NfsShare(),
                    nfs_share.NfsShare(),
                ],
                next_page_token="abc",
            ),
            nfs_share.ListNfsSharesResponse(
                nfs_shares=[],
                next_page_token="def",
            ),
            nfs_share.ListNfsSharesResponse(
                nfs_shares=[
                    nfs_share.NfsShare(),
                ],
                next_page_token="ghi",
            ),
            nfs_share.ListNfsSharesResponse(
                nfs_shares=[
                    nfs_share.NfsShare(),
                    nfs_share.NfsShare(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_nfs_shares(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, nfs_share.NfsShare) for i in results)


def test_list_nfs_shares_pages(transport_name: str = "grpc"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_nfs_shares), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            nfs_share.ListNfsSharesResponse(
                nfs_shares=[
                    nfs_share.NfsShare(),
                    nfs_share.NfsShare(),
                    nfs_share.NfsShare(),
                ],
                next_page_token="abc",
            ),
            nfs_share.ListNfsSharesResponse(
                nfs_shares=[],
                next_page_token="def",
            ),
            nfs_share.ListNfsSharesResponse(
                nfs_shares=[
                    nfs_share.NfsShare(),
                ],
                next_page_token="ghi",
            ),
            nfs_share.ListNfsSharesResponse(
                nfs_shares=[
                    nfs_share.NfsShare(),
                    nfs_share.NfsShare(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_nfs_shares(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_nfs_shares_async_pager():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_nfs_shares), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            nfs_share.ListNfsSharesResponse(
                nfs_shares=[
                    nfs_share.NfsShare(),
                    nfs_share.NfsShare(),
                    nfs_share.NfsShare(),
                ],
                next_page_token="abc",
            ),
            nfs_share.ListNfsSharesResponse(
                nfs_shares=[],
                next_page_token="def",
            ),
            nfs_share.ListNfsSharesResponse(
                nfs_shares=[
                    nfs_share.NfsShare(),
                ],
                next_page_token="ghi",
            ),
            nfs_share.ListNfsSharesResponse(
                nfs_shares=[
                    nfs_share.NfsShare(),
                    nfs_share.NfsShare(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_nfs_shares(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, nfs_share.NfsShare) for i in responses)


@pytest.mark.asyncio
async def test_list_nfs_shares_async_pages():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_nfs_shares), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            nfs_share.ListNfsSharesResponse(
                nfs_shares=[
                    nfs_share.NfsShare(),
                    nfs_share.NfsShare(),
                    nfs_share.NfsShare(),
                ],
                next_page_token="abc",
            ),
            nfs_share.ListNfsSharesResponse(
                nfs_shares=[],
                next_page_token="def",
            ),
            nfs_share.ListNfsSharesResponse(
                nfs_shares=[
                    nfs_share.NfsShare(),
                ],
                next_page_token="ghi",
            ),
            nfs_share.ListNfsSharesResponse(
                nfs_shares=[
                    nfs_share.NfsShare(),
                    nfs_share.NfsShare(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_nfs_shares(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        gcb_nfs_share.UpdateNfsShareRequest,
        dict,
    ],
)
def test_update_nfs_share(request_type, transport: str = "grpc"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_nfs_share), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_nfs_share(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcb_nfs_share.UpdateNfsShareRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_nfs_share_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_nfs_share), "__call__") as call:
        client.update_nfs_share()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcb_nfs_share.UpdateNfsShareRequest()


@pytest.mark.asyncio
async def test_update_nfs_share_async(
    transport: str = "grpc_asyncio", request_type=gcb_nfs_share.UpdateNfsShareRequest
):
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_nfs_share), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_nfs_share(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcb_nfs_share.UpdateNfsShareRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_nfs_share_async_from_dict():
    await test_update_nfs_share_async(request_type=dict)


def test_update_nfs_share_field_headers():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcb_nfs_share.UpdateNfsShareRequest()

    request.nfs_share.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_nfs_share), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_nfs_share(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "nfs_share.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_nfs_share_field_headers_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gcb_nfs_share.UpdateNfsShareRequest()

    request.nfs_share.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_nfs_share), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_nfs_share(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "nfs_share.name=name_value",
    ) in kw["metadata"]


def test_update_nfs_share_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_nfs_share), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_nfs_share(
            nfs_share=gcb_nfs_share.NfsShare(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].nfs_share
        mock_val = gcb_nfs_share.NfsShare(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_nfs_share_flattened_error():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_nfs_share(
            gcb_nfs_share.UpdateNfsShareRequest(),
            nfs_share=gcb_nfs_share.NfsShare(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_nfs_share_flattened_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_nfs_share), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_nfs_share(
            nfs_share=gcb_nfs_share.NfsShare(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].nfs_share
        mock_val = gcb_nfs_share.NfsShare(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_nfs_share_flattened_error_async():
    client = BareMetalSolutionAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_nfs_share(
            gcb_nfs_share.UpdateNfsShareRequest(),
            nfs_share=gcb_nfs_share.NfsShare(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        instance.ListInstancesRequest,
        dict,
    ],
)
def test_list_instances_rest(request_type):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = instance.ListInstancesResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = instance.ListInstancesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_instances(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListInstancesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_instances_rest_required_fields(
    request_type=instance.ListInstancesRequest,
):
    transport_class = transports.BareMetalSolutionRestTransport

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
    ).list_instances._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_instances._get_unset_required_fields(jsonified_request)
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

    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = instance.ListInstancesResponse()
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

            pb_return_value = instance.ListInstancesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_instances(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_instances_rest_unset_required_fields():
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_instances._get_unset_required_fields({})
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
def test_list_instances_rest_interceptors(null_interceptor):
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.BareMetalSolutionRestInterceptor(),
    )
    client = BareMetalSolutionClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "post_list_instances"
    ) as post, mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "pre_list_instances"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = instance.ListInstancesRequest.pb(instance.ListInstancesRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = instance.ListInstancesResponse.to_json(
            instance.ListInstancesResponse()
        )

        request = instance.ListInstancesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = instance.ListInstancesResponse()

        client.list_instances(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_instances_rest_bad_request(
    transport: str = "rest", request_type=instance.ListInstancesRequest
):
    client = BareMetalSolutionClient(
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
        client.list_instances(request)


def test_list_instances_rest_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = instance.ListInstancesResponse()

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
        pb_return_value = instance.ListInstancesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_instances(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{parent=projects/*/locations/*}/instances" % client.transport._host,
            args[1],
        )


def test_list_instances_rest_flattened_error(transport: str = "rest"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_instances(
            instance.ListInstancesRequest(),
            parent="parent_value",
        )


def test_list_instances_rest_pager(transport: str = "rest"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            instance.ListInstancesResponse(
                instances=[
                    instance.Instance(),
                    instance.Instance(),
                    instance.Instance(),
                ],
                next_page_token="abc",
            ),
            instance.ListInstancesResponse(
                instances=[],
                next_page_token="def",
            ),
            instance.ListInstancesResponse(
                instances=[
                    instance.Instance(),
                ],
                next_page_token="ghi",
            ),
            instance.ListInstancesResponse(
                instances=[
                    instance.Instance(),
                    instance.Instance(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(instance.ListInstancesResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_instances(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, instance.Instance) for i in results)

        pages = list(client.list_instances(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        instance.GetInstanceRequest,
        dict,
    ],
)
def test_get_instance_rest(request_type):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/instances/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = instance.Instance(
            name="name_value",
            id="id_value",
            machine_type="machine_type_value",
            state=instance.Instance.State.PROVISIONING,
            hyperthreading_enabled=True,
            interactive_serial_console_enabled=True,
            os_image="os_image_value",
            pod="pod_value",
            network_template="network_template_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = instance.Instance.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_instance(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, instance.Instance)
    assert response.name == "name_value"
    assert response.id == "id_value"
    assert response.machine_type == "machine_type_value"
    assert response.state == instance.Instance.State.PROVISIONING
    assert response.hyperthreading_enabled is True
    assert response.interactive_serial_console_enabled is True
    assert response.os_image == "os_image_value"
    assert response.pod == "pod_value"
    assert response.network_template == "network_template_value"


def test_get_instance_rest_required_fields(request_type=instance.GetInstanceRequest):
    transport_class = transports.BareMetalSolutionRestTransport

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
    ).get_instance._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_instance._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = instance.Instance()
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

            pb_return_value = instance.Instance.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_instance(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_instance_rest_unset_required_fields():
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_instance._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_instance_rest_interceptors(null_interceptor):
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.BareMetalSolutionRestInterceptor(),
    )
    client = BareMetalSolutionClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "post_get_instance"
    ) as post, mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "pre_get_instance"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = instance.GetInstanceRequest.pb(instance.GetInstanceRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = instance.Instance.to_json(instance.Instance())

        request = instance.GetInstanceRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = instance.Instance()

        client.get_instance(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_instance_rest_bad_request(
    transport: str = "rest", request_type=instance.GetInstanceRequest
):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/instances/sample3"}
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
        client.get_instance(request)


def test_get_instance_rest_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = instance.Instance()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/instances/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = instance.Instance.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_instance(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{name=projects/*/locations/*/instances/*}" % client.transport._host,
            args[1],
        )


def test_get_instance_rest_flattened_error(transport: str = "rest"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_instance(
            instance.GetInstanceRequest(),
            name="name_value",
        )


def test_get_instance_rest_error():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        gcb_instance.UpdateInstanceRequest,
        dict,
    ],
)
def test_update_instance_rest(request_type):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "instance": {"name": "projects/sample1/locations/sample2/instances/sample3"}
    }
    request_init["instance"] = {
        "name": "projects/sample1/locations/sample2/instances/sample3",
        "id": "id_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "machine_type": "machine_type_value",
        "state": 1,
        "hyperthreading_enabled": True,
        "labels": {},
        "luns": [
            {
                "name": "name_value",
                "id": "id_value",
                "state": 1,
                "size_gb": 739,
                "multiprotocol_type": 1,
                "storage_volume": "storage_volume_value",
                "shareable": True,
                "boot_lun": True,
                "storage_type": 1,
                "wwid": "wwid_value",
            }
        ],
        "networks": [
            {
                "name": "name_value",
                "id": "id_value",
                "type_": 1,
                "ip_address": "ip_address_value",
                "mac_address": ["mac_address_value1", "mac_address_value2"],
                "state": 1,
                "vlan_id": "vlan_id_value",
                "cidr": "cidr_value",
                "vrf": {
                    "name": "name_value",
                    "state": 1,
                    "qos_policy": {"bandwidth_gbps": 0.1472},
                    "vlan_attachments": [
                        {
                            "peer_vlan_id": 1256,
                            "peer_ip": "peer_ip_value",
                            "router_ip": "router_ip_value",
                        }
                    ],
                },
                "labels": {},
                "services_cidr": "services_cidr_value",
                "reservations": [
                    {
                        "start_address": "start_address_value",
                        "end_address": "end_address_value",
                        "note": "note_value",
                    }
                ],
            }
        ],
        "interactive_serial_console_enabled": True,
        "os_image": "os_image_value",
        "pod": "pod_value",
        "network_template": "network_template_value",
        "logical_interfaces": [
            {
                "logical_network_interfaces": [
                    {
                        "network": "network_value",
                        "ip_address": "ip_address_value",
                        "default_gateway": True,
                        "network_type": 1,
                        "id": "id_value",
                    }
                ],
                "name": "name_value",
                "interface_index": 1576,
            }
        ],
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
        response = client.update_instance(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_instance_rest_required_fields(
    request_type=gcb_instance.UpdateInstanceRequest,
):
    transport_class = transports.BareMetalSolutionRestTransport

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
    ).update_instance._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_instance._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = BareMetalSolutionClient(
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
                "method": "patch",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_instance(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_instance_rest_unset_required_fields():
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_instance._get_unset_required_fields({})
    assert set(unset_fields) == (set(("updateMask",)) & set(("instance",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_instance_rest_interceptors(null_interceptor):
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.BareMetalSolutionRestInterceptor(),
    )
    client = BareMetalSolutionClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "post_update_instance"
    ) as post, mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "pre_update_instance"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gcb_instance.UpdateInstanceRequest.pb(
            gcb_instance.UpdateInstanceRequest()
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

        request = gcb_instance.UpdateInstanceRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_instance(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_instance_rest_bad_request(
    transport: str = "rest", request_type=gcb_instance.UpdateInstanceRequest
):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "instance": {"name": "projects/sample1/locations/sample2/instances/sample3"}
    }
    request_init["instance"] = {
        "name": "projects/sample1/locations/sample2/instances/sample3",
        "id": "id_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "machine_type": "machine_type_value",
        "state": 1,
        "hyperthreading_enabled": True,
        "labels": {},
        "luns": [
            {
                "name": "name_value",
                "id": "id_value",
                "state": 1,
                "size_gb": 739,
                "multiprotocol_type": 1,
                "storage_volume": "storage_volume_value",
                "shareable": True,
                "boot_lun": True,
                "storage_type": 1,
                "wwid": "wwid_value",
            }
        ],
        "networks": [
            {
                "name": "name_value",
                "id": "id_value",
                "type_": 1,
                "ip_address": "ip_address_value",
                "mac_address": ["mac_address_value1", "mac_address_value2"],
                "state": 1,
                "vlan_id": "vlan_id_value",
                "cidr": "cidr_value",
                "vrf": {
                    "name": "name_value",
                    "state": 1,
                    "qos_policy": {"bandwidth_gbps": 0.1472},
                    "vlan_attachments": [
                        {
                            "peer_vlan_id": 1256,
                            "peer_ip": "peer_ip_value",
                            "router_ip": "router_ip_value",
                        }
                    ],
                },
                "labels": {},
                "services_cidr": "services_cidr_value",
                "reservations": [
                    {
                        "start_address": "start_address_value",
                        "end_address": "end_address_value",
                        "note": "note_value",
                    }
                ],
            }
        ],
        "interactive_serial_console_enabled": True,
        "os_image": "os_image_value",
        "pod": "pod_value",
        "network_template": "network_template_value",
        "logical_interfaces": [
            {
                "logical_network_interfaces": [
                    {
                        "network": "network_value",
                        "ip_address": "ip_address_value",
                        "default_gateway": True,
                        "network_type": 1,
                        "id": "id_value",
                    }
                ],
                "name": "name_value",
                "interface_index": 1576,
            }
        ],
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
        client.update_instance(request)


def test_update_instance_rest_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "instance": {"name": "projects/sample1/locations/sample2/instances/sample3"}
        }

        # get truthy value for each flattened field
        mock_args = dict(
            instance=gcb_instance.Instance(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_instance(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{instance.name=projects/*/locations/*/instances/*}"
            % client.transport._host,
            args[1],
        )


def test_update_instance_rest_flattened_error(transport: str = "rest"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_instance(
            gcb_instance.UpdateInstanceRequest(),
            instance=gcb_instance.Instance(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_instance_rest_error():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        instance.ResetInstanceRequest,
        dict,
    ],
)
def test_reset_instance_rest(request_type):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/instances/sample3"}
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
        response = client.reset_instance(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_reset_instance_rest_required_fields(
    request_type=instance.ResetInstanceRequest,
):
    transport_class = transports.BareMetalSolutionRestTransport

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
    ).reset_instance._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).reset_instance._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = BareMetalSolutionClient(
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

            response = client.reset_instance(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_reset_instance_rest_unset_required_fields():
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.reset_instance._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_reset_instance_rest_interceptors(null_interceptor):
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.BareMetalSolutionRestInterceptor(),
    )
    client = BareMetalSolutionClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "post_reset_instance"
    ) as post, mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "pre_reset_instance"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = instance.ResetInstanceRequest.pb(instance.ResetInstanceRequest())
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

        request = instance.ResetInstanceRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.reset_instance(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_reset_instance_rest_bad_request(
    transport: str = "rest", request_type=instance.ResetInstanceRequest
):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/instances/sample3"}
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
        client.reset_instance(request)


def test_reset_instance_rest_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/instances/sample3"
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

        client.reset_instance(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{name=projects/*/locations/*/instances/*}:reset"
            % client.transport._host,
            args[1],
        )


def test_reset_instance_rest_flattened_error(transport: str = "rest"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.reset_instance(
            instance.ResetInstanceRequest(),
            name="name_value",
        )


def test_reset_instance_rest_error():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        instance.StartInstanceRequest,
        dict,
    ],
)
def test_start_instance_rest(request_type):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/instances/sample3"}
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
        response = client.start_instance(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_start_instance_rest_required_fields(
    request_type=instance.StartInstanceRequest,
):
    transport_class = transports.BareMetalSolutionRestTransport

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
    ).start_instance._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).start_instance._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = BareMetalSolutionClient(
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

            response = client.start_instance(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_start_instance_rest_unset_required_fields():
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.start_instance._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_start_instance_rest_interceptors(null_interceptor):
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.BareMetalSolutionRestInterceptor(),
    )
    client = BareMetalSolutionClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "post_start_instance"
    ) as post, mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "pre_start_instance"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = instance.StartInstanceRequest.pb(instance.StartInstanceRequest())
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

        request = instance.StartInstanceRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.start_instance(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_start_instance_rest_bad_request(
    transport: str = "rest", request_type=instance.StartInstanceRequest
):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/instances/sample3"}
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
        client.start_instance(request)


def test_start_instance_rest_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/instances/sample3"
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

        client.start_instance(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{name=projects/*/locations/*/instances/*}:start"
            % client.transport._host,
            args[1],
        )


def test_start_instance_rest_flattened_error(transport: str = "rest"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.start_instance(
            instance.StartInstanceRequest(),
            name="name_value",
        )


def test_start_instance_rest_error():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        instance.StopInstanceRequest,
        dict,
    ],
)
def test_stop_instance_rest(request_type):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/instances/sample3"}
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
        response = client.stop_instance(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_stop_instance_rest_required_fields(request_type=instance.StopInstanceRequest):
    transport_class = transports.BareMetalSolutionRestTransport

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
    ).stop_instance._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).stop_instance._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = BareMetalSolutionClient(
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

            response = client.stop_instance(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_stop_instance_rest_unset_required_fields():
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.stop_instance._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_stop_instance_rest_interceptors(null_interceptor):
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.BareMetalSolutionRestInterceptor(),
    )
    client = BareMetalSolutionClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "post_stop_instance"
    ) as post, mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "pre_stop_instance"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = instance.StopInstanceRequest.pb(instance.StopInstanceRequest())
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

        request = instance.StopInstanceRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.stop_instance(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_stop_instance_rest_bad_request(
    transport: str = "rest", request_type=instance.StopInstanceRequest
):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/instances/sample3"}
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
        client.stop_instance(request)


def test_stop_instance_rest_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/instances/sample3"
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

        client.stop_instance(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{name=projects/*/locations/*/instances/*}:stop"
            % client.transport._host,
            args[1],
        )


def test_stop_instance_rest_flattened_error(transport: str = "rest"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.stop_instance(
            instance.StopInstanceRequest(),
            name="name_value",
        )


def test_stop_instance_rest_error():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        gcb_instance.DetachLunRequest,
        dict,
    ],
)
def test_detach_lun_rest(request_type):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"instance": "projects/sample1/locations/sample2/instances/sample3"}
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
        response = client.detach_lun(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_detach_lun_rest_required_fields(request_type=gcb_instance.DetachLunRequest):
    transport_class = transports.BareMetalSolutionRestTransport

    request_init = {}
    request_init["instance"] = ""
    request_init["lun"] = ""
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
    ).detach_lun._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["instance"] = "instance_value"
    jsonified_request["lun"] = "lun_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).detach_lun._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "instance" in jsonified_request
    assert jsonified_request["instance"] == "instance_value"
    assert "lun" in jsonified_request
    assert jsonified_request["lun"] == "lun_value"

    client = BareMetalSolutionClient(
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

            response = client.detach_lun(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_detach_lun_rest_unset_required_fields():
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.detach_lun._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "instance",
                "lun",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_detach_lun_rest_interceptors(null_interceptor):
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.BareMetalSolutionRestInterceptor(),
    )
    client = BareMetalSolutionClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "post_detach_lun"
    ) as post, mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "pre_detach_lun"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gcb_instance.DetachLunRequest.pb(gcb_instance.DetachLunRequest())
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

        request = gcb_instance.DetachLunRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.detach_lun(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_detach_lun_rest_bad_request(
    transport: str = "rest", request_type=gcb_instance.DetachLunRequest
):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"instance": "projects/sample1/locations/sample2/instances/sample3"}
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
        client.detach_lun(request)


def test_detach_lun_rest_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "instance": "projects/sample1/locations/sample2/instances/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            instance="instance_value",
            lun="lun_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.detach_lun(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{instance=projects/*/locations/*/instances/*}:detachLun"
            % client.transport._host,
            args[1],
        )


def test_detach_lun_rest_flattened_error(transport: str = "rest"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.detach_lun(
            gcb_instance.DetachLunRequest(),
            instance="instance_value",
            lun="lun_value",
        )


def test_detach_lun_rest_error():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        volume.ListVolumesRequest,
        dict,
    ],
)
def test_list_volumes_rest(request_type):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = volume.ListVolumesResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = volume.ListVolumesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_volumes(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListVolumesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_volumes_rest_required_fields(request_type=volume.ListVolumesRequest):
    transport_class = transports.BareMetalSolutionRestTransport

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
    ).list_volumes._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_volumes._get_unset_required_fields(jsonified_request)
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

    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = volume.ListVolumesResponse()
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

            pb_return_value = volume.ListVolumesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_volumes(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_volumes_rest_unset_required_fields():
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_volumes._get_unset_required_fields({})
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
def test_list_volumes_rest_interceptors(null_interceptor):
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.BareMetalSolutionRestInterceptor(),
    )
    client = BareMetalSolutionClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "post_list_volumes"
    ) as post, mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "pre_list_volumes"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = volume.ListVolumesRequest.pb(volume.ListVolumesRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = volume.ListVolumesResponse.to_json(
            volume.ListVolumesResponse()
        )

        request = volume.ListVolumesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = volume.ListVolumesResponse()

        client.list_volumes(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_volumes_rest_bad_request(
    transport: str = "rest", request_type=volume.ListVolumesRequest
):
    client = BareMetalSolutionClient(
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
        client.list_volumes(request)


def test_list_volumes_rest_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = volume.ListVolumesResponse()

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
        pb_return_value = volume.ListVolumesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_volumes(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{parent=projects/*/locations/*}/volumes" % client.transport._host,
            args[1],
        )


def test_list_volumes_rest_flattened_error(transport: str = "rest"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_volumes(
            volume.ListVolumesRequest(),
            parent="parent_value",
        )


def test_list_volumes_rest_pager(transport: str = "rest"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            volume.ListVolumesResponse(
                volumes=[
                    volume.Volume(),
                    volume.Volume(),
                    volume.Volume(),
                ],
                next_page_token="abc",
            ),
            volume.ListVolumesResponse(
                volumes=[],
                next_page_token="def",
            ),
            volume.ListVolumesResponse(
                volumes=[
                    volume.Volume(),
                ],
                next_page_token="ghi",
            ),
            volume.ListVolumesResponse(
                volumes=[
                    volume.Volume(),
                    volume.Volume(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(volume.ListVolumesResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_volumes(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, volume.Volume) for i in results)

        pages = list(client.list_volumes(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        volume.GetVolumeRequest,
        dict,
    ],
)
def test_get_volume_rest(request_type):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/volumes/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = volume.Volume(
            name="name_value",
            id="id_value",
            storage_type=volume.Volume.StorageType.SSD,
            state=volume.Volume.State.CREATING,
            requested_size_gib=1917,
            current_size_gib=1710,
            emergency_size_gib=1898,
            auto_grown_size_gib=2032,
            remaining_space_gib=1974,
            snapshot_auto_delete_behavior=volume.Volume.SnapshotAutoDeleteBehavior.DISABLED,
            snapshot_enabled=True,
            pod="pod_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = volume.Volume.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_volume(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, volume.Volume)
    assert response.name == "name_value"
    assert response.id == "id_value"
    assert response.storage_type == volume.Volume.StorageType.SSD
    assert response.state == volume.Volume.State.CREATING
    assert response.requested_size_gib == 1917
    assert response.current_size_gib == 1710
    assert response.emergency_size_gib == 1898
    assert response.auto_grown_size_gib == 2032
    assert response.remaining_space_gib == 1974
    assert (
        response.snapshot_auto_delete_behavior
        == volume.Volume.SnapshotAutoDeleteBehavior.DISABLED
    )
    assert response.snapshot_enabled is True
    assert response.pod == "pod_value"


def test_get_volume_rest_required_fields(request_type=volume.GetVolumeRequest):
    transport_class = transports.BareMetalSolutionRestTransport

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
    ).get_volume._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_volume._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = volume.Volume()
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

            pb_return_value = volume.Volume.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_volume(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_volume_rest_unset_required_fields():
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_volume._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_volume_rest_interceptors(null_interceptor):
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.BareMetalSolutionRestInterceptor(),
    )
    client = BareMetalSolutionClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "post_get_volume"
    ) as post, mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "pre_get_volume"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = volume.GetVolumeRequest.pb(volume.GetVolumeRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = volume.Volume.to_json(volume.Volume())

        request = volume.GetVolumeRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = volume.Volume()

        client.get_volume(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_volume_rest_bad_request(
    transport: str = "rest", request_type=volume.GetVolumeRequest
):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/volumes/sample3"}
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
        client.get_volume(request)


def test_get_volume_rest_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = volume.Volume()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/locations/sample2/volumes/sample3"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = volume.Volume.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_volume(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{name=projects/*/locations/*/volumes/*}" % client.transport._host,
            args[1],
        )


def test_get_volume_rest_flattened_error(transport: str = "rest"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_volume(
            volume.GetVolumeRequest(),
            name="name_value",
        )


def test_get_volume_rest_error():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        gcb_volume.UpdateVolumeRequest,
        dict,
    ],
)
def test_update_volume_rest(request_type):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "volume": {"name": "projects/sample1/locations/sample2/volumes/sample3"}
    }
    request_init["volume"] = {
        "name": "projects/sample1/locations/sample2/volumes/sample3",
        "id": "id_value",
        "storage_type": 1,
        "state": 1,
        "requested_size_gib": 1917,
        "current_size_gib": 1710,
        "emergency_size_gib": 1898,
        "auto_grown_size_gib": 2032,
        "remaining_space_gib": 1974,
        "snapshot_reservation_detail": {
            "reserved_space_gib": 1884,
            "reserved_space_used_percent": 2859,
            "reserved_space_remaining_gib": 2933,
            "reserved_space_percent": 2331,
        },
        "snapshot_auto_delete_behavior": 1,
        "labels": {},
        "snapshot_enabled": True,
        "pod": "pod_value",
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
        response = client.update_volume(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_volume_rest_required_fields(
    request_type=gcb_volume.UpdateVolumeRequest,
):
    transport_class = transports.BareMetalSolutionRestTransport

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
    ).update_volume._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_volume._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = BareMetalSolutionClient(
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
                "method": "patch",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_volume(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_volume_rest_unset_required_fields():
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_volume._get_unset_required_fields({})
    assert set(unset_fields) == (set(("updateMask",)) & set(("volume",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_volume_rest_interceptors(null_interceptor):
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.BareMetalSolutionRestInterceptor(),
    )
    client = BareMetalSolutionClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "post_update_volume"
    ) as post, mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "pre_update_volume"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gcb_volume.UpdateVolumeRequest.pb(gcb_volume.UpdateVolumeRequest())
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

        request = gcb_volume.UpdateVolumeRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_volume(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_volume_rest_bad_request(
    transport: str = "rest", request_type=gcb_volume.UpdateVolumeRequest
):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "volume": {"name": "projects/sample1/locations/sample2/volumes/sample3"}
    }
    request_init["volume"] = {
        "name": "projects/sample1/locations/sample2/volumes/sample3",
        "id": "id_value",
        "storage_type": 1,
        "state": 1,
        "requested_size_gib": 1917,
        "current_size_gib": 1710,
        "emergency_size_gib": 1898,
        "auto_grown_size_gib": 2032,
        "remaining_space_gib": 1974,
        "snapshot_reservation_detail": {
            "reserved_space_gib": 1884,
            "reserved_space_used_percent": 2859,
            "reserved_space_remaining_gib": 2933,
            "reserved_space_percent": 2331,
        },
        "snapshot_auto_delete_behavior": 1,
        "labels": {},
        "snapshot_enabled": True,
        "pod": "pod_value",
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
        client.update_volume(request)


def test_update_volume_rest_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "volume": {"name": "projects/sample1/locations/sample2/volumes/sample3"}
        }

        # get truthy value for each flattened field
        mock_args = dict(
            volume=gcb_volume.Volume(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_volume(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{volume.name=projects/*/locations/*/volumes/*}"
            % client.transport._host,
            args[1],
        )


def test_update_volume_rest_flattened_error(transport: str = "rest"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_volume(
            gcb_volume.UpdateVolumeRequest(),
            volume=gcb_volume.Volume(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_volume_rest_error():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        gcb_volume.ResizeVolumeRequest,
        dict,
    ],
)
def test_resize_volume_rest(request_type):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"volume": "projects/sample1/locations/sample2/volumes/sample3"}
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
        response = client.resize_volume(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_resize_volume_rest_required_fields(
    request_type=gcb_volume.ResizeVolumeRequest,
):
    transport_class = transports.BareMetalSolutionRestTransport

    request_init = {}
    request_init["volume"] = ""
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
    ).resize_volume._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["volume"] = "volume_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).resize_volume._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "volume" in jsonified_request
    assert jsonified_request["volume"] == "volume_value"

    client = BareMetalSolutionClient(
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

            response = client.resize_volume(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_resize_volume_rest_unset_required_fields():
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.resize_volume._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("volume",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_resize_volume_rest_interceptors(null_interceptor):
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.BareMetalSolutionRestInterceptor(),
    )
    client = BareMetalSolutionClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "post_resize_volume"
    ) as post, mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "pre_resize_volume"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gcb_volume.ResizeVolumeRequest.pb(gcb_volume.ResizeVolumeRequest())
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

        request = gcb_volume.ResizeVolumeRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.resize_volume(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_resize_volume_rest_bad_request(
    transport: str = "rest", request_type=gcb_volume.ResizeVolumeRequest
):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"volume": "projects/sample1/locations/sample2/volumes/sample3"}
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
        client.resize_volume(request)


def test_resize_volume_rest_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "volume": "projects/sample1/locations/sample2/volumes/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            volume="volume_value",
            size_gib=844,
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.resize_volume(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{volume=projects/*/locations/*/volumes/*}:resize"
            % client.transport._host,
            args[1],
        )


def test_resize_volume_rest_flattened_error(transport: str = "rest"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.resize_volume(
            gcb_volume.ResizeVolumeRequest(),
            volume="volume_value",
            size_gib=844,
        )


def test_resize_volume_rest_error():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        network.ListNetworksRequest,
        dict,
    ],
)
def test_list_networks_rest(request_type):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = network.ListNetworksResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = network.ListNetworksResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_networks(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListNetworksPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_networks_rest_required_fields(request_type=network.ListNetworksRequest):
    transport_class = transports.BareMetalSolutionRestTransport

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
    ).list_networks._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_networks._get_unset_required_fields(jsonified_request)
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

    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = network.ListNetworksResponse()
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

            pb_return_value = network.ListNetworksResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_networks(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_networks_rest_unset_required_fields():
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_networks._get_unset_required_fields({})
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
def test_list_networks_rest_interceptors(null_interceptor):
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.BareMetalSolutionRestInterceptor(),
    )
    client = BareMetalSolutionClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "post_list_networks"
    ) as post, mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "pre_list_networks"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = network.ListNetworksRequest.pb(network.ListNetworksRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = network.ListNetworksResponse.to_json(
            network.ListNetworksResponse()
        )

        request = network.ListNetworksRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = network.ListNetworksResponse()

        client.list_networks(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_networks_rest_bad_request(
    transport: str = "rest", request_type=network.ListNetworksRequest
):
    client = BareMetalSolutionClient(
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
        client.list_networks(request)


def test_list_networks_rest_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = network.ListNetworksResponse()

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
        pb_return_value = network.ListNetworksResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_networks(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{parent=projects/*/locations/*}/networks" % client.transport._host,
            args[1],
        )


def test_list_networks_rest_flattened_error(transport: str = "rest"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_networks(
            network.ListNetworksRequest(),
            parent="parent_value",
        )


def test_list_networks_rest_pager(transport: str = "rest"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            network.ListNetworksResponse(
                networks=[
                    network.Network(),
                    network.Network(),
                    network.Network(),
                ],
                next_page_token="abc",
            ),
            network.ListNetworksResponse(
                networks=[],
                next_page_token="def",
            ),
            network.ListNetworksResponse(
                networks=[
                    network.Network(),
                ],
                next_page_token="ghi",
            ),
            network.ListNetworksResponse(
                networks=[
                    network.Network(),
                    network.Network(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(network.ListNetworksResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_networks(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, network.Network) for i in results)

        pages = list(client.list_networks(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        network.ListNetworkUsageRequest,
        dict,
    ],
)
def test_list_network_usage_rest(request_type):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"location": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = network.ListNetworkUsageResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = network.ListNetworkUsageResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_network_usage(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, network.ListNetworkUsageResponse)


def test_list_network_usage_rest_required_fields(
    request_type=network.ListNetworkUsageRequest,
):
    transport_class = transports.BareMetalSolutionRestTransport

    request_init = {}
    request_init["location"] = ""
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
    ).list_network_usage._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["location"] = "location_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_network_usage._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "location" in jsonified_request
    assert jsonified_request["location"] == "location_value"

    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = network.ListNetworkUsageResponse()
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

            pb_return_value = network.ListNetworkUsageResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_network_usage(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_network_usage_rest_unset_required_fields():
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_network_usage._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("location",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_network_usage_rest_interceptors(null_interceptor):
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.BareMetalSolutionRestInterceptor(),
    )
    client = BareMetalSolutionClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "post_list_network_usage"
    ) as post, mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "pre_list_network_usage"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = network.ListNetworkUsageRequest.pb(
            network.ListNetworkUsageRequest()
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
        req.return_value._content = network.ListNetworkUsageResponse.to_json(
            network.ListNetworkUsageResponse()
        )

        request = network.ListNetworkUsageRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = network.ListNetworkUsageResponse()

        client.list_network_usage(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_network_usage_rest_bad_request(
    transport: str = "rest", request_type=network.ListNetworkUsageRequest
):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"location": "projects/sample1/locations/sample2"}
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
        client.list_network_usage(request)


def test_list_network_usage_rest_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = network.ListNetworkUsageResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"location": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            location="location_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = network.ListNetworkUsageResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_network_usage(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{location=projects/*/locations/*}/networks:listNetworkUsage"
            % client.transport._host,
            args[1],
        )


def test_list_network_usage_rest_flattened_error(transport: str = "rest"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_network_usage(
            network.ListNetworkUsageRequest(),
            location="location_value",
        )


def test_list_network_usage_rest_error():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        network.GetNetworkRequest,
        dict,
    ],
)
def test_get_network_rest(request_type):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/networks/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = network.Network(
            name="name_value",
            id="id_value",
            type_=network.Network.Type.CLIENT,
            ip_address="ip_address_value",
            mac_address=["mac_address_value"],
            state=network.Network.State.PROVISIONING,
            vlan_id="vlan_id_value",
            cidr="cidr_value",
            services_cidr="services_cidr_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = network.Network.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_network(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, network.Network)
    assert response.name == "name_value"
    assert response.id == "id_value"
    assert response.type_ == network.Network.Type.CLIENT
    assert response.ip_address == "ip_address_value"
    assert response.mac_address == ["mac_address_value"]
    assert response.state == network.Network.State.PROVISIONING
    assert response.vlan_id == "vlan_id_value"
    assert response.cidr == "cidr_value"
    assert response.services_cidr == "services_cidr_value"


def test_get_network_rest_required_fields(request_type=network.GetNetworkRequest):
    transport_class = transports.BareMetalSolutionRestTransport

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
    ).get_network._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_network._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = network.Network()
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

            pb_return_value = network.Network.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_network(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_network_rest_unset_required_fields():
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_network._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_network_rest_interceptors(null_interceptor):
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.BareMetalSolutionRestInterceptor(),
    )
    client = BareMetalSolutionClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "post_get_network"
    ) as post, mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "pre_get_network"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = network.GetNetworkRequest.pb(network.GetNetworkRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = network.Network.to_json(network.Network())

        request = network.GetNetworkRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = network.Network()

        client.get_network(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_network_rest_bad_request(
    transport: str = "rest", request_type=network.GetNetworkRequest
):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/networks/sample3"}
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
        client.get_network(request)


def test_get_network_rest_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = network.Network()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/locations/sample2/networks/sample3"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = network.Network.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_network(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{name=projects/*/locations/*/networks/*}" % client.transport._host,
            args[1],
        )


def test_get_network_rest_flattened_error(transport: str = "rest"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_network(
            network.GetNetworkRequest(),
            name="name_value",
        )


def test_get_network_rest_error():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        gcb_network.UpdateNetworkRequest,
        dict,
    ],
)
def test_update_network_rest(request_type):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "network": {"name": "projects/sample1/locations/sample2/networks/sample3"}
    }
    request_init["network"] = {
        "name": "projects/sample1/locations/sample2/networks/sample3",
        "id": "id_value",
        "type_": 1,
        "ip_address": "ip_address_value",
        "mac_address": ["mac_address_value1", "mac_address_value2"],
        "state": 1,
        "vlan_id": "vlan_id_value",
        "cidr": "cidr_value",
        "vrf": {
            "name": "name_value",
            "state": 1,
            "qos_policy": {"bandwidth_gbps": 0.1472},
            "vlan_attachments": [
                {
                    "peer_vlan_id": 1256,
                    "peer_ip": "peer_ip_value",
                    "router_ip": "router_ip_value",
                }
            ],
        },
        "labels": {},
        "services_cidr": "services_cidr_value",
        "reservations": [
            {
                "start_address": "start_address_value",
                "end_address": "end_address_value",
                "note": "note_value",
            }
        ],
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
        response = client.update_network(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_network_rest_required_fields(
    request_type=gcb_network.UpdateNetworkRequest,
):
    transport_class = transports.BareMetalSolutionRestTransport

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
    ).update_network._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_network._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = BareMetalSolutionClient(
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
                "method": "patch",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_network(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_network_rest_unset_required_fields():
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_network._get_unset_required_fields({})
    assert set(unset_fields) == (set(("updateMask",)) & set(("network",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_network_rest_interceptors(null_interceptor):
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.BareMetalSolutionRestInterceptor(),
    )
    client = BareMetalSolutionClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "post_update_network"
    ) as post, mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "pre_update_network"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gcb_network.UpdateNetworkRequest.pb(
            gcb_network.UpdateNetworkRequest()
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

        request = gcb_network.UpdateNetworkRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_network(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_network_rest_bad_request(
    transport: str = "rest", request_type=gcb_network.UpdateNetworkRequest
):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "network": {"name": "projects/sample1/locations/sample2/networks/sample3"}
    }
    request_init["network"] = {
        "name": "projects/sample1/locations/sample2/networks/sample3",
        "id": "id_value",
        "type_": 1,
        "ip_address": "ip_address_value",
        "mac_address": ["mac_address_value1", "mac_address_value2"],
        "state": 1,
        "vlan_id": "vlan_id_value",
        "cidr": "cidr_value",
        "vrf": {
            "name": "name_value",
            "state": 1,
            "qos_policy": {"bandwidth_gbps": 0.1472},
            "vlan_attachments": [
                {
                    "peer_vlan_id": 1256,
                    "peer_ip": "peer_ip_value",
                    "router_ip": "router_ip_value",
                }
            ],
        },
        "labels": {},
        "services_cidr": "services_cidr_value",
        "reservations": [
            {
                "start_address": "start_address_value",
                "end_address": "end_address_value",
                "note": "note_value",
            }
        ],
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
        client.update_network(request)


def test_update_network_rest_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "network": {"name": "projects/sample1/locations/sample2/networks/sample3"}
        }

        # get truthy value for each flattened field
        mock_args = dict(
            network=gcb_network.Network(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_network(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{network.name=projects/*/locations/*/networks/*}"
            % client.transport._host,
            args[1],
        )


def test_update_network_rest_flattened_error(transport: str = "rest"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_network(
            gcb_network.UpdateNetworkRequest(),
            network=gcb_network.Network(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_network_rest_error():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        lun.GetLunRequest,
        dict,
    ],
)
def test_get_lun_rest(request_type):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/volumes/sample3/luns/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = lun.Lun(
            name="name_value",
            id="id_value",
            state=lun.Lun.State.CREATING,
            size_gb=739,
            multiprotocol_type=lun.Lun.MultiprotocolType.LINUX,
            storage_volume="storage_volume_value",
            shareable=True,
            boot_lun=True,
            storage_type=lun.Lun.StorageType.SSD,
            wwid="wwid_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = lun.Lun.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_lun(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, lun.Lun)
    assert response.name == "name_value"
    assert response.id == "id_value"
    assert response.state == lun.Lun.State.CREATING
    assert response.size_gb == 739
    assert response.multiprotocol_type == lun.Lun.MultiprotocolType.LINUX
    assert response.storage_volume == "storage_volume_value"
    assert response.shareable is True
    assert response.boot_lun is True
    assert response.storage_type == lun.Lun.StorageType.SSD
    assert response.wwid == "wwid_value"


def test_get_lun_rest_required_fields(request_type=lun.GetLunRequest):
    transport_class = transports.BareMetalSolutionRestTransport

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
    ).get_lun._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_lun._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = lun.Lun()
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

            pb_return_value = lun.Lun.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_lun(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_lun_rest_unset_required_fields():
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_lun._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_lun_rest_interceptors(null_interceptor):
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.BareMetalSolutionRestInterceptor(),
    )
    client = BareMetalSolutionClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "post_get_lun"
    ) as post, mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "pre_get_lun"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = lun.GetLunRequest.pb(lun.GetLunRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = lun.Lun.to_json(lun.Lun())

        request = lun.GetLunRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = lun.Lun()

        client.get_lun(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_lun_rest_bad_request(
    transport: str = "rest", request_type=lun.GetLunRequest
):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/volumes/sample3/luns/sample4"
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
        client.get_lun(request)


def test_get_lun_rest_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = lun.Lun()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/volumes/sample3/luns/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = lun.Lun.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_lun(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{name=projects/*/locations/*/volumes/*/luns/*}"
            % client.transport._host,
            args[1],
        )


def test_get_lun_rest_flattened_error(transport: str = "rest"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_lun(
            lun.GetLunRequest(),
            name="name_value",
        )


def test_get_lun_rest_error():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        lun.ListLunsRequest,
        dict,
    ],
)
def test_list_luns_rest(request_type):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/volumes/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = lun.ListLunsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = lun.ListLunsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_luns(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListLunsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_luns_rest_required_fields(request_type=lun.ListLunsRequest):
    transport_class = transports.BareMetalSolutionRestTransport

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
    ).list_luns._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_luns._get_unset_required_fields(jsonified_request)
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

    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = lun.ListLunsResponse()
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

            pb_return_value = lun.ListLunsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_luns(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_luns_rest_unset_required_fields():
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_luns._get_unset_required_fields({})
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
def test_list_luns_rest_interceptors(null_interceptor):
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.BareMetalSolutionRestInterceptor(),
    )
    client = BareMetalSolutionClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "post_list_luns"
    ) as post, mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "pre_list_luns"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = lun.ListLunsRequest.pb(lun.ListLunsRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = lun.ListLunsResponse.to_json(lun.ListLunsResponse())

        request = lun.ListLunsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = lun.ListLunsResponse()

        client.list_luns(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_luns_rest_bad_request(
    transport: str = "rest", request_type=lun.ListLunsRequest
):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/volumes/sample3"}
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
        client.list_luns(request)


def test_list_luns_rest_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = lun.ListLunsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/volumes/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = lun.ListLunsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_luns(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{parent=projects/*/locations/*/volumes/*}/luns"
            % client.transport._host,
            args[1],
        )


def test_list_luns_rest_flattened_error(transport: str = "rest"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_luns(
            lun.ListLunsRequest(),
            parent="parent_value",
        )


def test_list_luns_rest_pager(transport: str = "rest"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            lun.ListLunsResponse(
                luns=[
                    lun.Lun(),
                    lun.Lun(),
                    lun.Lun(),
                ],
                next_page_token="abc",
            ),
            lun.ListLunsResponse(
                luns=[],
                next_page_token="def",
            ),
            lun.ListLunsResponse(
                luns=[
                    lun.Lun(),
                ],
                next_page_token="ghi",
            ),
            lun.ListLunsResponse(
                luns=[
                    lun.Lun(),
                    lun.Lun(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(lun.ListLunsResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/volumes/sample3"
        }

        pager = client.list_luns(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, lun.Lun) for i in results)

        pages = list(client.list_luns(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        nfs_share.GetNfsShareRequest,
        dict,
    ],
)
def test_get_nfs_share_rest(request_type):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/nfsShares/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = nfs_share.NfsShare(
            name="name_value",
            nfs_share_id="nfs_share_id_value",
            state=nfs_share.NfsShare.State.PROVISIONED,
            volume="volume_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = nfs_share.NfsShare.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_nfs_share(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, nfs_share.NfsShare)
    assert response.name == "name_value"
    assert response.nfs_share_id == "nfs_share_id_value"
    assert response.state == nfs_share.NfsShare.State.PROVISIONED
    assert response.volume == "volume_value"


def test_get_nfs_share_rest_required_fields(request_type=nfs_share.GetNfsShareRequest):
    transport_class = transports.BareMetalSolutionRestTransport

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
    ).get_nfs_share._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_nfs_share._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = nfs_share.NfsShare()
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

            pb_return_value = nfs_share.NfsShare.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_nfs_share(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_nfs_share_rest_unset_required_fields():
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_nfs_share._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_nfs_share_rest_interceptors(null_interceptor):
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.BareMetalSolutionRestInterceptor(),
    )
    client = BareMetalSolutionClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "post_get_nfs_share"
    ) as post, mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "pre_get_nfs_share"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = nfs_share.GetNfsShareRequest.pb(nfs_share.GetNfsShareRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = nfs_share.NfsShare.to_json(nfs_share.NfsShare())

        request = nfs_share.GetNfsShareRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = nfs_share.NfsShare()

        client.get_nfs_share(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_nfs_share_rest_bad_request(
    transport: str = "rest", request_type=nfs_share.GetNfsShareRequest
):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/nfsShares/sample3"}
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
        client.get_nfs_share(request)


def test_get_nfs_share_rest_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = nfs_share.NfsShare()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/nfsShares/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = nfs_share.NfsShare.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_nfs_share(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{name=projects/*/locations/*/nfsShares/*}" % client.transport._host,
            args[1],
        )


def test_get_nfs_share_rest_flattened_error(transport: str = "rest"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_nfs_share(
            nfs_share.GetNfsShareRequest(),
            name="name_value",
        )


def test_get_nfs_share_rest_error():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        nfs_share.ListNfsSharesRequest,
        dict,
    ],
)
def test_list_nfs_shares_rest(request_type):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = nfs_share.ListNfsSharesResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = nfs_share.ListNfsSharesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_nfs_shares(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListNfsSharesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_nfs_shares_rest_required_fields(
    request_type=nfs_share.ListNfsSharesRequest,
):
    transport_class = transports.BareMetalSolutionRestTransport

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
    ).list_nfs_shares._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_nfs_shares._get_unset_required_fields(jsonified_request)
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

    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = nfs_share.ListNfsSharesResponse()
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

            pb_return_value = nfs_share.ListNfsSharesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_nfs_shares(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_nfs_shares_rest_unset_required_fields():
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_nfs_shares._get_unset_required_fields({})
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
def test_list_nfs_shares_rest_interceptors(null_interceptor):
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.BareMetalSolutionRestInterceptor(),
    )
    client = BareMetalSolutionClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "post_list_nfs_shares"
    ) as post, mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "pre_list_nfs_shares"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = nfs_share.ListNfsSharesRequest.pb(nfs_share.ListNfsSharesRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = nfs_share.ListNfsSharesResponse.to_json(
            nfs_share.ListNfsSharesResponse()
        )

        request = nfs_share.ListNfsSharesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = nfs_share.ListNfsSharesResponse()

        client.list_nfs_shares(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_nfs_shares_rest_bad_request(
    transport: str = "rest", request_type=nfs_share.ListNfsSharesRequest
):
    client = BareMetalSolutionClient(
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
        client.list_nfs_shares(request)


def test_list_nfs_shares_rest_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = nfs_share.ListNfsSharesResponse()

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
        pb_return_value = nfs_share.ListNfsSharesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_nfs_shares(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{parent=projects/*/locations/*}/nfsShares" % client.transport._host,
            args[1],
        )


def test_list_nfs_shares_rest_flattened_error(transport: str = "rest"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_nfs_shares(
            nfs_share.ListNfsSharesRequest(),
            parent="parent_value",
        )


def test_list_nfs_shares_rest_pager(transport: str = "rest"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            nfs_share.ListNfsSharesResponse(
                nfs_shares=[
                    nfs_share.NfsShare(),
                    nfs_share.NfsShare(),
                    nfs_share.NfsShare(),
                ],
                next_page_token="abc",
            ),
            nfs_share.ListNfsSharesResponse(
                nfs_shares=[],
                next_page_token="def",
            ),
            nfs_share.ListNfsSharesResponse(
                nfs_shares=[
                    nfs_share.NfsShare(),
                ],
                next_page_token="ghi",
            ),
            nfs_share.ListNfsSharesResponse(
                nfs_shares=[
                    nfs_share.NfsShare(),
                    nfs_share.NfsShare(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(nfs_share.ListNfsSharesResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_nfs_shares(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, nfs_share.NfsShare) for i in results)

        pages = list(client.list_nfs_shares(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        gcb_nfs_share.UpdateNfsShareRequest,
        dict,
    ],
)
def test_update_nfs_share_rest(request_type):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "nfs_share": {"name": "projects/sample1/locations/sample2/nfsShares/sample3"}
    }
    request_init["nfs_share"] = {
        "name": "projects/sample1/locations/sample2/nfsShares/sample3",
        "nfs_share_id": "nfs_share_id_value",
        "state": 1,
        "volume": "volume_value",
        "allowed_clients": [
            {
                "network": "network_value",
                "share_ip": "share_ip_value",
                "allowed_clients_cidr": "allowed_clients_cidr_value",
                "mount_permissions": 1,
                "allow_dev": True,
                "allow_suid": True,
                "no_root_squash": True,
            }
        ],
        "labels": {},
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
        response = client.update_nfs_share(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_nfs_share_rest_required_fields(
    request_type=gcb_nfs_share.UpdateNfsShareRequest,
):
    transport_class = transports.BareMetalSolutionRestTransport

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
    ).update_nfs_share._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_nfs_share._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = BareMetalSolutionClient(
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
                "method": "patch",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_nfs_share(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_nfs_share_rest_unset_required_fields():
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_nfs_share._get_unset_required_fields({})
    assert set(unset_fields) == (set(("updateMask",)) & set(("nfsShare",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_nfs_share_rest_interceptors(null_interceptor):
    transport = transports.BareMetalSolutionRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.BareMetalSolutionRestInterceptor(),
    )
    client = BareMetalSolutionClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "post_update_nfs_share"
    ) as post, mock.patch.object(
        transports.BareMetalSolutionRestInterceptor, "pre_update_nfs_share"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gcb_nfs_share.UpdateNfsShareRequest.pb(
            gcb_nfs_share.UpdateNfsShareRequest()
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

        request = gcb_nfs_share.UpdateNfsShareRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_nfs_share(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_nfs_share_rest_bad_request(
    transport: str = "rest", request_type=gcb_nfs_share.UpdateNfsShareRequest
):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "nfs_share": {"name": "projects/sample1/locations/sample2/nfsShares/sample3"}
    }
    request_init["nfs_share"] = {
        "name": "projects/sample1/locations/sample2/nfsShares/sample3",
        "nfs_share_id": "nfs_share_id_value",
        "state": 1,
        "volume": "volume_value",
        "allowed_clients": [
            {
                "network": "network_value",
                "share_ip": "share_ip_value",
                "allowed_clients_cidr": "allowed_clients_cidr_value",
                "mount_permissions": 1,
                "allow_dev": True,
                "allow_suid": True,
                "no_root_squash": True,
            }
        ],
        "labels": {},
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
        client.update_nfs_share(request)


def test_update_nfs_share_rest_flattened():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "nfs_share": {
                "name": "projects/sample1/locations/sample2/nfsShares/sample3"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            nfs_share=gcb_nfs_share.NfsShare(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_nfs_share(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v2/{nfs_share.name=projects/*/locations/*/nfsShares/*}"
            % client.transport._host,
            args[1],
        )


def test_update_nfs_share_rest_flattened_error(transport: str = "rest"):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_nfs_share(
            gcb_nfs_share.UpdateNfsShareRequest(),
            nfs_share=gcb_nfs_share.NfsShare(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_nfs_share_rest_error():
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.BareMetalSolutionGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = BareMetalSolutionClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.BareMetalSolutionGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = BareMetalSolutionClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.BareMetalSolutionGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = BareMetalSolutionClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = BareMetalSolutionClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.BareMetalSolutionGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = BareMetalSolutionClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.BareMetalSolutionGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = BareMetalSolutionClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.BareMetalSolutionGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.BareMetalSolutionGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.BareMetalSolutionGrpcTransport,
        transports.BareMetalSolutionGrpcAsyncIOTransport,
        transports.BareMetalSolutionRestTransport,
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
    transport = BareMetalSolutionClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.BareMetalSolutionGrpcTransport,
    )


def test_bare_metal_solution_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.BareMetalSolutionTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_bare_metal_solution_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.bare_metal_solution_v2.services.bare_metal_solution.transports.BareMetalSolutionTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.BareMetalSolutionTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_instances",
        "get_instance",
        "update_instance",
        "reset_instance",
        "start_instance",
        "stop_instance",
        "detach_lun",
        "list_volumes",
        "get_volume",
        "update_volume",
        "resize_volume",
        "list_networks",
        "list_network_usage",
        "get_network",
        "update_network",
        "get_lun",
        "list_luns",
        "get_nfs_share",
        "list_nfs_shares",
        "update_nfs_share",
        "get_location",
        "list_locations",
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


def test_bare_metal_solution_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.bare_metal_solution_v2.services.bare_metal_solution.transports.BareMetalSolutionTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.BareMetalSolutionTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_bare_metal_solution_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.bare_metal_solution_v2.services.bare_metal_solution.transports.BareMetalSolutionTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.BareMetalSolutionTransport()
        adc.assert_called_once()


def test_bare_metal_solution_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        BareMetalSolutionClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.BareMetalSolutionGrpcTransport,
        transports.BareMetalSolutionGrpcAsyncIOTransport,
    ],
)
def test_bare_metal_solution_transport_auth_adc(transport_class):
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
        transports.BareMetalSolutionGrpcTransport,
        transports.BareMetalSolutionGrpcAsyncIOTransport,
        transports.BareMetalSolutionRestTransport,
    ],
)
def test_bare_metal_solution_transport_auth_gdch_credentials(transport_class):
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
        (transports.BareMetalSolutionGrpcTransport, grpc_helpers),
        (transports.BareMetalSolutionGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_bare_metal_solution_transport_create_channel(transport_class, grpc_helpers):
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
            "baremetalsolution.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="baremetalsolution.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.BareMetalSolutionGrpcTransport,
        transports.BareMetalSolutionGrpcAsyncIOTransport,
    ],
)
def test_bare_metal_solution_grpc_transport_client_cert_source_for_mtls(
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


def test_bare_metal_solution_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.BareMetalSolutionRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


def test_bare_metal_solution_rest_lro_client():
    client = BareMetalSolutionClient(
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
def test_bare_metal_solution_host_no_port(transport_name):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="baremetalsolution.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "baremetalsolution.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://baremetalsolution.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_bare_metal_solution_host_with_port(transport_name):
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="baremetalsolution.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "baremetalsolution.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://baremetalsolution.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_bare_metal_solution_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = BareMetalSolutionClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = BareMetalSolutionClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.list_instances._session
    session2 = client2.transport.list_instances._session
    assert session1 != session2
    session1 = client1.transport.get_instance._session
    session2 = client2.transport.get_instance._session
    assert session1 != session2
    session1 = client1.transport.update_instance._session
    session2 = client2.transport.update_instance._session
    assert session1 != session2
    session1 = client1.transport.reset_instance._session
    session2 = client2.transport.reset_instance._session
    assert session1 != session2
    session1 = client1.transport.start_instance._session
    session2 = client2.transport.start_instance._session
    assert session1 != session2
    session1 = client1.transport.stop_instance._session
    session2 = client2.transport.stop_instance._session
    assert session1 != session2
    session1 = client1.transport.detach_lun._session
    session2 = client2.transport.detach_lun._session
    assert session1 != session2
    session1 = client1.transport.list_volumes._session
    session2 = client2.transport.list_volumes._session
    assert session1 != session2
    session1 = client1.transport.get_volume._session
    session2 = client2.transport.get_volume._session
    assert session1 != session2
    session1 = client1.transport.update_volume._session
    session2 = client2.transport.update_volume._session
    assert session1 != session2
    session1 = client1.transport.resize_volume._session
    session2 = client2.transport.resize_volume._session
    assert session1 != session2
    session1 = client1.transport.list_networks._session
    session2 = client2.transport.list_networks._session
    assert session1 != session2
    session1 = client1.transport.list_network_usage._session
    session2 = client2.transport.list_network_usage._session
    assert session1 != session2
    session1 = client1.transport.get_network._session
    session2 = client2.transport.get_network._session
    assert session1 != session2
    session1 = client1.transport.update_network._session
    session2 = client2.transport.update_network._session
    assert session1 != session2
    session1 = client1.transport.get_lun._session
    session2 = client2.transport.get_lun._session
    assert session1 != session2
    session1 = client1.transport.list_luns._session
    session2 = client2.transport.list_luns._session
    assert session1 != session2
    session1 = client1.transport.get_nfs_share._session
    session2 = client2.transport.get_nfs_share._session
    assert session1 != session2
    session1 = client1.transport.list_nfs_shares._session
    session2 = client2.transport.list_nfs_shares._session
    assert session1 != session2
    session1 = client1.transport.update_nfs_share._session
    session2 = client2.transport.update_nfs_share._session
    assert session1 != session2


def test_bare_metal_solution_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.BareMetalSolutionGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_bare_metal_solution_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.BareMetalSolutionGrpcAsyncIOTransport(
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
        transports.BareMetalSolutionGrpcTransport,
        transports.BareMetalSolutionGrpcAsyncIOTransport,
    ],
)
def test_bare_metal_solution_transport_channel_mtls_with_client_cert_source(
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
        transports.BareMetalSolutionGrpcTransport,
        transports.BareMetalSolutionGrpcAsyncIOTransport,
    ],
)
def test_bare_metal_solution_transport_channel_mtls_with_adc(transport_class):
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


def test_bare_metal_solution_grpc_lro_client():
    client = BareMetalSolutionClient(
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


def test_bare_metal_solution_grpc_lro_async_client():
    client = BareMetalSolutionAsyncClient(
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


def test_instance_path():
    project = "squid"
    location = "clam"
    instance = "whelk"
    expected = "projects/{project}/locations/{location}/instances/{instance}".format(
        project=project,
        location=location,
        instance=instance,
    )
    actual = BareMetalSolutionClient.instance_path(project, location, instance)
    assert expected == actual


def test_parse_instance_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "instance": "nudibranch",
    }
    path = BareMetalSolutionClient.instance_path(**expected)

    # Check that the path construction is reversible.
    actual = BareMetalSolutionClient.parse_instance_path(path)
    assert expected == actual


def test_lun_path():
    project = "cuttlefish"
    location = "mussel"
    volume = "winkle"
    lun = "nautilus"
    expected = (
        "projects/{project}/locations/{location}/volumes/{volume}/luns/{lun}".format(
            project=project,
            location=location,
            volume=volume,
            lun=lun,
        )
    )
    actual = BareMetalSolutionClient.lun_path(project, location, volume, lun)
    assert expected == actual


def test_parse_lun_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
        "volume": "squid",
        "lun": "clam",
    }
    path = BareMetalSolutionClient.lun_path(**expected)

    # Check that the path construction is reversible.
    actual = BareMetalSolutionClient.parse_lun_path(path)
    assert expected == actual


def test_network_path():
    project = "whelk"
    location = "octopus"
    network = "oyster"
    expected = "projects/{project}/locations/{location}/networks/{network}".format(
        project=project,
        location=location,
        network=network,
    )
    actual = BareMetalSolutionClient.network_path(project, location, network)
    assert expected == actual


def test_parse_network_path():
    expected = {
        "project": "nudibranch",
        "location": "cuttlefish",
        "network": "mussel",
    }
    path = BareMetalSolutionClient.network_path(**expected)

    # Check that the path construction is reversible.
    actual = BareMetalSolutionClient.parse_network_path(path)
    assert expected == actual


def test_nfs_share_path():
    project = "winkle"
    location = "nautilus"
    nfs_share = "scallop"
    expected = "projects/{project}/locations/{location}/nfsShares/{nfs_share}".format(
        project=project,
        location=location,
        nfs_share=nfs_share,
    )
    actual = BareMetalSolutionClient.nfs_share_path(project, location, nfs_share)
    assert expected == actual


def test_parse_nfs_share_path():
    expected = {
        "project": "abalone",
        "location": "squid",
        "nfs_share": "clam",
    }
    path = BareMetalSolutionClient.nfs_share_path(**expected)

    # Check that the path construction is reversible.
    actual = BareMetalSolutionClient.parse_nfs_share_path(path)
    assert expected == actual


def test_server_network_template_path():
    project = "whelk"
    location = "octopus"
    server_network_template = "oyster"
    expected = "projects/{project}/locations/{location}/serverNetworkTemplate/{server_network_template}".format(
        project=project,
        location=location,
        server_network_template=server_network_template,
    )
    actual = BareMetalSolutionClient.server_network_template_path(
        project, location, server_network_template
    )
    assert expected == actual


def test_parse_server_network_template_path():
    expected = {
        "project": "nudibranch",
        "location": "cuttlefish",
        "server_network_template": "mussel",
    }
    path = BareMetalSolutionClient.server_network_template_path(**expected)

    # Check that the path construction is reversible.
    actual = BareMetalSolutionClient.parse_server_network_template_path(path)
    assert expected == actual


def test_volume_path():
    project = "winkle"
    location = "nautilus"
    volume = "scallop"
    expected = "projects/{project}/locations/{location}/volumes/{volume}".format(
        project=project,
        location=location,
        volume=volume,
    )
    actual = BareMetalSolutionClient.volume_path(project, location, volume)
    assert expected == actual


def test_parse_volume_path():
    expected = {
        "project": "abalone",
        "location": "squid",
        "volume": "clam",
    }
    path = BareMetalSolutionClient.volume_path(**expected)

    # Check that the path construction is reversible.
    actual = BareMetalSolutionClient.parse_volume_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "whelk"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = BareMetalSolutionClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "octopus",
    }
    path = BareMetalSolutionClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = BareMetalSolutionClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "oyster"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = BareMetalSolutionClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nudibranch",
    }
    path = BareMetalSolutionClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = BareMetalSolutionClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "cuttlefish"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = BareMetalSolutionClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "mussel",
    }
    path = BareMetalSolutionClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = BareMetalSolutionClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "winkle"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = BareMetalSolutionClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nautilus",
    }
    path = BareMetalSolutionClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = BareMetalSolutionClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "scallop"
    location = "abalone"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = BareMetalSolutionClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "squid",
        "location": "clam",
    }
    path = BareMetalSolutionClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = BareMetalSolutionClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.BareMetalSolutionTransport, "_prep_wrapped_messages"
    ) as prep:
        client = BareMetalSolutionClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.BareMetalSolutionTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = BareMetalSolutionClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = BareMetalSolutionAsyncClient(
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
    client = BareMetalSolutionClient(
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
    client = BareMetalSolutionClient(
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
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict({"name": "projects/sample1"}, request)

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
    client = BareMetalSolutionClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1"}
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


def test_list_locations(transport: str = "grpc"):
    client = BareMetalSolutionClient(
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
    client = BareMetalSolutionAsyncClient(
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
    client = BareMetalSolutionClient(
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
    client = BareMetalSolutionAsyncClient(
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
    client = BareMetalSolutionClient(
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
    client = BareMetalSolutionAsyncClient(
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
    client = BareMetalSolutionClient(
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
    client = BareMetalSolutionAsyncClient(
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
    client = BareMetalSolutionClient(credentials=ga_credentials.AnonymousCredentials())

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
    client = BareMetalSolutionAsyncClient(
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
    client = BareMetalSolutionClient(
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
    client = BareMetalSolutionAsyncClient(
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
        client = BareMetalSolutionClient(
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
        client = BareMetalSolutionClient(
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
        (BareMetalSolutionClient, transports.BareMetalSolutionGrpcTransport),
        (
            BareMetalSolutionAsyncClient,
            transports.BareMetalSolutionGrpcAsyncIOTransport,
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
